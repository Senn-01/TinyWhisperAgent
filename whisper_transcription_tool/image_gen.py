import os
import requests
from PIL import Image
from io import BytesIO
import openai
from typing import Optional, Literal, List
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich import box

# Constants
IMAGES_DIR = "data/images"

# Create necessary directories if they don't exist
os.makedirs(IMAGES_DIR, exist_ok=True)

# Initialize Rich console
console = Console()

def generate_image_from_transcript(transcript: str, quality: str = "standard") -> Optional[str]:
    """
    Generate an image based on the transcript using OpenAI's GPT-Image-1 model.
    
    Args:
        transcript: The text to base the image generation on
        quality: Image quality ("standard" or "hd")
        
    Returns:
        Optional[str]: Path to the saved image or None if generation failed
    """
    try:
        console.print("[bold blue]Creating image prompt from transcript...[/]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Processing transcript...[/]"),
            TimeElapsedColumn(),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("Generating prompt", total=None)
            
            # First, use GPT to create a good image prompt
            response = openai.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates detailed, vivid image generation prompts. Your prompts should capture the essence of the text and translate it into visual concepts. Be specific about style, mood, colors, composition, and other visual elements. Limit your response to 1000 characters."},
                    {"role": "user", "content": f"Create a detailed image generation prompt based on this transcript:\n\n{transcript}"}
                ]
            )
            
            image_prompt = response.choices[0].message.content
            progress.update(task, completed=True)
        
        console.print(Panel(f"[italic]{image_prompt}[/]", title="Generated Image Prompt", border_style="green"))
        
        # Now generate the image using GPT-Image-1
        console.print("[bold blue]Generating image with GPT-Image-1...[/]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Creating image...[/]"),
            TimeElapsedColumn(),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("Generating image", total=None)
            
            # Map UI options to API quality values
            # The API expects "low", "medium", "high", or "auto" for quality
            quality_map = {
                "1": "medium",  # Standard quality maps to "medium"
                "2": "high",    # HD quality maps to "high"
                "standard": "medium",
                "hd": "high"
            }
            
            api_quality = quality_map.get(quality, "medium")  # Default to medium if not in map
                
            # Generate the image with correct parameters
            image_response = openai.images.generate(
                model="gpt-image-1",
                prompt=image_prompt,
                size="1024x1024",
                quality=api_quality,
                n=1
            )
            
            # Get the image URL with error handling
            image_url = image_response.data[0].url if image_response.data and hasattr(image_response.data[0], 'url') else None
            
            # Check if URL is valid
            if not image_url:
                console.print("[bold red]Error: Image generation API did not return a valid URL[/]")
                progress.update(task, completed=True)
                return None
                
            progress.update(task, completed=True)
        
        # Download and save the image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gpt_image_{timestamp}.png"
        filepath = os.path.join(IMAGES_DIR, filename)
        
        # Download and save the image
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Downloading image...[/]"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task = progress.add_task("Downloading", total=100)
            success = download_image(image_url, filepath, progress, task)
            
        if success:
            console.print(f"[bold green]Image generated and saved to[/] [bold yellow]{filepath}[/]")
            return filepath
        else:
            console.print("[bold red]Failed to download the image.[/]")
            return None
        
    except Exception as e:
        console.print(f"[bold red]Error generating image from transcript:[/] {str(e)}")
        return None


def generate_image_from_prompt(prompt: str, quality: str = "standard") -> Optional[str]:
    """
    Generate an image based on a user-provided prompt using OpenAI's GPT-Image-1 model.
    
    Args:
        prompt: The prompt for image generation
        quality: Image quality ("standard" or "hd")
        
    Returns:
        Optional[str]: Path to the saved image or None if generation failed
    """
    try:
        console.print("[bold blue]Generating image with GPT-Image-1...[/]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Creating image...[/]"),
            TimeElapsedColumn(),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("Generating image", total=None)
            
            # Map UI options to API quality values
            # The API expects "low", "medium", "high", or "auto" for quality
            quality_map = {
                "1": "medium",  # Standard quality maps to "medium"
                "2": "high",    # HD quality maps to "high"
                "standard": "medium",
                "hd": "high"
            }
            
            api_quality = quality_map.get(quality, "medium")  # Default to medium if not in map
                
            # Generate the image with correct parameters
            image_response = openai.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size="1024x1024",
                quality=api_quality,
                n=1
            )
            
            # Get the image URL with error handling
            image_url = image_response.data[0].url if image_response.data and hasattr(image_response.data[0], 'url') else None
            
            # Check if URL is valid
            if not image_url:
                console.print("[bold red]Error: Image generation API did not return a valid URL[/]")
                progress.update(task, completed=True)
                return None
                
            progress.update(task, completed=True)
        
        # Download and save the image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gpt_image_{timestamp}.png"
        filepath = os.path.join(IMAGES_DIR, filename)
        
        # Download and save the image
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Downloading image...[/]"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task = progress.add_task("Downloading", total=100)
            success = download_image(image_url, filepath, progress, task)
            
        if success:
            console.print(f"[bold green]Image generated and saved to[/] [bold yellow]{filepath}[/]")
            return filepath
        else:
            console.print("[bold red]Failed to download the image.[/]")
            return None
        
    except Exception as e:
        console.print(f"[bold red]Error generating image from prompt:[/] {str(e)}")
        return None


