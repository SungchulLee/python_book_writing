# functools Module Overview

The `functools` module provides higher-order functions and operations on callable objects. It's essential for functional programming patterns in Python.

!!! tip "Mental Model"
    `functools` is Python's toolkit for working *on* functions rather than *with* them. It lets you freeze arguments (`partial`), cache results (`lru_cache`, `cache`), preserve metadata across decorators (`wraps`), fold sequences (`reduce`), and dispatch by type (`singledispatch`). Whenever you need to transform or augment a callable, check `functools` first.

```python
import functools
# or
from functools import partial, wraps, lru_cache, cache, reduce
```

---

## Module Contents at a Glance

| Function | Purpose | Python Version |
|----------|---------|----------------|
| `partial` | Freeze function arguments | 2.5+ |
| `reduce` | Cumulative fold operation | 2.6+ |
| `wraps` | Preserve decorator metadata | 2.5+ |
| `lru_cache` | Bounded memoization (LRU) | 3.2+ |
| `cache` | Unbounded memoization | 3.9+ |
| `total_ordering` | Complete comparison ops | 2.7+ |
| `singledispatch` | Type-based overloading | 3.4+ |
| `cached_property` | Lazy cached attribute | 3.8+ |
| `cmp_to_key` | Legacy comparison adapter | 2.7+ |

---

## How functools Fits into Python

### Relationship to Other Modules

```
functools          — higher-order functions, caching, dispatch
├── partial        — similar to lambda but preserves metadata
├── reduce         — moved here from built-ins in Python 3
├── wraps          — essential companion to decorators (Ch 5.6)
├── lru_cache      — memoization with eviction policy
├── cache          — simpler memoization (Python 3.9+)
└── singledispatch — type-based dispatch

operator           — function versions of operators (Ch 5.4)
itertools          — iterator combinators (Ch 7.2)
```

### Core Theme: Functions That Transform Functions

Every tool in `functools` takes a callable and produces a new callable:

```python
from functools import partial, lru_cache, wraps

# partial: fix arguments → new function
square = partial(pow, exp=2)

# lru_cache: add memoization → cached function
@lru_cache(maxsize=128)
def fib(n): ...

# wraps: copy metadata → wrapper with correct identity
def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

---

## Quick Examples

### partial — Freeze Arguments

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))    # 125
```

### reduce — Fold a Sequence

```python
from functools import reduce
import operator

numbers = [1, 2, 3, 4, 5]
product = reduce(operator.mul, numbers)
print(product)  # 120
```

### lru_cache — Memoize Results

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))  # Instant
print(fibonacci.cache_info())
# CacheInfo(hits=98, misses=101, maxsize=128, currsize=101)
```

### wraps — Preserve Metadata in Decorators

```python
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {time.perf_counter() - start:.4f}s")
        return result
    return wrapper

@timer
def process(data):
    """Process data."""
    return sum(data)

print(process.__name__)  # 'process' (not 'wrapper')
```

### total_ordering — Fill in Comparisons

```python
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor

    def __eq__(self, other):
        return (self.major, self.minor) == (other.major, other.minor)

    def __lt__(self, other):
        return (self.major, self.minor) < (other.major, other.minor)

# All six comparisons now work
v1, v2 = Version(1, 0), Version(2, 0)
print(v1 < v2)   # True (defined)
print(v1 <= v2)  # True (auto-generated)
print(v1 > v2)   # False (auto-generated)
```

### singledispatch — Type-Based Overloading

```python
from functools import singledispatch

@singledispatch
def process(data):
    raise NotImplementedError(f"Cannot process {type(data)}")

@process.register(list)
def _(data):
    return [x * 2 for x in data]

@process.register(str)
def _(data):
    return data.upper()

print(process([1, 2, 3]))  # [2, 4, 6]
print(process("hello"))    # HELLO
```

---

## Choosing the Right Tool

| Need | Tool | Example |
|------|------|---------|
| Fix some arguments | `partial` | `square = partial(pow, exp=2)` |
| Cache function results | `lru_cache` / `cache` | Recursive DP, expensive queries |
| Write a decorator | `wraps` | Logging, timing, retry decorators |
| Fold sequence to value | `reduce` | Product, flatten, compose |
| Auto-generate comparisons | `total_ordering` | Custom sortable classes |
| Dispatch by type | `singledispatch` | Format different data types |
| Cache a property | `cached_property` | Expensive computed attributes |

---

## Section Map

Each function has a dedicated page with detailed coverage:

- **functools.cache** — unbounded memoization for recursive algorithms
- **functools.lru_cache** — bounded memoization with LRU eviction
- **functools.partial** — partial function application
- **functools.reduce** — cumulative fold operations
- **functools.wraps** — metadata preservation for decorators
- **functools.total_ordering** — auto-generate comparison methods
- **functools.singledispatch** — single-argument type dispatch

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Module purpose | Higher-order functions and callable transformations |
| Most used | `wraps`, `lru_cache`, `partial` |
| Caching | `cache` (unbounded) vs `lru_cache` (bounded) |
| Decorators | Always use `@wraps(func)` |
| Folding | `reduce` works but prefer built-ins when available |
| Dispatch | `singledispatch` avoids if/elif type chains |

**Key Takeaways**:

- `functools` is the Swiss army knife for functional programming in Python
- `wraps` and `lru_cache` are used daily in production code
- `partial` creates cleaner specialized functions than lambdas
- `reduce` is powerful but often less readable than built-in alternatives
- `total_ordering` and `singledispatch` reduce boilerplate in OOP code

---

## Exercises

**Exercise 1.**
Write a decorator using `functools.wraps` that logs the name and arguments of any function call to a list called `log`. Apply it to two different functions, call each once, and print the log.

??? success "Solution to Exercise 1"

        from functools import wraps

        log = []

        def logger(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                log.append(f"{func.__name__}({args}, {kwargs})")
                return func(*args, **kwargs)
            return wrapper

        @logger
        def add(a, b):
            return a + b

        @logger
        def greet(name):
            return f"Hello, {name}"

        add(3, 4)
        greet("Alice")
        print(log)
        # ["add((3, 4), {})", "greet(('Alice',), {})"]

---

**Exercise 2.**
Use `functools.partial` to create a `json_dumps_pretty` function from `json.dumps` that always uses `indent=2` and `sort_keys=True`. Demonstrate by serializing a dictionary with nested data.

??? success "Solution to Exercise 2"

        import json
        from functools import partial

        json_dumps_pretty = partial(json.dumps, indent=2, sort_keys=True)

        data = {"name": "Alice", "scores": [95, 87, 91], "active": True}
        print(json_dumps_pretty(data))

---

**Exercise 3.**
Combine three `functools` features in one example: use `@lru_cache` to memoize a recursive function, `functools.reduce` to aggregate results, and `functools.partial` to create a specialized version of the aggregation. Specifically, memoize a `fibonacci(n)` function, then use `reduce` with `operator.add` to sum the first 20 Fibonacci numbers, and use `partial` to create a `sum_fibs` function that always sums a fixed range.

??? success "Solution to Exercise 3"

        from functools import lru_cache, partial, reduce
        import operator

        @lru_cache(maxsize=None)
        def fibonacci(n):
            if n < 2:
                return n
            return fibonacci(n - 1) + fibonacci(n - 2)

        # Sum first 20 Fibonacci numbers using reduce
        fibs = [fibonacci(i) for i in range(20)]
        total = reduce(operator.add, fibs)
        print(f"Sum of first 20 fibs: {total}")  # 10945

        # Create a reusable partial for summing any list
        sum_list = partial(reduce, operator.add)
        print(sum_list(fibs))  # 10945
