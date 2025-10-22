"""
Response handler for managing AI responses.
"""

import streamlit as st
from ..models.constants import MessageRole, AppConfig
from ..services.gemini_service import GeminiChatService
from ..services.chat_history import ChatHistoryManager
from ..ui.chat import ChatUI
from logger_config import get_logger

logger = get_logger(__name__)


class ResponseHandler:
    """Handles generating and displaying AI responses."""
    
    def __init__(self, chat_service: GeminiChatService):
        """
        Initialize the response handler.
        
        Args:
            chat_service: The Gemini chat service instance
        """
        self.chat_service = chat_service
    
    def handle_response(self, prompt: str) -> None:
        """
        Generate and display the AI response.
        
        Args:
            prompt: The user's input prompt
        """
        logger.info("Handling user prompt")
        
        with st.chat_message(MessageRole.ASSISTANT.value):
            with st.status(AppConfig.THINKING_MESSAGE, expanded=False) as status:
                try:
                    # Update status
                    status.update(label=AppConfig.GENERATING_MESSAGE, state="running")
                    
                    # Get streaming response
                    response_stream = self.chat_service.get_response_stream(
                        prompt, 
                        ChatHistoryManager.get_messages()
                    )
                    
                    # Display streamed response
                    full_response = ChatUI.display_streaming_response(response_stream)
                    
                    # Update status
                    status.update(label=AppConfig.COMPLETE_MESSAGE, state="complete")
                    logger.info("Response displayed successfully")
                    
                except Exception as e:
                    # Handle errors gracefully
                    logger.error(f"Error handling response: {str(e)}", exc_info=True)
                    full_response = AppConfig.API_ERROR_TEMPLATE.format(error=str(e))
                    ChatUI.display_error(full_response)
                    status.update(label=AppConfig.ERROR_MESSAGE, state="error")
            
            # Add response to history with timestamp
            ChatHistoryManager.add_message(MessageRole.ASSISTANT.value, full_response)
            
            # Display timestamp for the assistant's response if enabled
            show_timestamps = st.session_state.get("show_timestamps", True)
            if show_timestamps:
                messages = ChatHistoryManager.get_messages()
                if messages:
                    last_message = messages[-1]
                    if "timestamp" in last_message:
                        st.caption(f"🕐 {last_message['timestamp']}")
