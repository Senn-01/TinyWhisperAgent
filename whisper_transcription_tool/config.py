import os
from typing import Dict, Any, List

# Directory paths
DATA_DIR = "data"
RECORDINGS_DIR = os.path.join(DATA_DIR, "recordings")
TRANSCRIPTS_DIR = os.path.join(DATA_DIR, "transcripts")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
IMAGES_DIR = os.path.join(DATA_DIR, "images")

# Audio settings
AUDIO_SETTINGS = {
    "format": "paInt16",
    "channels": 1,
    "rate": 44100,
    "chunk": 1024,
    "temp_file": "temp_recording.wav"
}

# Transcription settings
TRANSCRIPTION_SETTINGS = {
    "model": "whisper-1",
    "response_format": "text"
}

# Image generation settings
IMAGE_SETTINGS = {
    "model": "gpt-image-1",
    "size": "1024x1024",
    "quality": "medium",
    "style": "vivid"
}

# GPT models for text processing
GPT_MODELS = {
    "default": "gpt-4.1",
    "summary": "gpt-4.1",
    "translation": "gpt-4.1",
    "formatting": "gpt-4.1"
}

# Create all required directories
def create_directories() -> None:
    """Create all required directories for the application."""
    for directory in [RECORDINGS_DIR, TRANSCRIPTS_DIR, PROCESSED_DIR, IMAGES_DIR]:
        os.makedirs(directory, exist_ok=True)