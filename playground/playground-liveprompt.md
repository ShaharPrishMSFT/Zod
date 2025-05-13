# Self-Evolving Agentic Prompt — ali-parser

<!--- COMPLETED-STEP SUMMARIES (append most salient take-aways, pitfalls, key decisions) --->

<!-- Example: 1 Installed Rust 1.78 + cargo-binutils; remember to pass `--target x86_64-pc-windows-msvc` when cross-compiling. -->

<!--- (Old step bodies are copied verbatim to `prompt.archive.md` by the agent) --->

---

## Progress Tracker

* 1. Bootstrap environment & prerequisites ... \[\[STEP-1 STATUS: PENDING]]
* 2. Draft minimal spec & directory layout ... \[\[STEP-2 STATUS: PENDING]]
* 3. Implement core skeleton (happy-path only) ... \[\[STEP-3 STATUS: PENDING]]
* 4. Wire tests + CI; prune TODOs ... \[\[STEP-4 STATUS: PENDING]]

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

#### 1. Bootstrap environment & prerequisites

* Install toolchain(s): Python (recent), pip.
* Create git repo, enable pre-commit hooks.
* Add baseline `.editorconfig`, `.gitignore`, license.

#### 2. Draft minimal spec & directory layout

* Write BNF-style grammar (or interface spec) in `/spec/grammar.bnf`.
* Sketch folder tree (`src/`, `tests/`, `scripts/`).
* Record any open design questions.

#### 3. Implement core skeleton (happy-path only)

* Generate project scaffolding manually.
* Implement the thinnest viable path from input -> parse -> return syntax tree.
* Stub unimplemented parts with `TODO:`.

#### 4. Wire tests + CI; prune TODOs

* Add unit tests using pytest.
* Configure local CI or script runner.
* Replace obvious `TODO:`s; log remaining ones in `issues.md`.

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
