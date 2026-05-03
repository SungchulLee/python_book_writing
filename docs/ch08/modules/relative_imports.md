# Relative Imports

Relative imports allow modules within a package to import each other using dot notation, without specifying the full package path.

!!! tip "Mental Model"
    Relative imports are filesystem-style navigation for packages. A single dot (`.`) means "this package," two dots (`..`) mean "parent package," just like `./` and `../` in a terminal. They keep intra-package imports stable even if the top-level package is renamed, but they only work inside packages — never in a script run directly with `python script.py`.

---

## Syntax

| Syntax | Meaning |
|--------|---------|
| `.` | Current package (same directory) |
| `..` | Parent package (one level up) |
| `...` | Grandparent package (two levels up) |

```python
from . import sibling          # Same directory
from .sibling import func      # Function from sibling
from .. import parent_module   # Parent directory
from ..utils import helper     # Module in parent's utils/
```

---

## Example Package Structure

```
mypackage/
├── __init__.py
├── core.py
├── utils.py
└── sub/
    ├── __init__.py
    ├── module_a.py
    └── module_b.py
```

### In `sub/module_a.py`

```python
# Import from same directory
from . import module_b
from .module_b import some_function

# Import from parent package
from .. import core
from .. import utils
from ..utils import helper_function

# Import from parent's sibling (if existed)
# from ..other_sub import something
```

### In `core.py`

```python
# Import from same directory
from . import utils
from .utils import helper

# Import subpackage
from .sub import module_a
from .sub.module_a import func
```

---

## Relative vs Absolute Imports

### Absolute Import

```python
from mypackage.sub.module_a import func
from mypackage.utils import helper
```

- Full path from top-level package
- Works from anywhere
- More explicit

### Relative Import

```python
from .module_a import func
from ..utils import helper
```

- Path relative to current module
- Shorter for internal imports
- Requires package context

---

## When Relative Imports Work

Relative imports **require**:

1. **`__init__.py`** in each directory (makes it a package)
2. **Module execution as part of a package** (not directly as script)

### This Works

```
project/
├── mypackage/
│   ├── __init__.py
│   ├── main.py
│   └── utils.py
```

```python
# mypackage/main.py
from .utils import helper  # ✅ Works when imported as package
```

```bash
# Run as module (from project directory)
python -m mypackage.main  # ✅ Works
```

### This Fails

```bash
# Run as script
python mypackage/main.py  # ❌ ImportError
```

Error:
```
ImportError: attempted relative import with no known parent package
```

---

## Why Direct Script Execution Fails

When you run `python mypackage/main.py`:

- Python sets `__name__ = "__main__"`
- Python sets `__package__ = None`
- No package context exists
- Relative imports cannot resolve

When you run `python -m mypackage.main`:

- Python sets `__name__ = "__main__"`
- Python sets `__package__ = "mypackage"`
- Package context exists
- Relative imports work

---

## The `-m` Flag

Always use `-m` to run modules inside packages:

```bash
# From project root (parent of mypackage)
python -m mypackage.main        # ✅ Correct
python -m mypackage.sub.module_a  # ✅ Correct

# Don't do this
python mypackage/main.py        # ❌ Breaks relative imports
```

---

## Without `__init__.py`

Since Python 3.3 (PEP 420), packages can exist without `__init__.py` (namespace packages).

**But relative imports still require `__init__.py`:**

```
mypackage/
├── core.py        # No __init__.py
└── utils.py
```

```python
# core.py
from .utils import helper  # ❌ ImportError
```

**Add `__init__.py` to enable relative imports:**

```
mypackage/
├── __init__.py    # Can be empty
├── core.py
└── utils.py
```

```python
# core.py
from .utils import helper  # ✅ Works
```

---

## Common Patterns

### Import Sibling Module

```python
# In mypackage/module_a.py
from . import module_b
from .module_b import some_class
```

### Import from Parent

