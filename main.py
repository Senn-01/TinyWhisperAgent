import os
import sys
import argparse
import openai
from typing import Optional, List, Dict, Any
from datetime import datetime

# Import modules
import audio
import transcription
import processors
import image_gen

def load_api_key() -> bool:
    """
    Load the OpenAI API key from environment variable.
    
    Returns:
        bool: True if API key was loaded successfully, False otherwise
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set your OpenAI API key with:")
        print("    export OPENAI_API_KEY='your-api-key'")
        return False
        
    openai.api_key = api_key
    return True


def display_main_menu() -> None:
    """Display the main menu options."""
    print("\n=== Whisper Transcription Tool ===")
    print("1. Record Audio")
    print("2. Transcribe Audio File")
    print("3. Process Transcript")
    print("4. Generate Image")
    print("5. File Management")
    print("0. Exit")


def display_process_menu() -> None:
    """Display the transcript processing menu options."""
    print("\n=== Process Transcript ===")
    print("1. Generate Summary")
    print("2. Extract Key Points")
    print("3. Extract Action Items")
    print("4. Reformat Transcript")
    print("5. Translate Transcript")
    print("6. Analyze Sentiment")
    print("0. Back to Main Menu")


def display_file_menu() -> None:
    """Display the file management menu options."""
    print("\n=== File Management ===")
    print("1. List Audio Files")
    print("2. List Transcript Files")
    print("3. List Image Files")
    print("4. Delete File")
    print("0. Back to Main Menu")


def record_audio_workflow() -> None:
    """Handle the audio recording workflow."""
    try:
        print("\n=== Record Audio ===")
        print("How long would you like to record? (in seconds, 0 for manual stop)")
        duration_input = input("Duration: ")
        
        try:
            duration = int(duration_input)
        except ValueError:
            print("Invalid input. Using manual stop.")
            duration = 0
            
        audio_file = audio.record_audio(duration)
        
        if audio_file:
            print(f"Recording saved to: {audio_file}")
            
            # Ask if user wants to transcribe the recording
            transcribe_now = input("Would you like to transcribe this recording now? (y/n): ").lower()
            if transcribe_now == 'y':
                transcribe_audio_workflow(audio_file)
        
    except KeyboardInterrupt:
        print("\nRecording interrupted.")
    except Exception as e:
        print(f"Error in recording workflow: {e}")


def transcribe_audio_workflow(file_path: Optional[str] = None) -> None:
    """
    Handle the audio transcription workflow.
    
    Args:
        file_path: Optional path to audio file to transcribe
    """
    try:
        print("\n=== Transcribe Audio ===")
        
        # If file path not provided, let user choose from available files
        if not file_path:
            audio_files = audio.list_audio_files()
            
            if not audio_files:
                print("No audio files found.")
                return
                
            print("\nAvailable audio files:")
            for file in audio_files:
                print(file)
                
            file_index = input("\nEnter the number of the file to transcribe (or 0 to cancel): ")
            
            try:
                index = int(file_index)
                if index == 0:
                    return
                file_path = audio.get_audio_file_path(index)
            except ValueError:
                print("Invalid input.")
                return
                
            if not file_path:
                return
        
        # Transcribe the audio file
        transcript = transcription.transcribe_audio(file_path)
        
        if transcript:
            print("\nTranscription completed successfully.")
            print("\nTranscript preview:")
            print("-" * 50)
            # Show first 150 characters of transcript with "..." if longer
            preview = transcript[:150] + ("..." if len(transcript) > 150 else "")
            print(preview)
            print("-" * 50)
            
            # Ask if user wants to process the transcript
            process_now = input("Would you like to process this transcript now? (y/n): ").lower()
            if process_now == 'y':
                process_transcript_workflow()
        
    except Exception as e:
        print(f"Error in transcription workflow: {e}")


def process_transcript_workflow() -> None:
    """Handle the transcript processing workflow."""
    try:
        # List available transcripts
        transcript_files = transcription.list_transcripts()
        
        if not transcript_files:
            print("No transcript files found.")
            return
            
        print("\nAvailable transcript files:")
        for file in transcript_files:
            print(file)
            
        file_index = input("\nEnter the number of the transcript to process (or 0 to cancel): ")
        
        try:
            index = int(file_index)
            if index == 0:
                return
            transcript = transcription.get_transcript_content(index)
        except ValueError:
            print("Invalid input.")
            return
            
        if not transcript:
            return
            
        # Display processing options
        while True:
            display_process_menu()
            choice = input("Enter your choice: ")
            
            if choice == '0':
                break
            elif choice == '1':
                summary = processors.get_summary(transcript)
                if summary:
                    print("\nSummary:")
                    print("-" * 50)
                    print(summary)
                    print("-" * 50)
            elif choice == '2':
                key_points = processors.get_key_points(transcript)
                if key_points:
                    print("\nKey Points:")
                    print("-" * 50)
                    print(key_points)
                    print("-" * 50)
            elif choice == '3':
                action_items = processors.get_action_items(transcript)
                if action_items:
                    print("\nAction Items:")
                    print("-" * 50)
                    print(action_items)
                    print("-" * 50)
            elif choice == '4':
                print("\nAvailable formats:")
                print("1. Clean (grammar fixes, punctuation)")
                print("2. Paragraphs (organized into paragraphs)")
                print("3. Structured (with headings and sections)")
                print("4. Q&A (question and answer format)")
                print("5. Minutes (meeting minutes format)")
                print("6. Narrative (story-like format)")
                
                format_choice = input("Choose a format (1-6): ")
                format_map = {
                    '1': 'clean',
                    '2': 'paragraphs',
                    '3': 'structured',
                    '4': 'qa',
                    '5': 'minutes',
                    '6': 'narrative'
                }
                
                format_type = format_map.get(format_choice, 'clean')
                reformatted = processors.reformat_transcript(transcript, format_type)
                
                if reformatted:
                    print("\nReformatted Transcript:")
                    print("-" * 50)
                    print(reformatted[:300] + "..." if len(reformatted) > 300 else reformatted)
                    print("-" * 50)
                    print(f"Full reformatted transcript saved to file.")
            elif choice == '5':
                target_language = input("Enter target language: ")
                translated = processors.translate_transcript(transcript, target_language)
                
                if translated:
                    print("\nTranslated Transcript:")
                    print("-" * 50)
                    print(translated[:300] + "..." if len(translated) > 300 else translated)
                    print("-" * 50)
                    print(f"Full translation saved to file.")
            elif choice == '6':
                sentiment = processors.analyze_sentiment(transcript)
                
                if sentiment:
                    print("\nSentiment Analysis:")
                    print("-" * 50)
                    print(sentiment)
                    print("-" * 50)
            else:
                print("Invalid choice. Please try again.")
        
    except Exception as e:
        print(f"Error in processing workflow: {e}")


def generate_image_workflow() -> None:
    """Handle the image generation workflow."""
    try:
        print("\n=== Generate Image ===")
        print("1. Generate from transcript")
        print("2. Generate from custom prompt")
        print("0. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == '0':
            return
        elif choice == '1':
            # List available transcripts
            transcript_files = transcription.list_transcripts()
            
            if not transcript_files:
                print("No transcript files found.")
                return
                
            print("\nAvailable transcript files:")
            for file in transcript_files:
                print(file)
                
            file_index = input("\nEnter the number of the transcript to use (or 0 to cancel): ")
            
            try:
                index = int(file_index)
                if index == 0:
                    return
                transcript = transcription.get_transcript_content(index)
            except ValueError:
                print("Invalid input.")
                return
                
            if not transcript:
                return
            
            # Ask for quality
            print("\nSelect image quality:")
            print("1. Standard")
            print("2. HD")
            quality_choice = input("Enter your choice (default is Standard): ")
            quality = "hd" if quality_choice == "2" else "standard"
                
            # Generate image from transcript
            image_path = image_gen.generate_image_from_transcript(transcript, quality=quality)
            
            if image_path:
                print(f"\nImage generated and saved to: {image_path}")
                
        elif choice == '2':
            # Generate from custom prompt
            prompt = input("\nEnter your image generation prompt: ")
            
            if not prompt:
                print("No prompt provided.")
                return
            
            # Ask for quality
            print("\nSelect image quality:")
            print("1. Standard")
            print("2. HD")
            quality_choice = input("Enter your choice (default is Standard): ")
            quality = "hd" if quality_choice == "2" else "standard"
            
            # Ask for style
            print("\nSelect image style:")
            print("1. Vivid")
            print("2. Natural")
            style_choice = input("Enter your choice (default is Vivid): ")
            style = "natural" if style_choice == "2" else "vivid"
                
            image_path = image_gen.generate_image_from_prompt(prompt, quality=quality, style=style)
            
            if image_path:
                print(f"\nImage generated and saved to: {image_path}")
        else:
            print("Invalid choice.")
        
    except Exception as e:
        print(f"Error in image generation workflow: {e}")


def file_management_workflow() -> None:
    """Handle the file management workflow."""
    try:
        while True:
            display_file_menu()
            choice = input("Enter your choice: ")
            
            if choice == '0':
                break
            elif choice == '1':
                # List audio files
                audio_files = audio.list_audio_files()
                
                if not audio_files:
                    print("No audio files found.")
                else:
                    print("\nAvailable audio files:")
                    for file in audio_files:
                        print(file)
            elif choice == '2':
                # List transcript files
                transcript_files = transcription.list_transcripts()
                
                if not transcript_files:
                    print("No transcript files found.")
                else:
                    print("\nAvailable transcript files:")
                    for file in transcript_files:
                        print(file)
            elif choice == '3':
                # List image files
                image_files = image_gen.list_images()
                
                if not image_files:
                    print("No image files found.")
                else:
                    print("\nAvailable image files:")
                    for file in image_files:
                        print(file)
            elif choice == '4':
                # Delete file
                print("\nWhat type of file would you like to delete?")
                print("1. Audio file")
                print("2. Transcript file")
                print("3. Image file")
                
                file_type = input("Enter your choice: ")
                
                if file_type == '1':
                    # Delete audio file
                    audio_files = audio.list_audio_files()
                    
                    if not audio_files:
                        print("No audio files found.")
                        continue
                        
                    print("\nAvailable audio files:")
                    for file in audio_files:
                        print(file)
                        
                    file_index = input("\nEnter the number of the file to delete (or 0 to cancel): ")
                    
                    try:
                        index = int(file_index)
                        if index == 0:
                            continue
                        file_path = audio.get_audio_file_path(index)
                    except ValueError:
                        print("Invalid input.")
                        continue
                        
                    if file_path and os.path.exists(file_path):
                        confirm = input(f"Are you sure you want to delete {os.path.basename(file_path)}? (y/n): ").lower()
                        if confirm == 'y':
                            if audio.delete_audio_file(file_path):
                                print("File deleted successfully.")
                elif file_type == '2':
                    # Delete transcript file
                    transcript_files = transcription.list_transcripts()
                    
                    if not transcript_files:
                        print("No transcript files found.")
                        continue
                        
                    print("\nAvailable transcript files:")
                    for file in transcript_files:
                        print(file)
                        
                    file_index = input("\nEnter the number of the file to delete (or 0 to cancel): ")
                    
                    try:
                        index = int(file_index)
                        if index == 0:
                            continue
                        file_path = transcription.get_transcript_file_path(index)
                    except ValueError:
                        print("Invalid input.")
                        continue
                        
                    if file_path and os.path.exists(file_path):
                        confirm = input(f"Are you sure you want to delete {os.path.basename(file_path)}? (y/n): ").lower()
                        if confirm == 'y':
                            try:
                                os.remove(file_path)
                                print("File deleted successfully.")
                            except Exception as e:
                                print(f"Error deleting file: {e}")
                elif file_type == '3':
                    # Delete image file
                    image_files = image_gen.list_images()
                    
                    if not image_files:
                        print("No image files found.")
                        continue
                        
                    print("\nAvailable image files:")
                    for file in image_files:
                        print(file)
                        
                    file_index = input("\nEnter the number of the file to delete (or 0 to cancel): ")
                    
                    try:
                        index = int(file_index)
                        if index == 0:
                            continue
                        file_path = image_gen.get_image_path(index)
                    except ValueError:
                        print("Invalid input.")
                        continue
                        
                    if file_path and os.path.exists(file_path):
                        confirm = input(f"Are you sure you want to delete {os.path.basename(file_path)}? (y/n): ").lower()
                        if confirm == 'y':
                            try:
                                os.remove(file_path)
                                print("File deleted successfully.")
                            except Exception as e:
                                print(f"Error deleting file: {e}")
                else:
                    print("Invalid choice.")
            else:
                print("Invalid choice. Please try again.")
        
    except Exception as e:
        print(f"Error in file management workflow: {e}")


def main() -> None:
    """Main application entry point."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Whisper Transcription Tool")
    parser.add_argument("--record", action="store_true", help="Record audio")
    parser.add_argument("--transcribe", metavar="FILE", help="Transcribe audio file")
    parser.add_argument("--duration", type=int, default=0, help="Recording duration in seconds (0 for manual stop)")
    args = parser.parse_args()
    
    # Load OpenAI API key
    if not load_api_key():
        sys.exit(1)
        
    # Handle command-line actions
    if args.record:
        audio.record_audio(args.duration)
        sys.exit(0)
    elif args.transcribe:
        if os.path.exists(args.transcribe):
            transcription.transcribe_audio(args.transcribe)
        else:
            print(f"Error: File {args.transcribe} not found.")
        sys.exit(0)
    
    # Main application loop
    try:
        while True:
            display_main_menu()
            choice = input("Enter your choice: ")
            
            if choice == '0':
                print("Exiting...")
                break
            elif choice == '1':
                record_audio_workflow()
            elif choice == '2':
                transcribe_audio_workflow()
            elif choice == '3':
                process_transcript_workflow()
            elif choice == '4':
                generate_image_workflow()
            elif choice == '5':
                file_management_workflow()
            else:
                print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
