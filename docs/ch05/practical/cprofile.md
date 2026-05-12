# cProfile Module

Python's built-in `cProfile` module provides a deterministic profiler that measures CPU time spent in each function. It's essential for identifying performance bottlenecks in your code.

!!! tip "Mental Model"
    `cProfile` is like a stopwatch for every function call in your program. It records how many times each function was called and how long it took, then ranks them. The key insight is to sort by cumulative time to find the real bottlenecks -- the functions where your program actually spends its life.

---

## Basic Usage

The `cProfile` module offers several ways to profile code: command-line usage, direct module calls, or context managers.

### Command-line Profiling

```python
# example_module.py
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def main():
    result = fibonacci(30)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
```

Run with profiling:
```
python -m cProfile -s cumulative example_module.py
```

### Programmatic Profiling

```python
import cProfile
import pstats
from io import StringIO

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Create profiler and run code
profiler = cProfile.Profile()
profiler.enable()

result = fibonacci(30)

profiler.disable()

# Print statistics
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 functions
```

## Interpreting Results

cProfile output shows:

- **ncalls**: Number of calls to the function
- **tottime**: Total time spent in the function (excluding subfunctions)
- **cumtime**: Cumulative time (including called functions)
- **filename:lineno(function)**: Where the function is defined

```
   ncalls  tottime  cumtime      filename:lineno(function)
   832039    0.156    0.321 example.py:1(fibonacci)
        1    0.000    0.320 example.py:6(main)
```

## Saving and Loading Profiling Data

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here
for i in range(1000):
    sum([i**2 for i in range(100)])

profiler.disable()

# Save to file
profiler.dump_stats('profile_data.prof')

# Load and analyze later
stats = pstats.Stats('profile_data.prof')
stats.sort_stats('cumulative')
stats.print_stats(5)
```

## Performance Tips

- Use `sort_stats()` with 'cumulative' for wall-clock time analysis
- Filter results with `print_stats(10)` to see top functions
- Compare profiles before and after optimizations
- Profile on realistic data to get accurate measurements

---


## Runnable Example: `cprofile_tutorial.py`

```python
"""
PYTHON CODE PROFILING & OPTIMIZATION - INTERMEDIATE LEVEL
==========================================================
Module 5: cProfile Basics - Function-Level Profiling

LEARNING OBJECTIVES:
- Master cProfile for function-level profiling
- Understand profiling output metrics
- Learn to identify performance bottlenecks
- Profile scripts and functions
- Interpret profiling data effectively

Author: Python Course Development Team
Date: 2024
"""

import cProfile
import pstats
from io import StringIO


# =============================================================================
# Definitions
# =============================================================================

def fibonacci_recursive(n):
    """Inefficient recursive Fibonacci"""
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)


def fibonacci_iterative(n):
    """Efficient iterative Fibonacci"""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def demonstrate_basic_profiling():
    """Basic cProfile usage"""
    print("=" * 70)
    print("BASIC CPROFILE USAGE")
    print("=" * 70)
    
    print("\nProfiling recursive Fibonacci(20):\n")
    
    # Profile using cProfile.run()
    cProfile.run('fibonacci_recursive(20)')


def profile_with_stats():
    """Profile and analyze with pstats"""
    print("\n" + "=" * 70)
    print("PROFILING WITH PSTATS")
    print("=" * 70)
    
    # Create profiler
    profiler = cProfile.Profile()
    
    # Profile the code
    profiler.enable()
    result = fibonacci_recursive(25)
    profiler.disable()
    
    # Analyze results
    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats('cumulative')
    
    print(f"\nFibonacci(25) = {result}\n")
    print("Top 10 functions by cumulative time:")
    stats.print_stats(10)


