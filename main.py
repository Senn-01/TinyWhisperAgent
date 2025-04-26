import os
import tempfile
import wave
import time
import threading
import pyaudio
import numpy as np
import openai
from datetime import datetime
import soundfile as sf
import sounddevice as sd
from pathlib import Path
import subprocess
import ffmpeg
import math

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
TEMP_AUDIO_FILE = "temp_recording.wav"
RECORD_DIR = "record"
TRANSCRIPT_DIR = "transcript"
IMPROVED_TRANSCRIPT_DIR = "improved-transcript"  # New directory for improved transcripts
MAX_FILE_SIZE = 24 * 1024 * 1024  # 24MB (slightly below the 25MB limit)

# Create necessary directories if they don't exist
os.makedirs(RECORD_DIR, exist_ok=True)
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
os.makedirs(IMPROVED_TRANSCRIPT_DIR, exist_ok=True)  # Create improved transcript directory

class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.thread = None

    def start_recording(self):
        """Start audio recording in a separate thread."""
        self.is_recording = True
        self.frames = []
        self.stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        def record():
            while self.is_recording:
                data = self.stream.read(CHUNK)
                self.frames.append(data)
        
        self.thread = threading.Thread(target=record)
        self.thread.start()
        print("Recording started... Press 'f' to finish recording.")

    def stop_recording(self):
        """Stop the recording and save the audio file."""
        if not self.is_recording:
            return None
            
        self.is_recording = False
        if self.thread:
            self.thread.join()
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        # Save the recorded audio to a WAV file
        wf = wave.open(TEMP_AUDIO_FILE, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        
        print(f"Recording saved to {TEMP_AUDIO_FILE}")
        return TEMP_AUDIO_FILE

    def close(self):
        """Clean up resources."""
        self.audio.terminate()


def transcribe_audio(file_path):
    """Transcribe the audio file using OpenAI's Whisper API."""
    try:
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > MAX_FILE_SIZE:
            print(f"File size ({file_size / (1024*1024):.2f} MB) exceeds Whisper's limit. Chunking file...")
            return transcribe_large_file(file_path)
        
        with open(file_path, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None


def transcribe_large_file(file_path):
    """Transcribe a large audio file by splitting it into chunks."""
    try:
        # Get audio duration
        probe = ffmpeg.probe(file_path)
        duration = float(probe['format']['duration'])
        file_size = os.path.getsize(file_path)
        
        # Calculate number of chunks needed (target 15MB per chunk to stay safely under the 25MB limit)
        # Use more chunks than theoretically needed to account for compression differences
        target_chunk_size = 15 * 1024 * 1024  # 15MB
        estimated_chunks = math.ceil(file_size / target_chunk_size) * 1.5  # Add 50% more chunks for safety
        chunk_duration = duration / max(1, estimated_chunks)
        num_chunks = math.ceil(duration / chunk_duration)
        
        print(f"Splitting file into approximately {num_chunks} chunks...")
        
        all_transcripts = []
        temp_files = []
        
        for i in range(num_chunks):
            start_time = i * chunk_duration
            end_time = min((i + 1) * chunk_duration, duration)
            
            # Create temporary file for this chunk
            chunk_file = f"temp_chunk_{i}.wav"
            temp_files.append(chunk_file)
            
            # Extract chunk using ffmpeg
            stream = ffmpeg.input(file_path, ss=start_time, t=end_time-start_time)
            stream = ffmpeg.output(stream, chunk_file, acodec='pcm_s16le', ac=1, ar=16000)
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True, overwrite_output=True)
            
            # Check if chunk is still too large
            chunk_size = os.path.getsize(chunk_file)
            if chunk_size > MAX_FILE_SIZE:
                print(f"Chunk {i+1} is still too large ({chunk_size/(1024*1024):.2f} MB). Subdividing...")
                
                # Remove the large chunk file
                os.remove(chunk_file)
                temp_files.remove(chunk_file)
                
                # Subdivide this portion of audio into smaller chunks
                sub_chunk_duration = (end_time - start_time) / 3  # Split into 3 sub-chunks
                for j in range(3):
                    sub_start = start_time + j * sub_chunk_duration
                    sub_end = min(start_time + (j + 1) * sub_chunk_duration, end_time)
                    
                    sub_chunk_file = f"temp_chunk_{i}_{j}.wav"
                    temp_files.append(sub_chunk_file)
                    
                    sub_stream = ffmpeg.input(file_path, ss=sub_start, t=sub_end-sub_start)
                    sub_stream = ffmpeg.output(sub_stream, sub_chunk_file, acodec='pcm_s16le', ac=1, ar=16000)
                    ffmpeg.run(sub_stream, capture_stdout=True, capture_stderr=True, overwrite_output=True)
                    
                    # Check if sub-chunk is small enough
                    sub_chunk_size = os.path.getsize(sub_chunk_file)
                    if sub_chunk_size <= MAX_FILE_SIZE:
                        # Transcribe sub-chunk
                        print(f"Transcribing sub-chunk {i+1}.{j+1}...")
                        with open(sub_chunk_file, "rb") as audio_file:
                            sub_chunk_transcript = openai.audio.transcriptions.create(
                                model="whisper-1",
                                file=audio_file
                            )
                        all_transcripts.append(sub_chunk_transcript.text)
                    else:
                        print(f"Warning: Sub-chunk {i+1}.{j+1} is still too large ({sub_chunk_size/(1024*1024):.2f} MB). Skipping.")
            else:
                # Transcribe chunk
                print(f"Transcribing chunk {i+1}/{num_chunks} ({chunk_size/(1024*1024):.2f} MB)...")
                with open(chunk_file, "rb") as audio_file:
                    chunk_transcript = openai.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )
                all_transcripts.append(chunk_transcript.text)
        
        # Combine all transcripts
        full_transcript = " ".join(all_transcripts)
        
        # Clean up temporary files
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        return full_transcript
    
    except Exception as e:
        print(f"Error during chunked transcription: {e}")
        # Clean up any temporary files
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        return None


