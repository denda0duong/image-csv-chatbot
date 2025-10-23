"""
Chat history management service.
"""

import streamlit as st
from typing import List, Dict, Optional
from ..models.message import ChatMessage
from .persistence_service import PersistenceService
from logger_config import get_logger

logger = get_logger(__name__)


class ChatHistoryManager:
    """Manages chat history stored in Streamlit session state with file persistence."""
    
    SESSION_KEY = "messages"
    SESSION_ID_KEY = "session_id"
    
    @staticmethod
    def initialize() -> None:
        """Initialize chat history in session state if it doesn't exist."""
        # Initialize persistence service
        PersistenceService.initialize()
        
        # Check if this is a fresh session (after page refresh)
        if ChatHistoryManager.SESSION_KEY not in st.session_state:
            # Try to load the most recent session
            sessions = PersistenceService.list_sessions()
            
            if sessions:
                # Load the most recent session (sessions are sorted newest first)
                most_recent = sessions[0]
                session_id = most_recent['session_id']
                loaded_messages = PersistenceService.load_session(session_id)
                
                if loaded_messages:
                    st.session_state[ChatHistoryManager.SESSION_KEY] = loaded_messages
                    st.session_state[ChatHistoryManager.SESSION_ID_KEY] = session_id
                    logger.info(f"Restored most recent session: {session_id} ({len(loaded_messages)} messages)")
                else:
                    # Failed to load, create new session
                    ChatHistoryManager._create_new_session()
            else:
                # No existing sessions, create new
                ChatHistoryManager._create_new_session()
        
        # Ensure session ID exists
        if ChatHistoryManager.SESSION_ID_KEY not in st.session_state:
            session_id = PersistenceService.generate_session_id()
            st.session_state[ChatHistoryManager.SESSION_ID_KEY] = session_id
            logger.info(f"Session ID created: {session_id}")
    
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
        Add a message to the chat history and persist to disk.
        
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
        
        # Auto-save to file after each message
        ChatHistoryManager._save_to_file()
    
    @staticmethod
    def clear() -> None:
        """Clear all messages from the chat history and create new session."""
        message_count = len(st.session_state.get(ChatHistoryManager.SESSION_KEY, []))
        
        # Delete old session file
        if ChatHistoryManager.SESSION_ID_KEY in st.session_state:
            old_session_id = st.session_state[ChatHistoryManager.SESSION_ID_KEY]
            PersistenceService.delete_session(old_session_id)
        
        # Clear messages
        st.session_state[ChatHistoryManager.SESSION_KEY] = []
        
        # Generate new session ID
        new_session_id = PersistenceService.generate_session_id()
        st.session_state[ChatHistoryManager.SESSION_ID_KEY] = new_session_id
        
        logger.info(f"Cleared chat history ({message_count} messages removed) - New session: {new_session_id}")
    
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
    
    @staticmethod
    def _save_to_file() -> None:
        """Save current chat history to file."""
        try:
            session_id = st.session_state.get(ChatHistoryManager.SESSION_ID_KEY)
            messages = st.session_state.get(ChatHistoryManager.SESSION_KEY, [])
            
            if session_id and messages:
                PersistenceService.save_session(session_id, messages)
        except Exception as e:
            logger.error(f"Error saving chat history: {str(e)}", exc_info=True)
    
    @staticmethod
    def _create_new_session() -> None:
        """Create a new empty session."""
        session_id = PersistenceService.generate_session_id()
        st.session_state[ChatHistoryManager.SESSION_KEY] = []
        st.session_state[ChatHistoryManager.SESSION_ID_KEY] = session_id
        logger.info(f"New session created: {session_id}")
