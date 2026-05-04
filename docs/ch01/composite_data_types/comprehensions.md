
# Comprehensions

A **comprehension** is a compact way to build a new collection from an iterable.

Python supports comprehensions for:

- lists — `[expr for x in iterable]`
- sets — `{expr for x in iterable}`
- dictionaries — `{key: value for x in iterable}`
- generator expressions — `(expr for x in iterable)`
- tuples — no comprehension syntax; use `tuple(expr for x in iterable)` instead

They provide a concise alternative to loops. In each case, the pattern is the same: apply an expression to each element and optionally filter with a condition.

!!! tip "Mental Model"
    A comprehension reads like a sentence: "give me `expr` for each `x` in `iterable` (optionally, only if `condition`)." It replaces the loop-accumulate pattern---create empty collection, loop, append---with a single declarative expression. The bracket style determines the output type: `[]` for list, `{}` for set or dict, `()` for generator.

## 1. List Comprehensions

A list comprehension creates a list.

```python
squares = [x * x for x in range(5)]
print(squares)
```

Output:

```text
[0, 1, 4, 9, 16]
```

The equivalent loop:

```python
squares = []
for x in range(5):
    squares.append(x * x)
```

Throughout this page, the loop equivalent is shown only for list comprehensions. The same expansion applies to set, dict, and generator forms.


## 2. Filtering in Comprehensions

A condition at the end filters which elements are included.

```python
evens = [x for x in range(10) if x % 2 == 0]
print(evens)
```

Output:

```text
[0, 2, 4, 6, 8]
```

### Ternary expression vs filter

The `if` at the end *filters*. An `if`/`else` in the expression *transforms*.

```python
labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
print(labels)
```

Output:

```text
['even', 'odd', 'even', 'odd', 'even']
```

Note the position: `if`/`else` before `for` transforms every element; `if` after `for` selects which elements to include.


## 3. Set Comprehensions

A set comprehension creates a set. Duplicates are removed automatically.

```python
lengths = {len(word) for word in ["cat", "dog", "elephant", "ant"]}
print(lengths)
```

Output:

```text
{3, 8}
```

`"cat"`, `"dog"`, and `"ant"` all have length 3 — the set keeps only one.


## 4. Dictionary Comprehensions

A dictionary comprehension creates a mapping.

```python
squares = {x: x * x for x in range(5)}
print(squares)
```

Output:

```text
{0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```


## 5. Generator Expressions

Generator expressions are the lazy counterpart of comprehensions. See [Generator Expressions](generator_expressions.md) for full coverage.

There is no tuple comprehension syntax. To build a tuple from a comprehension-like expression, wrap a generator explicitly:

```python
squares_tuple = tuple(x * x for x in range(5))
print(squares_tuple)
```


## 6. Nested Comprehensions

Comprehensions can iterate over multiple sequences. The order reads left to right: the outer `for` comes first, then the inner `for`.

Flattening a matrix:

```python
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [x for row in matrix for x in row]
print(flat)
```

Output:

```text
[1, 2, 3, 4, 5, 6]
```

Cartesian product — all pairs from two ranges:

```python
pairs = [(x, y) for x in range(3) for y in range(3)]
print(pairs)
```

Output:

```text
[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
```


## 7. When to Use Comprehensions

A comprehension that fits comfortably on one line is usually appropriate. Once it requires a nested loop with a condition, consider a regular loop instead.

```python
# this comprehension is too complex — use a loop
result = [f(x, y) for x in range(10) for y in range(10) if x != y and g(x, y)]
```

Comprehensions are generally preferred over `map()` and `filter()` in modern Python for readability.


## 8. Worked Examples

### Example 1: uppercase words

```python
words = ["python", "is", "fun"]
upper_words = [w.upper() for w in words]
print(upper_words)
```

Output:

```text
['PYTHON', 'IS', 'FUN']
```

### Example 2: positive numbers only

```python
nums = [-2, -1, 0, 1, 2]
positive = [x for x in nums if x > 0]
print(positive)
```

Output:

```text
[1, 2]
```

### Example 3: word lengths

```python
length_map = {word: len(word) for word in ["cat", "horse"]}
print(length_map)
```

Output:

```text
{'cat': 3, 'horse': 5}
```


## 9. Common Pitfalls

### Making comprehensions too complex

Readability matters more than compactness. If a comprehension is hard to read, use a loop.

### Confusing set and dictionary comprehension syntax

Braces create either a set or a dictionary depending on the presence of `:`.

```python
a = {x for x in range(3)}
b = {x: x for x in range(3)}

print(a)
print(b)
```

Output:

```text
{0, 1, 2}
{0: 0, 1: 1, 2: 2}
```

### Expecting comprehension variables to leak

In Python 3, comprehension variables do not leak into the enclosing scope. This is different from regular `for` loops.

```python
squares = [x for x in range(5)]
# x is not defined here — unlike a regular for loop
```


## 10. Key Ideas

