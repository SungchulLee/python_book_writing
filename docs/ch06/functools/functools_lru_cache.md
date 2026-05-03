# functools.lru_cache

The `@lru_cache` decorator provides memoization with a **Least Recently Used** eviction policy. It caches function results and automatically removes the oldest entries when the cache reaches its size limit.

!!! tip "Mental Model"
    `@lru_cache` is memoization with a memory budget. It stores results in a dictionary keyed by arguments, but when the cache is full, it evicts the least recently used entry. Think of it as a fixed-size notepad: you jot down answers to save work, but when the notepad is full, you erase the oldest note you haven't looked at recently.

```python
from functools import lru_cache
```

---

## Basic Usage

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Without cache: exponential time O(2^n)
# With cache: linear time O(n)
print(fibonacci(100))  # Instant!
```

---

## maxsize Options

The `maxsize` parameter controls cache behavior:

```python
from functools import lru_cache

# maxsize=128 (default) — LRU eviction when full
@lru_cache(maxsize=128)
def func1(x):
    return x ** 2

# maxsize=None — unlimited cache, never evicts
@lru_cache(maxsize=None)
def func2(x):
    return x ** 2

# maxsize=0 — no caching (useful for testing)
@lru_cache(maxsize=0)
def func3(x):
    return x ** 2

# Without parentheses (Python 3.8+) — uses default maxsize=128
@lru_cache
def func4(x):
    return x ** 2
```

### How LRU Eviction Works

```python
@lru_cache(maxsize=3)
def process(x):
    print(f"  Computing {x}")
    return x ** 2

process(1)  # Computing 1 → cache: [1]
process(2)  # Computing 2 → cache: [1, 2]
process(3)  # Computing 3 → cache: [1, 2, 3]
process(1)  # Cache hit    → cache: [2, 3, 1] (1 moved to end)
process(4)  # Computing 4  → cache: [3, 1, 4] (2 evicted — least recently used)
process(2)  # Computing 2  → cache: [1, 4, 2] (3 evicted)
```

---

## Cache Management Methods

Every decorated function gains three methods:

### cache_info()

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def square(x):
    return x ** 2

square(1)
square(2)
square(1)  # Cache hit
square(3)

info = square.cache_info()
print(info)
# CacheInfo(hits=1, misses=3, maxsize=128, currsize=3)

print(info.hits)      # 1  — number of cache hits
print(info.misses)    # 3  — number of cache misses
print(info.maxsize)   # 128 — maximum cache size
print(info.currsize)  # 3  — current number of cached entries
```

### cache_clear()

```python
@lru_cache(maxsize=128)
def compute(x):
    return x ** 2

compute(1)
compute(2)
print(compute.cache_info().currsize)  # 2

compute.cache_clear()
print(compute.cache_info().currsize)  # 0
```

### cache_parameters() (Python 3.9+)

```python
@lru_cache(maxsize=256, typed=True)
def func(x):
    return x ** 2

print(func.cache_parameters())
# {'maxsize': 256, 'typed': True}
```

---

## typed Parameter

By default, arguments of different types that compare equal share cache entries:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def compute(x):
    print(f"  Computing {x} ({type(x).__name__})")
    return x * 2

compute(3)    # Computing 3 (int)
compute(3.0)  # No output — cache hit! (3 == 3.0)
```

With `typed=True`, different types get separate entries:

```python
@lru_cache(maxsize=128, typed=True)
def compute(x):
    print(f"  Computing {x} ({type(x).__name__})")
    return x * 2

compute(3)    # Computing 3 (int)
compute(3.0)  # Computing 3.0 (float) — separate entry
```

---

## Argument Requirements

### Must Be Hashable

All arguments must be hashable because `lru_cache` uses them as dictionary keys:

```python
@lru_cache
def process(data):
    return sum(data)

# Works: hashable types
process((1, 2, 3))        # tuple — OK
process("hello")          # str — OK
process(frozenset({1}))   # frozenset — OK

# Fails: unhashable types
# process([1, 2, 3])      # TypeError: unhashable type: 'list'
# process({1, 2, 3})      # TypeError: unhashable type: 'set'
# process({'a': 1})       # TypeError: unhashable type: 'dict'
```

### Converting Unhashable Arguments

```python
from functools import lru_cache

