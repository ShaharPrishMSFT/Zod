"""
Script to parse input using grammar.lark and walk the tree with BaseInterpreter.
Usage:
    python parse_and_walk.py [source_file]
If no file is given, reads from stdin.
"""

import sys
import pathlib
from lark import Lark
from src.lang.runtime.base_interpreter import BaseInterpreter

GRAMMAR_PATH = str(pathlib.Path(__file__).parent.parent / "grammar" / "grammar.lark")

def main():
    if len(sys.argv) > 1:
        code = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    else:
        code = sys.stdin.read()

    parser = Lark.open(GRAMMAR_PATH, parser="lalr", propagate_positions=True, maybe_placeholders=False)
    tree = parser.parse(code)
    interpreter = BaseInterpreter()
    result = interpreter.transform(tree)
    print(result)

if __name__ == "__main__":
    main()
