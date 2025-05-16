"""
NOTE: For all tests that require importing the FormalAiSdk package, you must set
the PYTHONPATH environment variable to include the absolute path to 'src/client/python'
before running pytest.

Recommended for Windows (cmd):

    set PYTHONPATH=C:\src\zod\worktrees\formalai.lang\src\client\python
    pytest src\lang\runtime\python\tests\test_interpreter.py

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

def test_run_llm_stub_raises():
    interp = AIInterpreter("test_path.al")
    with pytest.raises(NotImplementedError):
        interp.run_llm_stub()

def test_run_llm_integration(monkeypatch):
    """Test LLM integration using run_llm with mocks to avoid real LLM calls."""
    ai_content = (
        "context my.agent\n"
        "--begin\n"
        "Hello LLM\n"
        "--end\n"
    )
    from src.lang.runtime.python.interpreter import interpreter as interp_mod

    # Skip if SDK is not available
    if interp_mod.LiteLLMExecutor is None or interp_mod.ModelFork is None:
        pytest.skip("FormalAiSdk not available for monkeypatching")

    class DummyExecutor:
        def __init__(self, *a, **kw): pass
    monkeypatch.setattr(interp_mod.LiteLLMExecutor, "__init__", lambda self, *a, **kw: None)

    # Patch Fork.Answer to just append a dummy message
    def dummy_answer(self, session):
        session.add_response("llm", "LLM response")
    monkeypatch.setattr(interp_mod.ModelFork, "Answer", dummy_answer)

    interp = AIInterpreter.from_code(ai_content)
    messages = interp.run_llm(prompt="What is your context?")
    # Should contain the context and the dummy LLM response
    actors = [m["actor"] for m in messages]
    contents = [m["content"] for m in messages]
    assert "user" in actors
    assert "llm" in actors
    assert "Hello LLM" in contents
    assert "LLM response" in contents
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
def test_process_context_stub_raises():
    interp = AIInterpreter("test_path.al")
    with pytest.raises(NotImplementedError):
        interp.process_context_stub()

def test_output_results_stub_raises():
    interp = AIInterpreter("test_path.al")
    with pytest.raises(NotImplementedError):
        interp.output_results_stub()

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