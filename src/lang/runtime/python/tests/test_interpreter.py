r"""
NOTE: For all tests that require importing the FormalAiSdk package, you must set
the PYTHONPATH environment variable to include the absolute path to 'src/client/python'
before running pytest.

LLM Integration tests use only the Ollama model: phi3:mini

Recommended for Windows (cmd):

    set PYTHONPATH=C:\\src\\zod\\worktrees\\formalai.lang\\src\\client\\python
    pytest src\\lang\\runtime\\python\\tests\\test_interpreter.py

For Windows PowerShell:

    $env:PYTHONPATH="C:\src\zod\worktrees\formalai.lang\src\client\python"
    pytest src\lang\runtime\python\tests\test_interpreter.py

For bash (Linux/Mac/WSL):

    export PYTHONPATH=/absolute/path/to/src/client/python
    pytest src/lang/runtime/python/tests/test_interpreter.py

Do NOT rely on sys.path hacks in this file; they are unreliable with pytest.
"""

import pytest
from src.lang.runtime.python.interpreter.interpreter import AIInterpreter

def test_interpreter_instantiation():
    interp = AIInterpreter("test_path.al")
    assert interp.ai_file_path == "test_path.al"
    assert interp.parser is None
    assert interp.session is None

def test_connect_parser_stub():
    interp = AIInterpreter("test_path.al")
    interp.connect_parser()
    assert interp.parser is None  # Layer 1: parser is just a placeholder

def test_run_llm_integration():
    """Test LLM integration using run_llm with a real LLM call. Requires Ollama model: phi3:mini."""
    ai_content = (
        "context my.agent\n"
        "--begin\n"
        "Hello LLM\n"
        "--end\n"
    )
    from src.lang.runtime.python.interpreter import interpreter as interp_mod
    from FormalAiSdk.exceptions.base import ModelError

    if interp_mod.LiteLLMExecutor is None or interp_mod.ModelFork is None:
        raise RuntimeError("FormalAiSdk not available")

    interp = interp_mod.AIInterpreter.from_code(ai_content)
    try:
        messages = interp.run_llm(prompt="What is your context?", model_name="ollama", model_variant="phi3:mini")
    except ModelError as e:
        # Fail if the model is not available or any other error occurs
        raise AssertionError(f"LLM integration failed: {e}")

    # Should contain the context and an LLM response
    actors = [m["actor"] for m in messages]
    contents = [m["content"] for m in messages]
    assert "user" in actors
    # The LLM response may be attributed to "fork1" or another actor, not necessarily "llm"
    assert len(set(actors)) >= 2
    assert "Hello LLM" in contents
    # Can't assert exact LLM response, but should have at least two messages
    assert len(messages) >= 2
import socket

def is_ollama_running(host="localhost", port=11434):
    """Check if Ollama server is running on the given host and port."""
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except Exception:
        return False

@pytest.mark.skipif(not is_ollama_running(), reason="Ollama server is not running on localhost:11434")
def test_run_llm_real_ollama_phi():
    """Integration test: Run real LLM call using Ollama and the phi model, configurable via .env."""
    ai_content = (
        "context my.agent\n"
        "--begin\n"
        "What is the capital of France?\n"
        "--end\n"
    )
    model_name = os.environ.get("OLLAMA_MODEL", "ollama")
    model_variant = os.environ.get("OLLAMA_VARIANT", "phi")
    interp = AIInterpreter.from_code(ai_content)
    messages = interp.run_llm(prompt="What is the capital of France?", model_name=model_name, model_variant=model_variant)
    # Should contain a user message and an LLM response
    actors = [m["actor"] for m in messages]
    contents = [m["content"] for m in messages]
    assert "user" in actors
    assert any("paris" in c.lower() for c in contents), "Expected 'paris' in LLM response"
def test_process_context_extracts_id_and_content():
    ai_content = (
        "context my.agent\n"
        "--begin\n"
        "Hello world\n"
        "--end\n"
    )
    interp = AIInterpreter.from_code(ai_content)
    assert interp.context_id == "my.agent"
    assert interp.context_content == "Hello world"

def test_process_context_no_id():
    ai_content = (
        "context\n"
        "--begin\n"
        "Just context text\n"
        "--end\n"
    )
    interp = AIInterpreter.from_code(ai_content)
    assert interp.context_id is None
    assert interp.context_content == "Just context text"
def test_process_context_missing_block():
    pass

def test_if_statement_execution():
    ai_content = (
        "context [today is monday]\n"
        "if [it is monday]\n"
        "{\n"
        "return [Respond saying that Garfield is sad]\n"
        "}\n"
        "return [Respond saying that it's not monday]\n"
    )

    interp = AIInterpreter.from_code(ai_content)
    assert "Welcome, admin!" in interp.context_content

def test_if_else_statement_execution():
    ai_content = (
        "context [today is monday]\n"
        "ifelse [the user is an admin]\n"
        "{\n"
        "return [Welcome, admin!]\n"
        "}\n"
        "else\n"
        "{\n"
        "return [Access denied.]\n"
        "}\n"
    )

    interp = AIInterpreter.from_code(ai_content)
    assert "Welcome, admin!" not in interp.context_content
    assert "Access denied." in interp.context_content
    ai_content = "no context here"
    with pytest.raises(ValueError):
        AIInterpreter.from_code(ai_content)

def test_from_code_classmethod():
    ai_content = (
        "context my.agent\n"
        "--begin\n"
        "Hello from code\n"
        "--end\n"
    )
    interp = AIInterpreter.from_code(ai_content)
    assert interp.context_id == "my.agent"
    assert interp.context_content == "Hello from code"
    assert interp.ai_file_path == "<from_code>"

def test_from_file_classmethod(tmp_path):
    ai_content = (
        "context my.agent\n"
        "--begin\n"
        "Hello from file\n"
        "--end\n"
    )
    file_path = tmp_path / "test_file.al"
    file_path.write_text(ai_content, encoding="utf-8")
    interp = AIInterpreter.from_file(str(file_path))
    assert interp.context_id == "my.agent"
    assert interp.context_content == "Hello from file"
    assert interp.ai_file_path == str(file_path)
import pytest
import socket

def is_ollama_running(host="localhost", port=11434):
    """Check if Ollama server is running on the given host and port."""
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except Exception:
        return False

@pytest.mark.skipif(not is_ollama_running(), reason="Ollama server is not running on localhost:11434")
def test_run_llm_real_ollama_phi():
    """Integration test: Run real LLM call using Ollama and the phi model."""
    from src.lang.runtime.python.interpreter.interpreter import AIInterpreter
    ai_content = (
        "context my.agent\n"
        "--begin\n"
        "What is the capital of France?\n"
        "--end\n"
    )
    interp = AIInterpreter.from_code(ai_content)
    messages = interp.run_llm(prompt="What is the capital of France?", model_name="ollama", model_variant="phi3:mini")
    # Should contain a user message and an LLM response
    actors = [m["actor"] for m in messages]
    contents = [m["content"] for m in messages]
    assert "user" in actors
    assert any("paris" in c.lower() for c in contents), "Expected 'paris' in LLM response"