import os
import time
import openai
import json
from typing import Optional, Dict, Any, List, Tuple, Union
from datetime import datetime

# Constants
TRANSCRIPTS_DIR = "data/transcripts"

# Create necessary directories if they don't exist
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

def transcribe_audio(audio_file_path: str, model: str = "whisper-1") -> Optional[Dict[str, Any]]:
    """
    Transcribe an audio file using OpenAI's Whisper API.
    
    Args:
        audio_file_path: Path to the audio file to transcribe
        model: Whisper model to use (default: "whisper-1")
        
    Returns:
        Optional[Dict[str, Any]]: The transcription result or None if transcription failed
    """
    if not os.path.exists(audio_file_path):
        print(f"Error: File {audio_file_path} not found.")
        return None
        
    try:
        print(f"Transcribing {os.path.basename(audio_file_path)} using whisper-1 model...")
        start_time = time.time()
        
        # Always use text response format (no timestamps needed for simplified version)
        response_format = "text"
        
        with open(audio_file_path, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format=response_format
            )
        
        elapsed_time = time.time() - start_time
        print(f"Transcription completed in {elapsed_time:.2f} seconds.")
        
        # Process response
        result = {
            "text": transcript.text if hasattr(transcript, "text") else transcript,
            "model_used": "whisper-1"
        }
        
        # Save the transcript to a file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transcript_{timestamp}.txt"
        filepath = os.path.join(TRANSCRIPTS_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(result["text"])
            
        print(f"Transcript saved to {filepath}")
        
        return result
        
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

def list_transcripts() -> List[str]:
    """
    List available transcript files.
    
    Returns:
        List[str]: List of transcript filenames with numbering
    """
    # Get all files in transcripts directory
    transcript_files = [f for f in os.listdir(TRANSCRIPTS_DIR) if f.endswith('.txt')]
    
    # Sort files by creation time (newest first)
    transcript_files.sort(key=lambda x: os.path.getctime(os.path.join(TRANSCRIPTS_DIR, x)), reverse=True)
    
    # Create numbered list
    numbered_files = []
    for i, file in enumerate(transcript_files, 1):
        file_path = os.path.join(TRANSCRIPTS_DIR, file)
        size_kb = os.path.getsize(file_path) / 1024
        timestamp = datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
        numbered_files.append(f"{i}. {file} ({size_kb:.1f} KB, {timestamp})")
    
    return numbered_files

def get_transcript_content(index: int) -> Optional[str]:
    """
    Get the content of a transcript file by index.
    
    Args:
        index: Index of the transcript file
        
    Returns:
        Optional[str]: Content of the transcript file or None if not found
    """
    try:
        # Get all transcript files
        transcript_files = [f for f in os.listdir(TRANSCRIPTS_DIR) if f.endswith('.txt')]
        
        # Sort files by creation time (newest first)
        transcript_files.sort(key=lambda x: os.path.getctime(os.path.join(TRANSCRIPTS_DIR, x)), reverse=True)
        
        # Check if index is valid
        if index < 1 or index > len(transcript_files):
            print(f"Invalid index: {index}. Valid range is 1-{len(transcript_files)}.")
            return None
            
        # Get the file at the specified index
        file = transcript_files[index - 1]
        file_path = os.path.join(TRANSCRIPTS_DIR, file)
        
        # Read the file content
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        return content
        
    except Exception as e:
        print(f"Error getting transcript content: {e}")
        return None

def get_transcript_file_path(index: int) -> Optional[str]:
    """
    Get the file path of a transcript file by index.
    
    Args:
        index: Index of the transcript file
        
    Returns:
        Optional[str]: Path to the transcript file or None if not found
    """
    try:
        # Get all transcript files
        transcript_files = [f for f in os.listdir(TRANSCRIPTS_DIR) if f.endswith('.txt')]
        
        # Sort files by creation time (newest first)
        transcript_files.sort(key=lambda x: os.path.getctime(os.path.join(TRANSCRIPTS_DIR, x)), reverse=True)
        
        # Check if index is valid
        if index < 1 or index > len(transcript_files):
            print(f"Invalid index: {index}. Valid range is 1-{len(transcript_files)}.")
            return None
            
        # Get the file at the specified index
        file = transcript_files[index - 1]
        file_path = os.path.join(TRANSCRIPTS_DIR, file)
        
        return file_path
        
    except Exception as e:
        print(f"Error getting transcript file path: {e}")
        return None