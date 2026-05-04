# Figure Styles

Matplotlib provides built-in style sheets for consistent and professional-looking plots.

!!! tip "Mental Model"
    Figure styles are global presets that override Matplotlib's defaults. Under the hood, each style is a set of **rcParams** — the hundreds of key-value pairs that control every visual aspect of a plot (font size, line width, color cycle, grid visibility, etc.). Calling `plt.style.use('ggplot')` bulk-overrides these params. You can inspect or set any individual param via `plt.rcParams['axes.labelsize'] = 14`.

    **Style is not decoration — it changes what stands out:**

    | Style choice | Perceptual effect |
    |-------------|------------------|
    | High contrast | Emphasizes differences |
    | Muted colors | Emphasizes trends over noise |
    | Dark background | Highlights bright elements (presentations) |
    | Thin lines + small fonts | Fits more data (dense dashboards) |

    **Consistency matters:** changing styles between figures forces the viewer to
    re-learn the visual language each time, creating cognitive friction. Pick one
    style per project and stick to it.

!!! note "Choosing a Style: Design Principles"
    - **Publication/print:** use `'seaborn-v0_8-whitegrid'` or a custom minimal style — high contrast, clear labels, vector export (PDF/SVG).
    - **Presentation/slides:** use `'dark_background'` or large-font styles — must be readable from a distance.
    - **Exploration/notebook:** use `'ggplot'` or `'bmh'` — pleasant colors for quick iteration.
    - **Consistency:** pick one style for your entire project and set it once at the top of your plotting module. Inconsistent styles across figures look unprofessional.

---

## Available Styles

List all available styles:

```python
import matplotlib.pyplot as plt

print(plt.style.available)
```

Common styles include:

- `'seaborn-v0_8-darkgrid'`
- `'ggplot'`
- `'bmh'`
- `'fivethirtyeight'`
- `'dark_background'`

---

## Using plt.style.use

Apply a style globally:

```python
import matplotlib.pyplot as plt

days = [0, 1, 2, 3, 4, 5, 6]
avg_t = [25, 28, 28, 26, 20, 22, 21]

plt.style.use("seaborn-v0_8-darkgrid")

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(days, avg_t, 'r--o')
plt.show()
```

---

## Temporary Style Context

Apply a style temporarily using a context manager:

```python
import matplotlib.pyplot as plt

with plt.style.context('ggplot'):
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4])
    plt.show()

# Style reverts after the context
```

---

## The xkcd Style

Create hand-drawn style plots:

```python
import matplotlib.pyplot as plt

days = [0, 1, 2, 3, 4, 5, 6]
avg_t = [25, 28, 28, 26, 20, 22, 21]

plt.xkcd()

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(days, avg_t, 'r--o')
plt.show()
```

!!! note
    The xkcd style requires the "Humor Sans" font for best results.

---

## Combining Multiple Styles

Styles can be combined by passing a list:

```python
plt.style.use(['seaborn-v0_8-darkgrid', 'seaborn-v0_8-talk'])
```

Later styles override earlier ones for conflicting settings.

---

## Creating Custom Styles

Create a custom style file (e.g., `mystyle.mplstyle`):

```
# mystyle.mplstyle
axes.facecolor: white
axes.edgecolor: black
axes.grid: True
grid.color: gray
grid.linestyle: --
lines.linewidth: 2
font.size: 12
```

Use it with:

```python
plt.style.use('./mystyle.mplstyle')
```

---

## Resetting to Default

Reset to Matplotlib defaults:

```python
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)
```

Or use the default style:

```python
plt.style.use('default')
```

---

## Key Takeaways

- `plt.style.available` lists all built-in styles
- `plt.style.use()` applies a style globally
- Use context managers for temporary style changes
- `plt.xkcd()` creates hand-drawn style plots
- Custom styles can be saved as `.mplstyle` files


---

## Exercises

**Exercise 1.** Write code that creates a figure with a light gray background (`facecolor='#f0f0f0'`) and a black border (`edgecolor='black'`, `linewidth=2`). Plot any function on it.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 2 * np.pi, 100)

    fig = plt.figure(figsize=(8, 5), facecolor='#f0f0f0',
                     edgecolor='black', linewidth=2)
    ax = fig.add_subplot(111)
    ax.plot(x, np.sin(x), 'b-', lw=2)
    ax.set_title('Figure with Custom Background')
    plt.show()
    ```

---

**Exercise 2.** List three different Matplotlib style sheets and explain when each might be appropriate. Write code that applies one of them using `plt.style.use()`.

??? success "Solution to Exercise 2"
    Three common Matplotlib style sheets:

    1. **`'ggplot'`** -- Mimics the look of R's ggplot2 library. Good for data science presentations with a clean, colorful aesthetic.
    2. **`'seaborn-v0_8'`** -- Based on Seaborn defaults. Good for statistical visualizations with soft colors and grid backgrounds.
    3. **`'dark_background'`** -- White/bright elements on dark background. Good for presentations on dark-themed slides or monitors.

    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    plt.style.use('ggplot')

    x = np.linspace(0, 10, 100)
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x), lw=2, label='sin(x)')
    ax.plot(x, np.cos(x), lw=2, label='cos(x)')
    ax.legend()
    ax.set_title('Using ggplot Style')
    plt.show()
    ```

---

**Exercise 3.** Write code that creates two figures (in the same script) using different style contexts via `plt.style.context()`. Use `'ggplot'` for the first and `'dark_background'` for the second.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 2 * np.pi, 100)

    with plt.style.context('ggplot'):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x, np.sin(x), lw=2)
        ax.set_title('ggplot style')
        plt.show()

    with plt.style.context('dark_background'):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x, np.cos(x), lw=2)
        ax.set_title('dark_background style')
        plt.show()
    ```

---

**Exercise 4.** Create a figure with customized `dpi=150` and `figsize=(6, 4)`. Calculate the resulting pixel dimensions and verify by printing `fig.get_size_inches()` and `fig.dpi`.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
    ax.plot([0, 1, 2], [0, 1, 4])
    ax.set_title('Custom DPI Figure')

    print(f"Size in inches: {fig.get_size_inches()}")  # [6. 4.]
    print(f"DPI: {fig.dpi}")                            # 150.0
    # Pixel dimensions: 6 * 150 = 900 x 4 * 150 = 600
    print(f"Pixel dimensions: {6 * 150} x {4 * 150}")   # 900 x 600
    plt.show()
    ```

---

**Exercise 5.** Explain what `rcParams` are and how styles modify them. Write code that (a) prints the current `axes.labelsize`, (b) changes it to 16 using `plt.rcParams`, (c) creates a plot to verify the change, and (d) resets to defaults with `plt.rcdefaults()`. When would you modify `rcParams` directly instead of using a style sheet?

??? success "Solution to Exercise 5"

    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    # (a) Current value
    print(f"Default label size: {plt.rcParams['axes.labelsize']}")

    # (b) Change it
    plt.rcParams['axes.labelsize'] = 16

    # (c) Verify
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])
    ax.set_xlabel('X (should be large)')
    ax.set_ylabel('Y (should be large)')
    plt.show()

    # (d) Reset
    plt.rcdefaults()
    print(f"After reset: {plt.rcParams['axes.labelsize']}")
    ```

    **When to use `rcParams` directly:** when you need to tweak one or two specific settings without changing everything else (e.g., increase just the font size for a presentation). Use a style sheet when you want a complete, reusable visual theme. In practice, many workflows combine both: set a base style with `plt.style.use()`, then override specific params with `plt.rcParams[...]`.
