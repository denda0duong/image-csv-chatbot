"""
Streamlit Chatbot Application
A multi-turn chat interface powered by Google Gemini API

This is the main entry point for the application. The code is organized
into separate modules for better maintainability and scalability.
"""

from src.models.constants import MessageRole
from src.services.chat_history import ChatHistoryManager
from src.services.gemini_service import GeminiChatService
from src.services.response_handler import ResponseHandler
from src.ui.chat import ChatUI
from src.ui.sidebar import SidebarUI


class ChatbotApp:
    """
    Main application orchestrator.
    
    This class coordinates all components of the chatbot application,
    following the Single Responsibility Principle with each component
    handling a specific aspect of the functionality.
    """
    
    def __init__(self):
        """Initialize the chatbot application with all required services."""
        self.chat_service = GeminiChatService()
        self.response_handler = ResponseHandler(self.chat_service)
        self.history_manager = ChatHistoryManager()
    
    def run(self) -> None:
        """
        Run the main application loop.
        
        This method orchestrates the entire application flow:
        1. Configure the page
        2. Initialize state
        3. Render UI components
        4. Handle user interactions
        """
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
        2. Display the message
        3. Generate and display AI response
        """
        if prompt := ChatUI.get_user_input():
            # Store and display user message
            self.history_manager.add_message(MessageRole.USER.value, prompt)
            ChatUI.display_message(MessageRole.USER.value, prompt)
            
            # Generate and display AI response
            self.response_handler.handle_response(prompt)


def main() -> None:
    """
    Application entry point.
    
    Creates and runs the chatbot application instance.
    """
    app = ChatbotApp()
    app.run()


if __name__ == "__main__":
    main()
