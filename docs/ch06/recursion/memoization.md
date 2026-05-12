# Memoization and Recursion

Memoization caches function results to avoid redundant computations. It transforms exponential-time recursive algorithms into polynomial-time solutions.

!!! tip "Mental Model"
    Memoization is a lookup table for function calls: before computing, check whether you've already solved this exact subproblem. If yes, return the cached answer; if no, compute it, store it, then return it. This single optimization can turn an exponential algorithm into a linear one by ensuring each unique subproblem is solved only once.

---

## The Problem: Redundant Computation

```python
def fibonacci(n):
    '''Naive fibonacci: exponential time O(2^n)'''
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# fibonacci(5) calls fibonacci(3) three times, fibonacci(2) five times!
# Time complexity: O(2^n)
import time
start = time.time()
result = fibonacci(35)
elapsed = time.time() - start
print(f"fibonacci(35) = {result}, took {elapsed:.2f} seconds")
```

## lru_cache Decorator

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci_cached(n):
    '''Memoized fibonacci: linear time O(n)'''
    if n <= 1:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)

# Now O(n) instead of O(2^n)!
import time
start = time.time()
result = fibonacci_cached(35)
elapsed = time.time() - start
print(f"fibonacci_cached(35) = {result}, took {elapsed:.6f} seconds")

# View cache statistics
print(fibonacci_cached.cache_info())
```

## Manual Memoization

```python
def fibonacci_memo(n, cache=None):
    '''Manual memoization with dictionary'''
    if cache is None:
        cache = {}
    
    if n in cache:
        return cache[n]
    
    if n <= 1:
        return n
    
    cache[n] = fibonacci_memo(n - 1, cache) + fibonacci_memo(n - 2, cache)
    return cache[n]

print(fibonacci_memo(30))  # Nearly instant
```

## Example: Longest Common Subsequence

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def lcs(text1, text2):
    '''Longest common subsequence using memoization'''
    if not text1 or not text2:
        return 0
    
    if text1[0] == text2[0]:
        return 1 + lcs(text1[1:], text2[1:])
    
    return max(
        lcs(text1[1:], text2),
        lcs(text1, text2[1:])
    )

print(lcs("abcde", "ace"))     # 3
print(lcs.cache_info())         # Show cache hits/misses
```

## Cache Strategies

```python
from functools import lru_cache

# Limited cache size (evicts least recently used)
@lru_cache(maxsize=128)
def expensive_function(x):
    return x ** 2

# Unbounded cache (use with caution)
@lru_cache(maxsize=None)
def mathematical_function(n):
    return n * (n + 1) // 2

# Clear cache when needed
expensive_function.cache_clear()
```

## Performance Impact

Memoization provides dramatic speedup for recursive algorithms with overlapping subproblems:

- Without memoization: O(2^n)
- With memoization: O(n)

---

## Exercises

**Exercise 1.**
Write a memoized recursive function `coin_change(amount, coins)` that returns the minimum number of coins needed to make the given amount. Use a dictionary for manual memoization. Test with `coin_change(11, (1, 5, 6))` (expected: `3`, using 5+5+1 or 6+5).

??? success "Solution to Exercise 1"

        def coin_change(amount, coins, memo=None):
            if memo is None:
                memo = {}
            if amount == 0:
                return 0
            if amount < 0:
                return float("inf")
            if amount in memo:
                return memo[amount]

            min_coins = float("inf")
            for coin in coins:
                result = coin_change(amount - coin, coins, memo)
                min_coins = min(min_coins, result + 1)

            memo[amount] = min_coins
            return min_coins

        print(coin_change(11, (1, 5, 6)))   # 3
        print(coin_change(15, (1, 5, 10)))  # 2

---

**Exercise 2.**
Implement the `climb_stairs(n)` problem (number of ways to reach step `n` by taking 1 or 2 steps at a time) using `@lru_cache`. Compute `climb_stairs(30)` and print the cache statistics.

??? success "Solution to Exercise 2"

        from functools import lru_cache

        @lru_cache(maxsize=None)
        def climb_stairs(n):
            if n <= 1:
                return 1
            return climb_stairs(n - 1) + climb_stairs(n - 2)

        print(climb_stairs(30))              # 1346269
        print(climb_stairs.cache_info())

---

**Exercise 3.**
Write a manual memoization decorator `@memoize` that stores results in a dictionary. Apply it to a recursive `fibonacci(n)` function. Compare performance by timing `fibonacci(35)` with and without the decorator.

??? success "Solution to Exercise 3"

        import time

        def memoize(func):
            cache = {}
            def wrapper(*args):
                if args not in cache:
                    cache[args] = func(*args)
                return cache[args]
            return wrapper

        # Without memoization
        def fib_slow(n):
            if n < 2:
                return n
            return fib_slow(n - 1) + fib_slow(n - 2)

        # With memoization
        @memoize
        def fib_fast(n):
            if n < 2:
                return n
            return fib_fast(n - 1) + fib_fast(n - 2)

        start = time.time()
        print(fib_slow(35))
        print(f"Without memo: {time.time() - start:.3f}s")

        start = time.time()
        print(fib_fast(35))
        print(f"With memo:    {time.time() - start:.6f}s")
