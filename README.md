# Whisper Transcription App

A powerful Python application that records audio, transcribes it using OpenAI's Whisper API, enhances transcripts with GPT-4.1, and generates images based on transcript content using GPT-Image-1.

## Features

- Record audio directly from your microphone
- Transcribe existing audio files from the 'record' directory (supports .mp3, .m4a, .wav, .flac, .ogg, .aac, .wma, .mka)
- Automatically handles large files by splitting them into chunks
- Save transcripts as markdown files with timestamps in a dedicated 'transcript' directory
- Advanced post-processing with OpenAI's GPT-4.1:
  - Generate concise summaries with key points
  - Create cleaner transcripts by removing filler words and verbal noise
- Generate images from transcript content using OpenAI's GPT-Image-1:
  - Automatic extraction of key visual elements
  - Intelligent prompt engineering for high-quality images
  - Save generated images with references back to source transcripts
- Interact with existing transcripts in multiple ways:
  - Ask questions about transcript content
  - Generate reformatted versions in various styles
  - Create visual representations of transcripts

## Prerequisites

- Python 3.9 or higher
- OpenAI API key with access to GPT-4.1 and GPT-Image-1
- A microphone connected to your computer (for recording)
- FFmpeg installed on your system (for audio file conversion)
- Pillow (PIL) for image processing

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd whisper
   ```

2. Install FFmpeg (if not already installed):
   - On Ubuntu/Debian: `sudo apt-get install ffmpeg`
   - On macOS: `brew install ffmpeg`
   - On Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use Chocolatey: `choco install ffmpeg`

3. Install the required dependencies:
   ```
   pip install .
   ```

## Usage

1. Run the application:
   ```
   python main.py
   ```

2. If you haven't set the `OPENAI_API_KEY` environment variable, you will be prompted to enter your OpenAI API key.

3. Choose from the following options:
   - Option 1: Record new audio
     - Press Enter to start recording
     - Press 'f' to finish recording
   - Option 2: Transcribe existing audio file
     - Select from the list of audio files in the 'record' directory
   - Option 3: Interact with existing transcripts
   - Option 4: Quit the application

4. After transcription is complete, you'll see a post-transcription menu with these options:
   - Option 1: Save transcript as is
   - Option 2: Generate summary (key points)
   - Option 3: Generate cleaner transcript
   - Option 4: Both summary and cleaner transcript
   - Option 5: Generate image from transcript
   - Option 6: Return to main menu

5. When interacting with existing transcripts, you can:
   - Ask questions about the transcript
   - Reformat the transcript in various styles
   - Generate an image based on transcript content
   - Return to the main menu

## Image Generation

The application uses a two-stage process for generating images from transcripts:

1. **Visual Element Extraction**: GPT-4.1 analyzes the transcript to identify key visual elements that could be visually represented.

2. **Prompt Engineering**: Another GPT-4.1 call converts these elements into a detailed prompt optimized for image generation.

3. **Image Creation**: The prompt is sent to OpenAI's GPT-Image-1 model, which generates a high-quality image.

4. **Image Storage**: Generated images are saved in the 'generated_images' directory with reference files linking back to source transcripts.

## File Organization

- Audio files are stored in the 'record' directory
- Transcripts are saved in the 'transcript' directory
- Enhanced transcripts (summaries, cleaned versions, Q&A) go to 'improved-transcript'
- Generated images are saved in the 'generated_images' directory
- The application automatically creates all necessary directories

## Transcript Formats

The application supports multiple transcript formats:

- Standard transcripts (raw from Whisper API)
- Cleaned transcripts (filler words and verbal noise removed)
- Bullet-point summaries
- Q&A format
- Speaker-separated format
- Simplified language
- Structured format with sections
- Action item extraction
- Custom formats

## Troubleshooting

- If you encounter issues with PyAudio installation, you may need to install additional system dependencies:
  - On Ubuntu/Debian: `sudo apt-get install portaudio19-dev`
  - On macOS: `brew install portaudio`
  - On Windows: PyAudio wheel should install without additional dependencies

- For image generation issues:
  - Ensure your OpenAI API key has access to GPT-Image-1
  - Check that the transcript contains visualizable content
  - Consider internet connection speed for downloading images
  - Verify Pillow (PIL) is properly installed for image saving

- For very large files, the chunking and processing may take some time

## License

This project is open-source and available under the MIT License.
# TinyWhisperAgent
