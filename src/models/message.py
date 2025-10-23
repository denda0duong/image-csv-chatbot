"""
Data models for the chatbot application.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class ChatMessage:
    """Represents a single message in the chat."""
    role: str
    content: str
    timestamp: Optional[str] = None
    plots: Optional[List[bytes]] = field(default_factory=list)
    image: Optional[bytes] = None
    
    def to_dict(self) -> Dict:
        """Convert message to dictionary format."""
        return {
            "role": self.role, 
            "content": self.content,
            "timestamp": self.timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "plots": self.plots or [],
            "image": self.image
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ChatMessage':
        """Create message from dictionary format."""
        return cls(
            role=data["role"], 
            content=data["content"],
            timestamp=data.get("timestamp"),
            plots=data.get("plots", []),
            image=data.get("image")
        )


@dataclass
class GeminiMessage:
    """Represents a message in Gemini API format."""
    role: str
    parts: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to Gemini API format."""
        return {"role": self.role, "parts": self.parts}
