# OOP vs Pyplot Style

Matplotlib supports two plotting interfaces: the pyplot (MATLAB-style) interface and the object-oriented (OOP) interface. Understanding both is essential for effective visualization.

!!! tip "Mental Model"
    Pyplot is like a TV remote -- you press buttons and the current channel changes behind the scenes. The OOP interface is like holding the TV object directly -- you call methods on a specific Figure and specific Axes, so there is never ambiguity about which plot you are modifying. Use pyplot for quick exploration; switch to OOP for **everything else.**

    The difference is not stylistic — it is **conceptual.** Pyplot tells
    Matplotlib what to do (a sequence of commands). OOP gives you objects that
    represent parts of the visualization (Figure, Axes, Artists). This means
    your code mirrors the structure of the visualization itself:

    ```text
    fig   → the whole message
    ax    → one perspective on the data
    lines → visual elements inside that perspective
    ```

    Using OOP is not just "better practice" — it is a way to **think about
    visualizations as structured objects**, which is essential for building
    complex, readable, and correct plots.

!!! note "The State Machine Under Pyplot"
    Pyplot maintains a **global stack** of figures and axes. Every `plt.*` call
    implicitly targets the figure and axes at the top of this stack. `plt.subplot()`
    pushes a new axes onto the stack and makes it "current." This is why bugs like
    the following are common:

    ```python
    plt.subplot(1, 2, 1)
    plt.plot(x1)

    plt.subplot(1, 2, 2)
    plt.plot(x2)

    plt.title("Oops")  # Applies to subplot 2, not subplot 1!
    ```

    The implicit state makes it **fragile and error-prone**, not impossible. The OOP
    style avoids this entirely because every call names its target explicitly
    (`ax1.set_title(...)`).

---

## Two Paradigms

### Pyplot Style (Implicit State)

The pyplot style uses `plt` functions that operate on the "current" figure and axes:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)

plt.figure(figsize=(10, 3))

plt.subplot(121)
plt.plot(x, np.sin(x))
plt.title("sin")
plt.xlabel("x")

plt.subplot(122)
plt.plot(x, np.cos(x))
plt.title("cos")
plt.xlabel("x")

plt.tight_layout()
plt.show()
```

Pyplot maintains a state machine with "current" figure and axes:

```python
plt.plot([1, 2, 3])   # Acts on current axes
plt.title('Title')    # Acts on current axes
```

**Limitation**: Pyplot's implicit state makes it **fragile and confusing** to manage
multiple subplots — modifying a previous subplot requires switching the "current"
axes back, which is error-prone and hard to read.

---

### OOP Style (Explicit References)

The OOP style explicitly creates and references Figure and Axes objects:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)

fig, axes = plt.subplots(1, 2, figsize=(10, 3))

axes[0].plot(x, np.sin(x))
axes[0].set_title("sin")
axes[0].set_xlabel("x")

axes[1].plot(x, np.cos(x))
axes[1].set_title("cos")
axes[1].set_xlabel("x")

# Can go back and modify any axes at any time
axes[0].set_ylabel("amplitude")

plt.tight_layout()
plt.show()
```

**Advantage**: Full control over each axes object at any point in your code.

---

## Method Name Differences

When switching from pyplot to OOP style, method names change (add `set_` prefix):

| Pyplot Style | OOP Style |
|--------------|-----------|
| `plt.title()` | `ax.set_title()` |
| `plt.xlabel()` | `ax.set_xlabel()` |
| `plt.ylabel()` | `ax.set_ylabel()` |
| `plt.xlim()` | `ax.set_xlim()` |
| `plt.ylim()` | `ax.set_ylim()` |
| `plt.xticks()` | `ax.set_xticks()` |
| `plt.yticks()` | `ax.set_yticks()` |
| `plt.legend()` | `ax.legend()` |
| `plt.grid()` | `ax.grid()` |

---

## When to Use Each

### Pyplot Style

Best for:
- Quick exploratory plots
- Simple single-axis figures
- Interactive REPL/notebook sessions
- MATLAB users transitioning to Python

```python
# Quick exploration
plt.plot([1, 2, 3], [1, 4, 9])
plt.show()
```

### OOP Style

Best for:
- Complex multi-panel figures
- Production-quality visualizations
- Reusable plotting functions
- GUI integration
- When you need to modify axes after creation

