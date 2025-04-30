import os
import wave
import threading
import pyaudio
import numpy as np
import soundfile as sf
import sounddevice as sd
import ffmpeg
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime
import time

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
TEMP_AUDIO_FILE = "temp_recording.wav"
RECORDINGS_DIR = "data/recordings"

# Create necessary directories if they don't exist
os.makedirs(RECORDINGS_DIR, exist_ok=True)

class AudioRecorder:
    """Class for handling audio recording functionality."""
    
    def __init__(self) -> None:
        """Initialize the audio recorder."""
        self.is_recording: bool = False
        self.frames: List[bytes] = []
        self.audio: pyaudio.PyAudio = pyaudio.PyAudio()
        self.stream: Optional[pyaudio.Stream] = None
        self.thread: Optional[threading.Thread] = None

    def start_recording(self) -> None:
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
        
        def record() -> None:
            while self.is_recording:
                data = self.stream.read(CHUNK)
                self.frames.append(data)
        
        self.thread = threading.Thread(target=record)
        self.thread.start()
        print("Recording started... Press 'f' to finish recording.")

    def stop_recording(self) -> Optional[str]:
        """
        Stop the recording and save the audio file.
        
        Returns:
            Optional[str]: Path to the saved audio file or None if recording was not in progress
        """
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

    def close(self) -> None:
        """Clean up resources."""
        self.audio.terminate()


def convert_to_wav(input_file: str) -> Optional[str]:
    """
    Convert audio file to WAV format if needed.
    
    Args:
        input_file: Path to the input audio file
        
    Returns:
        Optional[str]: Path to the converted WAV file or None if conversion failed
    """
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


def list_audio_files() -> list:
    """
    List all audio files in the recordings directory.
    
    Returns:
        list: List of audio file paths
    """
    try:
        files = os.listdir(RECORDINGS_DIR)
        audio_files = [f for f in files if f.endswith(('.wav', '.mp3', '.m4a'))]
        
        if not audio_files:
            print("No audio files found.")
            return []
            
        # Sort files by modification time (newest first)
        audio_files.sort(key=lambda x: os.path.getmtime(os.path.join(RECORDINGS_DIR, x)), reverse=True)
        
        # Format the list for display
        formatted_list = []
        for i, file in enumerate(audio_files):
            file_path = os.path.join(RECORDINGS_DIR, file)
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
            formatted_list.append(f"{i+1}. {file} ({size_mb:.2f} MB) - {mod_time}")
            
        return formatted_list
        
    except Exception as e:
        print(f"Error listing audio files: {e}")
        return []


def get_audio_file_path(index: int) -> Optional[str]:
    """
    Get the path to an audio file by its index in the list.
    
    Args:
        index: Index of the audio file (1-based)
        
    Returns:
        Optional[str]: Path to the audio file or None if not found
    """
    try:
        files = os.listdir(RECORDINGS_DIR)
        audio_files = [f for f in files if f.endswith(('.wav', '.mp3', '.m4a'))]
        
        if not audio_files:
            print("No audio files found.")
            return None
            
        # Sort files by modification time (newest first)
        audio_files.sort(key=lambda x: os.path.getmtime(os.path.join(RECORDINGS_DIR, x)), reverse=True)
        
        if index < 1 or index > len(audio_files):
            print(f"Invalid file index. Please choose a number between 1 and {len(audio_files)}.")
            return None
            
        file_path = os.path.join(RECORDINGS_DIR, audio_files[index-1])
        return file_path
        
    except Exception as e:
        print(f"Error getting audio file path: {e}")
        return None


def delete_audio_file(file_path: str) -> bool:
    """
    Delete an audio file.
    
    Args:
        file_path: Path to the audio file to delete
        
    Returns:
        bool: True if the file was deleted successfully, False otherwise
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {os.path.basename(file_path)} deleted.")
            return True
        else:
            print(f"File {file_path} not found.")
            return False
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False


def record_audio(duration: int = 0) -> Optional[str]:
    """
    Record audio from the microphone.
    
    Args:
        duration: Recording duration in seconds. If 0, record until Ctrl+C is pressed.
        
    Returns:
        Optional[str]: Path to the recorded audio file or None if recording failed
    """
    p = pyaudio.PyAudio()
    
    try:
        # Open stream
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        print("Recording started...")
        frames = []
        
        # Record for specified duration or until interrupted
        if duration > 0:
            # Record for specific duration
            for i in range(0, int(RATE / CHUNK * duration)):
                data = stream.read(CHUNK)
                frames.append(data)
                
            print(f"Recording completed ({duration} seconds)")
        else:
            # Record until Ctrl+C is pressed
            try:
                print("Press Ctrl+C to stop recording")
                start_time = time.time()
                while True:
                    data = stream.read(CHUNK)
                    frames.append(data)
                    
                    # Print elapsed time every 5 seconds
                    current_time = time.time()
                    elapsed = current_time - start_time
                    if elapsed % 5 < 0.1:  # Print approximately every 5 seconds
                        print(f"Recording... {int(elapsed)} seconds")
                        
            except KeyboardInterrupt:
                print("\nRecording stopped by user")
                
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        
        # Save the recorded audio to a file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recording_{timestamp}.wav"
        filepath = os.path.join(RECORDINGS_DIR, filename)
        
        with wave.open(filepath, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            
        print(f"Audio saved to {filepath}")
        return filepath
        
    except Exception as e:
        print(f"Error during recording: {e}")
        return None
        
    finally:
        p.terminate()