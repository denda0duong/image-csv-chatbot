"""
Chat history management service.
"""

import streamlit as st
from typing import List, Dict
from ..models.message import ChatMessage


class ChatHistoryManager:
    """Manages chat history stored in Streamlit session state."""
    
    SESSION_KEY = "messages"
    
    @staticmethod
    def initialize() -> None:
        """Initialize chat history in session state if it doesn't exist."""
        if ChatHistoryManager.SESSION_KEY not in st.session_state:
            st.session_state[ChatHistoryManager.SESSION_KEY] = []
    
    @staticmethod
    def get_messages() -> List[Dict[str, str]]:
        """
        Get all messages from the chat history.
        
        Returns:
            List of message dictionaries with 'role' and 'content' keys
        """
        return st.session_state.get(ChatHistoryManager.SESSION_KEY, [])
    
    @staticmethod
    def add_message(role: str, content: str) -> None:
        """
        Add a message to the chat history.
        
        Args:
            role: The role of the message sender
            content: The content of the message
        """
        message = ChatMessage(role=role, content=content)
        st.session_state[ChatHistoryManager.SESSION_KEY].append(message.to_dict())
    
    @staticmethod
    def clear() -> None:
        """Clear all messages from the chat history."""
        st.session_state[ChatHistoryManager.SESSION_KEY] = []
    
    @staticmethod
    def get_message_count() -> int:
        """
        Get the total number of messages in the chat history.
        
        Returns:
            Number of messages
        """
        return len(ChatHistoryManager.get_messages())
    
    @staticmethod
    def get_last_n_messages(n: int) -> List[Dict[str, str]]:
        """
        Get the last N messages from history.
        
        Args:
            n: Number of messages to retrieve
            
        Returns:
            List of the last N messages
        """
        messages = ChatHistoryManager.get_messages()
        return messages[-n:] if n < len(messages) else messages
