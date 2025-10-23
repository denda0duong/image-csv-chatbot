"""
Sidebar UI component.
"""

import streamlit as st
from PIL import Image
from ..services.chat_history import ChatHistoryManager
from ..services.csv_service import CSVService


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
        
        # CSV upload section
        SidebarUI._render_csv_upload()
        
        st.divider()
        
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
            help="Upload an image to discuss with AI. Vision model supports detailed image analysis!",
            key="image_file_uploader"
        )
        
        if uploaded_file is not None:
            # Convert uploaded file to PIL Image and store in session state
            image = Image.open(uploaded_file)
            st.session_state['uploaded_image'] = image
            
            # Display preview
            st.image(image, caption="Uploaded Image", width='stretch')
            
            # Show remove button
            if st.button("❌ Remove Image", width='stretch', key="remove_image_button"):
                if 'uploaded_image' in st.session_state:
                    del st.session_state['uploaded_image']
                st.rerun()
        elif 'uploaded_image' in st.session_state:
            # File uploader was cleared, remove from session state
            del st.session_state['uploaded_image']
    
    @staticmethod
    def _render_csv_upload() -> None:
        """Render the CSV upload section."""
        st.subheader("📊 CSV Data Upload")
        
        # File uploader for CSV
        uploaded_csv = st.file_uploader(
            "Upload a CSV file",
            type=['csv'],
            help="Upload a CSV file to analyze with AI. Supports files up to 2GB using file upload API!",
            key="csv_file_uploader"
        )
        
        # URL input for CSV
        csv_url = st.text_input(
            "Or enter CSV URL",
            placeholder="https://example.com/data.csv",
            help="Provide a direct URL to a CSV file. Supports large files up to 2GB!",
            key="csv_url_input"
        )
        
        # Load button
        load_clicked = st.button("📥 Load CSV", width='stretch', key="load_csv_button")
        
        # Handle CSV loading
        if load_clicked:
            # Priority: uploaded file first, then URL
            if uploaded_csv is not None:
                df = CSVService.load_csv(uploaded_csv)
                if df is not None:
                    st.session_state['df'] = df
                    st.session_state['csv_changed'] = True  # Mark as changed for re-upload
                    # Clear any existing uploaded file reference
                    if 'uploaded_csv_file' in st.session_state:
                        del st.session_state['uploaded_csv_file']
                    st.rerun()
            elif csv_url.strip():
                df = CSVService.load_csv(csv_url)
                if df is not None:
                    st.session_state['df'] = df
                    st.session_state['csv_changed'] = True  # Mark as changed for re-upload
                    # Clear any existing uploaded file reference
                    if 'uploaded_csv_file' in st.session_state:
                        del st.session_state['uploaded_csv_file']
                    st.rerun()
            else:
                st.warning("⚠️ Please upload a file or enter a URL first")
        
        # Display loaded CSV info
        if 'df' in st.session_state and st.session_state['df'] is not None:
            st.success("✅ CSV Loaded!")
            
            df = st.session_state['df']
            
            # Show summary
            st.caption(f"**{df.shape[0]:,}** rows × **{df.shape[1]}** columns")
            
            # Show token estimation
            estimated_tokens = CSVService.estimate_csv_tokens(df)
            max_tokens = 1_000_000
            token_percentage = (estimated_tokens / max_tokens) * 100
            
            # Color-code based on usage
            if estimated_tokens > max_tokens:
                st.error(f"🚫 **Token Limit Exceeded!**\n\n"
                        f"Estimated: ~{estimated_tokens:,} tokens\n"
                        f"Maximum: {max_tokens:,} tokens\n\n"
                        f"⚠️ This file is **too large** to process.\n"
                        f"Please reduce the dataset size.")
            elif token_percentage > 80:
                st.warning(f"⚠️ **High Token Usage**\n\n"
                          f"~{estimated_tokens:,} / {max_tokens:,} tokens ({token_percentage:.1f}%)\n\n"
                          f"File is near the limit. Consider reducing size for better performance.")
            elif token_percentage > 50:
                st.info(f"ℹ️ **Token Usage**\n\n"
                       f"~{estimated_tokens:,} / {max_tokens:,} tokens ({token_percentage:.1f}%)\n\n"
                       f"Moderate file size - should process fine.")
            else:
                st.success(f"✅ **Token Usage**\n\n"
                          f"~{estimated_tokens:,} / {max_tokens:,} tokens ({token_percentage:.1f}%)\n\n"
                          f"Small file - optimal for fast processing!")
            
            # Show first 5 rows
            st.dataframe(df.head(), width='stretch')
            
            # Remove CSV button
            if st.button("❌ Remove CSV", width='stretch', key="remove_csv_button"):
                if 'df' in st.session_state:
                    del st.session_state['df']
                if 'uploaded_csv_file' in st.session_state:
                    del st.session_state['uploaded_csv_file']
                if 'csv_changed' in st.session_state:
                    del st.session_state['csv_changed']
                st.rerun()
    
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
        - 📊 CSV data analysis with file upload API
        - 📤 **Supports files up to 2GB** (CSV & images)
        - 🚀 No token usage for CSV data
        - ⏱️ Message timestamps
        - 📋 Comprehensive logging
        
        **Coming Soon:**
        - 📎 Multiple file uploads
        - 💾 Export chat history
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
