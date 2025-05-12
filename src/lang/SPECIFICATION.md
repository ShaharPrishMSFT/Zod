# AgentLingua Specification

## 1. Overview
AgentLingua is a domain-specific language designed for AI agent interaction and conversation management. It combines formal structure with natural language capabilities, enabling precise control over AI behaviors while maintaining readability.

## 2. Core Language Components

### 2.1 Modules
```
module = (comment / block)*
```
- Modules are the top-level containers
- Can contain multiple blocks and comments
- Support hierarchical organization through namespaced IDs

### 2.2 Blocks
Three primary block types:
1. **Context Blocks**
   ```
   context [ID]? block_body
   ```
   - Define conversation contexts
   - Optional ID for context naming
   - Can contain natural or formal content

2. **Function Blocks**
   ```
   function ID block_body
   ```
   - Named operations with inputs
   - Required ID for referencing
   - Support parameter passing

3. **Rule Blocks**
   ```
   rule [ID]? block_body
   ```
   - Define conditional behaviors
   - Optional ID for rule naming
   - Support if/when conditions

### 2.3 Expressions
1. **Natural Expressions**
   ```
   natural_inline = "[" content "]"
   natural_block  = "--begin" content "--end"
   ```
   - Support both inline and block formats
   - Allow embedding of formal expressions (future)
   - Preserve natural language formatting

2. **Formal Expressions** 
   ```
   formal_expr = "{{" stmt "}}"
   ```
   - Embedded within natural content (future)
   - Support variable interpolation
   - Enable dynamic content generation

### 2.4 Statements
1. **Conditional Statements**
   ```
   if_stmt   = "if" natural_expr "then" action_clause ["else" action_clause]
   when_stmt = "when" natural_expr "then" action_clause
   ```
   - Support branching logic
   - Allow natural language conditions
   - Enable complex decision trees

2. **Input/Action Statements**
   ```
   input_stmt  = "input" natural_block
   action_stmt = "action" natural_expr
   ```
   - Handle user interactions
   - Define agent behaviors
   - Support state management

## 3. Type/Contract System (future)
- Strong typing through context validation
- Type inference in natural blocks
- Runtime type checking for inputs

## 4. Syntax Conventions
- Comments start with '#'
- IDs comprise of the location of the file, and the naming within. So the namespace utilities.source.git.push will be the "push" id inside the ./utilities/sources/git.al
- Natural blocks use '--begin' and '--end' delimiters
- Formal expressions embedded in natural blocks are enclosed in '{{' and '}}' (future)

## 5. Best Practices
1. **Organization**
   - Group related functionality in namespaced contexts
   - Use meaningful IDs for functions
   - Document blocks with comments

2. **Natural Language Integration**
   - Use natural blocks for AI instructions
   - Keep formal expressions concise
   - Maintain consistent formatting

3. **Error Handling**
   - Provide else clauses for error cases
   - Use when statements for validation
   - Include appropriate error messages

## 6. Examples

### Basic Context
```
# Simple context without ID
context
--begin
You are an AI agent. Tell me your name.
--end
```

### Function with Parameters
```
# Function with input parameter
function uigreetingwelcome {
    input [userName]
    action
    --begin
    Processing greeting:
    {{ action
        --begin
        User details to include:
        - Name: {{ userName }}
        - Time: {{ currentTime }}
        --end
    }}
    --end
}
```

### Rule with Conditions
```
rule auth.verify {
    if
    --begin
    Verifying authentication:
    {{ input [Credentials provided: {{ credentials }}] }}
    --end
    then {
        action [Access granted]
    }
    else {
        action [Access denied]
    }
}
