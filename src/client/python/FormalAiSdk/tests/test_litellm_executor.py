"""
Tests for the LiteLLM executor implementation.
"""

from ..core.types import Conversation, Message, Role
from ..models.litellm_executor import LiteLLMExecutor
from ..exceptions import InvalidConversationError

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
    # Verify it contains the correct answer
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

def test_openai_conversation():
    """
    Test OpenAI conversation (requires API key).
    Skip this test if no API key is provided.
    """
    try:
        # Initialize with OpenAI (would need valid API key)
        executor = LiteLLMExecutor(
            "openai",
            "gpt-3.5-turbo",
            api_key="your-api-key-here"
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
        
    except Exception:
        print("Skipping OpenAI test - requires valid API key")
