
# Path Handling (pathlib)

Python provides the **pathlib** module for working with file system paths.
It offers a modern, object-oriented interface that eliminates the most
common mistakes programmers make when handling paths: hard-coded separators,
fragile string concatenation, and scripts that break when run from a
different working directory.

```mermaid
flowchart TD
    A[pathlib.Path]
    A --> B[file path operations]
    A --> C[filesystem queries]
````

!!! tip "Mental Model"
    `pathlib.Path` treats file paths as objects, not raw strings. Instead of gluing strings together with `/` or `\\`, you build paths with the `/` operator and ask the Path object questions like "do you exist?" or "what is your extension?" This eliminates platform-specific bugs and makes path manipulation readable and safe.

---

## 1. Creating Paths

```python
from pathlib import Path

p = Path("data.txt")
```

A relative path like `Path("data.txt")` is resolved against the **current
working directory** at the time of use. This is fine in interactive sessions,
but scripts are often launched from a different directory than the one
containing the script file.

---

## 2. Script-Relative Paths

A common bug: a script opens `data.txt` assuming it sits next to the script,
but the user runs it from another directory and gets `FileNotFoundError`.

```python
# Wrong -- depends on where the user runs the script
p = Path("data.txt")

# Right -- always relative to the script's own directory
script_dir = Path(__file__).parent
p = script_dir / "data.txt"
```

`__file__` is a built-in variable that holds the path to the currently
executing script. `Path(__file__).parent` gives the directory that contains
the script, regardless of where the user launched it from.

---

## 3. Absolute Paths with `.resolve()`

`.resolve()` converts any path -- relative or containing `..` segments --
into an absolute, canonical path.

```python
p = Path("data") / ".." / "data" / "file.txt"
print(p)            # data/../data/file.txt
print(p.resolve())  # /home/alice/project/data/file.txt
```

This is useful for logging, error messages, and comparing two paths that
might refer to the same file through different relative routes.

---

## 4. Checking File Existence

```python
p.exists()
p.is_file()
p.is_dir()
```

---

## 5. Joining Paths

```python
p = Path("data") / "file.txt"
```

The `/` operator replaces fragile string concatenation like
`"data" + "/" + "file.txt"`, which breaks on Windows where the separator
is `\`.

---

## 6. Creating Directories

```python
output = Path("results") / "2024" / "january"
output.mkdir(parents=True, exist_ok=True)
```

`parents=True` creates intermediate directories (like `mkdir -p` in the
shell). `exist_ok=True` silences the error if the directory already exists.

---

## 7. Finding Files with `.glob()` and `.rglob()`

`.glob()` searches a single directory for files matching a pattern.
`.rglob()` searches recursively through all subdirectories.

```python
data = Path("data")

# All .csv files in data/
for csv_file in data.glob("*.csv"):
    print(csv_file)

# All .csv files in data/ and every subdirectory
for csv_file in data.rglob("*.csv"):
    print(csv_file)
```

Common patterns:

| Pattern | Matches |
|---|---|
| `"*.txt"` | all `.txt` files in the directory |
| `"**/*.txt"` | all `.txt` files recursively (same as `.rglob("*.txt")`) |
| `"data_*"` | files whose names start with `data_` |

---

## 8. Reading and Writing

```python
p = Path("hello.txt")

p.write_text("Hello")
print(p.read_text())
```

---

## 9. Iterating Through Directories

```python
p = Path("data")

for item in p.iterdir():
    print(item)
```

---

## 10. Advantages of pathlib

Each advantage below addresses a real failure case.

**Problem 1 -- Wrong working directory.**
A script opens `"config.json"` assuming the user runs it from the project
root. When someone runs it from their home directory, the file is not found.

```python
# Fragile: depends on working directory
config = open("config.json")

# Robust: always relative to the script
config_path = Path(__file__).parent / "config.json"
config = open(config_path)
```

**Problem 2 -- Hard-coded separators.**
A Windows developer writes `"data\\results\\output.csv"`. The path is
meaningless on macOS or Linux.

```python
# Breaks on other platforms
path = "data\\results\\output.csv"

# Works everywhere
path = Path("data") / "results" / "output.csv"
```

**Problem 3 -- Fragile string concatenation.**
Building paths with `+` is error-prone: a missing `/` silently produces
the wrong path.

```python
# Bug: "datafile.txt" instead of "data/file.txt"
path = "data" + "file.txt"

