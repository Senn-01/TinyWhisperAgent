# Technical Stack

[Roadmap](projectRoadmap.md) | [Task](currentTask.md) | [Stack](techStack.md) | [Summary](codebaseSummary.md)

## Version History
v1.0 - Initial tech stack documentation
v1.1 - Updated to use GPT-4.1 and added GPT-Image-1 integration

## Current Technology Stack

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.9+ | Primary programming language |
| OpenAI API | Latest | Access to Whisper, GPT-4.1, and GPT-Image-1 models |
| PyAudio | 0.2.13 | Audio recording and processing |
| ffmpeg | Latest | Audio file conversion and chunking |
| PIL (Pillow) | Latest | Image processing |

### AI/ML Models

| Model | Provider | Purpose |
|-------|----------|---------|
| Whisper API | OpenAI | Audio transcription |
| GPT-4.1 | OpenAI | Transcript processing and analysis |
| GPT-Image-1 | OpenAI | Image generation from transcript content |

### User Interface

| Technology | Purpose |
|------------|---------|
| Command Line Interface | User interaction through terminal |

### File Formats

| Format | Purpose |
|--------|---------|
| .wav, .mp3, etc. | Audio recording/input formats |
| .md (Markdown) | Output transcript format |
| .png, .jpg | Output image formats |

## Architecture Overview

The application follows a modular architecture with the following components:

1. **User Interface Layer**
   - Command-line menu system
   - User input handling
   - Output formatting

2. **Core Processing Layer**
   - Audio file handling
   - Live recording management
   - API interactions

3. **AI Processing Layer**
   - Transcription with Whisper API
   - Text processing with GPT-4.1
   - Image generation with GPT-Image-1

4. **Output Layer**
   - Transcript display and saving
   - Image storage and referencing
   - Formatting options

### Data Flow

```
User Input → Audio Processing → Whisper API → [Transcript] → GPT-4.1 Processing/GPT-Image-1 → Output
```

## External Dependencies

### APIs
- OpenAI API (requires API key with access to GPT-4.1 and GPT-Image-1)

### System Requirements
- Microphone access (for live recording)
- Internet connection (for API access)
- Python 3.9+ runtime
- Sufficient disk space for audio recordings and generated images

## Directory Structure

```
whisper/
├── main.py                 # Main application
├── record/                 # Audio recordings
├── transcript/             # Generated transcripts
├── improved-transcript/    # Enhanced transcripts
├── generated_images/       # Images from transcript content
└── cursor_docs/            # Project documentation
```

## Key Features

1. **Audio Processing**
   - Live recording capabilities
   - Support for various audio formats
   - Large file chunking for API limits

2. **Transcription**
   - High-quality speech-to-text conversion
   - Support for multiple languages
   - Long recording handling

3. **Advanced Processing**
   - Transcript summarization with GPT-4.1
   - Transcript cleaning and formatting
   - Q&A capabilities on transcript content

4. **Image Generation**
   - Visual representation of transcript content
   - High-quality image creation with GPT-Image-1
   - Automatic prompt engineering

## Future Technology Considerations

### Short-term Additions
- Configuration system (YAML or JSON based)
- Logging framework
- Progress indicators

### Medium-term Additions
- Local Whisper model support
- Speaker diarization libraries
- Batch processing system

### Long-term Additions
- Web framework (Flask/FastAPI)
- Database for transcript storage
- Authentication system

## Decision Records

| Date | Decision | Alternatives Considered | Reasoning |
|------|----------|-------------------------|-----------|
| N/A | Use OpenAI Whisper API | Local Whisper model | Simplicity of implementation, higher accuracy |
| N/A | Command-line interface | GUI, Web interface | Fastest to implement for MVP |
| N/A | Markdown output | Plain text, JSON, SRT | Readability and formatting options |
| N/A | GPT-4.1 for post-processing | GPT-3.5, Claude | Most advanced capabilities for summarization and cleaning 