import os
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple
import numpy as np
from dataclasses import dataclass
from FormalAiSdk.models.litellm_executor import LiteLLMExecutor
from FormalAiSdk.sdk.session import ModelSession

@dataclass
class TodoItem:
    """Represents a TODO comment found in code."""
    file: str
    line: int
    content: str
    context: str
    type: str  # 'TODO' or 'FIXME'

class TodoHarvester:
    def __init__(self):
        """Initialize TodoHarvester with LiteLLM executor and session."""
        self.executor = LiteLLMExecutor("ollama", "llama2")
        self.session = ModelSession("todo_assistant", self.executor)
        self.todo_pattern = re.compile(r'#\s*(TODO|FIXME):?\s*(.*)')

    def harvest_todos(self, codebase_path: str) -> Tuple[List[Dict], List[List[int]]]:
        """
        Scan codebase for TODOs and organize them into clusters.
        
        Args:
            codebase_path (str): Path to the codebase root directory
            
        Returns:
            Tuple[List[Dict], List[List[int]]]: Structured TODO items and their clusters
        """
        # Find all TODO comments
        todo_items = self._find_todos(codebase_path)
        
        # Convert TODOs to structured issues
        structured_issues = self._structure_todos(todo_items)
        
        # Cluster similar items
        clusters = self._cluster_similar_items(structured_issues)
        
        return structured_issues, clusters

    def _find_todos(self, codebase_path: str) -> List[TodoItem]:
        """Find all TODO and FIXME comments in the codebase."""
        todos = []
        path = Path(codebase_path)
        
        for file_path in path.rglob('*.py'):
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    lines = file.readlines()
                    for i, line in enumerate(lines, 1):
                        match = self.todo_pattern.search(line)
                        if match:
                            # Get surrounding context (3 lines before and after)
                            start = max(0, i - 4)
                            end = min(len(lines), i + 3)
                            context = ''.join(lines[start:end])
                            
                            todos.append(TodoItem(
                                file=str(file_path.relative_to(path)),
                                line=i,
                                content=match.group(2).strip(),
                                context=context.strip(),
                                type=match.group(1)
                            ))
                except UnicodeDecodeError:
                    continue  # Skip binary files
        
        return todos

    def _structure_todos(self, todos: List[TodoItem]) -> List[Dict]:
        """Convert TODO comments into structured GitHub-style issues."""
        self.session.add_response("system", """You are a technical issue writer.
        Convert TODO comments into well-structured GitHub issues.
        Include:
        1. Clear title
        2. Detailed description
        3. Labels/tags
        4. Priority assessment
        Use the context to provide accurate and helpful issue descriptions.""")

        structured_issues = []
        
        for todo in todos:
            # Create structuring fork for each TODO
            structure_fork = self.session.Fork(
                "issue_creator",
                "user",
                f"""Convert this TODO to a structured issue:
                File: {todo.file}
                Line: {todo.line}
                Type: {todo.type}
                Content: {todo.content}
                
                Context:
                {todo.context}"""
            )
            structure_fork.Answer(self.session)
            
            # Parse the structured response
            structured_issue = self._parse_issue_response(
                self.session.messages[-1].content,
                todo
            )
            structured_issues.append(structured_issue)

        return structured_issues

    def _parse_issue_response(self, response: str, todo: TodoItem) -> Dict:
        """Parse the AI's response into a structured issue format."""
        # Create analysis fork to extract structured data
        parse_fork = self.session.Fork(
            "issue_parser",
            "user",
            f"""Extract the following from the issue description as JSON:
            1. title
            2. description
            3. labels
            4. priority
            
            Issue text:
            {response}"""
        )
        parse_fork.Answer(self.session)
        
        try:
            import json
            parsed = json.loads(self.session.messages[-1].content)
        except json.JSONDecodeError:
            # Fallback structure if parsing fails
            parsed = {
                "title": todo.content,
                "description": response,
                "labels": [todo.type.lower()],
                "priority": "medium"
            }
        
        # Add source information
        parsed.update({
            "source_file": todo.file,
            "source_line": todo.line,
            "original_content": todo.content,
            "context": todo.context
        })
        
        return parsed

    def _cluster_similar_items(self, issues: List[Dict]) -> List[List[int]]:
        """
        Cluster similar issues using embedding-based similarity.
        
        Args:
            issues (List[Dict]): List of structured issues
            
        Returns:
            List[List[int]]: Lists of issue indices forming clusters
        """
        # Get embeddings for each issue
        embeddings = self._get_embeddings(issues)
        
        # Perform clustering using cosine similarity
        clusters = []
        used_indices = set()
        
        for i in range(len(issues)):
            if i in used_indices:
                continue
                
            cluster = [i]
            used_indices.add(i)
            
            # Find similar issues
            for j in range(i + 1, len(issues)):
                if j in used_indices:
                    continue
                    
                similarity = self._cosine_similarity(embeddings[i], embeddings[j])
                if similarity > 0.8:  # Similarity threshold
                    cluster.append(j)
                    used_indices.add(j)
            
            if cluster:
                clusters.append(cluster)
        
        return clusters

    def _get_embeddings(self, issues: List[Dict]) -> List[List[float]]:
        """Get embeddings for each issue using the model."""
        embeddings = []
        
        for issue in issues:
            # Create embedding fork
            embed_fork = self.session.Fork(
                "embedder",
                "user",
                f"""Create an embedding representation of this issue:
                Title: {issue['title']}
                Description: {issue['description']}
                Return only the embedding vector as a list of floats."""
            )
            embed_fork.Answer(self.session)
            
            # Parse embedding response
            try:
                import json
                embedding = json.loads(self.session.messages[-1].content)
                if isinstance(embedding, list) and all(isinstance(x, (int, float)) for x in embedding):
                    embeddings.append(embedding)
                else:
                    # Fallback to simple encoding if parsing fails
                    embeddings.append(self._simple_encode(issue['title'] + " " + issue['description']))
            except json.JSONDecodeError:
                embeddings.append(self._simple_encode(issue['title'] + " " + issue['description']))
        
        return embeddings

    def _simple_encode(self, text: str) -> List[float]:
        """Simple fallback encoding method using character frequencies."""
        encoding = np.zeros(128)  # ASCII encoding
        for char in text:
            code = ord(char) % 128
            encoding[code] += 1
        norm = np.linalg.norm(encoding)
        return (encoding / norm if norm > 0 else encoding).tolist()

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        a_array = np.array(a)
        b_array = np.array(b)
        
        norm_a = np.linalg.norm(a_array)
        norm_b = np.linalg.norm(b_array)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        return float(np.dot(a_array, b_array) / (norm_a * norm_b))

