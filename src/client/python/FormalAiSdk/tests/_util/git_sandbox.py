import os
import shutil
import subprocess
from pathlib import Path

class GitSandbox:
    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir or Path(__file__).parent / "sandbox")
        self.repo_dir = self.root_dir / "repo"

    def setup(self):
        # Remove any existing sandbox
        if self.root_dir.exists():
            shutil.rmtree(self.root_dir)
        self.repo_dir.mkdir(parents=True, exist_ok=True)
        # Initialize git repo
        subprocess.run(["git", "init"], cwd=self.repo_dir, check=True)
        return self

    def add_sample_code(self, filename="hello.py", content='print("Hello from sandbox!")\n'):
        # Write a dummy Python file
        sample_file = self.repo_dir / filename
        with open(sample_file, "w") as f:
            f.write(content)
        return self

    def commit(self, message="Initial commit"):
        # Stage all changes and commit
        subprocess.run(["git", "add", "."], cwd=self.repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", message], cwd=self.repo_dir, check=True)
        return self

    def create_branch(self, branch_name):
        subprocess.run(["git", "checkout", "-b", branch_name], cwd=self.repo_dir, check=True)
        return self

    def merge(self, branch_name):
        subprocess.run(["git", "merge", branch_name], cwd=self.repo_dir, check=True)
        return self

    def run(self, cmd, approve=True):
        """
        Simulate running the git_procedure script with approval or decline.
        This is a stub; actual implementation may require integration with CLI prompt logic.
        """
        # Example: simulate approval by passing a flag or using input redirection
        # Use the correct path for git_procedure.py in the procedures directory
        script_path = Path(__file__).parents[6] / "procedures" / "git_procedure.py"
        if not script_path.exists():
            raise FileNotFoundError(f"git_procedure.py not found at {script_path}")
        # Simulate user input: 'y' for approve, 'n' for decline
        user_input = b"y\n" if approve else b"n\n"
        proc = subprocess.run(
            ["python", str(script_path), "--repo", str(self.repo_dir), cmd],
            cwd=self.repo_dir,
            input=user_input,
            capture_output=True,
            check=False,
        )
        return proc

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
