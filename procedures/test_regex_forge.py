from regex_forge import RegexForge

def test_regex_patterns():
    """Test RegexForge with various pattern scenarios."""
    forge = RegexForge()
    
    test_cases = [
        {
            "description": """COPY THIS PATTERN:
^[a-zA-Z][\\w.-]*@[a-zA-Z0-9-]+(\\.[a-zA-Z0-9-]+)*\\.(com|net|org|co\\.uk)$

This pattern matches email addresses.""",
            "test_data": [
                "user@example.com",
                "first.last@domain.co.uk",
                "user_123@company.net",
                "test.email@sub.domain.org",
                "invalid.email@",
                "@invalid.com",
                "no-at-sign.com"
            ]
        },
        {
            "description": """COPY THIS PATTERN:
^(19|20)\\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\\d|3[01])$

This pattern matches dates in YYYY-MM-DD format.""",
            "test_data": [
                "2024-01-01",
                "2023-12-31",
                "2025-02-28",
                "2024-13-01",
                "2024-01-32",
                "24-01-01"
            ]
        },
        {
            "description": """COPY THIS PATTERN:
^def\\s+[a-zA-Z_]\\w*\\s*\\((?:[^()]*|\\([^()]*\\))\\)\\s*(?:->\\s*[^:]+)?\\s*:$

This pattern matches Python function definitions.""",
            "test_data": [
                "def my_function():",
                "def calculate(x: int, y: float) -> int:",
                "def process_data(data: List[str]) -> None:",
                "def complex_func(a: int, b: Optional[str] = None) -> List[int]:",
                "my_function()",
                "class MyClass:",
                "def invalid_syntax("
            ]
        }
    ]
    
    print("Testing RegexForge Patterns")
    print("==========================\n")
    
    for i, case in enumerate(test_cases, 1):
        print(f"Test Case {i}: {case['description']}")
        print("-" * 50)
        
        pattern, results = forge.generate_pattern(case['description'], case['test_data'])
        
        print(f"\nGenerated Pattern: {pattern}\n")
        print("Test Results:")
        for test, passed in results.items():
            print(f"✓ {test}" if passed else f"✗ {test}")
        print("\n")

if __name__ == "__main__":
    test_regex_patterns()
