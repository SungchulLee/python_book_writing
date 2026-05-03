# plt.subplot vs plt.subplots

Understanding the difference between `plt.subplot` (singular) and `plt.subplots` (plural) is essential for effective Matplotlib usage.

!!! tip "Mental Model"
    `plt.subplot` (singular, no "s") is the old MATLAB-style way -- you specify one subplot at a time using a 3-digit code. `plt.subplots` (plural, with "s") is the modern way -- it creates the entire grid at once and hands you back all the Axes in an array. Prefer `plt.subplots` for cleaner, more Pythonic code.

---

## plt.subplot (MATLAB Style)

`plt.subplot` creates a single subplot in a grid layout:

```python
import matplotlib.pyplot as plt

plt.subplot(2, 2, 1)  # Create the first subplot in a 2x2 grid
plt.plot([1, 2, 3, 4])

plt.subplot(2, 2, 2)  # Create the second subplot
plt.plot([4, 3, 2, 1])

plt.subplot(2, 2, 3)  # Create the third subplot
plt.plot([1, 1, 1, 1])

plt.subplot(2, 2, 4)  # Create the fourth subplot
plt.plot([1, 2, 1, 2])

plt.show()
```

**Syntax**: `plt.subplot(nrows, ncols, index)`

- Index starts at 1 (not 0)
- Counts left-to-right, top-to-bottom

---

## plt.subplots (OOP Style)

`plt.subplots` creates a Figure and all Axes objects at once:

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(4, 4))

axes[0, 0].plot([1, 2, 3, 4])
axes[0, 1].plot([4, 3, 2, 1])
axes[1, 0].plot([1, 1, 1, 1])
axes[1, 1].plot([1, 2, 1, 2])

plt.show()

print(type(axes))   # numpy.ndarray
print(axes.shape)   # (2, 2)
print(axes.dtype)   # object
```

**Returns**: A Figure object and a NumPy array of Axes objects.

---

## Unpacking Axes

You can unpack the axes array for cleaner code:

```python
import matplotlib.pyplot as plt

fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2, figsize=(4, 4))

ax0.plot([1, 2, 3, 4])
ax1.plot([4, 3, 2, 1])
ax2.plot([1, 1, 1, 1])
ax3.plot([1, 2, 1, 2])

plt.show()
```

---

## Axes Shape Behavior

The returned axes array shape depends on the grid dimensions:

```python
# Single axes returns an Axes object, not an array
fig, ax = plt.subplots()
print(type(ax))  # AxesSubplot

# 1xN or Nx1 returns a 1D array
fig, axes = plt.subplots(1, 3)
print(axes.shape)  # (3,)

# NxM returns a 2D array
fig, axes = plt.subplots(2, 3)
print(axes.shape)  # (2, 3)
```

---

## The squeeze Keyword

Use `squeeze=False` to always get a 2D array:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0.001, 1, 100)

# Without squeeze=False: shape is (3,)
fig, axs = plt.subplots(1, 3, figsize=(12, 3))
axs[0].plot(x, x**2)
axs[1].plot(x, np.sin(x))
axs[2].plot(x, np.exp(x))

# With squeeze=False: shape is (1, 3)
fig, axs = plt.subplots(1, 3, figsize=(12, 3), squeeze=False)
axs[0, 0].plot(x, x**2)
axs[0, 1].plot(x, np.sin(x))
axs[0, 2].plot(x, np.exp(x))

plt.tight_layout()
plt.show()
```

---

## Comparison Summary

| Feature | plt.subplot | plt.subplots |
|---------|-------------|--------------|
| Style | MATLAB | OOP |
| Returns | Axes | (Figure, Axes array) |
| Index starts at | 1 | 0 |
| Creates | One axes at a time | All axes at once |
| Flexibility | Limited | High |

---

!!! tip "Decision Rule"
    **Always use `plt.subplots()` unless you have a very specific reason not to.** It returns both the Figure and all Axes at once, supports the OOP interface, and integrates cleanly with `tight_layout()`, `savefig()`, and every other Figure method. The only time `plt.subplot()` makes sense is quick interactive one-liners in the REPL.

## Key Takeaways

- `plt.subplot`: singular, MATLAB style, 1-based indexing
- `plt.subplots`: plural, OOP style, returns Figure and Axes array
- Use `plt.subplots` for new code
- Use `squeeze=False` for consistent array shapes


---

## Exercises

**Exercise 1.** Write the same 2x2 subplot figure using both `plt.subplot()` (singular) and `plt.subplots()` (plural). Plot `sin`, `cos`, `tan`, and `exp` respectively. Which approach requires fewer lines of code?

??? success "Solution to Exercise 1"
        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 2 * np.pi, 100)
        funcs = [np.sin, np.cos, np.tan, np.exp]
        titles = ['sin', 'cos', 'tan', 'exp']

        # --- plt.subplot (singular) ---
        plt.figure(figsize=(8, 6))
        for i, (f, t) in enumerate(zip(funcs, titles), start=1):
            plt.subplot(2, 2, i)
            plt.plot(x, f(x))
            plt.title(t)
        plt.tight_layout()
        plt.show()

        # --- plt.subplots (plural) ---
        fig, axes = plt.subplots(2, 2, figsize=(8, 6))
        for ax, f, t in zip(axes.flat, funcs, titles):
            ax.plot(x, f(x))
            ax.set_title(t)
        plt.tight_layout()
        plt.show()

        # plt.subplots is more concise: one creation call + flat iteration.

---

**Exercise 2.** Explain the difference between `plt.subplot(nrows, ncols, index)` and `plt.subplots(nrows, ncols)`. What does each return?

??? success "Solution to Exercise 2"
    `plt.subplot(nrows, ncols, index)` creates **one Axes** at the given position in the grid and returns that single Axes object. You call it repeatedly to build up a figure.

    `plt.subplots(nrows, ncols)` creates the **entire grid at once** and returns a tuple `(fig, axes)` where `fig` is the Figure object and `axes` is a NumPy array of all Axes objects. For a 1x1 grid, `axes` is a single Axes (not an array); for 1xN or Nx1, it is a 1D array; for NxM, it is a 2D array.

---

**Exercise 3.** Write code that creates a 2x2 figure with `plt.subplots(2, 2)` and iterates over `axes.flat` to plot `y = x**n` for `n = 1, 2, 3, 4`.

??? success "Solution to Exercise 3"
        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 3, 50)
        fig, axes = plt.subplots(2, 2, figsize=(8, 6))

        for n, ax in enumerate(axes.flat, start=1):
            ax.plot(x, x**n)
            ax.set_title(f'y = x^{n}')
            ax.grid(True)

        plt.tight_layout()
        plt.show()

---

**Exercise 4.** Demonstrate that `plt.subplot(2, 2, 1)` and `plt.subplot(221)` are equivalent calls by creating two figures and verifying both produce the same grid position.

??? success "Solution to Exercise 4"
        import matplotlib.pyplot as plt

        # Three-argument form
        fig1 = plt.figure()
        ax1 = plt.subplot(2, 2, 1)
        ax1.set_title('subplot(2, 2, 1)')
        print(f"Position (3-arg): {ax1.get_geometry()}")

        # Compact integer form
        fig2 = plt.figure()
        ax2 = plt.subplot(221)
        ax2.set_title('subplot(221)')
        print(f"Position (int):   {ax2.get_geometry()}")

        # Both produce (2, 2, 1) — same grid position
        plt.show()
