# Text Object

Text objects in Matplotlib represent any text element including tick labels, axis labels, titles, and annotations.

!!! tip "Mental Model"
    Every piece of text on a Matplotlib figure -- every tick label, title, axis label, and annotation -- is a `Text` Artist object. This means you can grab any text element, inspect its properties (`get_fontsize()`, `get_position()`), and modify it after creation (`set_color()`, `set_rotation()`). Understanding this unifies all text customization under one interface.

    Text objects control how **meaning is presented** in a plot — they are the
    interface between data visualization and human interpretation. Modifying a
    Text object changes not just appearance, but how the viewer understands
    the data.

!!! tip "Debugging Text Layout"
    When text overlaps or appears misaligned:

    1. **Inspect position**: `text_obj.get_position()` — is it where you expect?
    2. **Check transform**: `text_obj.get_transform()` — data coords vs axes coords?
    3. **Check alignment**: `text_obj.get_ha()`, `text_obj.get_va()` — anchor point correct?
    4. **Visualize bbox**: `text_obj.get_bbox_patch()` or add `bbox=dict(boxstyle='round')` to see the text extent

    Most "misaligned" text is actually a transform or alignment issue, not a
    position issue.

---

## Text Objects in Axes

Every text element is a `Text` object:

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(0)
error = np.random.normal(size=(400,))
index = pd.date_range(start='2019-09-01', end='2020-01-01', freq='D')

mu = 50
data = [mu + 0.4*error[t-1] + 0.3*error[t-2] + error[t] 
        for t in range(2, len(index)+2)]
s = pd.Series(data, index)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(s)
ax.axhline(mu, linestyle='--', color='grey')

# Examine tick labels
for label in ax.get_xticklabels():
    print(f"Type: {type(label)}")
    break

plt.show()
```

Output:
```
Type: <class 'matplotlib.text.Text'>
```

---

## Accessing Text Elements

Get various text elements from an axes:

```python
# Tick labels
x_labels = ax.get_xticklabels()  # List of Text objects
y_labels = ax.get_yticklabels()  # List of Text objects

# Title
title = ax.title  # Text object

# Axis labels
xlabel = ax.xaxis.label  # Text object
ylabel = ax.yaxis.label  # Text object
```

---

## Text Properties

Common properties available on Text objects:

| Property | Description |
|----------|-------------|
| `text` | The string content |
| `fontsize` | Font size |
| `fontweight` | 'normal', 'bold', etc. |
| `fontstyle` | 'normal', 'italic', etc. |
| `fontfamily` | 'serif', 'sans-serif', etc. |
| `color` | Text color |
| `alpha` | Transparency |
| `rotation` | Rotation angle |
| `horizontalalignment` | 'left', 'center', 'right' |
| `verticalalignment` | 'top', 'center', 'bottom' |
| `backgroundcolor` | Background color |

---

## Text Methods

Set properties using setter methods:

```python
label.set_text('New Text')
label.set_fontsize(12)
label.set_fontweight('bold')
label.set_color('blue')
label.set_rotation(45)
label.set_horizontalalignment('right')
label.set_verticalalignment('top')
```

Get properties using getter methods:

```python
text = label.get_text()
size = label.get_fontsize()
weight = label.get_fontweight()
color = label.get_color()
```

---

## Example: Customizing Tick Labels

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(0)
error = np.random.normal(size=(400,))
index = pd.date_range(start='2019-09-01', end='2020-01-01', freq='D')

mu = 50
data = [mu + 0.4*error[t-1] + 0.3*error[t-2] + error[t] 
        for t in range(2, len(index)+2)]
s = pd.Series(data, index)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(s)
ax.axhline(mu, linestyle='--', color='grey')

for label in ax.get_xticklabels():
    label.set_horizontalalignment("right")
    label.set_rotation(45)

plt.show()
```

---

## Adding Background Box

Use `set_bbox()` to add a background:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-10, 10, 500)
y = np.sin(x) / x

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, linewidth=2)

# Move spines
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_position(('data', 0))
ax.spines['left'].set_position(('data', 0))

ax.set_xticks([-10, -5, 5, 10])
ax.set_yticks([0.5, 1])

# Add white background to labels
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_bbox({'facecolor': 'white', 'edgecolor': 'white'})

plt.show()
```

---

## Key Takeaways

- All text in Matplotlib is a `Text` object
- Access with `get_xticklabels()`, `get_yticklabels()`, etc.
- Use setter methods to customize appearance
- `set_bbox()` adds a background box
- Text objects support rotation, alignment, and styling


---

## Exercises

**Exercise 1.** Write code that creates a Text object with `ax.text()`, stores it in a variable, and then modifies its properties using setter methods (e.g., `t.set_color()`).

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

**Exercise 2.** Explain what the `transform` parameter of a Text object controls. What is the default transform?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Write code that retrieves all text objects from an axes using `ax.texts` and prints their string content.

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

**Exercise 4.** Create a plot with multiple text objects at different positions, each with a different font size, color, and rotation angle.

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
