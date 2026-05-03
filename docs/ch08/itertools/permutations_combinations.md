# permutations and combinations

These functions generate all permutations (order matters) and combinations (order doesn't matter) from an iterable.

!!! tip "Mental Model"
    Permutations answer "in how many ways can I arrange these items?" — order matters, so (A, B) differs from (B, A). Combinations answer "in how many ways can I choose a subset?" — order is ignored, so {A, B} and {B, A} count as one. Both generators are lazy, but beware: the number of results grows explosively with input size.

## permutations() - Order Matters

Generate all ordered arrangements of elements.

```python
from itertools import permutations

items = [1, 2, 3]
perms = list(permutations(items, 2))
print(perms)
print(f"Count: {len(perms)}")
```

```
[(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
Count: 6
```

## combinations() - Order Doesn't Matter

Generate all unique unordered subsets of elements.

```python
from itertools import combinations

items = [1, 2, 3, 4]
combos = list(combinations(items, 2))
print(combos)
print(f"Count: {len(combos)}")
```

```
[(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
Count: 6
```

## combinations_with_replacement()

Generate combinations where elements can be repeated.

```python
from itertools import combinations_with_replacement

items = ['A', 'B', 'C']
combos = list(combinations_with_replacement(items, 2))
print(combos)
```

```
[('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')]
```

---

## Exercises

**Exercise 1.**
Write a function `count_arrangements` that takes a string and an integer `r`, and returns the number of unique permutations of length `r` from the characters. For example, `count_arrangements("ABCD", 2)` should return `12`.

??? success "Solution to Exercise 1"

    ```python
    from itertools import permutations

    def count_arrangements(s, r):
        return len(list(permutations(s, r)))

    # Test
    print(count_arrangements("ABCD", 2))  # 12
    print(count_arrangements("ABC", 3))   # 6
    ```

---

**Exercise 2.**
Write a function `lottery_combinations` that takes a range of numbers (1 to n) and a pick count `k`, and returns all possible lottery combinations. For example, `lottery_combinations(5, 3)` should return all `combinations(range(1, 6), 3)` as a list of tuples.

??? success "Solution to Exercise 2"

    ```python
    from itertools import combinations

    def lottery_combinations(n, k):
        return list(combinations(range(1, n + 1), k))

    # Test
    result = lottery_combinations(5, 3)
    print(result)
    # [(1, 2, 3), (1, 2, 4), (1, 2, 5), (1, 3, 4),
    #  (1, 3, 5), (1, 4, 5), (2, 3, 4), (2, 3, 5),
    #  (2, 4, 5), (3, 4, 5)]
    print(f"Total: {len(result)}")  # 10
    ```

---

**Exercise 3.**
Write a function `coin_combinations` that takes a list of coin denominations and a target number of coins, and returns all possible multisets of coins of that size using `combinations_with_replacement`. For example, `coin_combinations([1, 5, 10], 2)` should return `[(1, 1), (1, 5), (1, 10), (5, 5), (5, 10), (10, 10)]`.

??? success "Solution to Exercise 3"

    ```python
    from itertools import combinations_with_replacement

    def coin_combinations(denominations, count):
        return list(combinations_with_replacement(denominations, count))

    # Test
    result = coin_combinations([1, 5, 10], 2)
    print(result)
    # [(1, 1), (1, 5), (1, 10), (5, 5), (5, 10), (10, 10)]
    ```