def compare_implementations():
    """Compare recursive vs iterative"""
    print("\n" + "=" * 70)
    print("COMPARING IMPLEMENTATIONS")
    print("=" * 70)
    
    n = 30
    
    print(f"\n1. Recursive Fibonacci({n}):")
    profiler1 = cProfile.Profile()
    profiler1.enable()
    result1 = fibonacci_recursive(n)
    profiler1.disable()
    
    stats1 = pstats.Stats(profiler1)
    print(f"   Result: {result1}")
    print(f"   Total calls: {stats1.total_calls:,}")
    
    print(f"\n2. Iterative Fibonacci({n}):")
    profiler2 = cProfile.Profile()
    profiler2.enable()
    result2 = fibonacci_iterative(n)
    profiler2.disable()
    
    stats2 = pstats.Stats(profiler2)
    print(f"   Result: {result2}")
    print(f"   Total calls: {stats2.total_calls:,}")
    
    print(f"\nRecursive made {stats1.total_calls:,} function calls!")
    print(f"Iterative made {stats2.total_calls:,} function calls!")


def main():
    """Run all demonstrations"""
    print("\n" + "=" * 70)
    print("CPROFILE BASICS - COMPREHENSIVE TUTORIAL")
    print("=" * 70 + "\n")
    
    demonstrate_basic_profiling()
    profile_with_stats()
    compare_implementations()
    
    print("\n" + "=" * 70)
    print("KEY METRICS IN CPROFILE OUTPUT")
    print("=" * 70)
    print("""
    ncalls:    Number of calls to the function
    tottime:   Total time spent in function (excluding subcalls)
    percall:   tottime / ncalls
    cumtime:   Cumulative time (including subcalls)
    percall:   cumtime / ncalls
    filename:lineno(function)
    
    Key Insights:
    - High cumtime: Function takes significant total time
    - High tottime: Function itself is slow (not subcalls)
    - High ncalls: Function is called very frequently
    - Focus optimization on high cumtime AND high tottime
    """)

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    main()
```


## Exercises

**Exercise 1.**
Write a function `slow_sum(n)` that computes the sum of squares by calling a helper function `square(x)` for each number. Profile it with `cProfile.Profile()`, sort results by `cumulative` time, and print the top 5 entries. Identify which function has the most calls.

??? success "Solution to Exercise 1"
        ```python
        import cProfile
        import pstats

        def square(x):
            return x * x

        def slow_sum(n):
            total = 0
            for i in range(n):
                total += square(i)
            return total

        profiler = cProfile.Profile()
        profiler.enable()
        slow_sum(100_000)
        profiler.disable()

        stats = pstats.Stats(profiler)
        stats.strip_dirs()
        stats.sort_stats('cumulative')
        stats.print_stats(5)
        ```

---

**Exercise 2.**
Use `cProfile` to profile two implementations of finding the n-th Fibonacci number: one recursive (without memoization) and one using `functools.lru_cache`. Compare the total number of function calls reported by each profile and print the ratio.

??? success "Solution to Exercise 2"
        ```python
        import cProfile
        import pstats
        from functools import lru_cache

        def fib_recursive(n):
            if n <= 1:
                return n
            return fib_recursive(n - 1) + fib_recursive(n - 2)

        @lru_cache(maxsize=None)
        def fib_cached(n):
            if n <= 1:
                return n
            return fib_cached(n - 1) + fib_cached(n - 2)

        p1 = cProfile.Profile()
        p1.enable()
        fib_recursive(30)
        p1.disable()
        s1 = pstats.Stats(p1)

        p2 = cProfile.Profile()
        p2.enable()
        fib_cached(30)
        p2.disable()
        s2 = pstats.Stats(p2)

        print(f"Recursive calls: {s1.total_calls:,}")
        print(f"Cached calls:    {s2.total_calls:,}")
        print(f"Ratio: {s1.total_calls / s2.total_calls:.0f}x")
        ```

---

**Exercise 3.**
Write a profiling context manager `class Profiler` that starts a `cProfile.Profile` on `__enter__` and on `__exit__` prints a summary of the top 10 functions sorted by total time. Use it to profile a block of code that sorts 10 random lists of 100,000 elements each.

??? success "Solution to Exercise 3"
        ```python
        import cProfile
        import pstats
        import random

        class Profiler:
            def __enter__(self):
                self._profiler = cProfile.Profile()
                self._profiler.enable()
                return self

            def __exit__(self, *args):
                self._profiler.disable()
                stats = pstats.Stats(self._profiler)
                stats.strip_dirs()
                stats.sort_stats('tottime')
                stats.print_stats(10)

        with Profiler():
            for _ in range(10):
                data = [random.random() for _ in range(100_000)]
                data.sort()
        ```

---
