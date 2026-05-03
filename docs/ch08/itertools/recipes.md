# itertools Recipes

Common utility functions built from itertools primitives, providing elegant solutions to frequent programming tasks.

!!! tip "Mental Model"
    itertools recipes are pre-assembled pipelines built from the module's primitives — the same way you combine basic LEGO bricks into recognizable structures. Functions like `flatten`, `pairwise`, and `batched` appear so often that they have become community standards. Knowing these recipes saves you from reinventing common patterns and signals clear intent to other developers.

## flatten() - Flatten Nested Iterables

Flatten a list of lists into a single sequence.

```python
from itertools import chain

def flatten(list_of_lists):
    return chain.from_iterable(list_of_lists)

data = [[1, 2], [3, 4], [5, 6]]
result = list(flatten(data))
print(result)
```

```
[1, 2, 3, 4, 5, 6]
```

## roundrobin() - Interleave Iterables

Take elements from each iterable in turn.

```python
from itertools import cycle, chain

def roundrobin(*iterables):
    pending = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(iter(it).__next__ for it in iterables)

result = list(roundrobin('ABC', 'D', 'EF'))
print(result)
```

```
['A', 'D', 'E', 'B', 'F', 'C']
```

## partition() - Separate Elements by Predicate

Partition an iterable into two based on a condition.

```python
from itertools import tee

def partition(pred, iterable):
    t1, t2 = tee(iterable)
    return (filter(pred, t1), filterfalse(pred, t2))

from itertools import filterfalse
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
evens, odds = partition(lambda x: x % 2 == 0, numbers)
print("Evens:", list(evens))
print("Odds:", list(odds))
```

```
Evens: [2, 4, 6, 8]
Odds: [1, 3, 5, 7]
```

---

## Exercises

**Exercise 1.**
Implement a `roundrobin` function that takes multiple iterables and yields items from each in turn, cycling through them until all are exhausted. For example, `list(roundrobin("ABC", "D", "EF"))` should return `['A', 'D', 'E', 'B', 'F', 'C']`.

??? success "Solution to Exercise 1"

    ```python
    from itertools import cycle, islice

    def roundrobin(*iterables):
        pending = len(iterables)
        nexts = cycle(iter(it).__next__ for it in iterables)
        while pending:
            try:
                for next_fn in nexts:
                    yield next_fn()
            except StopIteration:
                pending -= 1
                nexts = cycle(islice(nexts, pending))

    # Test
    print(list(roundrobin("ABC", "D", "EF")))
    # ['A', 'D', 'E', 'B', 'F', 'C']
    ```

---

**Exercise 2.**
Implement a `flatten` function that recursively flattens nested lists of arbitrary depth using itertools. For example, `flatten([1, [2, [3, 4], 5], [6]])` should return `[1, 2, 3, 4, 5, 6]`.

??? success "Solution to Exercise 2"

    ```python
    from itertools import chain

    def flatten(nested):
        result = []
        for item in nested:
            if isinstance(item, list):
                result.extend(flatten(item))
            else:
                result.append(item)
        return result

    # Test
    print(flatten([1, [2, [3, 4], 5], [6]]))
    # [1, 2, 3, 4, 5, 6]
    ```

---

**Exercise 3.**
Implement a `unique_everseen` function that yields unique elements from an iterable, preserving order and remembering all previously seen elements. For example, `list(unique_everseen("AABBCCDDA"))` should return `['A', 'B', 'C', 'D']`.

??? success "Solution to Exercise 3"

    ```python
    def unique_everseen(iterable):
        seen = set()
        for item in iterable:
            if item not in seen:
                seen.add(item)
                yield item

    # Test
    print(list(unique_everseen("AABBCCDDA")))
    # ['A', 'B', 'C', 'D']
    print(list(unique_everseen([3, 1, 4, 1, 5, 9, 2, 6, 5])))
    # [3, 1, 4, 5, 9, 2, 6]
    ```
