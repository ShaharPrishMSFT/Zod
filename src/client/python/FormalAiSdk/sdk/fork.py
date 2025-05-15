"""
Fork management for the FormalAI SDK.
"""

from typing import TYPE_CHECKING
from ..core.types import Message as CoreMessage, Role, Conversation as CoreConversation
from ..core.executor import ModelExecutor

if TYPE_CHECKING:
    from .session import ModelSession

class ModelFork:
    """
    Handles isolated model execution for a conversation fork.
    """
    def __init__(self, fork_id: str, from_actor: str, message: str, executor: ModelExecutor):
        """
        Initialize a new execution fork.
        
        Args:
            fork_id: Unique identifier for this fork
            from_actor: Actor whose message is being responded to
            message: The message to respond to
            executor: ModelExecutor instance to use for generating responses
        """
        self.fork_id = fork_id
        self.from_actor = from_actor
        self.message = message
        self.executor = executor
    
    def Answer(self, session: "ModelSession") -> None:
        """
        Execute the model and add its response to the session.
        
        Args:
            session: The trunk conversation to add the response to
            
        Example:
            fork = ModelFork("fork1", "user", "Hello", executor)
            fork.Answer(session)  # Executes model and adds response
        """
        # Get existing conversation history from session
        conversation = session.get_conversation_history()
        
        # Add fork's message to existing conversation
        conversation = conversation.add_message(
            Role.CLIENT if self.from_actor == session.actor else Role.AGENT,
            self.message
        )
        
        # Execute model with single message
        response: CoreMessage = self.executor.execute(conversation)
        
        # Add response to session under fork's ID
        session.add_response(self.fork_id, response.content)
