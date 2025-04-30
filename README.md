# Whisper Transcription Tool

A comprehensive Python application for audio recording, transcription, and processing using OpenAI's Whisper API and GPT models.

## Features

- **Audio Recording**: Record audio from your microphone
- **Transcription**: Transcribe audio files using OpenAI's Whisper API
- **Text Processing**:
  - Generate summaries
  - Extract key points
  - Extract action items
  - Reformat transcripts in various styles
  - Translate transcripts to other languages
  - Analyze sentiment
- **Image Generation**: Create images based on transcripts or custom prompts using OpenAI's GPT-Image-1 model
  - Support for HD or standard quality
  - Rich interactive UI with progress visualization
- **File Management**: Manage audio, transcript, and image files
- **Rich Terminal UI**: Beautiful, colorful terminal interface with interactive components

## Requirements

- Python 3.8+
- OpenAI API key
- PortAudio (for PyAudio)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd whisper-transcription-tool
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

4. PortAudio installation:
   - **macOS**: `brew install portaudio`
   - **Ubuntu/Debian**: `sudo apt-get install portaudio19-dev`
   - **Windows**: PortAudio binaries are included with PyAudio wheels

5. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key"
   ```
   For Windows:
   ```cmd
   set OPENAI_API_KEY=your-api-key
   ```

## Usage

### Running the Application

```bash
# After installing the package
whisper-tool

# OR from the project directory 
python main.py
```

This will start the interactive menu-driven interface where you can access all features.

### Simple Example

A basic example script is included to demonstrate the transcription functionality:

```bash
python examples/simple_transcription.py
```

### Command-Line Options

The application also supports command-line options for quick actions:

```bash
# Record audio (using Ctrl+C to stop)
whisper-tool --record

# Record audio for a specific duration (in seconds)
whisper-tool --record --duration 60

# Transcribe an audio file
whisper-tool --transcribe /path/to/audio/file.wav
```

## Directory Structure

The application uses the following directories to store files:

- `data/recordings/`: Recorded audio files
- `data/transcripts/`: Transcription files
- `data/processed/`: Processed text files (summaries, translations, etc.)
- `data/images/`: Generated images
- `logs/`: Application log files (created when needed)
- `whisper_transcription_tool/`: Main package
  - `cli/`: Command-line interface
  - `audio.py`, `transcription.py`, etc.: Core functionality modules

## Package Modules

- `whisper_transcription_tool/audio.py`: Audio recording and file management
- `whisper_transcription_tool/transcription.py`: Audio transcription using Whisper API
- `whisper_transcription_tool/processors.py`: Text processing using OpenAI GPT models
- `whisper_transcription_tool/image_gen.py`: Image generation using GPT-Image-1
- `whisper_transcription_tool/cli/main.py`: Main application and user interface
- `whisper_transcription_tool/config.py`: Centralized configuration settings
- `whisper_transcription_tool/logger.py`: Consistent logging system
- `whisper_transcription_tool/errors.py`: Custom exception classes

## Recent Updates

### v2.0 Updates

- **Complete Package Restructure**:
  - Reorganized code into a proper Python package structure
  - Created a clean and modular architecture
  - Improved imports and code organization
  - Better separation of concerns between modules

- **Simplified API**:
  - Removed speaker diarization functionality
  - Standardized on whisper-1 model for all transcriptions
  - Fixed image generation quality parameters
  - Improved error handling

- **Better Installation**:
  - Package can now be installed with pip
  - Added console script entry point
  - Simplified dependencies

- **Code Quality**:
  - Added type hints throughout the codebase
  - Improved error handling with custom exceptions
  - Consistent logging with dedicated logger module
  - Centralized configuration

## License

[MIT License](LICENSE)

## Acknowledgements

This application uses the following APIs and models:
- OpenAI's Whisper API for transcription
- OpenAI's GPT models for text processing
- OpenAI's GPT-Image-1 for image generation