def save_transcript_to_markdown(transcript, source_file=None, suffix=""):
    """Save the transcript to a markdown file in the transcript directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create filename based on source file if available
    if source_file:
        source_name = os.path.splitext(os.path.basename(source_file))[0]
        filename = f"{source_name}_{timestamp}{suffix}.md"
    else:
        filename = f"transcript_{timestamp}{suffix}.md"
    
    file_path = os.path.join(TRANSCRIPT_DIR, filename)
    
    with open(file_path, "w") as f:
        f.write(f"# Audio Transcript - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        if source_file:
            f.write(f"Source: {os.path.basename(source_file)}\n\n")
        f.write(transcript)
    
    print(f"Transcript saved to {file_path}")
    return file_path


def convert_to_wav(input_file):
    """Convert audio file to WAV format if needed."""
    if input_file.lower().endswith('.wav'):
        return input_file
        
    output_file = "temp_converted.wav"
    try:
        # Use ffmpeg to convert the file
        stream = ffmpeg.input(input_file)
        stream = ffmpeg.output(stream, output_file, acodec='pcm_s16le', ac=1, ar=16000)
        ffmpeg.run(stream, capture_stdout=True, capture_stderr=True, overwrite_output=True)
        return output_file
    except ffmpeg.Error as e:
        print(f"Error converting file: {e.stderr.decode()}")
        return None
    except Exception as e:
        print(f"Error converting file: {e}")
        return None


def list_audio_files():
    """List all audio files in the record directory."""
    audio_files = []
    for file in os.listdir(RECORD_DIR):
        if file.lower().endswith(('.mp3', '.m4a', '.wav', '.flac', '.ogg', '.aac', '.wma', '.mka')):
            audio_files.append(file)
    return audio_files


def get_summary(transcript):
    """Generate a summary of the transcript using OpenAI's GPT-4.1."""
    try:
        print("Generating summary...")
        response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts key points from transcripts. Create a concise summary with bullet points highlighting the most important information."},
                {"role": "user", "content": f"Please provide a summary of the following transcript, extracting the key points and main ideas:\n\n{transcript}"}
            ],
            temperature=0.3,
            max_tokens=16384    
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating summary: {e}")
        return None


