# Axes Shape Behavior

Understanding how `plt.subplots` returns different shaped arrays is crucial for writing robust plotting code.

!!! tip "Mental Model"
    `plt.subplots(r, c)` returns axes shaped like the grid: a single object for 1x1, a 1D array for a single row or column, and a 2D array for multi-row, multi-column grids. Use `squeeze=False` to always get a 2D array, which makes indexing uniform and avoids shape-related bugs.

!!! warning "Why This Matters"
    Shape inconsistency is the **#1 source of subplot bugs.** Code that works
    for a 2x2 grid (`axes[0, 1]`) crashes on a 1x2 grid (`axes` is 1D, so
    `axes[0, 1]` raises `IndexError`). The fix: always pass `squeeze=False`
    in functions that accept variable grid sizes.

    ```text
    Rule of thumb:
    1 subplot     → ax (scalar)
    1 row/column  → axes[i] (1D array)
    Grid          → axes[i, j] (2D array)
    Need consistency → squeeze=False (always 2D)
    ```

---

## Single Axes

With no arguments or `(1, 1)`, a single Axes object is returned (not an array):

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
print(type(ax))  # <class 'matplotlib.axes._subplots.AxesSubplot'>

fig, ax = plt.subplots(1, 1)
print(type(ax))  # <class 'matplotlib.axes._subplots.AxesSubplot'>
```

---

## 1D Arrays (1×N or N×1)

When creating a single row or column, the result is a 1D array:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)

# 1 row, 2 columns -> shape (2,), not (1, 2)
fig, axes = plt.subplots(1, 2)
axes[0].plot(x, np.sin(x))
axes[1].plot(x, np.cos(x))
plt.show()

print(type(axes))   # numpy.ndarray
print(axes.shape)   # (2,)
print(axes.dtype)   # object
```

```python
# 2 rows, 1 column -> shape (2,), not (2, 1)
fig, axes = plt.subplots(2, 1)
axes[0].plot(x, np.sin(x))
axes[1].plot(x, np.cos(x))
plt.show()

print(axes.shape)   # (2,)
```

---

## 2D Arrays (N×M)

Only when both dimensions are greater than 1:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)

fig, axes = plt.subplots(2, 2)

axes[0, 0].plot(x, np.sin(x))
axes[0, 1].plot(x, np.cos(x))
axes[1, 0].plot(x, np.sinh(x))
axes[1, 1].plot(x, np.cosh(x))

plt.show()

print(type(axes))   # numpy.ndarray
print(axes.shape)   # (2, 2)
print(axes.dtype)   # object
```

---

## The squeeze Parameter

Use `squeeze=False` to always get a 2D array:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0.001, 1, 100)

# Without squeeze=False
fig, axs = plt.subplots(1, 3, figsize=(12, 3))
print(axs.shape)  # (3,)
axs[0].plot(x, x**2)
axs[1].plot(x, np.sin(x))
axs[2].plot(x, np.exp(x))

# With squeeze=False
fig, axs = plt.subplots(1, 3, figsize=(12, 3), squeeze=False)
print(axs.shape)  # (1, 3)
axs[0, 0].plot(x, x**2)
axs[0, 1].plot(x, np.sin(x))
axs[0, 2].plot(x, np.exp(x))

plt.tight_layout()
plt.show()
```

---

## Why Use squeeze=False?

Consistent array access is useful when:

1. **Looping over subplots**:
```python
fig, axes = plt.subplots(1, 3, squeeze=False)
for i in range(1):
    for j in range(3):
        axes[i, j].plot([1, 2, 3])
```

2. **Writing generic functions**:
```python
def setup_grid(nrows, ncols):
    fig, axes = plt.subplots(nrows, ncols, squeeze=False)
    # Always use axes[i, j] regardless of dimensions
    return fig, axes
```

---

## Shape Summary Table

