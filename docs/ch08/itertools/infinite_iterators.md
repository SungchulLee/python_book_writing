# Infinite Iterators (count, cycle, repeat)

Infinite iterators generate an endless sequence of values. These are useful for creating infinite streams or repeating patterns that can be sliced or combined with other tools.

!!! tip "Mental Model"
    Infinite iterators are faucets that never run dry — `count` produces an endless number line, `cycle` loops a sequence forever, and `repeat` echoes a single value indefinitely. They are safe because they are lazy: no memory is consumed until you pull the next value. Pair them with `islice`, `zip`, or `takewhile` to draw exactly as many items as you need.

## count() - Infinite Counter

The `count()` function returns an iterator that generates numbers indefinitely starting from a given value and incrementing by a step.

```python
from itertools import count

# Count from 0 by default
counter = count()
print(next(counter))  # 0
print(next(counter))  # 1
print(next(counter))  # 2

# Count from 10 with step 5
counter2 = count(10, 5)
print(list(next(counter2) for _ in range(4)))  # [10, 15, 20, 25]
```

```
0
1
2
[10, 15, 20, 25]
```

## cycle() - Infinite Cycle

The `cycle()` function repeats an iterable indefinitely, cycling through its elements.

```python
from itertools import cycle, islice

colors = ['red', 'green', 'blue']
color_cycle = cycle(colors)

# Take first 8 elements
result = list(islice(color_cycle, 8))
print(result)
```

```
['red', 'green', 'blue', 'red', 'green', 'blue', 'red', 'green']
```

## repeat() - Infinite Repetition

The `repeat()` function repeats an element indefinitely or a specified number of times.

```python
from itertools import repeat

# Repeat indefinitely (limited by islice)
from itertools import islice
limited = list(islice(repeat('x'), 5))
print(limited)

# Repeat specific number of times
limited2 = list(repeat('hello', 3))
print(limited2)
```

```
['x', 'x', 'x', 'x', 'x']
['hello', 'hello', 'hello']
```

---

## Exercises

**Exercise 1.**
Use `count` and `islice` to generate the first 10 even numbers starting from 0 (i.e., 0, 2, 4, ..., 18). Do not use a list comprehension; use only itertools functions.

??? success "Solution to Exercise 1"

    ```python
    from itertools import count, islice

    evens = list(islice(count(0, 2), 10))
    print(evens)  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
    ```

---

**Exercise 2.**
Use `cycle` to assign colors from `["red", "green", "blue"]` to a list of 7 items. Return a list of `(item, color)` tuples. For example, given items `["a", "b", "c", "d", "e", "f", "g"]`, the result should pair each item with the cycling colors.

??? success "Solution to Exercise 2"

    ```python
    from itertools import cycle

    items = ["a", "b", "c", "d", "e", "f", "g"]
    colors = cycle(["red", "green", "blue"])
    result = [(item, next(colors)) for item in items]
    print(result)
    # [('a', 'red'), ('b', 'green'), ('c', 'blue'),
    #  ('d', 'red'), ('e', 'green'), ('f', 'blue'), ('g', 'red')]
    ```

---

**Exercise 3.**
Use `repeat` and `map` to create a list of 5 dictionaries, each initialized as `{"count": 0, "active": True}`. Ensure each dictionary is a separate object (not the same reference). Hint: use `repeat` with a lambda or function.

??? success "Solution to Exercise 3"

    ```python
    from itertools import repeat

    dicts = list(map(
        lambda _: {"count": 0, "active": True},
        repeat(None, 5)
    ))
    print(dicts)
    # Each dict is independent
    dicts[0]["count"] = 10
    print(dicts[0])  # {'count': 10, 'active': True}
    print(dicts[1])  # {'count': 0, 'active': True}
    ```
