# Title and Labels

Titles and axis labels provide context for your plots.

!!! tip "Mental Model"
    A plot without labels is like a photograph without a caption -- technically visible but missing context. `ax.set_title()` tells readers what they are looking at, `ax.set_xlabel()`/`ax.set_ylabel()` tell them what the axes represent. These three calls turn a raw chart into a self-explanatory figure.

---

## Setting Title

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-6, 6, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y)
ax.set_title("Sine Curve")
plt.show()
```

Get the current title:

```python
print(ax.get_title())  # "Sine Curve"
```

---

## Title Formatting

```python
ax.set_title("Sine Curve", fontsize=20, fontweight='bold', color='navy')
```

Position the title:

```python
ax.set_title('Title', loc='left')   # Left-aligned
ax.set_title('Title', loc='right')  # Right-aligned
ax.set_title('Title', pad=20)       # Add padding above
```

---

## Setting Axis Labels

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 1, 100)
y = x + x**2

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y, color='g')
ax.set_title('$y = x + x^2$', fontsize=20)
ax.set_xlabel('$x$', fontsize=20)
ax.set_ylabel('$y$', fontsize=20)
plt.show()
```

Get current labels:

```python
print(ax.get_xlabel())
print(ax.get_ylabel())
```

---

## LaTeX Support

Matplotlib supports LaTeX math notation using `$...$`:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title(r'$y = \sin(x)$')
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
plt.show()
```

Complex equations:

```python
ax.set_title(r'$y = \frac{1}{\sqrt{2\pi}} e^{-\frac{x^2}{2}}$')
```

!!! tip
    Use raw strings (`r'...'`) to avoid escaping backslashes.

---

## Using set() for Multiple Properties

Set multiple properties at once:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 1, 100)
y = x + x**2

fig, ax = plt.subplots()
ax.plot(x, y, color='g')
ax.set(
    title='$y = x + x^2$',
    xlabel='$x$',
    ylabel='$y$',
    xlim=[0, 1],
    ylim=(0, 2)
)
plt.show()
```

---

## Label Padding and Rotation

```python
ax.set_xlabel('Time (seconds)', labelpad=10)  # Add padding
ax.set_ylabel('Value', rotation=0, labelpad=15)  # Horizontal label
```

---

## Figure Super Title

For multi-subplot figures, use `suptitle`:

```python
import matplotlib.pyplot as plt
import numpy as np

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12, 3))
fig.suptitle("Figure Title", fontsize=20)

ax0.hist(np.random.normal(size=1000), bins=30)
ax0.set_title("Histogram")

ax1.boxplot(np.random.normal(size=1000))
ax1.set_title("Box Plot")

plt.tight_layout()
plt.show()
```

---

## Key Takeaways

- `ax.set_title()` sets the axes title
- `ax.set_xlabel()` and `ax.set_ylabel()` set axis labels
- Use `$...$` for LaTeX math notation
- Use `ax.set()` to set multiple properties at once
- `fig.suptitle()` adds a title above all subplots
- Get current values with `get_title()`, `get_xlabel()`, `get_ylabel()`

---

## Exercises

**Exercise 1.**
Create a plot of `y = cos(x)` and add a title, x-label, and y-label with the following customizations: title in bold 16pt font, x-label in italic 12pt with color blue, y-label in 12pt with color red. Use `fontdict` parameter for styling.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 2 * np.pi, 200)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(x, np.cos(x))

        ax.set_title('Cosine Function', fontdict={'fontsize': 16, 'fontweight': 'bold'})
        ax.set_xlabel('x (radians)', fontdict={'fontsize': 12, 'fontstyle': 'italic', 'color': 'blue'})
        ax.set_ylabel('cos(x)', fontdict={'fontsize': 12, 'color': 'red'})

        plt.tight_layout()
        plt.show()

---

**Exercise 2.**
Create a 2x2 subplot grid. Add individual titles to each subplot and a super title for the entire figure using `fig.suptitle()`. Also add a shared x-label with `fig.supxlabel()` and shared y-label with `fig.supylabel()`.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 2 * np.pi, 200)

        fig, axes = plt.subplots(2, 2, figsize=(10, 8))

        axes[0, 0].plot(x, np.sin(x))
        axes[0, 0].set_title('sin(x)')

        axes[0, 1].plot(x, np.cos(x))
        axes[0, 1].set_title('cos(x)')

        axes[1, 0].plot(x, np.sin(2*x))
        axes[1, 0].set_title('sin(2x)')

        axes[1, 1].plot(x, np.cos(2*x))
        axes[1, 1].set_title('cos(2x)')

        fig.suptitle('Trigonometric Functions', fontsize=16, fontweight='bold')
        fig.supxlabel('x (radians)')
        fig.supylabel('y')

        plt.tight_layout()
        plt.show()

---

**Exercise 3.**
Create a plot where the title includes LaTeX math: display the formula being plotted as part of the title. Plot $y = \frac{\sin(x)}{x}$ and title it with the rendered equation. Also add an xlabel with units in parentheses and a ylabel with a LaTeX symbol.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-10, 10, 1000)
        y = np.sinc(x / np.pi)  # sinc(x/pi) = sin(x)/x

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x, y, color='darkblue', linewidth=2)
        ax.set_title(r'$y = \frac{\sin(x)}{x}$', fontsize=16)
        ax.set_xlabel(r'$x$ (radians)', fontsize=12)
        ax.set_ylabel(r'$\mathrm{sinc}(x)$', fontsize=12)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