```python
# In mypackage/sub/child.py
from .. import parent_module
from ..parent_module import ParentClass
```

### Import Within __init__.py

```python
# mypackage/__init__.py
from .core import MainClass
from .utils import helper

__all__ = ['MainClass', 'helper']
```

---

## Absolute vs Relative: When to Use

| Use Case | Recommendation |
|----------|----------------|
| Internal package imports | Relative (shorter, refactor-friendly) |
| External package imports | Absolute (always) |
| Public API in `__init__.py` | Either works |
| Cross-package imports | Absolute |

### Example Mixed Usage

```python
# mypackage/core.py

# External: always absolute
import numpy as np
from pandas import DataFrame

# Internal: relative is cleaner
from .utils import helper
from .sub import processor
```

---

## Debugging Relative Import Issues

### Check Package Context

```python
# Add to your module
print(f"__name__: {__name__}")
print(f"__package__: {__package__}")
```

When run correctly:
```
__name__: mypackage.main
__package__: mypackage
```

When run as script (broken):
```
__name__: __main__
__package__: None
```

### Verify `__init__.py` Exists

```bash
ls mypackage/__init__.py
ls mypackage/sub/__init__.py
```

Every directory in the import chain needs `__init__.py` for relative imports.

---

## Summary

| Scenario | Works? | Solution |
|----------|--------|----------|
| `python -m pkg.module` | ✅ | — |
| `python pkg/module.py` | ❌ | Use `-m` flag |
| Missing `__init__.py` | ❌ | Add `__init__.py` |
| Top-level script with relative | ❌ | Use absolute imports |

---

## Key Takeaways

- `.` = current package, `..` = parent package
- Relative imports require package context (`__init__.py` + `-m` flag)
- Use `python -m package.module` to run modules inside packages
- Each directory in the chain needs `__init__.py`
- Use relative imports for internal package code
- Use absolute imports for external packages

---

## Exercises

**Exercise 1.**
Given a package `mypackage` with `mypackage/utils.py` and `mypackage/core.py`, write the import statement in `core.py` that imports the `helper` function from `utils.py` using a relative import. Then write the equivalent absolute import.

??? success "Solution to Exercise 1"

    ```python
    # mypackage/core.py

    # Relative import (preferred for internal imports)
    from .utils import helper

    # Equivalent absolute import
    from mypackage.utils import helper

    # Both achieve the same result, but relative imports
    # make the package more portable (rename-friendly).
    ```

---

**Exercise 2.**
Given a package structure `pkg/sub1/mod_a.py` and `pkg/sub2/mod_b.py`, write the relative import in `mod_a.py` to import `func_b` from `mod_b.py`. Explain why `..sub2.mod_b` is needed (two dots to go up to `pkg`, then down to `sub2`).

??? success "Solution to Exercise 2"

    ```python
    # pkg/sub1/mod_a.py

    # Two dots (..) go up to the parent package 'pkg'
    # Then navigate down to sub2.mod_b
    from ..sub2.mod_b import func_b

    # Breakdown:
    # . = current package (sub1)
    # .. = parent package (pkg)
    # ..sub2 = sibling package sub2
    # ..sub2.mod_b = module mod_b inside sub2
    ```

---

**Exercise 3.**
Write a script that demonstrates the common error when running a module with relative imports directly (e.g., `python mypackage/core.py` fails) versus correctly (e.g., `python -m mypackage.core` works). Explain why the `-m` flag is necessary.

??? success "Solution to Exercise 3"

    ```python
    # mypackage/core.py
    from .utils import helper  # Relative import

    def main():
        helper()

    if __name__ == "__main__":
        main()

    # Running directly FAILS:
    #   python mypackage/core.py
    #   ImportError: attempted relative import with no known parent package
    #
    # Running with -m flag WORKS:
    #   python -m mypackage.core
    #   The -m flag tells Python to treat it as a package module,
    #   so it sets __package__ correctly and relative imports resolve.
    ```
