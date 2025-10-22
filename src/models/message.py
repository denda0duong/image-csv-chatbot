"""
Data models for the chatbot application.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class ChatMessage:
    """Represents a single message in the chat."""
    role: str
    content: str
    timestamp: Optional[str] = None
    
    def to_dict(self) -> Dict[str, str]:
        """Convert message to dictionary format."""
        return {
            "role": self.role, 
            "content": self.content,
            "timestamp": self.timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'ChatMessage':
        """Create message from dictionary format."""
        return cls(
            role=data["role"], 
            content=data["content"],
            timestamp=data.get("timestamp")
        )


@dataclass
class GeminiMessage:
    """Represents a message in Gemini API format."""
    role: str
    parts: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to Gemini API format."""
        return {"role": self.role, "parts": self.parts}
