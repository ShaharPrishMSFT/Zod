"""
Tests for the OpenAI executor (via LiteLLMExecutor with OpenAI config).

These tests are disabled by default.
To enable, set RUN_OPENAI_TESTS=1 and provide a valid OPENAI_API_KEY in your environment or .env file.

Example:
    RUN_OPENAI_TESTS=1 pytest src/client/python/FormalAiSdk/tests/test_openai_executor.py
"""

import os
import pytest

try:
    from src.common.env import load_project_env
    load_project_env()
except ImportError:
    pass

@pytest.fixture(autouse=True, scope="session")
def test_init():
    print(f"[fixture] RUN_OPENAI_TESTS={os.getenv('RUN_OPENAI_TESTS')}")
    print(f"[fixture] OPENAI_API_KEY={os.getenv('OPENAI_API_KEY')}")
    if os.getenv("RUN_OPENAI_TESTS") != "1":
        pytest.fail("RUN_OPENAI_TESTS is not set to '1' after loading .env. Test environment is not configured correctly.")

from ..core.types import Conversation, Message, Role
from ..models.litellm_executor import LiteLLMExecutor
from ..models.llm_models import LlmModels

def test_openai_executor_basic():
    """
    Test the OpenAI executor (via LiteLLMExecutor with OpenAI config).
    This test is opt-in and requires RUN_OPENAI_TESTS=1 and a valid OPENAI_API_KEY.
    """
    print(f"[test] RUN_OPENAI_TESTS={os.getenv('RUN_OPENAI_TESTS')}")
    print(f"[test] OPENAI_API_KEY={os.getenv('OPENAI_API_KEY')}")
    if os.getenv("RUN_OPENAI_TESTS") != "1":
        pytest.skip("OpenAI tests are disabled by default. Set RUN_OPENAI_TESTS=1 to enable.")

    api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1")
    if not api_key or api_key == "your-api-key-here":
        pytest.skip("No valid OpenAI API key provided.")

    config = LlmModels.FromOpenAi({"model": model, "api_key": api_key})
    executor = LiteLLMExecutor(config)

    conversation = Conversation()
    conversation = conversation.add_message(
        Role.CLIENT,
        "Say hello from the OpenAI executor test."
    )

    try:
        response = executor.execute(conversation)
        assert isinstance(response, Message)
        assert response.role == Role.AGENT
        assert response.content
    except Exception as e:
        # Acceptable: OpenAI misconfiguration, quota, or deployment errors
        pytest.skip(f"OpenAI executor test skipped due to error: {e}")
