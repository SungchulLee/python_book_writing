# Package Creation

Learn how to create a proper Python package that can be installed with `pip` and shared with others.

!!! tip "Mental Model"
    A Python package is just a directory with the right metadata files so that `pip` knows how to install it. At minimum you need a `pyproject.toml` (or `setup.py`) declaring the package name, version, and dependencies, plus an `__init__.py` inside your source directory. Once this scaffolding is in place, `pip install .` makes your code importable from anywhere on the system.

---

## Package Structure

A minimal installable package:

```
mytools/
├── pyproject.toml      # Build configuration (modern)
├── setup.py            # Build configuration (legacy, optional)
├── README.md           # Documentation
├── LICENSE             # License file
├── mytools/            # Source code
│   ├── __init__.py
│   ├── core.py
│   └── utils.py
└── tests/              # Test files
    └── test_core.py
```

---

## Step 1: Create the Package Directory

```bash
mkdir mytools
cd mytools
mkdir mytools tests
```

---

## Step 2: Write Your Code

### `mytools/__init__.py`

```python
"""mytools - A collection of useful utilities."""

from .core import add, subtract
from .utils import helper

__version__ = "0.1.0"
__all__ = ["add", "subtract", "helper"]
```

### `mytools/core.py`

```python
"""Core mathematical functions."""

def add(a, b):
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    return a - b
```

### `mytools/utils.py`

```python
"""Utility functions."""

def helper(data):
    """Process data."""
    return [x * 2 for x in data]
```

---

## Step 3: Create pyproject.toml (Modern)

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "mytools"
version = "0.1.0"
description = "A collection of useful utilities"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.8"
authors = [
    {name = "Your Name", email = "your@email.com"}
]

dependencies = [
    # Add runtime dependencies here
    # "numpy>=1.20",
    # "pandas>=1.3",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black",
    "flake8",
]

[project.urls]
Homepage = "https://github.com/yourusername/mytools"
Documentation = "https://github.com/yourusername/mytools#readme"

[project.scripts]
# Command-line entry points
mytools-cli = "mytools.cli:main"
```

---

## Step 4: Create setup.py (Legacy/Optional)

For backward compatibility:

```python
from setuptools import setup, find_packages

setup(
    name="mytools",
    version="0.1.0",
    description="A collection of useful utilities",
    author="Your Name",
    author_email="your@email.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        # "numpy>=1.20",
    ],
)
```

---

## Step 5: Add README.md

```markdown
# mytools

A collection of useful utilities.

## Installation

```bash
pip install mytools
```

## Usage

```python
from mytools import add, subtract, helper

print(add(2, 3))        # 5
print(subtract(5, 2))   # 3
print(helper([1, 2, 3])) # [2, 4, 6]
```

## License

MIT
```

---

## Step 6: Add LICENSE

For MIT License:

```
MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Choose a license at https://choosealicense.com/

---

## Step 7: Install Locally (Development Mode)

```bash
# From the project root (where pyproject.toml is)
pip install -e .
```

The `-e` flag means "editable" — changes to source code take effect immediately.

```python
>>> import mytools
>>> mytools.add(2, 3)
5
>>> mytools.__version__
'0.1.0'
```

---

## Adding Tests

### `tests/test_core.py`

```python
import pytest
from mytools import add, subtract

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(1, 1) == 0
```

Run tests:

```bash
pip install pytest
pytest tests/
```

---

## Adding CLI Entry Points

### `mytools/cli.py`

```python
import argparse
from . import add, subtract

def main():
    parser = argparse.ArgumentParser(description="mytools CLI")
    parser.add_argument("operation", choices=["add", "subtract"])
    parser.add_argument("a", type=float)
    parser.add_argument("b", type=float)
    
    args = parser.parse_args()
    
    if args.operation == "add":
        result = add(args.a, args.b)
    else:
        result = subtract(args.a, args.b)
    
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
```

### Update pyproject.toml

```toml
[project.scripts]
mytools-cli = "mytools.cli:main"
```

After `pip install -e .`:

```bash
mytools-cli add 2 3
# Result: 5.0
```

---

## Building for Distribution

### Install Build Tools

```bash
pip install build twine
```

### Build the Package

```bash
python -m build
```

This creates:
```
dist/
├── mytools-0.1.0.tar.gz    # Source distribution
└── mytools-0.1.0-py3-none-any.whl  # Wheel (binary)
```

---

## Publishing to PyPI

### 1. Create PyPI Account

Register at https://pypi.org/account/register/

