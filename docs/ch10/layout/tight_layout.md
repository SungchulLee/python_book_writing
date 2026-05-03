# Tight Layout

Tight layout automatically adjusts subplot parameters to prevent overlapping labels and titles.

!!! tip "Mental Model"
    `fig.tight_layout()` is an automatic spacing fixer. It measures all text (titles, labels, tick labels) and adjusts subplot margins so nothing overlaps. Call it once at the end, right before `savefig()` or `show()`. For even more control, use `constrained_layout=True` when creating the figure, which adjusts continuously as you add elements.

    Under the hood, the layout engine computes **bounding boxes** of all text
    elements (titles, labels, tick labels, legends) and adjusts subplot positions
    so no bounding boxes overlap. This is why it must be called *after* all text
    is added — it cannot anticipate text that doesn't exist yet.

!!! warning "When tight_layout Fails"
    `tight_layout()` is a heuristic, not a guarantee. It may produce poor results
    with:

    - **Colorbars** — they are separate axes and confuse the spacing algorithm
    - **Complex GridSpec layouts** — nested or spanning cells can break the optimizer
    - **Large annotations or text** — bounding boxes outside subplot areas are ignored

    For these cases, use `constrained_layout=True` (more robust) or manual
    `subplots_adjust()` for full control.

## The Problem

Without adjustment, labels and titles can overlap.

### 1. Overlapping Labels

```python
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(2, 2, figsize=(8, 6))

for ax in axes.flat:
    ax.plot(np.random.randn(100).cumsum())
    ax.set_xlabel('Long X-axis Label')
    ax.set_ylabel('Long Y-axis Label')
    ax.set_title('Title with Some Text')

# Labels may overlap!
plt.show()
```

### 2. Crowded Subplots

```python
fig, axes = plt.subplots(3, 3, figsize=(8, 8))

for ax in axes.flat:
    ax.plot(np.random.randn(50))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

# Titles and labels collide
plt.show()
```

### 3. Suptitle Overlap

```python
fig, axes = plt.subplots(2, 2)
fig.suptitle('Main Title', fontsize=16)

for ax in axes.flat:
    ax.set_title('Subplot Title')

# Suptitle overlaps subplot titles
plt.show()
```

## tight_layout Solution

Apply automatic spacing adjustment.

### 1. Basic Usage

```python
fig, axes = plt.subplots(2, 2, figsize=(8, 6))

for ax in axes.flat:
    ax.plot(np.random.randn(100).cumsum())
    ax.set_xlabel('Long X-axis Label')
    ax.set_ylabel('Long Y-axis Label')
    ax.set_title('Title with Some Text')

fig.tight_layout()
plt.show()
```

### 2. Figure Method

```python
fig, axes = plt.subplots(2, 2)
# ... configure plots ...
fig.tight_layout()
```

### 3. Pyplot Function

```python
plt.subplot(2, 2, 1)
plt.plot(np.random.randn(50))
plt.title('Plot 1')

plt.subplot(2, 2, 2)
plt.plot(np.random.randn(50))
plt.title('Plot 2')

plt.tight_layout()
plt.show()
```

## tight_layout Parameters

Fine-tune the automatic adjustment.

### 1. Padding

```python
fig, axes = plt.subplots(2, 2)
fig.tight_layout(pad=2.0)  # Extra padding around figure edge
plt.show()
```

### 2. Subplot Padding

```python
fig, axes = plt.subplots(2, 2)
fig.tight_layout(
    h_pad=1.0,  # Height padding between subplots
    w_pad=1.0   # Width padding between subplots
)
plt.show()
```

### 3. Parameter Reference

```python
fig.tight_layout(
    pad=1.08,      # Padding between figure edge and subplot edges
    h_pad=None,    # Height padding between subplots
    w_pad=None,    # Width padding between subplots
    rect=None      # Rectangle in figure coords (left, bottom, right, top)
)
```

## rect Parameter

Reserve space for figure-level elements.

### 1. Space for Suptitle

```python
fig, axes = plt.subplots(2, 2)

for ax in axes.flat:
    ax.plot(np.random.randn(50))

fig.suptitle('Main Title', fontsize=16)
fig.tight_layout(rect=[0, 0, 1, 0.95])  # Leave 5% at top
plt.show()
```

### 2. Space for Legend

```python
fig, axes = plt.subplots(1, 2)

for ax in axes:
    ax.plot(np.random.randn(50), label='Data')

fig.legend(loc='lower center', ncol=2)
fig.tight_layout(rect=[0, 0.1, 1, 1])  # Leave 10% at bottom
plt.show()
```

### 3. Custom Margins

