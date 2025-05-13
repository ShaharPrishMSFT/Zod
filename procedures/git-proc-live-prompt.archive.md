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
