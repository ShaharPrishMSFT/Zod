# Technical Specification

## Overview
Infrastructure design for a structured, Pythonic model execution abstraction.

## Core Components

### Message Types
```python
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Dict

class Role(Enum):
    AGENT = auto()
    CLIENT = auto()

@dataclass
class Message:
    role: Role
    content: str
    metadata: Dict = field(default_factory=dict)

@dataclass
class Conversation:
    messages: List[Message]
    
    def add_message(self, role: Role, content: str) -> None:
        self.messages.append(Message(role=role, content=content))
```

### Model Executor
```python
class ModelExecutor:
    """Base class for model execution"""
    
    def execute(self, conversation: Conversation) -> Message:
        """
        Execute model with given conversation history.
        Returns the model's response as a Message.
        
        Example:
            executor = ModelExecutor()
            convo = Conversation([
                Message(Role.CLIENT, "Hello"),
                Message(Role.AGENT, "Hi there")
            ])
            response = executor.execute(convo)
        """
        raise NotImplementedError
```

## Implementation Details

### Project Structure
```
src/
  client/
    python/
      FormalAiSdk/
        core/
          types.py      # Core data structures (Message, Conversation)
          executor.py   # ModelExecutor base class
        models/        # Specific model implementations
          gpt.py      # Example concrete executor
        exceptions.py  # Basic exceptions
```

### Error Handling
- Simple, descriptive exception types
- Clear error messages
- Basic retry logic where appropriate

```python
class ExecutionError(Exception):
    """Base class for execution errors"""
    pass

class ModelError(ExecutionError):
    """Model-specific errors"""
    pass

class InvalidConversationError(ExecutionError):
    """Invalid conversation structure"""
    pass
```

### Current Phase
- Implementation of core data structures
- Basic executor interface
- Error definitions

### Next Steps
- Implement concrete model executor(s)
- Add basic retry logic
- Add simple logging
