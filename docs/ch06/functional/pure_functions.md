# Pure Functions

!!! tip "Mental Model"
    A pure function is a reliable black box: same inputs always produce the same output, and nothing outside the function changes. No printing, no modifying globals, no mutating arguments. This predictability makes pure functions trivially testable, safely cacheable, and easy to reason about.

## Definition

### 1. No Side Effects

```python
# Pure
def add(x, y):
    return x + y

# Impure
def add_and_print(x, y):
    print(f"Adding {x} and {y}")  # Side effect
    return x + y
```

### 2. Same Input → Same Output

```python
# Pure
def square(x):
    return x ** 2

# Impure
import random
def random_square(x):
    return x ** 2 + random.randint(0, 10)
```

## Benefits

### 1. Testable

```python
# Easy to test
def multiply(x, y):
    return x * y

assert multiply(3, 4) == 12
```

### 2. Cacheable

```python
@lru_cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

## Summary

- No side effects
- Deterministic
- Easy to test
- Cacheable

---

## Exercises

**Exercise 1.**
Identify which of the following functions are pure and which are impure. Explain why for each:
(a) `def add(x, y): return x + y`
(b) `def append_to(lst, item): lst.append(item); return lst`
(c) `def greet(name): print(f"Hello, {name}"); return name`
(d) `def square(x): return x * x`

??? success "Solution to Exercise 1"

        # (a) PURE — no side effects, same input always gives same output
        def add(x, y):
            return x + y

        # (b) IMPURE — mutates the input list (side effect)
        def append_to(lst, item):
            lst.append(item)
            return lst

        # (c) IMPURE — print() is a side effect (I/O)
        def greet(name):
            print(f"Hello, {name}")
            return name

        # (d) PURE — no side effects, deterministic
        def square(x):
            return x * x

---

**Exercise 2.**
Refactor this impure function into a pure one:
```python
total = 0
def add_to_total(x):
    global total
    total += x
    return total
```
The pure version should accept the current total as a parameter and return the new total without modifying any global state.

??? success "Solution to Exercise 2"

        # Impure version (uses global state)
        # total = 0
        # def add_to_total(x):
        #     global total
        #     total += x
        #     return total

        # Pure version
        def add_to_total(current_total, x):
            return current_total + x

        total = 0
        total = add_to_total(total, 5)
        print(total)  # 5
        total = add_to_total(total, 3)
        print(total)  # 8

        # Same inputs always produce the same output
        print(add_to_total(0, 5))   # 5
        print(add_to_total(0, 5))   # 5 (deterministic)

---

**Exercise 3.**
Write a pure function `transform_records(records, key, func)` that takes a list of dictionaries, a key name, and a transformation function. It should return a new list of dictionaries where the specified key's value has been transformed, without modifying the originals. Demonstrate with a list of `{"name": ..., "score": ...}` records and a function that doubles the score.

??? success "Solution to Exercise 3"

        def transform_records(records, key, func):
            """Return new records with key transformed. Does not mutate originals."""
            return [
                {**record, key: func(record[key])}
                for record in records
            ]

        students = [
            {"name": "Alice", "score": 85},
            {"name": "Bob", "score": 70},
        ]

        doubled = transform_records(students, "score", lambda s: s * 2)
        print(doubled)
        # [{'name': 'Alice', 'score': 170}, {'name': 'Bob', 'score': 140}]

        # Originals unchanged
        print(students)
        # [{'name': 'Alice', 'score': 85}, {'name': 'Bob', 'score': 70}]
