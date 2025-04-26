import os
import requests
from PIL import Image
from io import BytesIO
import openai
from typing import Optional, Literal
from datetime import datetime

# Constants
IMAGES_DIR = "images"

# Create necessary directories if they don't exist
os.makedirs(IMAGES_DIR, exist_ok=True)

def generate_image_from_transcript(transcript: str, quality: Literal["standard", "hd"] = "standard") -> Optional[str]:
    """
    Generate an image based on the transcript using OpenAI's GPT-Image-1 model.
    
    Args:
        transcript: The text to base the image generation on
        quality: Image quality ("standard" or "hd")
        
    Returns:
        Optional[str]: Path to the saved image or None if generation failed
    """
    try:
        print("Creating image prompt from transcript...")
        
        # First, use GPT to create a good image prompt
        response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates detailed, vivid image generation prompts. Your prompts should capture the essence of the text and translate it into visual concepts. Be specific about style, mood, colors, composition, and other visual elements. Limit your response to 1000 characters."},
                {"role": "user", "content": f"Create a detailed image generation prompt based on this transcript:\n\n{transcript}"}
            ]
        )
        
        image_prompt = response.choices[0].message.content
        print(f"Generated image prompt: {image_prompt}")
        
        # Now generate the image using GPT-Image-1
        print("Generating image with GPT-Image-1 (this may take a moment)...")
        image_response = openai.images.generate(
            model="gpt-image-1",
            prompt=image_prompt,
            size="1024x1024",
            quality=quality,
            n=1
        )
        
        # Get the image URL
        image_url = image_response.data[0].url
        
        # Download and save the image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gpt_image_{timestamp}.png"
        filepath = os.path.join(IMAGES_DIR, filename)
        
        # Download and save the image
        download_image(image_url, filepath)
        
        print(f"Image generated and saved to {filepath}")
        return filepath
        
    except Exception as e:
        print(f"Error generating image from transcript: {e}")
        return None


def generate_image_from_prompt(prompt: str, quality: Literal["standard", "hd"] = "standard", style: Literal["vivid", "natural"] = "vivid") -> Optional[str]:
    """
    Generate an image based on a user-provided prompt using OpenAI's GPT-Image-1 model.
    
    Args:
        prompt: The prompt for image generation
        quality: Image quality ("standard" or "hd")
        style: Image style ("vivid" or "natural")
        
    Returns:
        Optional[str]: Path to the saved image or None if generation failed
    """
    try:
        print("Generating image with GPT-Image-1 (this may take a moment)...")
        image_response = openai.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
            quality=quality,
            style=style,
            n=1
        )
        
        # Get the image URL
        image_url = image_response.data[0].url
        
        # Download and save the image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gpt_image_{timestamp}.png"
        filepath = os.path.join(IMAGES_DIR, filename)
        
        # Download and save the image
        download_image(image_url, filepath)
        
        print(f"Image generated and saved to {filepath}")
        return filepath
        
    except Exception as e:
        print(f"Error generating image from prompt: {e}")
        return None


def download_image(url: str, filepath: str) -> bool:
    """
    Download an image from a URL and save it to a file.
    
    Args:
        url: The URL of the image
        filepath: The path to save the image to
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        image = Image.open(BytesIO(response.content))
        image.save(filepath)
        
        return True
        
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False


def list_images() -> list:
    """
    List all images in the images directory.
    
    Returns:
        list: List of image file paths
    """
    try:
        files = os.listdir(IMAGES_DIR)
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
        
        if not image_files:
            print("No image files found.")
            return []
            
        # Sort files by modification time (newest first)
        image_files.sort(key=lambda x: os.path.getmtime(os.path.join(IMAGES_DIR, x)), reverse=True)
        
        # Format the list for display
        formatted_list = []
        for i, file in enumerate(image_files):
            file_path = os.path.join(IMAGES_DIR, file)
            size_kb = os.path.getsize(file_path) / 1024
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
            formatted_list.append(f"{i+1}. {file} ({size_kb:.2f} KB) - {mod_time}")
            
        return formatted_list
        
    except Exception as e:
        print(f"Error listing image files: {e}")
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
            print("No image files found.")
            return None
            
        # Sort files by modification time (newest first)
        image_files.sort(key=lambda x: os.path.getmtime(os.path.join(IMAGES_DIR, x)), reverse=True)
        
        if index < 1 or index > len(image_files):
            print(f"Invalid file index. Please choose a number between 1 and {len(image_files)}.")
            return None
            
        file_path = os.path.join(IMAGES_DIR, image_files[index-1])
        return file_path
        
    except Exception as e:
        print(f"Error getting image file path: {e}")
        return None 