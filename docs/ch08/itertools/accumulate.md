# accumulate

`accumulate()` applies a function cumulatively to items, computing running totals or products. Running accumulations appear frequently in data processing tasks such as computing cumulative sums for time series, tracking running extremes, or building prefix computations. This function provides a concise, iterator-based approach to these patterns without requiring manual loop state.

!!! tip "Mental Model"
    `accumulate` is a snowball rolling downhill — each step folds the next element into the running result. By default it adds, but you can supply any two-argument function to compute running products, running maximums, or any other cumulative operation. The key insight is that it yields every intermediate result, not just the final one.

## Cumulative Sum

The simplest use of `accumulate()` computes a running total. When no function argument is provided, it defaults to addition, yielding the cumulative sum at each position.

```python
from itertools import accumulate

data = [1, 2, 3, 4, 5]
result = list(accumulate(data))
print(result)
```

```
[1, 3, 6, 10, 15]
```

## Custom Accumulation Function

By passing a two-argument function as the second parameter, you can customize the accumulation operation. The function receives the accumulated value so far and the next element from the iterable.

```python
from itertools import accumulate
import operator

data = [1, 2, 3, 4]

# Cumulative product
product = list(accumulate(data, operator.mul))
print("Product:", product)

# Running maximum (using a wrapper for clarity)
def track_max(a, b):
    return max(a, b)

values = [3, 1, 5, 2, 8, 4]
max_so_far = list(accumulate(values, track_max))
print("Max so far:", max_so_far)
```

```
Product: [1, 2, 6, 24]
Max so far: [3, 3, 5, 5, 8, 8]
```

---

## Exercises

**Exercise 1.**
Use `accumulate` to compute a running balance from a list of transactions (positive for deposits, negative for withdrawals) starting from an initial balance of 1000. For example, given transactions `[200, -50, -100, 300]`, the running balances should be `[1200, 1150, 1050, 1350]`.

??? success "Solution to Exercise 1"

    ```python
    from itertools import accumulate
    import operator

    initial_balance = 1000
    transactions = [200, -50, -100, 300]
    adjusted = [initial_balance + transactions[0]] + transactions[1:]
    balances = list(accumulate(
        transactions, operator.add, initial=initial_balance
    ))
    # Drop the initial value
    print(balances[1:])  # [1200, 1150, 1050, 1350]
    ```

---

**Exercise 2.**
Use `accumulate` with `min` to compute the running minimum of a list of numbers. For example, given `[5, 3, 8, 1, 9, 2]`, the result should be `[5, 3, 3, 1, 1, 1]`.

??? success "Solution to Exercise 2"

    ```python
    from itertools import accumulate

    values = [5, 3, 8, 1, 9, 2]
    running_min = list(accumulate(values, min))
    print(running_min)  # [5, 3, 3, 1, 1, 1]
    ```

---

**Exercise 3.**
Use `accumulate` with a custom function to compute a running concatenation of strings with a separator. For example, given `["a", "b", "c", "d"]` with separator `"-"`, the result should be `["a", "a-b", "a-b-c", "a-b-c-d"]`.

??? success "Solution to Exercise 3"

    ```python
    from itertools import accumulate

    words = ["a", "b", "c", "d"]
    running_concat = list(accumulate(words, lambda a, b: f"{a}-{b}"))
    print(running_concat)
    # ['a', 'a-b', 'a-b-c', 'a-b-c-d']
    ```
