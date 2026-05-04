# Figure Methods

The Figure object provides methods for managing subplots, layout, and overall figure properties.

!!! tip "Mental Model"
    Figure methods operate on the whole canvas, not individual plots. Use `fig.suptitle()` for a master title above all subplots, `fig.tight_layout()` to fix overlapping labels, and `fig.savefig()` to export. If you want to change something inside one subplot, use Axes methods instead.

    The typical workflow order: **create → populate → layout → export.**

    The key distinction: **Figure methods control global structure; Axes methods
    control local content.** Confusing the two (e.g., calling `fig.set_xlabel()`
    instead of `ax.set_xlabel()`) is a common source of errors. Layout is about
    readability — overlapping labels cause confusion, cramped plots are unreadable,
    and excessive spacing wastes attention. Good layout makes the figure effortless
    to read.

!!! tip "Layout Methods: When to Use Each"
    | Method | Use when |
    |---|---|
    | `fig.tight_layout()` | Quick fix for overlapping labels (call after plotting) |
    | `fig.subplots_adjust(...)` | Manual control over spacing (margins, gaps) |
    | `constrained_layout=True` | Modern automatic layout that handles colorbars and legends (set at figure creation: `plt.subplots(..., layout='constrained')`) |

    **Prefer `constrained_layout`** for new code — it handles more edge cases than `tight_layout` and does not require a separate function call. Use `subplots_adjust` only when you need pixel-precise manual control.

---

## suptitle

Add a centered title to the entire figure:

```python
import matplotlib.pyplot as plt
import numpy as np

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12, 3))
fig.suptitle("Figure Super Title", fontsize=20)

ax0.hist(np.random.normal(size=1000), bins=30)
ax1.boxplot(np.random.normal(size=1000))

plt.show()
```

---

## subplots_adjust

Fine-tune spacing between subplots:

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.datasets import fetch_olivetti_faces

faces = fetch_olivetti_faces().images

fig, ax = plt.subplots(5, 5, figsize=(5, 5))
fig.subplots_adjust(hspace=0, wspace=0)

for i in range(5):
    for j in range(5):
        ax[i, j].xaxis.set_major_locator(mpl.ticker.NullLocator())
        ax[i, j].yaxis.set_major_locator(mpl.ticker.NullLocator())
        ax[i, j].imshow(faces[10 * i + j], cmap="bone")

plt.show()
```

Parameters:

- `left`, `right`, `bottom`, `top`: Subplot boundaries (0 to 1)
- `wspace`: Width space between subplots
- `hspace`: Height space between subplots

---

## tight_layout

Automatically adjust subplot parameters:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)

fig, axes = plt.subplots(2, 2, figsize=(8, 6))

axes[0, 0].plot(x, np.sin(x))
axes[0, 0].set_title("sin(x)")
axes[0, 0].set_xlabel("x")
axes[0, 0].set_ylabel("y")

axes[0, 1].plot(x, np.cos(x))
axes[0, 1].set_title("cos(x)")

axes[1, 0].plot(x, np.sinh(x))
axes[1, 0].set_title("sinh(x)")

axes[1, 1].plot(x, np.cosh(x))
axes[1, 1].set_title("cosh(x)")

fig.tight_layout()
plt.show()
```

---

## autofmt_xdate

Automatically format date labels to prevent overlap:

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import yfinance as yf

df = yf.Ticker('AAPL').history(start='2020-07-01', end='2020-12-31')

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(df.index, df['Close'])

date_format = mpl_dates.DateFormatter('%b, %d %Y')
ax.xaxis.set_major_formatter(date_format)

fig.autofmt_xdate()
plt.show()
```

---

## savefig

Save the figure to a file:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y_sin = np.sin(x)
y_cos = np.cos(x)

fig, ax = plt.subplots(figsize=(15, 4))
ax.plot(x, y_sin)
ax.plot(x, y_cos)

fig.savefig("sin_cos_graph.png", facecolor="#f1f1f1", transparent=True)
plt.show()
```

---

## get_size_inches and set_size_inches

Get or modify figure size after creation:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

# Get current size
print(fig.get_size_inches())  # [6.4, 4.8]

# Change size
fig.set_size_inches(12, 4)
print(fig.get_size_inches())  # [12., 4.]

plt.show()
```

---

## get_axes

Get a list of all Axes in the figure:

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2)

all_axes = fig.get_axes()
print(len(all_axes))  # 4

for ax in all_axes:
    ax.plot([1, 2, 3])

plt.show()
```

