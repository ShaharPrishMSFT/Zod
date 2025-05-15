# AgentLingua Parser: Whitespace Handling Issue in Natural Content

## Problem Statement

The test `test_parse_ast_context_block` expects the parser/AST to produce a `TextNode` with the text `"Hello world"` (with a space) from the following AgentLingua source:

```
# Comment
context my.agent
--begin
Hello world
--end
```

**Observed behavior:**  
- The parser produces a `TextNode` with the text `"Helloworld"` (no space).
- The test fails: `assert any(isinstance(n, TextNode) and "Hello world" in n.text for n in content)`.

**Debug output:**  
- The parse tree for `natural_content` contains only `TEXT_CHAR` tokens for each character except the space.
- The AST builder joins all token values, but since the space is not present as a token, it is omitted.

## Analysis and Guesses

- The grammar's `TEXT_CHAR` rule is currently:
  ```
  TEXT_CHAR: /[^\[\]{}\n]/   // any char except brackets, braces, or newline
  ```
- The grammar also has:
  ```
  %ignore WS
  ```
  which causes all whitespace (including spaces and tabs) to be ignored by the parser and not included in the parse tree.
- As a result, spaces are not present in the `natural_content` node, so the AST cannot reconstruct the original text with spaces.

**Hypothesis:**  
- The combination of `%ignore WS` and the definition of `TEXT_CHAR` causes all spaces to be dropped from natural content, resulting in `"Helloworld"` instead of `"Hello world"`.

**Potential fix:**  
- Remove `%ignore WS` (or at least do not ignore it within `natural_content`).
- Alternatively, redefine `TEXT_CHAR` to explicitly include spaces, or add a separate rule for spaces that are not ignored within `natural_content`.

## Current Grammar (as of this issue)

```peg
?start: (COMMENT | formal_decl_block | _NL)*

##########################
# Formal section         #
##########################

formal_decl_stripped: "context" WS_INLINE* ID? WS_INLINE* any_expr_in_formal
     | "function" WS_INLINE* ID WS_INLINE* any_expr_in_formal
     | "rule"     WS_INLINE* ID? WS_INLINE* any_expr_in_formal

formal_decl_block: WS_INLINE* formal_decl_stripped

comment_or_formal_stmt: (COMMENT_IN_BLOCKS | formal_stmt_line | _NL)

formal_block_stripped: "{" _NL? (_NL | formal_stmt)* _NL? "}"

formal_block: _NL formal_block_stripped

any_block_body_stripped: formal_block_stripped
          | natural_block_stripped

any_block_body: _NL any_block_body_stripped
formal_stmt_line:  _NL formal_stmt
    | formal_stmt

formal_stmt: if_stmt
    | when_stmt
    | input_stmt
    | action_stmt
    | nop_stmt

if_stmt: "if" any_expr_in_formal "then" (any_expr_in_formal | formal_block_stripped) _NL? ("else" (any_expr_in_formal | formal_block_stripped))?
when_stmt: "when" any_expr_in_formal "then" any_expr_in_formal
input_stmt: "input" WS_INLINE* natural_inline
action_stmt: "action" (any_expr_in_formal | formal_block_stripped)+
nop_stmt: "nop"

##########################
# Natural section        #
##########################

natural_expr: natural_inline
            | natural_block

natural_inline: "[" natural_content "]"
natural_block: _NL natural_block_stripped
natural_block_stripped: NAT_BEGIN _NL natural_content _NL NAT_END _NL?
NAT_BEGIN: "--begin"
NAT_END: "--end"

##########################
# Mixed/embedded         #
##########################

formal_expr_in_natural: "{{" _NL? formal_stmt _NL? "}}"
any_expr_in_formal: (natural_inline | formal_stmt | any_block_body)

##########################
# Primitives             #
##########################

ID: NAME ("." NAME)*
NAME: /[A-Za-z][A-Za-z0-9_]*/

natural_content: (formal_expr_in_natural | TEXT_CHAR | WS | _NL)*

TEXT_CHAR: /[^\[\]{}\n]/   // any char except brackets, braces, or newline

##########################
# Tokens & helpers       #
##########################

_NL: /(?:\r?\n)+/
COMMENT: /[ \t]*#[^\n]*/
COMMENT_IN_BLOCKS: _NL COMMENT

%import common.WS_INLINE
%import common.WS
%ignore COMMENT
%ignore COMMENT_IN_BLOCKS
%ignore WS
```

## Summary

- The test fails because spaces are not present in the parse tree due to `%ignore WS`.
- To fix, whitespace should not be ignored within `natural_content`, or `TEXT_CHAR` should be redefined to include spaces.
- The solution likely involves either removing `%ignore WS` or restructuring the grammar so that whitespace is preserved in natural content blocks.
