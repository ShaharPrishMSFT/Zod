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

def test_system_message_handling(actor, test_session):
    """Test that system messages from the session are included in fork execution."""
    messages_seen = []
    
    class InspectingExecutor(ModelExecutor):
        def execute(self, conversation):
            nonlocal messages_seen
            messages_seen.extend(conversation.messages)
            return CoreMessage(role=Role.AGENT, content="Response")
    
    test_session.executor = InspectingExecutor()
    
    # Add system and user messages
    test_session.add_response("system", "You are a helpful assistant")
    test_session.add_response(actor, "Hello")
    
    # Execute fork
    fork = ModelFork("fork1", actor, "Test message", test_session.executor)
    fork.Answer(test_session)
    
    # Verify that system message was included
    assert len(messages_seen) == 3  # system + user + fork message
    assert messages_seen[0].content == "You are a helpful assistant"
    assert messages_seen[0].role == Role.AGENT  # system messages are treated as AGENT role
    assert messages_seen[1].content == "Hello"
    assert messages_seen[2].content == "Test message"

def test_fork_conversation_content(actor, test_session):
    """Test the exact content and structure of conversation passed to executor."""
    last_conversation = None
    
    class CapturingExecutor(ModelExecutor):
        def execute(self, conversation):
            nonlocal last_conversation
            last_conversation = conversation
            return CoreMessage(role=Role.AGENT, content="Response")
    
    test_session.executor = CapturingExecutor()
    test_session.add_response("system", "System context")
    test_session.add_response(actor, "User input")
    test_session.add_response("assistant", "Assistant reply")
    
    fork = ModelFork("fork1", actor, "Fork message", test_session.executor)
    fork.Answer(test_session)
    
    assert last_conversation is not None
    assert len(last_conversation.messages) == 4
    
    # Verify exact message content and role mapping
    assert last_conversation.messages[0].content == "System context"
    assert last_conversation.messages[0].role == Role.AGENT
    assert last_conversation.messages[1].content == "User input"
    assert last_conversation.messages[1].role == Role.CLIENT
    assert last_conversation.messages[2].content == "Assistant reply"
    assert last_conversation.messages[2].role == Role.AGENT
    assert last_conversation.messages[3].content == "Fork message"
    assert last_conversation.messages[3].role == Role.CLIENT
