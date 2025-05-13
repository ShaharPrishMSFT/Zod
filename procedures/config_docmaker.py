import json
import yaml
from pathlib import Path
from typing import Dict, Union, Tuple, List
from FormalAiSdk.models.litellm_executor import LiteLLMExecutor
from FormalAiSdk.sdk.session import ModelSession

class ConfigDocMaker:
    def __init__(self):
        """Initialize ConfigDocMaker with LiteLLM executor and session."""
        self.executor = LiteLLMExecutor("ollama", "llama2")
        self.session = ModelSession("config_assistant", self.executor)

    def process_config(self, config_path: str) -> Tuple[Dict, str, List[str]]:
        """
        Process a configuration file, validate it, and generate documentation.
        
        Args:
            config_path (str): Path to the config file (YAML or JSON)
            
        Returns:
            Tuple[Dict, str, List[str]]: Parsed config, documentation, and validation issues
        """
        # Load and parse the config file
        config_data = self._load_config(config_path)
        
        # Validate the configuration
        validation_issues = self._validate_config(config_data)
        
        # Generate documentation
        documentation = self._generate_documentation(config_data)
        
        return config_data, documentation, validation_issues

    def _load_config(self, config_path: str) -> Dict:
        """Load and parse config file based on its extension."""
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(path, 'r') as file:
            content = file.read()
            try:
                if path.suffix.lower() in ['.yaml', '.yml']:
                    return yaml.safe_load(content)
                elif path.suffix.lower() == '.json':
                    return json.loads(content)
                else:
                    raise ValueError(f"Unsupported file format: {path.suffix}")
            except (yaml.YAMLError, json.JSONDecodeError) as e:
                raise ValueError(f"Failed to parse config file: {str(e)}")

    def _validate_config(self, config: Dict) -> List[str]:
        """
        Validate the configuration and suggest improvements.
        
        Args:
            config (Dict): Parsed configuration data
            
        Returns:
            List[str]: List of validation issues and suggestions
        """
        self.session.add_response("system", """You are a configuration validator.
        Analyze the configuration for:
        1. Missing required fields
        2. Type inconsistencies
        3. Security concerns
        4. Best practices violations
        Return a list of specific issues and suggested fixes.""")

        # Create validation fork
        validation_fork = self.session.Fork(
            "validator",
            "user",
            f"Validate this configuration:\n{json.dumps(config, indent=2)}"
        )
        validation_fork.Answer(self.session)

        # Parse validation response into list of issues
        return self._parse_validation_response(self.session.messages[-1].content)

    def _generate_documentation(self, config: Dict) -> str:
        """
        Generate comprehensive documentation for the configuration.
        
        Args:
            config (Dict): Parsed configuration data
            
        Returns:
            str: Markdown-formatted documentation
        """
        self.session.add_response("system", """You are a technical documentation writer.
        Create clear, comprehensive documentation for configuration files.
        Include:
        1. Purpose of each key
        2. Expected value types and formats
        3. Default values and effects
        4. Examples of valid values
        Format the output in Markdown.""")

        # Create documentation fork
        doc_fork = self.session.Fork(
            "documentor",
            "user",
            f"Generate documentation for this configuration:\n{json.dumps(config, indent=2)}"
        )
        doc_fork.Answer(self.session)

        return self.session.messages[-1].content

    def _parse_validation_response(self, response: str) -> List[str]:
        """Parse the validation response into a list of issues."""
        # Split response into lines and filter out empty lines
        lines = [line.strip() for line in response.split('\n') if line.strip()]
        
        # Extract issues (lines starting with common list markers)
        issues = []
        for line in lines:
            if line.startswith(('- ', '* ', '• ', '1. ', '2. ', '3. ')):
                issues.append(line.lstrip('- *•123. '))
        
        return issues

def main():
    """Example usage of ConfigDocMaker."""
    docmaker = ConfigDocMaker()
    
    # Example config file
    example_config = {
        "api": {
            "endpoint": "https://api.example.com",
            "timeout": 30,
            "retry": {
                "max_attempts": 3,
                "delay": 1.5
            }
        },
        "logging": {
            "level": "INFO",
            "file": "app.log"
        }
    }
    
    # Save example config
    config_path = "example_config.json"
    with open(config_path, 'w') as f:
        json.dump(example_config, f, indent=2)
    
    try:
        # Process the config
        config, docs, issues = docmaker.process_config(config_path)
        
        print("Configuration Documentation")
        print("=========================")
        print(docs)
        
        if issues:
            print("\nValidation Issues")
            print("================")
            for issue in issues:
                print(f"- {issue}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Clean up example file
        Path(config_path).unlink()

if __name__ == "__main__":
    main()
