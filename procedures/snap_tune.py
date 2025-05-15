import cProfile
import pstats
import io
import ast
import textwrap
from typing import Dict, Tuple, List
from FormalAiSdk.models.litellm_executor import LiteLLMExecutor
from FormalAiSdk.sdk.session import ModelSession

class SnapTune:
    def __init__(self):
        """Initialize SnapTune with LiteLLM executor and session."""
        self.executor = LiteLLMExecutor("ollama", "llama2")
        self.session = ModelSession("performance_assistant", self.executor)

    def analyze_code(self, code: str, performance_criteria: Dict = None) -> Tuple[str, Dict, str]:
        """
        Analyze code performance and suggest optimizations.
        
        Args:
            code (str): Python code to analyze
            performance_criteria (Dict): Optional criteria for optimization focus
            
        Returns:
            Tuple[str, Dict, str]: Optimized code, performance metrics, analysis report
        """
        # Validate and prepare code
        self._validate_code(code)
        prepared_code = self._prepare_code(code)
        
        # Profile the code
        profile_results = self._profile_code(prepared_code)
        
        # Analyze results and get optimization suggestions
        optimized_code, analysis_report = self._get_optimization_suggestions(
            code, profile_results, performance_criteria
        )
        
        return optimized_code, profile_results, analysis_report

    def _validate_code(self, code: str):
        """Validate that the code is syntactically correct Python."""
        try:
            ast.parse(code)
        except SyntaxError as e:
            raise ValueError(f"Invalid Python code: {str(e)}")

    def _prepare_code(self, code: str) -> str:
        """Prepare code for profiling by wrapping it in a function."""
        return f"""
def _code_to_profile():
{textwrap.indent(code, '    ')}

_code_to_profile()
"""

    def _profile_code(self, code: str) -> Dict:
        """
        Profile the code and collect performance metrics.
        
        Args:
            code (str): Prepared Python code to profile
            
        Returns:
            Dict: Performance metrics including timing and call counts
        """
        # Create a string buffer to capture profiling output
        pr = cProfile.Profile()
        s = io.StringIO()
        
        # Profile the code
        try:
            # Execute the code while profiling
            exec_globals = {}
            exec(code, exec_globals)
            pr.runctx(code, globals(), exec_globals)
            
            # Get stats
            ps = pstats.Stats(pr, stream=s)
            ps.sort_stats('cumulative')
            ps.print_stats()
            
            # Parse profiling results
            profiling_output = s.getvalue()
            return self._parse_profile_output(profiling_output)
            
        except Exception as e:
            raise RuntimeError(f"Error during code profiling: {str(e)}")

    def _parse_profile_output(self, output: str) -> Dict:
        """Parse cProfile output into structured metrics."""
        metrics = {
            'total_time': 0.0,
            'function_stats': [],
            'bottlenecks': []
        }
        
        lines = output.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('   ncalls'):
                parts = line.strip().split()
                if len(parts) >= 6:
                    try:
                        stats = {
                            'ncalls': parts[0],
                            'tottime': float(parts[1]),
                            'percall': float(parts[2]),
                            'cumtime': float(parts[3]),
                            'function': parts[5]
                        }
                        metrics['function_stats'].append(stats)
                        if stats['tottime'] > 0.1:  # Identify potential bottlenecks
                            metrics['bottlenecks'].append(stats['function'])
                    except (IndexError, ValueError):
                        continue
        
        if metrics['function_stats']:
            metrics['total_time'] = sum(stat['tottime'] for stat in metrics['function_stats'])
        
        return metrics

    def _get_optimization_suggestions(
        self, original_code: str, profile_results: Dict, criteria: Dict = None
    ) -> Tuple[str, str]:
        """
        Generate optimization suggestions based on profiling results.
        
        Args:
            original_code (str): Original source code
            profile_results (Dict): Profiling metrics
            criteria (Dict): Optional performance criteria to focus on
            
        Returns:
            Tuple[str, str]: Optimized code and analysis report
        """
        # Add context about performance optimization
        self.session.add_response("system", """You are a Python performance optimization expert.
        Analyze code and profiling results to suggest concrete improvements.
        Focus on:
        1. Algorithm efficiency
        2. Data structure choices
        3. Resource usage
        4. Common performance pitfalls
        Provide specific, implementable suggestions.""")

        # Create analysis fork
        analysis_request = f"""
        Original Code:
        {original_code}
        
        Profiling Results:
        {profile_results}
        
        Performance Criteria:
        {criteria if criteria else 'No specific criteria provided'}
        
        Suggest optimizations and provide improved code.
        """

        analysis_fork = self.session.Fork(
            "optimizer",
            "user",
            analysis_request
        )
        analysis_fork.Answer(self.session)

        # Extract optimized code and analysis from response
        return self._parse_optimization_response(self.session.messages[-1].content)

    def _parse_optimization_response(self, response: str) -> Tuple[str, str]:
        """Parse the optimization response to extract code and analysis."""
        # Split response into analysis and code sections
        parts = response.split("```python")
        
        if len(parts) < 2:
            return response, ""  # No code block found
            
        analysis = parts[0].strip()
        code = parts[1].split("```")[0].strip()
        
        return code, analysis

def main():
    """Example usage of SnapTune."""
    snap = SnapTune()
    
    # Example code to optimize
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(20)
print(f"Fibonacci result: {result}")
"""

    try:
        # Analyze the code with specific performance criteria
        criteria = {
            "focus": "execution_time",
            "target": "reduce_recursive_calls"
        }
        
        optimized_code, metrics, analysis = snap.analyze_code(sample_code, criteria)
        
        print("Performance Analysis")
        print("===================")
        print(analysis)
        
        print("\nOptimized Code")
        print("==============")
        print(optimized_code)
        
        print("\nPerformance Metrics")
        print("==================")
        print(f"Total Time: {metrics['total_time']:.4f} seconds")
        if metrics['bottlenecks']:
            print("\nBottlenecks:")
            for bottleneck in metrics['bottlenecks']:
                print(f"- {bottleneck}")
                
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
