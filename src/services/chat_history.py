"""
Chat history management service.
"""

import streamlit as st
from typing import List, Dict, Optional
from ..models.message import ChatMessage
from logger_config import get_logger

logger = get_logger(__name__)


class ChatHistoryManager:
    """Manages chat history stored in Streamlit session state."""
    
    SESSION_KEY = "messages"
    
    @staticmethod
    def initialize() -> None:
        """Initialize chat history in session state if it doesn't exist."""
        if ChatHistoryManager.SESSION_KEY not in st.session_state:
            st.session_state[ChatHistoryManager.SESSION_KEY] = []
            logger.info("Chat history initialized")
    
    @staticmethod
    def get_messages() -> List[Dict]:
        """
        Get all messages from the chat history.
        
        Returns:
            List of message dictionaries with 'role', 'content', and optional 'plots' keys
        """
        messages = st.session_state.get(ChatHistoryManager.SESSION_KEY, [])
        logger.debug(f"Retrieved {len(messages)} messages from history")
        return messages
    
    @staticmethod
    def add_message(role: str, content: str, plots: Optional[List[bytes]] = None, image: Optional[bytes] = None) -> None:
        """
        Add a message to the chat history.
        
        Args:
            role: The role of the message sender
            content: The content of the message
            plots: Optional list of plot image data (as bytes)
            image: Optional user-uploaded image data (as bytes)
        """
        message = ChatMessage(role=role, content=content, plots=plots or [], image=image)
        st.session_state[ChatHistoryManager.SESSION_KEY].append(message.to_dict())
        plot_info = f" with {len(plots)} plot(s)" if plots else ""
        image_info = " with image" if image else ""
        logger.info(f"Added {role} message to history (length: {len(content)} chars{plot_info}{image_info})")
    
    @staticmethod
    def clear() -> None:
        """Clear all messages from the chat history."""
        message_count = len(st.session_state.get(ChatHistoryManager.SESSION_KEY, []))
        st.session_state[ChatHistoryManager.SESSION_KEY] = []
        logger.info(f"Cleared chat history ({message_count} messages removed)")
    
    @staticmethod
    def get_message_count() -> int:
        """
        Get the total number of messages in the chat history.
        
        Returns:
            Number of messages
        """
        return len(ChatHistoryManager.get_messages())
    
    @staticmethod
    def get_last_n_messages(n: int) -> List[Dict]:
        """
        Get the last N messages from history.
        
        Args:
            n: Number of messages to retrieve
            
        Returns:
            List of the last N messages
        """
        messages = ChatHistoryManager.get_messages()
        return messages[-n:] if n < len(messages) else messages
