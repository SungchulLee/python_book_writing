# dtype and Shape

!!! tip "Mental Model"
    Every `ndarray` is defined by two metadata attributes: `dtype` (what kind of number each element is) and `shape` (how the flat buffer is folded into dimensions). Together they fully describe the array's structure, and most NumPy errors trace back to a mismatch in one or both.

    The deeper insight: `dtype` is the **interpretation of bytes** (the same 4 bytes
    can be a float32 or an int32) and `shape` is the **interpretation of structure**
    (the same 12 elements can be a (3,4) matrix or a (2,6) matrix). Changing either
    reinterprets existing data without moving it.

## Type System

### 1. Built-in dtypes

NumPy provides a rich type system:

```python
import numpy as np

# Integer types
int8 = np.array([1, 2], dtype=np.int8)     # -128 to 127
int16 = np.array([1, 2], dtype=np.int16)   # -32768 to 32767
int32 = np.array([1, 2], dtype=np.int32)
int64 = np.array([1, 2], dtype=np.int64)   # Default integer

# Unsigned integers
uint8 = np.array([1, 2], dtype=np.uint8)   # 0 to 255
uint16 = np.array([1, 2], dtype=np.uint16)

# Floating point
float16 = np.array([1.0], dtype=np.float16)  # Half precision
float32 = np.array([1.0], dtype=np.float32)  # Single precision
float64 = np.array([1.0], dtype=np.float64)  # Double (default)

# Complex
complex64 = np.array([1+2j], dtype=np.complex64)
complex128 = np.array([1+2j], dtype=np.complex128)

# Boolean
bool_arr = np.array([True, False], dtype=np.bool_)

# String
str_arr = np.array(['a', 'b'], dtype='U10')  # Unicode, max 10 chars
```

### 2. Type Inspection

```python
arr = np.array([1, 2, 3])
print(arr.dtype)       # dtype('int64')
print(arr.dtype.name)  # 'int64'
print(arr.dtype.kind)  # 'i' (integer)
print(arr.dtype.itemsize)  # 8 bytes
```

### 3. Type Casting

```python
# Implicit upcasting
arr1 = np.array([1, 2, 3])       # int64
arr2 = np.array([1.0, 2.0, 3.0]) # float64
result = arr1 + arr2             # float64 (upcast)

# Explicit casting
arr_int = np.array([1.5, 2.7, 3.9])
arr_int_cast = arr_int.astype(np.int32)  # [1, 2, 3]

# Safe casting check
can_cast = np.can_cast(np.float64, np.int32)
print(can_cast)  # False
```

## Shape Metadata

### 1. Dimension Properties

```python
# 1D array
arr1d = np.array([1, 2, 3, 4])
print(arr1d.shape)  # (4,)
print(arr1d.ndim)   # 1

# 2D array
arr2d = np.array([[1, 2, 3], [4, 5, 6]])
print(arr2d.shape)  # (2, 3)
print(arr2d.ndim)   # 2

# 3D array
arr3d = np.arange(24).reshape(2, 3, 4)
print(arr3d.shape)  # (2, 3, 4)
print(arr3d.ndim)   # 3
```

### 2. Reshaping

```python
arr = np.arange(12)

# Explicit shape
reshaped = arr.reshape(3, 4)
print(reshaped.shape)  # (3, 4)

# Infer one dimension
reshaped = arr.reshape(3, -1)  # (3, 4) inferred
reshaped = arr.reshape(-1, 4)  # (3, 4) inferred

# Flatten
flat = reshaped.reshape(-1)  # (12,)
```

### 3. Dimension Manipulation

```python
arr = np.array([1, 2, 3])

# Add dimension
arr_2d = arr[np.newaxis, :]  # (1, 3)
arr_2d = arr[:, np.newaxis]  # (3, 1)

# Using reshape
arr_2d = arr.reshape(1, -1)  # (1, 3)
arr_2d = arr.reshape(-1, 1)  # (3, 1)

# Squeeze (remove size-1 dimensions)
arr_squeezed = np.array([[[1, 2, 3]]])  # (1, 1, 3)
print(arr_squeezed.squeeze().shape)     # (3,)
```

## Structured dtypes

### 1. Record Arrays

```python
# Define structured dtype
dt = np.dtype([('name', 'U10'), ('age', 'i4'), ('weight', 'f4')])

# Create array
data = np.array([
    ('Alice', 25, 55.5),
    ('Bob', 30, 75.0)
], dtype=dt)

print(data['name'])    # ['Alice' 'Bob']
print(data['age'])     # [25 30]
print(data[0])         # ('Alice', 25, 55.5)
```

### 2. Field Access

```python
# Access by field
ages = data['age']
ages[0] = 26
print(data[0]['age'])  # 26 - structured array is a view
```

### 3. Nested Structures

