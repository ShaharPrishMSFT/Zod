# AgentLingua Interpreter (Parser) Documentation

## Overview

The AgentLingua interpreter is a parser for the AgentLingua DSL, implemented using [Lark](https://github.com/lark-parser/lark) and a PEG grammar. It is responsible for parsing AgentLingua source files and producing an abstract syntax tree (AST) that can be used for further processing, analysis, or execution by downstream components.

## Key Features

- **PEG-based grammar**: The parser uses a PEG grammar defined in `src/lang/grammar/grammar.peg`.
- **Lark Earley parser**: Utilizes Lark's Earley parser for flexible and robust parsing.
- **AST construction**: Converts the Lark parse tree into a structured AST with node types like `ContextNode`, `NaturalBlockNode`, and `TextNode`.
- **Error handling**: Provides detailed error messages with line/column information and context.

## Main API

The main entry point is the `AgentLinguaParser` class, located at `src/lang/aliparser/aliparser/parser.py`.

### Example Usage

```python
from src.lang.aliparser.aliparser.parser import AgentLinguaParser

source = '''
# Comment
context my.agent
--begin
Hello world
--end
'''

parser = AgentLinguaParser()
tree = parser.parse(source)         # Returns a Lark parse tree
ast_nodes = parser.parse_ast(source)  # Returns a list of AST nodes
```

### AST Node Types

- `ContextNode`: Represents a context declaration (e.g., `context my.agent ...`).
- `NaturalBlockNode`: Represents a block of natural language text.
- `TextNode`: Represents a line or segment of text.

## How It Is Used

- The parser is used in test cases (see `src/lang/aliparser/aliparser/test_parser.py`) to verify correct parsing and AST construction.
- It can be used as a library to parse AgentLingua source files and obtain a structured representation for further processing.
- The AST can be traversed or transformed by downstream tools, interpreters, or code generators.

## Example Output

Given the input:

```
context my.agent
--begin
Hello world
--end
```

The parser produces an AST similar to:

```python
[
    ContextNode(
        name="my.agent",
        body=NaturalBlockNode([
            TextNode("Hello world")
        ])
    )
]
```

## Error Handling

If the input is invalid, the parser raises a `ParserError` with details about the location and nature of the error.

## File Locations

- **Parser implementation**: `src/lang/aliparser/aliparser/parser.py`
- **Grammar file**: `src/lang/grammar/grammar.peg`
- **Tests**: `src/lang/aliparser/aliparser/test_parser.py`

## Further Reading

- [Lark documentation](https://lark-parser.readthedocs.io/)
- [PEG grammars](https://en.wikipedia.org/wiki/Parsing_expression_grammar)
