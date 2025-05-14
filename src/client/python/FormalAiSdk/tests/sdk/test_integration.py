"""
Integration tests for the SDK using real Ollama models.
"""

import pytest
from datetime import datetime

from FormalAiSdk.sdk.session import ModelSession
from FormalAiSdk.models.llm_models import LlmModels
from FormalAiSdk.models.litellm_executor import LiteLLMExecutor

@pytest.fixture
def model_config():
    """Create model config for ollama/mistral (Ollama)."""
    return LlmModels.From({"provider": "ollama", "model": "ollama/mistral"})

@pytest.fixture
def executor(model_config):
    """Create LiteLLM executor configured for tinyllama."""
    return LiteLLMExecutor(model_config)

@pytest.fixture
def session(model_config):
    """Create a session with the tinyllama model config."""
    return ModelSession("user", model_config=model_config)

@pytest.mark.integration
def test_basic_math(session):
    """Test basic conversation flow with real model using math question."""
    # Ask a simple math question
    session.add_response("user", "What is 2+2?")
    
    # Create fork and get model response
    fork = session.Fork("fork1", "user", "What is 2+2?")
    fork.Answer(session)
    
    # Verify response
    assert len(session.messages) == 2
    response = session.messages[1]
    assert response.actor == "fork1"
    assert any(ans in response.content.lower() for ans in ["4", "four"]), \
        f"Response should contain the answer '4'. Got: {response.content}"

@pytest.mark.integration
def test_multi_turn_math(session):
    """Test multi-turn conversation with real model building on previous answer."""
    # First turn - ask about 2+2
    session.add_response("user", "What is 2+2?")
    fork1 = session.Fork("fork1", "user", "What is 2+2?")
    fork1.Answer(session)
    
    # Second turn - ask about multiplying the previous answer
    session.add_response("user", "What is that number multiplied by 2?")
    fork2 = session.Fork("fork2", "user", "What is 4 multiplied by 2?")
    fork2.Answer(session)
    
    # Verify responses
    assert len(session.messages) == 4
    assert [msg.actor for msg in session.messages] == ["user", "fork1", "user", "fork2"]
    # Check first answer contains 4
    assert any(ans in session.messages[1].content.lower() for ans in ["4", "four"])
    # Check second answer contains 8
    assert any(ans in session.messages[3].content.lower() for ans in ["8", "eight"])

@pytest.mark.integration
def test_concurrent_math_forks(session):
    """Test multiple forks with different math questions."""
    # Add initial message
    session.add_response("user", "I have some math questions.")
    
    # Create multiple forks with different questions
    fork1 = session.Fork("fork1", "user", "What is 3+3?")
    fork2 = session.Fork("fork2", "user", "What is 5+5?")
    
    # Execute both forks
    fork1.Answer(session)
    fork2.Answer(session)
    
    # Verify responses
    assert len(session.messages) == 3
    assert session.messages[0].actor == "user"
    assert session.messages[1].actor == "fork1"
    assert session.messages[2].actor == "fork2"
    
    # Check answers
    assert any(ans in session.messages[1].content.lower() for ans in ["6", "six"])
    assert any(ans in session.messages[2].content.lower() for ans in ["10", "ten"])
