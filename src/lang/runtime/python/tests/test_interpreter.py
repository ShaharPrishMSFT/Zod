import pytest
from src.lang.runtime.python.interpreter.interpreter import AIInterpreter

def test_interpreter_instantiation():
    interp = AIInterpreter("dummy_file.ai")
    assert interp.ai_file_path == "dummy_file.ai"
    assert interp.parser is None
    assert interp.session is None

def test_connect_parser_stub():
    interp = AIInterpreter("dummy_file.ai")
    interp.connect_parser()
    assert interp.parser is None  # Layer 1: parser is just a placeholder

def test_run_llm_stub_raises():
    interp = AIInterpreter("dummy_file.ai")
    with pytest.raises(NotImplementedError):
        interp.run_llm_stub()

def test_process_context_stub_raises():
    interp = AIInterpreter("dummy_file.ai")
    with pytest.raises(NotImplementedError):
        interp.process_context_stub()

def test_output_results_stub_raises():
    interp = AIInterpreter("dummy_file.ai")
    with pytest.raises(NotImplementedError):
        interp.output_results_stub()

def test_process_context_extracts_id_and_content():
    interp = AIInterpreter("dummy_file.ai")
    ai_content = (
        "context my.agent\n"
        "--begin\n"
        "Hello world\n"
        "--end\n"
    )
    interp.process_context(ai_content)
    assert interp.context_id == "my.agent"
    assert interp.context_content == "Hello world"

def test_process_context_no_id():
    interp = AIInterpreter("dummy_file.ai")
    ai_content = (
        "context\n"
        "--begin\n"
        "Just context text\n"
        "--end\n"
    )
    interp.process_context(ai_content)
    assert interp.context_id is None
    assert interp.context_content == "Just context text"

def test_process_context_missing_block():
    interp = AIInterpreter("dummy_file.ai")
    ai_content = "no context here"
    with pytest.raises(ValueError):
        interp.process_context(ai_content)

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