from __future__ import annotations

"""
Light-weight lexical scanner for AgentLingua source.

This module purposefully limits itself to *lexing only* for STEP-3 of the
ali-parser roadmap.  It recognises:

    • COMMENT              – single-line “# …” until end-of-line
    • COMMENT_IN_BLOCKS    – “/* … */” multi-line comment
    • _NL                  – normalised newline token (\\n or \\r\\n)

All other characters are currently skipped; full tokenisation will be added
in subsequent steps.

The scanner maintains line / column counters and records simple error strings
(e.g. unterminated block comment).  Down-stream parser stages may choose to
consume the `Token` objects or access `.errors` for diagnostics.
"""

from dataclasses import dataclass
import re
from typing import List, Sequence


@dataclass(slots=True)
class Token:
    """A minimal token structure suitable for early bootstrap work."""
    type: str
    value: str
    line: int
    column: int


class Lexer:
    _RE_NEWLINE = re.compile(r"\r\n|\n")  # recognise CRLF & LF

    def __init__(self, text: str) -> None:
        self.text: str = text
        self.pos: int = 0
        self.line: int = 1
        self.col: int = 1
        self.length: int = len(text)

        self._tokens: list[Token] = []
        self.errors: list[str] = []

        self._scan()

    # --------------------------------------------------------------------- #
    # Public API                                                            #
    # --------------------------------------------------------------------- #

    def tokens(self) -> Sequence[Token]:
        """Return immutable view of produced tokens."""
        return tuple(self._tokens)

    # --------------------------------------------------------------------- #
    # Internal helpers                                                      #
    # --------------------------------------------------------------------- #

    def _peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        if idx < self.length:
            return self.text[idx]
        return ""

    def _advance(self, count: int = 1) -> None:
        """Advance `count` characters updating line/col trackers."""
        for _ in range(count):
            if self.pos >= self.length:
                return
            ch = self.text[self.pos]
            self.pos += 1
            if ch == "\n":
                self.line += 1
                self.col = 1
            else:
                self.col += 1

    # ------------------------------------------------------------------ #

    def _scan(self) -> None:  # noqa: C901  – early bootstrap
        while self.pos < self.length:
            ch = self._peek()

            # -------- Whitespace (except newline) ----------------------- #
            if ch in {" ", "\t", "\r"}:
                self._advance()
                continue

            # -------- Newline ------------------------------------------ #
            if ch == "\n":
                self._emit("_NL", "\n")
                self._advance()
                continue

            # -------- Single-line comment ------------------------------ #
            if ch == "#":
                start_col = self.col
                start_pos = self.pos
                # consume until newline or EOF
                while self._peek() not in {"\n", ""}:
                    self._advance()
                value = self.text[start_pos:self.pos]
                self._emit("COMMENT", value, start_line=self.line, start_col=start_col)
                continue

            # -------- Block comment ------------------------------------ #
            if ch == "/" and self._peek(1) == "*":
                start_line, start_col = self.line, self.col
                self._advance(2)  # skip '/*'
                content_start = self.pos
                terminated = False
                while self.pos < self.length:
                    if self._peek() == "*" and self._peek(1) == "/":
                        value = self.text[content_start:self.pos]
                        self._advance(2)
                        terminated = True
                        break
                    self._advance()
                if not terminated:
                    # Unterminated comment till EOF
                    value = self.text[content_start:]
                    self.errors.append(
                        f"Unterminated block comment starting "
                        f"at {start_line}:{start_col}"
                    )
                self._emit(
                    "COMMENT_IN_BLOCKS",
                    value,
                    start_line=start_line,
                    start_col=start_col,
                )
                continue

            # -------- Unknown chars (skip for now) ---------------------- #
            self._advance()

    # ------------------------------------------------------------------ #

    def _emit(
        self,
        type_: str,
        value: str,
        *,
        start_line: int | None = None,
        start_col: int | None = None,
    ) -> None:
        tok = Token(
            type=type_,
            value=value,
            line=start_line if start_line is not None else self.line,
            column=start_col if start_col is not None else self.col,
        )
        self._tokens.append(tok)


# ---------------------------------------------------------------------- #
# Minimal parser façade (placeholder)                                    #
# ---------------------------------------------------------------------- #


class Parser:
    """Stub parser exposing only lexing for STEP-3."""

    def __init__(self, source: str) -> None:
        self.lexer = Lexer(source)

    def lex(self) -> Sequence[Token]:
        """Return the token stream produced by the lexer."""
        return self.lexer.tokens()
