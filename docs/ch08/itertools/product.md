# product - Cartesian Product

The `product()` function computes the Cartesian product of input iterables, generating all ordered tuples by selecting one element from each iterable. It replaces nested for-loops with a single flat iterator, producing more concise code and avoiding deep indentation when iterating over multiple dimensions.

!!! tip "Mental Model"
    `product` is a nested-loop flattener. If you would write `for x in A: for y in B: for z in C:`, then `product(A, B, C)` yields every `(x, y, z)` combination in a single flat stream. Each additional iterable adds another "dimension," and the total number of tuples is the product of all input lengths.

## Basic Cartesian Product

Pass two or more iterables to `product()` and it yields every possible ordered tuple containing one element from each. This is equivalent to nested for-loops but expressed as a single flat iterator.

```python
from itertools import product

colors = ['red', 'green']
sizes = ['S', 'M', 'L']

combinations = list(product(colors, sizes))
print(combinations)
```

```
[('red', 'S'), ('red', 'M'), ('red', 'L'), ('green', 'S'), ('green', 'M'), ('green', 'L')]
```

## Multiple Iterables and Repeat

The `repeat` parameter specifies how many times the input iterable is repeated in the product. `product(A, repeat=3)` is equivalent to `product(A, A, A)`.

```python
from itertools import product

# Pairs from a single iterable
pairs = list(product([1, 2, 3], repeat=2))
print(pairs)

# Self-product with 3 iterations
triples = list(product('AB', repeat=3))
print(triples)
```

```
[(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
[('A', 'A', 'A'), ('A', 'A', 'B'), ('A', 'B', 'A'), ('A', 'B', 'B'), ('B', 'A', 'A'), ('B', 'A', 'B'), ('B', 'B', 'A'), ('B', 'B', 'B')]
```

---

## Exercises

**Exercise 1.**
Use `product` to generate all possible outcomes of rolling two six-sided dice (numbers 1-6). Return the results as a list of tuples. How many outcomes are there in total?

??? success "Solution to Exercise 1"

    ```python
    from itertools import product

    dice = list(product(range(1, 7), repeat=2))
    print(f"Total outcomes: {len(dice)}")  # 36
    print(dice[:6])  # First 6: (1,1) through (1,6)
    ```

---

**Exercise 2.**
Use `product` with `repeat=4` to generate all 4-digit binary strings (using characters `"0"` and `"1"`). Convert each tuple to a string and return the list. For example, the list should include `"0000"`, `"0001"`, ..., `"1111"`.

??? success "Solution to Exercise 2"

    ```python
    from itertools import product

    binary_strings = [
        "".join(bits) for bits in product("01", repeat=4)
    ]
    print(binary_strings)
    # ['0000', '0001', '0010', ..., '1111']
    print(f"Total: {len(binary_strings)}")  # 16
    ```

---

**Exercise 3.**
Write a function `grid_coordinates` that takes two ranges (rows and columns) and uses `product` to generate all `(row, col)` coordinates. For example, `grid_coordinates(range(3), range(4))` should return 12 tuples from `(0, 0)` to `(2, 3)`.

??? success "Solution to Exercise 3"

    ```python
    from itertools import product

    def grid_coordinates(rows, cols):
        return list(product(rows, cols))

    # Test
    coords = grid_coordinates(range(3), range(4))
    print(coords)
    # [(0, 0), (0, 1), ..., (2, 3)]
    print(f"Total: {len(coords)}")  # 12
    ```
