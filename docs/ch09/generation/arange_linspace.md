# arange and linspace

NumPy provides two primary functions for generating sequences of numbers: `np.arange` for integer steps and `np.linspace` for evenly spaced floats.

!!! tip "Mental Model"
    Use `arange` when you know the step size and `linspace` when you know the number of points. `arange` excludes the endpoint like Python's `range`, while `linspace` includes it by default. For floating-point grids, `linspace` is almost always safer because it guarantees the exact count of points.

!!! warning "Floating-Point Implications"
    `arange` computes each value by repeatedly adding the step, which can **accumulate floating-point error** — the final element may drift from the expected endpoint. `linspace` computes each value independently as `start + i * (stop - start) / (num - 1)`, so it produces **deterministic, reproducible grids** regardless of the number of points. For continuous-domain sampling (plotting, FFT grids, numerical integration), always prefer `linspace`.


## np.arange Function

Generates values within a half-open interval `[start, stop)` with a given step.

### 1. Single Argument

```python
import numpy as np

def main():
    a = np.arange(9)
    print("np.arange(9)")
    print(a)

if __name__ == "__main__":
    main()
```

Output:

```
np.arange(9)
[0 1 2 3 4 5 6 7 8]
```

### 2. Two Arguments

```python
import numpy as np

def main():
    a = np.arange(1, 9)
    print("np.arange(1, 9)")
    print(a)

if __name__ == "__main__":
    main()
```

Output:

```
np.arange(1, 9)
[1 2 3 4 5 6 7 8]
```

### 3. Three Arguments

```python
import numpy as np

def main():
    a = np.arange(1, 9, 2)
    print("np.arange(1, 9, 2)")
    print(a)

if __name__ == "__main__":
    main()
```

Output:

```
np.arange(1, 9, 2)
[1 3 5 7]
```


## np.linspace Function

Generates evenly spaced numbers over a closed interval `[start, stop]`.

### 1. Default Samples

```python
import numpy as np

def main():
    a = np.linspace(-1, 2)
    print("np.linspace(-1, 2)")
    print(a)

if __name__ == "__main__":
    main()
```

Default is 50 evenly spaced samples.

### 2. Custom Samples

```python
import numpy as np

def main():
    a = np.linspace(-1, 2, 4)
    print("np.linspace(-1, 2, 4)")
    print(a)

if __name__ == "__main__":
    main()
```

Output:

```
np.linspace(-1, 2, 4)
[-1.  0.  1.  2.]
```


## Key Differences

Understanding when to use each function is essential.

### 1. Endpoint Inclusion

`np.arange` excludes the endpoint; `np.linspace` includes it by default.

### 2. Parameter Meaning

`np.arange` specifies step size; `np.linspace` specifies number of samples.

### 3. Typical Use Cases

Use `np.arange` for integer sequences and `np.linspace` for continuous intervals.


## Floating Point Caution

Using `np.arange` with floats can produce unexpected results.

### 1. Rounding Issues

```python
import numpy as np

a = np.arange(0, 1, 0.1)
print(len(a))  # May vary due to floating-point precision
```

### 2. Recommendation

For floating-point sequences, prefer `np.linspace` to guarantee exact sample count.


## Scientific Computing

Both functions are essential for numerical computations.

### 1. Plotting Curves

```python
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)
```

### 2. Index Arrays

```python
import numpy as np

indices = np.arange(len(data))
```

### 3. Grid Generation

`np.linspace` combined with `np.meshgrid` creates 2D coordinate grids.

---

## Exercises

**Exercise 1.**
Create an array of all odd numbers from 1 to 99 (inclusive) using `np.arange`. Verify the result has exactly 50 elements and the last element is 99.

??? success "Solution to Exercise 1"

        import numpy as np

        odds = np.arange(1, 100, 2)
        print(f"Length: {len(odds)}")     # 50
        print(f"Last element: {odds[-1]}") # 99

---

**Exercise 2.**
Using `np.linspace`, create an array of 5 evenly spaced values from 0 to 1 (inclusive). Then create the same array using `np.arange` with an appropriate step size. Print both arrays and verify they are equal with `np.allclose`.

??? success "Solution to Exercise 2"

        import numpy as np

        a_linspace = np.linspace(0, 1, 5)
        a_arange = np.arange(0, 1.25, 0.25)

        print(f"linspace: {a_linspace}")
        print(f"arange:   {a_arange}")
        print(f"Equal: {np.allclose(a_linspace, a_arange)}")

---

**Exercise 3.**
Demonstrate the floating-point issue with `np.arange(0, 1, 0.3)`. Print the resulting array and its length. Then produce an equivalent result using `np.linspace` that guarantees exactly 4 evenly spaced values from 0 to 0.9 (inclusive).

??? success "Solution to Exercise 3"

        import numpy as np

        # arange with float step — unpredictable length
        a = np.arange(0, 1, 0.3)
        print(f"arange result: {a}")
        print(f"Length: {len(a)}")  # may be 3 or 4

        # linspace guarantees exact count
        b = np.linspace(0, 0.9, 4)
        print(f"linspace result: {b}")
        print(f"Length: {len(b)}")  # always 4