```python
def plot_data(ax, data, title):
    """Reusable plotting function."""
    ax.plot(data)
    ax.set_title(title)
    ax.grid(True)
    return ax

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
plot_data(ax1, [1, 2, 3], "Dataset A")
plot_data(ax2, [3, 2, 1], "Dataset B")
plt.show()
```

---

## Mixing Styles (Caution)

You can mix styles, but it can lead to confusion:

```python
fig, ax = plt.subplots()     # OOP: create figure and axes
ax.plot([1, 2, 3])           # OOP: plot on axes
plt.title('Title')           # Pyplot: acts on "current" axes
plt.show()                   # Pyplot: display
```

This works because `plt.subplots()` sets the created axes as "current", but mixing styles makes code harder to follow.

---

## Best Practices

### 1. Prefer OOP for Functions

```python
# ✓ GOOD - Explicit axes parameter
def make_plot(ax, data):
    ax.plot(data)
    ax.set_title('Data')
    return ax

# ✗ BAD - Relies on implicit state
def make_plot(data):
    plt.plot(data)  # Which figure? Which axes?
    plt.title('Data')
```

### 2. Return Figure Objects

```python
def create_figure(data):
    """Create and return figure for caller to display."""
    fig, ax = plt.subplots()
    ax.plot(data)
    ax.set_title('Results')
    return fig  # Caller controls when to display

# Usage
fig = create_figure([1, 2, 3])
fig.savefig('plot.png')  # Save
plt.show()               # Display
```

### 3. Avoid plt.show() Inside Functions

```python
# ✓ GOOD - Let caller decide when to show
def plot_results(ax, results):
    ax.bar(range(len(results)), results)
    ax.set_xlabel('Index')
    # No plt.show() here

# ✗ BAD - Blocks execution and closes figure
def plot_results(results):
    plt.bar(range(len(results)), results)
    plt.show()  # Can't save or modify after this
```

### 4. Use Consistent Style

```python
# ✓ GOOD - All OOP
fig, axes = plt.subplots(2, 2)
for ax in axes.flat:
    ax.plot([1, 2, 3])
    ax.set_title('Plot')
fig.suptitle('Main Title')
plt.tight_layout()
plt.show()

# ✗ AVOID - Mixed styles
plt.figure()
ax = plt.subplot(221)
ax.plot([1, 2, 3])
plt.title('Plot')  # Mixing styles
```

---

## Quick Reference

```python
# Pyplot style
plt.figure(figsize=(8, 6))
plt.plot(x, y)
plt.title('Title')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.savefig('plot.png')
plt.show()

# OOP style
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x, y)
ax.set_title('Title')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.legend()
fig.savefig('plot.png')
plt.show()
```

---

## Summary

| Aspect | Pyplot Style | OOP Style |
|--------|--------------|-----------|
| State | Implicit (current axes) | Explicit (ax reference) |
| Control | Limited | Full |
| Multi-panel | Awkward | Natural |
| Reusability | Poor | Excellent |
| Best for | Quick plots | Production code |

**Key Takeaways**:

- Pyplot maintains implicit "current" figure/axes state
- OOP style uses explicit `fig` and `ax` references
- Method names add `set_` prefix in OOP style
- **Prefer OOP style** for anything beyond simple exploratory plots
- Return figure objects from functions; let caller handle display
- Avoid mixing styles in the same codebase

!!! tip "Design Philosophy"
    The OOP vs pyplot choice reflects a universal programming principle:

    ```text
    Explicit > implicit
    Local control > global state
    Composable functions > side effects
    ```

    OOP-style plotting follows all three: you name every target, control every
    axes locally, and compose plots from functions that return figure objects.
    This is why it scales to complex dashboards and production code while pyplot
    does not.

    **Cognitive load:** implicit state forces you to remember which figure and
    axes are "current" — a mental burden that grows with plot complexity.
    Explicit objects remove that burden entirely. This is why OOP scales and
    pyplot doesn't: the code tells you what it modifies, so you don't have to.

    **Mixing styles breaks the model:** once you hold explicit `ax` references,
    calling `plt.title()` silently targets a different axes than you think.
    You lose track of which object is being modified, defeating the purpose of
    OOP entirely. Pick one style per script and commit to it.

---

## Runnable Example: `plotting_styles_tutorial.py`

