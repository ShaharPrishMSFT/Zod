"""
LlmModels: Unified entry points for model configuration.

- LlmModels.FromOpenAi(openai_config=None): returns OpenAI config dict, using env defaults if not provided.
- LlmModels.From(litellm_config=None): returns generic LiteLLM config dict, using env defaults if not provided.
"""

import os

class LlmModels:
    @staticmethod
    def FromOpenAi(openai_config=None):
        """
        Build OpenAI model config from explicit config or environment variables.

        Args:
            openai_config (dict, optional): Explicit config. If not provided, uses env vars.

        Returns:
            dict: Config dict with keys: provider, model, api_key, api_base (optional), api_version (optional)
        """
        config = openai_config.copy() if openai_config else {}
        config.setdefault("provider", "openai")
        config.setdefault("model", os.getenv("OPENAI_MODEL", "gpt-4.1"))
        config.setdefault("api_key", os.getenv("OPENAI_API_KEY"))
        # Optionally support custom base/version for OpenAI
        api_base = os.getenv("OPENAI_API_BASE")
        if api_base:
            config.setdefault("api_base", api_base)
        api_version = os.getenv("OPENAI_API_VERSION")
        if api_version:
            config.setdefault("api_version", api_version)
        return config

    @staticmethod
    def From(litellm_config=None):
        """
        Build generic LiteLLM model config from explicit config or environment variables.

        Args:
            litellm_config (dict, optional): Explicit config. If not provided, uses env vars.

        Returns:
            dict: Config dict with keys: provider, model, api_key, api_base, api_version, deployment (as available)
        """
        config = litellm_config.copy() if litellm_config else {}
        # Provider: openai, azure, ollama, etc.
        config.setdefault("provider", os.getenv("LITELLM_PROVIDER", "openai"))
        config.setdefault("model", os.getenv("LITELLM_MODEL", "gpt-4.1"))
        config.setdefault("api_key", os.getenv("LITELLM_API_KEY") or os.getenv("OPENAI_API_KEY"))
        config.setdefault("api_base", os.getenv("LITELLM_API_BASE") or os.getenv("OPENAI_API_BASE"))
        config.setdefault("api_version", os.getenv("LITELLM_API_VERSION") or os.getenv("OPENAI_API_VERSION"))
        config.setdefault("deployment", os.getenv("LITELLM_DEPLOYMENT") or os.getenv("AZURE_DEPLOYMENT_NAME"))
        return config
