"""
Custom exceptions for the Whisper Transcription Tool.
"""
from typing import Optional


class WhisperTranscriptionError(Exception):
    """Base exception for all Whisper Transcription Tool errors."""
    def __init__(self, message: str = "An error occurred in the Whisper Transcription Tool"):
        self.message = message
        super().__init__(self.message)


class AudioError(WhisperTranscriptionError):
    """Exception raised for errors in audio recording or processing."""
    def __init__(self, message: str = "An error occurred with audio processing"):
        self.message = message
        super().__init__(self.message)


class TranscriptionError(WhisperTranscriptionError):
    """Exception raised for errors in audio transcription."""
    def __init__(self, message: str = "An error occurred during transcription", 
                 status_code: Optional[int] = None, 
                 model: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.model = model
        error_msg = f"{message}"
        if status_code:
            error_msg += f" (Status code: {status_code})"
        if model:
            error_msg += f" (Model: {model})"
        super().__init__(error_msg)


class APIError(WhisperTranscriptionError):
    """Exception raised for API-related errors."""
    def __init__(self, message: str = "API error occurred", 
                 status_code: Optional[int] = None, 
                 endpoint: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.endpoint = endpoint
        error_msg = f"{message}"
        if status_code:
            error_msg += f" (Status code: {status_code})"
        if endpoint:
            error_msg += f" (Endpoint: {endpoint})"
        super().__init__(error_msg)


class ProcessingError(WhisperTranscriptionError):
    """Exception raised for errors in transcript processing."""
    def __init__(self, message: str = "An error occurred during transcript processing", 
                 processor_type: Optional[str] = None):
        self.message = message
        self.processor_type = processor_type
        error_msg = f"{message}"
        if processor_type:
            error_msg += f" (Processor: {processor_type})"
        super().__init__(error_msg)


class ImageGenerationError(WhisperTranscriptionError):
    """Exception raised for errors in image generation."""
    def __init__(self, message: str = "An error occurred during image generation", 
                 model: Optional[str] = None):
        self.message = message
        self.model = model
        error_msg = f"{message}"
        if model:
            error_msg += f" (Model: {model})"
        super().__init__(error_msg)


class FileError(WhisperTranscriptionError):
    """Exception raised for file-related errors."""
    def __init__(self, message: str = "A file error occurred", 
                 file_path: Optional[str] = None, 
                 operation: Optional[str] = None):
        self.message = message
        self.file_path = file_path
        self.operation = operation
        error_msg = f"{message}"
        if operation:
            error_msg += f" (Operation: {operation})"
        if file_path:
            error_msg += f" (File: {file_path})"
        super().__init__(error_msg)


class ConfigError(WhisperTranscriptionError):
    """Exception raised for configuration errors."""
    def __init__(self, message: str = "A configuration error occurred", 
                 config_key: Optional[str] = None):
        self.message = message
        self.config_key = config_key
        error_msg = f"{message}"
        if config_key:
            error_msg += f" (Config key: {config_key})"
        super().__init__(error_msg)