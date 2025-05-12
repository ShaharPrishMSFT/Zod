# AgentLingua

AgentLingua is a domain-specific language designed for creating robust and type-safe AI agent interactions. It provides a clean syntax for defining agent behaviors, managing conversations, and handling state transitions.

## Quick Start

1. Create a new .al file in your project
2. Define your agent's context:
```
context your.agent
--begin
You are a specialized agent designed to [your purpose].
--end
```

3. Add functions for specific behaviors:
```
function greet.user {
    input [userName]
    action
    --begin
    Welcome {{ userName }}! How can I assist you today?
    --end
}
```

4. Define rules for conditional behavior:
```
rule check.authorization {
    when [User requests sensitive data] then {
        action [Verify user credentials]
    }
}
```

## File Structure
- `/grammar` - Contains the core language grammar
- `/examples` - Sample AgentLingua files demonstrating various features

## Documentation
See [SPECIFICATION.md](SPECIFICATION.md) for detailed language documentation.

## Examples

Check the `/examples` directory for sample code, including:
- Basic context definition
- Function parameters and actions
- Rule-based behavior
- Natural language integration
- State management
