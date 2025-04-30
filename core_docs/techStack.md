# Tech Stack

## Core Technologies
- Python 3.8+
- OpenAI API suite
  - Whisper API for transcription
  - GPT-4.1 for text processing
  - DALL-E 3 for image generation (upgrading from gpt-image-1)

## Libraries & Frameworks
- Rich: Terminal UI framework for beautiful console interfaces
- Requests: HTTP library for API calls
- PIL/Pillow: Image processing library
- PyAudio: Audio recording and processing
- OpenAI Python SDK: Interface with OpenAI APIs

## Architecture
- CLI-based application with modular design
- Core components:
  - `audio.py`: Audio recording and file management
  - `transcription.py`: Audio transcription using Whisper API
  - `processors.py`: Text processing using GPT models
  - `image_gen.py`: Image generation using DALL-E 3
  - `conversation.py`: Handling conversations with AI assistant (to be implemented)

## Data Management
- `data/recordings/`: Recorded audio files
- `data/transcripts/`: Transcription files
- `data/processed/`: Processed text files
- `data/images/`: Generated images
- `data/conversation/`: Conversation logs (to be implemented)

## References
- OpenAI Whisper API: https://platform.openai.com/docs/guides/speech-to-text
- OpenAI Chat Completions API: https://platform.openai.com/docs/guides/chat
- OpenAI DALL-E 3 API: https://platform.openai.com/docs/guides/images/dall-e
- DALL-E 3 Features: https://cookbook.openai.com/articles/what_is_new_with_dalle_3
- GPT-4.1 Model: https://openrouter.ai/openai/gpt-4.1
- Rich Documentation: https://rich.readthedocs.io/en/latest/
- PyAudio Documentation: https://people.csail.mit.edu/hubert/pyaudio/docs/ 