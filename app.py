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
from src.services.csv_service import CSVService
from src.services.prompts import DataAnalystPrompts
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
        5. Handle optional CSV data (via file upload to Gemini)
        """
        if prompt := ChatUI.get_user_input():
            logger.info(f"User submitted message (length: {len(prompt)} chars)")
            
            # Check if there's an uploaded image
            uploaded_image = st.session_state.get('uploaded_image', None)
            if uploaded_image:
                logger.info("User message includes an image")
            
            # Check if there's a loaded CSV DataFrame
            df = st.session_state.get('df', None)
            uploaded_csv_file = None
            
            if df is not None:
                logger.info(f"[REQUEST] CSV present: {df.shape[0]} rows × {df.shape[1]} cols")
                
                # Validate token limits before uploading
                import time
                validate_start = time.time()
                test_prompt = DataAnalystPrompts.get_file_upload_prompt(prompt)
                validation = CSVService.validate_token_limit(df, test_prompt)
                validate_time = time.time() - validate_start
                logger.info(f"[REQUEST] Token validation: {validate_time:.2f}s - {validation['message']}")
                
                if not validation['is_valid']:
                    logger.warning(f"[REQUEST] Token limit exceeded: {validation['estimated_total_tokens']:,} tokens")
                    st.error(f"❌ **Token Limit Exceeded**\n\n{validation['message']}\n\n"
                            "Reduce dataset size by filtering rows or removing columns.")
                    return
                
                if validation['estimated_total_tokens'] > 500_000:
                    st.info(f"ℹ️ Large dataset - {validation['message']}")
                
                # Upload CSV to Gemini
                if 'uploaded_csv_file' not in st.session_state or st.session_state.get('csv_changed', True):
                    logger.info("[REQUEST] Uploading CSV to Gemini...")
                    uploaded_csv_file = CSVService.upload_csv_to_gemini(df)
                    if uploaded_csv_file:
                        st.session_state['uploaded_csv_file'] = uploaded_csv_file
                        st.session_state['csv_changed'] = False
                        logger.info("[REQUEST] CSV upload successful")
                    else:
                        logger.error("[REQUEST] CSV upload failed")
                else:
                    uploaded_csv_file = st.session_state.get('uploaded_csv_file')
                    logger.info(f"[REQUEST] Using cached uploaded file: {uploaded_csv_file.name if uploaded_csv_file else 'None'}")
            
            # Prepare enhanced prompt
            enhanced_prompt = prompt
            if uploaded_csv_file:
                enhanced_prompt = DataAnalystPrompts.get_file_upload_prompt(prompt)
                logger.info(f"[REQUEST] Enhanced prompt: {len(enhanced_prompt)} chars")
            elif df is not None:
                logger.error("[REQUEST] CSV present but upload failed")
                st.error("❌ Upload failed - please reload the CSV file")
                return
            
            logger.info(f"[REQUEST] Sending to AI - User prompt: '{prompt[:100]}...'")
            
            # Store user message with timestamp (original prompt, not enhanced)
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
                
                # If there's CSV data, show indicator in chat
                if df is not None:
                    with st.chat_message(MessageRole.USER.value):
                        upload_status = "📤 File uploaded to Gemini" if uploaded_csv_file else "⚠️ Upload failed"
                        st.caption(f"{upload_status}: {df.shape[0]:,} rows × {df.shape[1]} columns")
            
            # Generate and display AI response
            # Pass uploaded_csv_file if using file upload, otherwise image only
            self.response_handler.handle_response(
                enhanced_prompt, 
                image=uploaded_image,
                uploaded_file_ref=uploaded_csv_file
            )
            
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
