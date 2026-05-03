# functools.cache (Python 3.9+)

The `@cache` decorator provides simple, unbounded memoization. It's a simpler alternative to `@lru_cache` when you don't need cache size limits.

!!! tip "Mental Model"
    `@cache` is a dictionary that sits in front of your function: before executing, it checks whether it has already seen these arguments. If yes, it returns the stored result instantly. The cache grows without bound, so it trades memory for speed -- perfect for pure functions with a finite input domain.

```python
from functools import cache  # Python 3.9+
```

---

## Basic Usage

```python
from functools import cache

@cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Without cache: exponential time O(2^n)
# With cache: linear time O(n)
print(fibonacci(100))  # Instant!
```

---

## cache vs lru_cache

| Feature | `@cache` | `@lru_cache` |
|---------|----------|--------------|
| Python version | 3.9+ | 3.2+ |
| Cache size | Unlimited | Configurable (default 128) |
| Eviction | Never | LRU (Least Recently Used) |
| Memory | Grows forever | Bounded |
| Syntax | `@cache` | `@lru_cache(maxsize=N)` |
| Use case | Small domains, recursive | Large domains, memory limits |

### Equivalence

```python
from functools import cache, lru_cache

# These are equivalent:
@cache
def func1(x): pass

@lru_cache(maxsize=None)
def func2(x): pass
```

---

## When to Use cache

### Good Use Cases

```python
from functools import cache

# 1. Recursive algorithms with overlapping subproblems
@cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# 2. Pure functions with expensive computation
@cache
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# 3. Functions with limited input domain
@cache
def parse_config(config_name):
    """Config names are finite and repeated often."""
    return load_and_parse(config_name)
```

### When NOT to Use

```python
# 1. Functions with unlimited input domain
@cache  # Bad: cache grows forever!
def process(data):
    return expensive_operation(data)

# 2. Functions with mutable arguments
@cache  # Error: lists aren't hashable
def process_list(items):  
    return sum(items)

# 3. Functions with side effects
@cache  # Bad: side effect only happens once!
def log_and_compute(x):
    print(f"Computing {x}")  # Only prints first time
    return x ** 2
```

---

## Cache Management

### Check Cache Statistics

```python
from functools import cache

@cache
def square(x):
    return x ** 2

square(1)
square(2)
square(1)  # Cache hit
square(3)

print(square.cache_info())
# CacheInfo(hits=1, misses=3, maxsize=None, currsize=3)
```

### Clear the Cache

```python
@cache
def compute(x):
    return x ** 2

compute(1)
compute(2)

# Clear all cached values
compute.cache_clear()

print(square.cache_info())
# CacheInfo(hits=0, misses=0, maxsize=None, currsize=0)
```

### Cache Parameters (Python 3.9+)

```python
from functools import cache

@cache
def func(x):
    return x ** 2

# Get cache parameters
print(func.cache_parameters())
# {'maxsize': None, 'typed': False}
```

---

## Practical Examples

### Recursive Dynamic Programming

```python
from functools import cache

@cache
def coin_change(amount, coins):
    """Minimum coins needed for amount."""
    if amount == 0:
        return 0
    if amount < 0:
        return float('inf')
    
    return 1 + min(
        coin_change(amount - coin, coins) 
        for coin in coins
    )

# Convert list to tuple (hashable)
coins = (1, 5, 10, 25)
print(coin_change(67, coins))  # 7
```

### Path Counting

```python
from functools import cache

@cache
def count_paths(m, n):
    """Count paths in m x n grid (right and down only)."""
    if m == 1 or n == 1:
        return 1
    return count_paths(m - 1, n) + count_paths(m, n - 1)

print(count_paths(20, 20))  # 35345263800
```

### String Edit Distance

```python
from functools import cache

@cache
def edit_distance(s1, s2):
    """Levenshtein distance between two strings."""
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)
    
    if s1[0] == s2[0]:
        return edit_distance(s1[1:], s2[1:])
    
    return 1 + min(
        edit_distance(s1[1:], s2),      # delete
        edit_distance(s1, s2[1:]),      # insert
        edit_distance(s1[1:], s2[1:])   # replace
    )

print(edit_distance("kitten", "sitting"))  # 3
```

### Configuration Lookup

```python
from functools import cache
import json

@cache
def get_config(name):
    """Load configuration (cached after first load)."""
    with open(f"configs/{name}.json") as f:
        return json.load(f)

# First call: reads file
config1 = get_config("database")

# Second call: returns cached value
config2 = get_config("database")
```

---

## Argument Requirements

### Must Be Hashable

```python
from functools import cache

@cache
def process(data):
    return sum(data)

# Works: hashable types
process((1, 2, 3))      # tuple - OK
process("hello")        # str - OK
process(frozenset({1})) # frozenset - OK

# Fails: unhashable types
# process([1, 2, 3])    # list - TypeError
# process({1, 2, 3})    # set - TypeError
# process({'a': 1})     # dict - TypeError
```

