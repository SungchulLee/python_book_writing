# Arrays vs DataFrames

!!! tip "Mental Model"
    NumPy arrays are homogeneous grids optimized for numerical computation -- every element shares one dtype. DataFrames are heterogeneous tables where each column can have a different dtype, plus labeled axes for alignment. Choose NumPy when all data is the same type and speed matters most; choose pandas when you need mixed types, labels, or missing-value handling.

## Data Structure

### 1. NumPy Array

Homogeneous, n-dimensional:

```python
import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.dtype)  # All elements same type
print(arr.shape)  # (2, 3)
```

### 2. Pandas DataFrame

Heterogeneous, labeled, tabular:

```python
import pandas as pd

df = pd.DataFrame({
    'name': ['Alice', 'Bob'],
    'age': [25, 30],
    'score': [85.5, 92.0]
})
print(df.dtypes)  # Different types per column
```

### 3. Key Difference

Array: Single dtype, unlabeled
DataFrame: Multiple dtypes, labeled

## When to Use Each

### 1. Use NumPy When

```python
# Matrix operations
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
C = A @ B  # Matrix multiplication

# Numerical computation
data = np.random.randn(1000, 100)
result = data.mean(axis=0)
```

### 2. Use Pandas When

```python
# Heterogeneous data
df = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=10),
    'category': ['A', 'B'] * 5,
    'value': np.random.rand(10)
})

# Data analysis
summary = df.groupby('category')['value'].mean()
```

### 3. Conversion

```python
# DataFrame to array
arr = df.values  # or df.to_numpy()

# Array to DataFrame
df = pd.DataFrame(arr, columns=['col1', 'col2'])
```

## Real-World Example

### 1. Financial Data

```python
import yfinance as yf

# Returns DataFrame (heterogeneous)
df = yf.download("AAPL", start="2023-01-01")
print(df.dtypes)

# Extract for numpy (homogeneous numerical)
close_prices = df['Close'].values
returns = np.diff(close_prices) / close_prices[:-1]
```

### 2. Image Processing

```python
from PIL import Image

# Load as array (homogeneous)
img = np.array(Image.open('photo.jpg'))
print(img.shape)  # (height, width, 3)

# Process
img_gray = img.mean(axis=2)
```

### 3. Time Series

```python
# Use DataFrame for labeled time series
df = pd.DataFrame({
    'timestamp': pd.date_range('2023-01-01', periods=100, freq='H'),
    'temperature': np.random.randn(100) + 20
}).set_index('timestamp')

# Use array for computation
temps = df['temperature'].values
ma = np.convolve(temps, np.ones(5)/5, mode='valid')
```


---

## Exercises

**Exercise 1.** Create a NumPy 2D array and a Pandas DataFrame with the same data. Demonstrate one operation that is easier with DataFrame (e.g., column selection by name).

??? success "Solution to Exercise 1"
    ```python
    import pandas as pd
    import numpy as np

    arr = np.array([[1, 2, 3], [4, 5, 6]])
    df = pd.DataFrame(arr, columns=['a', 'b', 'c'])
    print(df['b'])  # Easy column selection by name
    ```

---

**Exercise 2.** Explain three advantages of Pandas DataFrames over NumPy arrays for tabular data analysis.

??? success "Solution to Exercise 2"

    1. **Named columns**: DataFrames allow accessing columns by name rather than integer index.
    2. **Mixed types**: Each column can have a different dtype (int, float, string, etc.).
    3. **Built-in methods**: DataFrames provide `groupby`, `merge`, `pivot`, and other high-level data manipulation methods not available in NumPy.

---

**Exercise 3.** Write code that converts a NumPy array to a DataFrame with named columns, and then converts a DataFrame back to a NumPy array using `.to_numpy()`.

??? success "Solution to Exercise 3"
    ```python
    import pandas as pd
    import numpy as np

    arr = np.array([[1, 2], [3, 4], [5, 6]])
    df = pd.DataFrame(arr, columns=['x', 'y'])
    print(df)
    arr_back = df.to_numpy()
    print(arr_back)
    ```

---

**Exercise 4.** Create a DataFrame with mixed types (int, float, string) and show that `df.dtypes` reports different dtypes per column, while a NumPy array would coerce all to one type.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    df = pd.DataFrame({'int_col': [1, 2], 'float_col': [1.5, 2.5], 'str_col': ['a', 'b']})
    print(df.dtypes)
    # int64, float64, object -- different types per column
    arr = np.array([[1, 1.5, 'a'], [2, 2.5, 'b']])
    print(arr.dtype)  # All coerced to '<U32' (string)
    ```
