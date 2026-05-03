# tee

`tee()` creates multiple independent iterators from a single iterable, useful when you need to iterate over the same data multiple times. Python iterators can only be traversed once — once exhausted, their data is gone. `tee()` solves this by creating independent copies that each maintain their own position, though it buffers consumed elements in memory until all copies have advanced past them.

!!! tip "Mental Model"
    `tee` is a Y-splitter for an iterator stream — one input pipe feeds two (or more) independent output pipes. Each copy advances independently, but any elements that one copy has consumed while another hasn't yet must be buffered in memory. If the copies advance at very different rates, that buffer grows without bound, so `tee` works best when the copies are consumed roughly in lockstep.

## Creating Independent Iterators

After calling `tee()`, the original iterator should no longer be used directly. Each returned iterator independently yields all elements from the original source.

```python
from itertools import tee

data = [1, 2, 3, 4, 5]
it1, it2 = tee(iter(data), 2)

print("Iterator 1:", list(it1))
print("Iterator 2:", list(it2))
```

```
Iterator 1: [1, 2, 3, 4, 5]
Iterator 2: [1, 2, 3, 4, 5]
```

## Multiple Independent Iterations

The second argument to `tee()` specifies the number of independent iterators to create. Each copy can be consumed independently for different computations.

```python
from itertools import tee

source = range(3)
it1, it2, it3 = tee(source, 3)

print("Sum:", sum(it1))
for val in it2:
    print(f"Value: {val}")
print("Doubled:", list(2*x for x in it3))
```

```
Sum: 3
Value: 0
Value: 1
Value: 2
Doubled: [0, 2, 4]
```

---

## Exercises

**Exercise 1.**
Use `tee` to compute both the sum and the product of an iterator in a single pass. Write a function `sum_and_product` that takes an iterable of numbers and returns a tuple `(total_sum, total_product)`. For example, `sum_and_product([1, 2, 3, 4])` should return `(10, 24)`.

??? success "Solution to Exercise 1"

    ```python
    from itertools import tee
    from functools import reduce
    import operator

    def sum_and_product(iterable):
        it1, it2 = tee(iterable)
        total_sum = sum(it1)
        total_product = reduce(operator.mul, it2, 1)
        return (total_sum, total_product)

    # Test
    print(sum_and_product([1, 2, 3, 4]))  # (10, 24)
    ```

---

**Exercise 2.**
Use `tee` to create a function `pairwise_diff` that takes an iterable of numbers and returns a list of the differences between consecutive elements. For example, `pairwise_diff([10, 7, 3, 8])` should return `[-3, -4, 5]`.

??? success "Solution to Exercise 2"

    ```python
    from itertools import tee

    def pairwise_diff(iterable):
        a, b = tee(iterable)
        next(b, None)
        return [y - x for x, y in zip(a, b)]

    # Test
    print(pairwise_diff([10, 7, 3, 8]))  # [-3, -4, 5]
    ```

---

**Exercise 3.**
Use `tee` with `n=3` to compute the mean, minimum, and maximum of an iterator in a single pass. Write a function `stats` that returns `(mean, min_val, max_val)`. For example, `stats([4, 1, 7, 3])` should return `(3.75, 1, 7)`.

??? success "Solution to Exercise 3"

    ```python
    from itertools import tee

    def stats(iterable):
        it1, it2, it3 = tee(iterable, 3)
        values = list(it1)
        mean = sum(it2) / len(values)
        min_val = min(it3)
        max_val = max(values)
        return (mean, min_val, max_val)

    # Test
    print(stats([4, 1, 7, 3]))  # (3.75, 1, 7)
    ```
