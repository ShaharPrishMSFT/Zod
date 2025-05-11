"""
Core data structures for FormalAI SDK.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict

class Role(Enum):
    """Defines possible roles in a conversation."""
    AGENT = auto()
    CLIENT = auto()

@dataclass
class Message:
    """
    Represents a single message in a conversation.
    
    Attributes:
        role: The role of the message sender (AGENT or CLIENT)
        content: The actual message content
        metadata: Optional metadata associated with the message
    """
    role: Role
    content: str
    metadata: Dict = field(default_factory=dict)

@dataclass
class Conversation:
    """
    Represents a conversation consisting of a sequence of messages.
    
    Attributes:
        messages: List of messages in the conversation
    """
    messages: List[Message] = field(default_factory=list)
    
    def add_message(self, role: Role, content: str) -> None:
        """
        Add a new message to the conversation.
        
        Args:
            role: The role of the message sender
            content: The message content
            
        Example:
            conversation = Conversation()
            conversation.add_message(Role.CLIENT, "Hello")
            conversation.add_message(Role.AGENT, "Hi there")
        """
        self.messages.append(Message(role=role, content=content))
