# FormalAiSdk: Local Python Package Usage

FormalAiSdk is designed to be used as a robust, reusable Python package across the FormalAI project.

## Local Installation

1. **Navigate to the SDK root:**
   ```
   cd src/client/python
   ```

2. **Install the SDK in editable mode:**
   ```
   pip install -e .
   ```

   This makes the `FormalAiSdk` package importable from anywhere in your environment.

## Usage Example

```python
from FormalAiSdk.models.llm_models import LlmModels
```

## Troubleshooting

- If you get `ModuleNotFoundError`, ensure you ran the install command from the correct directory and are using the right Python environment.
- If you restructure the SDK, re-run the install command.

## Uninstall

```
pip uninstall FormalAiSdk
```

## Notes

- This setup is for local development only. For sharing with others or deployment, consider publishing to a private or public PyPI server.