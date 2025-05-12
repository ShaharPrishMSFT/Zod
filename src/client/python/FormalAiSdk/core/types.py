"""
Core data structures for FormalAI SDK.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict

class Role(Enum):
    """Defines possible roles in a conversation."""
    AGENT = auto()   # For assistant/AI responses
    CLIENT = auto()  # For user messages
    SYSTEM = auto()  # For system instructions/context

@dataclass(frozen=True)
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

    def __post_init__(self):
        # Create a deep copy of the metadata to ensure independence
        # We need to use object.__setattr__ because the class is frozen
        object.__setattr__(self, 'metadata', dict(self.metadata))

@dataclass(frozen=True)
class Conversation:
    """
    Represents a conversation consisting of a sequence of messages.
    
    Attributes:
        messages: List[Message] = A list of messages in the conversation. The list is immutable,
                                but new messages can be added using add_message().
    """
    messages: List[Message] = field(default_factory=list)
    
    def __post_init__(self):
        # Create a new list for messages to ensure independence
        messages_copy = list(self.messages)
        # We need to use object.__setattr__ because the class is frozen
        object.__setattr__(self, 'messages', messages_copy)
    
    def add_message(self, role: Role, content: str) -> 'Conversation':
        """
        Creates a new Conversation with the additional message.
        
        Args:
            role: The role of the message sender
            content: The message content
            
        Returns:
            A new Conversation instance with the additional message
            
        Example:
            conversation = Conversation()
            conversation = conversation.add_message(Role.CLIENT, "Hello")
            conversation = conversation.add_message(Role.AGENT, "Hi there")
        """
        new_messages = list(self.messages)
        new_messages.append(Message(role=role, content=content))
        return Conversation(messages=new_messages)