def get_cleaner_transcript(transcript):
    """Generate a cleaner version of the transcript using OpenAI's GPT-4.1."""
    try:
        print("Generating cleaner transcript...")
        response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that cleans up transcripts. Remove filler words, repetitions, false starts, and other verbal noise while preserving the original meaning and flow of the conversation."},
                {"role": "user", "content": f"Please clean up the following transcript by removing filler words, repetitions, false starts, and other verbal noise. Preserve the original meaning and flow of the conversation:\n\n{transcript}"}
            ],
            temperature=0.3,
            max_tokens=16384
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating cleaner transcript: {e}")
        return None


def generate_image_from_transcript(transcript):
    """Generate an image based on transcript content using OpenAI's GPT-Image-1."""
    try:
        print("Generating image from transcript content...")
        
        # First summarize the key visual elements from the transcript
        summary_response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts key visual elements from text. Create a concise, visually descriptive summary of the main scene, objects, people, or concepts described in the following text. Focus only on the most important visually representable elements."},
                {"role": "user", "content": f"Please extract the most important visual elements from this transcript that could be turned into an image:\n\n{transcript}"}
            ],
            temperature=0.3,
            max_tokens=1024
        )
        
        visual_summary = summary_response.choices[0].message.content
        
        # Generate image creation prompt
        image_prompt_response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant specialized in creating detailed image generation prompts. Your task is to create a vivid, detailed prompt for an image generation model based on key visual elements provided. Focus on describing a single cohesive scene with visual details like color, composition, lighting, style, and mood. Keep the prompt under 200 words."},
                {"role": "user", "content": f"Create a detailed image generation prompt based on these key visual elements:\n\n{visual_summary}"}
            ],
            temperature=0.7,
            max_tokens=512
        )
        
        image_prompt = image_prompt_response.choices[0].message.content
        print(f"Image generation prompt: {image_prompt}")
        
        # Generate the image using GPT-Image-1
        image_result = openai.images.generate(
            model="gpt-image-1",
            prompt=image_prompt,
            size="1024x1024",
            quality="standard"
        )
        
        # Save the image
        if hasattr(image_result.data[0], 'url'):
            # If URL is returned (typically when using the API in production)
            image_url = image_result.data[0].url
            print(f"Image URL: {image_url}")
            return image_url
        elif hasattr(image_result.data[0], 'b64_json'):
            # If base64 data is returned
            import base64
            from PIL import Image
            from io import BytesIO
            import datetime
            
            # Create timestamp for filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Directory for generated images
            image_dir = "generated_images"
            os.makedirs(image_dir, exist_ok=True)
            
            # Save the image to a file
            image_filename = f"{image_dir}/transcript_image_{timestamp}.png"
            
            # Decode and save image
            image_data = base64.b64decode(image_result.data[0].b64_json)
            image = Image.open(BytesIO(image_data))
            image.save(image_filename)
            
            print(f"Image saved to {image_filename}")
            return image_filename
        else:
            print("No image data returned in the expected format")
            return None
            
    except Exception as e:
        print(f"Error generating image: {e}")
        return None


def post_transcription_menu(transcript, source_file=None):
    """Display a menu of options after transcription is complete."""
    while True:
        print("\nPost-Transcription Options:")
        print("1. Save transcript as is")
        print("2. Generate summary (key points)")
        print("3. Generate cleaner transcript")
        print("4. Both summary and cleaner transcript")
        print("5. Generate image from transcript")
        print("6. Return to main menu")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == "1":
            # Save transcript as is
            save_transcript_to_markdown(transcript, source_file)
            return
        
        elif choice == "2":
            # Generate summary
            summary = get_summary(transcript)
            if summary:
                print("\nSummary:")
                print(summary)
                save_transcript_to_markdown(summary, source_file, "_summary")
        
        elif choice == "3":
            # Generate cleaner transcript
            cleaner = get_cleaner_transcript(transcript)
            if cleaner:
                print("\nCleaner Transcript:")
                print(cleaner)
                save_transcript_to_markdown(cleaner, source_file, "_clean")
        
        elif choice == "4":
            # Generate both summary and cleaner transcript
            summary = get_summary(transcript)
            if summary:
                print("\nSummary:")
                print(summary)
                save_transcript_to_markdown(summary, source_file, "_summary")
            
            cleaner = get_cleaner_transcript(transcript)
            if cleaner:
                print("\nCleaner Transcript:")
                print(cleaner)
                save_transcript_to_markdown(cleaner, source_file, "_clean")
        
        elif choice == "5":
            # Generate image from transcript
            image_path = generate_image_from_transcript(transcript)
            if image_path:
                print(f"\nImage generated: {image_path}")
        
        elif choice == "6":
            # Return to main menu
            return
        
        else:
            print("Invalid choice. Please try again.")


