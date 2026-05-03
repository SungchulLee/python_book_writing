# NumPy Constants

NumPy provides fundamental mathematical constants and special values.

!!! tip "Mental Model"
    NumPy bundles the standard mathematical constants (`np.pi`, `np.e`, `np.inf`, `np.nan`) so you never need to hard-code magic numbers. `np.inf` and `np.nan` are IEEE 754 special values that propagate through arithmetic in well-defined ways -- learning their propagation rules prevents subtle bugs in numerical code.


!!! note "The Numerical Value Model"
    NumPy operates in the **IEEE 754 floating-point system**, which extends "numbers" beyond ordinary values:

    - **Finite numbers** — normal computation results
    - **Infinity** (`np.inf`) — overflow or division by zero
    - **NaN** (`np.nan`) — undefined or missing values

    These special values propagate through computations automatically: `nan + x = nan`, `inf + finite = inf`, `inf - inf = nan`. This means missing data can silently spread through a pipeline, and `nan != nan` (so `==` cannot detect NaN — use `np.isnan` instead). Understanding this model is essential for writing correct numerical code.

## Version Check

Verify the installed NumPy version.

### 1. Check Version

```python
import numpy as np

def main():
    print(f'{np.__version__ = }')

if __name__ == "__main__":
    main()
```

### 2. Compatibility

Different versions may have different features and behaviors.


## Mathematical Constants

NumPy includes commonly used mathematical constants.

### 1. Pi Constant

```python
import numpy as np

def main():
    print(f'{np.pi = }')

if __name__ == "__main__":
    main()
```

Output:

```
np.pi = 3.141592653589793
```

### 2. Euler's Number

```python
import numpy as np

def main():
    print(f'{np.e = }')

if __name__ == "__main__":
    main()
```

Output:

```
np.e = 2.718281828459045
```


## Trigonometric Plot

Use constants for precise mathematical visualizations.

### 1. Sine and Cosine

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    x = np.linspace(-np.pi, np.pi, 100)
    sin = np.sin(x)
    cos = np.cos(x)

    fig, ax = plt.subplots(figsize=(6.5, 4))

    ax.plot(x, sin, label='sin(x)')
    ax.plot(x, cos, label='cos(x)')

    ax.legend()

    ax.set_xticks((-np.pi, -np.pi/2, 0, np.pi/2, np.pi))
    ax.set_xticklabels(("-$\pi$", "-$\pi$/2", "0", "$\pi$/2", "$\pi$"))

    ax.set_yticks((-1, 1))

    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Axis Styling

Position spines at center and hide top/right borders for clean mathematical plots.


## Special Value np.nan

Represent missing or undefined numerical data.

### 1. Creating NaN Arrays

```python
import numpy as np

def main():
    x = np.array([
        [93., 84., 73., 68.],
        [97., 67., 57., np.nan],
        [87., 87., np.nan, 77.]
    ])
    print(x)

if __name__ == "__main__":
    main()
```

Output:

```
[[93. 84. 73. 68.]
 [97. 67. 57. nan]
 [87. 87. nan 77.]]
```

### 2. NaN Properties

```python
import numpy as np

print(np.nan == np.nan)      # False
print(np.isnan(np.nan))      # True
```

### 3. NaN Propagation

Any arithmetic with `np.nan` produces `np.nan`.


## Infinity Values

NumPy supports positive and negative infinity.

### 1. Infinity Constant

```python
import numpy as np

print(f'{np.inf = }')
print(f'{-np.inf = }')
print(f'{np.inf > 1e308 = }')
```

### 2. Checking Infinity

```python
import numpy as np

print(np.isinf(np.inf))      # True
print(np.isfinite(np.inf))   # False
print(np.isfinite(1.0))      # True
```


## Practical Usage

Constants enable precise scientific computing.

### 1. Circle Area

```python
import numpy as np

radius = 5
area = np.pi * radius ** 2
```

### 2. Exponential Decay

```python
import numpy as np

t = np.linspace(0, 5, 100)
decay = np.e ** (-t)
```

### 3. Missing Data

```python
import numpy as np

data = np.array([1, 2, np.nan, 4])
mean = np.nanmean(data)  # Ignores NaN
```

## The Floating-Point Value System

`nan` and `inf` are not NumPy inventions --- they are part of the IEEE 754 floating-point standard that all modern hardware implements. Think of the floating-point number system as having three categories:

```text
Finite numbers:  -1.5, 0.0, 3.14, 1e308
Infinity:        np.inf, -np.inf    (result of overflow or 1/0)
Not a Number:    np.nan             (result of 0/0 or undefined ops)
```

Both propagate through arithmetic automatically:

- `nan + anything = nan` (unknown stays unknown)
- `inf + finite = inf` (unbounded stays unbounded)
- `inf - inf = nan` (indeterminate)

Understanding these rules prevents silent bugs in numerical pipelines where missing data (`nan`) or overflow (`inf`) can propagate through an entire computation unnoticed.

---

## Exercises

**Exercise 1.** Print the values of `np.pi`, `np.e`, `np.inf`, and `np.nan`. Then check which of these are finite using `np.isfinite()`.

??? success "Solution to Exercise 1"
    ```python
    import numpy as np

    constants = [np.pi, np.e, np.inf, np.nan]
    names = ["pi", "e", "inf", "nan"]

    for name, val in zip(names, constants):
        print(f"np.{name} = {val}, finite: {np.isfinite(val)}")
    ```

---

**Exercise 2.** Predict the output:

```python
import numpy as np
print(np.inf > 1e308)
print(np.nan == np.nan)
print(np.isnan(np.nan))
```

??? success "Solution to Exercise 2"
    ```
    True
    False
    True
    ```

    `np.inf` is greater than any finite number. `np.nan` is not equal to anything, including itself (IEEE 754 standard). `np.isnan()` is the correct way to check for NaN.

---

**Exercise 3.** Create an array `[1.0, np.nan, 3.0, np.nan, 5.0]` and compute the mean using both `np.mean()` and `np.nanmean()`. Explain the difference.

??? success "Solution to Exercise 3"
    ```python
    import numpy as np

    arr = np.array([1.0, np.nan, 3.0, np.nan, 5.0])
    print(np.mean(arr))     # nan (any NaN contaminates the result)
    print(np.nanmean(arr))  # 3.0 (ignores NaN values)
    ```

---

**Exercise 4.** Use `np.pi` and `np.e` to verify Euler's identity: $e^{i\pi} + 1 \approx 0$. Print the result and explain why it is not exactly zero.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np

    result = np.exp(1j * np.pi) + 1
    print(result)           # approximately 0+1.2246e-16j
    print(abs(result))      # approximately 1.2e-16

    # Not exactly zero due to floating-point precision limits
    ```
