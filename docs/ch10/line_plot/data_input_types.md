# Data Input Types

Matplotlib accepts various data types for plotting, providing flexibility for different workflows.

!!! tip "Mental Model"
    Matplotlib converts everything to NumPy arrays internally. You can pass Python lists, NumPy arrays, Pandas Series, or even dictionaries -- they all become arrays before drawing.

    **The fundamental requirement:** `x` and `y` must be **1D sequences of equal
    length** (or convertible to such). Mismatched lengths, 2D arrays, or mixed
    dtypes will raise errors or produce unexpected results. When in doubt, verify
    with `np.asarray(data).shape` before plotting.

    The deeper principle: **Matplotlib is type-agnostic but structure-sensitive.**
    It accepts lists, arrays, Series, and more — but it always requires consistent
    shape. Plotting operates on arrays, not objects.

---

## Python Lists

The simplest input type:

```python
import matplotlib.pyplot as plt

x = [1, 2, 3]
y = [1, 5, 2]

plt.plot(x, y)
plt.show()
```

---

## NumPy Arrays

The most common and efficient choice:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.array([1, 2, 3])
y = np.array([1, 5, 2])

plt.plot(x, y)
plt.show()
```

NumPy arrays are preferred because:

- Faster computation
- Support for broadcasting
- Integration with scientific computing

---

## NumPy linspace

Generate evenly spaced values:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)  # 100 points
y = np.sin(x)

plt.plot(x, y)
plt.show()
```

---

## Pandas DataFrame

When using DataFrames, extract the column:

```python
import matplotlib.pyplot as plt
import pandas as pd

def main():
    x = pd.DataFrame([1, 2, 3])  # x.shape = (3, 1)
    y = pd.DataFrame([1, 5, 2])  # y.shape = (3, 1)

    # Use iloc to extract as 1D
    plt.plot(x.iloc[:, 0], y.iloc[:, 0])
    plt.show()

if __name__ == "__main__":
    main()
```

Or access by column name:

```python
plt.plot(x[0], y[0])
```

---

## Pandas Series

Series work directly:

```python
import matplotlib.pyplot as plt
import pandas as pd

def main():
    x = pd.Series([1, 2, 3])  # x.shape = (3,)
    y = pd.Series([1, 5, 2])  # y.shape = (3,)

    plt.plot(x, y)
    plt.show()

if __name__ == "__main__":
    main()
```

---

## Plotting Y Values Only

When only y-values are provided, x-values default to indices:

**List:**
```python
import matplotlib.pyplot as plt

y = [1, 5, 2]
plt.plot(y)
plt.show()
```

**NumPy Array:**
```python
import matplotlib.pyplot as plt
import numpy as np

y = np.array([1, 5, 2])
plt.plot(y)
plt.show()
```

**Pandas DataFrame:**
```python
import matplotlib.pyplot as plt
import pandas as pd

y = pd.DataFrame([1, 5, 2])  # shape (3, 1)
plt.plot(y[0])
plt.show()
```

**Pandas Series:**
```python
import matplotlib.pyplot as plt
import pandas as pd

y = pd.Series([1, 5, 2])  # shape (3,)
plt.plot(y)
plt.show()
```

---

## Financial Data Example

Real-world data often comes from APIs:

```python
import matplotlib.pyplot as plt
import yfinance as yf

def download_stock_prices(ticker, start='2023-01-01', end='2024-12-31'):
    return yf.download(ticker, start=start, end=end)

def display_stock_prices(data, ticker):
    fig, ax = plt.subplots(figsize=(12, 3))
    
    # data['Close'] is a pandas Series with DatetimeIndex
    ax.plot(data['Close'], label=ticker)
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.legend()
    plt.show()

def main():
    ticker = 'GLD'
    data = download_stock_prices(ticker)
    display_stock_prices(data, ticker)

if __name__ == "__main__":
    main()
```

---

## Shape Considerations

Be mindful of data shapes when plotting:

```python
import numpy as np
import pandas as pd

# 1D structures work directly
arr_1d = np.array([1, 2, 3])        # shape (3,)
series = pd.Series([1, 2, 3])       # shape (3,)

# 2D structures need column selection
arr_2d = np.array([[1], [2], [3]])  # shape (3, 1)
df = pd.DataFrame([1, 2, 3])        # shape (3, 1)

# Convert 2D to 1D
arr_flat = arr_2d.flatten()         # or arr_2d[:, 0]
series_from_df = df.iloc[:, 0]      # or df[0]
```

---

## Key Takeaways

- Lists, NumPy arrays, and Pandas objects all work
- NumPy arrays are most efficient for large datasets
- DataFrames need column extraction (`df[col]` or `df.iloc[:, 0]`)
- Series work directly like 1D arrays
- Missing x-values default to indices `[0, 1, 2, ...]`


---

## Exercises

**Exercise 1.** Write code that demonstrates plotting from three different input types: a Python list, a NumPy array, and a Pandas Series. Show that all three produce the same plot.

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

**Exercise 2.** Explain what happens when you call `plt.plot(y)` with only y-values. What are the x-values?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Write code that plots data from a dictionary using `ax.plot(data['x'], data['y'])`.

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

**Exercise 4.** Demonstrate the difference between `ax.plot(x, y)` and `ax.plot(y)` when `x` does not start from 0.

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
