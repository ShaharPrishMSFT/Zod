import os
import shutil
import subprocess
import time
from pathlib import Path

class GitSandbox:
    """
    Pure git sandbox for test isolation and timing.
    This class must NEVER invoke the agentic procedure (git_procedure.py).
    All methods execute raw git commands directly in the sandbox repo.
    """
    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir or Path(__file__).parent / "sandbox")
        self.repo_dir = self.root_dir / "repo"

    def run_git_command(self, cmd, **kwargs):
        """
        Run a git command in the sandbox repo with timing instrumentation.
        cmd: list or string (e.g., ["git", "status"] or "git status")
        kwargs: passed to subprocess.run
        Prints timing logs to both stdout and stderr with a distinctive prefix.
        """
        import shlex, sys
        if isinstance(cmd, str):
            cmd = shlex.split(cmd)
        msg = f"[SANDBOX TIMING] Running: {' '.join(cmd)}"
        print(msg)
        print(msg, file=sys.stderr)
        start = time.time()
        proc = subprocess.run(
            cmd,
            cwd=self.repo_dir,
            **kwargs
        )
        end = time.time()
        msg = f"[SANDBOX TIMING] Command took {end - start:.3f} seconds"
        print(msg)
        print(msg, file=sys.stderr)
        return proc

    def setup(self):
        # Remove any existing sandbox
        if self.root_dir.exists():
            shutil.rmtree(self.root_dir)
        self.repo_dir.mkdir(parents=True, exist_ok=True)
        # Initialize git repo
        self.run_git_command(["git", "init"], check=True)
        # Create and switch to 'main' branch for test consistency
        self.run_git_command(["git", "checkout", "-b", "main"], check=True)
        # Add initial file and commit so the branch exists
        self.add_sample_code()
        self.commit("Initial commit")
        return self

    def add_sample_code(self, filename="hello.py", content='print("Hello from sandbox!")\n'):
        # Write a dummy Python file
        sample_file = self.repo_dir / filename
        with open(sample_file, "w") as f:
            f.write(content)
        return self

    def commit(self, message="Initial commit"):
        # Stage all changes and commit
        self.run_git_command(["git", "add", "."], check=True)
        self.run_git_command(["git", "commit", "-m", message], check=True)
        return self

    def create_branch(self, branch_name):
        self.run_git_command(["git", "checkout", "-b", branch_name], check=True)
        return self

    def merge(self, branch_name):
        self.run_git_command(["git", "merge", branch_name], check=True)
        return self

    # The run() method has been removed to enforce that the sandbox never calls the agentic procedure.

# Ensure the sandbox root is git-ignored
def ensure_gitignore():
    gitignore_path = Path(__file__).parent / ".gitignore"
    sandbox_line = "sandbox/\n"
    if gitignore_path.exists():
        with open(gitignore_path, "r") as f:
            lines = f.readlines()
        if sandbox_line not in lines:
            with open(gitignore_path, "a") as f:
                f.write(sandbox_line)
    else:
        with open(gitignore_path, "w") as f:
            f.write(sandbox_line)

ensure_gitignore()