def main():
    """Example usage of TodoHarvester."""
    harvester = TodoHarvester()
    
    # Create example Python file with TODOs
    example_code = """
# TODO: Implement error handling for edge cases
def process_data(data):
    print("Processing...")
    # FIXME: This is inefficient, needs optimization
    for item in data:
        process_item(item)
    
# TODO: Add input validation
def process_item(item):
    pass  # Implementation pending
"""
    
    # Save example file
    example_path = Path("example_code")
    example_path.mkdir(exist_ok=True)
    with open(example_path / "sample.py", "w") as f:
        f.write(example_code)
    
    try:
        # Process the codebase
        issues, clusters = harvester.harvest_todos(str(example_path))
        
        print("Found TODOs:")
        print("============")
        for i, issue in enumerate(issues):
            print(f"\n{i + 1}. {issue['title']}")
            print(f"   File: {issue['source_file']}:{issue['source_line']}")
            print(f"   Priority: {issue['priority']}")
            print(f"   Labels: {', '.join(issue['labels'])}")
            print(f"   Description: {issue['description'][:100]}...")
        
        print("\nClusters:")
        print("=========")
        for i, cluster in enumerate(clusters):
            print(f"\nCluster {i + 1}:")
            for issue_idx in cluster:
                print(f"- {issues[issue_idx]['title']}")
                
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Clean up example files
        if example_path.exists():
            for file in example_path.glob("*"):
                file.unlink()
            example_path.rmdir()

if __name__ == "__main__":
    main()
