"""
Type definitions for the FormalAI SDK.
"""

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    """
    Represents a message in a conversation.
    
    Attributes:
        actor: The identifier of the actor who sent the message
        content: The text content of the message
        timestamp: When the message was created
    """
    actor: str
    content: str
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
