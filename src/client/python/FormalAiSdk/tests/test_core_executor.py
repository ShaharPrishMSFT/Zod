"""
Tests for the base ModelExecutor class.
"""

import pytest
from ..core.executor import ModelExecutor
from ..core.types import Conversation, Message, Role
from ..exceptions import ExecutionError

def test_model_executor_is_abstract():
    """Test that ModelExecutor cannot be instantiated directly."""
    with pytest.raises(TypeError):
        ModelExecutor()

def test_execute_method_required():
    """Test that concrete implementations must implement execute method."""
    class IncompleteExecutor(ModelExecutor):
        pass
    
    with pytest.raises(TypeError):
        IncompleteExecutor()

def test_concrete_implementation():
    """Test that a concrete implementation works correctly."""
    class TestExecutor(ModelExecutor):
        def execute(self, conversation: Conversation) -> Message:
            return Message(
                role=Role.AGENT,
                content="Test response",
                metadata={"test": True}
            )
    
    # Should instantiate without error
    executor = TestExecutor()
    
    # Should execute correctly
    conversation = Conversation([
        Message(role=Role.CLIENT, content="Test message")
    ])
    response = executor.execute(conversation)
    
    assert isinstance(response, Message)
    assert response.role == Role.AGENT
    assert response.content == "Test response"
    assert response.metadata == {"test": True}

def test_executor_type_checking():
    """Test type checking in concrete implementation."""
    class TestExecutor(ModelExecutor):
        def execute(self, conversation: Conversation) -> Message:
            if not isinstance(conversation, Conversation):
                raise TypeError("conversation must be a Conversation instance")
            return Message(role=Role.AGENT, content="Test response")
    
    executor = TestExecutor()
    
    # Test with invalid conversation type
    with pytest.raises(TypeError):
        executor.execute("not a conversation")
    
    # Test with valid conversation
    conversation = Conversation([
        Message(role=Role.CLIENT, content="Hello")
    ])
    response = executor.execute(conversation)
    assert isinstance(response, Message)
