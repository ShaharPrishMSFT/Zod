"""
Test suite for the agentic git procedure tool.

By default, these tests use the real agentic utility (git_procedure.py) to map English instructions to git commands via LLM.

To run tests with a deterministic mock mapping (for speed and isolation), set the environment variable:
    USE_LLM_MOCK=1 pytest procedures/test_git_procedure.py

When USE_LLM_MOCK=1 is set, the INSTRUCTION_TO_COMMAND mapping is used instead of the LLM/tool pipeline.
"""

import pytest
import os
import sys
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/client/python")))
from FormalAiSdk.tests._util.git_sandbox import GitSandbox

# Mapping from plain-English instruction to expected git command
INSTRUCTION_TO_COMMAND = {
    "Create a new branch called 'feature-x'": "git checkout -b feature-x",
    "Switch to the 'main' branch": "git checkout main",
    "Stage the file 'foo.txt'": "git add foo.txt",
    "Commit staged changes with message 'Initial commit'": "git commit -m 'Initial commit'",
    "Show the last 3 commits": "git log -3",
    "Create and switch to a branch named 'bugfix'": "git checkout -b bugfix",
    "Merge branch 'feature-x' into 'main'": "git checkout main && git merge feature-x",
    "Revert the last commit": "git revert HEAD",
    "Delete the branch 'feature-x'": "git branch -d feature-x",
    "Show the current status": "git status",
}

@pytest.fixture
def sandbox(tmp_path):
    setup_start = time.time()
    sb = GitSandbox(str(tmp_path))
    sb.setup()
    setup_time = time.time() - setup_start
    print(f"[SANDBOX SETUP TIMING] setup took {setup_time:.3f} seconds")
    sb.add_sample_code()
    return sb

def print_llm_mapping(instruction, command, git_output=None):
    print("\n" + "="*40)
    print("LLM Mapping")
    print("-" * 40)
    print(f"Instruction sent to LLM:\n  {instruction}")
    print(f"Git command received from LLM:\n  {command}")
    if git_output is not None:
        print("-" * 40)
        print("Git command output:")
        print(git_output)
    print("="*40 + "\n")

def get_stdout(proc):
    """
    Helper to extract stdout as a string from a CompletedProcess or return as-is if already a string.
    """
    if hasattr(proc, "stdout"):
        out = proc.stdout
        if isinstance(out, bytes):
            return out.decode()
        return str(out)
    return str(proc)

import subprocess