# Strategy 1: Wrapper that converts to tuple
def process_list(items):
    return _process(tuple(items))

@lru_cache(maxsize=128)
def _process(items):
    return sum(items)

# Strategy 2: Convert dict to frozenset of items
def process_dict(d):
    return _process_dict(frozenset(d.items()))

@lru_cache(maxsize=128)
def _process_dict(items):
    return dict(items)
```

---

## Practical Examples

### Recursive Dynamic Programming

```python
from functools import lru_cache

@lru_cache(maxsize=None)
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

coins = (1, 5, 10, 25)
print(coin_change(67, coins))  # 7
```

### Expensive Computation

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_query(user_id, date):
    """Cache database results for repeated queries."""
    return fetch_from_database(user_id, date)

# First call: hits database
result1 = expensive_query("user_123", "2024-01-01")

# Second call: returns cached result
result2 = expensive_query("user_123", "2024-01-01")
```

### Web API Response Caching

```python
from functools import lru_cache
import json

@lru_cache(maxsize=256)
def get_exchange_rate(base, target):
    """Cache exchange rates (limited domain)."""
    response = requests.get(f"https://api.example.com/rate/{base}/{target}")
    return response.json()['rate']

# Avoids repeated API calls for same currency pair
rate = get_exchange_rate("USD", "EUR")
```

### Recursive String Operations

```python
from functools import lru_cache

@lru_cache(maxsize=None)
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

---

## lru_cache vs cache

| Feature | `@lru_cache` | `@cache` |
|---------|-------------|----------|
| Python version | 3.2+ | 3.9+ |
| Cache size | Configurable (default 128) | Unlimited |
| Eviction | LRU (Least Recently Used) | Never |
| Memory | Bounded | Grows forever |
| `typed` parameter | Yes | No |
| Use case | Large/unknown domains | Small domains, recursive |

```python
from functools import lru_cache, cache

# Equivalent:
@cache
def func1(x): ...

@lru_cache(maxsize=None)
def func2(x): ...
```

**Decision guide**:

- Use `@cache` for recursive algorithms with bounded input (fibonacci, DP)
- Use `@lru_cache(maxsize=N)` for functions with large/unbounded input domains
- Use `@lru_cache(maxsize=None)` as a pre-3.9 equivalent of `@cache`

---

## Memory Considerations

### Monitoring Cache Size

```python
@lru_cache(maxsize=1000)
def process(x):
    return x ** 2

for i in range(5000):
    process(i)

info = process.cache_info()
print(f"Size: {info.currsize}/{info.maxsize}")  # Size: 1000/1000
print(f"Hit rate: {info.hits / (info.hits + info.misses):.1%}")
```

### Tuning maxsize

```python
# Too small: many evictions, low hit rate
@lru_cache(maxsize=10)
def func(x): ...

# Too large: wastes memory
@lru_cache(maxsize=1_000_000)
def func(x): ...

# Strategy: monitor hit rate and adjust
# Good hit rate (>80%) → maxsize is adequate
# Low hit rate (<50%) → increase maxsize or rethink caching
```

### Clearing Cache for Long-Running Processes

```python
@lru_cache(maxsize=1000)
def compute(x):
    return expensive_operation(x)

def process_batch(items):
    results = [compute(item) for item in items]
    # Clear cache between batches to free memory
    compute.cache_clear()
    return results
```

---

## Thread Safety

`lru_cache` is thread-safe. The underlying dictionary is protected by a lock:

```python
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

@lru_cache(maxsize=128)
def compute(x):
    return x ** 2

# Safe to call from multiple threads
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(compute, range(100)))
```

However, the decorated function itself may still have race conditions if it has side effects.

---

## Common Pitfalls

### Caching Functions with Side Effects

```python
@lru_cache
def log_and_compute(x):
    print(f"Computing {x}")  # Side effect: only executes on cache miss
    return x ** 2

log_and_compute(5)  # "Computing 5" — printed
log_and_compute(5)  # Nothing printed — cached result returned
```

### Methods and self

```python
class MyClass:
    @lru_cache(maxsize=128)  # Caution: self is part of the cache key
    def compute(self, x):
        return x ** 2

# Each instance has separate cache entries
# AND instances are kept alive by cache references!
```

**Solution**: use `__hash__` carefully or prefer `cached_property` for instance methods.

### Mutable Default State

```python
# The cache does NOT detect changes to external state
data = [1, 2, 3]

