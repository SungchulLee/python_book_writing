
# any() and all()

These functions **evaluate predicates over collections**---`any()` returns `True` if at least one element is truthy; `all()` returns `True` only if every element is truthy. They are the built-in way to express "does anything match?" and "does everything match?" without writing a loop.

```mermaid
flowchart LR
    A[Iterable]
    A --> B[any()]
    A --> C[all()]
```

!!! tip "Mental Model"
    `any()` is a logical OR across a collection; `all()` is a logical AND. Both short-circuit---`any()` stops at the first truthy value, `all()` stops at the first falsy one. They replace the pattern of looping with a flag variable and are the idiomatic way to ask yes/no questions about entire sequences.

## any()

Returns True if **any element is True**.

```python
values = [False, False, True]

print(any(values))
```

Output:

```
True
```

## all()

Returns True if **all elements are True**.

```python
values = [True, True, True]

print(all(values))
```

Output:

```
True
```

---

## Practical Example

```python
# Check if any system has failed
statuses = ["OK", "OK", "ERROR", "OK"]
has_error = any(s == "ERROR" for s in statuses)
print(has_error)   # True

# Check if all students passed
scores = [75, 82, 91, 68]
all_passed = all(score >= 60 for score in scores)
print(all_passed)  # True
```

## Exercises

**Exercise 1.**
`any()` and `all()` apply truthiness rules, not just boolean values. Predict the output:

```python
print(any([0, "", None, False]))
print(any([0, "", None, False, 1]))
print(all([1, "hello", True, [1]]))
print(all([1, "hello", True, []]))
```

Why does the empty list `[]` inside the collection cause `all()` to return `False`? What truthiness rule is being applied to the *elements*?

??? success "Solution to Exercise 1"
    Output:

    ```text
    False
    True
    True
    False
    ```

    `any()` and `all()` apply Python's standard truthiness rules: `0`, `""`, `None`, `False`, `[]`, `{}`, `set()` are all falsy. Everything else is truthy.

    `all([1, "hello", True, []])` returns `False` because `[]` (empty list) is falsy. `all()` requires **every** element to be truthy. The empty list fails this test because empty containers are falsy in Python.

---

**Exercise 2.**
`any()` and `all()` on empty iterables have specific behaviors. Predict the output:

```python
print(any([]))
print(all([]))
```

Why does `any([])` return `False` while `all([])` returns `True`? What logical principle (vacuous truth) explains the `all([])` result?

??? success "Solution to Exercise 2"
    Output:

    ```text
    False
    True
    ```

    `any([])` returns `False`: "are any elements truthy?" -- with no elements, no element is truthy.

    `all([])` returns `True` by **vacuous truth**: "are all elements truthy?" -- with no elements, there is no element that is falsy, so the statement is vacuously true. This follows mathematical logic: "for all x in S, P(x)" is true when S is empty because there is no counterexample.

    This is consistent with `sum([]) == 0` and `math.prod([]) == 1` -- empty aggregations return the identity element for their operation.

---

**Exercise 3.**
`any()` and `all()` short-circuit. Predict the output:

```python
def check(x):
    print(f"checking {x}")
    return x > 0

print(any(check(x) for x in [-1, -2, 3, 4]))
print("---")
print(all(check(x) for x in [1, 2, -3, 4]))
```

How many times is `check()` called in each case? Why does `any()` stop at the first truthy result and `all()` stop at the first falsy result?

??? success "Solution to Exercise 3"
    Output:

    ```text
    checking -1
    checking -2
    checking 3
    True
    ---
    checking 1
    checking 2
    checking -3
    False
    ```

    `any()` calls `check()` three times: `-1` (False), `-2` (False), `3` (True) -- stops immediately, never checks `4`. `all()` calls `check()` three times: `1` (True), `2` (True), `-3` (False) -- stops immediately, never checks `4`.

    `any()` short-circuits at the first truthy result because one True is sufficient. `all()` short-circuits at the first falsy result because one False is sufficient to fail. This is analogous to how `or` and `and` short-circuit, and it means `any()` and `all()` can efficiently process large or infinite generators.
