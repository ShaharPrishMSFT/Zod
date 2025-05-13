# Repository Survey Report

## Top-Level Folders

- **docs/**: Project documentation, including main and Python SDK READMEs.
- **personalities/**: Agent personality definitions and configurations for various roles (e.g., generalist, configuration, UI).
- **procedures/**: Procedural scripts, live prompts, and related utilities for agentic workflows.
- **requests/**: Worktree communication system for structured cross-worktree requests.
- **src/**: Main source code, including:
  - **client/python/**: Python SDK, core logic, models, and tests.
  - **lang/**: AgentLingua DSL, grammar, and examples.

## Key Modules

- **FormalAiSdk**: Core Python SDK for managing AI model conversations (trunk/fork architecture).
- **AgentLingua**: Domain-specific language for agent behaviors and state management.
- **Personalities**: Modular agent personalities for different operational domains.
- **Procedures**: Self-evolving agentic prompts and procedural logic.

## Test Locations

- **src/client/python/FormalAiSdk/tests/**: Main test suite for the Python SDK.
- **src/lang/tests/**: Tests for AgentLingua language components.

## Tooling and Config Files

- **src/client/python/pytest.ini**: Pytest configuration for Python tests.
- **src/client/python/setup.py**: Python package setup script.
- No `.pre-commit-config.yaml` or CI/CD config files (.github/, .gitlab-ci.yml) found in the listed structure.

## Notable Structure and Quirks

- **Deeply nested SDK**: The FormalAiSdk is nested under `src/client/python/`.
- **Personalities and Requests**: Unique modular structure for agent personalities and inter-worktree communication.
- **Procedures directory**: Contains live prompts and procedural scripts, supporting agentic iteration.
- **No top-level tests/**: All tests are within relevant submodules.
- **No standard virtual environment or requirements.txt detected in the root or src/client/python/**.
