# sys Module Overview

The `sys` module provides access to interpreter variables and system-specific parameters.

!!! tip "Mental Model"
    If `os` talks to the operating system, `sys` talks to the Python interpreter itself. It exposes the version you are running, the module search path, the recursion limit, reference counts, and the command-line arguments that started the process. Reach for `sys` when you need to introspect or configure the interpreter rather than the OS.

## Python Information

Access Python version and implementation details.

```python
import sys

# Python version
print(f"Version: {sys.version}")
print(f"Version info: {sys.version_info}")

# Python implementation
print(f"Implementation: {sys.implementation.name}")

# Executable path
print(f"Executable: {sys.executable}")

# Modules loaded
print(f"Modules loaded: {len(sys.modules)}")
```

```
Version: 3.12.0 (main, Feb 12 2026)
Version info: sys.version_info(major=3, minor=12, micro=0)
Implementation: cpython
Executable: /usr/bin/python3
Modules loaded: 50+
```

## Platform Information

Get platform and system details.

```python
import sys

# Platform
print(f"Platform: {sys.platform}")

# Byte order
print(f"Byte order: {sys.byteorder}")

# Maximum integer size
print(f"Max size: {sys.maxsize}")

# Floating point info
print(f"Float epsilon: {sys.float_info.epsilon}")
```

```
Platform: linux
Byte order: little
Max size: 9223372036854775807
Float epsilon: 2.220446049250313e-16
```

---

## Exercises

**Exercise 1.**
Write a function `python_info` that returns a dictionary containing the Python version string, major version, minor version, and the platform. Use `sys.version`, `sys.version_info`, and `sys.platform`.

??? success "Solution to Exercise 1"

    ```python
    import sys

    def python_info():
        return {
            "version": sys.version.split()[0],
            "major": sys.version_info.major,
            "minor": sys.version_info.minor,
            "platform": sys.platform,
        }

    # Test
    info = python_info()
    for key, value in info.items():
        print(f"{key}: {value}")
    ```

---

**Exercise 2.**
Write a function `check_python_minimum` that takes a minimum major and minor version (e.g., 3, 10) and returns `True` if the running Python meets or exceeds that version. Use `sys.version_info`.

??? success "Solution to Exercise 2"

    ```python
    import sys

    def check_python_minimum(major, minor):
        return sys.version_info >= (major, minor)

    # Test
    print(check_python_minimum(3, 8))   # True (if Python >= 3.8)
    print(check_python_minimum(3, 15))  # False (unlikely yet)
    ```

---

**Exercise 3.**
Write a function `sys_size_info` that returns a dictionary with the size (in bytes) of common Python objects using `sys.getsizeof`: an empty list, an empty dict, an empty string, the integer 0, and `None`.

??? success "Solution to Exercise 3"

    ```python
    import sys

    def sys_size_info():
        return {
            "empty_list": sys.getsizeof([]),
            "empty_dict": sys.getsizeof({}),
            "empty_str": sys.getsizeof(""),
            "int_zero": sys.getsizeof(0),
            "none": sys.getsizeof(None),
        }

    # Test
    sizes = sys_size_info()
    for obj, size in sizes.items():
        print(f"{obj}: {size} bytes")
    ```
