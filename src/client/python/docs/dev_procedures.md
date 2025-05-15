# Developer Procedures for `src/client/python`

This document outlines the key procedures, tools, and folder structure for working with the Python SDK/client in `src/client/python`.

---

## Folder Structure Overview

- `FormalAiSdk/` — Main SDK codebase.
- `models/` — Model and executor classes (e.g., `litellm_executor.py`, `llm_models.py`).
- `core/` — Core logic and executors (e.g., `openai_executor.py`).
- `examples/` — Example usage scripts for the SDK.
- `tests/` — Test suite, including unit, integration, and SDK tests.
- `utils/` — Utility scripts (e.g., `check_openai.py`).

---

## Key Tools and Scripts

### Running Tests

- **Run all tests:**  
  ```bash
  pytest src/client/python/FormalAiSdk/tests/
  ```
- **Run a specific test file:**  
  ```bash
  pytest src/client/python/FormalAiSdk/tests/test_openai_executor.py
  ```

### Running Examples

- **Execute example scripts:**  
  ```bash
  python src/client/python/FormalAiSdk/examples/basic_conversation.py
  ```

### Using Executors

- **OpenAI Executor:**  
  - Use `core/openai_executor.py` for direct OpenAI API access.
  - Configure environment variables (`OPENAI_API_KEY`, `OPENAI_API_BASE`, etc.) in your `.env` file.
- **Other Executors:**  
  - See `models/` for additional executors and model integrations.

### Environment Setup

- **Check OpenAI environment:**  
  ```bash
  python src/common/check_openai.py
  ```

---

## Development Workflow

- Add new models or executors in `models/` or `core/`.
- Add or update tests in `tests/` to cover new or changed functionality.
- Add example scripts in `examples/` to demonstrate usage.
- Use `utils/` for utility scripts and environment checks.
- Run tests and example scripts before committing changes.

---

## Automation and CI

- Use `pytest` for automated test coverage.
- (Document any CI integration, linting, or formatting tools if present.)
- Use scripts in `utils/` for environment validation.

---

## Troubleshooting

- For test failures, check the relevant test file in `tests/`.
- For environment or API issues, use `check_openai.py` to verify configuration.
- For SDK or executor issues, review the implementation in `core/` and `models/`.
