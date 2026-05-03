# Bool as Subclass

In Python, `bool` is a subclass of `int`, giving boolean values numeric properties.

!!! tip "Mental Model"
    `True` is literally the integer `1` and `False` is literally `0`, just wearing a boolean costume. Because `bool` inherits from `int`, booleans participate in arithmetic, indexing, and summation. `sum(bool_list)` counts `True` values precisely because each `True` adds 1.

---

## Numeric Behavior

Boolean values exhibit numeric behavior and participate in arithmetic operations.

### 1. Subclass of int

```python
print(True + 1)  # Output: 2
print(False * 5)  # Output: 0
print(isinstance(True, int))  # Output: True
```

### 2. Internal Values

`True` and `False` are internally represented as `1` and `0`:

```python
print(True == 1)   # True
print(False == 0)  # True
```

### 3. Arithmetic Use

Boolean values can be used in arithmetic computations:

```python
x = True
y = False
print(x + y)  # Output: 1 (since True is 1 and False is 0)
```

---

## Type Coercion

Since `bool` is a subclass of `int`, it follows standard type coercion rules.

### 1. Implicit Conversion

```python
print(3 * True)   # Output: 3
print(10 - False) # Output: 10
```

### 2. Coercion Rules

Boolean values seamlessly integrate with other numeric types without explicit conversion.

---

## Type Checking

Explicit type checking can prevent unintended behavior.

### 1. isinstance Check

```python
value = True
if isinstance(value, bool):
    print("This is a boolean value.")
```

### 2. Strict Checking

Use `isinstance` when strict type differentiation is required.

---

## Design Implications

The bool-int relationship has important consequences.

### 1. Performance

Allows efficient boolean computations in numerical algorithms.

### 2. Integration

Facilitates seamless integration into arithmetic expressions and logical computations.

### 3. Caution Needed

This feature necessitates caution in contexts where strict type differentiation is required.

---

## Conclusion

While `bool` is distinct semantically (representing truth, not numbers), its inheritance from `int` enables powerful numeric operations and optimizations in Python code.

---

## Exercises


**Exercise 1.**
Without running the code, predict the output. Then verify.

```python
print(True + True + True)
print(True * 10)
print(False * 100)
print(isinstance(True, int))
```

??? success "Solution to Exercise 1"

        ```python
        print(True + True + True)    # 3
        print(True * 10)             # 10
        print(False * 100)           # 0
        print(isinstance(True, int)) # True
        ```

    Since `bool` is a subclass of `int`, `True` behaves as `1` and `False` as `0` in arithmetic operations. `isinstance(True, int)` returns `True` because of the inheritance relationship.

---

**Exercise 2.**
Write a function `count_true(values)` that takes a list of booleans and returns the count of `True` values. Do this in two ways: once using `sum()`, and once without using `sum()`.

??? success "Solution to Exercise 2"

        ```python
        def count_true_sum(values):
            return sum(values)

        def count_true_loop(values):
            count = 0
            for v in values:
                if v:
                    count += 1
            return count

        data = [True, False, True, True, False]
        print(count_true_sum(data))   # 3
        print(count_true_loop(data))  # 3
        ```

    `sum()` works because `True` is `1` and `False` is `0`. The loop version explicitly checks each value.

---

**Exercise 3.**
Explain why `True == 1` and `True is not 1` can both be true at the same time. Write code demonstrating both.

??? success "Solution to Exercise 3"

        ```python
        print(True == 1)       # True  (value equality)
        print(True is 1)       # False (different objects in CPython 3.12+)
        print(type(True))      # <class 'bool'>
        print(type(1))         # <class 'int'>
        ```

    `==` compares values: `True` and `1` have the same value. `is` compares object identity: `True` is a `bool` singleton and `1` is an `int` object. They are equal in value but may be different objects in memory. Note that in some CPython versions, `True is 1` may return `True` due to integer caching, but this behavior should not be relied upon.
