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
  - Style selection (vivid or natural)
- **File Management**: Manage audio, transcript, and image files

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

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
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
python main.py
```

This will start the interactive menu-driven interface where you can access all features.

### Command-Line Options

The application also supports command-line options for quick actions:

```bash
# Record audio (using Ctrl+C to stop)
python main.py --record

# Record audio for a specific duration (in seconds)
python main.py --record --duration 60

# Transcribe an audio file
python main.py --transcribe /path/to/audio/file.wav
```

## Directory Structure

The application creates the following directories to store files:

- `recordings/`: Recorded audio files
- `transcripts/`: Transcription files
- `processed/`: Processed text files (summaries, translations, etc.)
- `images/`: Generated images

## Modules

- `audio.py`: Audio recording and file management
- `transcription.py`: Audio transcription using Whisper API
- `processors.py`: Text processing using OpenAI GPT models
- `image_gen.py`: Image generation using GPT-Image-1
- `main.py`: Main application and user interface

## License

[MIT License](LICENSE)

## Acknowledgements

This application uses the following APIs from OpenAI:
- Whisper API for transcription
- GPT models for text processing
- GPT-Image-1 for image generation
