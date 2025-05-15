"""
Runtime shim so `import aliparser` works from the repository root
during development/testing without requiring an editable install
(`pip install -e .`).

It re-exports the actual implementation located at
`src.lang.aliparser.aliparser`.
"""

from __future__ import annotations

import importlib
import sys
from types import ModuleType

_real_pkg = importlib.import_module("src.lang.aliparser.aliparser")

# Re-export public names
Lexer = _real_pkg.Lexer  # type: ignore[attr-defined]
Parser = _real_pkg.Parser  # type: ignore[attr-defined]
Token = _real_pkg.Token  # type: ignore[attr-defined]

__all__: list[str] = ["Lexer", "Parser", "Token"]

# Proxy any other attribute look-ups to the real package
class _ProxyModule(ModuleType):
    def __getattr__(self, name: str):  # noqa: D401
        return getattr(_real_pkg, name)

sys.modules[__name__] = _ProxyModule(__name__)
