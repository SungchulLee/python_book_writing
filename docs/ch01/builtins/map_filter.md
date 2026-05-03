# map() and filter()

These are **functional-style transformations**: `map()` applies a function to every element; `filter()` selects elements matching a predicate. Both return lazy iterators---use `list()` if you need all results at once. In modern Python, list comprehensions are often preferred for readability, but `map()` and `filter()` remain useful when passing an existing named function directly.

!!! tip "Mental Model"
    `map()` transforms every item through a function; `filter()` keeps only the items that pass a test. Both produce lazy iterators, meaning they process elements on demand rather than building a full list upfront. They are the functional equivalents of a for-loop with an append and a for-loop with an if-check.

## map()

```python
def square(x: int) -> int:
    return x ** 2

numbers = [1, 2, 3, 4, 5]
squared = list(map(square, numbers))
print(squared)   # [1, 4, 9, 16, 25]
```

With a lambda instead of a named function:

```python
squared = list(map(lambda x: x ** 2, numbers))
print(squared)   # [1, 4, 9, 16, 25]
```

`map()` can take multiple iterables — the function receives one element from each:

```python
a = [1, 2, 3]
b = [10, 20, 30]
sums = list(map(lambda x, y: x + y, a, b))
print(sums)   # [11, 22, 33]
```

Passing a named method works too:

```python
words = ["hello", "world", "python"]
upper = list(map(str.upper, words))
print(upper)   # ['HELLO', 'WORLD', 'PYTHON']
```

## filter()

```python
def is_even(x: int) -> bool:
    return x % 2 == 0

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(is_even, numbers))
print(evens)   # [2, 4, 6, 8, 10]
```

With a lambda:

```python
evens = list(filter(lambda x: x % 2 == 0, numbers))
```

Filtering strings:

```python
words = ["apple", "banana", "apricot", "cherry", "avocado"]
a_words = list(filter(lambda w: w.startswith("a"), words))
print(a_words)   # ['apple', 'apricot', 'avocado']
```

Passing `None` as the function keeps all truthy values:

```python
values = [0, 1, False, True, "", "hello", None, [], [1, 2]]
truthy = list(filter(None, values))
print(truthy)   # [1, True, 'hello', [1, 2]]
```

## Combining map() and filter()

Chain them by passing one as the input to the other:

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Squares of even numbers only
result = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, numbers)))
print(result)   # [4, 16, 36, 64, 100]
```

## map() and filter() vs List Comprehensions

Both approaches produce identical results. Choose based on readability:

```python
numbers = [1, 2, 3, 4, 5]

# Transform
list(map(lambda x: x ** 2, numbers))   # map
[x ** 2 for x in numbers]              # comprehension

# Filter
list(filter(lambda x: x % 2 == 0, numbers))   # filter
[x for x in numbers if x % 2 == 0]            # comprehension

# Combined
list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers)))  # map + filter
[x**2 for x in numbers if x % 2 == 0]                              # comprehension
```

List comprehensions are generally preferred in modern Python — they read left to right and require no lambda. Reach for `map()` or `filter()` when you already have a named function to pass:

```python
words = ["  alice  ", "BOB", "  Charlie"]
cleaned = list(map(str.strip, words))   # cleaner than a lambda here
```

## Practical Examples

**Clean and format names:**

```python
names = ["  alice  ", "BOB", "  Charlie"]
cleaned = list(map(lambda s: s.strip().title(), names))
print(cleaned)   # ['Alice', 'Bob', 'Charlie']
```

**Temperature conversion:**

```python
celsius = [0, 10, 20, 30, 100]
fahrenheit = list(map(lambda c: c * 9 / 5 + 32, celsius))
print(fahrenheit)   # [32.0, 50.0, 68.0, 86.0, 212.0]
```

**Filter passing grades:**

```python
grades = [45, 78, 92, 55, 67, 88, 34, 91]
passing = list(filter(lambda g: g >= 60, grades))
print(passing)                                      # [78, 92, 67, 88, 91]
print(f"Pass rate: {len(passing)/len(grades)*100:.1f}%")   # 62.5%
```

**Validate email addresses:**

```python
emails = ["user@example.com", "invalid", "test@test.org", "no-at-sign"]
valid = list(filter(lambda e: "@" in e and "." in e, emails))
print(valid)   # ['user@example.com', 'test@test.org']
```

## Key Ideas

`map()` transforms every element; `filter()` selects elements. Both are lazy — they produce one result at a time without building the full list in memory. List comprehensions are usually clearer for simple cases; `map()` and `filter()` shine when a named function is already available to pass directly.

We return to `map()` and `filter()` as functional programming tools --- alongside `reduce()` and function composition --- in a later chapter on functional programming.

---

## Practical Example

```python
# Cleaning user input
raw_names = ["  alice  ", "BOB", "  Charlie"]
cleaned = list(map(lambda s: s.strip().title(), raw_names))
print(cleaned)   # ['Alice', 'Bob', 'Charlie']

