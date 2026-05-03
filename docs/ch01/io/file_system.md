# File System Basics

Programs interact with files stored on disk. To work with files effectively, you
need to understand how the file system is organized, how paths work, and how Python
provides tools for navigating directories.

!!! tip "Mental Model"
    The file system is a tree of folders and files. Every file has a unique address called a path, which traces the route from a starting point to the file. Understanding absolute vs. relative paths and how the current working directory affects file lookups is essential before reading or writing any file in Python.

---

## 1. Directory Structure

Files are organized in a hierarchical tree of folders (directories):

```text
project/
    script.py
    data/
        input.txt
        output.txt
    tests/
        test_script.py
```

Every file has a unique location in this tree, described by its **path**.

---

## 2. Paths

A **path** specifies the location of a file or directory.

### Absolute path

An absolute path starts from the **root** of the file system and uniquely
identifies a location regardless of where the program is running:

```python
# Linux / macOS
"/home/user/project/data/input.txt"

# Windows
"C:\\Users\\user\\project\\data\\input.txt"
```

### Relative path

A relative path is interpreted starting from the **current working directory**:

```python
"data/input.txt"          # file in a subdirectory
"../other_project/f.txt"  # file in a sibling directory
"./script.py"             # file in the current directory
```

Relative paths are shorter but depend on where the program is executed from.

---

## 3. Special Symbols

| Symbol | Meaning | Example |
|--------|---------|---------|
| `/`    | root directory (Unix) | `/home/user` |
| `~`    | home directory | `~/Documents` |
| `.`    | current directory | `./script.py` |
| `..`   | parent directory | `../data.txt` |

On Windows, the root is a drive letter like `C:\` and the separator is `\`.

---

## 4. Current Working Directory

Python resolves relative paths from the **current working directory** (cwd).
The cwd is typically the directory from which the Python interpreter was launched,
*not* the directory containing the script.

```python
import os

# Get the current working directory
print(os.getcwd())

# Change the current working directory
os.chdir("/home/user/project")
```

This distinction matters: if you run `python scripts/run.py` from `/home/user`,
the cwd is `/home/user`, not `/home/user/scripts`.

---

## 5. Checking Paths with os.path

The `os.path` module provides functions to inspect and manipulate paths:

```python
import os.path

os.path.exists("data.txt")       # True if the path exists
os.path.isfile("data.txt")       # True if it is a file
os.path.isdir("data")            # True if it is a directory
os.path.getsize("data.txt")      # File size in bytes
os.path.abspath("data.txt")      # Convert to absolute path
os.path.join("data", "input.txt")  # Join path components
```

Using `os.path.join` is preferred over string concatenation because it handles
the correct separator for the operating system.

---

## 6. Listing Directory Contents

```python
import os

# List all entries in a directory
entries = os.listdir("data")
print(entries)  # ['input.txt', 'output.txt']

# List with full paths
for name in os.listdir("data"):
    full_path = os.path.join("data", name)
    print(full_path, "is file:", os.path.isfile(full_path))
```

---

## 7. Creating and Removing Directories

```python
import os

# Create a single directory
os.mkdir("results")

# Create nested directories (like mkdir -p)
os.makedirs("results/2024/january", exist_ok=True)

# Remove an empty directory
os.rmdir("results")

# Remove nested empty directories
os.removedirs("results/2024/january")
```

The `exist_ok=True` parameter prevents an error if the directory already exists.

---

## 8. The pathlib Module (Modern Approach)

Python 3.4+ provides `pathlib`, which offers an object-oriented interface:

```python
from pathlib import Path

p = Path("data") / "input.txt"   # Build path with /
print(p.exists())                 # True if exists
print(p.is_file())                # True if file
print(p.resolve())                # Absolute path
print(p.parent)                   # Parent directory
print(p.name)                     # File name
print(p.suffix)                   # File extension (.txt)

# Read and write
content = p.read_text()
p.write_text("hello")

# Iterate over directory
for child in Path("data").iterdir():
    print(child)
```

`pathlib.Path` is generally preferred over `os.path` in modern Python code.

---

## 9. Key Idea

File operations depend on **where your program is running** (the current working
directory), not just where the script file is located. Always be aware of the cwd
when using relative paths, or use absolute paths to avoid ambiguity.

---

## Summary

- Files are organized in a hierarchical directory tree.
- Paths can be **absolute** (from root) or **relative** (from cwd).
- `os.getcwd()` returns the current working directory.
- `os.path` and `pathlib.Path` provide tools for path manipulation.
- Use `os.path.join()` or `Path / "name"` to build paths portably.
- `pathlib` is the modern, recommended approach for path handling.

## Exercises

**Exercise 1.**
Given the directory structure below and a cwd of `/home/user`, what does
`os.path.abspath("project/data.txt")` return?

```text
/home/user/
    project/
        data.txt
```

??? success "Solution to Exercise 1"
    `os.path.abspath` joins the cwd with the relative path:
    `/home/user` + `project/data.txt` = `/home/user/project/data.txt`.

---

**Exercise 2.**
Write a function `list_py_files(directory)` that returns a list of all `.py` files
in the given directory (not recursive).

??? success "Solution to Exercise 2"
    ```python
    from pathlib import Path

    def list_py_files(directory):
        """Return a list of .py file paths in directory."""
        return [p for p in Path(directory).iterdir()
                if p.is_file() and p.suffix == ".py"]
    ```

---

**Exercise 3.**
Explain the difference between `os.path.exists()` and `os.path.isfile()`.

??? success "Solution to Exercise 3"
    `os.path.exists(path)` returns `True` if `path` refers to any existing file
    system entry -- a file, directory, or symbolic link. `os.path.isfile(path)`
    returns `True` only if `path` is a regular file (not a directory or special
    file). For example, if `data` is a directory, `os.path.exists("data")` is
    `True` but `os.path.isfile("data")` is `False`.

---

**Exercise 4.**
Write a function `ensure_dir(path)` that creates a directory (and any necessary
parent directories) if it does not already exist. Use `pathlib`.

??? success "Solution to Exercise 4"
    ```python
    from pathlib import Path

    def ensure_dir(path):
        """Create directory and parents if they do not exist."""
        Path(path).mkdir(parents=True, exist_ok=True)
    ```

    `parents=True` creates intermediate directories, and `exist_ok=True` avoids
    an error if the directory already exists.

---

**Exercise 5.**
A script at `/home/user/project/scripts/run.py` opens `open("../data/input.txt")`.
If you run the script from `/home/user/project`, what file does it open? What if
you run it from `/home/user`?

??? success "Solution to Exercise 5"
    The relative path `../data/input.txt` is resolved from the **cwd**, not from
    the script's location.

    - From `/home/user/project`: the path resolves to `/home/user/data/input.txt`.
    - From `/home/user`: the path resolves to `/home/data/input.txt`.

    Neither of these is likely the intended file. To avoid this problem, compute
    the path relative to the script:

    ```python
    from pathlib import Path
    base = Path(__file__).resolve().parent
    data_file = base / ".." / "data" / "input.txt"
    ```

    This always resolves to `/home/user/project/data/input.txt` regardless of cwd.
