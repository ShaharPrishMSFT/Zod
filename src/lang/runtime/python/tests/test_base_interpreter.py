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

# Only test the specific file for focused debugging
example_file = EXAMPLES_DIR / "02_rule_with_else.al"

@pytest.mark.parametrize("example_path", [example_file])
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
