# Self-Evolving Agentic Prompt — git\_procedure

---

## Progress Tracker

* 1. Survey existing repo layout & configs ... [[STEP-1 STATUS: DONE (2025-05-13)]]
* 2. Build Git sandbox utility for isolated testing ... [[STEP-2 STATUS: DONE (2025-05-13)]]
* 3. Implement approval flows and English→CLI mapping (status only) ... [[STEP-3 STATUS: DONE (2025-05-13)]]
* 4. Write tests using sandbox util (approve / decline) ... \[\[STEP-4 STATUS: PENDING]]

**When a step is finished**

1. Replace its `PENDING` with `DONE (yyyy‑mm‑dd)`.
2. **Cut the full step body** from *Current Step Bodies* and paste it verbatim into `prompt.archive.md`, preserving the original numbering.
3. Add a one‑line summary of the step to *COMPLETED‑STEP SUMMARIES* (above).
4. Keep the *Technical Index* capped at 10 items by dropping the least valuable entry.
5. **All commits must include a message starting with `Step X complete:` and a contextual description of what changed.**

---

## How the Agent Evolves

1. Read this prompt top‑to‑bottom.
2. Execute the next `PENDING` step; commit work in review‑sized diffs.
3. Update this file as described in **When a step is finished**.
4. On restart, resume at the first `PENDING` step.
5. Iterate until all steps are `DONE`.

---

### COMPLETED-STEP SUMMARIES

1. Surveyed repo structure, key modules, tests, tooling, and quirks. (2025-05-13)
2. Built Git sandbox utility for isolated testing and ensured .gitignore coverage. (2025-05-13)
3. Implemented LLM-driven English→CLI mapping and sandboxed execution, removing approval prompt. (2025-05-13)

### Technical Index (max 10 items)

2. plain‑English → git CLI mapping
3. pytest with tmp\_path fixtures
4. Git sandbox utility under `tests/_util/`
5. prompt‑before‑execution UX pattern
6. approval negative‑path handling
7. existing repo layout analysis
8. isolated test repo with sample code
9. agentic iteration model
10. stub‑first coding approach

---

### Important Paths / Files

* Root folder        -> ./
* Main executable    -> ./procedures
* Test suite         -> ./procedures/tests/
* Archive file       -> ./procedures/git-proc-live-prompt.archive.md

---

### Current Step Bodies

#### 4. Write tests using sandbox util (approve / decline)

* Positive: user approves, `git status` returns expected string.
* Negative: user declines, command is **not** executed (assert no changes to repo).
* All tests live under `tests/`, use `GitSandbox` fixture.

---

```mermaid
flowchart TD
    A[Start / Restart] --> B{Next pending step?}
    B -- no --> Z[All steps DONE]
    B -- yes --> C[Execute step N]
    C --> D[Commit & PR (review‑sized)]
    D --> E[Update prompt: status, summary, tech index]
    E --> B
```
