"""
Gemini AI chat service.
"""

from typing import List, Dict, Generator, Union
from PIL import Image
from config import model, MODEL_NAME, GENERATION_CONFIG_WITH_CODE_EXECUTION
from ..models.constants import MessageRole
from ..models.message import GeminiMessage
from .plot_service import PlotService
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
    
    def get_response_with_plots(
        self,
        prompt: str,
        history: List[Dict[str, str]],
        image: Union[Image.Image, None] = None,
        uploaded_file_ref = None
    ) -> Dict[str, any]:
        """
        Get response from model and extract any generated plots.
        
        This is used for non-streaming responses when plots might be generated.
        Gemini's code execution generates plots that are included in the response.
        
        Args:
            prompt: The user's input prompt
            history: Previous conversation history
            image: Optional image to include
            uploaded_file_ref: Optional uploaded file reference
            
        Returns:
            Dictionary containing:
                - 'text': Response text
                - 'plots': List of PlotData objects
        """
        import time
        
        try:
            start_time = time.time()
            plots = []
            
            # File upload API for CSV
            if uploaded_file_ref and GENAI_CLIENT_AVAILABLE:
                logger.info("[RESPONSE] Using file upload API with plot detection")
                client = genai.Client()
                
                # Use generation config with code execution enabled
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=[uploaded_file_ref, prompt],
                    config=GENERATION_CONFIG_WITH_CODE_EXECUTION
                )
                
                # Extract plots from response
                plots = PlotService.extract_plots_from_response(response)
                
                # Extract text from response (handle mixed content with images)
                response_text = self._extract_text_from_response(response)
                
            # Regular chat with history
            else:
                logger.info("[RESPONSE] Using regular chat API with plot detection")
                gemini_history = self._convert_to_gemini_format(history[:-1])
                chat = self.model.start_chat(history=gemini_history if gemini_history else [])
                message_content = [prompt, image] if image else prompt
                response = chat.send_message(message_content)
                
                # Extract plots from response
                plots = PlotService.extract_plots_from_response(response)
                
                # Extract text from response (handle mixed content with images)
                response_text = self._extract_text_from_response(response)
            
            elapsed = time.time() - start_time
            logger.info(f"[RESPONSE] Complete in {elapsed:.2f}s - text: {len(response_text)} chars, plots: {len(plots)}")
            
            return {
                'text': response_text,
                'plots': plots
            }
            
        except Exception as e:
            logger.error(f"Error getting response with plots: {e}", exc_info=True)
            raise

    def _extract_text_from_response(self, response) -> str:
        """
        Extract text content from Gemini response.
        Handles responses with mixed content (text + inline_data).
        
        Args:
            response: Gemini API response object
            
        Returns:
            Extracted text content as string
        """
        try:
            # Try direct text access first (works for text-only responses)
            if hasattr(response, 'text') and not any(
                hasattr(part, 'inline_data') 
                for part in response.candidates[0].content.parts
            ):
                return response.text
            
            # Extract text parts manually for mixed content responses
            text_parts = []
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'text'):
                    text_parts.append(part.text)
            
            return ''.join(text_parts)
            
        except Exception as e:
            logger.error(f"[ERROR] Error extracting text from response: {str(e)}")
            return ""
