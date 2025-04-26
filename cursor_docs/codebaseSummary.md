# Codebase Summary

[Roadmap](projectRoadmap.md) | [Task](currentTask.md) | [Stack](techStack.md) | [Summary](codebaseSummary.md)

## Version History
v1.0 - Initial codebase summary documentation
v1.1 - Updated to include GPT-4.1 and GPT-Image-1 integration
v1.2 - Added GitHub repository information and code verification
v1.3 - Updated to include GPT-Image-1 quality and style parameters

## Project Overview

The Whisper Transcription App is a Python-based command-line tool that leverages OpenAI's Whisper API for audio transcription, GPT-4.1 for post-processing of transcripts, and GPT-Image-1 for generating images from transcript content. The application provides a simple interface for transcribing audio files or recording live audio, then offers post-processing options such as summarization, transcript cleaning, and image generation.

## Repository Information

- **GitHub Repository**: [https://github.com/Senn-01/TinyWhisperAgent.git](https://github.com/Senn-01/TinyWhisperAgent.git)

## Directory Structure

```
whisper/
├── main.py                 # Main application entry point with CLI interface
├── record/                 # Directory for storing audio recordings
├── transcript/             # Directory for storing generated transcripts
├── improved-transcript/    # Directory for storing processed transcripts 
├── generated_images/       # Directory for storing generated images
└── cursor_docs/            # Project documentation
    ├── techStack.md        # Technology stack details
    └── codebaseSummary.md  # This file
```

## Code Evaluation Against Cursor Rules

The current codebase has both strengths and areas for improvement when compared to the Cursor AI development guidelines:

### Strengths:
- ✅ Clear error handling in most functions with exception catching and user feedback
- ✅ Detailed documentation in README and technical docs
- ✅ Configuration management using environment variables for API keys
- ✅ Descriptive variable and function names
- ✅ Clean organization of output files in dedicated directories

### Areas for Improvement:
- ❌ **Monolithic Design**: The entire application is in one file instead of separate modules
- ❌ **Missing Type Hints**: Functions lack Python type annotations
- ❌ **Limited Testing**: No pytest implementation
- ❌ **No CI/CD**: Missing GitHub Actions or similar automation
- ❌ **Limited Docstrings**: Functions have basic docstrings but lack parameter documentation
- ❌ **Error Context**: Some error handling doesn't capture sufficient context

### Recommended Refactoring:
1. Split `main.py` into modules:
   - `audio.py` - Recording and file handling
   - `transcription.py` - Whisper API integration
   - `processors.py` - GPT-4.1 text processing
   - `image_gen.py` - GPT-Image-1 integration
   - `ui.py` - Command-line interface

2. Add comprehensive type hints to all functions
3. Implement a basic test suite with pytest
4. Add GitHub Actions workflow for CI
5. Enhance error handling with more context

## Core Components

### Audio Processing
- `AudioRecorder` class for handling live audio recording
- Functions for processing audio files, converting formats, and chunking large files
- Integration with ffmpeg for audio manipulation

### Transcription Engine
- Whisper API integration for converting speech to text
- Handling of various audio formats
- Support for transcribing large files by splitting into chunks

### Post-Processing with GPT-4.1
- Transcript summarization
- Transcript cleaning and reformatting
- Q&A functionality based on transcript content
- Multiple reformatting options (bullet points, Q&A format, etc.)

### Image Generation with GPT-Image-1
- Visual representation of transcript content
- Two-stage prompt engineering process:
  1. Extract key visual elements from transcript using GPT-4.1
  2. Generate detailed image prompt from visual elements
- Configurable image generation parameters:
  - Quality: Standard or HD resolution
  - Style: Vivid or Natural aesthetic
- Image saving with timestamp and reference system

### User Interface
- Menu-driven command-line interface
- Options for recording, file selection, and transcript interaction
- Feedback and progress reporting

## Key Functions

| Function | Purpose |
|----------|---------|
| `main()` | Entry point, displays main menu |
| `handle_file_transcription()` | Processes audio files for transcription |
| `handle_live_recording()` | Records and processes live audio |
| `transcribe_audio()` | Sends audio to Whisper API and handles response |
| `transcribe_large_file()` | Splits and processes large audio files |
| `post_transcription_menu()` | Displays options after transcription |
| `get_summary()` | Generates summary using GPT-4.1 |
| `get_cleaner_transcript()` | Generates cleaned transcript using GPT-4.1 |
| `generate_image_from_transcript()` | Creates images using GPT-Image-1 with quality options |
| `generate_image_from_prompt()` | Creates images using GPT-Image-1 with quality and style options |
| `handle_transcript_interaction()` | Provides tools for working with existing transcripts |
| `save_transcript_to_markdown()` | Saves transcript to disk as markdown |

## Workflow

1. **Audio Input**
   - Live recording through microphone
   - Selection of existing audio file

2. **Transcription**
   - Processing audio through Whisper API
   - Handling large files through chunking

3. **Post-Processing**
   - Summarization of transcript
   - Cleaning and reformatting
   - Custom Q&A
   - Image generation

4. **Output**
   - Save transcripts as markdown
   - Store generated images
   - Create references between transcripts and images

## AI Model Usage

### GPT-4.1
- Used for intelligent text processing tasks
- Runs with temperature=0.3 for consistent outputs
- Handles tasks requiring deep language understanding

### GPT-Image-1
- Used to visualize transcript content
- Works with 1024x1024 resolution
- Supports quality settings: standard and HD
- Offers style options: vivid and natural
- Requires carefully crafted prompts (generated by GPT-4.1)

### Whisper
- Handles speech-to-text conversion
- Supports multiple languages and audio formats
- File size limitations managed through chunking

## External Dependencies

The application depends on several Python packages:
- `openai`: For API access to GPT-4.1, GPT-Image-1, and Whisper
- `pyaudio`: For recording capabilities
- `ffmpeg`: For audio processing
- `PIL`: For image handling
- Standard library modules: `os`, `tempfile`, `datetime`, etc.

## Future Development Opportunities

1. Code Modularization
   - Split monolithic main.py into separate modules
   - Create classes for main components

2. Enhanced Error Handling
   - Add more robust error recovery
   - Improve feedback on API failures

3. Configuration System
   - External configuration file
   - User preference saving

4. Additional Features
   - Batch processing of audio files
   - More advanced image generation options
   - Speaker diarization integration 