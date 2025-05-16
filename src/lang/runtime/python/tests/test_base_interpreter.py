# TODO: This test should be auto-generated to match the current grammar and sample files.

import pathlib
import sys
import pytest
from lark import Lark, exceptions

# Ensure src/lang/runtime is on sys.path for direct import
sys.path.insert(0, str(pathlib.Path(__file__).parents[2]))

from base_interpreter import BaseInterpreter

EXAMPLES_DIR = pathlib.Path(__file__).parents[3] / "examples"
GRAMMAR_PATH = pathlib.Path(__file__).parents[3] / "grammar" / "grammar.lark"

# Parameterize over all .al files in the examples directory
example_files = list(EXAMPLES_DIR.glob("*.al"))

import hashlib
import re

def compute_grammar_hash(grammar_path):
    with open(grammar_path, "rb") as f:
        data = f.read()
    return hashlib.sha256(data).hexdigest()[:16]

def extract_grammar_hash_from_base_interpreter(base_interpreter_path):
    with open(base_interpreter_path, "r", encoding="utf-8") as f:
        for line in f:
            m = re.match(r'GRAMMAR_HASH\s*=\s*["\']([0-9a-fA-F]+)["\']', line)
            if m:
                return m.group(1)
    raise RuntimeError("GRAMMAR_HASH not found in base_interpreter.py")

def test_grammar_and_base_interpreter_hash_match():
    """
    Fails if the grammar and generated base_interpreter.py do not have exactly the same hash.
    """
    base_interpreter_path = pathlib.Path(__file__).parents[3] / "runtime" / "base_interpreter.py"
    grammar_hash = compute_grammar_hash(GRAMMAR_PATH)
    generated_hash = extract_grammar_hash_from_base_interpreter(base_interpreter_path)
    assert grammar_hash == generated_hash, (
        f"Grammar file ({GRAMMAR_PATH}) and generated base_interpreter.py ({base_interpreter_path}) "
        f"do not have exactly the same hash.\n"
        f"grammar.lark hash: {grammar_hash}\n"
        f"base_interpreter.py hash: {generated_hash}\n"
        "Please regenerate the base interpreter after editing the grammar."
    )

@pytest.mark.parametrize("example_path", example_files)
def test_base_interpreter_walks_example(example_path):
    code = example_path.read_text(encoding="utf-8")
    parser = Lark.open(str(GRAMMAR_PATH), parser="lalr", propagate_positions=True, maybe_placeholders=False)
    try:
        tree = parser.parse(code)
        interpreter = BaseInterpreter()
        result = interpreter.transform(tree)
        assert result is not None
    except exceptions.LarkError as e:
        # Try to extract line/column info if available
        line = getattr(e, 'line', None)
        column = getattr(e, 'column', None)
        msg = f"\nParse error in file: {example_path}\n"
        if line is not None and column is not None:
            code_lines = code.splitlines()
            error_line = code_lines[line - 1] if 0 < line <= len(code_lines) else ""
            msg += f"At line {line}, column {column}:\n{error_line}\n{' ' * (column - 1)}^\n"
        msg += f"{type(e).__name__}: {e}"
        pytest.fail(msg)
