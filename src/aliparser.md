# Self-Evolving Agentic Prompt — ali-parser

<!--- COMPLETED-STEP SUMMARIES (append most salient take-aways, pitfalls, key decisions) --->

<!-- Example: 1 Installed Rust 1.78 + cargo-binutils; remember to pass `--target x86_64-pc-windows-msvc` when cross-compiling. -->

1. Project exists in a git worktree with Python 3.13/pip installed; minimal additional setup needed.
2. Grammar defined in PEG format, follows existing grammar.peg specification; project structure aligns with Python package standards.
3. Implemented core lexical elements: lexer with comment/newline tokens, line tracking, initial tests added.

<!--- (Old step bodies are copied verbatim to `prompt.archive.md` by the agent) --->

---

## Progress Tracker

* 1. Bootstrap environment & prerequisites ... \[\[STEP-1 STATUS: DONE (2025-05-13)]]
* 2. Draft minimal spec & directory layout ... \[\[STEP-2 STATUS: DONE (2025-05-13)]]
* 3. Implement Core Lexical Elements ... \[\[STEP-3 STATUS: DONE (2025-05-13)]]
* 4. Implement Context Parser ... \[\[STEP-4 STATUS: PENDING]]
* 5. Expand Parser with Input and Rule Support ... \[\[STEP-5 STATUS: PENDING]]
* 6. Parser Validation and Enhancement ... \[\[STEP-6 STATUS: PENDING]]

When a step is finished, replace its `PENDING` with `DONE (yyyy-mm-dd)` and copy the full step block to `prompt.archive.md`.

---

## How the Agent Evolves

1. Read this prompt top-to-bottom.
2. Execute the next `PENDING` step; edit code in review-sized chunks (complex code => smaller diffs).
3. Update this file:

   * Move finished step(s) to archive, keep only their key take-aways above.
   * Mark step status.
   * Maintain the Technical Index at exactly 10 high-value items (drop the least useful).
4. If execution restarts, resume from the first `PENDING` step.
5. Repeat until all steps are `DONE`.

---

### Technical Index (max 10 items)

1. \[\[URI\_OR\_TITLE\_1]]
2. \[\[URI\_OR\_TITLE\_2]]
3. \[\[URI\_OR\_TITLE\_3]]
4. \[\[URI\_OR\_TITLE\_4]]
5. \[\[URI\_OR\_TITLE\_5]]
6. \[\[URI\_OR\_TITLE\_6]]
7. \[\[URI\_OR\_TITLE\_7]]
8. \[\[URI\_OR\_TITLE\_8]]
9. \[\[URI\_OR\_TITLE\_9]]
10. \[\[URI\_OR\_TITLE\_10]]

---

### Important Paths / Files

* Root folder        -> /src/lang/
* Main executable    -> ail.exe
* Tests              -> tests/
* CI pipeline        -> All local

---

### Current Step Bodies

#### 3. Implement Core Lexical Elements
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

#### 4. Implement Context Parser
* Add context block parsing:
  - formal_decl_block for context declarations
  - natural_block with --begin/--end
  - natural_content with TEXT_CHAR
* Build AST node types:
  - Context node structure
  - Natural block nodes
  - Text content nodes
* Enhance error handling:
  - Block matching validation
  - Missing delimiter detection
  - Context syntax validation

#### 5. Expand Parser with Input and Rule Support
* Implement input statement parsing:
  - input_stmt node type
  - natural_inline handling for [parameters]
  - Parameter validation
* Add rule statement support:
  - when_stmt parsing
  - Condition expression handling
  - Action block parsing
  - Rule block validation
* Extend validation:
  - Input parameter syntax checking
  - Rule condition/action structure validation
* Add unit tests for input and rule parsing

#### 6. Parser Validation and Enhancement
* Add syntax validation:
  - Complete block structure validation
  - Nested block handling
  - Cross-reference checking
* Implement semantic checks:
  - Symbol table for identifiers
  - Scope tracking
  - Reference validation
* Add error recovery:
  - Synchronization points
  - Skip-to-next statement on error
  - Partial AST for incomplete input
* Enhance error messages:
  - Line/column information
  - Helpful suggestions
  - Error catalogs

---

```mermaid
flowchart TD
    A[Start / Restart] --> B{Next pending step?}
    B -- no --> Z[All steps DONE]
    B -- yes --> C[Execute step N]
    C --> D[Commit & PR (review-sized)]
    D --> E[Update prompt: status, summary, tech index]
    E --> B
```

---

## Project Snapshot (terse)

> Just the parser for a PEG schema. It exposes a parser API that builds a syntax tree from a PEG-based DSL but performs no evaluation. Used downstream by an external executor or interpreter.

---

Follow the process, keep diffs tidy, value practicality over dogma.
