# os Module Overview

The `os` module provides a portable way to interact with the operating system, including file operations, environment variables, and process management.

!!! tip "Mental Model"
    The `os` module is Python's bridge to the operating system. It wraps platform-specific system calls behind a single, portable API so your code works on Linux, macOS, and Windows without `#ifdef` gymnastics. Think of it as three toolkits in one: filesystem operations, environment variable access, and process management.

## os Module Basics

Access operating system functionality.

```python
import os

# Get current working directory
cwd = os.getcwd()
print(f"Current directory: {cwd}")

# Get environment variables
path = os.environ.get('PATH', 'Not set')
print(f"PATH exists: {bool(path)}")

# Get OS name
print(f"OS: {os.name}")

# Get system
import platform
print(f"System: {platform.system()}")
```

```
Current directory: /home/user
PATH exists: True
OS: posix
System: Linux
```

## File and Directory Information

Get information about files and directories.

```python
import os
import tempfile

# Create temp file for demo
with tempfile.NamedTemporaryFile(delete=False) as f:
    temp_path = f.name
    f.write(b"test content")

try:
    # Check file existence
    print(f"File exists: {os.path.exists(temp_path)}")
    
    # Check file type
    print(f"Is file: {os.path.isfile(temp_path)}")
    print(f"Is dir: {os.path.isdir(temp_path)}")
    
    # Get file size
    print(f"Size: {os.path.getsize(temp_path)} bytes")
finally:
    os.unlink(temp_path)
```

```
File exists: True
Is file: True
Is dir: False
Size: 12 bytes
```

---

## Exercises

**Exercise 1.**
Write a function `file_info` that takes a file path and returns a dictionary with `"exists"`, `"size"`, `"is_file"`, and `"is_dir"` keys. Use `os.path` functions. Return size as 0 if the file does not exist.

??? success "Solution to Exercise 1"

    ```python
    import os

    def file_info(path):
        exists = os.path.exists(path)
        return {
            "exists": exists,
            "size": os.path.getsize(path) if exists else 0,
            "is_file": os.path.isfile(path),
            "is_dir": os.path.isdir(path),
        }

    # Test
    print(file_info("/tmp"))
    # {'exists': True, 'size': ..., 'is_file': False, 'is_dir': True}
    ```

---

**Exercise 2.**
Write a function `current_directory_contents` that returns a dictionary with two keys: `"files"` (list of file names) and `"dirs"` (list of directory names) in the current working directory. Use `os.listdir` and `os.path.isfile`/`os.path.isdir`.

??? success "Solution to Exercise 2"

    ```python
    import os

    def current_directory_contents():
        cwd = os.getcwd()
        entries = os.listdir(cwd)
        return {
            "files": [e for e in entries if os.path.isfile(os.path.join(cwd, e))],
            "dirs": [e for e in entries if os.path.isdir(os.path.join(cwd, e))],
        }

    # Test
    contents = current_directory_contents()
    print(f"Files: {len(contents['files'])}, Dirs: {len(contents['dirs'])}")
    ```

---

**Exercise 3.**
Write a function `get_os_info` that returns a dictionary containing the current working directory, the OS name (`os.name`), and the path separator (`os.sep`).

??? success "Solution to Exercise 3"

    ```python
    import os

    def get_os_info():
        return {
            "cwd": os.getcwd(),
            "os_name": os.name,
            "path_separator": os.sep,
        }

    # Test
    info = get_os_info()
    for key, value in info.items():
        print(f"{key}: {value}")
    ```