def handle_file_transcription():
    """Handle transcription of an existing audio file."""
    audio_files = list_audio_files()
    
    if not audio_files:
        print(f"\nNo audio files found in the '{RECORD_DIR}' directory.")
        print("Supported formats: .mp3, .m4a, .wav, .flac, .ogg, .aac, .wma, .mka")
        return
    
    print("\nAvailable audio files:")
    for i, file in enumerate(audio_files, 1):
        file_path = os.path.join(RECORD_DIR, file)
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
        print(f"{i}. {file} ({file_size:.2f} MB)")
    
    try:
        choice = int(input("\nEnter the number of the file to transcribe: ").strip())
        if choice < 1 or choice > len(audio_files):
            print("Invalid choice.")
            return
        
        file_name = audio_files[choice - 1]
        file_path = os.path.join(RECORD_DIR, file_name)
        
        print(f"\nProcessing: {file_name}")
        print("Converting file to WAV format if needed...")
        wav_file = convert_to_wav(file_path)
        
        if not wav_file:
            print("Error: Could not process the audio file.")
            return
            
        print("Transcribing audio...")
        transcript = transcribe_audio(wav_file)
        
        if transcript:
            print("\nTranscript:")
            print(transcript)
            
            # Show post-transcription menu
            post_transcription_menu(transcript, file_path)
        
        # Clean up temporary file if it was converted
        if wav_file != file_path and os.path.exists(wav_file):
            os.remove(wav_file)
    
    except ValueError:
        print("Please enter a valid number.")


def handle_live_recording():
    """Handle live audio recording and transcription."""
    recorder = AudioRecorder()
    
    try:
        recorder.start_recording()
        
        # Wait for user to finish recording
        while True:
            if input().strip().lower() == 'f':
                break
        
        audio_file = recorder.stop_recording()
        if audio_file:
            print("Transcribing audio...")
            transcript = transcribe_audio(audio_file)
            
            if transcript:
                print("\nTranscript:")
                print(transcript)
                
                # Show post-transcription menu
                post_transcription_menu(transcript)
    
    finally:
        recorder.close()
        # Clean up temporary audio file
        if os.path.exists(TEMP_AUDIO_FILE):
            os.remove(TEMP_AUDIO_FILE)


def list_transcripts():
    """List all transcript files in the transcript directory."""
    transcript_files = []
    for file in os.listdir(TRANSCRIPT_DIR):
        if file.lower().endswith('.md'):
            transcript_files.append(file)
    return transcript_files


def get_transcript_content(file_path):
    """Read the content of a transcript file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Try to extract just the transcript part (skip the header)
    lines = content.split('\n')
    transcript_start = 0
    
    # Find where actual transcript begins (after headers)
    for i, line in enumerate(lines):
        if line.startswith('# Audio Transcript') or line.startswith('Source:'):
            transcript_start = i + 1
    
    # Skip empty lines
    while transcript_start < len(lines) and not lines[transcript_start].strip():
        transcript_start += 1
    
    # Return just the transcript portion
    if transcript_start < len(lines):
        return '\n'.join(lines[transcript_start:])
    
    # If parsing fails, return the whole content
    return content


def ask_questions_about_transcript(transcript):
    """Ask questions about a transcript using OpenAI's GPT-4.1."""
    print("\nWhat would you like to know about this transcript?")
    print("Examples:")
    print("- Summarize this transcript")
    print("- What are the key points?")
    print("- Who are the main speakers?")
    print("- What decisions were made?")
    print("- What action items were mentioned?")
    
    question = input("\nEnter your question: ").strip()
    
    if not question:
        print("No question provided.")
        return None
    
    try:
        print(f"Processing your question: '{question}'...")
        response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes transcripts and provides accurate, concise information about them."},
                {"role": "user", "content": f"Here is a transcript:\n\n{transcript}\n\nQuestion: {question}"}
            ],
            temperature=0.3,
            max_tokens=16384
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error processing question: {e}")
        return None


