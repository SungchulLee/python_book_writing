# memory_profiler

The `memory_profiler` module tracks memory usage at the line level, helping identify memory leaks and inefficient memory access patterns.

!!! tip "Mental Model"
    `memory_profiler` does for memory what `line_profiler` does for time -- it shows you the memory increment of each line. Decorate a function with `@profile`, run the script, and you get a line-by-line ledger of memory consumption. Look for lines with large positive increments to find your biggest memory consumers.

---

## Installation

```bash
pip install memory_profiler
```

## Basic Usage

```python
# memory_example.py
from memory_profiler import profile

@profile
def create_list():
    large_list = [i ** 2 for i in range(100000)]
    filtered = [x for x in large_list if x % 2 == 0]
    return filtered

if __name__ == "__main__":
    result = create_list()
```

Run with:
```
python -m memory_profiler memory_example.py
```

## Output Format

```
Filename: memory_example.py

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
     3   38.4 MiB      0.0 MiB           1   @profile
     4                                        def create_list():
     5   42.8 MiB      4.4 MiB           1       large_list = [i ** 2 for i in range(100000)]
     6   43.2 MiB      0.4 MiB           1       filtered = [x for x in large_list if x % 2 == 0]
     7                                        return filtered
```

## Programmatic Memory Profiling

```python
from memory_profiler import profile

def process_arrays():
    # This will be tracked
    arr1 = list(range(1000000))
    arr2 = [x ** 2 for x in arr1]
    del arr1  # Memory freed
    return arr2

# Get memory without decorator
from memory_profiler import show_results

profile(process_arrays)()
```

## Memory Optimization Patterns

```python
# Inefficient: creates multiple intermediate lists
def inefficient():
    data = [i for i in range(100000)]
    filtered = [x for x in data if x > 50000]
    squared = [x ** 2 for x in filtered]
    return squared

# Efficient: single pass generator
def efficient():
    return (x ** 2 for x in range(100000) if x > 50000)
```

## Practical Tips

- Use generators instead of list comprehensions for large datasets
- Delete large objects explicitly when done: `del large_obj`
- Profile before and after optimization
- Monitor peak memory usage, not just line-by-line

---

## Exercises

**Exercise 1.**
Write two versions of a function that reads a range of 1,000,000 integers and returns only the even squares: one using list comprehensions (creating intermediate lists) and one using a single generator expression. Use `tracemalloc` to compare peak memory for each approach.

??? success "Solution to Exercise 1"
        ```python
        import tracemalloc

        def with_lists():
            nums = list(range(1_000_000))
            evens = [x for x in nums if x % 2 == 0]
            squares = [x ** 2 for x in evens]
            return squares

        def with_generator():
            return list(
                x ** 2 for x in range(1_000_000) if x % 2 == 0
            )

        tracemalloc.start()
        with_lists()
        _, peak_lists = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tracemalloc.start()
        with_generator()
        _, peak_gen = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"List approach peak:      {peak_lists / 1024 / 1024:.1f} MB")
        print(f"Generator approach peak: {peak_gen / 1024 / 1024:.1f} MB")
        ```

---

**Exercise 2.**
Write a function that builds a dictionary of 100,000 entries, then deletes it with `del` and calls `gc.collect()`. Use `tracemalloc` snapshots before creation, after creation, and after deletion to show the memory growth and reclamation.

??? success "Solution to Exercise 2"
        ```python
        import tracemalloc
        import gc

        tracemalloc.start()
        snap1 = tracemalloc.take_snapshot()

        d = {f"key_{i}": list(range(10)) for i in range(100_000)}
        snap2 = tracemalloc.take_snapshot()

        del d
        gc.collect()
        snap3 = tracemalloc.take_snapshot()

        growth = snap2.compare_to(snap1, 'lineno')
        reclaim = snap3.compare_to(snap2, 'lineno')

        total_growth = sum(s.size_diff for s in growth if s.size_diff > 0)
        total_freed = sum(s.size_diff for s in reclaim if s.size_diff < 0)

        print(f"Growth:     +{total_growth / 1024 / 1024:.1f} MB")
        print(f"Reclaimed:  {total_freed / 1024 / 1024:.1f} MB")
        tracemalloc.stop()
        ```

---

**Exercise 3.**
Create a function `memory_report(func, *args)` that wraps any callable with `tracemalloc`, runs it, and returns a dictionary with keys `current_kb`, `peak_kb`, and `top_allocations` (a list of the top 3 allocation lines). Test it with a function that creates a nested list of 1,000 sublists with 1,000 elements each.

??? success "Solution to Exercise 3"
        ```python
        import tracemalloc

        def memory_report(func, *args):
            tracemalloc.start()
            func(*args)
            current, peak = tracemalloc.get_traced_memory()
            snapshot = tracemalloc.take_snapshot()
            top = snapshot.statistics('lineno')[:3]
            tracemalloc.stop()
            return {
                "current_kb": current / 1024,
                "peak_kb": peak / 1024,
                "top_allocations": [str(s) for s in top],
            }

        def build_nested():
            return [[i * j for j in range(1_000)]
                    for i in range(1_000)]

        report = memory_report(build_nested)
        print(f"Current: {report['current_kb']:.1f} KB")
        print(f"Peak:    {report['peak_kb']:.1f} KB")
        print("Top allocations:")
        for entry in report["top_allocations"]:
            print(f"  {entry}")
        ```
