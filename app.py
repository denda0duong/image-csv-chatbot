"""
Streamlit Chatbot Application
A multi-turn chat interface powered by Google Gemini API

This module provides the main user interface for the chatbot application.
It handles user interactions, message display, and communication with the AI model.
"""

import streamlit as st
from typing import List, Dict, Generator
from config import model


class ChatMessage:
    """Represents a single message in the chat history."""
    
    USER = "user"
    ASSISTANT = "assistant"
    MODEL = "model"


class ChatHistoryManager:
    """Manages chat history stored in Streamlit session state."""
    
    @staticmethod
    def initialize() -> None:
        """Initialize chat history in session state if it doesn't exist."""
        if "messages" not in st.session_state:
            st.session_state.messages = []
    
    @staticmethod
    def get_messages() -> List[Dict[str, str]]:
        """
        Get all messages from the chat history.
        
        Returns:
            List of message dictionaries with 'role' and 'content' keys
        """
        return st.session_state.messages
    
    @staticmethod
    def add_message(role: str, content: str) -> None:
        """
        Add a message to the chat history.
        
        Args:
            role: The role of the message sender (user or assistant)
            content: The content of the message
        """
        st.session_state.messages.append({"role": role, "content": content})
    
    @staticmethod
    def clear() -> None:
        """Clear all messages from the chat history."""
        st.session_state.messages = []
    
    @staticmethod
    def get_message_count() -> int:
        """
        Get the total number of messages in the chat history.
        
        Returns:
            Number of messages
        """
        return len(st.session_state.messages)


class GeminiChatService:
    """Handles communication with the Gemini AI model."""
    
    def __init__(self):
        """Initialize the chat service with the Gemini model."""
        self.model = model
    
    def _convert_history_to_gemini_format(
        self, 
        messages: List[Dict[str, str]]
    ) -> List[Dict[str, any]]:
        """
        Convert chat history to Gemini API format.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            List of messages in Gemini format
        """
        gemini_history = []
        for msg in messages:
            role = ChatMessage.USER if msg["role"] == ChatMessage.USER else ChatMessage.MODEL
            gemini_history.append({
                "role": role,
                "parts": [msg["content"]]
            })
        return gemini_history
    
    def get_response_stream(
        self, 
        prompt: str, 
        history: List[Dict[str, str]]
    ) -> Generator[str, None, None]:
        """
        Get a streaming response from the model.
        
        Args:
            prompt: The user's input prompt
            history: Previous conversation history
            
        Yields:
            Chunks of the model's response
            
        Raises:
            Exception: If there's an error communicating with the model
        """
        # Convert history to Gemini format (excluding the current prompt)
        gemini_history = self._convert_history_to_gemini_format(history[:-1])
        
        # Start chat with history
        chat = self.model.start_chat(history=gemini_history if gemini_history else [])
        
        # Get streaming response
        response = chat.send_message(prompt, stream=True)
        
        # Yield response chunks
        for chunk in response:
            if chunk.text:
                yield chunk.text


class StreamlitUI:
    """Handles all UI components and rendering."""
    
    @staticmethod
    def configure_page() -> None:
        """Configure the Streamlit page settings."""
        st.set_page_config(
            page_title="Image CSV Chatbot",
            page_icon="🤖",
            layout="centered"
        )
    
    @staticmethod
    def render_header() -> None:
        """Render the application header."""
        st.title("🤖 Image CSV Chatbot")
        st.caption("Powered by Google Gemini AI")
    
    @staticmethod
    def render_chat_history(messages: List[Dict[str, str]]) -> None:
        """
        Render all messages in the chat history.
        
        Args:
            messages: List of message dictionaries to display
        """
        for message in messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    @staticmethod
    def render_sidebar(message_count: int) -> None:
        """
        Render the sidebar with controls and information.
        
        Args:
            message_count: Current number of messages in history
        """
        with st.sidebar:
            st.header("⚙️ Settings")
            
            # Clear chat button
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                ChatHistoryManager.clear()
                st.rerun()
            
            # Display message count
            st.info(f"💬 Messages in history: {message_count}")
            
            st.divider()
            
            # App information
            st.header("ℹ️ About")
            st.markdown("""
            This chatbot uses Google's Gemini AI model to have intelligent conversations.
            
            **Features:**
            - Multi-turn conversations
            - Streaming responses
            - Chat history persistence
            - Context-aware responses
            
            **Coming Soon:**
            - 📊 CSV file analysis
            - 🖼️ Image analysis
            - 📁 File uploads
            """)
            
            st.divider()
            
            # Usage tips
            st.header("💡 Tips")
            st.markdown("""
            - Ask follow-up questions naturally
            - Reference previous messages in the conversation
            - Clear chat to start fresh
            - Try creative prompts!
            """)


class ChatbotApp:
    """Main application class that orchestrates the chatbot functionality."""
    
    def __init__(self):
        """Initialize the chatbot application."""
        self.chat_service = GeminiChatService()
        self.ui = StreamlitUI()
        self.history_manager = ChatHistoryManager()
    
    def run(self) -> None:
        """Run the main application loop."""
        # Configure page
        self.ui.configure_page()
        
        # Initialize chat history
        self.history_manager.initialize()
        
        # Render UI components
        self.ui.render_header()
        self.ui.render_chat_history(self.history_manager.get_messages())
        
        # Handle user input
        self._handle_chat_input()
        
        # Render sidebar
        self.ui.render_sidebar(self.history_manager.get_message_count())
    
    def _handle_chat_input(self) -> None:
        """Handle user input from the chat input widget."""
        if prompt := st.chat_input("Ask me anything..."):
            # Add user message to history
            self.history_manager.add_message(ChatMessage.USER, prompt)
            
            # Display user message
            with st.chat_message(ChatMessage.USER):
                st.markdown(prompt)
            
            # Generate and display assistant response
            self._generate_response(prompt)
    
    def _generate_response(self, prompt: str) -> None:
        """
        Generate and display the assistant's response.
        
        Args:
            prompt: The user's input prompt
        """
        with st.chat_message(ChatMessage.ASSISTANT):
            with st.status("Thinking...", expanded=False) as status:
                try:
                    # Update status
                    status.update(label="Generating response...", state="running")
                    
                    # Get streaming response
                    response_stream = self.chat_service.get_response_stream(
                        prompt, 
                        self.history_manager.get_messages()
                    )
                    
                    # Display streamed response
                    full_response = st.write_stream(response_stream)
                    
                    # Update status
                    status.update(label="Complete!", state="complete")
                    
                except Exception as e:
                    # Handle errors gracefully
                    full_response = (
                        f"❌ Error: {str(e)}\n\n"
                        "Please check your API key in the .env file and try again."
                    )
                    st.error(full_response)
                    status.update(label="Error occurred", state="error")
            
            # Add response to history
            self.history_manager.add_message(ChatMessage.ASSISTANT, full_response)


def main() -> None:
    """Application entry point."""
    app = ChatbotApp()
    app.run()


if __name__ == "__main__":
    main()