def reformat_transcript(transcript):
    """Reformat a transcript using OpenAI's GPT-4.1."""
    print("\nHow would you like to reformat this transcript?")
    print("1. Cleaner transcript (remove filler words and verbal noise)")
    print("2. Bullet point summary")
    print("3. Q&A format (extract questions and answers)")
    print("4. Speaker-separated format")
    print("5. Simplified language version")
    print("6. Structured format with sections and headings")
    print("7. Extract actionable items")
    print("8. Custom format (describe what you want)")
    
    choice = input("\nEnter your choice (1-8): ").strip()
    
    system_prompts = {
        "1": "You are a transcript editor that removes filler words, repetitions, false starts, and other verbal noise while preserving the original meaning and flow of the conversation.",
        "2": "You are a transcript editor that converts a transcript into a well-organized bullet point list capturing all the important points.",
        "3": "You are a transcript editor that identifies all questions and answers in a transcript and formats them in a clean Q&A format.",
        "4": "You are a transcript editor that identifies different speakers in a transcript and clearly separates their contributions.",
        "5": "You are a transcript editor that simplifies the language in a transcript, making it more accessible and easier to understand.",
        "6": "You are a transcript editor that adds a clear structure to a transcript with appropriate headings and sections based on the content.",
        "7": "You are a transcript editor that extracts all actionable items, tasks, or commitments mentioned in a transcript.",
        "8": "You are a transcript editor that reformats transcripts according to specific user requests."
    }
    
    user_prompts = {
        "1": "Please clean up the following transcript by removing filler words, repetitions, false starts, and other verbal noise. Preserve the original meaning and flow of the conversation.",
        "2": "Please convert this transcript into a well-organized bullet point list that captures all the important points.",
        "3": "Please identify all questions and answers in this transcript and format them in a clean Q&A format.",
        "4": "Please identify different speakers in this transcript and clearly separate their contributions.",
        "5": "Please simplify the language in this transcript, making it more accessible and easier to understand.",
        "6": "Please add a clear structure to this transcript with appropriate headings and sections based on the content.",
        "7": "Please extract all actionable items, tasks, or commitments mentioned in this transcript.",
        "8": "Please describe how you would like the transcript to be reformatted:"
    }
    
    if choice not in user_prompts:
        print("Invalid choice.")
        return None
    
    user_prompt = user_prompts[choice]
    system_prompt = system_prompts[choice]
    
    # For custom format, get the user's description
    if choice == "8":
        custom_request = input(user_prompt).strip()
        if not custom_request:
            print("No formatting request provided.")
            return None
        user_prompt = f"Please reformat this transcript according to the following request: {custom_request}"
    
    try:
        print("Reformatting transcript...")
        response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{user_prompt}\n\n{transcript}"}
            ],
            temperature=0.3,
            max_tokens=16384    
        )
        
        formatted_result = response.choices[0].message.content
        
        # Get format names for file naming
        format_names = {
            "1": "clean",
            "2": "bullet",
            "3": "qa",
            "4": "speakers",
            "5": "simplified",
            "6": "structured",
            "7": "actions",
            "8": "custom"
        }
        
        return formatted_result, format_names[choice]
    except Exception as e:
        print(f"Error reformatting transcript: {e}")
        return None, None


