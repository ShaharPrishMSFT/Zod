"""
LiteLLM-based model executor implementation.
Supports both OpenAI and Ollama models through a unified interface.
"""

from typing import Optional, List, Dict, Any

import litellm

from ..core.executor import ModelExecutor
from ..core.types import Conversation, Message, Role
from ..exceptions import ExecutionError, ModelError, InvalidConversationError

class LiteLLMExecutor(ModelExecutor):
    """
    ModelExecutor implementation using LiteLLM as the backend.
    
    This executor can work with both cloud-based models (like OpenAI)
    and local models (like Ollama's llama) through a unified interface.
    
    Attributes:
        provider: The LLM provider to use ("openai" or "ollama")
        model: The specific model to use (e.g., "gpt-3.5-turbo" for OpenAI or "llama2" for Ollama)
        api_key: Optional API key for cloud providers (not needed for Ollama)
    """
    
    def __init__(self, provider: str, model: str, api_key: Optional[str] = None):
        """
        Initialize the LiteLLM executor.

        Args:
            provider: The LLM provider to use ("openai", "azure", or "ollama")
            model: The model name to use (for Azure, this is the deployment name)
            api_key: Optional API key for cloud providers

        Example:
            # For OpenAI
            executor = LiteLLMExecutor("openai", "gpt-3.5-turbo", "sk-...")

            # For Azure OpenAI
            executor = LiteLLMExecutor("azure", "gpt-4.1", "<azure-key>")

            # For Ollama
            executor = LiteLLMExecutor("ollama", "llama2")
        """
        self.provider = provider.lower()

        # Azure OpenAI support
        if self.provider == "azure" or (
            provider is None and (
                "AZURE_API_KEY" in os.environ and
                "AZURE_API_BASE" in os.environ and
                "AZURE_DEPLOYMENT_NAME" in os.environ
            )
        ):
            import os
            azure_key = api_key or os.environ.get("AZURE_API_KEY")
            azure_base = os.environ.get("AZURE_API_BASE")
            azure_version = os.environ.get("AZURE_API_VERSION", "2025-01-01-preview")
            deployment = model or os.environ.get("AZURE_DEPLOYMENT_NAME")
            self.model = f"azure/{deployment}"
            self.litellm_kwargs = {
                "api_key": azure_key,
                "api_base": azure_base,
                "api_version": azure_version,
            }
        else:
            # OpenAI or Ollama
            self.model = f"{provider}/{model}"
            self.litellm_kwargs = {}
            if api_key:
                litellm.api_key = api_key
    
    def _convert_role(self, role: Role) -> str:
        """Convert our Role enum to LiteLLM role string."""
        return {
            Role.AGENT: "assistant",
            Role.CLIENT: "user"
        }[role]
    
    def _convert_messages(self, conversation: Conversation) -> List[Dict[str, str]]:
        """Convert our Message objects to LiteLLM format."""
        return [
            {
                "role": self._convert_role(msg.role),
                "content": msg.content
            }
            for msg in conversation.messages
        ]
    
    def _create_message(self, content: str) -> Message:
        """Create a Message object from LiteLLM response content."""
        return Message(
            role=Role.AGENT,
            content=content
        )
    
    def execute(self, conversation: Conversation) -> Message:
        """
        Execute model with given conversation history.
        
        Args:
            conversation: The conversation history to process
            
        Returns:
            Message: The model's response as a Message object
            
        Raises:
            ModelError: If there's an error during model execution
            InvalidConversationError: If the conversation is empty or invalid
            
        Example:
            executor = LiteLLMExecutor("ollama", "llama2")
            convo = Conversation([
                Message(Role.CLIENT, "Hello"),
                Message(Role.AGENT, "Hi there")
            ])
            response = executor.execute(convo)
        """
        if not conversation.messages:
            raise InvalidConversationError("Conversation cannot be empty")
        
        try:
            messages = self._convert_messages(conversation)
            
            # Execute the model
            response = litellm.completion(
                model=self.model,
                messages=messages,
                **self.litellm_kwargs
            )
            
            # Extract the response content
            content = response["choices"][0]["message"]["content"]
            
            return self._create_message(content)
            
        except Exception as e:
            raise ModelError(f"Error during model execution: {str(e)}") from e
