"""
Sidebar UI component.
"""

import streamlit as st
from PIL import Image
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
        
        # Image upload section
        SidebarUI._render_image_upload()
        
        st.divider()
        
        # Show timestamps toggle
        if "show_timestamps" not in st.session_state:
            st.session_state.show_timestamps = True
        
        st.session_state.show_timestamps = st.toggle(
            "🕐 Show Timestamps",
            value=st.session_state.show_timestamps,
            help="Display when each message was sent"
        )
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", width="stretch"):
            ChatHistoryManager.clear()
            st.rerun()
        
        # Display message count
        st.info(f"💬 Messages in history: {message_count}")
    
    @staticmethod
    def _render_image_upload() -> None:
        """Render the image upload section."""
        st.subheader("🖼️ Image Upload")
        
        uploaded_file = st.file_uploader(
            "Upload an image",
            type=['png', 'jpg', 'jpeg'],
            help="Upload an image to discuss with the AI"
        )
        
        if uploaded_file is not None:
            # Convert uploaded file to PIL Image and store in session state
            image = Image.open(uploaded_file)
            st.session_state['uploaded_image'] = image
            
            # Display preview
            st.image(image, caption="Uploaded Image", width='stretch')
            
            # Show remove button
            if st.button("❌ Remove Image", width='stretch'):
                if 'uploaded_image' in st.session_state:
                    del st.session_state['uploaded_image']
                st.rerun()
        elif 'uploaded_image' in st.session_state:
            # File uploader was cleared, remove from session state
            del st.session_state['uploaded_image']
    
    @staticmethod
    def _render_about() -> None:
        """Render the about section."""
        st.header("ℹ️ About")
        st.markdown("""
        This chatbot uses Google's Gemini AI model to have intelligent conversations.
        
        **Features:**
        - 💬 Multi-turn conversations
        - 📝 Streaming responses
        - 💾 Chat history persistence
        - 🧠 Context-aware responses
        - 🖼️ Image analysis with vision AI
        - ⏱️ Message timestamps
        - 📊 Comprehensive logging
        
        **Coming Soon:**
        - 📊 CSV file analysis
        - � Multiple file uploads
        - � Export chat history
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
