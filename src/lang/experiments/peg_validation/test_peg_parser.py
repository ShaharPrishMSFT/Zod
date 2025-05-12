from pathlib import Path
from lark import Lark, Tree, UnexpectedInput, UnexpectedToken
from typing import Dict, List, NamedTuple, Optional, Tuple
import sys
import argparse

class ParseResult(NamedTuple):
    success: bool
    error_details: str = None
    tree: Tree = None

def load_grammar() -> str:
    grammar_path = Path(__file__).parent.parent.parent / "grammar" / "grammar.peg"
    with open(grammar_path, "r") as f:
        return f.read()

def find_example_files() -> List[Path]:
    examples_dir = Path(__file__).parent.parent.parent / "examples"
    return sorted(list(examples_dir.glob("*.al")))

def create_parser() -> Lark:
    grammar = load_grammar()
    return Lark(grammar, start="start", parser="earley")

def format_error_details(e: UnexpectedToken, content: str, file_name: str) -> str:
    return (
        f"File: {file_name}\n"
        f"Error at line {e.line}, column {e.column}\n"
        f"Unexpected input: {e.token if hasattr(e, 'token') else 'unknown'}\n"
        f"\nContext:\n{e.get_context(content)}\n"
        f"{'-' * 50}"
    )

def parse_file(parser: Lark, file_path: Path) -> ParseResult:
    try:
        with open(file_path, "r") as f:
            content = f.read()
        tree = parser.parse(content)
        return ParseResult(success=True, tree=tree)
    except UnexpectedToken as e:
        return ParseResult(
            success=False,
            error_details=format_error_details(e, content, file_path.name)
        )
    except UnexpectedInput as e:
        return ParseResult(
            success=False,
            error_details=format_error_details(e, content, file_path.name)
        )
    except Exception as e:
        return ParseResult(
            success=False,
            error_details=f"File: {file_path.name}\nUnexpected error: {str(e)}\n{'-' * 50}"
        )

def format_summary(results: Dict[Path, ParseResult]) -> List[str]:
    summary = []
    for file_path, result in sorted(results.items()):
        filename = file_path.name
        status = "✅" if result.success else "❌"
        summary.append(f"{status} {filename}")
    return summary

def test_examples(example_num: Optional[int] = None) -> Tuple[bool, List[str]]:
    print("\nTesting AgentLingua Examples")
    print("=" * 25)
    
    example_files = find_example_files()
    if not example_files:
        return False, ["❌ No .al files found in examples directory"]
    
    # Filter for specific example if requested
    if example_num is not None:
        example_files = [f for f in example_files if f.name.startswith(f"{example_num:02d}_")]
        if not example_files:
            return False, [f"❌ No example file found for number {example_num}"]
    
    parser = create_parser()
    results: Dict[Path, ParseResult] = {}
    
    # Process each file
    for file_path in example_files:
        print(f"\nTesting {file_path.name}...", end=" ", flush=True)
        result = parse_file(parser, file_path)
        if result.success:
            print("✅")
            print("Parse tree:")
            print(result.tree.pretty())
        else:
            print("❌")
        results[file_path] = result
    
    # Print summary
    successful = sum(1 for r in results.values() if r.success)
    total = len(results)
    
    print("\nSummary")
    print("-" * 7)
    print(f"Total files tested: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    
    # Print failure details if any
    if total - successful > 0:
        print("\nFailures")
        print("-" * 8)
        for file_path, result in results.items():
            if not result.success:
                print(f"\n{result.error_details}")

    # Generate detailed summary
    summary = format_summary(results)
    print("\nDetailed Results")
    print("-" * 15)
    for line in summary:
        print(line)

    return successful == total, summary

def main():
    parser = argparse.ArgumentParser(description="Test AgentLingua example files")
    parser.add_argument("example", nargs="?", type=int, 
                       help="Optional example number to test (e.g., 0, 1, 2)")
    args = parser.parse_args()
    
    success, _ = test_examples(args.example)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
