# AutoGen (AutoFac) Installation

This section focuses on installing AutoGen with Ollama support, also referred to as AutoFac in some contexts.

## Step 1: Install Python Environment

Create and activate a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

## Step 2: Install AutoGen with Ollama Support

Install required packages:
```bash
pip install autogen-agentchat
pip install autogen-ext[ollama]
```

> Optionally include additional extensions depending on your platform or tools.

## Step 3: Verify Installation

Run the following in Python to verify AutoGen is available:
```python
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient

print("AutoGen and Ollama extensions installed successfully.")
```

## Additional Notes

- AutoGen uses `pydantic`, `openai`, and other dependencies; ensure no version conflicts in your environment.
- To run Ollama integration, ensure Ollama is installed and running (`ollama serve`).
- If Ollama is not already running as a service, you can start it from: `C:\Users\shaharp\appdata\local\Programs\Ollama\ollama.exe`
- Ollama runs on port 11434 by default
- Currently configured to work with the tinyllama model (1B parameters, Q4_0 quantization)

This concludes the installation-specific instructions for AutoGen (AutoFac) with Ollama support.
