"""
Tests for the LiteLLM executor implementation.

OpenAI-related tests are disabled by default.
To enable them, set the environment variable RUN_OPENAI_TESTS=1 before running pytest.
API keys and test flags can be set in a .env file at the project root.
If python-dotenv is installed, .env will be loaded automatically.

Example:
    RUN_OPENAI_TESTS=1 pytest
    # or set in .env:
    # OPENAI_API_KEY=sk-...
    # RUN_OPENAI_TESTS=1

"""

try:
    from dotenv import load_dotenv
    load_dotenv(override=False)
except ImportError:
    pass

import os
import pytest

from ..core.types import Conversation, Message, Role
from ..core.litellm_executor import LiteLLMExecutor
from ..models.llm_models import LlmModels
from ..exceptions import InvalidConversationError

openai_enabled = os.getenv("RUN_OPENAI_TESTS") == "1"

def test_ollama_conversation():
    """Test a basic conversation with Ollama."""
    # Initialize the executor with Ollama
    config = LlmModels.From({"provider": "ollama", "model": "ollama/mistral"})
    executor = LiteLLMExecutor(config)
    
    # Create a test conversation
    conversation = Conversation()
    # Add initial message
    conversation = conversation.add_message(Role.CLIENT, "Hello, what is 2+2?")
    
    # Get first response (2+2)
    response = executor.execute(conversation)
    # Verify it contains the correct answer
    assert any(ans in response.content.lower() for ans in ["4", "four"]), \
        f"Response should contain the answer '4'. Got: {response.content}"
    
    # Create new conversation with response
    messages = list(conversation.messages) + [response]
    conversation = Conversation(messages=messages)
    
    # Add follow-up question
    conversation = conversation.add_message(Role.CLIENT, "What is 4 multiplied by 2?")
    
    # Get second response (4*2)
    response = executor.execute(conversation)
    # Accept verbose or step-by-step answers as long as "8" or "eight" appears anywhere
    if not any(ans in response.content.lower() for ans in ["8", "eight"]):
        print("WARNING: Model did not return the correct answer for 4*2. Full response:")
        print(response.content)
    assert any(ans in response.content.lower() for ans in ["8", "eight"]), \
        f"Response should contain the answer '8'. Got: {response.content}"
    
    # Additional assertions
    assert isinstance(response, Message)
    assert response.role == Role.AGENT
    assert isinstance(response.metadata, dict)

def test_empty_conversation():
    """Test handling of empty conversations."""
    config = LlmModels.From({"provider": "ollama", "model": "ollama/mistral"})
    executor = LiteLLMExecutor(config)
    
    # Try to execute with empty conversation
    conversation = Conversation()
    
    try:
        executor.execute(conversation)
        assert False, "Should have raised InvalidConversationError"
    except InvalidConversationError:
        assert True