```python
"""
Matplotlib Tutorial - Beginner Level
=====================================
Topic: Two Plotting Styles - MATLAB Style vs Object-Oriented Style
Author: Educational Python Course
Level: Beginner

Learning Objectives:
-------------------
1. Understand the difference between MATLAB-style and OOP-style
2. Learn when to use each style
3. Understand the concept of Figure and Axes objects
4. Create simple plots using both styles
5. Recognize the advantages of each approach

Prerequisites:
-------------
- Completion of 01_introduction_and_first_plot.py
- Basic understanding of object-oriented programming concepts
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# SECTION 1: Introduction to Two Plotting Styles
# ============================================================================

if __name__ == "__main__":

    """
    Matplotlib provides TWO different interfaces for creating plots:

    1. MATLAB-Style (Pyplot Interface)
       - Uses plt.plot(), plt.xlabel(), plt.title(), etc.
       - Simpler and more intuitive for beginners
       - Good for quick, simple plots
       - Similar to MATLAB's plotting commands
       - Implicitly works on the "current" figure and axes

    2. Object-Oriented Style (OO Interface)
       - Uses explicit Figure and Axes objects
       - More verbose but more powerful
       - Better for complex plots with multiple subplots
       - Recommended for more control and clarity
       - Explicitly specify which axes to work with

    IMPORTANT: Both styles produce the same results, but OOP style gives you
    more control and is better for complex visualizations.
    """

    # ============================================================================
    # SECTION 2: MATLAB-Style Plotting (Pyplot Interface)
    # ============================================================================

    print("=" * 70)
    print("MATLAB-STYLE PLOTTING")
    print("=" * 70)

    # Generate data
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # MATLAB-style: Use plt.* functions directly
    # These functions operate on the "current" figure and axes
    plt.figure()  # Create a new figure (optional, but explicit)
    plt.plot(x, y)
    plt.xlabel('x')
    plt.ylabel('sin(x)')
    plt.title('MATLAB-Style Plot')
    plt.grid(True)
    plt.show()

    """
    What's happening behind the scenes:
    - plt.plot() automatically creates a figure and axes if they don't exist
    - plt.xlabel() adds a label to the current axes
    - All plt.* functions work on the "current" active figure/axes
    - This is convenient for simple plots but can be confusing with multiple plots
    """

    # ============================================================================
    # SECTION 3: Object-Oriented Style (OOP Interface)
    # ============================================================================

    print("=" * 70)
    print("OBJECT-ORIENTED STYLE PLOTTING")
    print("=" * 70)

    # Generate data
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # OOP-style: Create explicit Figure and Axes objects
    # fig is the entire window or page
    # ax is a single plot area within the figure
    fig, ax = plt.subplots()

    # Now we call methods on the axes object (ax)
    # Notice: ax.plot() instead of plt.plot()
    ax.plot(x, y)
    ax.set_xlabel('x')  # Note: set_xlabel, not xlabel
    ax.set_ylabel('sin(x)')  # Note: set_ylabel, not ylabel
    ax.set_title('Object-Oriented Style Plot')  # Note: set_title, not title
    ax.grid(True)

    plt.show()

    """
    What's different:
    - We explicitly create fig and ax objects using plt.subplots()
    - We call methods on ax (the axes object), not plt
    - Method names have 'set_' prefix: set_xlabel, set_ylabel, set_title
    - This gives us explicit control over which axes we're modifying
    """

    # ============================================================================
    # SECTION 4: Method Name Differences - IMPORTANT!
    # ============================================================================

    """
    CRITICAL: Method names change between MATLAB-style and OOP-style!

    MATLAB-Style (plt.*)          |  OOP-Style (ax.*)
    ------------------------------|----------------------------------
    plt.xlabel()                  |  ax.set_xlabel()
    plt.ylabel()                  |  ax.set_ylabel()
    plt.title()                   |  ax.set_title()
    plt.xlim()                    |  ax.set_xlim()
    plt.ylim()                    |  ax.set_ylim()
    plt.xticks()                  |  ax.set_xticks()
    plt.yticks()                  |  ax.set_yticks()
    plt.legend()                  |  ax.legend() (same name!)
    plt.grid()                    |  ax.grid() (same name!)
    plt.plot()                    |  ax.plot() (same name!)

    Rule of Thumb:
    - In OOP-style, most "setting" functions add a 'set_' prefix
    - Some functions keep the same name (plot, legend, grid, etc.)
    """

    # ============================================================================
    # SECTION 5: Side-by-Side Comparison
    # ============================================================================

    print("=" * 70)
    print("SIDE-BY-SIDE COMPARISON")
    print("=" * 70)

    x = np.linspace(0, 10, 100)
    y = np.cos(x)

    # --------------------
    # MATLAB-Style
    # --------------------
    plt.figure(figsize=(6, 4))  # figsize in inches (width, height)
    plt.plot(x, y, 'b-', linewidth=2)
    plt.xlabel('x')
    plt.ylabel('cos(x)')
    plt.title('MATLAB-Style: Cosine Function')
    plt.grid(True, alpha=0.3)  # alpha controls transparency
    plt.xlim(0, 10)  # Set x-axis limits
    plt.ylim(-1.5, 1.5)  # Set y-axis limits
    plt.show()

    # --------------------
    # OOP-Style (Equivalent)
    # --------------------
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, y, 'b-', linewidth=2)
    ax.set_xlabel('x')
    ax.set_ylabel('cos(x)')
    ax.set_title('OOP-Style: Cosine Function')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 10)
    ax.set_ylim(-1.5, 1.5)
    plt.show()

    # Both produce identical results!

    # ============================================================================
    # SECTION 6: Understanding Figure and Axes Objects
    # ============================================================================

    """
    Key Concepts:
    ------------

    Figure (fig):
    - The entire window or page that contains your plot(s)
    - Can contain one or more Axes
    - Controls overall properties: size, DPI, background color
    - Think of it as the canvas

    Axes (ax):
    - A single plot area within the Figure
    - Contains the actual plot elements: lines, labels, ticks, etc.
    - A Figure can have multiple Axes (subplots)
    - Think of it as the drawing on the canvas

    Hierarchy:
      Figure (the whole window)
        └── Axes (individual plot area)
              └── Plot elements (lines, markers, text, etc.)
    """

    # Create a figure and axes explicitly
    fig, ax = plt.subplots()

    print(f"Type of fig: {type(fig)}")  # matplotlib.figure.Figure
    print(f"Type of ax: {type(ax)}")    # matplotlib.axes._subplots.AxesSubplot

    # You can access the figure from axes
    print(f"ax.figure is fig: {ax.figure is fig}")  # True

    # Plot something
    x = np.linspace(0, 5, 50)
    ax.plot(x, x**2, 'r-')
    ax.set_title('Understanding Figure and Axes')

    plt.show()

    # ============================================================================
    # SECTION 7: When to Use Each Style
    # ============================================================================

    """
    Use MATLAB-Style when:
    ---------------------
    1. Creating quick, simple plots for exploration
    2. You only need one plot
    3. You're familiar with MATLAB
    4. Code simplicity is more important than explicit control
    5. Working interactively (Jupyter notebooks, IPython)

    Use OOP-Style when:
    ------------------
    1. Creating complex figures with multiple subplots
    2. You need explicit control over which plot you're modifying
    3. Writing functions that create plots
    4. Building applications with embedded plots
    5. You want clearer, more maintainable code
    6. Working on larger projects (RECOMMENDED)

    General Recommendation:
    ----------------------
    - Learn both styles
    - Use MATLAB-style for quick exploration
    - Use OOP-style for production code and complex visualizations
    - NEVER mix both styles in the same code (pick one and stick with it)
    """

    # ============================================================================
    # SECTION 8: Practical Example - Why OOP is Better for Multiple Plots
    # ============================================================================

    # Imagine you want to create two different plots
    # With MATLAB-style, this can get confusing:

    # MATLAB-style (works but less clear)
    plt.figure(1)
    x = np.linspace(0, 5, 50)
    plt.plot(x, x**2)
    plt.title('Figure 1: Quadratic')

    plt.figure(2)
    plt.plot(x, x**3)
    plt.title('Figure 2: Cubic')

    plt.figure(1)  # Go back to first figure
    plt.xlabel('x')  # Add label to first figure

    plt.show()

    # OOP-style (clearer and more explicit)
    x = np.linspace(0, 5, 50)

    # Create first plot
    fig1, ax1 = plt.subplots()
    ax1.plot(x, x**2)
    ax1.set_title('Figure 1: Quadratic')
    ax1.set_xlabel('x')  # No confusion about which plot we're modifying

    # Create second plot
    fig2, ax2 = plt.subplots()
    ax2.plot(x, x**3)
    ax2.set_title('Figure 2: Cubic')
    ax2.set_xlabel('x')

    plt.show()

    # With OOP style, it's always clear which axes object we're working with!

    # ============================================================================
    # SECTION 9: Converting Between Styles
    # ============================================================================

    """
    If you see MATLAB-style code, you can convert it to OOP-style:

    MATLAB-Style:
    ------------
    plt.plot(x, y)
    plt.xlabel('x label')
    plt.ylabel('y label')
    plt.title('My Title')
    plt.show()

    OOP-Style:
    ---------
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel('x label')
    ax.set_ylabel('y label')
    ax.set_title('My Title')
    plt.show()

    Just remember:
    1. Create fig, ax first
    2. Change plt.* to ax.*
    3. Add 'set_' prefix for labels, title, limits, ticks
    """

    # ============================================================================
    # KEY TAKEAWAYS
    # ============================================================================

    """
    1. Matplotlib has two styles: MATLAB-style (plt.*) and OOP-style (fig, ax)
    2. Both produce identical results
    3. OOP-style uses explicit Figure and Axes objects
    4. Method names differ: plt.xlabel() vs ax.set_xlabel()
    5. OOP-style is recommended for complex plots and maintainable code
    6. MATLAB-style is good for quick, simple plots
    7. Choose one style per script/project and be consistent
    8. Understanding both styles helps you read others' code
    """

    print("\n" + "=" * 70)
    print("SUMMARY OF METHOD NAME DIFFERENCES")
    print("=" * 70)
    print("MATLAB-style          -->  OOP-style")
    print("-" * 70)
    print("plt.plot()            -->  ax.plot()")
    print("plt.xlabel()          -->  ax.set_xlabel()")
    print("plt.ylabel()          -->  ax.set_ylabel()")
    print("plt.title()           -->  ax.set_title()")
    print("plt.xlim()            -->  ax.set_xlim()")
    print("plt.ylim()            -->  ax.set_ylim()")
    print("plt.legend()          -->  ax.legend()")
    print("plt.grid()            -->  ax.grid()")
    print("=" * 70)
```


