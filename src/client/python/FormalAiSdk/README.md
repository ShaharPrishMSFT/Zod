# Making FormalAiSdk a Local Python Package

## Context

The FormalAiSdk is a core component used by other parts of the FormalAI project. To avoid import errors and make usage as seamless as a C# class library, you should install it as a local Python package. This allows you to import it anywhere in your environment with:

```python
from FormalAiSdk.models.llm_models import LlmModels
```

## Why Package the SDK?

- Avoids fragile sys.path or PYTHONPATH hacks.
- Ensures consistent imports in scripts, tests, and notebooks.
- Makes the SDK feel like a standard, reusable component.

## How to Set Up for Local Development

### 1. Ensure Directory Structure

You should be in:
```
src/client/python/FormalAiSdk/
```
with all SDK code under this directory and `__init__.py` files in every subdirectory.

### 2. Add a `setup.py` File

Create a `setup.py` in `src/client/python/FormalAiSdk/` with at least:

```python
from setuptools import setup, find_packages

setup(
    name="FormalAiSdk",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.8",
)
```

### 3. Install the SDK Locally

From the `src/client/python/FormalAiSdk/` directory, run:

```
pip install -e .
```

This installs the SDK in "editable" mode, so changes to the code are immediately reflected in your environment.

### 4. Import the SDK Anywhere

Now you can import SDK modules from anywhere in your project:

```python
from FormalAiSdk.models.llm_models import LlmModels
```

No need to set PYTHONPATH or modify sys.path.

## Troubleshooting

- If you get `ModuleNotFoundError`, make sure you ran `pip install -e .` in the correct directory.
- If using a virtual environment, activate it before installing.
- If you restructure the SDK, re-run the install command.

## Notes

- This setup is for local development only. For sharing with others or deployment, consider publishing to a private or public PyPI server.
- If you need to uninstall, run `pip uninstall FormalAiSdk`.