"""
Gemini AI chat service.
"""

from typing import List, Dict, Generator
from config import model
from ..models.constants import MessageRole
from ..models.message import GeminiMessage
from logger_config import get_logger

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
        try:
            logger.info(f"Generating response for prompt (length: {len(prompt)} chars)")
            logger.debug(f"History size: {len(history)} messages")
            
            # Convert history to Gemini format (excluding the current prompt)
            gemini_history = self._convert_to_gemini_format(history[:-1])
            
            # Start chat with history
            chat = self.model.start_chat(history=gemini_history if gemini_history else [])
            
            # Get streaming response
            response = chat.send_message(prompt, stream=True)
            
            chunk_count = 0
            # Yield response chunks
            for chunk in response:
                if chunk.text:
                    chunk_count += 1
                    yield chunk.text
            
            logger.info(f"Response generated successfully ({chunk_count} chunks)")
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}", exc_info=True)
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