### Converting Unhashable Arguments

```python
from functools import cache

# Wrapper to handle lists
def process_list(items):
    return _process_tuple(tuple(items))

@cache
def _process_tuple(items):
    return sum(items)

# Now works with lists
result = process_list([1, 2, 3, 4, 5])
```

---

## typed Parameter

By default, arguments of different types that compare equal share cache entries:

```python
from functools import lru_cache

@lru_cache(maxsize=None)  # Same as @cache
def func(x):
    print(f"Computing for {x} ({type(x).__name__})")
    return x * 2

func(3)    # Computing for 3 (int)
func(3.0)  # No output - uses cached result for 3

# With typed=True (requires lru_cache)
@lru_cache(maxsize=None, typed=True)
def func_typed(x):
    print(f"Computing for {x} ({type(x).__name__})")
    return x * 2

func_typed(3)    # Computing for 3 (int)
func_typed(3.0)  # Computing for 3.0 (float) - separate entry
```

Note: `@cache` doesn't support `typed` parameter. Use `@lru_cache(maxsize=None, typed=True)` if needed.

---

## Memory Considerations

### Cache Grows Without Bound

```python
from functools import cache

@cache
def process(x):
    return x ** 2

# Each unique argument adds to cache
for i in range(1_000_000):
    process(i)

# Cache now holds 1 million entries!
print(process.cache_info().currsize)  # 1000000
```

### Clearing Cache Periodically

```python
from functools import cache

@cache
def compute(x):
    return expensive_operation(x)

def process_batch(items):
    results = [compute(item) for item in items]
    compute.cache_clear()  # Clear after batch
    return results
```

### Use lru_cache for Bounded Memory

```python
from functools import lru_cache

# Limit cache to 1000 entries
@lru_cache(maxsize=1000)
def process(x):
    return x ** 2

# Automatically evicts oldest entries when full
```

---

## Comparison with Manual Memoization

```python
# Manual memoization
def fibonacci_manual(n, memo={}):
    if n in memo:
        return memo[n]
    if n < 2:
        return n
    memo[n] = fibonacci_manual(n - 1) + fibonacci_manual(n - 2)
    return memo[n]

# With @cache (cleaner)
from functools import cache

@cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

Benefits of `@cache`:
- Cleaner code (no manual memo dict)
- Thread-safe
- Built-in cache management (info, clear)
- Properly handles function metadata

---

## Summary

| Feature | Details |
|---------|---------|
| Import | `from functools import cache` |
| Python version | 3.9+ |
| Equivalent | `@lru_cache(maxsize=None)` |
| Cache size | Unlimited |
| Argument requirement | Must be hashable |
| Methods | `.cache_info()`, `.cache_clear()`, `.cache_parameters()` |

**Key Takeaways**:

- `@cache` is simpler than `@lru_cache` for unlimited caching
- Use for recursive algorithms and expensive pure functions
- Arguments must be hashable (use tuples, not lists)
- Cache grows forever — clear manually or use `@lru_cache` for bounds
- Don't use with side effects or unlimited input domains
- Available in Python 3.9+; use `@lru_cache(maxsize=None)` for earlier versions

---

## Exercises

**Exercise 1.**
Write a recursive `factorial(n)` function decorated with `@cache`. Call it for `n = 100` and verify the result. Then inspect the cache with `factorial.cache_info()` and print the number of hits and misses.

??? success "Solution to Exercise 1"

        from functools import cache

        @cache
        def factorial(n):
            if n <= 1:
                return 1
            return n * factorial(n - 1)

        print(factorial(100))
        info = factorial.cache_info()
        print(f"Hits: {info.hits}, Misses: {info.misses}")

---

**Exercise 2.**
Use `@cache` to memoize a `count_paths(m, n)` function that counts the number of unique paths from the top-left to the bottom-right of an `m x n` grid (moving only right or down). Verify that `count_paths(3, 3)` returns `6` and `count_paths(10, 10)` returns `48620`.

??? success "Solution to Exercise 2"

        from functools import cache

        @cache
        def count_paths(m, n):
            if m == 1 or n == 1:
                return 1
            return count_paths(m - 1, n) + count_paths(m, n - 1)

        print(count_paths(3, 3))     # 6
        print(count_paths(10, 10))   # 48620

---

**Exercise 3.**
Demonstrate the unbounded-growth risk of `@cache`. Write a cached function `process(data)` that accepts a tuple of integers and returns their sum. Call it with 10,000 different inputs, print the cache size via `cache_info()`, then call `cache_clear()` and confirm the cache is empty.

??? success "Solution to Exercise 3"

        from functools import cache

        @cache
        def process(data):
            return sum(data)

        for i in range(10_000):
            process((i, i + 1, i + 2))

        info = process.cache_info()
        print(f"Cache size (misses): {info.misses}")  # 10000

        process.cache_clear()
        info = process.cache_info()
        print(f"After clear — hits: {info.hits}, misses: {info.misses}")  # 0, 0