Comprehensions create collections concisely by combining an expression, one or more `for` clauses, and an optional `if` filter. List, set, dictionary, and generator forms all follow the same pattern — the only differences are the enclosing brackets and the presence of `:` for dictionaries. A trailing `if` selects which elements to include; an `if`/`else` before `for` transforms every element. Generator expressions are lazy and memory-efficient — prefer them when the full collection is not needed. Keep comprehensions simple: once they require nested loops with conditions, a regular loop is clearer.

Comprehensions build on [Lists](lists.md), [Sets](sets.md), and [Dictionaries](dictionaries.md) covered earlier in this section. For deeper coverage of how these collections work internally, see the hashing and hash tables topic in a later chapter.




---

## Notebook Examples

```python
squares = [x * x for x in range(5)] # list comprehension

print(squares)
```

```python
squares = []

for x in range(5): # list comprehension
    squares.append(x * x)

print(squares)
```

```python
evens = [x for x in range(10) if x % 2 == 0]

print(evens)
```

```python
evens = []

for x in range(10):
    if x % 2 == 0:
        evens.append(x)

print(evens)
```

```python
evens = []

for x in range(0,10,2):
    evens.append(x)

print(evens)
```

```python
evens = list(range(0,10,2))

print(evens)
```

```python
evens = list(filter(lambda x: x % 2 == 0, range(10))) # iterator

print(evens)
```

```python
# list, tuple, set, dict, (generator) comprehension

squares = [x * x for x in range(5)] # list comprehension
squares = (x * x for x in range(5)) # tuple comprehension (X) generator (==iterator) comprehension

for _ in range(3):
    try:
        print(next(squares))
    except StopIteration as e:
        print(e)
        break
else: # no break
    print("break does not work here")

print("we are out of the for loop")
```

```python
# list, tuple, set, dict, (generator) comprehension

squares = [x * x for x in range(5)] # list comprehension
squares = (x * x for x in range(5)) # tuple comprehension (X) generator (==iterator) comprehension
squares = tuple( x * x for x in range(5) ) # tuple comprehension : gerator ---> tuple
squares = { x * x for x in range(5) } # set
squares = { x : x * x for x in range(5) } # dict

print(squares)
```

---

## Exercises

**Exercise 1.**
In Python 3, comprehension variables do not leak into the enclosing scope, but regular `for` loop variables do. Predict the output:

```python
squares = [x**2 for x in range(5)]
# print(x)  # Would this work?

for y in range(5):
    pass
print(y)  # What about this?
```

Explain *why* Python made comprehension variables private but loop variables visible. What scoping mechanism is at work?

??? success "Solution to Exercise 1"
    `print(x)` after the comprehension would raise `NameError` in Python 3 -- `x` is not defined in the enclosing scope. The comprehension runs in its own implicit scope.

    `print(y)` prints `4` -- the last value from the `for` loop. Regular `for` loops do NOT create a new scope; the loop variable `y` remains in the enclosing scope after the loop ends.

    The reason for the difference: comprehensions were redesigned in Python 3 to run in their own scope (implemented as an implicit function call). This prevents accidental variable name collisions. Regular `for` loops were kept backward-compatible -- changing their scoping would break enormous amounts of existing code. The result is an intentional asymmetry in Python's scoping rules.

---

**Exercise 2.**
Rewrite the following nested loop as a single list comprehension:

```python
result = []
for i in range(3):
    for j in range(3):
        if i != j:
            result.append((i, j))
```

Then explain: at what level of nesting does a comprehension become less readable than an explicit loop? What is the guiding principle?

??? success "Solution to Exercise 2"
    ```python
    result = [(i, j) for i in range(3) for j in range(3) if i != j]
    ```

    The `for` clauses in a comprehension are read left-to-right, matching the nesting order of the explicit loop (outer loop first, inner loop second).

    **Readability guideline:** A comprehension with one `for` and one `if` is almost always clearer than an explicit loop. Two `for` clauses (one level of nesting) are acceptable if the logic is simple. Three or more `for` clauses, or complex conditions, should be written as explicit loops. The guiding principle: if a comprehension takes more than a moment to understand, it should be an explicit loop. Comprehensions optimize for **readability**, not for minimizing line count.

---

**Exercise 3.**
A generator expression `(x**2 for x in range(1_000_000))` and a list comprehension `[x**2 for x in range(1_000_000)]` produce the same values. Explain the key difference in memory usage. When should you prefer a generator expression over a list comprehension?

??? success "Solution to Exercise 3"
    The list comprehension `[x**2 for x in range(1_000_000)]` creates a **list of 1 million integers** in memory all at once. This uses approximately 8 MB of memory (plus Python object overhead).

    The generator expression `(x**2 for x in range(1_000_000))` creates a **generator object** that computes values **lazily** -- one at a time, only when requested. It uses essentially constant memory regardless of the range size, because it only holds the current value and the iteration state.

    Prefer a generator expression when:

    - You only need to iterate through the values once (e.g., `sum(x**2 for x in range(1_000_000))`)
    - The dataset is large and storing all values would waste memory
    - You are passing the result to a function that consumes an iterable (like `sum`, `max`, `min`, `any`, `all`)

    Prefer a list comprehension when you need to access the result multiple times, index into it, or know its length.
