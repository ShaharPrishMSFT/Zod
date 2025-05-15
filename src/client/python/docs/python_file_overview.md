# Python File Overview for `src/client/python`

This document provides an overview of the Python files in `src/client/python`, grouped by folder (most important first), with a brief description of each file's contents and purpose.

---

## FormalAiSdk/ (Main SDK Codebase)

### core/
- **executor.py**: Core executor logic for running models.
- **openai_executor.py**: Direct OpenAI API executor implementation.

### models/
- **litellm_executor.py**: Executor using the LiteLLM abstraction.
- **llm_models.py**: Model configuration and management.
- **autogen/**: (Subfolder for autogen-related model code.)

### sdk/
- **fork.py**: SDK logic for process forking and session management.
- **session.py**: Session management for SDK usage.

### examples/
- **basic_conversation.py**: Example script for a basic conversation using the SDK.
- **chat_with_azure.py**: Example script for Azure OpenAI chat.

### exceptions/
- **base.py**: Base exception classes for the SDK.

### utils/
- **check_openai_direct.py**: Utility for checking OpenAI API connectivity.
- **check_litellm_openai.py**: Utility for checking LiteLLM/OpenAI integration.
- **azure_openai_litellm_issue_report.md**: Issue report template for Azure OpenAI + LiteLLM.

### tests/
- **test_openai_executor.py**: Tests for the OpenAI executor.
- **test_litellm_executor.py**: Tests for the LiteLLM executor.
- **test_llm_models.py**: Tests for model configuration.
- **conftest.py**: Pytest configuration and fixtures.
- **sdk/**: SDK integration and session tests.

### Other files
- **exceptions.py**: (May be a legacy or re-export file.)

---

## src/common/

- **env.py**: Shared environment loader for loading `.env` files and environment variables.
- **check_openai.py**: Minimal utility to check OpenAI API connectivity using the official SDK.

---

## src/client/python/docs/

- **dev_procedures.md**: Developer procedures and workflow documentation for the Python SDK/client.
- **python_file_overview.md**: (This file) Overview of Python files and their purposes.

---

## src/client/python/pytest.ini

- **pytest.ini**: Pytest configuration file for the Python SDK test suite.