| Subplots | Returns | Shape | Access |
|----------|---------|-------|--------|
| `plt.subplots()` | Axes | N/A | `ax` |
| `plt.subplots(1, 3)` | 1D array | `(3,)` | `axes[j]` |
| `plt.subplots(3, 1)` | 1D array | `(3,)` | `axes[i]` |
| `plt.subplots(2, 3)` | 2D array | `(2, 3)` | `axes[i, j]` |
| `plt.subplots(1, 3, squeeze=False)` | 2D array | `(1, 3)` | `axes[0, j]` |

---

## Practical Implications

Handle different cases in code:

```python
import matplotlib.pyplot as plt
import numpy as np

def plot_functions(funcs, figsize=(12, 3)):
    n = len(funcs)
    fig, axes = plt.subplots(1, n, figsize=figsize, squeeze=False)
    
    x = np.linspace(0, 2*np.pi, 100)
    
    for j, func in enumerate(funcs):
        axes[0, j].plot(x, func(x))
    
    plt.tight_layout()
    return fig, axes

# Works for any number of functions
plot_functions([np.sin, np.cos, np.tan])
plt.show()
```

---

## Key Takeaways

- Single axes returns an Axes object, not an array
- 1×N or N×1 returns a 1D array with shape `(N,)`
- N×M (both > 1) returns a 2D array with shape `(N, M)`
- Use `squeeze=False` for consistent 2D array access
- Handle shape variations when writing generic plotting functions

---

## Exercises

**Exercise 1.**
Call `plt.subplots()` with no arguments and print the type and shape of the returned axes object. Then call `plt.subplots(1, 3)` and print the type and shape. Finally call `plt.subplots(2, 3)` and print the type and shape. Explain the differences.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        fig1, ax1 = plt.subplots()
        print(f"No args: type={type(ax1)}, not an array")
        plt.close(fig1)

        fig2, ax2 = plt.subplots(1, 3)
        print(f"(1, 3): type={type(ax2)}, shape={ax2.shape}")
        plt.close(fig2)

        fig3, ax3 = plt.subplots(2, 3)
        print(f"(2, 3): type={type(ax3)}, shape={ax3.shape}")
        plt.close(fig3)

        # No args -> single Axes object
        # (1, 3) -> 1D array of shape (3,)
        # (2, 3) -> 2D array of shape (2, 3)

---

**Exercise 2.**
Create a 3x3 grid using `plt.subplots(3, 3)`. Use `axes.flat` to iterate over all 9 axes and plot `y = sin(n*x)` where `n` goes from 1 to 9. Title each subplot with the value of `n`.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 2 * np.pi, 200)

        fig, axes = plt.subplots(3, 3, figsize=(10, 10))
        for n, ax in enumerate(axes.flat, 1):
            ax.plot(x, np.sin(n * x))
            ax.set_title(f'n = {n}')

        plt.tight_layout()
        plt.show()

---

**Exercise 3.**
Create a 2x3 subplot grid with `squeeze=False` and verify the return shape is always 2D by printing `axes.shape`. Then access axes using 2D indexing `axes[row, col]` to plot different functions. Compare this with the default `squeeze=True` behavior for a 1x3 grid.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 2 * np.pi, 200)

        # With squeeze=False, always 2D
        fig, axes = plt.subplots(2, 3, squeeze=False, figsize=(12, 6))
        print(f"squeeze=False, (2,3): shape={axes.shape}")

        funcs = [np.sin, np.cos, np.tan, np.exp, np.log1p, np.sqrt]
        names = ['sin', 'cos', 'tan', 'exp', 'log1p', 'sqrt']

        for i in range(2):
            for j in range(3):
                idx = i * 3 + j
                axes[i, j].plot(x, funcs[idx](x))
                axes[i, j].set_title(names[idx])

        plt.tight_layout()
        plt.show()

        # Compare with squeeze=True (default) for 1x3
        fig2, axes2 = plt.subplots(1, 3, squeeze=True)
        print(f"squeeze=True, (1,3): shape={axes2.shape}")  # (3,) not (1,3)

        fig3, axes3 = plt.subplots(1, 3, squeeze=False)
        print(f"squeeze=False, (1,3): shape={axes3.shape}")  # (1,3)
        plt.close('all')
