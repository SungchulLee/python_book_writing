# Generator Expressions

A generator expression produces values **lazily**---one at a time, on demand---rather than building an entire collection in memory. This makes generators ideal for processing large datasets or building pipelines where not all values are needed at once.

Generator expressions use the same syntax as list comprehensions, but with parentheses instead of brackets:

```python
# List comprehension — builds entire list in memory
squares_list = [x**2 for x in range(1000)]

# Generator expression — produces values one at a time
squares_gen = (x**2 for x in range(1000))
```

!!! tip "Mental Model"
    A generator expression is a recipe, not a meal. It remembers how to compute each value but does not compute any of them until asked. This means it uses almost no memory regardless of how many values it can produce---ideal for large or infinite sequences where you only need one element at a time.

---

## Lazy Evaluation

A list comprehension evaluates every element immediately and stores them all. A generator expression computes each value only when requested.

```python
# Stores 1,000,000 values in memory
large_list = [x**2 for x in range(1_000_000)]

# Stores only the expression, not the values
large_gen = (x**2 for x in range(1_000_000))
```

This means a generator uses **constant memory** regardless of how many values it can produce.

---

## Single-Use Iteration

A generator can only be iterated **once**. After exhaustion, it produces no more values.

```python
gen = (x for x in range(3))
print(list(gen))
print(list(gen))
```

Output:

```text
[0, 1, 2]
[]
```

The first iteration consumes all values. The second finds nothing. This is fundamentally different from lists, which can be iterated any number of times.

---

## Pipelines

Generators compose naturally into processing pipelines where each stage transforms or filters data lazily:

```python
numbers = range(1000)
squares = (x**2 for x in numbers)
evens = (x for x in squares if x % 2 == 0)
result = sum(evens)
```

No intermediate list is created. Each value flows through the pipeline one at a time.

---

## When to Use Generator Expressions

Use a generator when:

- the dataset is large or unbounded
- you only need to iterate once
- intermediate results do not need to be stored

Use a list comprehension when:

- you need to access elements multiple times
- you need `len()`, indexing, or slicing
- the dataset is small enough to fit in memory

---

## Reimplementing map and filter

Generator expressions can replace `map()` and `filter()`:

| Operation | Built-in | Generator Expression |
|-----------|----------|----------------------|
| map | `map(f, xs)` | `(f(x) for x in xs)` |
| filter | `filter(p, xs)` | `(x for x in xs if p(x))` |

All three approaches are **lazy**---values are computed on demand.

---

## Summary

- Generator expressions produce values lazily, one at a time
- They use constant memory regardless of dataset size
- They can only be iterated once (single-use iterators)
- They compose into pipelines for efficient data processing
- Use generators for large data; use list comprehensions when reuse or random access is needed


## Exercises

**Exercise 1.**
A generator can only be iterated once. Predict the output:

```python
gen = (x**2 for x in range(5))
print(sum(gen))
print(sum(gen))
```

Why does the second `sum()` return `0`? How does this differ from a list comprehension? What is the underlying mechanism (the iterator protocol) that causes this behavior?

??? success "Solution to Exercise 1"
    Output:

    ```text
    30
    0
    ```

    A generator is a **single-use iterator**. The first `sum(gen)` iterates through all values (0, 1, 4, 9, 16), consuming the generator. After exhaustion, the generator is empty -- it has no way to "rewind." The second `sum(gen)` iterates over an already-exhausted generator, finding no values, and returns `0`.

    A list comprehension creates a **reusable list in memory**. You can iterate over it multiple times because all values are stored.

    The underlying mechanism is the **iterator protocol**: a generator object has a `__next__()` method that produces values one at a time and raises `StopIteration` when exhausted. Once `StopIteration` has been raised, subsequent calls to `__next__()` continue to raise `StopIteration` -- the generator cannot restart.

---

**Exercise 2.**
A generator expression uses parentheses `()`, but so does a tuple. Explain how Python distinguishes between these two:

```python
a = (1, 2, 3)
b = (x for x in range(3))
print(type(a))
print(type(b))
```

What syntactic clue tells Python that `b` is a generator, not a tuple? How do you create a tuple from a generator expression?

??? success "Solution to Exercise 2"
    Output:

    ```text
    <class 'tuple'>
    <class 'generator'>
    ```

    Python distinguishes them by the `for` keyword inside the parentheses. `(1, 2, 3)` contains literal expressions separated by commas -- it is a tuple. `(x for x in range(3))` contains a `for` clause -- it is a generator expression.

    To create a tuple from a generator expression:

    ```python
    t = tuple(x for x in range(3))  # (0, 1, 2)
    ```

    Note: `tuple()` accepts any iterable, including generators. The parentheses around the generator expression are optional when it is the sole argument to a function: `tuple(x for x in range(3))` and `tuple((x for x in range(3)))` are equivalent.

---

**Exercise 3.**
A programmer processes a 10 GB log file:

```python
# Approach A: list comprehension
errors = [line for line in open("huge.log") if "ERROR" in line]
count = len(errors)

# Approach B: generator expression
count = sum(1 for line in open("huge.log") if "ERROR" in line)
```

Explain the memory difference between the two approaches. Why does Approach B use constant memory while Approach A uses memory proportional to the number of matching lines? Why can you use `len()` with Approach A but not with Approach B?

??? success "Solution to Exercise 3"
    **Approach A** reads every matching line into a list stored in memory. If there are 1 million error lines averaging 200 bytes each, the list consumes ~200 MB. If the entire file matches, memory usage equals the file size (10 GB).

    **Approach B** processes one line at a time. At any moment, only one line is in memory. Each line is read, checked for "ERROR", and either counted (`+1`) or discarded. Memory usage is constant regardless of file size or number of matches.

    You can use `len()` with Approach A because a list knows its length (it stores all elements). You cannot use `len()` on a generator because a generator does not know how many elements it will produce -- values are computed lazily, one at a time. The only way to count generator elements is to iterate through them (which is what `sum(1 for ...)` does).

    Note: both approaches should use `with open(...)` for proper file handling. The examples omit this for brevity.
