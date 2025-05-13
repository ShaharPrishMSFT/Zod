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
from ..models.litellm_executor import LiteLLMExecutor
from ..exceptions import InvalidConversationError

openai_enabled = os.getenv("RUN_OPENAI_TESTS") == "1"

def test_ollama_conversation():
    """Test a basic conversation with Ollama."""
    # Initialize the executor with Ollama
    executor = LiteLLMExecutor("ollama", "tinyllama")
    
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
    executor = LiteLLMExecutor("ollama", "tinyllama")
    
    # Try to execute with empty conversation
    conversation = Conversation()
    
    try:
        executor.execute(conversation)
        assert False, "Should have raised InvalidConversationError"
    except InvalidConversationError:
        assert True

@pytest.mark.skipif(not openai_enabled, reason="OpenAI tests are disabled by default. Set RUN_OPENAI_TESTS=1 to enable.")
def test_openai_conversation():
    """
    Test OpenAI conversation (requires API key).
    This test will only run if RUN_OPENAI_TESTS=1 is set in the environment.
    The model used can be set via OPENAI_MODEL (default: gpt-4.1).
    """
    api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1")
    if not api_key or api_key == "your-api-key-here":
        pytest.skip("No valid OpenAI API key provided.")

    # Initialize with OpenAI
    executor = LiteLLMExecutor(
        "openai",
        model,
        api_key=api_key
    )

    # Create test conversation
    conversation = Conversation()
    conversation = conversation.add_message(
        Role.CLIENT,
        "What are the key features of Python?"
    )

    # Get response
    response = executor.execute(conversation)

    # Assertions
    assert isinstance(response, Message)
    assert response.role == Role.AGENT
    assert response.content  # Should have some content

@pytest.mark.skipif(not openai_enabled, reason="OpenAI tests are disabled by default. Set RUN_OPENAI_TESTS=1 to enable.")
def test_openai_invalid_model():
    """
    Test OpenAI executor with an invalid model name to ensure proper error handling.
    This test will only run if RUN_OPENAI_TESTS=1 is set in the environment.
    """
    api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    if not api_key or api_key == "your-api-key-here":
        pytest.skip("No valid OpenAI API key provided.")

    executor = LiteLLMExecutor(
        "openai",
        "nonexistent-model",
        api_key=api_key
    )
    conversation = Conversation()
    conversation = conversation.add_message(
        Role.CLIENT,
        "This should fail due to invalid model."
    )
    with pytest.raises(Exception):
        executor.execute(conversation)
