# Report: Grammar Failures in Simple Context Block Tests

This report documents the failures of two grammar-related tests in `src/lang/aliparser/aliparser/test_parser.py` as of 2025-05-14. Both failures are due to the parser's handling of whitespace in natural language blocks.

---

## 1. Test: `test_parse_simple_context_block`

- **Script:** `src/lang/aliparser/aliparser/test_parser.py`
- **Description:**  
  Attempts to parse a simple AgentLingua context block containing a line like `Hello world` inside a natural block.
- **Failure:**  
  ```
  src.lang.aliparser.aliparser.parser.ParserError: Unexpected input (line 4, column 12)
  Context:
  Hello world
             ^
  ```
- **Explanation:**  
  The parser does not accept the space in "Hello world" as valid input in a natural block. This is due to the grammar's handling of whitespace, which currently does not allow spaces in this context.

---

## 2. Test: `test_parse_ast_context_block`

- **Script:** `src/lang/aliparser/aliparser/test_parser.py`
- **Description:**  
  Attempts to parse a simple AgentLingua context block containing a line like `Hello world` inside a natural block, and then build the AST.
- **Failure:**  
  ```
  src.lang.aliparser.aliparser.parser.ParserError: Unexpected input (line 4, column 12)
  Context:
  Hello world
             ^
  ```
- **Explanation:**  
  The parser fails at the same location and for the same reason: it does not accept the space in a natural block.

---

## Root Cause

The grammar currently does not allow spaces in natural blocks, causing the parser to fail on lines containing spaces (e.g., "Hello world"). This is a whitespace handling issue in the grammar definition.

---

## Action Required

The grammar file must be updated to allow spaces in natural blocks for these tests to pass.
