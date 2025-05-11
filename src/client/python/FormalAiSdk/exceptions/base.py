"""
Base exception classes for FormalAI SDK.
"""

class ExecutionError(Exception):
    """Base class for execution errors in FormalAI SDK."""
    pass

class ModelError(ExecutionError):
    """
    Raised when there is a model-specific error during execution.
    
    This could include issues like:
    - Model API errors
    - Invalid model responses
    - Model timeout issues
    """
    pass

class InvalidConversationError(ExecutionError):
    """
    Raised when there are issues with conversation structure or content.
    
    This could include:
    - Missing required fields
    - Invalid message sequences
    - Malformed message content
    """
    pass
