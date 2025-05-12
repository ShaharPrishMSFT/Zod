# Language Experiments

## CRITICAL: PEG Format Requirements

**ABSOLUTELY CRITICAL**: The purpose of these experiments is to validate and ensure Lark's support for the PEG format EXACTLY AS IT IS. We will NOT attempt to find workarounds by using different formats or alternative syntaxes.

The goal is to make the PEG format work as specified in our grammar files, not to adapt our grammar to different formats. This means:

- We MUST use the exact PEG syntax as defined in our grammar files
- NO conversion to EBNF or other formats
- NO adaptation of our grammar to fit Lark's preferred syntax
- The solution MUST work with PEG format directly

This is a hard requirement and there is no room for compromise on this point. Any experiments here should focus on making the PEG format work, not finding alternative approaches.
