# len() and range()

`range()` defines an iteration space; `len()` measures the size of a collection. Together they are among the most frequently used built-ins in Python.

!!! tip "Mental Model"
    `len()` asks "how big is this?" and `range()` asks "give me numbers from here to there." `range()` is lazy---it describes a sequence of integers without storing them all in memory. Together they let you measure collections and generate index sequences for iteration.

## len()

`len()` returns the number of elements in a container.

```python
numbers = [1, 2, 3, 4]
print(len(numbers))   # 4

text = "Python"
print(len(text))      # 6
```

Works with any sized container: lists, tuples, strings, dictionaries, and sets.

## range()

`range()` generates a sequence of integers. It is lazy — the numbers are produced on demand rather than stored all at once.

Three forms:

```python
range(stop)             # 0 up to (not including) stop
range(start, stop)      # start up to (not including) stop
range(start, stop, step)# start up to stop, stepping by step
```

```python
for i in range(5):
    print(i)   # 0 1 2 3 4
```

```python
for i in range(2, 10, 2):
    print(i)   # 2 4 6 8
```

`range()` produces integers only. To iterate over a list by index, combine it with `len()`:

```python
fruits = ["apple", "banana", "cherry"]
for i in range(len(fruits)):
    print(i, fruits[i])
```

Output:

```text
0 apple
1 banana
2 cherry
```

In practice this pattern is rare — `enumerate()` is almost always clearer. See [enumerate() and zip()](enumerate_zip.md).

## Key Ideas

`len()` measures a container; `range()` generates integers for iteration.
`range()` is lazy and memory-efficient — `range(1_000_000)` uses no more memory than `range(5)`.
Avoid `range(len(seq))` when you need both index and value — use `enumerate()` instead.

---

## Practical Example

```python
# Pagination: split items into pages of size 3
items = ["a", "b", "c", "d", "e", "f", "g"]
page_size = 3

for i in range(0, len(items), page_size):
    page = items[i:i+page_size]
    print(page)
```



---

## Notebook Examples

```python
for i in range(10):
    print(i, end=" ")

print()
print(i) # 9
```

---

## Exercises

**Exercise 1.**
`range()` is lazy -- it does not store all values in memory. Predict the output:

```python
r = range(1_000_000)
print(type(r))
print(len(r))
print(r[999_999])
print(500_000 in r)
```

Why can `range` support `len()`, indexing, and `in` without storing all million numbers? What data structure does `range` use internally?

??? success "Solution to Exercise 1"
    Output:

    ```text
    <class 'range'>
    1000000
    999999
    True
    ```

    `range` stores only three values internally: `start`, `stop`, and `step`. It computes any requested value on the fly using arithmetic: `r[i]` = `start + i * step`. `len(r)` = `(stop - start + step - 1) // step`. `x in r` checks if `x` is within bounds and lands on a step.

    This is why `range(1_000_000)` uses the same amount of memory as `range(5)` -- it never materializes the sequence. This is an example of a **lazy object** (as introduced in the [overview](builtins_overview.md)) that supports random access through computation rather than storage.

---

**Exercise 2.**
`len()` works by calling the `__len__` method on the object. Predict which calls succeed and which raise errors:

```python
print(len([1, 2, 3]))
print(len("hello"))
print(len({1, 2, 3}))
print(len(42))
print(len(range(10)))
```

Why does `len(42)` fail? What does an object need to support `len()`?

??? success "Solution to Exercise 2"
    ```text
    3
    5
    3
    TypeError: object of type 'int' has no len()
    10
    ```

    `len(42)` raises `TypeError` because integers do not have a `__len__` method. `len()` works by calling `obj.__len__()`, so an object supports `len()` if and only if its class defines `__len__`.

    Lists, strings, sets, dicts, tuples, and ranges all define `__len__`. Integers, floats, booleans, and `None` do not, because they are not containers.

---

**Exercise 3.**
`range()` supports negative steps. Predict the output:

```python
print(list(range(10, 0, -1)))
print(list(range(10, 0, -3)))
print(list(range(0, 10, -1)))
print(list(range(5, 5)))
```

Why does `range(0, 10, -1)` produce an empty list? What is the general rule for when a `range` is empty?

??? success "Solution to Exercise 3"
    Output:

    ```text
    [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    [10, 7, 4, 1]
    []
    []
    ```

    `range(0, 10, -1)` is empty because with a negative step, `range` counts downward, but `start` (0) is already less than `stop` (10). There is no way to count down from 0 to 10.

    The general rule: a `range` is empty when:
    - `step > 0` and `start >= stop` (counting up but already past the target)
    - `step < 0` and `start <= stop` (counting down but already past the target)

    `range(5, 5)` is empty because `start == stop` -- there are no integers in the half-open interval `[5, 5)`.