def download_image(url: str, filepath: str, progress=None, task_id=None) -> bool:
    """
    Download an image from a URL and save it to a file.
    
    Args:
        url: The URL of the image
        filepath: The path to save the image to
        progress: Optional Progress instance for updating download progress
        task_id: ID of the task in the progress bar
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Validate URL before making request
        if not url or url == "None":
            console.print(f"[bold red]Error downloading image:[/] Invalid URL '{url}': No scheme supplied.")
            return False
            
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Get total size in bytes
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        
        if progress and task_id:
            progress.update(task_id, total=total_size if total_size > 0 else 100)
            progress.start_task(task_id)
        
        content = BytesIO()
        downloaded = 0
        
        for data in response.iter_content(block_size):
            content.write(data)
            downloaded += len(data)
            if progress and task_id and total_size > 0:
                progress.update(task_id, completed=downloaded)
        
        content.seek(0)
        image = Image.open(content)
        image.save(filepath)
        
        if progress and task_id:
            progress.update(task_id, completed=total_size if total_size > 0 else 100)
        
        return True
        
    except Exception as e:
        console.print(f"[bold red]Error downloading image:[/] {str(e)}")
        return False


def list_images() -> List[str]:
    """
    List all images in the images directory.
    
    Returns:
        List[str]: List of formatted image file descriptions
    """
    try:
        files = os.listdir(IMAGES_DIR)
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
        
        if not image_files:
            console.print("[yellow]No image files found.[/]")
            return []
            
        # Sort files by modification time (newest first)
        image_files.sort(key=lambda x: os.path.getmtime(os.path.join(IMAGES_DIR, x)), reverse=True)
        
        # Create a table for display
        table = Table(box=box.ROUNDED, title="Available Images", show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Filename", style="cyan")
        table.add_column("Size", style="green")
        table.add_column("Date", style="blue")
        
        # Format the list for display
        formatted_list = []
        for i, file in enumerate(image_files):
            file_path = os.path.join(IMAGES_DIR, file)
            size_kb = os.path.getsize(file_path) / 1024
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
            
            # Add to table
            table.add_row(
                str(i+1),
                file,
                f"{size_kb:.2f} KB",
                mod_time
            )
            
            # Also add to formatted list for return
            formatted_list.append(f"{i+1}. {file} ({size_kb:.2f} KB) - {mod_time}")
        
        console.print(table)
        return formatted_list
        
    except Exception as e:
        console.print(f"[bold red]Error listing image files:[/] {str(e)}")
        return []


def get_image_path(index: int) -> Optional[str]:
    """
    Get the path to an image file by its index in the list.
    
    Args:
        index: Index of the image file (1-based)
        
    Returns:
        Optional[str]: Path to the image file or None if not found
    """
    try:
        files = os.listdir(IMAGES_DIR)
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
        
        if not image_files:
            console.print("[yellow]No image files found.[/]")
            return None
            
        # Sort files by modification time (newest first)
        image_files.sort(key=lambda x: os.path.getmtime(os.path.join(IMAGES_DIR, x)), reverse=True)
        
        if index < 1 or index > len(image_files):
            console.print(f"[bold red]Invalid file index.[/] Please choose a number between 1 and {len(image_files)}.")
            return None
            
        file_path = os.path.join(IMAGES_DIR, image_files[index-1])
        return file_path
        
    except Exception as e:
        console.print(f"[bold red]Error getting image file path:[/] {str(e)}")
        return None