def handle_transcript_interaction():
    """Handle interaction with existing transcripts."""
    transcript_files = list_transcripts()
    
    if not transcript_files:
        print(f"\nNo transcript files found in the '{TRANSCRIPT_DIR}' directory.")
        return
    
    print("\nAvailable transcripts:")
    for i, file in enumerate(transcript_files, 1):
        print(f"{i}. {file}")
    
    try:
        choice = int(input("\nEnter the number of the transcript to interact with: ").strip())
        if choice < 1 or choice > len(transcript_files):
            print("Invalid choice.")
            return
        
        file_name = transcript_files[choice - 1]
        file_path = os.path.join(TRANSCRIPT_DIR, file_name)
        
        # Read the transcript content
        transcript = get_transcript_content(file_path)
        if not transcript:
            print("Error: Could not read the transcript file.")
            return
        
        print("\nTranscript Interaction Options:")
        print("1. Ask questions about the transcript")
        print("2. Reformat the transcript")
        print("3. Generate image from transcript")
        print("4. Return to main menu")
        
        interaction_choice = input("Enter your choice (1-4): ").strip()
        
        if interaction_choice == "1":
            # Handle questions about the transcript
            answer = ask_questions_about_transcript(transcript)
            if answer:
                print("\nAnswer:")
                print(answer)
                
                # Ask if the user wants to save the answer
                save_choice = input("\nWould you like to save this answer? (y/n): ").strip().lower()
                if save_choice == 'y':
                    # Create a filename for the answer
                    base_name = os.path.splitext(file_name)[0]
                    question_text = input("\nEnter a short label for this answer (for the filename): ").strip()
                    if not question_text:
                        question_text = "qa"
                    
                    # Remove invalid characters from filename
                    question_text = "".join(c for c in question_text if c.isalnum() or c in " _-").strip()
                    question_text = question_text.replace(" ", "_")
                    
                    answer_filename = f"{base_name}_{question_text}.md"
                    answer_path = os.path.join(IMPROVED_TRANSCRIPT_DIR, answer_filename)
                    
                    with open(answer_path, "w") as f:
                        f.write(f"# Question Answer - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                        f.write(f"Source: {file_name}\n\n")
                        f.write(f"**Question:** {question}\n\n")
                        f.write("**Answer:**\n\n")
                        f.write(answer)
                    
                    print(f"Answer saved to {answer_path}")
        
        elif interaction_choice == "2":
            # Handle transcript reformatting
            formatted_result, format_type = reformat_transcript(transcript)
            if formatted_result and format_type:
                print("\nReformatted Transcript:")
                print(formatted_result)
                
                # Ask if the user wants to save the reformatted transcript
                save_choice = input("\nWould you like to save this reformatted transcript? (y/n): ").strip().lower()
                if save_choice == 'y':
                    # Create a filename for the reformatted transcript
                    base_name = os.path.splitext(file_name)[0]
                    formatted_filename = f"{base_name}_{format_type}.md"
                    formatted_path = os.path.join(IMPROVED_TRANSCRIPT_DIR, formatted_filename)
                    
                    with open(formatted_path, "w") as f:
                        f.write(f"# Reformatted Transcript - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                        f.write(f"Source: {file_name}\n\n")
                        f.write(formatted_result)
                    
                    print(f"Reformatted transcript saved to {formatted_path}")
        
        elif interaction_choice == "3":
            # Generate image from transcript
            image_path = generate_image_from_transcript(transcript)
            if image_path:
                print(f"\nImage generated: {image_path}")
                
                # Create a record in the improved transcript directory linking to the image
                base_name = os.path.splitext(file_name)[0]
                image_record_filename = f"{base_name}_image_reference.md"
                image_record_path = os.path.join(IMPROVED_TRANSCRIPT_DIR, image_record_filename)
                
                with open(image_record_path, "w") as f:
                    f.write(f"# Generated Image - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write(f"Source Transcript: {file_name}\n\n")
                    f.write(f"Image Path: {image_path}\n\n")
                    
                    # If it's a URL, add Markdown image link
                    if image_path.startswith("http"):
                        f.write(f"![Generated Image]({image_path})\n")
                    else:
                        f.write(f"![Generated Image](../{image_path})\n")
                
                print(f"Image reference saved to {image_record_path}")
        
        elif interaction_choice == "4":
            # Return to main menu
            return
        
        else:
            print("Invalid choice.")
    
    except ValueError:
        print("Please enter a valid number.")


def main():
    print("Welcome to the Whisper Transcription App!")
    print("Make sure you have set your OpenAI API key.")
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        api_key = input("Please enter your OpenAI API key: ")
        os.environ["OPENAI_API_KEY"] = api_key
    
    while True:
        print("\nMenu:")
        print("1. Record new audio")
        print("2. Transcribe existing audio file")
        print("3. Interact with existing transcripts")
        print("4. Quit")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            handle_live_recording()
        elif choice == "2":
            handle_file_transcription()
        elif choice == "3":
            handle_transcript_interaction()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
