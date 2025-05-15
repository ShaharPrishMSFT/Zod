# Archived Steps from ali-parser

## Step 1: Bootstrap environment & prerequisites (DONE 2025-05-13)

* Install toolchain(s): Python (recent), pip.
* Create git repo, enable pre-commit hooks.
* Add baseline `.editorconfig`, `.gitignore`, license.

## Step 2: Draft minimal spec & directory layout (DONE 2025-05-13)

* Write BNF-style grammar (or interface spec) in `/spec/grammar.bnf`.
* Sketch folder tree (`src/`, `tests/`, `scripts/`).
* Record any open design questions.

## Step 4: Implement Core Lexical Elements (DONE 2025-05-13)

* Create base Parser class fundamentals:
  - Token stream initialization
  - Basic error recording
  - Position tracking (line/column)
* Implement comment handling:
  - COMMENT token for "# ..." style comments
  - COMMENT_IN_BLOCKS for multi-line comments
  - Comment preservation in AST
* Add newline management:
  - _NL token recognition
  - Handling of \r\n and \n
  - Proper line counting
* Create initial test infrastructure:
  - Test helpers and fixtures
  - Comment parsing tests
  - Newline handling tests
