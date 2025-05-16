# Installation Guide

This directory contains installation guides for various components of the project.

## Available Guides

- [AutoGen (AutoFac)](./autogen.md) - Installation guide for AutoGen with Ollama support
- [Ollama](./ollama.md) - Installation and configuration guide for Ollama LLM runtime

## FormalAiSdk Local Package Installation

To use the FormalAiSdk as a robust, reusable Python package in your environment:

1. **Navigate to the SDK root:**
   ```
   cd src/client/python
   ```

2. **Install the SDK in editable mode:**
   ```
   pip install -e .
   ```

   This makes the `FormalAiSdk` package importable from anywhere in your environment.

3. **Usage Example:**
   ```python
   from FormalAiSdk.models.llm_models import LlmModels
   ```

4. **Troubleshooting:**
   - If you get `ModuleNotFoundError`, ensure you ran the install command from the correct directory and are using the right Python environment.
   - If you restructure the SDK, re-run the install command.

5. **Uninstall:**
   ```
   pip uninstall FormalAiSdk
   ```

## Quick Start

1. Install Ollama first using the [Ollama installation guide](./ollama.md)
2. Then follow the [AutoGen installation guide](./autogen.md) to set up the agent framework

---

## Setting Up Environment Secrets (Windows/PowerShell)

To quickly set up your `.env` file and required secrets, run the provided PowerShell script:

```powershell
scripts/setup_env.ps1
```

- This will copy `.env.example` to `.env` if needed.
- You will be prompted to enter any missing secret values (such as `OPENAI_API_KEY`).
- Optionally, you can install Python dependencies as part of the setup.

After running the script, your `.env` file will be ready for use at the root of your worktree (e.g., `c:/src/Max/worktrees/formalai.python.infra/.env`).

### How to Test Your Environment in CMD

1. **Check that `.env` exists and contains your secrets:**
   - Open `.env` in a text editor and verify that `OPENAI_API_KEY` is present and set.

2. **Test in CMD that the variable is available to Python:**
   - By default, Python scripts do not automatically load `.env` files unless you use a package like `python-dotenv`.
   - To check if the variable is available in your current CMD session:
     ```
     set OPENAI_API_KEY
     ```
     This should print the value if it is set in your environment.

   - To test that Python can see it, run:
     ```
     python -c "import os; print(os.environ.get('OPENAI_API_KEY'))"
     ```
     This should print your API key if it is set in the environment.

3. **If using `.env` only (not global env vars):**
   - Use a tool like `python-dotenv` or ensure your application loads `.env` at startup.
   - To test with `python-dotenv`:
     ```
     pip install python-dotenv
     python -m dotenv run -- python your_script.py
     ```
   - Or, temporarily set the variable in your CMD session:
     ```
     set OPENAI_API_KEY=your-key-here
     python your_script.py
     ```

---

## Need Help?

If you encounter any issues during installation, please refer to the troubleshooting sections in each guide.
