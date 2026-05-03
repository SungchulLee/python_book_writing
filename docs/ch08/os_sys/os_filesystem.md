# File System Operations (os)

Perform file and directory operations like creating, removing, listing, and copying.

!!! tip "Mental Model"
    The `os` module's filesystem functions are Python wrappers around the same system calls your shell uses — `mkdir`, `rmdir`, `listdir`, `rename`, `remove`. They operate on path strings and return basic results. For richer, object-oriented path handling, pair them with `pathlib`, but `os` remains the go-to for low-level operations like walking directory trees or changing permissions.

## Directory Operations

Create and navigate directories.

```python
import os
import tempfile
import shutil

# Create temporary directory
temp_dir = tempfile.mkdtemp()
print(f"Created: {temp_dir}")

try:
    # Create subdirectory
    subdir = os.path.join(temp_dir, 'subdir')
    os.makedirs(subdir, exist_ok=True)
    print(f"Created subdir: {subdir}")
    
    # List directory contents
    os.chdir(temp_dir)
    print(f"Contents: {os.listdir('.')}")
finally:
    shutil.rmtree(temp_dir)
```

```
Created: /tmp/tmpXXXXXX
Created subdir: /tmp/tmpXXXXXX/subdir
Contents: ['subdir']
```

## File Operations

Create, rename, and remove files.

```python
import os
import tempfile

temp_dir = tempfile.mkdtemp()
try:
    # Create file
    file1 = os.path.join(temp_dir, 'file1.txt')
    with open(file1, 'w') as f:
        f.write('content')
    print(f"Created: {os.path.basename(file1)}")
    
    # Rename file
    file2 = os.path.join(temp_dir, 'file2.txt')
    os.rename(file1, file2)
    print(f"Renamed to: {os.path.basename(file2)}")
    
    # Remove file
    os.remove(file2)
    print("Removed file")
finally:
    import shutil
    shutil.rmtree(temp_dir)
```

```
Created: file1.txt
Renamed to: file2.txt
Removed file
```

---

## Exercises

**Exercise 1.**
Write a function `list_files_by_extension` that takes a directory path and an extension (e.g., `".txt"`) and returns a sorted list of file names matching that extension. Use `os.listdir` and `os.path.splitext`.

??? success "Solution to Exercise 1"

    ```python
    import os

    def list_files_by_extension(directory, ext):
        return sorted(
            f for f in os.listdir(directory)
            if os.path.splitext(f)[1] == ext
        )

    # Test
    # print(list_files_by_extension(".", ".py"))
    ```

---

**Exercise 2.**
Write a function `create_directory_tree` that takes a base path and a list of relative directory paths, and creates all of them using `os.makedirs` with `exist_ok=True`. Return the list of created paths.

??? success "Solution to Exercise 2"

    ```python
    import os

    def create_directory_tree(base, dirs):
        created = []
        for d in dirs:
            path = os.path.join(base, d)
            os.makedirs(path, exist_ok=True)
            created.append(path)
        return created

    # Test
    # paths = create_directory_tree("/tmp/test", ["a/b", "c", "a/d"])
    # print(paths)
    ```

---

**Exercise 3.**
Write a function `safe_delete` that takes a file path and deletes the file only if it exists and is a regular file (not a directory). Return `True` if deleted, `False` otherwise. Use `os.path.isfile` and `os.remove`.

??? success "Solution to Exercise 3"

    ```python
    import os

    def safe_delete(file_path):
        if os.path.isfile(file_path):
            os.remove(file_path)
            return True
        return False

    # Test
    # print(safe_delete("nonexistent.txt"))  # False
    ```
