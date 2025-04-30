import os
import json
import openai
from typing import Optional, List, Dict, Any
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

# Constants
CONVERSATION_DIR = "data/conversation"

# Create necessary directories if they don't exist
os.makedirs(CONVERSATION_DIR, exist_ok=True)

# Initialize Rich console
console = Console()

class Conversation:
    """Class to handle conversation with AI assistant."""
    
    def __init__(self, transcript: Optional[str] = None):
        """
        Initialize a new conversation.
        
        Args:
            transcript: Optional transcript to initialize the conversation context
        """
        self.history = []
        self.start_time = datetime.now()
        
        # Add transcript as system message if provided
        if transcript:
            self.history.append({
                "role": "system", 
                "content": (
                    "You are a helpful assistant. The following is a transcript "
                    "that the user is referring to. Use this information to answer their questions:\n\n"
                    f"{transcript}"
                )
            })
        else:
            self.history.append({
                "role": "system",
                "content": "You are a helpful assistant."
            })
    
    def add_user_message(self, message: str) -> None:
        """
        Add a user message to the conversation history.
        
        Args:
            message: The message from the user
        """
        self.history.append({"role": "user", "content": message})
    
    def add_assistant_message(self, message: str) -> None:
        """
        Add an assistant message to the conversation history.
        
        Args:
            message: The message from the assistant
        """
        self.history.append({"role": "assistant", "content": message})
    
    def get_assistant_response(self) -> str:
        """
        Generate a response from the assistant using the conversation history.
        
        Returns:
            str: The assistant's response
        """
        try:
            console.print("[bold blue]Assistant is thinking...[/]")
            
            response = openai.chat.completions.create(
                model="gpt-4.1",
                messages=self.history,
                temperature=0.7,
                max_tokens=1000
            )
            
            assistant_message = response.choices[0].message.content
            self.add_assistant_message(assistant_message)
            
            return assistant_message
            
        except Exception as e:
            console.print(f"[bold red]Error getting assistant response: {str(e)}[/]")
            # Return a fallback message
            fallback_message = "I'm sorry, I encountered an issue processing your request. Please try again."
            self.add_assistant_message(fallback_message)
            return fallback_message
    
    def save_conversation(self) -> Optional[str]:
        """
        Save the conversation history to a file.
        
        Returns:
            Optional[str]: Path to the saved file or None if saving failed
        """
        try:
            timestamp = self.start_time.strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
            filepath = os.path.join(CONVERSATION_DIR, filename)
            
            # Create a conversation object to save
            conversation_data = {
                "timestamp": self.start_time.isoformat(),
                "history": self.history
            }
            
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(conversation_data, file, indent=2)
                
            console.print(f"[bold green]Conversation saved to {filepath}[/]")
            return filepath
            
        except Exception as e:
            console.print(f"[bold red]Error saving conversation: {str(e)}[/]")
            return None
    
    def display_conversation(self) -> None:
        """Display the conversation history in the console."""
        for message in self.history:
            if message["role"] == "user":
                console.print(Panel(message["content"], title="You", title_align="left", border_style="blue"))
            elif message["role"] == "assistant":
                console.print(Panel(Markdown(message["content"]), title="Assistant", title_align="left", border_style="green"))
            # Skip system messages in display

def interactive_conversation(transcript: Optional[str] = None) -> None:
    """
    Start an interactive conversation with the assistant.
    
    Args:
        transcript: Optional transcript to initialize the conversation context
    """
    try:
        conversation = Conversation(transcript)
        
        console.print(Panel(
            "[bold]Conversation with AI Assistant[/]\nType your questions below. Type 'exit', 'quit', or 'q' to end the conversation.",
            border_style="blue"
        ))
        
        while True:
            user_input = console.input("[bold blue]You:[/] ")
            
            # Check for exit commands
            if user_input.lower() in ["exit", "quit", "q"]:
                break
            
            conversation.add_user_message(user_input)
            
            # Get and display assistant response
            assistant_response = conversation.get_assistant_response()
            console.print(Panel(Markdown(assistant_response), title="Assistant", border_style="green"))
        
        # Save conversation when done
        conversation.save_conversation()
        console.print("[bold blue]Conversation ended.[/]")
        
    except KeyboardInterrupt:
        console.print("\n[bold blue]Conversation interrupted.[/]")
        # Try to save the conversation if it was interrupted
        if 'conversation' in locals():
            conversation.save_conversation()
    except Exception as e:
        console.print(f"[bold red]Error in conversation: {str(e)}[/]")

def list_conversations() -> List[str]:
    """
    List all saved conversations.
    
    Returns:
        List[str]: List of formatted conversation file descriptions
    """
    try:
        files = os.listdir(CONVERSATION_DIR)
        conversation_files = [f for f in files if f.lower().endswith('.json')]
        
        if not conversation_files:
            console.print("[yellow]No conversation files found.[/]")
            return []
            
        # Sort files by modification time (newest first)
        conversation_files.sort(key=lambda x: os.path.getmtime(os.path.join(CONVERSATION_DIR, x)), reverse=True)
        
        # Format the list for display
        formatted_list = []
        for i, file in enumerate(conversation_files):
            file_path = os.path.join(CONVERSATION_DIR, file)
            size_kb = os.path.getsize(file_path) / 1024
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
            
            formatted_list.append(f"{i+1}. {file} ({size_kb:.2f} KB) - {mod_time}")
            console.print(f"{i+1}. {file} ({size_kb:.2f} KB) - {mod_time}")
            
        return formatted_list
        
    except Exception as e:
        console.print(f"[bold red]Error listing conversation files: {str(e)}[/]")
        return []

def get_conversation_file_path(index: int) -> Optional[str]:
    """
    Get the path to a conversation file by its index in the list.
    
    Args:
        index: Index of the conversation file (1-based)
        
    Returns:
        Optional[str]: Path to the conversation file or None if not found
    """
    try:
        files = os.listdir(CONVERSATION_DIR)
        conversation_files = [f for f in files if f.lower().endswith('.json')]
        
        if not conversation_files:
            console.print("[yellow]No conversation files found.[/]")
            return None
            
        # Sort files by modification time (newest first)
        conversation_files.sort(key=lambda x: os.path.getmtime(os.path.join(CONVERSATION_DIR, x)), reverse=True)
        
        if index < 1 or index > len(conversation_files):
            console.print(f"[bold red]Invalid file index.[/] Please choose a number between 1 and {len(conversation_files)}.")
            return None
            
        file_path = os.path.join(CONVERSATION_DIR, conversation_files[index-1])
        return file_path
        
    except Exception as e:
        console.print(f"[bold red]Error getting conversation file path: {str(e)}[/]")
        return None

def load_conversation(file_path: str) -> Optional[Conversation]:
    """
    Load a conversation from a file.
    
    Args:
        file_path: Path to the conversation file
        
    Returns:
        Optional[Conversation]: Loaded conversation or None if loading failed
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        conversation = Conversation()
        conversation.history = data["history"]
        conversation.start_time = datetime.fromisoformat(data["timestamp"])
        
        return conversation
        
    except Exception as e:
        console.print(f"[bold red]Error loading conversation: {str(e)}[/]")
        return None 