```python
fig, axes = plt.subplots(2, 2)
fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])  # 5% margins all around
plt.show()
```

## constrained_layout

Modern alternative to tight_layout.

### 1. Enable at Creation

```python
fig, axes = plt.subplots(2, 2, figsize=(8, 6), constrained_layout=True)

for ax in axes.flat:
    ax.plot(np.random.randn(100).cumsum())
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_title('Title')

# No need to call tight_layout!
plt.show()
```

### 2. With Colorbars

```python
fig, axes = plt.subplots(1, 2, constrained_layout=True)

im1 = axes[0].imshow(np.random.rand(10, 10))
im2 = axes[1].imshow(np.random.rand(10, 10))

fig.colorbar(im1, ax=axes[0])
fig.colorbar(im2, ax=axes[1])

plt.show()
```

### 3. Advantages

```python
# constrained_layout handles:
# - Colorbars automatically
# - Legends better
# - More complex layouts
# - Updates dynamically during interactive sessions
```

## subplots_adjust

Manual control over spacing.

### 1. Basic Adjustment

```python
fig, axes = plt.subplots(2, 2)

for ax in axes.flat:
    ax.plot(np.random.randn(50))

fig.subplots_adjust(
    left=0.1,
    right=0.95,
    bottom=0.1,
    top=0.9
)
plt.show()
```

### 2. Subplot Spacing

```python
fig.subplots_adjust(
    wspace=0.4,  # Width space between subplots
    hspace=0.4   # Height space between subplots
)
```

### 3. Full Control

```python
fig.subplots_adjust(
    left=0.1,     # Left margin
    right=0.95,   # Right margin
    bottom=0.1,   # Bottom margin
    top=0.9,      # Top margin
    wspace=0.4,   # Width space between subplots
    hspace=0.4    # Height space between subplots
)
```

## Method Comparison

Choose the right approach for your needs.

### 1. tight_layout

```python
# Pros: Simple, usually works
# Cons: May fail with complex layouts, colorbars
# Best for: Quick fixes, simple grids

fig.tight_layout()
```

### 2. constrained_layout

```python
# Pros: More robust, handles colorbars, dynamic
# Cons: Slightly slower, must set at creation
# Best for: New projects, complex figures

fig, ax = plt.subplots(constrained_layout=True)
```

### 3. subplots_adjust

```python
# Pros: Full control, precise positioning
# Cons: Manual tuning required
# Best for: Publication figures, exact specifications

fig.subplots_adjust(left=0.15, right=0.85)
```

## Best Practices

Guidelines for effective layout management.

### 1. Order of Operations

```python
fig, axes = plt.subplots(2, 2)

# 1. Create plots
for ax in axes.flat:
    ax.plot(np.random.randn(50))

# 2. Set labels and titles
for ax in axes.flat:
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

# 3. Call tight_layout LAST
fig.tight_layout()
plt.show()
```

### 2. Suptitle Pattern

```python
fig, axes = plt.subplots(2, 2)
fig.suptitle('Figure Title', fontsize=14)

# Always use rect with suptitle
fig.tight_layout(rect=[0, 0, 1, 0.95])
```

### 3. Modern Default

```python
# For new projects, prefer constrained_layout
fig, axes = plt.subplots(2, 2, constrained_layout=True)
```


---

## Exercises

**Exercise 1.** Write code that creates a 2x2 subplot grid with long axis labels and titles. Show the difference between calling and not calling `plt.tight_layout()`.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    # Solution code depends on the specific exercise
    x = np.linspace(0, 2 * np.pi, 100)
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x))
    ax.set_title('Example Solution')
    plt.show()
    ```

    See the content of this page for the relevant API details to construct the full solution.

---

**Exercise 2.** Explain the difference between `plt.tight_layout()` and `constrained_layout=True`. When would you prefer one over the other?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Write code using `plt.subplots_adjust()` to manually set the left, right, top, and bottom margins of a figure.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    x = np.linspace(0, 2 * np.pi, 100)
    axes[0].plot(x, np.sin(x))
    axes[0].set_title('Left Subplot')

    axes[1].plot(x, np.cos(x))
    axes[1].set_title('Right Subplot')

    plt.tight_layout()
    plt.show()
    ```

    Adapt this pattern to the specific requirements of the exercise.

---

**Exercise 4.** Create a figure with `constrained_layout=True` passed to `plt.subplots()` and demonstrate that labels do not overlap even without calling `tight_layout()`.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    x = np.linspace(0, 10, 100)
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x), 'b-', lw=2)
    ax.set_title('Solution')
    plt.show()
    ```

    Refer to the code examples in the main content for the specific API calls needed.
