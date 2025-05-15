import sys
from pathlib import Path
project_root = str(Path(__file__).resolve().parents[5])
sys.path.insert(0, project_root)

from src.common.env import load_project_env
load_project_env()

"""
Tests for the OpenAI executor (via LiteLLMExecutor with OpenAI config).

These tests are disabled by default.
To enable, set RUN_OPENAI_TESTS=1 and provide a valid OPENAI_API_KEY in your environment or .env file.

Example:
    RUN_OPENAI_TESTS=1 pytest src/client/python/FormalAiSdk/tests/test_openai_executor.py
"""

import os
import pytest

@pytest.fixture(autouse=True, scope="session")
def test_init():
    print(f"[fixture] RUN_OPENAI_TESTS={os.getenv('RUN_OPENAI_TESTS')}")
    print(f"[fixture] OPENAI_API_KEY={os.getenv('OPENAI_API_KEY')}")
    if os.getenv("RUN_OPENAI_TESTS") != "1":
        pytest.skip("RUN_OPENAI_TESTS is not set to '1' after loading .env. Test environment is not configured correctly.")

from ..core.openai_executor import OpenAIExecutor

def test_openai_executor_basic():
    """
    Test the OpenAI executor using the official OpenAI Python SDK.
    This test is opt-in and requires RUN_OPENAI_TESTS=1 and a valid OPENAI_API_KEY.
    """
    import os
    import pytest
    if os.getenv("RUN_OPENAI_TESTS") != "1":
        pytest.skip("OpenAI tests are disabled by default. Set RUN_OPENAI_TESTS=1 to enable.")

    print(f"[test] RUN_OPENAI_TESTS={os.getenv('RUN_OPENAI_TESTS')}")
    print(f"[test] OPENAI_API_KEY={os.getenv('OPENAI_API_KEY')}")

    try:
        executor = OpenAIExecutor()
        result = executor.execute("Say hello from the OpenAI executor test.")
        assert result
        assert "hello" in result.lower(), f"Response does not contain 'hello': {result}"
        print("OpenAI API response:", result)
    except Exception as e:
        # Only skip if the error is due to missing credentials or setup
        if "No valid OpenAI API key provided" in str(e) or "RUN_OPENAI_TESTS" in str(e):
            pytest.skip(f"Test skipped due to setup issue: {e}")
        raise
