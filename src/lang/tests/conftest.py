from pathlib import Path
from typing import List, Dict
import pytest
from lark import Lark

@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent

@pytest.fixture(scope="session")
def grammar_path(project_root: Path) -> Path:
    """Return the path to the grammar file."""
    return project_root / "grammar" / "grammar.peg"

@pytest.fixture(scope="session")
def examples_dir(project_root: Path) -> Path:
    """Return the path to the examples directory."""
    return project_root / "examples"

@pytest.fixture(scope="session")
def grammar_content(grammar_path: Path) -> str:
    """Load and return the grammar content."""
    with open(grammar_path, "r") as f:
        return f.read()

@pytest.fixture(scope="session")
def example_files(examples_dir: Path) -> List[Path]:
    """Return a list of all example files."""
    return sorted(list(examples_dir.glob("*.al")))

@pytest.fixture(scope="session")
def example_contents(example_files: List[Path]) -> Dict[str, str]:
    """Load all example files and return their contents in a dictionary."""
    contents = {}
    for file_path in example_files:
        with open(file_path, "r") as f:
            contents[file_path.name] = f.read()
    return contents

@pytest.fixture(scope="session")
def parser(grammar_content: str) -> Lark:
    """Create and return a Lark parser for the grammar."""
    return Lark(grammar_content, start="start", parser="earley")