### 2. Upload with Twine

```bash
# Test PyPI first (recommended)
twine upload --repository testpypi dist/*

# Production PyPI
twine upload dist/*
```

### 3. Using API Token (Recommended)

```bash
# Create token at https://pypi.org/manage/account/token/
twine upload --username __token__ --password pypi-XXXXX dist/*
```

---

## requirements.txt vs pyproject.toml

| File | Purpose |
|------|---------|
| `pyproject.toml` | Package metadata and dependencies for installation |
| `requirements.txt` | Exact versions for reproducible environments |

### requirements.txt

```
numpy==1.24.0
pandas==2.0.0
pytest==7.4.0
```

Generate from installed packages:

```bash
pip freeze > requirements.txt
```

Install from file:

```bash
pip install -r requirements.txt
```

---

## Complete Project Structure

```
mytools/
├── pyproject.toml
├── setup.py              # Optional (legacy)
├── README.md
├── LICENSE
├── requirements.txt      # For development
├── .gitignore
├── mytools/
│   ├── __init__.py
│   ├── __main__.py       # For `python -m mytools`
│   ├── core.py
│   ├── utils.py
│   └── cli.py
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_utils.py
└── docs/
    └── index.md
```

### `.gitignore`

```
__pycache__/
*.pyc
*.egg-info/
dist/
build/
.eggs/
*.egg
.pytest_cache/
.venv/
venv/
```

### `mytools/__main__.py`

```python
"""Allow running as `python -m mytools`."""
from .cli import main

if __name__ == "__main__":
    main()
```

---

## Summary

| Step | Command/File |
|------|--------------|
| Create structure | `mkdir mytools && cd mytools` |
| Write code | `mytools/__init__.py`, `mytools/core.py` |
| Configure build | `pyproject.toml` |
| Install locally | `pip install -e .` |
| Run tests | `pytest tests/` |
| Build | `python -m build` |
| Publish | `twine upload dist/*` |

---

## Key Takeaways

- Use `pyproject.toml` for modern package configuration
- `pip install -e .` for editable/development installation
- Export public API in `__init__.py`
- Add `__main__.py` for `python -m package` support
- Use `[project.scripts]` for CLI entry points
- Build with `python -m build`, publish with `twine`

---

## Exercises

**Exercise 1.**
Write a minimal `pyproject.toml` file for a package called `myutils` with version `"0.1.0"`, a description, and Python 3.8+ requirement. Include a `[project.scripts]` entry that maps the command `myutils-cli` to `myutils.cli:main`.

??? success "Solution to Exercise 1"

    ```toml
    [build-system]
    requires = ["setuptools>=61.0"]
    build-backend = "setuptools.backends._legacy:_Backend"

    [project]
    name = "myutils"
    version = "0.1.0"
    description = "A collection of utility functions"
    requires-python = ">=3.8"

    [project.scripts]
    myutils-cli = "myutils.cli:main"
    ```

---

**Exercise 2.**
Create the directory structure for a Python package called `datatools` that has two submodules: `datatools.io` (for reading/writing) and `datatools.transform` (for data transformations). Write the `__init__.py` files so that `from datatools import read_csv, normalize` works.

??? success "Solution to Exercise 2"

    ```
    datatools/
        __init__.py
        io.py
        transform.py
    ```

    ```python
    # datatools/__init__.py
    from datatools.io import read_csv
    from datatools.transform import normalize

    __all__ = ["read_csv", "normalize"]
    ```

    ```python
    # datatools/io.py
    def read_csv(path):
        print(f"Reading {path}")
        return []
    ```

    ```python
    # datatools/transform.py
    def normalize(data):
        print("Normalizing data")
        return data
    ```

---

**Exercise 3.**
Write a `__main__.py` file for a package called `analyzer` so that running `python -m analyzer` prints usage information and accepts a `--version` flag. Use `argparse` inside `__main__.py`.

??? success "Solution to Exercise 3"

    ```python
    # analyzer/__main__.py
    import argparse

    def main():
        parser = argparse.ArgumentParser(
            prog="analyzer",
            description="Data analysis tool"
        )
        parser.add_argument(
            "--version", action="version", version="analyzer 1.0.0"
        )
        parser.add_argument("input", nargs="?", help="Input file")
        args = parser.parse_args()

        if args.input:
            print(f"Analyzing {args.input}...")
        else:
            parser.print_help()

    main()
    # Run with: python -m analyzer
    # or: python -m analyzer --version
    ```