```python
dt = np.dtype([
    ('name', 'U10'),
    ('position', [('x', 'f4'), ('y', 'f4')])
])

data = np.array([
    ('Alice', (1.0, 2.0)),
    ('Bob', (3.0, 4.0))
], dtype=dt)

print(data['position']['x'])  # [1. 3.]
```

## Type Promotion

### 1. Automatic Promotion

```python
# Integer + Float → Float
arr_int = np.array([1, 2, 3])
arr_float = np.array([1.0, 2.0, 3.0])
result = arr_int + arr_float
print(result.dtype)  # float64

# Smaller + Larger → Larger
arr_8 = np.array([1], dtype=np.int8)
arr_64 = np.array([1], dtype=np.int64)
result = arr_8 + arr_64
print(result.dtype)  # int64
```

### 2. Result Type

```python
# Check result dtype before operation
result_dtype = np.result_type(np.int8, np.float32)
print(result_dtype)  # float32
```

### 3. Promotion Rules

```python
# bool < int < float < complex
print(np.result_type(np.bool_, np.int32))     # int32
print(np.result_type(np.int32, np.float64))   # float64
print(np.result_type(np.float32, np.complex64))  # complex64
```

## Memory Efficiency

### 1. Choosing dtypes

```python
# Small integers - use smaller types
small_ints = np.arange(100, dtype=np.int8)  # 100 bytes
large_ints = np.arange(100, dtype=np.int64) # 800 bytes

# Precision trade-offs
half = np.array([1.0], dtype=np.float16)    # 2 bytes, less precision
double = np.array([1.0], dtype=np.float64)  # 8 bytes, more precision
```

### 2. String Optimization

```python
# Fixed-length strings
arr = np.array(['a', 'bb', 'ccc'], dtype='U3')  # 3 chars max
print(arr.dtype)  # '<U3'
print(arr.nbytes) # 36 bytes (3 items × 3 chars × 4 bytes/char)

# Oversized strings waste memory
arr_big = np.array(['a', 'bb', 'ccc'], dtype='U100')  # wasteful
print(arr_big.nbytes)  # 1200 bytes
```

### 3. Boolean Masking

```python
# Boolean arrays are memory efficient for masks
arr = np.arange(1000000)
mask = arr > 500000  # dtype=bool, 1 byte per element
filtered = arr[mask]
```

## Shape Broadcasting

### 1. Dimension Compatibility

```python
# Same shape - compatible
arr1 = np.ones((3, 4))
arr2 = np.ones((3, 4))
result = arr1 + arr2  # ✅ (3, 4)

# Trailing dimensions match
arr1 = np.ones((5, 3, 4))
arr2 = np.ones((3, 4))
result = arr1 + arr2  # ✅ (5, 3, 4)

# Size-1 dimensions stretch
arr1 = np.ones((3, 1))
arr2 = np.ones((1, 4))
result = arr1 + arr2  # ✅ (3, 4)
```

### 2. Shape Rules

Broadcasting works when:
- Dimensions are equal, or
- One dimension is 1, or
- Dimension doesn't exist (added as size 1)

```python
# (3, 4) + (4,) → (3, 4) + (1, 4) → (3, 4) ✅
# (3, 4) + (3,) → incompatible ❌
# (3, 4) + (3, 1) → (3, 4) ✅
```

### 3. Explicit Broadcasting

```python
arr1 = np.array([[1], [2], [3]])  # (3, 1)
arr2 = np.array([10, 20, 30])     # (3,)

# Manual broadcast
arr2_broadcast = arr2[np.newaxis, :]  # (1, 3)
result = arr1 + arr2_broadcast        # (3, 3)
```

---

## Exercises

**Exercise 1.** Write a short code example that demonstrates the main concept covered on this page. Include comments explaining each step.

??? success "Solution to Exercise 1"
    Refer to the code examples in the page content above. A complete solution would recreate the key pattern with clear comments explaining the NumPy operations involved.

---

**Exercise 2.** Predict the output of a code snippet that uses the features described on this page. Explain why the output is what it is.

??? success "Solution to Exercise 2"
    The output depends on how NumPy handles the specific operation. Key factors include array shapes, dtypes, and broadcasting rules. Trace through the computation step by step.

---

**Exercise 3.** Write a practical function that applies the concepts from this page to solve a real data processing task. Test it with sample data.

??? success "Solution to Exercise 3"
    ```python
    import numpy as np

    # Example: apply the page's concept to process sample data
    data = np.random.default_rng(42).random((5, 3))
    # Apply the relevant operation
    result = data  # replace with actual operation
    print(result)
    ```

---

**Exercise 4.** Identify a common mistake when using the features described on this page. Write code that demonstrates the mistake and then show the corrected version.

??? success "Solution to Exercise 4"
    A common mistake is misunderstanding array shapes or dtypes. Always check `.shape` and `.dtype` when debugging unexpected results.
