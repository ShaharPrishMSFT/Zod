import pytest
from pathlib import Path
from ._util.git_sandbox import GitSandbox
import subprocess

def test_playground_experiment(tmp_path):
    """
    Playground test: Only verifies basic, local functionality.
    No advanced procedures, LLM, or agentic logic allowed.
    """
    # Document experiment objective
    objective = "Test isolated file creation and cleanup in playground."
    experiment_dir = tmp_path / "playground_experiment"
    experiment_dir.mkdir()
    test_file = experiment_dir / "test.txt"
    test_file.write_text("Hello, playground!")
    
    # Assert file was created and contains expected content
    assert test_file.exists()
    assert test_file.read_text() == "Hello, playground!"
    
    # Document result
    result = f"Created {test_file} with content: {test_file.read_text()}"
    print(result)
    
    # Cleanup is automatic with tmp_path fixture

def test_create_and_read_multiple_files(tmp_path):
    """
    Create a subdirectory and multiple files, then read their contents.
    """
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    files = []
    for i in range(3):
        f = subdir / f"file_{i}.txt"
        f.write_text(f"Content {i}")
        files.append(f)
    # Assert all files exist and contents are correct
    for i, f in enumerate(files):
        assert f.exists()
        assert f.read_text() == f"Content {i}"

def test_rename_and_delete_file(tmp_path):
    """
    Create a file, rename it, then delete it.
    """
    file1 = tmp_path / "to_rename.txt"
    file1.write_text("Rename me")
    file2 = tmp_path / "renamed.txt"
    file1.rename(file2)
    assert not file1.exists()
    assert file2.exists()
    assert file2.read_text() == "Rename me"
    # Now delete
    file2.unlink()
    assert not file2.exists()

def test_git_commit(tmp_path):
    """
    Test committing a file in a git sandbox.
    """
    sandbox = GitSandbox(root_dir=tmp_path)
    sandbox.setup().add_sample_code("foo.py", "print('foo')").commit("Add foo.py")
    # Check that foo.py exists
    foo_file = sandbox.repo_dir / "foo.py"
    assert foo_file.exists()
    # Check that the commit exists in git log
    result = subprocess.run(
        ["git", "log", "--oneline"],
        cwd=sandbox.repo_dir,
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Add foo.py" in result.stdout

def test_git_merge(tmp_path):
    """
    Test merging a feature branch into main in a git sandbox.
    """
    sandbox = GitSandbox(root_dir=tmp_path)
    sandbox.setup().add_sample_code("main.py", "print('main')").commit("main commit")
    sandbox.create_branch("feature").add_sample_code("feature.py", "print('feature')").commit("feature commit")
    # Switch back to master and merge
    subprocess.run(["git", "checkout", "master"], cwd=sandbox.repo_dir, check=True)
    sandbox.merge("feature")
    # Check that both main.py and feature.py exist
    main_file = sandbox.repo_dir / "main.py"
    feature_file = sandbox.repo_dir / "feature.py"
    assert main_file.exists()
    assert feature_file.exists()
    # Check that both commits are in git log
    result = subprocess.run(
        ["git", "log", "--oneline"],
        cwd=sandbox.repo_dir,
        capture_output=True,
        text=True,
        check=True,
    )
    assert "main commit" in result.stdout
    assert "feature commit" in result.stdout

# NOTE: Do not add tests here that use advanced procedures, LLM, or agentic/approval flows.
