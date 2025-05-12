"""
Tests for the SDK fork management.
"""

import pytest
from FormalAiSdk.core.types import Message as CoreMessage, Role
from FormalAiSdk.core.executor import ModelExecutor
from FormalAiSdk.sdk.session import ModelSession
from FormalAiSdk.sdk.fork import ModelFork

class MockExecutor(ModelExecutor):
    """Mock executor that returns predefined responses."""
    def execute(self, conversation):
        return CoreMessage(role=Role.AGENT, content="Mock response")

@pytest.fixture
def actor():
    return "test_user"

@pytest.fixture
def mock_executor():
    return MockExecutor()

@pytest.fixture
def test_session(actor):
    return ModelSession(actor)

def test_init(actor, mock_executor):
    """Test fork initialization."""
    fork = ModelFork("fork1", actor, "Hello", mock_executor)
    assert fork.fork_id == "fork1"
    assert fork.from_actor == actor
    assert fork.message == "Hello"
    assert fork.executor is mock_executor

def test_answer(actor, mock_executor, test_session):
    """Test fork execution and response integration."""
    # Add initial message to session
    test_session.add_response(actor, "Hello")
    
    # Create and execute fork
    fork = ModelFork("fork1", actor, "Hello", mock_executor)
    fork.Answer(test_session)
    
    # Verify response was added
    assert len(test_session.messages) == 2
    response = test_session.messages[1]
    assert response.actor == "fork1"
    assert response.content == "Mock response"

def test_multiple_forks(actor, mock_executor, test_session):
    """Test multiple forks interacting with same session."""
    # Add initial message
    test_session.add_response(actor, "Hello")
    
    # Create and execute multiple forks
    fork1 = ModelFork("fork1", actor, "Hello", mock_executor)
    fork2 = ModelFork("fork2", actor, "Hi", mock_executor)
    
    fork1.Answer(test_session)
    fork2.Answer(test_session)
    
    # Verify responses
    assert len(test_session.messages) == 3
    assert test_session.messages[1].actor == "fork1"
    assert test_session.messages[2].actor == "fork2"
