# Python Components

The Python components of FormalAI include a powerful SDK for managing AI model conversations using a unique trunk/fork architecture.

## Key Components

### SDK
The core SDK provides a structured way to manage AI model interactions through:
- **Trunk Conversations**: Main conversation threads
- **Execution Forks**: Isolated model execution branches
- **Model Executors**: Pluggable execution backends (e.g., LiteLLM)

## Getting Started

1. Install the SDK:
```bash
pip install formalai-sdk
```

2. Create a basic conversation:
```python
from FormalAiSdk.models.litellm_executor import LiteLLMExecutor
from FormalAiSdk.sdk.session import ModelSession

# Initialize with your preferred model
executor = LiteLLMExecutor("ollama", "llama2")
session = ModelSession("user", executor)
```

See the [SDK Examples](sdk/examples.md) for detailed usage patterns and advanced features.
