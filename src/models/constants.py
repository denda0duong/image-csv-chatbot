"""
Constants and enums used throughout the application.
"""

from enum import Enum


class MessageRole(Enum):
    """Enum for message roles in the chat."""
    USER = "user"
    ASSISTANT = "assistant"
    MODEL = "model"


class AppConfig:
    """Application configuration constants."""
    
    # UI Configuration
    PAGE_TITLE = "Image CSV Chatbot"
    PAGE_ICON = "🤖"
    LAYOUT = "centered"
    
    # Chat Configuration
    DEFAULT_PROMPT = "Ask me anything..."
    THINKING_MESSAGE = "Thinking..."
    GENERATING_MESSAGE = "Generating response..."
    COMPLETE_MESSAGE = "Complete!"
    ERROR_MESSAGE = "Error occurred"
    
    # Error Messages
    API_ERROR_TEMPLATE = (
        "❌ Error: {error}\n\n"
        "Please check your API key in the .env file and try again."
    )
