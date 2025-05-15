"""
ali-parser package root.

Exposes the Lark-based AgentLinguaParser and ParserError for AgentLingua PEG parsing.
"""

from __future__ import annotations

from .parser import AgentLinguaParser, ParserError

__all__: list[str] = ["AgentLinguaParser", "ParserError"]

__version__: str = "0.1.0"
