# os.path vs pathlib

Compare the traditional os.path module with the modern pathlib module for path operations.

!!! tip "Mental Model"
    `os.path` treats paths as plain strings and manipulates them with standalone functions (`os.path.join`, `os.path.exists`). `pathlib` wraps paths in `Path` objects with methods and operator overloads (`path / "subdir"`, `path.exists()`). The result is the same — `pathlib` is just more readable and composable. New code should prefer `pathlib`; use `os.path` when interfacing with older APIs that expect strings.

## os.path Approach

Traditional string-based path manipulation.

```python
import os

# Build path with os.path.join
parts = ['home', 'user', 'documents', 'file.txt']
path = os.path.join(*parts)
print(f"os.path: {path}")

# Extract components
print(f"dirname: {os.path.dirname(path)}")
print(f"basename: {os.path.basename(path)}")
print(f"split: {os.path.splitext(path)}")

# Check file
import tempfile
with tempfile.NamedTemporaryFile() as f:
    print(f"exists: {os.path.exists(f.name)}")
```

```
os.path: home/user/documents/file.txt
dirname: home/user/documents
basename: file.txt
split: ('home/user/documents/file', '.txt')
exists: True
```

## pathlib Approach

Modern object-oriented path manipulation.

```python
from pathlib import Path
import tempfile

# Create Path object
path = Path('home') / 'user' / 'documents' / 'file.txt'
print(f"pathlib: {path}")

# Access components
print(f"parent: {path.parent}")
print(f"name: {path.name}")
print(f"suffix: {path.suffix}")
print(f"stem: {path.stem}")

# Check file
with tempfile.NamedTemporaryFile() as f:
    p = Path(f.name)
    print(f"exists: {p.exists()}")
    print(f"is_file: {p.is_file()}")
```

```
pathlib: home/user/documents/file.txt
parent: home/user/documents
name: file.txt
suffix: .txt
stem: file
exists: True
is_file: True
```

---

## Exercises

**Exercise 1.**
Write two versions of a function `build_output_path` -- one using `os.path` and one using `pathlib` -- that takes a base directory, a subdirectory name, and a filename, and returns the full path with a `.csv` extension. Compare the readability of both approaches.

??? success "Solution to Exercise 1"

    ```python
    import os
    from pathlib import Path

    # os.path version
    def build_output_path_os(base, subdir, filename):
        return os.path.join(base, subdir, filename + ".csv")

    # pathlib version
    def build_output_path_pathlib(base, subdir, filename):
        return Path(base) / subdir / (filename + ".csv")

    # Test
    print(build_output_path_os("/data", "output", "results"))
    # /data/output/results.csv
    print(build_output_path_pathlib("/data", "output", "results"))
    # /data/output/results.csv
    ```

---

**Exercise 2.**
Using `pathlib.Path`, write a function `find_all_python_files` that takes a directory path and recursively finds all `.py` files. Return a list of `Path` objects sorted by name. Use the `rglob` method.

??? success "Solution to Exercise 2"

    ```python
    from pathlib import Path

    def find_all_python_files(directory):
        return sorted(Path(directory).rglob("*.py"), key=lambda p: p.name)

    # Test
    # files = find_all_python_files(".")
    # for f in files[:5]:
    #     print(f)
    ```

---

**Exercise 3.**
Write a function `path_components` that takes a file path string and returns a dictionary with `"parent"`, `"name"`, `"stem"`, and `"suffix"` using `pathlib.Path`. For example, `path_components("/home/user/data.csv")` should return `{"parent": "/home/user", "name": "data.csv", "stem": "data", "suffix": ".csv"}`.

??? success "Solution to Exercise 3"

    ```python
    from pathlib import Path

    def path_components(path_str):
        p = Path(path_str)
        return {
            "parent": str(p.parent),
            "name": p.name,
            "stem": p.stem,
            "suffix": p.suffix,
        }

    # Test
    print(path_components("/home/user/data.csv"))
    # {'parent': '/home/user', 'name': 'data.csv',
    #  'stem': 'data', 'suffix': '.csv'}
    ```
