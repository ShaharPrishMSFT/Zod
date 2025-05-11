"""
Base model executor interface for FormalAI SDK.
"""

from abc import ABC, abstractmethod
from .types import Conversation, Message

class ModelExecutor(ABC):
    """
    Base class for model execution.
    
    This abstract class defines the interface that all model executors
    must implement. Concrete implementations will provide specific logic
    for different model types and APIs.
    """
    
    @abstractmethod
    def execute(self, conversation: Conversation) -> Message:
        """
        Execute model with given conversation history.
        
        Args:
            conversation: The conversation history to process
            
        Returns:
            Message: The model's response as a Message object
            
        Raises:
            ExecutionError: Base class for execution-related errors
            ModelError: For model-specific execution issues
            InvalidConversationError: If conversation structure is invalid
            
        Example:
            executor = ModelExecutor()
            convo = Conversation([
                Message(Role.CLIENT, "Hello"),
                Message(Role.AGENT, "Hi there")
            ])
            response = executor.execute(convo)
        """
        raise NotImplementedError
