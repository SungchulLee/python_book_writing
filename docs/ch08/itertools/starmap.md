# starmap

`starmap()` applies a function to unpacked tuples from an iterable, similar to `map()` but with automatic argument unpacking. This is useful when your data arrives as pre-packed argument tuples — for example, from `zip()`, a database query, or a CSV reader — and you want to apply a multi-argument function to each without writing an explicit loop or lambda wrapper.

!!! tip "Mental Model"
    `starmap` is `map` with a star — literally. Where `map(f, items)` calls `f(item)` for each item, `starmap(f, items)` calls `f(*item)`, unpacking each tuple into separate arguments. Whenever your data is already packed as argument tuples (e.g., pairs of coordinates), `starmap` eliminates the lambda that `map` would require.

## Using starmap

Each element in the input iterable is unpacked as positional arguments to the function. This is equivalent to calling `func(*args)` for each `args` tuple in the iterable.

```python
from itertools import starmap
import operator

tuples = [(2, 3), (4, 5), (6, 7)]
results = list(starmap(operator.add, tuples))
print(results)
```

```
[5, 9, 13]
```

## starmap vs map

The key difference from the built-in `map()` is that `map()` passes each element as a single argument, while `starmap()` unpacks each element into separate positional arguments.

```python
from itertools import starmap

def power(base, exp):
    return base ** exp

data = [(2, 3), (3, 2), (5, 2)]

# starmap unpacks tuples
result1 = list(starmap(power, data))
print("starmap:", result1)

# map passes tuples as single arguments
try:
    result2 = list(map(power, data))
except TypeError as e:
    print(f"map error: {e}")
```

```
starmap: [8, 9, 25]
map error: power() missing 1 required positional argument: 'exp'
```

---

## Exercises

**Exercise 1.**
Use `starmap` with `operator.mul` to compute the element-wise product of two lists. For example, given `[(2, 3), (4, 5), (6, 7)]`, return `[6, 20, 42]`.

??? success "Solution to Exercise 1"

    ```python
    from itertools import starmap
    import operator

    pairs = [(2, 3), (4, 5), (6, 7)]
    result = list(starmap(operator.mul, pairs))
    print(result)  # [6, 20, 42]
    ```

---

**Exercise 2.**
Use `starmap` to call `str.format` on a list of `(template, value)` pairs. For example, given `[("Hello, {}!", "Alice"), ("Score: {}", 95), ("{} items", 3)]`, return `["Hello, Alice!", "Score: 95", "3 items"]`.

??? success "Solution to Exercise 2"

    ```python
    from itertools import starmap

    data = [
        ("Hello, {}!", "Alice"),
        ("Score: {}", 95),
        ("{} items", 3),
    ]
    result = list(starmap(str.format, data))
    print(result)
    # ['Hello, Alice!', 'Score: 95', '3 items']
    ```

---

**Exercise 3.**
Write a function `apply_functions` that takes a list of `(function, argument)` pairs and uses `starmap` to apply each function to its argument. For example, given `[(abs, -5), (str.upper, "hello"), (len, [1, 2, 3])]`, return `[5, "HELLO", 3]`.

??? success "Solution to Exercise 3"

    ```python
    from itertools import starmap

    def apply_functions(pairs):
        return list(starmap(lambda f, x: f(x), pairs))

    # Test
    result = apply_functions([
        (abs, -5),
        (str.upper, "hello"),
        (len, [1, 2, 3]),
    ])
    print(result)  # [5, 'HELLO', 3]
    ```
