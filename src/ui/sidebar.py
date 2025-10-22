"""
Sidebar UI component.
"""

import streamlit as st
from ..services.chat_history import ChatHistoryManager


class SidebarUI:
    """Handles sidebar UI components."""
    
    @staticmethod
    def render(message_count: int) -> None:
        """
        Render the sidebar with controls and information.
        
        Args:
            message_count: Current number of messages in history
        """
        with st.sidebar:
            SidebarUI._render_settings(message_count)
            st.divider()
            SidebarUI._render_about()
            st.divider()
            SidebarUI._render_tips()
    
    @staticmethod
    def _render_settings(message_count: int) -> None:
        """Render the settings section."""
        st.header("⚙️ Settings")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            ChatHistoryManager.clear()
            st.rerun()
        
        # Display message count
        st.info(f"💬 Messages in history: {message_count}")
    
    @staticmethod
    def _render_about() -> None:
        """Render the about section."""
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
    
    @staticmethod
    def _render_tips() -> None:
        """Render the tips section."""
        st.header("💡 Tips")
        st.markdown("""
        - Ask follow-up questions naturally
        - Reference previous messages in the conversation
        - Clear chat to start fresh
        - Try creative prompts!
        """)
