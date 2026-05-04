
# min(), max(), sum()

These built-ins are **reductions**---they collapse a collection down to a single value.

```mermaid
flowchart LR
    A[Numbers]
    A --> B[min()]
    A --> C[max()]
    A --> D[sum()]
````

!!! tip "Mental Model"
    These three functions reduce a collection to a single answer: the smallest, the largest, or the total. They scan through an iterable once, so you never need to write a loop just to find a minimum, maximum, or sum. Think of them as questions you ask a collection: "what is the least?", "the most?", "the total?"

---

## min()

Returns smallest value.

```python
numbers = [5,2,9,1]

print(min(numbers))
```

Output

```
1
```

---

## max()

Returns largest value.

```python
print(max(numbers))
```

Output

```
9
```

---

## sum()

Computes total.

```python
print(sum(numbers))
```

Output

```
17
```

---

## Practical Example

```python
# Sales analysis
sales = [1200, 800, 1500, 950]

print("Highest:", max(sales))
print("Lowest:", min(sales))
print("Total:", sum(sales))
```



---

## Notebook Examples

```python
print( sum([1,2,3]) )
```

```python
sum = 10
print( sum )
print( sum([1,2,3]) )
```

---

## Exercises

**Exercise 1.**
`min()` and `max()` can accept a `key` argument. Predict the output:

```python
words = ["banana", "apple", "cherry", "date"]
print(min(words))
print(min(words, key=len))
print(max(words, key=len))
```

Why does `min(words)` return `"apple"` while `min(words, key=len)` returns `"date"`? What does `key` do -- does it change the returned value or just affect the comparison?

??? success "Solution to Exercise 1"
    Output:

    ```text
    apple
    date
    cherry
    ```

    `min(words)` compares strings lexicographically: `"apple"` < `"banana"` < `"cherry"` < `"date"`.

    `min(words, key=len)` compares by string length: `len("date")=4` < `len("apple")=5` < `len("banana")=6` < `len("cherry")=6`. So `"date"` has the minimum length.

    The `key` function only affects the comparison -- the **original value** is returned, not the key. `min(words, key=len)` returns `"date"` (the original string), not `4` (its length).

---

**Exercise 2.**
`sum()` has a `start` parameter. Predict the output:

```python
print(sum([1, 2, 3]))
print(sum([1, 2, 3], 10))
print(sum([[1, 2], [3, 4]], []))
```

Why does `sum([[1, 2], [3, 4]], [])` produce `[1, 2, 3, 4]`? Why does `sum()` not work with strings (e.g., `sum(["a", "b"], "")` raises `TypeError`)?

??? success "Solution to Exercise 2"
    Output:

    ```text
    6
    16
    [1, 2, 3, 4]
    ```

    `sum([1, 2, 3], 10)` starts from `10` and adds each element: `10 + 1 + 2 + 3 = 16`.

    `sum([[1, 2], [3, 4]], [])` starts from `[]` and concatenates: `[] + [1, 2] + [3, 4] = [1, 2, 3, 4]`. This works because `+` is defined for lists (concatenation). However, this pattern is **not recommended** for flattening lists---it is O(n^2) because each `+` creates a new list. Use a comprehension (`[x for sub in lists for x in sub]`) or `itertools.chain.from_iterable()` instead.

    `sum(["a", "b"], "")` raises `TypeError: sum() can't sum strings [use ''.join(seq) instead]`. Python explicitly forbids string summation because it is O(n^2) -- each `+` creates a new string. `"".join(seq)` is the correct O(n) approach. Python blocks the inefficient path and suggests the efficient one.

---

**Exercise 3.**
What happens when these functions receive an empty iterable?

```python
print(sum([]))
print(min([]))
print(max([]))
```

Why does `sum([])` return `0` while `min([])` raises `ValueError`? What design decision explains this difference?

??? success "Solution to Exercise 3"
    `sum([])` returns `0`. `min([])` and `max([])` both raise `ValueError: min() arg is an empty sequence`.

    The difference: `sum` has a well-defined identity element -- `0`. The sum of nothing is `0` (the additive identity). But `min` and `max` have no meaningful answer for an empty sequence -- what is the minimum of nothing? There is no sensible default.

    You can provide a default for `min`/`max` in Python 3.4+: `min([], default=0)` returns `0` instead of raising an error.
