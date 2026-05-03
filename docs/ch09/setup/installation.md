# Installation

!!! tip "Mental Model"
    NumPy is a single `pip install numpy` away. It ships pre-compiled wheels for all major platforms, so there is no need to compile C code yourself. If you use Anaconda, NumPy is already included. Pin the version in your `requirements.txt` to ensure reproducible environments across machines.

    **Key insight:** installing NumPy is not just setup — it is defining a **reproducible computational environment**. The same code can produce different results under different NumPy versions (default dtypes, random number generators, and numerical precision have all changed between releases). Pinning versions and using virtual environments ensures that your computations are repeatable.

## pip Install

### 1. Basic Install

Install NumPy using Python's package manager.

```bash
pip install numpy
```

### 2. Specific Version

Install a specific version if needed.

```bash
pip install numpy==1.26.0
```

### 3. Upgrade Existing

Upgrade to the latest version.

```bash
pip install --upgrade numpy
```

## conda Install

### 1. Basic Install

Install NumPy using Anaconda/Miniconda.

```bash
conda install numpy
```

### 2. From conda-forge

Install from the conda-forge channel.

```bash
conda install -c conda-forge numpy
```

### 3. Specific Version

```bash
conda install numpy=1.26.0
```

## Virtual Environment

### 1. Create Environment

Isolate NumPy installation in a virtual environment.

```bash
# Using venv
python -m venv myenv

# Activate (Linux/macOS)
source myenv/bin/activate

# Activate (Windows)
myenv\Scripts\activate
```

### 2. Install in venv

```bash
# After activation
pip install numpy
```

### 3. conda Environment

```bash
# Create with NumPy
conda create -n myenv numpy

# Activate
conda activate myenv
```

## Platform Support

### 1. Cross-Platform

NumPy works on all major operating systems.

```python
import numpy as np
import platform

def main():
    print(f"OS: {platform.system()}")
    print(f"NumPy version: {np.__version__}")

if __name__ == "__main__":
    main()
```

### 2. Supported Systems

- **Windows**: Windows 10/11, x64
- **macOS**: Intel and Apple Silicon (M1/M2/M3)
- **Linux**: Most distributions, x64 and ARM

### 3. Python Versions

NumPy supports recent Python versions. Check compatibility:

```bash
# Check your Python version
python --version

# NumPy 1.26+ requires Python 3.9+
```


---

## Exercises

**Exercise 1.** Install NumPy using pip and verify the installation by printing the version number. What command do you run?

??? success "Solution to Exercise 1"
    ```python
    import numpy as np
    print(np.__version__)
    ```

    Install with: `pip install numpy`

---

**Exercise 2.** Write a script that checks if NumPy is installed and prints a helpful error message if it is not.

??? success "Solution to Exercise 2"
    ```python
    try:
        import numpy as np
        print(f"NumPy {np.__version__} is installed")
    except ImportError:
        print("NumPy is not installed. Run: pip install numpy")
    ```

---

**Exercise 3.** Explain the difference between `pip install numpy` and `conda install numpy`. When might you prefer one over the other?

??? success "Solution to Exercise 3"
    `pip install numpy` installs from PyPI and works in any Python environment. `conda install numpy` uses Anaconda's package manager, which can install optimized BLAS/LAPACK libraries automatically, potentially giving better performance for linear algebra operations. Use `conda` if you are in a conda environment; use `pip` otherwise.

---

**Exercise 4.** Import NumPy and create a simple array `[1, 2, 3]`. Print both the array and its type.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np

    arr = np.array([1, 2, 3])
    print(arr)        # [1 2 3]
    print(type(arr))  # <class 'numpy.ndarray'>
    ```

---

**Exercise 5.**
Create a `requirements.txt` file that pins NumPy to a specific version (e.g., `numpy==1.26.0`). Then write a Python script that reads this file, extracts the pinned NumPy version, and compares it to the currently installed version. Print whether they match.

??? success "Solution to Exercise 5"
    ```python
    import numpy as np

    # Simulate reading requirements.txt
    pinned = "1.26.0"  # In real code: parse from file
    installed = np.__version__

    print(f"Pinned:    {pinned}")
    print(f"Installed: {installed}")
    print(f"Match: {installed.startswith(pinned)}")

    # In practice, create a requirements.txt with:
    #   numpy==1.26.0
    # and install with:
    #   pip install -r requirements.txt
    ```

    Pinning versions ensures that every developer, CI server, and deployment machine uses the same NumPy version. Without pinning, `pip install numpy` installs the latest release, which may change behavior (e.g., `np.random.seed` vs `default_rng`, default integer dtype changes).
