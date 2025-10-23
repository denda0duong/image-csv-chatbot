"""
Gemini AI chat service.
"""

from typing import List, Dict, Generator, Union
from PIL import Image
from config import model, MODEL_NAME
from ..models.constants import MessageRole
from ..models.message import GeminiMessage
from logger_config import get_logger

# Import new genai client for file upload support
try:
    from google import genai
    GENAI_CLIENT_AVAILABLE = True
except ImportError:
    GENAI_CLIENT_AVAILABLE = False
    genai = None

logger = get_logger(__name__)


class GeminiChatService:
    """Handles communication with the Gemini AI model."""
    
    def __init__(self):
        """Initialize the chat service with the Gemini model."""
        self.model = model
        logger.info("GeminiChatService initialized")
    
    def _convert_to_gemini_format(
        self, 
        messages: List[Dict[str, str]]
    ) -> List[Dict]:
        """
        Convert chat history to Gemini API format.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            List of messages in Gemini format
        """
        gemini_messages = []
        for msg in messages:
            role = MessageRole.USER.value if msg["role"] == MessageRole.USER.value else MessageRole.MODEL.value
            gemini_msg = GeminiMessage(role=role, parts=[msg["content"]])
            gemini_messages.append(gemini_msg.to_dict())
        return gemini_messages
    
    def get_response_stream(
        self, 
        prompt: str, 
        history: List[Dict[str, str]],
        image: Union[Image.Image, None] = None,
        uploaded_file_ref = None
    ) -> Generator[str, None, None]:
        """Get streaming response from model."""
        import time
        try:
            start_time = time.time()
            
            # File upload API for CSV
            if uploaded_file_ref and GENAI_CLIENT_AVAILABLE:
                logger.info(f"[RESPONSE] Using file upload API for: {uploaded_file_ref.name}")
                logger.info(f"[RESPONSE] Prompt length: {len(prompt)} chars")
                
                api_start = time.time()
                client = genai.Client()
                response = client.models.generate_content_stream(
                    model=MODEL_NAME,
                    contents=[uploaded_file_ref, prompt]
                )
                api_call_time = time.time() - api_start
                logger.info(f"[RESPONSE] API call initiated in {api_call_time:.2f}s")
                
                chunk_count = 0
                first_chunk_time = None
                for chunk in response:
                    if chunk.text:
                        if chunk_count == 0:
                            first_chunk_time = time.time() - start_time
                            logger.info(f"[RESPONSE] First chunk received in {first_chunk_time:.2f}s")
                        chunk_count += 1
                        yield chunk.text
                
                total_time = time.time() - start_time
                logger.info(f"[RESPONSE] ✅ Complete: {chunk_count} chunks in {total_time:.2f}s")
                return
            
            # Regular chat with history
            logger.info(f"[RESPONSE] Using regular chat API, history: {len(history)} messages")
            gemini_history = self._convert_to_gemini_format(history[:-1])
            chat = self.model.start_chat(history=gemini_history if gemini_history else [])
            message_content = [prompt, image] if image else prompt
            response = chat.send_message(message_content, stream=True)
            
            chunk_count = 0
            for chunk in response:
                if chunk.text:
                    chunk_count += 1
                    yield chunk.text
            
            total_time = time.time() - start_time
            logger.info(f"[RESPONSE] ✅ Complete: {chunk_count} chunks in {total_time:.2f}s")
            
        except Exception as e:
            logger.error(f"[RESPONSE] Error after {time.time() - start_time:.2f}s: {str(e)}", exc_info=True)
            if "token" in str(e).lower():
                raise ValueError("❌ Token limit exceeded - try clearing chat history or using a smaller CSV")
            raise
    
    def get_response(
        self, 
        prompt: str, 
        history: List[Dict[str, str]] = None
    ) -> str:
        """
        Get a non-streaming response from the model.
        
        Args:
            prompt: The user's input prompt
            history: Optional previous conversation history
            
        Returns:
            The model's response as a string
            
        Raises:
            Exception: If there's an error communicating with the model
        """
        if history:
            gemini_history = self._convert_to_gemini_format(history)
            chat = self.model.start_chat(history=gemini_history)
            response = chat.send_message(prompt)
        else:
            response = self.model.generate_content(prompt)
        
        return response.text
