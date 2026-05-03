# Type Conversion

!!! tip "Mental Model"
    Type conversion creates a new object of the target type from an existing value. `int("42")` builds a new `int` from a string; `str(42)` builds a new string from an int. The original object is never modified. Conversion can fail at runtime if the value is not representable in the target type -- `int("hello")` raises `ValueError`.

## Built-in Converters

### 1. To Integer

```python
x = int("42")       # From string
y = int(3.7)        # From float (truncates)
z = int(True)       # From bool
print(x, y, z)      # 42 3 1
```

### 2. To Float

```python
x = float("3.14")
y = float(42)
z = float(True)
print(x, y, z)      # 3.14 42.0 1.0
```

### 3. To String

```python
x = str(42)
y = str(3.14)
z = str([1, 2, 3])
print(x, y, z)      # "42" "3.14" "[1, 2, 3]"
```

## Collection Conversion

### 1. To List

```python
x = list((1, 2, 3))        # From tuple
y = list("hello")          # From string  
z = list(range(5))         # From range
print(x, y, z)
```

### 2. To Tuple/Set

```python
x = tuple([1, 2, 3])
y = set([1, 2, 2, 3])      # Removes duplicates
print(x, y)                # (1, 2, 3) {1, 2, 3}
```

### 3. To Dict

```python
x = dict([('a', 1), ('b', 2)])
keys = ['x', 'y']
values = [1, 2]
y = dict(zip(keys, values))
print(x, y)
```

## Numeric Conversion

### 1. Base Conversion

```python
x = int('1010', 2)         # Binary to int
y = int('FF', 16)          # Hex to int
print(x, y)                # 10 255
```

### 2. Int to Base

```python
print(bin(10))             # '0b1010'
print(hex(255))            # '0xff'
print(oct(63))             # '0o77'
```

## Error Handling

### 1. Safe Conversion

```python
def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

print(safe_int("42"))      # 42
print(safe_int("bad"))     # 0
```

## Boolean Conversion

### 1. Truthy/Falsy

```python
print(bool(1))             # True
print(bool(0))             # False
print(bool(""))            # False
print(bool([]))            # False
print(bool(None))          # False
```

## Conversion Table

| From | To | Function |
|------|-----|----------|
| str | int | `int()` |
| str | float | `float()` |
| int | str | `str()` |
| list | tuple | `tuple()` |
| list | set | `set()` |


---

## Exercises


**Exercise 1.**
Write a function `safe_convert(value, target_type)` that attempts to convert `value` to `target_type` (e.g., `int`, `float`, `str`). If conversion fails, return `None` instead of raising an error.

??? success "Solution to Exercise 1"

    ```python
    def safe_convert(value, target_type):
        try:
            return target_type(value)
        except (ValueError, TypeError):
            return None

    print(safe_convert("42", int))      # 42
    print(safe_convert("hello", int))   # None
    print(safe_convert("3.14", float))  # 3.14
    print(safe_convert(42, str))        # '42'
    ```

    The `try/except` block catches both `ValueError` (invalid literal) and `TypeError` (unsupported conversion) to provide safe conversion.

---

**Exercise 2.**
Demonstrate the difference between `int(3.9)` (truncation) and `round(3.9)` (rounding). Then show how to use `math.floor()` and `math.ceil()` for explicit directional conversion.

??? success "Solution to Exercise 2"

    ```python
    import math

    print(int(3.9))         # 3 (truncates toward zero)
    print(round(3.9))       # 4 (rounds to nearest)
    print(math.floor(3.9))  # 3 (rounds toward -inf)
    print(math.ceil(3.9))   # 4 (rounds toward +inf)

    # Negative number
    print(int(-3.9))         # -3 (truncates toward zero)
    print(math.floor(-3.9))  # -4 (rounds toward -inf)
    ```

    `int()` truncates toward zero, `math.floor()` rounds toward negative infinity, and `math.ceil()` rounds toward positive infinity. The difference is visible with negative numbers.

---

**Exercise 3.**
Convert the list `[1, 2, 2, 3, 3, 3]` to a `set`, then to a sorted `list`, then to a `tuple`. Print the result at each step and explain what each conversion does.

??? success "Solution to Exercise 3"

    ```python
    original = [1, 2, 2, 3, 3, 3]

    as_set = set(original)
    print(f"Set: {as_set}")          # {1, 2, 3} (duplicates removed)

    as_sorted_list = sorted(as_set)
    print(f"Sorted list: {as_sorted_list}")  # [1, 2, 3]

    as_tuple = tuple(as_sorted_list)
    print(f"Tuple: {as_tuple}")      # (1, 2, 3)
    ```

    `set()` removes duplicates, `sorted()` returns a new sorted list, and `tuple()` converts the list to an immutable tuple.
