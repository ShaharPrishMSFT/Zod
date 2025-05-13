# AgentLingua Playground Specification

A minimal AgentLingua playground should provide a code editor tuned for the `.al` language, with built-in parsing and error feedback. The **functional spec** covers the editor’s capabilities, file I/O, parsing behavior, and feedback mechanisms. The **interface spec** describes the UI layout, panels, and controls. We also include a couple of tiny `.al` code examples and optional tips for text handling and error display.

## Functional Specification

* **Editor Features:** The playground must include a rich text editor (e.g. CodeMirror or Monaco) with AgentLingua syntax support. This means **syntax highlighting** for `.al` keywords, comments, and structure (e.g. colorizing `agent`, `behavior`, etc.). It should offer **autocomplete/IntelliSense** for known keywords, actions or agent names to speed up writing. The editor should support standard code editing features (multi-line editing, indentation on Enter, Tab to indent, Undo/Redo, find/replace). Real-time parsing of partial input is encouraged: for instance, triggering the parser as the user types and marking errors inline.

* **File Loading/Saving:** Provide a simple file menu or buttons to **load a `.al` file** from the user’s machine (e.g. via file input or drag-drop) and to **save** the current code back to a file or clipboard. An **“Open”** button or menu should read a `.al` file into the editor. A **“Save”** or **“Download”** action should let the user export the current text as a `.al` file. Optionally, support copy/paste or local storage for quick editing. The goal is no cumbersome edit-save cycles: changes should be parsed immediately or on command (see Validation) so the user can see feedback without repeated manual saves.

* **Validation / Parser Integration:** Integrate the AgentLingua parser so the code can be validated on demand (e.g. via a **“Validate”** or **“Run”** button) or continuously as the user types. On each validation, the DSL input is fed to the parser. If parsing succeeds, the playground shows a success indication; if it fails, it reports errors. This should happen in (near) real-time to give immediate feedback: for example, some editors re-parse on every change and display errors as markers. The key is to avoid forcing the user to save-run in an external tool – the playground itself parses the code and reports issues instantly.

* **Output and Feedback:** After parsing, display the results in an adjacent panel. For a valid parse, this might be an abstract syntax tree or a simple “Valid syntax” message. For demonstration, the playground could show a generated representation (e.g. a JSON AST, or a human-readable interpretation of the `.al` file). If parsing fails, the output panel (or a status bar) should display error messages with line/column numbers. In-editor, errors should be highlighted (e.g. red underlines or gutter icons). The editor can annotate invalid tokens inline, for example by assigning mismatched text to an “unmatched” category so it’s visibly flagged. Hovering or clicking on an error highlight should show the parser’s error message.

* **Logging / Debug Area:** Include a collapsible log or console area (often at the bottom) to show detailed parser messages, stack traces, or debug info. This can capture things like “Parsing completed successfully” or full error stacks. If the AgentLingua parser produces debug output or warnings, they should appear here. Users may also find it helpful to see the raw output of the parse (e.g. the AST or tokens) in this area. Essentially, the log is an auxiliary text area for verbose feedback beyond the inline errors and main output.

## Interface Specification

* **Layout & Panels:** On a large screen, use a **split view**. The **left (or main) panel** is the code editor with `.al` source. The **right panel** shows parse output (AST, messages, or generated data). A **bottom area** (or a hidden panel) contains logs/errors. Panels should be resizable or collapsible. On a small screen (mobile/tablet), stack panels: show the editor on top and allow switching (via tabs or buttons) to the output and log panels below. For instance, tabs like “Editor”, “Parse Result”, “Logs” can toggle visibility on narrow displays.

* **Controls & Interactions:**

  * **Buttons/Menus:** At the top of the UI, include buttons or menu items for **Open**, **Save**, **Validate/Run**, and **Reset/Clear**. “Open” lets the user pick a `.al` file; “Save” exports the text. “Validate” or “Parse” manually runs the parser (if real-time parsing isn’t always on). “Reset” clears the editor or loads a default template. Each action should provide visual feedback (e.g. disable “Save” if nothing changed, show a checkmark if parse succeeds).
  * **Dropdowns/Options:** A theme switcher (light/dark) and font-size control can improve usability. If multiple AgentLingua grammar versions exist, a dropdown could let the user pick the grammar version.
  * **Editor Toolbar:** Optionally, include a small toolbar in the editor panel for common tasks (like indent/dedent, comment/uncomment) if the editor library doesn’t already support them via keyboard.
  * **Inline Editor:** The code area itself should allow mouse and keyboard editing: clicking to place the cursor, dragging to select, standard keys for indent (Tab) and dedent (Shift+Tab). Errors in the text should show as red underlines or gutter markers; hovering shows a tooltip with the error message.
  * **Feedback Panel:** The parse output area should update after validation. If valid, it might show the AST or a confirmation message. If invalid, it can be blank or show “Parse error – see log.” The log panel should be scrollable and show the full text of any error messages or debugging info.

* **Responsive Layout:**

  * **Large Screen:** Use a horizontal split: editor on the left \~60% width, output on the right \~40%. The log panel can be a collapsible strip at the bottom of either panel or the full width. All major UI elements (buttons, editor, output) should be visible simultaneously.
  * **Small Screen:** Possibly default to showing only the editor. Provide tabs or a menu to switch to “Output” and “Logs”. For example, a top tab bar: “Editor | Output | Logs”. When “Output” is active, the code editor is hidden and vice versa. Controls (Open/Save/Validate) remain visible (or move into a mobile menu). This ensures usability on phones/tablets.

## Minimal `.al` Examples

Below are two trivial AgentLingua code snippets to test basic syntax.

```al
# Functions must have an ID

context
--begin
You are an AI agent. Tell me your name.
--end
```

```al
function greet.user {
    input [userName]
    action
    --begin
    Hello {{ userName }}!
    --end
}
```

These examples include context and function definitions. The playground editor should accept them without errors and display an appropriate parse result (e.g. an AST or confirmation of validity). They test indentation, keywords, and basic structure.

## Optional Suggestions

* **Multiline Input & Indentation:** Use a code editor component that automatically handles indentation. For example, when the user presses Enter after a colon or bracket, the next line should auto-indent. Tab and Shift+Tab should indent/unindent lines. CodeMirror/Monaco support configuring an `indentUnit`. Ensure that pasted multi-line text preserves its newlines and that the cursor behavior is natural. If AgentLingua supports block strings or multi-line text (e.g. long descriptions), ensure those can be typed and folded.

* **Error Handling & Highlights:** When the parser finds a syntax error, mark it inline in the editor. Common UX patterns are to underline the error with a red squiggle and put an icon or marker in the gutter. Hovering over the marked text should show the error message. Use the editor’s annotation features so the user sees exactly where the parse failed. Also display the error in the log panel with context. If the code is valid, clear any previous error highlights. This live feedback (a la Monaco’s error markers) gives users immediate clues to fix their code.

* **Validation Triggers:** You may allow both on-demand and live validation. If real-time parsing is heavy, at least run the parser when the user clicks “Validate”. After parsing, the interface should scroll to or select the error line if there is one. The log can also suggest an “expected token” or “hint” if the grammar supports it. Keeping the edit-parse-debug cycle as tight as possible is key: ideally “edit → parse → feedback” with no manual save step.

Overall, the AgentLingua playground’s interface and functionality should make writing `.al` code smooth: a smart editor pane, clear parse results, and helpful inline error cues (all minimal and focused on basic editing/parsing).
