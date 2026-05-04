# Dtype Basics

The `dtype` attribute specifies how array bytes are interpreted.

!!! tip "Mental Model"
    A NumPy array is a flat buffer of bytes; the `dtype` is the lens that tells NumPy how to interpret each chunk of those bytes. Choosing a dtype is like choosing a unit of measurement -- `float64` gives you precision, `uint8` saves memory, and picking wrong silently corrupts your numbers.


## Dtype Reference

NumPy supports many data types with different precision and range.

| Data type     | Description |
|:--------------|:------------|
| `bool_`       | Boolean (True or False) stored as a byte |
| `int_`        | Default integer type (int64 or int32) |
| `int8`        | Byte (-128 to 127) |
| `int16`       | Integer (-32768 to 32767) |
| `int32`       | Integer (-2147483648 to 2147483647) |
| `int64`       | Integer (-9223372036854775808 to 9223372036854775807) |
| `uint8`       | Unsigned integer (0 to 255) |
| `uint16`      | Unsigned integer (0 to 65535) |
| `uint32`      | Unsigned integer (0 to 4294967295) |
| `uint64`      | Unsigned integer (0 to 18446744073709551615) |
| `float16`     | Half precision (sign, 5-bit exp, 10-bit mantissa) |
| `float32`     | Single precision (sign, 8-bit exp, 23-bit mantissa) |
| `float64`     | Double precision (sign, 11-bit exp, 52-bit mantissa) |
| `complex64`   | Complex with two 32-bit floats |
| `complex128`  | Complex with two 64-bit floats |


## Checking Dtype

The `dtype` attribute reveals an array's data type.

### 1. Basic Examples

```python
import numpy as np

def main():
    x = np.array([1, 2, 3])
    y = np.array([1, 2, 3], dtype='uint8')
    z = np.array([1, 2, 3], dtype='float32')
    w = np.array([1., 2, 3])
    print(x.dtype)
    print(y.dtype)
    print(z.dtype)
    print(w.dtype)

if __name__ == "__main__":
    main()
```

Output:

```
int64
uint8
float32
float64
```

### 2. Float Inference

Including a decimal point (`1.`) triggers float64 inference.


## Default Dtypes

Some functions have specific default dtypes.

### 1. zeros and ones

```python
import numpy as np

def main():
    a = np.zeros((2, 3))
    b = np.ones((2, 3))
    print(f"{a.dtype = }")
    print(f"{b.dtype = }")

if __name__ == "__main__":
    main()
```

Output:

```
a.dtype = dtype('float64')
b.dtype = dtype('float64')
```

### 2. float64 Default

`np.zeros` and `np.ones` default to `float64`, not integers.


## MNIST Example

Image datasets commonly use `uint8` for efficiency.

### 1. Loading MNIST

```python
import numpy as np
import matplotlib.pyplot as plt
import torchvision.transforms as transforms
from torchvision.datasets import MNIST

def main():
    train_dataset = MNIST(root='data/', train=True,
                          transform=transforms.ToTensor(),
                          download=True)

    fig, ax = plt.subplots(figsize=(9, 6))
    fig.suptitle(f'{train_dataset.data.dtype = }', fontsize=15)

    img = np.empty((28 * 10, 28 * 15))
    for i in range(10):
        for j in range(15):
            img[i*28:(i+1)*28, j*28:(j+1)*28] = train_dataset.data[i*15+j]
    ax.imshow(img, cmap='binary')
    ax.axis('off')
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Why uint8

8-bit unsigned integers (0-255) perfectly represent pixel intensities.


## Framework Comparison

Different frameworks have different default integer types.

### 1. NumPy Default

```python
import numpy as np

a = np.array([1, 2, 3])      # int64
b = np.array([1., 2, 3])     # float64
c = a + b
print(c)
```

### 2. PyTorch Default

```python
import torch

a = torch.tensor([1, 2, 3])    # int64 (or int32)
b = torch.tensor([1., 2, 3])   # float32
# c = a + b  # Error: different types
```

### 3. TensorFlow Default

```python
import tensorflow as tf

