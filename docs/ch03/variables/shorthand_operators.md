# Shorthand Operators

!!! tip "Mental Model"
    `x += y` looks like a shortcut for `x = x + y`, and for immutable types it behaves identically -- a new object is created and rebound to `x`. But for mutable types like lists, `+=` calls `__iadd__`, which mutates the object in place. This distinction matters when multiple names reference the same mutable object.

## Augmented Assignment

### 1. Arithmetic

| Operator | Equivalent | Description |
|:---------|:-----------|:------------|
| `+=` | `x = x + y` | Add and assign |
| `-=` | `x = x - y` | Subtract |
| `*=` | `x = x * y` | Multiply |
| `/=` | `x = x / y` | Divide |
| `//=` | `x = x // y` | Floor divide |
| `%=` | `x = x % y` | Modulus |
| `**=` | `x = x ** y` | Power |

### 2. Bitwise

| Operator | Equivalent | Description |
|:---------|:-----------|:------------|
| `&=` | `x = x & y` | Bitwise AND |
| `\|=` | `x = x \| y` | Bitwise OR |
| `^=` | `x = x ^ y` | Bitwise XOR |
| `>>=` | `x = x >> y` | Right shift |
| `<<=` | `x = x << y` | Left shift |

## Immutable Types

### 1. Integers

```python
i = 9
print(f"{id(i) = }")

i = i + 3
print(f"{i = }")      # i = 12
print(f"{id(i) = }")  # Different ID

# vs shorthand
i = 9
original_id = id(i)
i += 3
print(f"{i = }")      # i = 12
print(f"{id(i) != original_id = }")  # True
```

### 2. Strings

```python
s = "hello"
original_id = id(s)

s = s + " world"
print(f"{id(s) != original_id = }")  # True

# Shorthand also creates new
s = "hello"
original_id = id(s)
s += " world"
print(f"{id(s) != original_id = }")  # True
```

## Mutable Types

### 1. Lists In-Place

```python
lst = [1, 2, 3]
original_id = id(lst)

# += modifies in-place
lst += [4, 5]
print(f"{lst = }")  # lst = [1, 2, 3, 4, 5]
print(f"{id(lst) == original_id = }")  # True
```

### 2. Lists New Object

```python
lst = [1, 2, 3]
original_id = id(lst)

# + creates new list
lst = lst + [4, 5]
print(f"{lst = }")  # lst = [1, 2, 3, 4, 5]
print(f"{id(lst) != original_id = }")  # True
```

## Behavior Summary

### 1. Immutable

For `int`, `str`, `tuple`:

```python
x = 10
# Both create new objects
x = x + 1   # New object
x += 1      # New object
```

### 2. Mutable

For `list`, `dict`, `set`:

```python
x = [1, 2]
x += [3]      # In-place (same object)
x = x + [3]   # New object
```

## Practical Examples

### 1. Counter Pattern

```python
count = 0
for i in range(10):
    count += 1
print(f"{count = }")  # count = 10
```

### 2. Accumulator

```python
total = 0
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    total += num
print(f"{total = }")  # total = 15
```

### 3. String Building

```python
# Inefficient
result = ""
for i in range(5):
    result += str(i)
print(result)  # "01234"

# Better: use join
result = "".join(str(i) for i in range(5))
print(result)  # "01234"
```

## Special Cases

### 1. List Extend

```python
# These are equivalent
lst = [1, 2, 3]
lst += [4, 5]  # Calls __iadd__
# Same as: lst.extend([4, 5])
```

### 2. Set Operations

```python
s = {1, 2, 3}
s |= {3, 4, 5}  # Union
print(s)  # {1, 2, 3, 4, 5}

s &= {3, 4}  # Intersection
print(s)  # {3, 4}
```

### 3. Dictionary Update

```python
d = {'a': 1}
d |= {'b': 2}  # Python 3.9+
print(d)  # {'a': 1, 'b': 2}
```

## Performance Notes

### 1. In-Place Faster

```python
# Faster for large lists
big_list = list(range(1000000))
big_list += [1000000]  # In-place

# Slower (creates new)
big_list = big_list + [1000000]
```

### 2. String Concat

```python
# Slow for many iterations
s = ""
for i in range(1000):
    s += str(i)  # 1000 objects

# Fast
s = "".join(str(i) for i in range(1000))
```


---

## Exercises


**Exercise 1.**
Show the difference between `+=` and `+` for lists. Create a list, use `+=` to extend it, and show the `id()` does not change. Then use `+` and show the `id()` does change.

??? success "Solution to Exercise 1"

    ```python
    # += modifies in place (same object)
    lst = [1, 2, 3]
    original_id = id(lst)
    lst += [4, 5]
    print(f"Same object: {id(lst) == original_id}")  # True

    # + creates new object
    lst = [1, 2, 3]
    original_id = id(lst)
    lst = lst + [4, 5]
    print(f"Same object: {id(lst) == original_id}")  # False
    ```

    For mutable types like lists, `+=` calls `__iadd__` (in-place addition). The `+` operator calls `__add__` and creates a new list.

---

**Exercise 2.**
Write a loop that computes the sum of squares from 1 to 100 using the `+=` operator. Then show the equivalent one-liner using `sum()` with a generator.

??? success "Solution to Exercise 2"

    ```python
    # Using += in a loop
    total = 0
    for i in range(1, 101):
        total += i ** 2
    print(total)  # 338350

    # One-liner equivalent
    print(sum(i ** 2 for i in range(1, 101)))  # 338350
    ```

    Both approaches compute the same result. The `sum()` with generator is more Pythonic and avoids the explicit loop.

---

**Exercise 3.**
Demonstrate that `+=` on a string creates a new object (since strings are immutable) by checking the `id()` before and after the operation.

??? success "Solution to Exercise 3"

    ```python
    s = "hello"
    original_id = id(s)
    s += " world"
    print(f"Same object: {id(s) == original_id}")  # False
    print(s)  # hello world
    ```

    Strings are immutable, so `+=` cannot modify the original object. Python creates a new string and rebinds the variable to it.
