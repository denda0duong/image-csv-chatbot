"""
Chat UI component.
"""

import streamlit as st
from typing import List, Dict
from ..models.constants import MessageRole, AppConfig


class ChatUI:
    """Handles chat UI components."""
    
    @staticmethod
    def configure_page() -> None:
        """Configure the Streamlit page settings."""
        st.set_page_config(
            page_title=AppConfig.PAGE_TITLE,
            page_icon=AppConfig.PAGE_ICON,
            layout=AppConfig.LAYOUT
        )
    
    @staticmethod
    def render_header() -> None:
        """Render the application header."""
        st.title(f"{AppConfig.PAGE_ICON} {AppConfig.PAGE_TITLE}")
        st.caption("Powered by Google Gemini AI")
    
    @staticmethod
    def render_messages(messages: List[Dict[str, str]]) -> None:
        """
        Render all messages in the chat history.
        
        Args:
            messages: List of message dictionaries to display
        """
        for message in messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    @staticmethod
    def get_user_input() -> str:
        """
        Get user input from the chat input widget.
        
        Returns:
            The user's input text, or empty string if no input
        """
        return st.chat_input(AppConfig.DEFAULT_PROMPT)
    
    @staticmethod
    def display_message(role: str, content: str) -> None:
        """
        Display a single message.
        
        Args:
            role: The role of the message sender
            content: The content to display
        """
        with st.chat_message(role):
            st.markdown(content)
    
    @staticmethod
    def display_streaming_response(response_generator) -> str:
        """
        Display a streaming response from the AI.
        
        Args:
            response_generator: Generator yielding response chunks
            
        Returns:
            The complete response text
        """
        return st.write_stream(response_generator)
    
    @staticmethod
    def display_error(error_message: str) -> None:
        """
        Display an error message.
        
        Args:
            error_message: The error message to display
        """
        st.error(error_message)
