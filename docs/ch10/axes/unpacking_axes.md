# Unpacking Axes

Python's tuple unpacking provides a clean way to name individual axes when creating subplots.

!!! tip "Mental Model"
    `fig, ax = plt.subplots()` is just Python tuple unpacking -- the function returns a pair and you name each element. For grids, `fig, (ax1, ax2) = plt.subplots(1, 2)` unpacks the axes array in the same way. Giving each Axes a descriptive name makes your code read like a sentence instead of an index lookup.

    The deeper principle: **naming axes = naming meaning.** Compare
    `axes[0]` vs `ax_price` — the first is a position, the second is a concept.
    Descriptive names make code self-documenting and prevent mix-ups when a
    layout has many panels:

    ```python
    fig, (ax_price, ax_volume, ax_returns) = plt.subplots(3, 1)
    ```

!!! warning "Unpacking is Fragile"
    Unpacking hardcodes the number of axes. If the layout changes (e.g., from
    2 to 3 panels), the unpacking line breaks immediately:

    ```python
    # This works for 2 panels
    fig, (ax1, ax2) = plt.subplots(1, 2)

    # Adding a third panel requires changing the unpack line too
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    ```

    For functions that accept a **variable number of panels**, use indexing
    (`axes[i]`) or `axes.flat` instead. Reserve unpacking for fixed, known
    layouts where readability outweighs flexibility.

---

## Unpacking a Single Axes

The most common pattern:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()
```

---

## Unpacking 1D Arrays

For single rows or columns:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)

# Unpack 1x2 grid
fig, (ax0, ax1) = plt.subplots(1, 2)
ax0.plot(x, np.sin(x))
ax1.plot(x, np.cos(x))
plt.show()
```

```python
# Unpack 2x1 grid
fig, (ax0, ax1) = plt.subplots(2, 1)
ax0.plot(x, np.sin(x))
ax1.plot(x, np.cos(x))
plt.show()
```

```python
# Unpack 1x3 grid
fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(12, 3))
ax0.plot(x, x**2)
ax1.plot(x, np.sin(x))
ax2.plot(x, np.exp(x))
plt.tight_layout()
plt.show()
```

---

## Unpacking 2D Arrays

Use nested tuple unpacking for grids:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)

# Unpack 2x2 grid
fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2)

ax0.plot(x, np.sin(x))
ax0.set_title("sin")

ax1.plot(x, np.cos(x))
ax1.set_title("cos")

ax2.plot(x, np.sinh(x))
ax2.set_title("sinh")

ax3.plot(x, np.cosh(x))
ax3.set_title("cosh")

plt.tight_layout()
plt.show()
```

---

## 2×3 Grid Unpacking

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0.001, 1, 100)

fig, ((ax0, ax1, ax2), (ax3, ax4, ax5)) = plt.subplots(2, 3, figsize=(12, 6))

ax0.plot(x, x**2)
ax1.plot(x, np.sin(x))
ax2.plot(x, np.exp(x))
ax3.plot(x, np.log(x))
ax4.plot(x, np.sin(x) / np.exp(x))
ax5.plot(x, np.log(x) / np.exp(x))

plt.tight_layout()
plt.show()
```

---

## When to Use Array Indexing vs Unpacking

**Use unpacking when:**

- Fixed number of subplots
- Each subplot has distinct content
- Want descriptive variable names

```python
fig, (ax_price, ax_volume) = plt.subplots(2, 1, sharex=True)
ax_price.plot(dates, prices)
ax_volume.bar(dates, volume)
```

**Use array indexing when:**

- Dynamic number of subplots
- Applying the same operation to all
- Looping over subplots

```python
fig, axes = plt.subplots(3, 4)
for i, ax in enumerate(axes.flat):
    ax.plot(data[i])
```

---

## Combining Both Approaches

Sometimes a hybrid approach is clearest:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2*np.pi, 100)

# Create the grid
fig, axes = plt.subplots(2, 2, figsize=(8, 6))

# Unpack for clarity
(ax_sin, ax_cos), (ax_tan, ax_exp) = axes

ax_sin.plot(x, np.sin(x))
ax_sin.set_title("sin(x)")

ax_cos.plot(x, np.cos(x))
ax_cos.set_title("cos(x)")

ax_tan.plot(x, np.tan(x))
ax_tan.set_ylim(-5, 5)
ax_tan.set_title("tan(x)")

ax_exp.plot(x, np.exp(np.sin(x)))
ax_exp.set_title("exp(sin(x))")

plt.tight_layout()
plt.show()
```

---

## Using axes.flat

Iterate over all axes regardless of shape:

```python
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(2, 3, figsize=(12, 6))

for i, ax in enumerate(axes.flat):
    x = np.linspace(0, 2*np.pi, 100)
    ax.plot(x, np.sin((i+1) * x))
    ax.set_title(f"sin({i+1}x)")

plt.tight_layout()
plt.show()
```

---

## Key Takeaways

- `fig, ax = plt.subplots()` for single axes
- `fig, (ax0, ax1) = plt.subplots(1, 2)` for 1D arrays
- `fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2)` for 2D arrays
- Use unpacking for fixed layouts with distinct content
- Use array indexing for dynamic or looped operations
- `axes.flat` flattens any shape for iteration

---

## Exercises

**Exercise 1.**
Use tuple unpacking to create a 1x2 subplot layout: `fig, (ax_left, ax_right) = plt.subplots(1, 2)`. Plot a histogram on the left and a box plot on the right using 1000 samples from a normal distribution.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        data = np.random.randn(1000)

        fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(10, 4))

        ax_left.hist(data, bins=30, color='steelblue', edgecolor='white')
        ax_left.set_title('Histogram')

        ax_right.boxplot(data)
        ax_right.set_title('Box Plot')

        plt.tight_layout()
        plt.show()

---

**Exercise 2.**
Create a 2x2 subplot grid and use nested unpacking: `fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)`. Plot `sin`, `cos`, `tan`, and `exp` on the four axes respectively. Add titles and use `plt.tight_layout()`.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 2 * np.pi, 200)

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8))

        ax1.plot(x, np.sin(x))
        ax1.set_title('sin(x)')

        ax2.plot(x, np.cos(x), color='red')
        ax2.set_title('cos(x)')

        ax3.plot(x, np.tan(x), color='green')
        ax3.set_ylim(-5, 5)
        ax3.set_title('tan(x)')

        ax4.plot(x, np.exp(x / 3), color='orange')
        ax4.set_title('exp(x/3)')

        plt.tight_layout()
        plt.show()

---

**Exercise 3.**
Create a 3x1 layout and unpack as `fig, (ax_top, ax_mid, ax_bot) = plt.subplots(3, 1, figsize=(8, 10), sharex=True)`. Plot a stock-like random walk on the top, its daily returns on the middle, and a cumulative return on the bottom. Use descriptive y-labels for each.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        returns = np.random.randn(200) * 0.02
        prices = 100 * np.cumprod(1 + returns)
        cum_returns = np.cumprod(1 + returns) - 1

        fig, (ax_top, ax_mid, ax_bot) = plt.subplots(3, 1, figsize=(8, 10), sharex=True)

        ax_top.plot(prices, color='navy')
        ax_top.set_ylabel('Price')
        ax_top.set_title('Stock Dashboard')

        ax_mid.bar(range(len(returns)), returns, color=['green' if r > 0 else 'red' for r in returns], width=1)
        ax_mid.set_ylabel('Daily Return')

        ax_bot.plot(cum_returns, color='purple')
        ax_bot.set_ylabel('Cumulative Return')
        ax_bot.set_xlabel('Day')

        plt.tight_layout()
        plt.show()
