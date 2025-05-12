"""
Tests for the SDK session management.
"""

from datetime import datetime
import pytest

from FormalAiSdk.sdk.types import Message
from FormalAiSdk.sdk.session import ModelSession
from FormalAiSdk.sdk.fork import ModelFork
from FormalAiSdk.core.types import Role, Conversation
from FormalAiSdk.tests.sdk.test_fork import MockExecutor

@pytest.fixture
def actor():
    return "test_user"

@pytest.fixture
def mock_executor():
    return MockExecutor()

@pytest.fixture
def session(actor, mock_executor):
    return ModelSession(actor, mock_executor)

def test_init(session, actor):
    """Test session initialization."""
    assert session.actor == actor
    assert len(session.messages) == 0

def test_add_response(session):
    """Test adding responses to session."""
    session.add_response("user", "Hello")
    session.add_response("bot", "Hi there")

    # Check messages were added
    assert len(session.messages) == 2
    
    # Check first message
    msg1 = session.messages[0]
    assert msg1.actor == "user"
    assert msg1.content == "Hello"
    assert isinstance(msg1.timestamp, datetime)

    # Check second message
    msg2 = session.messages[1]
    assert msg2.actor == "bot"
    assert msg2.content == "Hi there"
    assert isinstance(msg2.timestamp, datetime)

def test_to_core_conversation(session, actor):
    """Test conversion to core Conversation format."""
    # Add some messages
    session.add_response(actor, "Hello")
    session.add_response("bot", "Hi there")
    
    # Convert to core format
    conv = session.to_core_conversation()
    
    # Verify conversion
    assert isinstance(conv, Conversation)
    assert len(conv.messages) == 2
    
    # Check role mapping
    assert conv.messages[0].role == Role.CLIENT  # trunk owner
    assert conv.messages[1].role == Role.AGENT   # other actor

def test_fork_creation(session, actor, mock_executor):
    """Test creating a fork from the session."""
    fork = session.Fork("fork1", actor, "Hello")
    
    # Verify fork attributes
    assert isinstance(fork, ModelFork)
    assert fork.fork_id == "fork1"
    assert fork.from_actor == actor
    assert fork.message == "Hello"
    assert fork.executor is mock_executor

def test_fork_without_executor(actor):
    """Test fork creation fails without executor."""
    session = ModelSession(actor)  # No executor provided
    
    with pytest.raises(ValueError):
        session.Fork("fork1", actor, "Hello")