# Filter valid emails
emails = ["user@example.com", "invalid", "test@test.org"]
valid = list(filter(lambda e: "@" in e and "." in e, emails))
print(valid)   # ['user@example.com', 'test@test.org']
```

## Exercises

**Exercise 1.**
`map()` and `filter()` return lazy iterators, not lists. Predict the output:

```python
numbers = [1, 2, 3, 4, 5]
result = map(lambda x: x**2, numbers)
print(result)
print(list(result))
print(list(result))
```

Why does the second `list(result)` return an empty list? How does this laziness behavior compare to list comprehensions?

??? success "Solution to Exercise 1"
    Output:

    ```text
    <map object at 0x...>
    [1, 4, 9, 16, 25]
    []
    ```

    `map()` returns a **lazy iterator**, not a list. Printing it shows the object representation. The first `list(result)` consumes the iterator, producing all values. The second `list(result)` returns `[]` because the iterator is **exhausted** -- it has already produced all its values and cannot restart.

    List comprehensions `[x**2 for x in numbers]` return a list that can be iterated multiple times. The trade-off: comprehensions use memory (all values stored at once), while `map()` uses constant memory (values produced one at a time).

---

**Exercise 2.**
`filter(None, iterable)` removes falsy values. Predict the output:

```python
values = [0, 1, "", "hello", None, [], [0], False, True, {}, {"a": 1}]
print(list(filter(None, values)))
```

Why does `filter(None, ...)` use `None` as a function? What does Python do internally when the function argument is `None`? Is `[0]` truthy even though it contains a falsy element?

??? success "Solution to Exercise 2"
    Output:

    ```text
    [1, 'hello', [0], True, {'a': 1}]
    ```

    When `None` is passed as the function argument, `filter()` uses the **truthiness** of each element as the filter criterion. Internally, it is equivalent to `filter(bool, values)` -- it keeps only elements where `bool(element)` is `True`.

    `[0]` is truthy because truthiness for containers depends on **length**, not contents. `bool([0])` is `True` because the list is non-empty (it has one element). The value of that element (`0`) does not matter for the container's truthiness.

    Removed values: `0`, `""`, `None`, `[]`, `False`, `{}` -- all are falsy because they represent "empty" or "zero" values.

---

**Exercise 3.**
A programmer converts `map`/`filter` chains to a list comprehension:

```python
# Original
result = list(map(str.upper, filter(lambda s: len(s) > 3, words)))

# Equivalent comprehension
result = [s.upper() for s in words if len(s) > 3]
```

Are these exactly equivalent? Which is more readable? Give one case where `map()` is genuinely cleaner than a comprehension, and one case where a comprehension is clearly better.

??? success "Solution to Exercise 3"
    Yes, these are exactly equivalent in behavior. Both filter words longer than 3 characters and convert them to uppercase.

    The comprehension is more readable in this case because:
    - It reads left to right: "for each `s` in `words`, if length > 3, give me `s.upper()`."
    - The `map`/`filter` chain reads inside-out: you must parse `filter(...)` first, then `map(...)`.

    Case where `map()` is cleaner:

    ```python
    # map with an existing function -- no lambda needed
    cleaned = list(map(str.strip, raw_lines))
    # vs comprehension
    cleaned = [line.strip() for line in raw_lines]
    ```

    When you already have a named function that matches exactly, `map(func, iterable)` is concise.

    Case where comprehension is clearly better:

    ```python
    # comprehension with complex expression
    result = [x**2 + 1 for x in data if x > 0 and x % 2 == 0]
    # vs map/filter
    result = list(map(lambda x: x**2 + 1, filter(lambda x: x > 0 and x % 2 == 0, data)))
    ```

    When both transform and filter are needed with non-trivial logic, the comprehension is far more readable.