---

## Exercises

**Exercise 1.** Rewrite the following pyplot-style code using the OOP style (explicit Figure and Axes objects):

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x), 'r-')
plt.title('Sine Wave')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()
```

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 10, 100)

    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x), 'r-')
    ax.set_title('Sine Wave')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.grid(True)
    plt.show()
    ```

---

**Exercise 2.** Explain two advantages of the OOP style (`fig, ax = plt.subplots()`) over the pyplot style (`plt.plot()`) when creating complex, multi-subplot figures.

??? success "Solution to Exercise 2"
    1. **Explicit control over multiple subplots**: With the OOP style, each Axes object is a distinct variable (`ax1`, `ax2`, etc.), making it clear which subplot you are modifying. In pyplot style, the "current axes" concept can be ambiguous and error-prone with multiple subplots.

    2. **Better for reusable functions**: You can write functions that accept an `ax` parameter and draw on it, making your plotting code modular and testable. With pyplot, functions implicitly modify global state, which is harder to compose and debug.

---

**Exercise 3.** Write code using the OOP style that creates a 1x2 subplot figure. Plot $\sin(x)$ on the left and $\cos(x)$ on the right, each with its own title, axis labels, and grid.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 2 * np.pi, 200)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    ax1.plot(x, np.sin(x), 'b-', lw=2)
    ax1.set_title(r'$y = \sin(x)$')
    ax1.set_xlabel('$x$')
    ax1.set_ylabel('$y$')
    ax1.grid(True, alpha=0.3)

    ax2.plot(x, np.cos(x), 'r-', lw=2)
    ax2.set_title(r'$y = \cos(x)$')
    ax2.set_xlabel('$x$')
    ax2.set_ylabel('$y$')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
    ```

---

**Exercise 4.** Predict what happens if you call `plt.plot()` twice without calling `plt.show()` in between. Then predict what happens if you use the OOP style and call `ax.plot()` twice on the same Axes object.

??? success "Solution to Exercise 4"
    Calling `plt.plot()` twice without `plt.show()` in between adds both lines to the **same** current axes. Both lines appear on the same plot when `plt.show()` is finally called.

    Similarly, calling `ax.plot()` twice on the same Axes object also adds both lines to that axes. The behavior is identical: both lines appear together on the same subplot.

    The key difference is only in clarity: with the OOP style, it is explicit which axes you are drawing on.