# Correct by construction
path = Path("data") / "file.txt"
```

---

## 11. Summary

Key ideas:

* `Path(__file__).parent` anchors paths to the script's location
* `.resolve()` produces an absolute, canonical path
* `.mkdir(parents=True, exist_ok=True)` safely creates directory trees
* `.glob()` and `.rglob()` find files by pattern
* the `/` operator replaces string concatenation and hard-coded separators
* methods like `.read_text()`, `.write_text()`, `.exists()`, and `.is_file()` keep path operations on a single object


## Exercises

**Exercise 1.**
`pathlib.Path` uses the `/` operator for path joining. Explain why this works:

```python
from pathlib import Path

p = Path("data") / "subfolder" / "file.txt"
print(p)
print(type(p))
```

What Python mechanism allows `/` to join paths? Why is this preferred over string concatenation (`"data" + "/" + "subfolder" + "/" + "file.txt"`)?

??? success "Solution to Exercise 1"
    Output (on a Unix-like system):

    ```text
    data/subfolder/file.txt
    <class 'PosixPath'>
    ```

    The `/` operator works because `Path` defines the `__truediv__` method, which Python calls when `/` is used. This is **operator overloading** -- the same mechanism that lets `+` mean addition for numbers and concatenation for strings.

    `Path("/")` is preferred over string concatenation because:

    1. **Platform independence**: `Path` uses the correct separator (`/` on Unix, `\` on Windows) automatically.
    2. **Type safety**: the result is a `Path` object with path-specific methods, not a raw string.
    3. **Readability**: `Path("data") / "file.txt"` is cleaner than `os.path.join("data", "file.txt")`.
    4. **Validation**: `Path` understands path semantics (e.g., resolving `.` and `..`).

---

**Exercise 2.**
`Path` objects provide methods that combine multiple `os` module calls. Compare:

```python
import os
from pathlib import Path

# os module approach
if os.path.exists("data.txt") and os.path.isfile("data.txt"):
    size = os.path.getsize("data.txt")

# pathlib approach
p = Path("data.txt")
if p.exists() and p.is_file():
    size = p.stat().st_size
```

What advantage does the object-oriented `pathlib` approach have? Why does `Path` have methods like `.read_text()` and `.write_text()` when `open()` already exists?

??? success "Solution to Exercise 2"
    The object-oriented approach groups all path-related operations on a single object. Instead of calling free functions from `os.path` and passing the path string each time, you call methods on the `Path` object.

    Advantages:

    1. **Discoverability**: all path operations are methods on the `Path` object, so IDE autocompletion shows available operations.
    2. **Chaining**: `Path("dir").mkdir(parents=True, exist_ok=True)` reads naturally.
    3. **Consistency**: one object carries the path state, reducing the chance of passing the wrong string to a function.

    `.read_text()` and `.write_text()` exist for convenience:

    ```python
    # Instead of three lines:
    with open("data.txt") as f:
        content = f.read()

    # One line:
    content = Path("data.txt").read_text()
    ```

    They are shorthand for the common pattern of "open, read/write, close" when you want the entire file content. For line-by-line processing or binary data, `open()` with `with` is still needed.

---

**Exercise 3.**
A programmer writes platform-specific path code:

```python
path = "C:\\Users\\alice\\data\\file.txt"  # Windows only
```

Explain why this fails on macOS/Linux. Show how `pathlib.Path` solves the cross-platform problem. What does `Path.home()` return, and why is it useful for writing portable code?

??? success "Solution to Exercise 3"
    `"C:\\Users\\alice\\data\\file.txt"` is a Windows-specific path. On macOS/Linux, this is treated as a single directory name containing backslashes, not as a directory hierarchy. The file would not be found.

    `pathlib.Path` solves this:

    ```python
    from pathlib import Path
    p = Path.home() / "data" / "file.txt"
    ```

    `Path.home()` returns the current user's home directory as a `Path` object:

    - Windows: `C:\Users\alice`
    - macOS: `/Users/alice`
    - Linux: `/home/alice`

    The `/` operator joins paths using the platform-appropriate separator. This code works identically on all platforms, eliminating hardcoded paths and OS-specific separators.
