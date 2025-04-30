import os
import sys
import argparse
from typing import Optional, List, Dict, Any
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import modules from the package
from whisper_transcription_tool import audio, transcription, processors, image_gen, config

# Initialize Rich console
console = Console()

def load_api_key() -> bool:
    """
    Load the OpenAI API key from environment variable.
    
    Returns:
        bool: True if API key was loaded successfully, False otherwise
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set your OpenAI API key with:")
        print("    export OPENAI_API_KEY='your-api-key'")
        return False
        
    import openai
    openai.api_key = api_key
    return True


def display_main_menu() -> None:
    """Display the main menu options."""
    console.print(Panel("[bold]Whisper Transcription Tool[/]", style="blue"))
    console.print("[1] Record Audio")
    console.print("[2] Transcribe Audio File")
    console.print("[3] Process Transcript")
    console.print("[4] Generate Image")
    console.print("[5] File Management")
    console.print("[0] Exit")


def display_process_menu() -> None:
    """Display the transcript processing menu options."""
    print("\n=== Process Transcript ===")
    print("1. Generate Summary")
    print("2. Extract Key Points")
    print("3. Extract Action Items")
    print("4. Reformat Transcript")
    print("5. Translate Transcript")
    print("6. Analyze Sentiment")
    print("7. Converse with AI Assistant")
    print("0. Back to Main Menu")


def display_file_menu() -> None:
    """Display the file management menu options."""
    console.print(Panel("[bold]File Management[/]", style="blue"))
    console.print("[1] List Audio Files")
    console.print("[2] List Transcript Files")
    console.print("[3] List Image Files")
    console.print("[4] List Conversation Files")
    console.print("[5] Delete File")
    console.print("[0] Back to Main Menu")


def record_audio_workflow() -> None:
    """Handle the audio recording workflow."""
    try:
        print("\n=== Record Audio ===")
        print("How long would you like to record? (in seconds, 0 for manual stop)")
        duration_input = input("Duration: ")
        
        try:
            duration = int(duration_input)
        except ValueError:
            print("Invalid input. Using manual stop.")
            duration = 0
            
        audio_file = audio.record_audio(duration)
        
        if audio_file:
            print(f"Recording saved to: {audio_file}")
            
            # Ask if user wants to transcribe the recording
            transcribe_now = input("Would you like to transcribe this recording now? (y/n): ").lower()
            if transcribe_now == 'y':
                transcribe_audio_workflow(audio_file)
        
    except KeyboardInterrupt:
        print("\nRecording interrupted.")
    except Exception as e:
        print(f"Error in recording workflow: {e}")


def transcribe_audio_workflow(file_path: Optional[str] = None) -> None:
    """
    Handle the audio transcription workflow.
    
    Args:
        file_path: Optional path to audio file to transcribe
    """
    try:
        print("\n=== Transcribe Audio ===")
        
        # If file path not provided, let user choose from available files
        if not file_path:
            audio_files = audio.list_audio_files()
            
            if not audio_files:
                print("No audio files found.")
                return
                
            print("\nAvailable audio files:")
            for file in audio_files:
                print(file)
                
            file_index = input("\nEnter the number of the file to transcribe (or 0 to cancel): ")
            
            try:
                index = int(file_index)
                if index == 0:
                    return
                file_path = audio.get_audio_file_path(index)
            except ValueError:
                print("Invalid input.")
                return
                
            if not file_path:
                return
        
        # Using only whisper-1 model
        model = "whisper-1"  # Fixed model
        
        console.print("[bold blue]Transcribing audio using whisper-1 model...[/]")
        
        # Transcribe audio
        print("\nTranscribing (this may take a while)...")
        result = transcription.transcribe_audio(file_path, model=model)
        
        if result:
            print("\nTranscription completed.")
            print("\nTranscript preview:")
            transcript_text = result["text"]
            preview_length = min(200, len(transcript_text))
            print(f"{transcript_text[:preview_length]}...")
            
            # Ask what to do with the transcript
            process_now = input("\nWould you like to process this transcript now? (y/n): ").lower()
            if process_now == 'y':
                process_transcript_workflow()
        else:
            print("Transcription failed.")
            
    except Exception as e:
        print(f"Error in transcription workflow: {e}")


def process_transcript_workflow() -> None:
    """Handle the transcript processing workflow."""
    try:
        # List available transcripts
        transcript_files = transcription.list_transcripts()
        
        if not transcript_files:
            print("No transcript files found.")
            return
            
        print("\nAvailable transcript files:")
        for file in transcript_files:
            print(file)
            
        file_index = input("\nEnter the number of the transcript to process (or 0 to cancel): ")
        
        try:
            index = int(file_index)
            if index == 0:
                return
            transcript = transcription.get_transcript_content(index)
        except ValueError:
            print("Invalid input.")
            return
            
        if not transcript:
            return
            
        # Display processing options
        while True:
            display_process_menu()
            choice = input("Enter your choice: ")
            
            if choice == '0':
                break
            elif choice == '1':
                summary = processors.get_summary(transcript)
                if summary:
                    print("\nSummary:")
                    print("-" * 50)
                    print(summary)
                    print("-" * 50)
            elif choice == '2':
                key_points = processors.get_key_points(transcript)
                if key_points:
                    print("\nKey Points:")
                    print("-" * 50)
                    print(key_points)
                    print("-" * 50)
            elif choice == '3':
                action_items = processors.get_action_items(transcript)
                if action_items:
                    print("\nAction Items:")
                    print("-" * 50)
                    print(action_items)
                    print("-" * 50)
            elif choice == '4':
                print("\nAvailable formats:")
                print("1. Clean (grammar fixes, punctuation)")
                print("2. Paragraphs (organized into paragraphs)")
                print("3. Structured (with headings and sections)")
                print("4. Q&A (question and answer format)")
                print("5. Minutes (meeting minutes format)")
                print("6. Narrative (story-like format)")
                
                format_choice = input("Choose a format (1-6): ")
                format_map = {
                    '1': 'clean',
                    '2': 'paragraphs',
                    '3': 'structured',
                    '4': 'qa',
                    '5': 'minutes',
                    '6': 'narrative'
                }
                
                format_type = format_map.get(format_choice, 'clean')
                reformatted = processors.reformat_transcript(transcript, format_type)
                
                if reformatted:
                    print("\nReformatted Transcript:")
                    print("-" * 50)
                    print(reformatted[:300] + "..." if len(reformatted) > 300 else reformatted)
                    print("-" * 50)
                    print(f"Full reformatted transcript saved to file.")
            elif choice == '5':
                target_language = input("Enter target language: ")
                translated = processors.translate_transcript(transcript, target_language)
                
                if translated:
                    print("\nTranslated Transcript:")
                    print("-" * 50)
                    print(translated[:300] + "..." if len(translated) > 300 else translated)
                    print("-" * 50)
                    print(f"Full translation saved to file.")
            elif choice == '6':
                sentiment = processors.analyze_sentiment(transcript)
                
                if sentiment:
                    print("\nSentiment Analysis:")
                    print("-" * 50)
                    print(sentiment)
                    print("-" * 50)
            elif choice == '7':
                # Start conversation with the assistant
                from whisper_transcription_tool import conversation
                conversation.interactive_conversation(transcript)
            else:
                print("Invalid choice. Please try again.")
        
    except Exception as e:
        print(f"Error in processing workflow: {e}")


def generate_image_workflow() -> None:
    """Handle the image generation workflow."""
    try:
        console.print(Panel("[bold]Generate Image[/]", style="blue"))
        console.print("[1] Generate from transcript")
        console.print("[2] Generate from custom prompt")
        console.print("[0] Back to Main Menu")
        
        choice = Prompt.ask("Enter your choice", choices=["0", "1", "2"], default="0")
        
        if choice == '0':
            return
        elif choice == '1':
            # List available transcripts
            transcript_files = transcription.list_transcripts()
            
            if not transcript_files:
                console.print("[yellow]No transcript files found.[/]")
                return
                
            console.print(Panel("[bold]Available transcript files[/]", style="blue"))
            for file in transcript_files:
                console.print(file)
                
            file_index = IntPrompt.ask("Enter the number of the transcript to use (or 0 to cancel)", default=0)
            
            if file_index == 0:
                return
                
            try:
                transcript = transcription.get_transcript_content(file_index)
                if not transcript:
                    return
            except ValueError:
                console.print("[bold red]Invalid input.[/]")
                return
            
            # Ask for quality
            console.print(Panel("[bold]Select image quality[/]", style="blue"))
            console.print("[1] Medium (Standard)")
            console.print("[2] High (HD)")
            quality_choice = Prompt.ask("Enter your choice", choices=["1", "2"], default="1")
            quality = "hd" if quality_choice == "2" else "standard"
                
            # Generate image from transcript
            image_path = image_gen.generate_image_from_transcript(transcript, quality=quality)
            
        elif choice == '2':
            # Generate from custom prompt
            prompt = Prompt.ask("\nEnter your image generation prompt")
            
            if not prompt:
                console.print("[yellow]No prompt provided.[/]")
                return
            
            # Ask for quality
            console.print(Panel("[bold]Select image quality[/]", style="blue"))
            console.print("[1] Medium (Standard)")
            console.print("[2] High (HD)")
            quality_choice = Prompt.ask("Enter your choice", choices=["1", "2"], default="1")
            quality = "hd" if quality_choice == "2" else "standard"
            
            # Generate image from custom prompt
            image_path = image_gen.generate_image_from_prompt(prompt, quality=quality)
            
        else:
            console.print("[bold red]Invalid choice.[/]")
        
    except Exception as e:
        console.print(f"[bold red]Error in image generation workflow:[/] {str(e)}")


def file_management_workflow() -> None:
    """Handle the file management workflow."""
    try:
        while True:
            display_file_menu()
            choice = Prompt.ask("Enter your choice", choices=["0", "1", "2", "3", "4", "5"], default="0")
            
            if choice == '0':
                break
            elif choice == '1':
                # List audio files
                audio_files = audio.list_audio_files()
                
                if not audio_files:
                    console.print("[yellow]No audio files found.[/]")
                else:
                    console.print(Panel("[bold]Available audio files[/]", style="blue"))
                    for file in audio_files:
                        console.print(file)
            elif choice == '2':
                # List transcript files
                transcript_files = transcription.list_transcripts()
                
                if not transcript_files:
                    console.print("[yellow]No transcript files found.[/]")
                else:
                    console.print(Panel("[bold]Available transcript files[/]", style="blue"))
                    for file in transcript_files:
                        console.print(file)
            elif choice == '3':
                # List image files - Now uses Rich tables from the image_gen module
                image_files = image_gen.list_images()
                
            elif choice == '4':
                # List conversation files
                from whisper_transcription_tool import conversation
                conversation_files = conversation.list_conversations()
                
                if not conversation_files:
                    console.print("[yellow]No conversation files found.[/]")
                else:
                    console.print(Panel("[bold]Available conversation files[/]", style="blue"))
                    
            elif choice == '5':
                # Delete file
                console.print(Panel("[bold]What type of file would you like to delete?[/]", style="blue"))
                console.print("[1] Audio file")
                console.print("[2] Transcript file")
                console.print("[3] Image file")
                console.print("[4] Conversation file")
                
                file_type = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4"], default="1")
                
                if file_type == '1':
                    # Delete audio file
                    audio_files = audio.list_audio_files()
                    
                    if not audio_files:
                        console.print("[yellow]No audio files found.[/]")
                        continue
                        
                    console.print(Panel("[bold]Available audio files[/]", style="blue"))
                    for file in audio_files:
                        console.print(file)
                        
                    file_index = IntPrompt.ask("Enter the number of the file to delete (or 0 to cancel)", default=0)
                    
                    if file_index == 0:
                        continue
                    
                    try:
                        file_path = audio.get_audio_file_path(file_index)
                    except ValueError:
                        console.print("[bold red]Invalid input.[/]")
                        continue
                        
                    if file_path and os.path.exists(file_path):
                        confirm = Confirm.ask(f"Are you sure you want to delete {os.path.basename(file_path)}?")
                        if confirm:
                            if audio.delete_audio_file(file_path):
                                console.print("[bold green]File deleted successfully.[/]")
                elif file_type == '2':
                    # Delete transcript file
                    transcript_files = transcription.list_transcripts()
                    
                    if not transcript_files:
                        console.print("[yellow]No transcript files found.[/]")
                        continue
                        
                    console.print(Panel("[bold]Available transcript files[/]", style="blue"))
                    for file in transcript_files:
                        console.print(file)
                        
                    file_index = IntPrompt.ask("Enter the number of the file to delete (or 0 to cancel)", default=0)
                    
                    if file_index == 0:
                        continue
                    
                    try:
                        file_path = transcription.get_transcript_file_path(file_index)
                    except ValueError:
                        console.print("[bold red]Invalid input.[/]")
                        continue
                        
                    if file_path and os.path.exists(file_path):
                        confirm = Confirm.ask(f"Are you sure you want to delete {os.path.basename(file_path)}?")
                        if confirm:
                            try:
                                os.remove(file_path)
                                console.print("[bold green]File deleted successfully.[/]")
                            except Exception as e:
                                console.print(f"[bold red]Error deleting file:[/] {str(e)}")
                elif file_type == '3':
                    # Delete image file
                    image_files = image_gen.list_images()
                    
                    if not image_files:
                        continue
                        
                    file_index = IntPrompt.ask("Enter the number of the file to delete (or 0 to cancel)", default=0)
                    
                    if file_index == 0:
                        continue
                    
                    try:
                        file_path = image_gen.get_image_path(file_index)
                    except ValueError:
                        console.print("[bold red]Invalid input.[/]")
                        continue
                        
                    if file_path and os.path.exists(file_path):
                        confirm = Confirm.ask(f"Are you sure you want to delete {os.path.basename(file_path)}?")
                        if confirm:
                            try:
                                os.remove(file_path)
                                console.print("[bold green]File deleted successfully.[/]")
                            except Exception as e:
                                console.print(f"[bold red]Error deleting file:[/] {str(e)}")
                elif file_type == '4':
                    # Delete conversation file
                    from whisper_transcription_tool import conversation
                    conversation_files = conversation.list_conversations()
                    
                    if not conversation_files:
                        console.print("[yellow]No conversation files found.[/]")
                        continue
                    
                    file_index = IntPrompt.ask("Enter the number of the file to delete (or 0 to cancel)", default=0)
                    
                    if file_index == 0:
                        continue
                    
                    try:
                        file_path = conversation.get_conversation_file_path(file_index)
                    except ValueError:
                        console.print("[bold red]Invalid input.[/]")
                        continue
                        
                    if file_path and os.path.exists(file_path):
                        confirm = Confirm.ask(f"Are you sure you want to delete {os.path.basename(file_path)}?")
                        if confirm:
                            try:
                                os.remove(file_path)
                                console.print("[bold green]File deleted successfully.[/]")
                            except Exception as e:
                                console.print(f"[bold red]Error deleting file:[/] {str(e)}")
                else:
                    console.print("[bold red]Invalid choice.[/]")
            else:
                console.print("[bold red]Invalid choice. Please try again.[/]")
        
    except Exception as e:
        console.print(f"[bold red]Error in file management workflow:[/] {str(e)}")


def main() -> None:
    """Main application entry point."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Whisper Transcription Tool")
    parser.add_argument("--record", action="store_true", help="Record audio")
    parser.add_argument("--transcribe", metavar="FILE", help="Transcribe audio file")
    parser.add_argument("--duration", type=int, default=0, help="Recording duration in seconds (0 for manual stop)")
    args = parser.parse_args()
    
    # Create necessary directories
    config.create_directories()
    
    # Load OpenAI API key
    if not load_api_key():
        sys.exit(1)
        
    # Handle command-line actions
    if args.record:
        audio.record_audio(args.duration)
        sys.exit(0)
    elif args.transcribe:
        if os.path.exists(args.transcribe):
            transcription.transcribe_audio(args.transcribe)
        else:
            console.print(f"[bold red]Error:[/] File {args.transcribe} not found.")
        sys.exit(0)
    
    # Main application loop
    try:
        while True:
            display_main_menu()
            choice = Prompt.ask("Enter your choice", choices=["0", "1", "2", "3", "4", "5"], default="0")
            
            if choice == '0':
                console.print("[green]Exiting...[/]")
                break
            elif choice == '1':
                record_audio_workflow()
            elif choice == '2':
                transcribe_audio_workflow()
            elif choice == '3':
                process_transcript_workflow()
            elif choice == '4':
                generate_image_workflow()
            elif choice == '5':
                file_management_workflow()
            else:
                console.print("[bold red]Invalid choice. Please try again.[/]")
    except KeyboardInterrupt:
        console.print("\n[green]Exiting...[/]")
    except Exception as e:
        console.print(f"[bold red]An error occurred:[/] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()