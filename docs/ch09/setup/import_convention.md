# Import Convention

!!! note "Computational Environment Model"
    Reliable numerical computing requires three things:

    1. **A consistent environment** — [installation](installation.md) with pinned versions
    2. **A standard interface** — import conventions (this page)
    3. **A known version** — [version checking](version_check.md) for compatibility

    Together these ensure reproducibility, portability, and correctness. This section
    is not just setup — it is the foundation for every computation in this book.

    The governing law: **Result = f(code, data, environment).** A numerical result
    is only reproducible when all three inputs are controlled. The code is what you
    write; the data is what you feed in; the environment is the library version,
    platform, and runtime that execute it.

!!! tip "Mental Model"
    `import numpy as np` is the universally accepted convention — virtually every NumPy tutorial, library, and codebase uses it. The `np` alias gives you a **namespace for numerical computation**: every function behind `np.` is a NumPy operation, making code self-documenting. Never use `from numpy import *`, which pollutes your namespace and hides where functions come from.

    This is not merely a style convention — it is **interface design for
    computation.** The import statement defines the boundary through which you
    access numerical operations. A consistent namespace (`np`) ensures that every
    operation is explicitly tied to NumPy, making code readable, auditable, and
    unambiguous when multiple libraries coexist (e.g., `np.sum` vs `math.sum` vs
    built-in `sum`).

## Standard Import

### 1. The np Alias

NumPy is conventionally imported with the alias `np`.

```python
import numpy as np
```

This is the universal standard across the Python scientific computing community.

### 2. Why np

The alias provides several benefits:

- **Brevity**: `np.array()` vs `numpy.array()`
- **Readability**: Instantly recognizable
- **Convention**: Expected in all codebases

### 3. Community Standard

Using `np` signals familiarity with best practices.

```python
import numpy as np

def main():
    # Immediately recognizable as NumPy
    a = np.array([1, 2, 3])
    b = np.zeros((3, 3))
    c = np.linspace(0, 1, 10)

if __name__ == "__main__":
    main()
```

## Alternative Imports

### 1. Full Name Import

Possible but not recommended.

```python
import numpy

def main():
    # Verbose
    a = numpy.array([1, 2, 3])

if __name__ == "__main__":
    main()
```

### 2. Selective Import

Import specific functions directly.

```python
from numpy import array, zeros, linspace

def main():
    a = array([1, 2, 3])
    b = zeros((3, 3))
    c = linspace(0, 1, 10)

if __name__ == "__main__":
    main()
```

### 3. Star Import

Avoid this—pollutes namespace.

```python
# NOT recommended
from numpy import *

def main():
    # Unclear where functions come from
    a = array([1, 2, 3])  # numpy or builtin?

if __name__ == "__main__":
    main()
```

## Related Libraries

### 1. Common Pattern

Scientific Python libraries follow similar conventions.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

### 2. Full Stack Import

Typical scientific computing imports.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def main():
    data = np.random.randn(100)
    df = pd.DataFrame({'values': data})
    print(stats.describe(data))

if __name__ == "__main__":
    main()
```

### 3. Type Hints Import

For type annotations.

```python
import numpy as np
from numpy.typing import NDArray

def normalize(arr: NDArray[np.float64]) -> NDArray[np.float64]:
    return arr / arr.sum()

def main():
    a = np.array([1.0, 2.0, 3.0])
    result = normalize(a)
    print(result)

if __name__ == "__main__":
    main()
```


---

## Exercises

**Exercise 1.** What is the standard convention for importing NumPy? Write the import statement and explain why the alias `np` is used.

??? success "Solution to Exercise 1"
    ```python
    import numpy as np
    ```

    The alias `np` is a universally recognized convention that keeps code concise while making it clear that NumPy functions are being used. Nearly all NumPy documentation, tutorials, and codebases use this convention.

---

**Exercise 2.** Predict the output:

```python
import numpy as np
a = np.arange(5)
print(a)
print(type(a))
```

??? success "Solution to Exercise 2"
    ```
    [0 1 2 3 4]
    <class 'numpy.ndarray'>
    ```

---

**Exercise 3.** Some code uses `from numpy import array, zeros, ones`. Explain why this is less preferred than `import numpy as np` in most projects.

??? success "Solution to Exercise 3"
    Importing specific names (`from numpy import array`) pollutes the namespace and makes it unclear where functions come from. With `np.array`, readers immediately know it is a NumPy function. It also avoids name collisions with built-in `array` or other libraries.

---

**Exercise 4.** Write a one-liner using the `np` convention that creates a 3x3 identity matrix and prints it.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    print(np.eye(3))
    ```

---

**Exercise 5.**
A colleague's script begins with `from numpy import array, zeros, linspace, mean, std, random`. It works, but later they add `from statistics import mean` for a different purpose and the script breaks silently. Explain the bug and how `import numpy as np` prevents it.

??? success "Solution to Exercise 5"
    Both `numpy` and `statistics` export a function called `mean`. When both are imported with `from ... import mean`, the second import shadows the first — `mean` now refers to `statistics.mean`, not `numpy.mean`. NumPy's `mean` accepts arrays and axis parameters; `statistics.mean` does not. The script may raise errors or silently compute wrong results.

    With the `np` convention, there is no ambiguity:

    ```python
    import numpy as np
    from statistics import mean

    np.mean(arr)   # NumPy mean — clear
    mean(values)   # statistics mean — clear
    ```

    Namespaced imports eliminate name collisions entirely. This is the primary reason `import numpy as np` is preferred over selective imports.
