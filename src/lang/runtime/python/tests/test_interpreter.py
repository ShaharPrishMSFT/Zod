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