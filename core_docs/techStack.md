# Technology Stack (v2)

## Core Technologies
- **Python**: Main programming language (3.8+)
- **OpenAI APIs**:
  - Whisper API for transcription (whisper-1 model only)
  - GPT models for text processing
  - GPT-Image-1 for image generation

## Frameworks & Libraries
- **PyAudio**: Audio recording from microphone (0.2.14)
- **Rich**: Terminal UI components and styling (14.0.0+)
- **Pillow**: Image processing (10.1.0)
- **Requests**: HTTP requests handling (2.31.0)
- **python-dotenv**: Environment variable management (1.0.0+)
- **Pydantic**: Data validation (2.0.0+)

## Development Tools
- **pytest**: Testing framework (7.4.0+)
- **pytest-cov**: Test coverage reporting (4.1.0+)
- **black**: Code formatting (23.3.0+)
- **ruff**: Linting (0.0.270+)
- **mypy**: Type checking (1.3.0+)

## Architecture
- **Modular Design**: Separate modules for each functionality
  - `audio.py`: Audio recording and file management
  - `transcription.py`: Audio transcription using Whisper API
  - `processors.py`: Text processing using OpenAI GPT models
  - `image_gen.py`: Image generation using GPT-Image-1
  - `main.py`: Main application and user interface
  - `config.py`: Centralized configuration settings
  - `logger.py`: Consistent logging system
  - `errors.py`: Custom exception classes and error handling utilities

- **File Organization**:
  - `recordings/`: Recorded audio files
  - `transcripts/`: Transcription files
  - `processed/`: Processed text files
  - `images/`: Generated images
  - `tests/`: Test modules and fixtures

## Configuration
- Environment variables for API keys:
  - `OPENAI_API_KEY`: Required for OpenAI services

## References
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [OpenAI Whisper GitHub](https://github.com/openai/whisper)
- [Rich Documentation](https://rich.readthedocs.io/) 