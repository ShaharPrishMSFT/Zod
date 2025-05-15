"""
Session management for the FormalAI SDK.
"""

from typing import List
from ..core.types import Role, Conversation as CoreConversation
from ..core.executor import ModelExecutor
from .types import Message
from .fork import ModelFork

class ModelSession:
    """
    Manages a trunk conversation.
    """
    def __init__(self, actor: str, model_config: dict = None, executor: ModelExecutor = None):
        """
        Initialize a new trunk conversation.

        Args:
            actor: The actor who owns the trunk conversation
            model_config: Unified model configuration dict (from LlmModels.FromOpenAi or LlmModels.From)
            executor: Optional ModelExecutor for handling model responses (overrides model_config if provided)
        """
        self.actor = actor
        self.messages: List[Message] = []
        self.model_config = model_config
        if executor is not None:
            self.executor = executor
        elif model_config is not None:
            from ..models.litellm_executor import LiteLLMExecutor
            self.executor = LiteLLMExecutor(model_config)
        else:
            self.executor = None

    def get_conversation_history(self, include_last_n: int = None) -> CoreConversation:
        """
        Get conversation history as a core Conversation object.
        Optionally limit to last N messages.
        """
        messages = self.messages
        if include_last_n is not None:
            messages = messages[-include_last_n:]
        
        conversation = CoreConversation()
        for msg in messages:
            # Map roles based on actor type
            if msg.actor == self.actor:
                role = Role.CLIENT
            elif msg.actor == "system":
                role = Role.SYSTEM
            else:
                role = Role.AGENT
            conversation = conversation.add_message(role, msg.content)
        return conversation

    def Fork(self, fork_id: str, from_actor: str, message: str) -> ModelFork:
        """
        Create a new fork for model execution.
        
        Args:
            fork_id: Unique identifier for this fork
            from_actor: Actor whose message is being responded to
            message: The message to respond to
            
        Returns:
            A ModelFork instance configured to execute the response
            
        Raises:
            ValueError: If no executor was provided to the session
        """
        if not self.executor:
            raise ValueError("No executor available for fork creation")
            
        return ModelFork(fork_id, from_actor, message, self.executor)

    def add_response(self, actor: str, content: str) -> None:
        """
        Add a response to the trunk conversation.
        
        Args:
            actor: The actor providing the response
            content: The response content
        """
        message = Message(actor=actor, content=content)
        self.messages.append(message)

    def to_core_conversation(self) -> CoreConversation:
        """
        Convert to a core Conversation object with all messages.
        
        Returns:
            CoreConversation: Full conversation history in core format
        """
        return self.get_conversation_history()
