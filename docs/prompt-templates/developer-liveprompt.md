# Prompt: Create and Manage a Live Prompt Mechanism

## Goal

Create a *single, persistent markdown file* (“live prompt”) that an AI agent will use both as its instructions **and** as its working log for a multi-step task.

## High-Level Rules for the Agent

1. **One File, Markdown Only** – Write or update exactly one `.md` file.
2. **Immutable Sections** – Anything *outside* the explicitly editable fields is *frozen*; never alter wording, order, or formatting elsewhere.
3. **Editable Fields** – The agent may update **only**:

   * `Current Status` section (every field inside it).
   * Each step’s `Progress` sub-field.
4. **Protected Blocks** – Text wrapped in:

   ```
   <!-- protected -->
   ...content...
   <!-- end protected -->
   ```

   is absolutely read-only. Do **not** add, delete, or change anything inside those markers.
5. **Persistence** – Always load the existing file (do *not* start over), then save edits in place.

## Output Template (to be created or preserved exactly)

```md
# Live Prompt for [Subject Name]

## What Is This?
This markdown file is both an instruction set and a shared workspace for an AI agent.  
It contains:
- **Current Status** – live, agent-editable summary of where the work stands.  
- **Steps** – fixed definitions of the workflow. Each step has an editable **Progress** field.

<!-- protected -->
## Editing Rules (System-Critical – Do Not Change)
1. Edit only the fields listed under **Editable Fields** above.  
2. Never modify text inside any `<!-- protected --> ... <!-- end protected -->` block.  
3. Preserve all headings, bullet points, and markdown syntax exactly.
<!-- end protected -->

## Current Status
### Stage *(editable)*
[Current stage title]

### Task *(editable)*
[Specific task in focus]

### Context *(editable, optional)*
[Relevant notes]

---

## Steps

### Step 1 – [Title] *(immutable)*
#### Description *(immutable)*
[What this step entails]

#### Completion Criteria *(immutable)*
[How we know it is done]

#### Progress *(editable)*
[Agent updates go here]

---

### Step 2 – [Title]
#### Description
[What this step entails]

#### Completion Criteria
[How we know it is done]

#### Progress *(editable)*
[Agent updates go here]

---

### Step 3 – [Title]
#### Description
[What this step entails]

#### Completion Criteria
[How we know it is done]

#### Progress *(editable)*
[Agent updates go here]

---
```

## Intended Use

Ideal for research, documentation, or engineering pipelines that unfold over multiple stages and require a human-readable, version-controlled progress log.
