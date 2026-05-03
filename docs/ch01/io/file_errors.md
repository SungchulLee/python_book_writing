# Handling File Errors

File operations can fail for many reasons: the file may not exist, the user may lack
permission, or the disk may be full. Robust programs anticipate these failures and
handle them gracefully using Python's exception mechanism.

!!! tip "Mental Model"
    File errors are boundary failures---they happen where your program meets the outside world. The file might not exist, permissions might be wrong, or the disk might be full. Wrapping file operations in `try/except` blocks lets your program fail gracefully instead of crashing when the real world does not cooperate.

---

## 1. Common File Exceptions

Python raises specific exceptions for different file-related errors:

| Exception | When it occurs |
|-----------|---------------|
| `FileNotFoundError` | Opening a file that does not exist (read mode) |
| `PermissionError` | Insufficient permissions to read/write |
| `IsADirectoryError` | Attempting to open a directory as a file |
| `FileExistsError` | Creating a file that already exists (with `'x'` mode) |
| `OSError` | General OS-level errors (disk full, bad path, etc.) |

All of these are subclasses of `OSError`, so catching `OSError` catches them all.

---

## 2. Basic try/except

The simplest pattern wraps the file operation in a `try` block and catches the
most likely exception:

```python
try:
    with open("data.txt") as f:
        content = f.read()
        print(content)
except FileNotFoundError:
    print("Error: 'data.txt' was not found.")
```

The `with` statement ensures the file is closed even if an exception occurs inside
the block.

---

## 3. Catching Multiple Exceptions

When several failure modes are possible, catch each one separately to provide
specific error messages:

```python
try:
    with open("data.txt") as f:
        data = f.read()
except FileNotFoundError:
    print("File does not exist.")
except PermissionError:
    print("Permission denied. Check file permissions.")
except OSError as e:
    print(f"OS error: {e}")
```

More specific exceptions should come before more general ones. If `OSError` were
listed first, it would catch `FileNotFoundError` and `PermissionError` before their
handlers could run.

---

## 4. The else and finally Clauses

The full `try` statement supports two additional clauses:

```python
try:
    f = open("data.txt")
except FileNotFoundError:
    print("File not found.")
else:
    # Runs only if no exception occurred
    content = f.read()
    print(f"Read {len(content)} characters.")
    f.close()
finally:
    # Always runs, whether or not an exception occurred
    print("File operation attempted.")
```

- **`else`**: runs when the `try` block completes without raising an exception.
  Use it to separate "success" logic from error handling.
- **`finally`**: runs unconditionally. It is typically used for cleanup, though
  the `with` statement handles file closing more cleanly.

---

## 5. Accessing Exception Details

Exception objects carry useful information. The `as` keyword binds the exception
to a variable:

```python
try:
    with open("/etc/shadow") as f:
        f.read()
except PermissionError as e:
    print(f"Error number: {e.errno}")
    print(f"Message: {e.strerror}")
    print(f"Filename: {e.filename}")
```

The attributes `errno`, `strerror`, and `filename` are available on all `OSError`
subclasses.

---

## 6. Raising Exceptions

Sometimes you want to validate a file before processing it and raise your own
exception:

```python
import os

def read_config(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path) as f:
        return f.read()
```

Use `raise` to signal errors explicitly when a condition check fails.

---

## 7. Practical Pattern: Safe File Reading

A reusable function that reads a file with error handling:

```python
def safe_read(path):
    """Read a file and return its contents, or None on failure."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
    except PermissionError:
        print(f"Permission denied: {path}")
    except OSError as e:
        print(f"Cannot read {path}: {e}")
    return None
```

---

## Summary

- File operations can raise `FileNotFoundError`, `PermissionError`, and other
  `OSError` subclasses.
- Use `try/except` to handle errors; list specific exceptions before general ones.
- The `else` clause runs on success; `finally` runs unconditionally.
- Use `as e` to access details like `e.errno`, `e.strerror`, and `e.filename`.
- The `with` statement ensures files are closed regardless of exceptions.

## Exercises

**Exercise 1.**
Write a function `count_lines(path)` that returns the number of lines in a file,
or $-1$ if the file cannot be read.

??? success "Solution to Exercise 1"
    ```python
    def count_lines(path):
        """Return the number of lines in path, or -1 on failure."""
        try:
            with open(path) as f:
                return sum(1 for _ in f)
        except OSError:
            return -1
    ```

---

**Exercise 2.**
What is the output of the following code if `missing.txt` does not exist?

```python
try:
    with open("missing.txt") as f:
        data = f.read()
except FileNotFoundError:
    print("A")
else:
    print("B")
finally:
    print("C")
```

??? success "Solution to Exercise 2"
    Opening `missing.txt` raises `FileNotFoundError`. The `except` block prints `A`.
    The `else` block is skipped (it only runs if no exception occurred). The `finally`
    block always runs and prints `C`. Output:

    ```text
    A
    C
    ```

---

**Exercise 3.**
Explain why catching the bare `Exception` class (or worse, `BaseException`) is
discouraged when handling file errors.

??? success "Solution to Exercise 3"
    Catching `Exception` intercepts all standard exceptions, including unrelated
    ones like `KeyboardInterrupt` (via `BaseException`), `TypeError`, `ValueError`,
    and bugs in the code itself. This masks real programming errors and makes
    debugging difficult. Instead, catch the narrowest applicable exception (e.g.,
    `FileNotFoundError` or `OSError`) so that unexpected errors propagate normally
    and are noticed.

---

**Exercise 4.**
Write a function `safe_write(path, text)` that writes `text` to a file. If the
write fails, it should print an error message and return `False`; on success it
returns `True`.

??? success "Solution to Exercise 4"
    ```python
    def safe_write(path, text):
        """Write text to path. Return True on success, False on failure."""
        try:
            with open(path, "w") as f:
                f.write(text)
            return True
        except PermissionError:
            print(f"Permission denied: {path}")
        except OSError as e:
            print(f"Cannot write to {path}: {e}")
        return False
    ```