---

## clear

Clear the entire figure:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3])

fig.clear()  # Removes all axes and content

ax_new = fig.add_subplot(111)
ax_new.plot([3, 2, 1])

plt.show()
```

---

## Key Takeaways

- `suptitle()` adds a title above all subplots
- `subplots_adjust()` controls subplot spacing manually
- `tight_layout()` automatically adjusts spacing
- `autofmt_xdate()` formats date labels
- `savefig()` exports the figure to a file


---

## Exercises

**Exercise 1.** Write code that creates a figure, adds two subplots side by side using `fig.add_subplot()`, plots different data on each, and uses `fig.suptitle()` to add an overall title.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure(figsize=(12, 4))
    fig.suptitle('Two Subplots Example', fontsize=16)

    ax1 = fig.add_subplot(1, 2, 1)
    x = np.linspace(0, 2 * np.pi, 100)
    ax1.plot(x, np.sin(x), 'b-')
    ax1.set_title('Sine')

    ax2 = fig.add_subplot(1, 2, 2)
    ax2.plot(x, np.cos(x), 'r-')
    ax2.set_title('Cosine')

    plt.tight_layout()
    plt.show()
    ```

---

**Exercise 2.** Explain the difference between `ax.set_title()` and `fig.suptitle()`. When would you use each?

??? success "Solution to Exercise 2"
    `ax.set_title()` adds a title to a specific Axes (subplot), appearing directly above that subplot. `fig.suptitle()` adds a "super title" to the entire Figure, appearing above all subplots.

    Use `ax.set_title()` when you want to label individual subplots with their own titles. Use `fig.suptitle()` when you want an overarching title for the whole figure, especially when you have multiple subplots that share a common theme.

---

**Exercise 3.** Write code that creates a figure and uses `fig.text()` to add text at the center-bottom of the figure (coordinates `(0.5, 0.02)`). Plot a simple line on the axes above.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.linspace(0, 10, 100)
    ax.plot(x, np.sin(x), 'b-', lw=2)
    ax.set_title('Sine Wave')

    fig.text(0.5, 0.02, 'This text is placed at the bottom center of the figure',
             ha='center', fontsize=12, style='italic')

    plt.subplots_adjust(bottom=0.12)
    plt.show()
    ```

---

**Exercise 4.** Create a figure with `fig.add_axes()` to place two overlapping axes at custom positions. The first axes should fill most of the figure, and the second should be a small inset in the top-right corner.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 10, 200)

    fig = plt.figure(figsize=(8, 6))

    ax_main = fig.add_axes([0.1, 0.1, 0.85, 0.85])
    ax_main.plot(x, np.sin(x), 'b-', lw=2)
    ax_main.set_title('Main Plot')

    ax_inset = fig.add_axes([0.6, 0.6, 0.3, 0.25])
    ax_inset.plot(x, np.cos(x), 'r-', lw=1.5)
    ax_inset.set_title('Inset', fontsize=9)

    plt.show()
    ```

---

**Exercise 5.** Compare `fig.tight_layout()` and `constrained_layout=True`. Create a 2x2 subplot grid with long axis labels that overlap. Fix it first with `tight_layout()`, then recreate and fix it with `plt.subplots(..., layout='constrained')`. Which approach handles colorbars better?

??? success "Solution to Exercise 5"

    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 10, 50)

    # Approach 1: tight_layout
    fig1, axes1 = plt.subplots(2, 2, figsize=(8, 6))
    for ax in axes1.flat:
        ax.plot(x, np.random.randn(50))
        ax.set_xlabel('Long X-axis Label Here')
        ax.set_ylabel('Long Y-axis Label')
    fig1.tight_layout()
    fig1.suptitle('tight_layout', y=1.02)

    # Approach 2: constrained_layout
    fig2, axes2 = plt.subplots(2, 2, figsize=(8, 6), layout='constrained')
    for ax in axes2.flat:
        ax.plot(x, np.random.randn(50))
        ax.set_xlabel('Long X-axis Label Here')
        ax.set_ylabel('Long Y-axis Label')
    fig2.suptitle('constrained_layout')

    plt.show()
    ```

    `constrained_layout` handles colorbars better because it reserves space for them during layout computation. With `tight_layout`, adding a colorbar after the layout call can re-introduce overlaps. `constrained_layout` is the modern recommended approach.
