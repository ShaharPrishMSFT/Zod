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
    
    def __init__(self, model_config: dict):
        """
        Initialize the LiteLLM executor using a unified config dictionary.

        Args:
            model_config (dict): Model configuration as returned by LlmModels.FromOpenAi or LlmModels.From.
                Expected keys: provider, model, api_key, api_base, api_version, deployment, etc.

        Example:
            # For OpenAI
            config = LlmModels.FromOpenAi()
            executor = LiteLLMExecutor(config)

            # For Azure OpenAI
            config = LlmModels.From({
                "provider": "azure",
                "model": "azure/my-deployment",
                "api_key": "...",
                "api_base": "...",
                "api_version": "2025-01-01-preview"
            })
            executor = LiteLLMExecutor(config)

            # For Ollama
            config = LlmModels.From({
                "provider": "ollama",
                "model": "ollama/llama2"
            })
            executor = LiteLLMExecutor(config)
        """
        self.provider = model_config.get("provider", "openai").lower()
        self.model = model_config.get("model")
        self.litellm_kwargs = {}

        # Azure OpenAI support
        if self.provider == "azure":
            self.model = self.model or f"azure/{model_config.get('deployment')}"
            self.litellm_kwargs = {
                "api_key": model_config.get("api_key"),
                "api_base": model_config.get("api_base"),
                "api_version": model_config.get("api_version", "2025-01-01-preview"),
            }
        elif self.provider == "openai":
            # OpenAI cloud
            self.model = self.model or "gpt-4.1"
            self.litellm_kwargs = {}
            api_key = model_config.get("api_key")
            if api_key:
                litellm.api_key = api_key
            api_base = model_config.get("api_base")
            if api_base:
                self.litellm_kwargs["api_base"] = api_base
            api_version = model_config.get("api_version")
            if api_version:
                self.litellm_kwargs["api_version"] = api_version
        elif self.provider == "ollama":
            # Ollama local
            self.model = self.model or "ollama/llama2"
            self.litellm_kwargs = {}
        else:
            # Generic fallback
            self.litellm_kwargs = {k: v for k, v in model_config.items() if k not in ("provider", "model")}

    
    def _convert_role(self, role: Role) -> str:
        """Convert our Role enum to LiteLLM role string."""
        # Map our roles to litellm roles
        role_mapping = {
            Role.AGENT: "assistant",
            Role.CLIENT: "user",
            Role.SYSTEM: "system"  # Handle system messages
        }
        return role_mapping.get(role, "user")  # Default to user if unknown role
    
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
            
            if self.provider == "ollama":
                # For Ollama, construct a single prompt string
                prompt = ""
                for msg in messages:
                    if msg["role"] == "system":
                        prompt += f"<system>\n{msg['content']}\n</system>\n\n"
                    elif msg["role"] == "user":
                        prompt += f"{msg['content']}\n\n"
                    else:  # assistant
                        prompt += f"Assistant: {msg['content']}\n\n"
                
                # Execute with constructed prompt
                response = litellm.completion(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
            else:
                # For other providers, use standard message format
                response = litellm.completion(
                    model=self.model,
                    messages=messages
                )
            
            # Extract the response content
            content = response["choices"][0]["message"]["content"]
            
            return self._create_message(content)
            
        except Exception as e:
            raise ModelError(f"Error during model execution: {str(e)}") from e