def run_tool_and_command(sandbox, instruction, print_output=False):
    """
    Simulate the agentic tool: by default, call the real agentic utility (git_procedure.py) to map instruction to command.
    If USE_LLM_MOCK=1 is set in the environment, use the INSTRUCTION_TO_COMMAND mapping for deterministic testing.
    """
    use_mock = os.environ.get("USE_LLM_MOCK") == "1"
    output = ""
    print(f"DEBUG: use_mock = {use_mock}")
    if use_mock:
        if instruction not in INSTRUCTION_TO_COMMAND:
            print(f"MOCK MODE ERROR: Instruction not found in mapping: {instruction}")
            print(f"Available keys: {list(INSTRUCTION_TO_COMMAND.keys())}")
            # Print a fuzzy match suggestion
            import difflib
            close = difflib.get_close_matches(instruction, INSTRUCTION_TO_COMMAND.keys())
            if close:
                print(f"Did you mean: {close[0]}")
            raise KeyError(f"Instruction not found in INSTRUCTION_TO_COMMAND: {instruction}")
        command = INSTRUCTION_TO_COMMAND[instruction]
        print(f"MOCK MODE: Using command '{command}' for instruction '{instruction}'")
        print(f"DEBUG: command to execute = {command!r}")
        # Actually execute the mapped command(s) in the sandbox
        output = ""
        for cmd in command.split("&&"):
            cmd = cmd.strip()
            proc = sandbox.run_git_command(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            if print_output and proc is not None:
                out = ""
                if hasattr(proc, "stdout") and proc.stdout:
                    out += proc.stdout.decode() if isinstance(proc.stdout, bytes) else str(proc.stdout)
                if hasattr(proc, "stderr") and proc.stderr:
                    out += proc.stderr.decode() if isinstance(proc.stderr, bytes) else str(proc.stderr)
                output += out
    else:
        # Call the real agentic utility as a subprocess
        proc = subprocess.run(
            [
                sys.executable,
                os.path.join(os.path.dirname(__file__), "git_procedure.py"),
                "--capture-output",
                "--repo", sandbox.repo_dir,
                instruction
            ],
            capture_output=True,
            text=True,
            check=True
        )
        command = proc.stdout.strip()
        # In agentic mode, the subprocess call above already runs the full command via git_procedure.py
        if print_output and command:
            output += command
    if print_output:
        print_llm_mapping(instruction, command, output)
    else:
        print_llm_mapping(instruction, command)
    return command, output

print(f"[PYTEST ENV] USE_LLM_MOCK at import: {os.environ.get('USE_LLM_MOCK')}")

def test_create_new_branch(sandbox):
    import time, os
    print(f"[PYTEST ENV] USE_LLM_MOCK at test start: {os.environ.get('USE_LLM_MOCK')}")
    test_start = time.time()
    print(f"[TEST TIMING] test_create_new_branch started")
    print(f"DEBUG: sandbox.repo_dir = {sandbox.repo_dir}")
    print("DEBUG: repo directory contents before command:")
    print(os.listdir(sandbox.repo_dir))
    instruction = "Create a new branch called 'feature-x'"
    run_tool_and_command(sandbox, instruction)
    print("DEBUG: repo directory contents after command:")
    print(os.listdir(sandbox.repo_dir))
    use_mock = os.environ.get("USE_LLM_MOCK") == "1"
    if use_mock:
        # Run git commands in the sandbox repo with timing for assertions
        branches = sandbox.run_git_command(
            ["git", "branch"],
            capture_output=True,
            text=True,
            check=False
        ).stdout
        print(f"DEBUG: branches output: {branches}")
        assert "feature-x" in branches
        head = sandbox.run_git_command(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=False
        ).stdout.strip()
        print(f"DEBUG: HEAD output: {head}")
        assert head == "feature-x"
    else:
        print("Agentic mode: skipping direct git assertions in test_create_new_branch.")
    print(f"[TEST TIMING] test_create_new_branch took {time.time() - test_start:.3f} seconds")

def test_switch_to_main_branch(sandbox):
    import time, os
    print(f"[PYTEST ENV] USE_LLM_MOCK at test start: {os.environ.get('USE_LLM_MOCK')}")
    test_start = time.time()
    print(f"[TEST TIMING] test_switch_to_main_branch started")
    # First create and switch to another branch
    sandbox.run_git_command("git checkout -b temp", check=True)
    instruction = "Switch to the 'main' branch"
    run_tool_and_command(sandbox, instruction)
    head = sandbox.run_git_command("git rev-parse --abbrev-ref HEAD", capture_output=True, text=True, check=True).stdout.strip()
    print(f"DEBUG: HEAD output: {head}")
    assert head == "main"
    print(f"[TEST TIMING] test_switch_to_main_branch took {time.time() - test_start:.3f} seconds")

def test_stage_file(sandbox):
    # Modify foo.txt
    foo_path = os.path.join(sandbox.repo_dir, "foo.txt")
    with open(foo_path, "a") as f:
        f.write("new line\n")
    instruction = "Stage the file 'foo.txt'"
    run_tool_and_command(sandbox, instruction)
    status = sandbox.run_git_command("git status", capture_output=True, text=True, check=True).stdout
    assert "new file:   foo.txt" in status or "modified:   foo.txt" in status

def test_commit_staged_changes(sandbox):
    # Modify and stage foo.txt
    foo_path = os.path.join(sandbox.repo_dir, "foo.txt")
    with open(foo_path, "a") as f:
        f.write("commit me\n")
    sandbox.run_git_command("git add foo.txt", check=True)
    instruction = "Commit staged changes with message 'Initial commit'"
    run_tool_and_command(sandbox, instruction)
    log = sandbox.run_git_command("git log -1 --pretty=%B", capture_output=True, text=True, check=True).stdout
    assert "Initial commit" in log

def test_show_last_3_commits(sandbox):
    # Make 3 commits
    for i in range(3):
        fname = os.path.join(sandbox.repo_dir, f"file{i}.txt")
        with open(fname, "w") as f:
            f.write(f"content {i}\n")
        sandbox.run_git_command(f"git add file{i}.txt", check=True)
        sandbox.run_git_command(f"git commit -m 'commit {i}'", check=True)
    instruction = "Show the last 3 commits"
    output = run_tool_and_command(sandbox, instruction)
    log = sandbox.run_git_command("git log -3 --pretty=%B", capture_output=True, text=True, check=True).stdout
    assert "commit 2" in log and "commit 1" in log and "commit 0" in log

def test_create_and_switch_to_bugfix_branch(sandbox):
    instruction = "Create and switch to a branch named 'bugfix'"
    run_tool_and_command(sandbox, instruction)
    branches = sandbox.run_git_command("git branch", capture_output=True, text=True, check=True).stdout
    assert "bugfix" in branches
    head = sandbox.run_git_command("git rev-parse --abbrev-ref HEAD", capture_output=True, text=True, check=True).stdout.strip()
    assert head == "bugfix"

def test_merge_feature_x_into_main(sandbox):
    # Create feature-x branch and make a commit
    sandbox.run_git_command("git checkout -b feature-x", check=True)
    fname = os.path.join(sandbox.repo_dir, "feature.txt")
    with open(fname, "w") as f:
        f.write("feature branch\n")
    sandbox.run_git_command("git add feature.txt", check=True)
    sandbox.run_git_command("git commit -m 'feature commit'", check=True)
    # Switch back to main
    sandbox.run_git_command("git checkout main", check=True)
    instruction = "Merge branch 'feature-x' into 'main'"
    run_tool_and_command(sandbox, instruction)
    log = sandbox.run_git_command("git log --oneline", capture_output=True, text=True, check=True).stdout
    assert "feature commit" in log

def test_revert_last_commit(sandbox):
    # Make a commit to revert
    fname = os.path.join(sandbox.repo_dir, "revertme.txt")
    with open(fname, "w") as f:
        f.write("to be reverted\n")
    sandbox.run_git_command("git add revertme.txt", check=True)
    sandbox.run_git_command("git commit -m 'to revert'", check=True)
    instruction = "Revert the last commit"
    run_tool_and_command(sandbox, instruction)
    log = sandbox.run_git_command("git log -1 --pretty=%B", capture_output=True, text=True, check=True).stdout
    assert "Revert" in log or "revert" in log

def test_delete_feature_x_branch(sandbox):
    # Create feature-x branch, switch to main
    sandbox.run_git_command("git checkout -b feature-x", check=True)
    sandbox.run_git_command("git checkout main", check=True)
    instruction = "Delete the branch 'feature-x'"
    run_tool_and_command(sandbox, instruction)
    branches = sandbox.run_git_command("git branch", capture_output=True, text=True, check=True).stdout
    assert "feature-x" not in branches

def test_show_current_status(sandbox):
    instruction = "Show the current status"
    command, output = run_tool_and_command(sandbox, instruction, print_output=True)
    # output should contain the result of the git command
    assert "On branch" in output

def test_mock_mode_fails():
    """
    This test will always fail if USE_LLM_MOCK=1 is set.
    This is intentional: it signals in CI that the tests are running in mock mode and not exercising the real agent/tool pipeline.
    If you see this failure, it does NOT mean the code is broken—just that the tests are not running against the real LLM/tool.
    """
    if os.environ.get("USE_LLM_MOCK") == "1":
        pytest.fail(
            "USE_LLM_MOCK=1 is set: Tests are running in mock mode and NOT exercising the real agent/tool pipeline. "
            "This failure is intentional for CI. Unset USE_LLM_MOCK to run real integration tests."
        )
