# Map Filter Reduce

!!! tip "Mental Model"
    `map` transforms every element, `filter` selects elements that pass a test, and `reduce` collapses a sequence into a single value. Together they form the classic functional trio: transform, select, accumulate. In modern Python, list comprehensions often replace `map` and `filter`, but understanding these primitives clarifies how data flows through pipelines.

## map()

### 1. Transform Elements

```python
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print(squared)  # [1, 4, 9, 16, 25]
```

### 2. Multiple Iterables

```python
a = [1, 2, 3]
b = [10, 20, 30]
result = list(map(lambda x, y: x + y, a, b))
print(result)  # [11, 22, 33]
```

### 3. Lazy Iterator

`map()` returns an iterator, not a list. Values are computed on demand.

```python
numbers = [1, 2, 3, 4]
squares = map(lambda x: x**2, numbers)
print(squares)        # <map object at 0x...>
print(list(squares))  # [1, 4, 9, 16]
```

## filter()

### 1. Select Elements

```python
numbers = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6]
```

### 2. Lazy Iterator

`filter()` also returns an iterator.

```python
numbers = [1, 2, 3, 4, 5, 6]
evens = filter(lambda x: x % 2 == 0, numbers)
print(evens)        # <filter object at 0x...>
print(list(evens))  # [2, 4, 6]
```

## reduce()

### 1. Accumulate

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]
total = reduce(lambda x, y: x + y, numbers)
print(total)  # 15
```

### 2. With Initial

```python
product = reduce(lambda x, y: x * y, numbers, 1)
print(product)  # 120
```

## Comprehensions Alternative

### 1. More Pythonic

```python
# map equivalent
squared = [x**2 for x in numbers]

# filter equivalent
evens = [x for x in numbers if x % 2 == 0]
```

## Functional Composition

Chain filter, map, and reduce for data pipelines.

### 1. Pipeline Example

```python
from functools import reduce

names = ["Alice", "Bob", "Charlie", "David"]

# filter → map → reduce
result = reduce(
    lambda a, b: a + " & " + b,
    map(str.upper, filter(lambda name: len(name) > 4, names))
)

print(result)  # ALICE & CHARLIE & DAVID
```

### 2. Step by Step

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

# Step 1: filter evens
evens = filter(lambda x: x % 2 == 0, numbers)

# Step 2: map to squares
squares = map(lambda x: x ** 2, evens)

# Step 3: reduce to sum
total = reduce(lambda x, y: x + y, squares)

print(total)  # 56 (4 + 16 + 36)
```

## Summary

- map: transform
- filter: select
- reduce: accumulate
- Comprehensions often better

---

## Exercises

**Exercise 1.**
Given a list of dictionaries `[{"name": "Alice", "score": 85}, {"name": "Bob", "score": 42}, {"name": "Charlie", "score": 91}]`, use `filter()` to keep only entries with `score >= 60`, then use `map()` to extract just the names. Print the resulting list.

??? success "Solution to Exercise 1"

        students = [
            {"name": "Alice", "score": 85},
            {"name": "Bob", "score": 42},
            {"name": "Charlie", "score": 91},
        ]

        passing = filter(lambda s: s["score"] >= 60, students)
        names = list(map(lambda s: s["name"], passing))
        print(names)  # ['Alice', 'Charlie']

---

**Exercise 2.**
Use `functools.reduce` to implement a function `my_max(numbers)` that finds the maximum value in a list without using the built-in `max()`. Handle the empty-list case by raising `ValueError`.

??? success "Solution to Exercise 2"

        from functools import reduce

        def my_max(numbers):
            if not numbers:
                raise ValueError("my_max() arg is an empty sequence")
            return reduce(lambda a, b: a if a > b else b, numbers)

        print(my_max([3, 1, 4, 1, 5, 9, 2, 6]))  # 9
        print(my_max([-5, -2, -8]))                 # -2
        try:
            my_max([])
        except ValueError as e:
            print(e)

---

**Exercise 3.**
Rewrite the following pipeline using list comprehensions instead of `map` and `filter`:
```python
result = list(map(str, filter(lambda x: x % 2 == 0, map(lambda x: x ** 2, range(10)))))
```
Verify both versions produce the same output.

??? success "Solution to Exercise 3"

        # Original with map/filter
        result1 = list(
            map(str, filter(lambda x: x % 2 == 0, map(lambda x: x ** 2, range(10))))
        )

        # Comprehension version
        result2 = [str(x ** 2) for x in range(10) if (x ** 2) % 2 == 0]

        print(result1)
        print(result2)
        print(result1 == result2)  # True
