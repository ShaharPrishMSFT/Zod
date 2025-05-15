import re
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src", "client", "python"))
from FormalAiSdk.models.litellm_executor import LiteLLMExecutor
from FormalAiSdk.sdk.session import ModelSession
from typing import List, Dict, Tuple

class RegexForge:
    def __init__(self):
        """Initialize RegexForge with LiteLLM executor and session."""
        self.executor = LiteLLMExecutor("ollama", "mistral")
        self.session = ModelSession("regex_assistant", self.executor)

    def generate_pattern(self, description: str, test_data: List[str]) -> Tuple[str, Dict[str, bool]]:
        """
        Generate a regex pattern based on natural language description and test data.
        
        Args:
            description (str): Natural language description of the desired pattern
            test_data (List[str]): List of strings to test the pattern against
            
        Returns:
            Tuple[str, Dict[str, bool]]: Generated regex pattern and test results
        """
        # Add context and requirements
        self.session.add_response("system", """You are a pattern copier. Your task is simple:

        When you see something like this:
        COPY THIS PATTERN:
        ^\\d{4}-\\d{2}-\\d{2}$

        You respond with only:
        ^\\d{4}-\\d{2}-\\d{2}$

        Don't add any text, explanation, or modifications.
        Just copy the exact pattern you see.

        REMEMBER: Use the provided template and make only necessary minor adjustments.""")

        # Format the request with test data
        request = f"""Description: {description}
        Test cases:
        {'-' * 20}
        {chr(10).join(test_data)}
        {'-' * 20}
        Create a regex pattern that satisfies these requirements."""

        self.session.add_response("user", request)

        # Create fork for pattern generation
        generation_fork = self.session.Fork(
            "pattern_generator",
            "user",
            "Find the pattern marked 'COPY THIS PATTERN' in the description.\n" +
            "Copy and paste that exact pattern.\n" +
            "Nothing else - just the pattern itself."
        )
        generation_fork.Answer(self.session)

        # Extract pattern from response
        pattern = self._extract_pattern(self.session.messages[-1].content)

        # Create fork for pattern refinement
        test_results = self._test_pattern(pattern, test_data)
        if not all(test_results.values()):
            refinement_fork = self.session.Fork(
                "pattern_refiner",
                "user",
                f"""COPY THIS PATTERN:
                {pattern}"""
            )
            refinement_fork.Answer(self.session)
            pattern = self._extract_pattern(self.session.messages[-1].content)
            test_results = self._test_pattern(pattern, test_data)

        return pattern, test_results

    def _extract_pattern(self, response: str) -> str:
        """Extract the regex pattern from the model's response."""
        # Look for pattern after "COPY THIS PATTERN" marker
        if "COPY THIS PATTERN" in response:
            after_marker = response.split("COPY THIS PATTERN")[1]
            after_marker = after_marker.split("\n")[1].strip()
            # Clean up any wrapping characters
            for wrapper in ['`', 'r"', 'r\'', '"', '\'', '⚠️', '🔒', ':']:
                after_marker = after_marker.strip(wrapper).strip()
            return after_marker
        
        # Fallback to first non-empty line that looks like a pattern
        for line in response.split('\n'):
            line = line.strip()
            if not line:
                continue
            # Skip lines that are clearly instructions/headers
            if any(x in line.lower() for x in ['copy', 'pattern', 'test', 'critical', '⚠️', '🔒']):
                continue
            # Skip lines that are dividers
            if set(line).issubset({'-', '=', '*', '_'}):
                continue
            # Clean up any wrapping characters
            for wrapper in ['`', 'r"', 'r\'', '"', '\'']:
                line = line.strip(wrapper).strip()
            # If it contains regex-like characters, return it
            if any(x in line for x in ['^', '$', '*', '+', '[', ']', '(', ')', '\\']):
                return line
        
        return ""

    def _test_pattern(self, pattern: str, test_data: List[str]) -> Dict[str, bool]:
        """
        Test a regex pattern against provided test cases.
        
        Args:
            pattern (str): Regex pattern to test
            test_data (List[str]): List of strings to test against
            
        Returns:
            Dict[str, bool]: Test results for each test case
        """
        try:
            compiled_pattern = re.compile(pattern)
            return {test: bool(compiled_pattern.match(test)) for test in test_data}
        except re.error:
            return {test: False for test in test_data}

def main():
    """Example usage of RegexForge."""
    forge = RegexForge()
    
    # Example: Generate pattern for matching email addresses
    description = "Create a pattern to match email addresses"
    test_data = [
        "user@example.com",
        "first.last@domain.co.uk",
        "invalid.email@",
        "@invalid.com"
    ]
    
    pattern, results = forge.generate_pattern(description, test_data)
    
    print(f"Generated Pattern: {pattern}")
    print("\nTest Results:")
    for test, passed in results.items():
        print(f"{test}: {'✓' if passed else '✗'}")

if __name__ == "__main__":
    main()
