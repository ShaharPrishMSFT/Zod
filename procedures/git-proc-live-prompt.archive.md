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

#### 4. Plan and document 10 end-to-end git procedure tests

Plan a suite of 10 end-to-end tests that use the agentic tool to:
- Generate a git command from a plain-English instruction
- Run the command on the playground git repository (using the GitSandbox utility)
- Observe and verify the effects on the git repository to ensure the intended outcome

Each test plan includes:
- **Instruction**: The plain-English instruction given to the tool
- **Expected Command**: The git command the tool should generate
- **Initial State**: The starting state of the repo
- **Action**: What is run/executed
- **Expected State**: The desired state after execution
- **Assertion**: How to verify the outcome

**Test Plans:**

1. **Create a new branch**
   - Instruction: "Create a new branch called 'feature-x'"
   - Expected Command: `git checkout -b feature-x`
   - Initial State: On main branch, clean working directory
   - Action: Run tool, approve command, execute in sandbox
   - Expected State: HEAD is at 'feature-x', branch exists
   - Assertion: `git branch` output includes 'feature-x', HEAD is correct

2. **Switch branches**
   - Instruction: "Switch to the 'main' branch"
   - Expected Command: `git checkout main`
   - Initial State: On another branch, clean working directory
   - Action: Run tool, approve command, execute in sandbox
   - Expected State: HEAD is at 'main'
   - Assertion: `git branch` shows HEAD at 'main'

3. **Stage a file**
   - Instruction: "Stage the file 'foo.txt'"
   - Expected Command: `git add foo.txt`
   - Initial State: Unstaged changes in 'foo.txt'
   - Action: Run tool, approve command, execute in sandbox
   - Expected State: 'foo.txt' is staged
   - Assertion: `git status` shows 'foo.txt' in staged area

4. **Commit staged changes**
   - Instruction: "Commit staged changes with message 'Initial commit'"
   - Expected Command: `git commit -m 'Initial commit'`
   - Initial State: Staged changes present
   - Action: Run tool, approve command, execute in sandbox
   - Expected State: New commit created with correct message
   - Assertion: `git log -1` shows commit with message

5. **Show commit log**
   - Instruction: "Show the last 3 commits"
   - Expected Command: `git log -3`
   - Initial State: At least 3 commits exist
   - Action: Run tool, approve command, execute in sandbox
   - Expected State: Output lists last 3 commits
   - Assertion: Output matches `git log -3`

6. **Create and switch to a new branch**
   - Instruction: "Create and switch to a branch named 'bugfix'"
   - Expected Command: `git checkout -b bugfix`
   - Initial State: On main branch, clean working directory
   - Action: Run tool, approve command, execute in sandbox
   - Expected State: HEAD is at 'bugfix', branch exists
   - Assertion: `git branch` output includes 'bugfix', HEAD is correct

7. **Merge a branch**
   - Instruction: "Merge branch 'feature-x' into 'main'"
   - Expected Command: `git checkout main && git merge feature-x`
   - Initial State: 'feature-x' and 'main' exist, 'feature-x' ahead
   - Action: Run tool, approve command, execute in sandbox
   - Expected State: 'main' contains 'feature-x' changes
   - Assertion: `git log` and file contents reflect merge

8. **Revert a commit**
   - Instruction: "Revert the last commit"
   - Expected Command: `git revert HEAD`
   - Initial State: At least one commit exists
   - Action: Run tool, approve command, execute in sandbox
   - Expected State: New commit that undoes last commit
   - Assertion: `git log` shows revert, file state matches

9. **Delete a branch**
   - Instruction: "Delete the branch 'feature-x'"
   - Expected Command: `git branch -d feature-x`
   - Initial State: 'feature-x' exists, not checked out
   - Action: Run tool, approve command, execute in sandbox
   - Expected State: 'feature-x' branch deleted
   - Assertion: `git branch` output does not include 'feature-x'

10. **Show status**
    - Instruction: "Show the current status"
    - Expected Command: `git status`
    - Initial State: Any
    - Action: Run tool, approve command, execute in sandbox
    - Expected State: Output matches current repo state
    - Assertion: Output matches `git status`

#### 5. Write tests using sandbox util (approve / decline)

* Positive: user approves, `git status` returns expected string.
* Negative: user declines, command is **not** executed (assert no changes to repo).
* All tests live under `tests/`, use `GitSandbox` fixture.

---
