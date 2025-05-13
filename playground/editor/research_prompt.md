# AgentLingua – Deep-Research Prompt

This prompt is intended for ChatGPT / Claude / other LLMs to conduct an in-depth analysis of the **AgentLingua** DSL and its supporting Python SDK.  
Copy the whole prompt (from **System** to **Interaction Style**) into your LLM chat, then provide additional queries as needed.

---

## System  
You are an expert language-design and AI-tooling researcher with extensive knowledge of domain-specific languages, conversational agents, and formal grammar engineering.  
Work methodically, cite specific lines from the provided resources, and produce concrete, actionable insights.

## Goals  
1. Map the current syntax and semantics of AgentLingua in a concise reference table.  
2. Compare AgentLingua with at least three similar agent / dialogue DSLs (e.g., Rasa Stories, Botpress Flows, Microsoft LUIS). Highlight strengths & gaps.  
3. Propose up to **five** minimal grammar or tooling extensions that would unlock high-value use-cases while preserving the language’s elegance.  
4. Generate **five runnable `.al` example files**, each ≤ 40 lines, illustrating best practices or new extensions.  
5. Identify risks / limitations (e.g., ambiguity, scalability, tooling) and suggest mitigations.

## Resources  
All relevant resources are embedded below for self-contained analysis.

---

## Embedded Resources

### 1. AgentLingua Quick Start & Examples (`src/lang/README.md`)
```
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
```

---

### 2. AgentLingua Full Specification (`src/lang/SPECIFICATION.md`)
```
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
```
```

---

### 3. Minimal AgentLingua Example (`src/lang/examples/00_super_simple.al`)
```al
# Functions must have an ID

context
--begin
You are an AI agent. Tell me your name.
--end
```

---

### 4. FormalAI-SDK Python Interface (core executor)
```python
"""
Base model executor interface for FormalAI SDK.
"""

from abc import ABC, abstractmethod
from .types import Conversation, Message

class ModelExecutor(ABC):
    """
    Base class for model execution.
    
    This abstract class defines the interface that all model executors
    must implement. Concrete implementations will provide specific logic
    for different model types and APIs.
    """
    
    @abstractmethod
    def execute(self, conversation: Conversation) -> Message:
        """
        Execute model with given conversation history.
        
        Args:
            conversation: The conversation history to process
            
        Returns:
            Message: The model's response as a Message object
            
        Raises:
            ExecutionError: Base class for execution-related errors
            ModelError: For model-specific execution issues
            InvalidConversationError: If conversation structure is invalid
            
        Example:
            executor = ModelExecutor()
            convo = Conversation([
                Message(Role.CLIENT, "Hello"),
                Message(Role.AGENT, "Hi there")
            ])
            response = executor.execute(convo)
        """
        raise NotImplementedError
```

---

## Constraints  
1. Rely solely on repo-visible information – no external undocumented knowledge.  
2. All example files **must parse without error** when run through `FormalAI-SDK`.  
3. Favor deterministic outputs and explicit declarations.  
4. Keep explanations clear and numbered; avoid long prose paragraphs.

## Deliverables  
a. Comparative table (AgentLingua vs. three DSLs) with criteria columns.  
b. Ranked list of proposed extensions (1 ≈ highest impact).  
c. The five `.al` example files (inline fenced code blocks).  
d. Risk / limitation list with mitigation strategies.

## Interaction Style  
Use structured, numbered subsections.  
Place code inside triple-backtick fences with the correct language hint (`al`, `python`, etc.).  
Adopt a concise academic tone.

---

### AgentLingua Language Sheet  

**Purpose**: DSL for specifying AI-agent conversations, state, and control logic in a single, readable file.  
**Audience**: Prompt engineers & developers requiring type-safe, version-controlled agent definitions.

| Aspect | Details |
| --- | --- |
| Paradigm | Declarative with embedded natural language |
| Primary Blocks | `context`, `function`, `rule` |
| Execution Target | FormalAI-SDK runtime |
| Safety Roadmap | Static type/contracts (future) + runtime validation |
| Interop | Namespaced IDs consumable by other modules or SDK calls |
| Design Goals | Verbatim conversational text, diff-friendly, gradual typing |

#### Syntax Snapshot
```al
# welcome_bot.al
context welcome.greeting
--begin
You are a helpful concierge bot.
--end

function ask.name {
    input [userName?]
    action
    --begin
    Hello{{ userName? }}! May I know your full name?
    --end
}

rule personalize.greeting {
    when [User provided name] then {
        action [Invoke function greet.user]
    }
}
```

### Suggested Editor-Playground Technology  

**Primary choice:** **Streamlit** (Python)  
*Rationale:* ultra-quick local setup, no build pipeline, friendly widgets, easy integration with FormalAI-SDK, supports file drop-down, parse button, and JSON viewer.

**Alternative (optional):** Local **Jupyter Notebook** with custom `%parse_al` magic — fully offline, but UI is less streamlined for non-technical users.

### MVP Feature Set (tiny)  

1. **Editor Pane** – CodeMirror text area with rudimentary `.al` syntax highlight.  
2. **Validate Button** – Runs FormalAI-SDK parser, shows “Success” or error list.  
3. **Example Loader** – Dropdown listing files from `src/lang/examples/`; loads into editor.  
4. **Output Panel** – Displays AST / parse tree JSON of last run.  
5. **Log Area** – Shows parser / executor stdout for debugging.

_Defer authentication, persistence, multi-user handling until later iterations._
