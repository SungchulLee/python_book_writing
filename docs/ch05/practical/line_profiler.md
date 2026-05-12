# line_profiler

The `line_profiler` tool profiles code at the line level, showing exactly which lines consume the most time. It requires installation via pip.

!!! tip "Mental Model"
    While `cProfile` tells you which function is slow, `line_profiler` tells you which line inside that function is slow. It is the microscope you reach for after the telescope has pointed you to the right function. Decorate the suspect function with `@profile`, run with `kernprof`, and read the per-line time percentages.

---

## Installation and Setup

```bash
pip install line_profiler
```

## Using line_profiler

Mark functions with `@profile` decorator and run with `kernprof`:

```python
# example.py
@profile
def process_data(n):
    result = 0
    for i in range(n):
        result += i ** 2  # Expensive operation
    
    total = sum(range(n))  # Another loop
    return result, total

if __name__ == "__main__":
    process_data(10000)
```

Run with profiler:
```
kernprof -l -v example.py
```

## Output Interpretation

```
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     1                                           @profile
     2                                           def process_data(n):
     3         1            2      2.0      0.0      result = 0
     4     10001          456     0.0      5.2      for i in range(n):
     5     10000         8234     0.8     94.2          result += i ** 2
     6         1          122    122.0      1.4      total = sum(range(n))
     7         1            1      1.0      0.0      return result, total
```

## Advanced Features

```python
# Profiling without @profile decorator
from line_profiler import LineProfiler

def expensive_function():
    data = []
    for i in range(100):
        data.append(i ** 2)
    return data

profiler = LineProfiler()
profiler.add_function(expensive_function)
profiler.enable()
expensive_function()
profiler.disable()
profiler.print_stats()
```

## Combining with cProfile

For a complete picture, use both tools:

- **cProfile** identifies which functions are slow
- **line_profiler** identifies which lines within those functions are slow

---

## Exercises

**Exercise 1.**
Write a function `process_data(n)` that (a) creates a list of n random floats, (b) sorts the list, (c) computes the sum, and (d) finds the median by indexing. Use `LineProfiler` programmatically (without the `@profile` decorator) to profile it, print the stats, and identify which line takes the most time.

??? success "Solution to Exercise 1"
        ```python
        from line_profiler import LineProfiler
        import random

        def process_data(n):
            data = [random.random() for _ in range(n)]
            data.sort()
            total = sum(data)
            median = data[n // 2]
            return total, median

        profiler = LineProfiler()
        profiler.add_function(process_data)
        profiler.enable()
        process_data(500_000)
        profiler.disable()
        profiler.print_stats()
        ```

---

**Exercise 2.**
Create two versions of a function that counts word frequencies in a large string: one using a manual dictionary loop and one using `collections.Counter`. Profile both with `LineProfiler` and compare which lines are hotspots in each version.

??? success "Solution to Exercise 2"
        ```python
        from line_profiler import LineProfiler
        from collections import Counter

        text = " ".join(["word"] * 100_000 + ["hello"] * 50_000)

        def count_manual(text):
            freq = {}
            for word in text.split():
                if word in freq:
                    freq[word] += 1
                else:
                    freq[word] = 1
            return freq

        def count_counter(text):
            return Counter(text.split())

        for func in [count_manual, count_counter]:
            lp = LineProfiler()
            lp.add_function(func)
            lp.enable()
            func(text)
            lp.disable()
            lp.print_stats()
        ```

---

**Exercise 3.**
Write a matrix multiplication function `matmul(A, B)` using nested loops. Profile it with `LineProfiler` on two 100x100 matrices. Identify the innermost loop line and compute what percentage of total time it consumes.

??? success "Solution to Exercise 3"
        ```python
        from line_profiler import LineProfiler

        def matmul(A, B):
            n = len(A)
            m = len(B[0])
            k = len(B)
            C = [[0] * m for _ in range(n)]
            for i in range(n):
                for j in range(m):
                    total = 0
                    for p in range(k):
                        total += A[i][p] * B[p][j]
                    C[i][j] = total
            return C

        import random
        n = 100
        A = [[random.random() for _ in range(n)] for _ in range(n)]
        B = [[random.random() for _ in range(n)] for _ in range(n)]

        lp = LineProfiler()
        lp.add_function(matmul)
        lp.enable()
        matmul(A, B)
        lp.disable()
        lp.print_stats()
        ```
