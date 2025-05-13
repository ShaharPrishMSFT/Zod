# Self-Evolving Agentic Prompt — ali-parser

<!--- COMPLETED-STEP SUMMARIES (append most salient take-aways, pitfalls, key decisions) --->

- Minimal local implementation can be achieved as a static HTML/JS app using CodeMirror (preferred for MVP) and a JS PEG parser, with all dependencies loaded via CDN.
- Main features: code editor with syntax highlighting, real-time/on-demand parsing, inline error feedback, file open/save via browser, output panel for AST/errors, collapsible log/debug area.
- No build step or backend required; use browser APIs for file I/O.
- Key risks: parser integration (PEG grammar compatibility with JS parser), custom syntax highlighting, mapping parser errors to editor positions.
- Focus on practicality: minimal styling, rapid prototyping, and clear separation of concerns.

- CodeMirror integrated via CDN, no build step.
- Custom AgentLingua mode provides basic syntax highlighting for `.al` files.
- Editor supports multi-line editing, indentation, undo/redo, and find/replace.
- Minimal .al example loads by default.
- Foundation set for future features (autocomplete, real-time parsing, etc.).

- Editor must support real-time parsing and inline error feedback for `.al` files.
- Split view: code editor (left), parse output (right), collapsible log/debug area (bottom).
- File I/O is seamless: Open/Save/Copy controls use browser APIs for loading and exporting `.al` files, with user feedback and no backend or build step required.
- Inline error markers and hover tooltips are essential for usability.
- Responsive layout: horizontal split on large screens, tabbed panels on small screens.

---

## Progress Tracker

* 1. Reason about minimal local implementation ... [[STEP-1 STATUS: DONE (2025-05-13)]]
* 2. Integrate syntax-highlighting editor ... [[STEP-2 STATUS: DONE (2025-05-13)]]
* 3. Implement file load/save functionality ... [[STEP-3 STATUS: DONE (2025-05-13)]]
* 4. Plan for building tests to test the UI to see that it's working ... [[STEP-4 STATUS: PENDING]]
* 5. Implement the tests to the current functionality ... [[STEP-5 STATUS: PENDING]]
* 6. Integrate real-time parser and validation ... [[STEP-6 STATUS: PENDING]]
* 7. Build output and feedback panel ... [[STEP-7 STATUS: PENDING]]
* 8. Add logging and debug area ... [[STEP-8 STATUS: PENDING]]

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

1. [Playground Specification](playground/playground-spec.md)
2. [Main README](personalities/formalai.playground/readme.md)
3. [Grammar Definition](src/lang/grammar/grammar.peg)
4. [Minimal .al Example](src/lang/examples/00_super_simple.al)
5. AgentLingua syntax highlighting
6. Real-time parser integration
7. File I/O (Open/Save)
8. Inline error markers & tooltips
9. AST/output panel
10. Collapsible log/debug area

---

### Important Paths / Files

* Root folder        -> /src/lang/
* Main executable    -> ail.exe
* Tests              -> tests/
* CI pipeline        -> All local

---

### Current Step Bodies

#### 4. Plan for building tests to test the UI to see that it's working

* Identify which UI features require testing (Open, Save, Copy, editor initialization, status messages).
* Decide on the testing approach: automated browser tests (e.g., Playwright, Cypress) or manual test scripts/checklists.
* Specify test cases for each feature (e.g., file loads into editor, save triggers download, copy updates clipboard, status messages appear).
* Determine how to verify results (file content, clipboard content, UI updates).

#### 5. Implement the tests to the current functionality

* Set up the chosen test framework or manual test checklist.
* Write and organize tests for each UI feature as planned in step 4.
* Run the tests and document results.
* Adjust implementation or tests as needed based on failures or gaps.

#### 6. Integrate real-time parser and validation

* Connect the AgentLingua parser to the editor.
* Enable real-time or on-demand parsing (e.g., on every change or via a "Validate" button).
* Display inline error markers and feedback as the user types.

#### 7. Build output and feedback panel

* Create a panel adjacent to the editor to display parse results (AST, confirmation, or error messages).
* Show success/failure status after each parse.
* For errors, display line/column info and highlight issues in the editor.

#### 8. Add logging and debug area

* Implement a collapsible log or console panel (typically at the bottom).
* Display detailed parser messages, debug output, and raw parse results (e.g., AST or tokens).
* Ensure the log area is scrollable and can be hidden or shown as needed.

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
