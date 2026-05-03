# Version Check

!!! tip "Mental Model"
    `np.__version__` is the quickest way to verify which NumPy you are running. Think of the version as a **contract between your code and the library**: your code assumes certain functions exist and behave in certain ways, and the version guarantees those assumptions hold. When the version changes, the contract may change too.

    The critical insight: **version changes behavior, not just features.** A new
    version may add functions (features), but it may also change default dtypes,
    random number algorithms, or floating-point edge-case handling (behavior).
    Code that produces correct results under one version can silently produce
    different results under another — this is why version pinning is a
    correctness issue, not just a convenience.

!!! danger "Same Code, Different Version, Different Result"
    ```python
    # NumPy < 1.20: np.random.seed(42); np.random.random()
    # produces 0.3745401188...

    # NumPy >= 1.25 with default_rng:
    # rng = np.random.default_rng(42); rng.random()
    # produces 0.7739560485...
    ```
    The old and new random APIs produce completely different sequences from the same seed. Code that worked "correctly" under one version silently produces different results under another. This is why version checking and pinning are essential for reproducible computation.

## Check Version

### 1. Using __version__

Check the installed NumPy version.

```python
import numpy as np

def main():
    print(f"NumPy version: {np.__version__}")

if __name__ == "__main__":
    main()
```

**Output:**

```
NumPy version: 1.26.0
```

### 2. Command Line

Check version from terminal.

```bash
python -c "import numpy; print(numpy.__version__)"
```

Or using pip:

```bash
pip show numpy
```

### 3. Detailed Info

Get comprehensive build information.

```python
import numpy as np

def main():
    print(np.show_config())

if __name__ == "__main__":
    main()
```

## Verify Install

### 1. Basic Test

Verify NumPy works correctly.

```python
import numpy as np

def main():
    # Create array
    a = np.array([1, 2, 3, 4, 5])
    
    # Basic operations
    print(f"Array: {a}")
    print(f"Sum: {a.sum()}")
    print(f"Mean: {a.mean()}")
    
    print("NumPy is working!")

if __name__ == "__main__":
    main()
```

### 2. Matrix Operations

Test linear algebra functionality.

```python
import numpy as np

def main():
    A = np.array([[1, 2], [3, 4]])
    b = np.array([5, 6])
    
    # Matrix multiplication
    result = A @ b
    print(f"Matrix multiply: {result}")
    
    # Determinant
    det = np.linalg.det(A)
    print(f"Determinant: {det}")
    
    print("Linear algebra working!")

if __name__ == "__main__":
    main()
```

### 3. Random Generation

Test random number generation.

```python
import numpy as np

def main():
    np.random.seed(42)
    
    samples = np.random.randn(5)
    print(f"Random samples: {samples}")
    
    print("Random generation working!")

if __name__ == "__main__":
    main()
```

## Troubleshooting

### 1. Import Error

If NumPy is not found:

```bash
# Check if installed
pip list | grep numpy

# Reinstall if needed
pip uninstall numpy
pip install numpy
```

### 2. Version Mismatch

If you need a different version:

```python
import numpy as np

def main():
    required = "1.24.0"
    installed = np.__version__
    
    print(f"Required: {required}")
    print(f"Installed: {installed}")
    
    # Compare versions
    from packaging import version
    if version.parse(installed) < version.parse(required):
        print("Upgrade needed!")

if __name__ == "__main__":
    main()
```

### 3. Multiple Pythons

Ensure correct Python environment:

```bash
# Check which Python
which python

# Check which pip
which pip

# They should match
python -c "import sys; print(sys.executable)"
```


---

## Exercises

**Exercise 1.** Write a script that prints the NumPy version and checks if it is at least version 1.20. Print a warning if the version is older.

??? success "Solution to Exercise 1"
    ```python
    import numpy as np

    version = np.__version__
    print(f"NumPy version: {version}")

    major, minor = [int(x) for x in version.split(".")[:2]]
    if (major, minor) < (1, 20):
        print("Warning: NumPy 1.20+ recommended")
    else:
        print("Version OK")
    ```

---

**Exercise 2.** Use `np.show_config()` to display the build configuration. What information does this provide?

??? success "Solution to Exercise 2"
    ```python
    import numpy as np
    np.show_config()
    ```

    This shows build details including the BLAS/LAPACK libraries used, compiler information, and optimization flags. It helps diagnose performance issues or verify that optimized linear algebra libraries are linked.

---

**Exercise 3.** Write a function `check_numpy_version(min_version: str) -> bool` that parses version strings and returns `True` if the installed version meets the requirement.

??? success "Solution to Exercise 3"
    ```python
    import numpy as np

    def check_numpy_version(min_version: str) -> bool:
        installed = tuple(int(x) for x in np.__version__.split(".")[:3])
        required = tuple(int(x) for x in min_version.split("."))
        return installed >= required

    print(check_numpy_version("1.20.0"))  # True or False
    ```

---

**Exercise 4.** Explain why checking the NumPy version matters when writing code that uses newer features like `np.random.default_rng()`.

??? success "Solution to Exercise 4"
    `np.random.default_rng()` was introduced in NumPy 1.17. Code using newer APIs will fail with `AttributeError` on older versions. Checking the version at startup lets you provide helpful error messages or fall back to older APIs.

---

**Exercise 5.**
Write a decorator `requires_numpy(min_version)` that checks the NumPy version before running a function. If the version is too old, it should raise `RuntimeError` with a helpful message. Apply it to a function that uses `np.random.default_rng` (requires 1.17+).

??? success "Solution to Exercise 5"
    ```python
    import numpy as np
    import functools

    def requires_numpy(min_version):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                installed = tuple(int(x) for x in np.__version__.split(".")[:3])
                required = tuple(int(x) for x in min_version.split("."))
                if installed < required:
                    raise RuntimeError(
                        f"{func.__name__} requires NumPy >= {min_version}, "
                        f"but {np.__version__} is installed"
                    )
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @requires_numpy("1.17.0")
    def generate_samples(n, seed=42):
        rng = np.random.default_rng(seed)
        return rng.standard_normal(n)

    print(generate_samples(5))
    ```

    This pattern is useful in libraries that must support multiple NumPy versions. The decorator makes version requirements explicit and produces clear error messages instead of cryptic `AttributeError`s.
