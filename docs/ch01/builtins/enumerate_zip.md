# enumerate() and zip()

These functions are **iteration transformers**---they restructure how you loop over data. `enumerate()` adds indices to an iterable; `zip()` combines multiple iterables element-by-element. Both yield tuples.

!!! tip "Mental Model"
    `enumerate()` answers "which position am I at?" while iterating; `zip()` answers "what goes together?" across parallel sequences. Both wrap an existing iteration with extra structure, so you never need to manually track indices or align multiple lists by position.

## enumerate()

`enumerate()` adds an index counter to any iterable. It is the idiomatic replacement for `range(len(sequence))`:

```python
fruits = ["apple", "banana", "cherry"]

# Avoid this
for i in range(len(fruits)):
    print(i, fruits[i])

# Prefer this
for i, fruit in enumerate(fruits):
    print(i, fruit)
```

Output:

```text
0 apple
1 banana
2 cherry
```

The default counter starts at 0. Use `start=` to begin at a different value:

```python
tasks = ["Buy groceries", "Call mom", "Finish homework"]
for i, task in enumerate(tasks, start=1):
    print(f"{i}. {task}")
```

Output:

```text
1. Buy groceries
2. Call mom
3. Finish homework
```

## zip()

`zip()` combines elements from multiple iterables into tuples, stopping at the shortest:

```python
names = ["Alice", "Bob", "Charlie"]
ages  = [25, 30, 35]

for name, age in zip(names, ages):
    print(name, age)
```

Output:

```text
Alice 25
Bob 30
Charlie 35
```

Three iterables at once:

```python
names  = ["Alice", "Bob", "Charlie"]
ages   = [25, 30, 35]
cities = ["NYC", "LA", "Chicago"]

for name, age, city in zip(names, ages, cities):
    print(f"{name} is {age} and lives in {city}")
```

Output:

```text
Alice is 25 and lives in NYC
Bob is 30 and lives in LA
Charlie is 35 and lives in Chicago
```

### Converting zip output

`zip()` is lazy — wrap it in `list()` to materialise the pairs:

```python
pairs = list(zip(names, ages))
print(pairs)   # [('Alice', 25), ('Bob', 30), ('Charlie', 35)]
```

### Building a dictionary from two lists

```python
keys   = ["name", "age", "city"]
values = ["Alice", 25, "NYC"]
person = dict(zip(keys, values))
print(person)   # {'name': 'Alice', 'age': 25, 'city': 'NYC'}
```

### Unzipping

The `*` operator unpacks a list of pairs back into separate sequences:

```python
pairs = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
names, ages = zip(*pairs)
print(names)   # ('Alice', 'Bob', 'Charlie')
print(ages)    # (25, 30, 35)
```

## Key Ideas

`enumerate()` is the idiomatic way to iterate with an index — prefer it over `range(len(seq))`.
`zip()` is the idiomatic way to iterate over two or more sequences in parallel — prefer it over indexing both manually.
Both functions are lazy: they produce one tuple at a time without building the full result in memory.

---

## Practical Example

```python
# Combine related data with numbered output
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

for i, (name, score) in enumerate(zip(names, scores), start=1):
    print(f"{i}. {name}: {score}")
```

## Exercises

**Exercise 1.**
`zip()` stops at the shortest iterable. Predict the output:

```python
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30]

for name, age in zip(names, ages):
    print(name, age)
```

Why does Python silently drop `"Charlie"` instead of raising an error? How would you use `itertools.zip_longest` to include all elements? In Python 3.10+, how does `zip(strict=True)` change this behavior?

??? success "Solution to Exercise 1"
    Output:

    ```text
    Alice 25
    Bob 30
    ```

    `"Charlie"` is silently dropped because `zip()` stops at the shortest iterable. This is by design: `zip()` was created for the common case where iterables are expected to have equal length, and stopping early is a safe default.

    To include all elements with a fill value:

    ```python
    from itertools import zip_longest
    for name, age in zip_longest(names, ages, fillvalue="N/A"):
        print(name, age)
    # Output: Alice 25, Bob 30, Charlie N/A
    ```

    In Python 3.10+, `zip(names, ages, strict=True)` raises `ValueError` if the iterables have different lengths. This is useful when unequal lengths indicate a bug in the data.

---

**Exercise 2.**
`enumerate()` produces tuples. Predict the output and explain the unpacking:

```python
words = ["hello", "world"]
result = list(enumerate(words, start=10))
print(result)

for i, word in enumerate(words):
    print(f"{i}: {word}")
```

What is the type of each element in the `enumerate` output? Why does `enumerate(words, start=10)` not change the actual indices of the list?

??? success "Solution to Exercise 2"
    Output:

    ```text
    [(10, 'hello'), (11, 'world')]
    0: hello
    1: world
    ```

    Each element from `enumerate()` is a tuple of `(index, value)`. The `start=10` parameter changes the counter starting point but does NOT change the list's actual indices. `words[0]` is still `"hello"` -- `enumerate` just provides a counter alongside iteration.

    The tuple unpacking `for i, word in enumerate(words)` works because each tuple `(0, "hello")` is unpacked into `i = 0` and `word = "hello"`. This is the same unpacking mechanism as `a, b = (1, 2)`.

---

**Exercise 3.**
The "unzip" pattern uses `zip(*pairs)`. Predict the output and explain the mechanism:

```python
pairs = [(1, "a"), (2, "b"), (3, "c")]
numbers, letters = zip(*pairs)
print(numbers)
print(letters)
print(type(numbers))
```

What does the `*` operator do to `pairs` before passing to `zip()`? Why does the result contain tuples, not lists? What happens if `pairs` is empty?

??? success "Solution to Exercise 3"
    Output:

    ```text
    (1, 2, 3)
    ('a', 'b', 'c')
    <class 'tuple'>
    ```

    The `*` operator **unpacks** the list `pairs` into separate arguments: `zip(*pairs)` becomes `zip((1, "a"), (2, "b"), (3, "c"))`. This is equivalent to calling `zip` with three separate tuples.

    `zip` then pairs the first elements `(1, 2, 3)`, the second elements `("a", "b", "c")`, etc. The result contains tuples (not lists) because `zip` always produces tuples.

    If `pairs` is empty (`pairs = []`), then `zip(*pairs)` is `zip()` with no arguments. `numbers, letters = zip()` raises `ValueError: not enough values to unpack` because `zip()` produces nothing. To handle empty input, you would need a guard: `if pairs: numbers, letters = zip(*pairs)`.
