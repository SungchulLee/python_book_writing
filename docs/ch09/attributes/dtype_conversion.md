# Changing Dtype

NumPy provides multiple ways to convert array data types.

!!! tip "Mental Model"
    Think of dtype conversion as pouring data from one container shape into another. `astype` always makes a fresh copy with the new type, while specifying `dtype` at creation time avoids the extra copy altogether. Be aware that narrowing conversions (e.g., float to int) silently truncate -- NumPy will not warn you.


## The astype Method

The `astype` method returns a copy with the specified dtype.

### 1. Basic Conversion

```python
import numpy as np

def main():
    x = np.zeros((2, 3))
    y = x.astype(np.uint8)
    print(f"{x.dtype = }")
    print(f"{y.dtype = }")

if __name__ == "__main__":
    main()
```

Output:

```
x.dtype = dtype('float64')
y.dtype = dtype('uint8')
```

### 2. Returns Copy

`astype` always creates a new array; the original is unchanged.


## dtype Keyword

Specify dtype directly during array creation.

### 1. At Creation Time

```python
import numpy as np

def main():
    x = np.array([1, 2, 3])
    print(f"{x.dtype = }", end="\n\n")

    x = np.array([1, 2, 3], dtype=np.uint8)
    print(f"{x.dtype = }", end="\n\n")

    x = np.array([1, 2, 3], dtype=np.float32)
    print(f"{x.dtype = }")

if __name__ == "__main__":
    main()
```

Output:

```
x.dtype = dtype('int64')

x.dtype = dtype('uint8')

x.dtype = dtype('float32')
```

### 2. Efficiency

Specifying dtype at creation avoids an extra conversion step.


## Full Replacement

Reassigning a variable replaces everything, including dtype.

### 1. Complete Override

```python
import numpy as np

def main():
    a = np.zeros(shape=(3,), dtype=np.uint8)
    b = np.array([-0.87796192, -0.97481932, -1.8001195], dtype=np.float64)
    print(f"{a = }")
    print(f"{b = }", end="\n\n")

    a = b
    print(f"{a = }")
    print(f"{b = }")

if __name__ == "__main__":
    main()
```

Output:

```
a = array([0, 0, 0], dtype=uint8)
b = array([-0.87796192, -0.97481932, -1.8001195])

a = array([-0.87796192, -0.97481932, -1.8001195])
b = array([-0.87796192, -0.97481932, -1.8001195])
```

### 2. Name Rebinding

This rebinds the name `a` to a new object; no type coercion occurs.


## Partial Same Dtype

Assigning to a slice with matching dtype works correctly.

### 1. Compatible Types

```python
import numpy as np

def main():
    a = np.zeros(shape=(2, 3), dtype=np.float64)
    b = np.array([-0.87796192, -0.97481932, -1.8001195], dtype=np.float64)
    print(f"{a = }")
    print(f"{b = }", end="\n\n")

    a[0, :] = b
    print(f"{a = }")
    print(f"{b = }")

if __name__ == "__main__":
    main()
```

Output:

```
a = array([[0., 0., 0.],
           [0., 0., 0.]])
b = array([-0.87796192, -0.97481932, -1.8001195])

a = array([[-0.87796192, -0.97481932, -1.8001195],
           [ 0.        ,  0.        ,  0.        ]])
b = array([-0.87796192, -0.97481932, -1.8001195])
```

### 2. No Data Loss

When dtypes match, values are copied exactly.


## Partial Diff Dtype

Assigning to a slice with different dtype causes truncation.

### 1. Truncation Example

```python
import numpy as np

def main():
    a = np.zeros(shape=(2, 3), dtype=np.uint8)
    b = np.array([-0.87796192, -0.97481932, -1.8001195], dtype=np.float64)
    print(f"{a = }")
    print(f"{b = }", end="\n\n")

    a[0, :] = b
    print(f"{a = }")
    print(f"{b = }")

if __name__ == "__main__":
    main()
```

Output:

```
a = array([[0, 0, 0],
           [0, 0, 0]], dtype=uint8)
b = array([-0.87796192, -0.97481932, -1.8001195])

a = array([[0, 0, 0],
           [0, 0, 0]], dtype=uint8)
b = array([-0.87796192, -0.97481932, -1.8001195])
```

### 2. Conversion Rules

```python
import numpy as np

def main():
    print(f"{np.uint8(-0.87796192) = }")
    print(f"{np.uint8(-0.97481932) = }")
    print(f"{np.uint8(-1.8001195) = }")

if __name__ == "__main__":
    main()
```

Output:

```
np.uint8(-0.87796192) = 0
np.uint8(-0.97481932) = 0
np.uint8(-1.8001195) = 255
```

### 3. Warning

Negative floats converting to uint8 produce unexpected results due to overflow.

## Safe vs Unsafe Casting

NumPy distinguishes casting safety levels. Use `np.can_cast` to check before converting:

```python
import numpy as np

print(np.can_cast(np.float64, np.float32))  # True (safe — might lose precision)
print(np.can_cast(np.float64, np.int32))    # False (unsafe — truncates)
print(np.can_cast(np.int32, np.int64))      # True (safe — no data loss)
```

In functions that accept a `casting` parameter, use `casting='safe'` to prevent silent data loss:

```python
# np.add(float_array, int_array, casting='safe')  # raises if unsafe
```

---

## Exercises

**Exercise 1.**
Create a float64 array `a = np.array([1.7, 2.3, 3.9, 4.1])` and convert it to `int32` using `.astype()`. Print both arrays and note which values changed. Then convert the int32 result back to float64 and verify that the original fractional parts are lost.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.array([1.7, 2.3, 3.9, 4.1])
        b = a.astype(np.int32)
        print(a)  # [1.7 2.3 3.9 4.1]
        print(b)  # [1 2 3 4]  (truncated toward zero)

        c = b.astype(np.float64)
        print(c)  # [1. 2. 3. 4.]  — fractional parts are lost

---

**Exercise 2.**
Create an integer array `a = np.array([0, 1, 2, 3])` and convert it to `bool` using `.astype(bool)`. Print the result and explain why only one element becomes `False`. Then convert the boolean array back to `int8` and print the values.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.array([0, 1, 2, 3])
        b = a.astype(bool)
        print(b)  # [False  True  True  True]
        # Only 0 becomes False; all nonzero values become True.

        c = b.astype(np.int8)
        print(c)  # [0 1 1 1]

---

**Exercise 3.**
Create a large array `a = np.arange(1_000_000, dtype=np.float64)` and convert it to `float32`. Compare the `nbytes` of both arrays and compute the memory savings as a percentage.

??? success "Solution to Exercise 3"

        import numpy as np

        a = np.arange(1_000_000, dtype=np.float64)
        b = a.astype(np.float32)

        print(f"float64 nbytes: {a.nbytes:,}")  # 8,000,000
        print(f"float32 nbytes: {b.nbytes:,}")  # 4,000,000

        savings = (1 - b.nbytes / a.nbytes) * 100
        print(f"Memory savings: {savings:.0f}%")  # 50%
