# TODO: This test should be auto-generated to match the current grammar and sample files.

import pathlib
import sys
import pytest
from lark import Lark

# Ensure project root is on sys.path for absolute imports
sys.path.insert(0, str(pathlib.Path(__file__).parents[4]))

from ...base_interpreter import BaseInterpreter

EXAMPLES_DIR = pathlib.Path(__file__).parents[3] / "examples"
GRAMMAR_PATH = pathlib.Path(__file__).parents[3] / "grammar" / "grammar.lark"

@pytest.mark.parametrize("example_path", list(EXAMPLES_DIR.glob("*.al")))
def test_base_interpreter_walks_example(example_path):
    code = example_path.read_text(encoding="utf-8")
    parser = Lark.open(str(GRAMMAR_PATH), parser="lalr", propagate_positions=True, maybe_placeholders=False)
    tree = parser.parse(code)
    interpreter = BaseInterpreter()
    result = interpreter.transform(tree)
    assert result is not None
