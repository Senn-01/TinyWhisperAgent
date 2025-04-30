import os
import openai
from typing import Optional, Dict, Any, List
from datetime import datetime

# Constants
PROCESSED_DIR = "data/processed"

# Create necessary directories if they don't exist
os.makedirs(PROCESSED_DIR, exist_ok=True)

def get_summary(transcript: str) -> Optional[str]:
    """
    Generate a summary of the transcript using OpenAI's GPT model.
    
    Args:
        transcript: The text to summarize
        
    Returns:
        Optional[str]: The generated summary or None if generation failed
    """
    try:
        print("Generating summary...")
        
        response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates concise, insightful summaries. Identify the main topics, key points, and conclusions."},
                {"role": "user", "content": f"Please summarize the following transcript:\n\n{transcript}"}
            ]
        )
        
        summary = response.choices[0].message.content
        
        # Save the summary to a file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"summary_{timestamp}.txt"
        filepath = os.path.join(PROCESSED_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(summary)
            
        print(f"Summary saved to {filepath}")
        return summary
        
    except Exception as e:
        print(f"Error generating summary: {e}")
        return None


def get_key_points(transcript: str) -> Optional[str]:
    """
    Extract key points from a transcript using OpenAI's GPT model.
    
    Args:
        transcript: The text to analyze
        
    Returns:
        Optional[str]: The extracted key points or None if extraction failed
    """
    try:
        print("Extracting key points...")
        
        response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that identifies and extracts the most important points from text. Format as a bulleted list with clear, concise statements."},
                {"role": "user", "content": f"Please extract the key points from the following transcript as a bulleted list:\n\n{transcript}"}
            ]
        )
        
        key_points = response.choices[0].message.content
        
        # Save the key points to a file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"key_points_{timestamp}.txt"
        filepath = os.path.join(PROCESSED_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(key_points)
            
        print(f"Key points saved to {filepath}")
        return key_points
        
    except Exception as e:
        print(f"Error extracting key points: {e}")
        return None


def get_action_items(transcript: str) -> Optional[str]:
    """
    Extract action items from a transcript using OpenAI's GPT model.
    
    Args:
        transcript: The text to analyze
        
    Returns:
        Optional[str]: The extracted action items or None if extraction failed
    """
    try:
        print("Extracting action items...")
        
        response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that identifies action items, tasks, and commitments mentioned in text. Format as a prioritized list with clear ownership and timelines if mentioned."},
                {"role": "user", "content": f"Please extract all action items, tasks, and commitments from the following transcript as a bulleted list:\n\n{transcript}"}
            ]
        )
        
        action_items = response.choices[0].message.content
        
        # Save the action items to a file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"action_items_{timestamp}.txt"
        filepath = os.path.join(PROCESSED_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(action_items)
            
        print(f"Action items saved to {filepath}")
        return action_items
        
    except Exception as e:
        print(f"Error extracting action items: {e}")
        return None


def reformat_transcript(transcript: str, format_type: str = "clean") -> Optional[str]:
    """
    Reformat the transcript using OpenAI's GPT model.
    
    Args:
        transcript: The text to reformat
        format_type: The type of formatting to apply (clean, paragraphs, structured, qa, minutes, narrative)
        
    Returns:
        Optional[str]: The reformatted transcript or None if reformatting failed
    """
    # Define system prompts for different formatting options
    format_options = {
        "clean": {
            "system": "You are a helpful assistant that reformats transcripts into clean, readable text. Fix grammar, punctuation, and formatting without changing the content's meaning.",
            "user": "Please reformat this transcript into clean, readable text with proper grammar and punctuation."
        },
        "paragraphs": {
            "system": "You are a helpful assistant that reformats transcripts into paragraphs. Organize the text into coherent paragraphs with proper transitions.",
            "user": "Please reformat this transcript into well-structured paragraphs."
        },
        "structured": {
            "system": "You are a helpful assistant that reformats transcripts into a structured document with headings and sections.",
            "user": "Please reformat this transcript into a structured document with appropriate headings and sections."
        },
        "qa": {
            "system": "You are a helpful assistant that reformats transcripts into a Q&A format. Identify questions and answers in the conversation.",
            "user": "Please reformat this transcript into a Q&A format."
        },
        "minutes": {
            "system": "You are a helpful assistant that reformats transcripts into meeting minutes with action items, decisions, and discussion points.",
            "user": "Please reformat this transcript into meeting minutes with action items, decisions, and discussion points."
        },
        "narrative": {
            "system": "You are a helpful assistant that reformats transcripts into a narrative story, making the content more engaging while preserving the factual information.",
            "user": "Please reformat this transcript into a narrative story, making it more engaging while preserving the factual information."
        }
    }
    
    # Default to clean formatting if the specified format is not available
    format_info = format_options.get(format_type.lower(), format_options["clean"])
    
    try:
        print(f"Reformatting transcript to {format_type} format...")
        
        response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": format_info["system"]},
                {"role": "user", "content": f"{format_info['user']}\n\n{transcript}"}
            ]
        )
        
        reformatted = response.choices[0].message.content
        
        # Save the reformatted transcript to a file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reformatted_{format_type}_{timestamp}.txt"
        filepath = os.path.join(PROCESSED_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(reformatted)
            
        print(f"Reformatted transcript saved to {filepath}")
        return reformatted
        
    except Exception as e:
        print(f"Error reformatting transcript: {e}")
        return None


def translate_transcript(transcript: str, target_language: str) -> Optional[str]:
    """
    Translate the transcript to another language using OpenAI's GPT model.
    
    Args:
        transcript: The text to translate
        target_language: The language to translate to
        
    Returns:
        Optional[str]: The translated transcript or None if translation failed
    """
    try:
        print(f"Translating transcript to {target_language}...")
        
        response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that translates text to {target_language}. Maintain the original meaning and tone while producing natural, fluent text in the target language."},
                {"role": "user", "content": f"Please translate the following text to {target_language}:\n\n{transcript}"}
            ]
        )
        
        translated = response.choices[0].message.content
        
        # Save the translated transcript to a file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"translated_{target_language}_{timestamp}.txt"
        filepath = os.path.join(PROCESSED_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(translated)
            
        print(f"Translated transcript saved to {filepath}")
        return translated
        
    except Exception as e:
        print(f"Error translating transcript: {e}")
        return None


def analyze_sentiment(transcript: str) -> Optional[Dict[str, Any]]:
    """
    Analyze the sentiment of the transcript using OpenAI's GPT model.
    
    Args:
        transcript: The text to analyze
        
    Returns:
        Optional[Dict[str, Any]]: The sentiment analysis results or None if analysis failed
    """
    try:
        print("Analyzing sentiment...")
        
        response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes the sentiment of text. Provide a detailed analysis including overall sentiment (positive, negative, neutral), emotional tone, and notable sentiment shifts. Format as JSON with keys for 'overall_sentiment', 'confidence' (1-10), 'emotional_tone', 'key_positive_points', 'key_negative_points', and 'sentiment_shifts'."},
                {"role": "user", "content": f"Please analyze the sentiment of the following transcript and provide the results in JSON format:\n\n{transcript}"}
            ]
        )
        
        analysis = response.choices[0].message.content
        
        # Save the sentiment analysis to a file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sentiment_analysis_{timestamp}.txt"
        filepath = os.path.join(PROCESSED_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(analysis)
            
        print(f"Sentiment analysis saved to {filepath}")
        return analysis
        
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return None