a = tf.constant([1, 2, 3])     # int32
b = tf.constant([1., 2, 3])    # float32
# c = a + b  # Error: different types
```

NumPy promotes types automatically; PyTorch and TensorFlow require explicit conversion.

## Common Dtype Pitfalls

!!! warning "Overflow and Precision"

    **uint8 wraparound**: values outside 0--255 silently wrap around. `np.uint8(256)` becomes `0`, `np.uint8(-1)` becomes `255`. This is the most common bug in image processing pipelines.

    **float32 precision loss**: `float32` has ~7 decimal digits of precision. In iterative algorithms (gradient descent, cumulative sums), rounding errors accumulate. Use `float64` when precision matters more than memory.

    **Integer overflow**: `np.int8(127) + np.int8(1)` wraps to `-128` with no warning.

| Dtype | Bytes | Use when | Avoid when |
|---|---|---|---|
| `float32` | 4 | GPU training, images | High-precision numerics |
| `float64` | 8 | Scientific computing | Memory-constrained workloads |
| `uint8` | 1 | Image pixels (0--255) | Arithmetic that may exceed 0--255 |
| `int64` | 8 | General integers | Memory-critical large arrays |

---



---

## Notebook Examples

```python
import numpy as np

a = np.array([1,2,3])
b = np.array([4,5,6])
c = a + b # vector addition

print(a.dtype, b.dtype, c.dtype)
```

```python
import numpy as np

a = np.array([1,2,3.])
b = np.array([4,5,6])
c = a + b # vector addition

print(a.dtype, b.dtype, c.dtype)
```

```python
import torch

x = torch.tensor([1,2,3])
print(x, x.dtype)
```

```python
import torch

x = torch.tensor([1,2,3.])
print(x, x.dtype)
```

```python
import torch
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

# Transform: convert images to tensor
transform = transforms.ToTensor()

# Download MNIST
mnist = datasets.MNIST(root="./data", train=True, download=True, transform=None)

# Get first 64 images
images = [mnist[i][0] for i in range(64)]  # (image, label)

# Plot
fig, axes = plt.subplots(8, 8, figsize=(8, 8))

for i, ax in enumerate(axes.flat):
    #ax.imshow(images[i].squeeze(), cmap="binary")
    ax.imshow(images[i], cmap="binary")
    ax.axis("off")

plt.tight_layout()
plt.show()
```

```python
from torchvision import datasets
import numpy as np

# Download MNIST (no transform → raw PIL images)
mnist = datasets.MNIST(root="./data", train=True, download=True, transform=None)

# Get one image
img, label = mnist[0]

# Convert to NumPy
img_np = np.array(img)

# Check dtype
print("Type:", type(img))
print("NumPy dtype:", img_np.dtype)
print("Min/Max:", img_np.min(), img_np.max())
```

---

## Exercises

**Exercise 1.**
Create a NumPy array from the Python list `[1, 2.5, 3, 4.0]` and print its dtype. Then create the same array with an explicit `dtype=np.int32` and print the resulting values to observe the truncation behavior.

??? success "Solution to Exercise 1"

        import numpy as np

        # Default dtype inference
        a = np.array([1, 2.5, 3, 4.0])
        print(a.dtype)   # float64 (because 2.5 and 4.0 are floats)
        print(a)          # [1.  2.5 3.  4. ]

        # Explicit int32 dtype — floats are truncated
        b = np.array([1, 2.5, 3, 4.0], dtype=np.int32)
        print(b.dtype)   # int32
        print(b)          # [1 2 3 4]  (2.5 truncated to 2)

---

**Exercise 2.**
Given an array `a = np.array([100, 200, 300], dtype=np.int16)`, check whether the dtype is an integer kind using the `.kind` attribute. Then print the `itemsize` and verify that the total memory (`nbytes`) equals `len(a) * itemsize`.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.array([100, 200, 300], dtype=np.int16)

        # Check integer kind
        print(a.dtype.kind)      # 'i' (signed integer)
        print(a.dtype.itemsize)  # 2 (bytes per element)

        # Verify total memory
        print(a.nbytes)                        # 6
        print(len(a) * a.dtype.itemsize)       # 6
        print(a.nbytes == len(a) * a.dtype.itemsize)  # True

---

**Exercise 3.**
Create two arrays: `x = np.array([1, 2, 3], dtype=np.float32)` and `y = np.array([4, 5, 6], dtype=np.float64)`. Compute `z = x + y` and print the dtype of `z`. Explain why NumPy chose that dtype by referencing the type promotion rules.

??? success "Solution to Exercise 3"

        import numpy as np

        x = np.array([1, 2, 3], dtype=np.float32)
        y = np.array([4, 5, 6], dtype=np.float64)
        z = x + y
        print(z.dtype)  # float64

        # Explanation: NumPy promotes to the higher-precision type.
        # float32 + float64 -> float64, following the rule that
        # the result dtype is the smallest type that can safely
        # represent both operands.
