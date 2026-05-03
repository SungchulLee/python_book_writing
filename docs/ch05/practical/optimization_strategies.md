# Optimization Strategies

Strategic code optimization requires identifying bottlenecks and applying targeted improvements. Here are proven techniques.

!!! tip "Mental Model"
    Optimization follows a strict priority order: algorithm first, data structure second, micro-optimization last. Replacing an O(n^2) loop with an O(n) set lookup dwarfs any micro-tweak. Always profile before optimizing -- the bottleneck is rarely where you think it is.

---

## Algorithmic Optimization

Always start with algorithm improvement for the biggest gains:

```python
# O(n²) - Inefficient
def find_duplicates_slow(numbers):
    duplicates = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] == numbers[j]:
                duplicates.append(numbers[i])
    return list(set(duplicates))

# O(n) - Efficient
def find_duplicates_fast(numbers):
    seen = set()
    duplicates = set()
    for num in numbers:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)
    return duplicates
```

## Built-in Functions vs. Loops

```python
# Slow: Python loop
def sum_squares_slow(numbers):
    total = 0
    for n in numbers:
        total += n ** 2
    return total

# Fast: Built-in function
def sum_squares_fast(numbers):
    return sum(n ** 2 for n in numbers)

# Fastest: NumPy for large data
import numpy as np
def sum_squares_numpy(numbers):
    return np.sum(np.array(numbers) ** 2)
```

## Caching and Memoization

```python
from functools import lru_cache

# Without caching: O(2^n)
def fib_slow(n):
    if n <= 1:
        return n
    return fib_slow(n - 1) + fib_slow(n - 2)

# With caching: O(n)
@lru_cache(maxsize=None)
def fib_fast(n):
    if n <= 1:
        return n
    return fib_fast(n - 1) + fib_fast(n - 2)
```

## String Operations

```python
# Slow: String concatenation in loop
result = ""
for i in range(1000):
    result += f"Item {i}
"

# Fast: Use join
result = "
".join(f"Item {i}" for i in range(1000))

# Also fast: StringIO for multiple operations
from io import StringIO
output = StringIO()
for i in range(1000):
    output.write(f"Item {i}
")
result = output.getvalue()
```

## Optimization Checklist

- Profile first to identify bottlenecks
- Improve algorithm complexity before micro-optimizations
- Use built-in functions (they're written in C)
- Avoid repeated attribute lookups
- Consider data structure choice (list vs. set vs. dict)
- Use generators for large datasets
- Cache expensive computations
- Consider NumPy/Pandas for numerical work

---

## Exercises

**Exercise 1.**
Write two versions of a function that finds all duplicate values in a list of 100,000 random integers (range 0-50,000): one with O(n^2) nested loops and one with O(n) using a set. Use `timeit` to benchmark both and print the speedup factor.

??? success "Solution to Exercise 1"
        ```python
        import timeit
        import random

        data = [random.randint(0, 50_000) for _ in range(100_000)]

        def find_dups_slow(nums):
            dups = set()
            for i in range(len(nums)):
                for j in range(i + 1, len(nums)):
                    if nums[i] == nums[j]:
                        dups.add(nums[i])
            return dups

        def find_dups_fast(nums):
            seen = set()
            dups = set()
            for n in nums:
                if n in seen:
                    dups.add(n)
                seen.add(n)
            return dups

        # Only time slow on a small subset
        small = data[:1000]
        t_slow = timeit.timeit(lambda: find_dups_slow(small), number=1)
        t_fast = timeit.timeit(lambda: find_dups_fast(data), number=1)

        print(f"O(n^2) on 1,000 items: {t_slow:.4f}s")
        print(f"O(n) on 100,000 items: {t_fast:.4f}s")
        print(f"Speedup: {t_slow / t_fast:.0f}x (on 100x fewer items!)")
        ```

---

**Exercise 2.**
Write a function that concatenates 50,000 strings using three methods: (a) `+=` in a loop, (b) `''.join()` on a list, and (c) `io.StringIO`. Benchmark all three with `timeit` and print a comparison table.

??? success "Solution to Exercise 2"
        ```python
        import timeit
        from io import StringIO

        n = 50_000

        def concat_plus():
            result = ""
            for i in range(n):
                result += f"item_{i} "
            return result

        def concat_join():
            return " ".join(f"item_{i}" for i in range(n))

        def concat_stringio():
            buf = StringIO()
            for i in range(n):
                buf.write(f"item_{i} ")
            return buf.getvalue()

        methods = [
            ("+=", concat_plus),
            ("join", concat_join),
            ("StringIO", concat_stringio),
        ]

        print(f"{'Method':<12} {'Time (s)':>10}")
        print("-" * 24)
        for name, func in methods:
            t = min(timeit.repeat(func, repeat=3, number=1))
            print(f"{name:<12} {t:>10.4f}")
        ```

---

**Exercise 3.**
Implement a Fibonacci function three ways: (a) naive recursion, (b) `@lru_cache`, and (c) iterative. Benchmark each for n=30 using `timeit`, print the times, and compute how many times faster the cached version is compared to the naive version.

??? success "Solution to Exercise 3"
        ```python
        import timeit
        from functools import lru_cache

        def fib_naive(n):
            if n <= 1:
                return n
            return fib_naive(n - 1) + fib_naive(n - 2)

        @lru_cache(maxsize=None)
        def fib_cached(n):
            if n <= 1:
                return n
            return fib_cached(n - 1) + fib_cached(n - 2)

        def fib_iter(n):
            if n <= 1:
                return n
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            return b

        t_naive = timeit.timeit(lambda: fib_naive(30), number=1)
        fib_cached.cache_clear()
        t_cached = timeit.timeit(lambda: fib_cached(30), number=1)
        t_iter = timeit.timeit(lambda: fib_iter(30), number=1)

        print(f"Naive:     {t_naive:.6f}s")
        print(f"Cached:    {t_cached:.6f}s")
        print(f"Iterative: {t_iter:.6f}s")
        print(f"Cached vs naive: {t_naive / t_cached:.0f}x faster")
        ```
