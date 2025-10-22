"""
Streamlit Chatbot Application
A multi-turn chat interface powered by Google Gemini API

This is the main entry point for the application. The code is organized
into separate modules for better maintainability and scalability.
"""

import streamlit as st
from src.models.constants import MessageRole
from src.services.chat_history import ChatHistoryManager
from src.services.gemini_service import GeminiChatService
from src.services.response_handler import ResponseHandler
from src.ui.chat import ChatUI
from src.ui.sidebar import SidebarUI
from logger_config import LoggerConfig, get_logger

# Initialize logging
LoggerConfig.setup_logging()
logger = get_logger(__name__)


class ChatbotApp:
    """
    Main application orchestrator.
    
    This class coordinates all components of the chatbot application,
    following the Single Responsibility Principle with each component
    handling a specific aspect of the functionality.
    """
    
    def __init__(self):
        """Initialize the chatbot application with all required services."""
        logger.info("Initializing ChatbotApp")
        self.chat_service = GeminiChatService()
        self.response_handler = ResponseHandler(self.chat_service)
        self.history_manager = ChatHistoryManager()
        logger.info("ChatbotApp initialized successfully")
    
    def run(self) -> None:
        """
        Run the main application loop.
        
        This method orchestrates the entire application flow:
        1. Configure the page
        2. Initialize state
        3. Render UI components
        4. Handle user interactions
        """
        logger.debug("Running main application loop")
        
        # Setup
        ChatUI.configure_page()
        self.history_manager.initialize()
        
        # Main UI
        ChatUI.render_header()
        ChatUI.render_messages(self.history_manager.get_messages())
        
        # Handle user input
        self._handle_user_input()
        
        # Sidebar
        SidebarUI.render(self.history_manager.get_message_count())
    
    def _handle_user_input(self) -> None:
        """
        Handle user input from the chat interface.
        
        When a user submits a message:
        1. Add it to chat history
        2. Display the message with timestamp
        3. Generate and display AI response
        4. Handle optional image input
        """
        if prompt := ChatUI.get_user_input():
            logger.info(f"User submitted message (length: {len(prompt)} chars)")
            
            # Check if there's an uploaded image
            uploaded_image = st.session_state.get('uploaded_image', None)
            if uploaded_image:
                logger.info("User message includes an image")
            
            # Store user message with timestamp
            self.history_manager.add_message(MessageRole.USER.value, prompt)
            
            # Get the last message (just added) to display with timestamp
            messages = self.history_manager.get_messages()
            last_message = messages[-1] if messages else None
            
            # Display user message with timestamp
            if last_message:
                ChatUI.display_message(
                    MessageRole.USER.value, 
                    prompt,
                    last_message.get("timestamp")
                )
                
                # If there's an image, display it in the chat
                if uploaded_image:
                    with st.chat_message(MessageRole.USER.value):
                        st.image(uploaded_image, caption="Uploaded Image", width="stretch")
            
            # Generate and display AI response (with image if present)
            self.response_handler.handle_response(prompt, image=uploaded_image)
            
            # Clear the image from session state after processing
            if uploaded_image and 'uploaded_image' in st.session_state:
                del st.session_state['uploaded_image']
                logger.info("Cleared uploaded image from session state")


def main() -> None:
    """
    Application entry point.
    
    Creates and runs the chatbot application instance.
    """
    app = ChatbotApp()
    app.run()


if __name__ == "__main__":
    main()
