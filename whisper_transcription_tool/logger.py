"""
Logging configuration for the Whisper Transcription Tool.
"""
import os
import sys
import logging
from datetime import datetime
from typing import Optional


class WhisperLogger:
    """Custom logger for the Whisper Transcription Tool."""
    
    def __init__(self, name: str = "whisper_transcription", 
                 log_level: int = logging.INFO,
                 log_to_console: bool = True,
                 log_to_file: bool = True,
                 log_file: Optional[str] = None) -> None:
        """
        Initialize the logger.
        
        Args:
            name: Name of the logger
            log_level: Logging level
            log_to_console: Whether to log to console
            log_to_file: Whether to log to file
            log_file: Optional path to log file
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.logger.handlers = []  # Clear any existing handlers
        
        # Create formatters
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
        
        # Add console handler
        if log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
        
        # Add file handler
        if log_to_file:
            # Create logs directory if it doesn't exist
            os.makedirs("logs", exist_ok=True)
            
            # Use provided log file or create a default one
            if not log_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                log_file = f"logs/whisper_transcription_{timestamp}.log"
                
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str) -> None:
        """Log a debug message."""
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """Log an info message."""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log an error message."""
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """Log a critical message."""
        self.logger.critical(message)


# Default logger instance
logger = WhisperLogger()


def get_logger(name: str = None, log_level: int = None) -> WhisperLogger:
    """
    Get a configured logger instance.
    
    Args:
        name: Optional logger name
        log_level: Optional log level
        
    Returns:
        WhisperLogger: Configured logger instance
    """
    if name or log_level:
        return WhisperLogger(
            name=name or "whisper_transcription",
            log_level=log_level or logging.INFO
        )
    return logger