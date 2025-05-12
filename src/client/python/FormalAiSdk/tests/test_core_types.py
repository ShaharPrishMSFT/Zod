"""
Tests for core data structures in FormalAI SDK.
"""

import pytest
from ..core.types import Role, Message, Conversation

def test_role_enum():
    """Test Role enum functionality."""
    # Test enum values exist
    assert Role.AGENT
    assert Role.CLIENT
    
    # Test enum value comparison
    assert Role.AGENT != Role.CLIENT
    
    # Test enum type
    assert isinstance(Role.AGENT, Role)
    assert isinstance(Role.CLIENT, Role)

def test_message_creation():
    """Test Message class creation and attributes."""
    # Test basic message creation
    msg = Message(role=Role.AGENT, content="Hello")
    assert msg.role == Role.AGENT
    assert msg.content == "Hello"
    assert msg.metadata == {}
    
    # Test message with metadata
    metadata = {"temperature": 0.7}
    msg = Message(role=Role.CLIENT, content="Hi", metadata=metadata)
    assert msg.role == Role.CLIENT
    assert msg.content == "Hi"
    assert msg.metadata == metadata

def test_message_immutability():
    """Test that Message attributes behave correctly."""
    msg = Message(role=Role.AGENT, content="Hello")
    
    # Verify attributes can't be changed
    with pytest.raises(AttributeError):
        msg.role = Role.CLIENT
    with pytest.raises(AttributeError):
        msg.content = "New content"
    
    # Verify metadata dict is independent
    metadata = {"key": "value"}
    msg = Message(role=Role.AGENT, content="Hello", metadata=metadata)
    metadata["key"] = "new_value"
    assert msg.metadata["key"] == "value"

def test_conversation_creation():
    """Test Conversation class creation."""
    # Test empty conversation
    conv = Conversation()
    assert len(conv.messages) == 0
    
    # Test conversation with initial messages
    messages = [
        Message(role=Role.CLIENT, content="Hello"),
        Message(role=Role.AGENT, content="Hi there")
    ]
    conv = Conversation(messages=messages)
    assert len(conv.messages) == 2
    assert conv.messages == messages

def test_conversation_add_message():
    """Test adding messages to conversation."""
    conv = Conversation()
    
    # Add client message
    # Add client message and get new conversation
    conv = conv.add_message(Role.CLIENT, "Hello")
    assert len(conv.messages) == 1
    assert conv.messages[0].role == Role.CLIENT
    assert conv.messages[0].content == "Hello"
    
    # Add agent message and get new conversation
    conv = conv.add_message(Role.AGENT, "Hi there")
    assert len(conv.messages) == 2
    assert conv.messages[1].role == Role.AGENT
    assert conv.messages[1].content == "Hi there"
    
    # Verify message order is preserved
    messages = [msg.content for msg in conv.messages]
    assert messages == ["Hello", "Hi there"]

def test_conversation_message_independence():
    """Test that modifying the messages list doesn't affect the conversation."""
    # Create a conversation with messages
    messages = [
        Message(role=Role.CLIENT, content="Hello"),
        Message(role=Role.AGENT, content="Hi")
    ]
    conv = Conversation(messages=messages)
    
    # Try to modify original messages list
    messages.append(Message(role=Role.CLIENT, content="New message"))
    assert len(conv.messages) == 2  # Original conversation should be unchanged
    
    # Verify conversation messages can't be modified externally
    with pytest.raises(AttributeError):
        conv.messages = []