@lru_cache
def process(index):
    return data[index]  # Caches based on index, not data contents

process(0)      # Returns 1
data[0] = 999
process(0)      # Still returns 1 (cached!)
```

---

## Implementation Details

- Uses a **doubly-linked list** for O(1) LRU operations
- Uses a **dictionary** for O(1) lookups
- Cache key is `(args, kwargs)` converted to a hashable form
- `maxsize` should be a power of 2 for best performance (internal hash table sizing)

```python
# Optimal maxsize values
@lru_cache(maxsize=64)    # 2^6
@lru_cache(maxsize=128)   # 2^7 (default)
@lru_cache(maxsize=256)   # 2^8
@lru_cache(maxsize=1024)  # 2^10
```

---

## Summary

| Feature | Details |
|---------|---------|
| Import | `from functools import lru_cache` |
| Python version | 3.2+ |
| Default maxsize | 128 |
| Eviction policy | Least Recently Used |
| Arguments | Must be hashable |
| Thread safe | Yes |
| Methods | `.cache_info()`, `.cache_clear()`, `.cache_parameters()` |

**Key Takeaways**:

- `@lru_cache` provides bounded memoization with automatic LRU eviction
- Set `maxsize` based on expected input domain (power of 2 is optimal)
- Monitor hit rate with `cache_info()` to tune `maxsize`
- Use `typed=True` when `int` and `float` arguments need separate cache entries
- Arguments must be hashable — convert lists to tuples, dicts to frozensets
- Thread-safe but beware of side effects in the cached function
- For unlimited caching, use `@cache` (Python 3.9+) or `@lru_cache(maxsize=None)`

---

## Exercises

**Exercise 1.**
Write a function `expensive_lookup(key)` that simulates a slow database call with `time.sleep(0.5)` and returns `key.upper()`. Decorate it with `@lru_cache(maxsize=32)`. Call it three times with the same key and verify that only the first call is slow. Print `cache_info()` to confirm the hit count.

??? success "Solution to Exercise 1"

        import time
        from functools import lru_cache

        @lru_cache(maxsize=32)
        def expensive_lookup(key):
            time.sleep(0.5)
            return key.upper()

        start = time.time()
        print(expensive_lookup("hello"))  # Slow
        print(f"First call: {time.time() - start:.2f}s")

        start = time.time()
        print(expensive_lookup("hello"))  # Fast (cached)
        print(f"Second call: {time.time() - start:.2f}s")

        print(expensive_lookup("hello"))  # Fast (cached)
        print(expensive_lookup.cache_info())

---

**Exercise 2.**
Demonstrate the effect of `typed=True`. Write a cached function `add_one(x)` decorated with `@lru_cache(maxsize=128, typed=True)`. Call it with `add_one(1)` and `add_one(1.0)`. Print `cache_info()` and verify that both are cache misses (two separate entries). Then repeat without `typed=True` and show that `1` and `1.0` share a cache entry.

??? success "Solution to Exercise 2"

        from functools import lru_cache

        # With typed=True
        @lru_cache(maxsize=128, typed=True)
        def add_one_typed(x):
            return x + 1

        add_one_typed(1)
        add_one_typed(1.0)
        print(add_one_typed.cache_info())  # misses=2 (separate entries)

        # Without typed (default False)
        @lru_cache(maxsize=128)
        def add_one_untyped(x):
            return x + 1

        add_one_untyped(1)
        add_one_untyped(1.0)
        print(add_one_untyped.cache_info())  # misses=1 (shared entry)

---

**Exercise 3.**
Write a recursive `climb_stairs(n)` function (number of ways to climb `n` stairs taking 1 or 2 steps at a time) and decorate it with `@lru_cache(maxsize=64)`. Compute `climb_stairs(50)`, print the result and cache stats. Then call `cache_clear()` and verify the cache is reset.

??? success "Solution to Exercise 3"

        from functools import lru_cache

        @lru_cache(maxsize=64)
        def climb_stairs(n):
            if n <= 1:
                return 1
            return climb_stairs(n - 1) + climb_stairs(n - 2)

        print(climb_stairs(50))              # 20365011074
        print(climb_stairs.cache_info())
        climb_stairs.cache_clear()
        print(climb_stairs.cache_info())     # hits=0, misses=0
