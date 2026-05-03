
# sorted() and reversed()

These built-ins are **ordering transformations**---they change the order in which elements are accessed without modifying the original object. They differ in an important way: `sorted()` creates a **new list** (materialized result), while `reversed()` returns a **lazy iterator**.

```mermaid
flowchart TD
    A[Sequence]
    A --> B[sorted()]
    A --> C[reversed()]
````

!!! tip "Mental Model"
    `sorted()` produces a brand-new list arranged in order; `reversed()` produces a lazy iterator that walks backward through a sequence. Neither modifies the original data. Use `sorted()` when you need a reordered copy, and `reversed()` when you just need to traverse in reverse without building a new list.

---

## sorted()

Returns a **new sorted list**, leaving the original iterable unchanged.

```python
numbers = [3,1,4,2]

print(sorted(numbers))
```

Output

```
[1,2,3,4]
```

Descending order:

```python
print(sorted(numbers, reverse=True))
```

---

## Sorting Strings

```python
names = ["Charlie","Alice","Bob"]

print(sorted(names))
```

Output

```
['Alice','Bob','Charlie']
```

---

## reversed()

Returns an iterator that yields elements in reverse order.

```python
numbers = [1,2,3]

for n in reversed(numbers):
    print(n)
```

Output

```
3
2
1
```

To get a reversed list directly:

```python
print(list(reversed(numbers)))  # [3, 2, 1]
```

---

## Practical Example

```python
# Sort users by score (descending)
users = [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 92},
    {"name": "Charlie", "score": 78},
]

sorted_users = sorted(users, key=lambda u: u["score"], reverse=True)

for user in sorted_users:
    print(user["name"], user["score"])
```

---

## Exercises

**Exercise 1.**
`sorted()` returns a new list, while `list.sort()` sorts in place. Predict the output:

```python
a = [3, 1, 2]
b = sorted(a)
c = a.sort()
print(a)
print(b)
print(c)
```

Why does `c` contain `None`? What is the fundamental design difference between `sorted()` and `.sort()`, and when should you use each?

??? success "Solution to Exercise 1"
    Output:

    ```text
    [1, 2, 3]
    [1, 2, 3]
    None
    ```

    `sorted(a)` creates and returns a **new sorted list**, leaving `a` unchanged -- but then `a.sort()` sorts `a` **in place** and returns `None`.

    `c` is `None` because `.sort()` returns `None` by convention -- it modifies the list in place rather than creating a new one. This is Python's convention for mutating methods: they return `None` to signal that the operation was in-place.

    Use `sorted()` when you need the original order preserved or when working with immutable sequences (tuples, strings). Use `.sort()` when you want to sort a list in place to save memory.

---

**Exercise 2.**
`sorted()` accepts a `key` function. Predict the output:

```python
words = ["banana", "Apple", "cherry"]
print(sorted(words))
print(sorted(words, key=str.lower))
print(sorted(words, key=len))
```

Why do the three sorts produce different orders? What does the `key` function do -- does it modify the elements or just affect comparison?

??? success "Solution to Exercise 2"
    Output:

    ```text
    ['Apple', 'banana', 'cherry']
    ['Apple', 'banana', 'cherry']
    ['Apple', 'banana', 'cherry']
    ```

    `sorted(words)` sorts by default Unicode code point order. Uppercase letters have lower code points than lowercase (`"A"` = 65, `"b"` = 98), so `"Apple"` sorts before `"banana"` and `"cherry"`: `['Apple', 'banana', 'cherry']`.

    `sorted(words, key=str.lower)` compares lowercase versions: `"apple"`, `"banana"`, `"cherry"`. Alphabetically this gives `['Apple', 'banana', 'cherry']`. The result happens to be the same here because `"apple"` sorts first in both orderings.

    `sorted(words, key=len)` compares lengths: `len("Apple")=5`, `len("banana")=6`, `len("cherry")=6`. The shortest word comes first: `['Apple', 'banana', 'cherry']`. Stable sorting preserves original order for equal lengths (`"banana"` before `"cherry"`).

    The `key` function does NOT modify the elements---it only produces comparison keys. The original elements appear in the output.

    Note: these examples happen to produce the same result because of the specific input. With different words, the three sorting criteria would produce different orderings.

---

**Exercise 3.**
`reversed()` returns an iterator, not a list. Predict the output:

```python
r = reversed([1, 2, 3])
print(type(r))
print(list(r))
print(list(r))
```

Why is the second `list(r)` empty? How does `reversed()` differ from slicing with `[::-1]` in terms of memory usage and return type?

??? success "Solution to Exercise 3"
    Output:

    ```text
    <class 'list_reverseiterator'>
    [3, 2, 1]
    []
    ```

    `reversed()` returns a **lazy iterator** that can only be consumed once. The first `list(r)` exhausts the iterator. The second `list(r)` gets an empty iterator.

    `reversed()` vs `[::-1]`:
    - `reversed([1, 2, 3])` creates an iterator that produces elements in reverse order **without copying the list**. Memory usage: O(1).
    - `[1, 2, 3][::-1]` creates a **new list** with all elements in reverse. Memory usage: O(n).

    For simply iterating in reverse, `reversed()` is more memory-efficient. For getting a reversed list to keep around, `[::-1]` is more convenient.
