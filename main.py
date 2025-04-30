#!/usr/bin/env python3
"""
Main entry point for the Whisper Transcription Tool.
"""
import sys
from whisper_transcription_tool.cli import main

if __name__ == "__main__":
    sys.exit(main.main())