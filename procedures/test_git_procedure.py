import pytest
import os
import sys
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
    # Set up a fresh git sandbox for each test
    sb = GitSandbox(str(tmp_path))
    sb.setup()
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

def run_tool_and_command(sandbox, instruction, print_output=False):
    """
    Simulate the agentic tool: map instruction to command, run in sandbox.
    """
    command = INSTRUCTION_TO_COMMAND[instruction]
    output = ""
    # Support multi-command (e.g., checkout + merge)
    for cmd in command.split("&&"):
        proc = sandbox.run(cmd.strip(), approve=True)
        if print_output and proc is not None:
            # proc may be CompletedProcess or similar
            out = ""
            if hasattr(proc, "stdout") and proc.stdout:
                out += proc.stdout.decode() if isinstance(proc.stdout, bytes) else str(proc.stdout)
            if hasattr(proc, "stderr") and proc.stderr:
                out += proc.stderr.decode() if isinstance(proc.stderr, bytes) else str(proc.stderr)
            output += out
    if print_output:
        print_llm_mapping(instruction, command, output)
    else:
        print_llm_mapping(instruction, command)
    return command, output

def test_create_new_branch(sandbox):
    instruction = "Create a new branch called 'feature-x'"
    run_tool_and_command(sandbox, instruction)
    branches = sandbox.run("git branch", approve=True)
    assert "feature-x" in branches
    head = sandbox.run("git rev-parse --abbrev-ref HEAD", approve=True).strip()
    assert head == "feature-x"

def test_switch_to_main_branch(sandbox):
    # First create and switch to another branch
    sandbox.run("git checkout -b temp", approve=True)
    instruction = "Switch to the 'main' branch"
    run_tool_and_command(sandbox, instruction)
    head = sandbox.run("git rev-parse --abbrev-ref HEAD", approve=True).strip()
    assert head == "main"

def test_stage_file(sandbox):
    # Modify foo.txt
    foo_path = os.path.join(sandbox.repo_dir, "foo.txt")
    with open(foo_path, "a") as f:
        f.write("new line\n")
    instruction = "Stage the file 'foo.txt'"
    run_tool_and_command(sandbox, instruction)
    status = sandbox.run("git status", approve=True)
    assert "new file:   foo.txt" in status or "modified:   foo.txt" in status

def test_commit_staged_changes(sandbox):
    # Modify and stage foo.txt
    foo_path = os.path.join(sandbox.repo_dir, "foo.txt")
    with open(foo_path, "a") as f:
        f.write("commit me\n")
    sandbox.run("git add foo.txt", approve=True)
    instruction = "Commit staged changes with message 'Initial commit'"
    run_tool_and_command(sandbox, instruction)
    log = sandbox.run("git log -1 --pretty=%B", approve=True)
    assert "Initial commit" in log

def test_show_last_3_commits(sandbox):
    # Make 3 commits
    for i in range(3):
        fname = os.path.join(sandbox.repo_dir, f"file{i}.txt")
        with open(fname, "w") as f:
            f.write(f"content {i}\n")
        sandbox.run(f"git add file{i}.txt", approve=True)
        sandbox.run(f"git commit -m 'commit {i}'", approve=True)
    instruction = "Show the last 3 commits"
    output = run_tool_and_command(sandbox, instruction)
    log = sandbox.run("git log -3 --pretty=%B", approve=True)
    assert "commit 2" in log and "commit 1" in log and "commit 0" in log

def test_create_and_switch_to_bugfix_branch(sandbox):
    instruction = "Create and switch to a branch named 'bugfix'"
    run_tool_and_command(sandbox, instruction)
    branches = sandbox.run("git branch", approve=True)
    assert "bugfix" in branches
    head = sandbox.run("git rev-parse --abbrev-ref HEAD", approve=True).strip()
    assert head == "bugfix"

def test_merge_feature_x_into_main(sandbox):
    # Create feature-x branch and make a commit
    sandbox.run("git checkout -b feature-x", approve=True)
    fname = os.path.join(sandbox.repo_dir, "feature.txt")
    with open(fname, "w") as f:
        f.write("feature branch\n")
    sandbox.run("git add feature.txt", approve=True)
    sandbox.run("git commit -m 'feature commit'", approve=True)
    # Switch back to main
    sandbox.run("git checkout main", approve=True)
    instruction = "Merge branch 'feature-x' into 'main'"
    run_tool_and_command(sandbox, instruction)
    log = sandbox.run("git log --oneline", approve=True)
    assert "feature commit" in log

def test_revert_last_commit(sandbox):
    # Make a commit to revert
    fname = os.path.join(sandbox.repo_dir, "revertme.txt")
    with open(fname, "w") as f:
        f.write("to be reverted\n")
    sandbox.run("git add revertme.txt", approve=True)
    sandbox.run("git commit -m 'to revert'", approve=True)
    instruction = "Revert the last commit"
    run_tool_and_command(sandbox, instruction)
    log = sandbox.run("git log -1 --pretty=%B", approve=True)
    assert "Revert" in log or "revert" in log

def test_delete_feature_x_branch(sandbox):
    # Create feature-x branch, switch to main
    sandbox.run("git checkout -b feature-x", approve=True)
    sandbox.run("git checkout main", approve=True)
    instruction = "Delete the branch 'feature-x'"
    run_tool_and_command(sandbox, instruction)
    branches = sandbox.run("git branch", approve=True)
    assert "feature-x" not in branches

def test_show_current_status(sandbox):
    instruction = "Show the current status"
    command, output = run_tool_and_command(sandbox, instruction, print_output=True)
    # output should contain the result of the git command
    assert "On branch" in output
