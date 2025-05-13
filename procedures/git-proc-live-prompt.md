# Self-Evolving Agentic Prompt — git\_procedure

---

## Progress Tracker

* 1. Survey existing repo layout & configs ... \[\[STEP-1 STATUS: PENDING]]
* 2. Build Git sandbox utility for isolated testing ... \[\[STEP-2 STATUS: PENDING]]
* 3. Implement approval flows and English→CLI mapping (status only) ... \[\[STEP-3 STATUS: PENDING]]
* 4. Write tests using sandbox util (approve / decline) ... \[\[STEP-4 STATUS: PENDING]]

**When a step is finished**

1. Replace its `PENDING` with `DONE (yyyy‑mm‑dd)`.
2. **Cut the full step body** from *Current Step Bodies* and paste it verbatim into `prompt.archive.md`, preserving the original numbering.
3. Add a one‑line summary of the step to *COMPLETED‑STEP SUMMARIES* (above).
4. Keep the *Technical Index* capped at 10 items by dropping the least valuable entry.

---

## How the Agent Evolves

1. Read this prompt top‑to‑bottom.
2. Execute the next `PENDING` step; commit work in review‑sized diffs.
3. Update this file as described in **When a step is finished**.
4. On restart, resume at the first `PENDING` step.
5. Iterate until all steps are `DONE`.

---

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

#### 1. Survey existing repo layout & configs

* Enumerate folders, key modules, and existing tests.
* Note conventional locations (e.g., `src/`, `tests/`, `procedures/` if present).
* Identify any tooling already configured (pre‑commit, CI, etc.).
* Record pitfalls or quirks (e.g., unusual virtual‑env setup).

#### 2. Build Git sandbox utility for isolated testing

* Create `tests/_util/git_sandbox.py` with helper class `GitSandbox`.

  * `setup()` – creates a fresh sub‑folder (git‑ignored) and runs `git init`.
  * `add_sample_code()` – writes dummy Python files to mimic real work.
  * `run(cmd, approve=True/False)` – invokes `git_procedure` with simulated approval.
* Ensure sandbox root is covered by `.gitignore`.

#### 3. Implement approval flows and English→CLI mapping (status only)

* Extend `src/git_procedure.py`:

  * Parse description like "Show me the status" into `git status`.
  * Prompt user; on **yes** run command, on **no** exit with message.
  * Stream output live.
* Integrate with `GitSandbox` to operate inside sandbox repo.

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
