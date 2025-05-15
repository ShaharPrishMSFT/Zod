**Fast-track recipe (≈ 10 min) to turn a PEG file into a runnable Lark-powered interpreter**

---

### 2 · One‑liner that **parses anything you feed it**

```python
from lark import Lark, Transformer
PARSER = Lark.open("grammar.lark",
                   parser="lalr",          # fast deterministic parse
                   propagate_positions=True,   # line/col on every node
                   maybe_placeholders=False)   # strict – no implicit None

class Interpreter(Transformer):          # add methods = semantics
    pass                                  # stub for now

def run(src: str):
    tree = PARSER.parse(src)              # concrete‑syntax tree
    return Interpreter().transform(tree)  # your result (AST / value / side‑effects)
```

*Drop this in `driver.py`, import it anywhere, and call `run(code)`.*

---

### 3 · Instant **method stubs** for every grammar rule

Paste this in a scratch cell once; it prints boilerplate you can copy‑paste into `Interpreter`:

```python
for rule in PARSER.rules:
    name = rule.alias or rule.options.name
    print(f"    def {name}(self, children):\n        ...\n")
```

---

### 4 · (2‑second build) **freeze the parser** so import is zero‑cost

```bash
python -m lark.tools.standalone grammar.lark > fastparser.py
```

Now replace the first two lines above with:

```python
from fastparser import Lark_StandAlone as PARSER
```

No grammar loading at runtime; perfect for CLI tools and CI.

---

### 5 · Typical interpreter pattern in `Interpreter`

```python
class Interpreter(Transformer):
    def number(self, n):     return int(n[0])
    def add(self, items):    return items[0] + items[1]
    def sub(self, items):    return items[0] - items[1]
    # ‑‑ keep adding semantic actions per rule
```

*Each method receives raw child values (already transformed); return whatever your language semantics dictate.*

---

### 6 · CLI glue (optional)

```python
if __name__ == "__main__":
    import sys, pathlib
    code = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else sys.stdin.read()
    print(run(code))
```

Run with `python driver.py program.src`.

---

#### Why this is “fastest”

| Step                               | Time | What you gain             |
| ---------------------------------- | ---- | ------------------------- |
| Install Lark                       | 5 s  | zero dependencies         |
| `Lark.open` with `parser="lalr"`   | 1 s  | 200 k‑line/s parse speed  |
| Auto‑generated method stubs        | 2 s  | no manual boilerplate     |
| `lark.tools.standalone` (optional) | 2 s  | load‑time drops to \~1 ms |

After that, writing semantics is pure Python. No meta‑code generation, no C compilation, and the grammar file stays readable next to your source.
