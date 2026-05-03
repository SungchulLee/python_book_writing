# tempfile Module

The tempfile module creates temporary files and directories with automatic cleanup. It is essential for safe temporary storage without polluting the file system.

!!! tip "Mental Model"
    `tempfile` is a janitor for scratch files. It creates files and directories in the OS temp folder with unique names (no collisions), and when used as a context manager it automatically deletes them on exit. This means you never have to worry about cleanup paths, name conflicts, or leftover files cluttering the filesystem.

---

## Named Temporary Files

### Creating Temp Files

```python
import tempfile
import os

with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    f.write("Temporary content")
    temp_name = f.name

print(f"File: {temp_name}")
print(f"Exists: {os.path.exists(temp_name)}")

os.unlink(temp_name)
```

Output:
```
File: /tmp/tmpXXXXXXXX
Exists: True
```

### Auto-Cleanup Context Manager

```python
import tempfile

with tempfile.NamedTemporaryFile(mode='w', delete=True) as f:
    f.write("Data")
    f.flush()
    print(f"Writing to {f.name}")

print(f"After context: file deleted")
```

Output:
```
Writing to /tmp/tmpXXXXXXXX
After context: file deleted
```

## Temporary Directories

### Creating Temp Directories

```python
import tempfile
import os

with tempfile.TemporaryDirectory() as tmpdir:
    filepath = os.path.join(tmpdir, "file.txt")
    with open(filepath, 'w') as f:
        f.write("Data")
    print(f"Created: {filepath}")

print(f"Directory cleaned up")
```

Output:
```
Created: /tmp/tmpXXXXXXXX/file.txt
Directory cleaned up
```

## SpooledTemporaryFile

### In-Memory Until Size Limit

```python
import tempfile

with tempfile.SpooledTemporaryFile(max_size=1024, mode='w+') as f:
    f.write("Small data")
    f.seek(0)
    print(f.read())
```

Output:
```
Small data
```

## Practical Usage

### Temporary Processing

```python
import tempfile
import os

data = ["line1\n", "line2\n", "line3\n"]

with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
    f.writelines(data)
    temp_file = f.name

with open(temp_file, 'r') as f:
    lines = f.readlines()
    print(f"Read {len(lines)} lines")

os.unlink(temp_file)
```

Output:
```
Read 3 lines
```

---

## Exercises


**Exercise 1.**
Use `tempfile.NamedTemporaryFile` to create a temporary file, write some data to it, read it back, and print the temporary file's path. Show that the file is deleted after the `with` block.

??? success "Solution to Exercise 1"

        ```python
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=True) as f:
            f.write("temporary data")
            f.flush()
            print(f"Temp file: {f.name}")
            print(f"Exists: {os.path.exists(f.name)}")  # True

        print(f"Exists after: {os.path.exists(f.name)}")  # False
        ```

    `NamedTemporaryFile` provides a visible file path and automatic cleanup when the context manager exits.

---

**Exercise 2.**
Use `tempfile.mkdtemp()` to create a temporary directory, create a file inside it, and then clean up using `shutil.rmtree()`.

??? success "Solution to Exercise 2"

        ```python
        import tempfile
        import shutil
        import os

        tmpdir = tempfile.mkdtemp()
        filepath = os.path.join(tmpdir, "data.txt")

        with open(filepath, "w") as f:
            f.write("hello")

        print(os.listdir(tmpdir))  # ['data.txt']

        shutil.rmtree(tmpdir)
        print(os.path.exists(tmpdir))  # False
        ```

    `mkdtemp()` creates the directory but does not clean it up automatically. Use `shutil.rmtree()` for cleanup.

---

**Exercise 3.**
Explain the difference between `tempfile.TemporaryFile` and `tempfile.NamedTemporaryFile`. When would you use each?

??? success "Solution to Exercise 3"

    `TemporaryFile` creates an anonymous temporary file with no visible name in the filesystem (on Unix). It cannot be accessed by other processes. `NamedTemporaryFile` creates a file with a visible name that can be passed to other processes.

        ```python
        import tempfile

        # No visible name (Unix)
        with tempfile.TemporaryFile(mode="w") as f:
            f.write("anonymous")
            # f.name exists but may not be accessible on disk

        # Visible name
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            print(f.name)  # /tmp/tmpXXXXXX
        ```

    Use `TemporaryFile` when no other process needs to access the file. Use `NamedTemporaryFile` when you need to pass the path to external tools.
