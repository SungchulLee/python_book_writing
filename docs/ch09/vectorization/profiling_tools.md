# Profiling Tools

Empirical performance analysis guides optimization efforts.

!!! tip "Mental Model"
    Never guess where the bottleneck is -- measure it. `%timeit` gives quick micro-benchmarks in Jupyter, `cProfile` identifies which functions consume the most time, and `line_profiler` pinpoints the expensive lines within a function. Profile first, then optimize only the hot path.

    Profiling is the **decision engine** of the [optimization hierarchy](vectorization_basics.md):
    it tells you *which* level of the hierarchy to apply and *where*. Without
    measurement, you risk optimizing code that is not the bottleneck — or worse,
    making it slower through premature complexity. The workflow is always:
    **profile → identify hot path → apply the highest applicable optimization → re-profile.**


## IPython %timeit

Quick timing in interactive environments.

### 1. Basic Usage

```python
%timeit arr ** 2
```

Output:

```
1.23 µs ± 45.2 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
```

### 2. Multi-line Timing

```python
%%timeit
result = np.zeros(1000)
for i in range(1000):
    result[i] = i ** 2
```

### 3. Control Runs

```python
%timeit -n 100 -r 5 arr ** 2  # 100 loops, 5 runs
```


## timeit Module

Scripted benchmarks outside IPython.

### 1. Basic Script

```python
import timeit
import numpy as np

def main():
    setup = "import numpy as np; arr = np.random.randn(10000)"
    stmt = "arr ** 2"
    
    time = timeit.timeit(stmt, setup, number=1000)
    print(f"Total time: {time:.4f} sec")
    print(f"Per call:   {time/1000*1000:.4f} ms")

if __name__ == "__main__":
    main()
```

### 2. Compare Functions

```python
import timeit
import numpy as np

def method_loop(arr):
    result = np.empty_like(arr)
    for i in range(len(arr)):
        result[i] = arr[i] ** 2
    return result

def method_vectorized(arr):
    return arr ** 2

def main():
    arr = np.random.randn(10000)
    
    loop_time = timeit.timeit(
        lambda: method_loop(arr), number=100
    )
    vec_time = timeit.timeit(
        lambda: method_vectorized(arr), number=100
    )
    
    print(f"Loop time:       {loop_time:.4f} sec")
    print(f"Vectorized time: {vec_time:.4f} sec")
    print(f"Speedup:         {loop_time/vec_time:.0f}x")

if __name__ == "__main__":
    main()
```


## time.perf_counter

Manual timing with high precision.

### 1. Basic Pattern

```python
import time
import numpy as np

def main():
    arr = np.random.randn(1_000_000)
    
    start = time.perf_counter()
    result = arr ** 2
    elapsed = time.perf_counter() - start
    
    print(f"Elapsed: {elapsed:.6f} sec")

if __name__ == "__main__":
    main()
```

### 2. Multiple Runs

```python
import time
import numpy as np

def main():
    arr = np.random.randn(1_000_000)
    times = []
    
    for _ in range(10):
        start = time.perf_counter()
        result = arr ** 2
        times.append(time.perf_counter() - start)
    
    print(f"Mean: {np.mean(times):.6f} sec")
    print(f"Std:  {np.std(times):.6f} sec")

if __name__ == "__main__":
    main()
```


## cProfile Module

Function-level profiling for entire programs.

### 1. Command Line

```bash
python -m cProfile -s cumtime my_script.py
```

### 2. In Script

```python
import cProfile
import numpy as np

def my_function():
    arr = np.random.randn(100000)
    for _ in range(100):
        result = arr ** 2

cProfile.run('my_function()')
```

### 3. Output Example

```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      100    0.050    0.001    0.050    0.001 {method 'random' ...}
      100    0.030    0.000    0.030    0.000 {built-in method numpy...}
```


## line_profiler

Line-by-line timing for detailed analysis.

### 1. Installation

```bash
pip install line_profiler
```

### 2. Decorator Usage

```python
@profile
def my_function():
    arr = np.random.randn(100000)  # Line 1
    result = arr ** 2               # Line 2
    total = np.sum(result)          # Line 3
    return total
```

### 3. Run Command

```bash
kernprof -l -v my_script.py
```


## memory_profiler

Track memory usage during execution.

### 1. Installation

```bash
pip install memory_profiler
```

### 2. Usage

```python
from memory_profiler import profile

@profile
def my_function():
    arr = np.random.randn(1_000_000)
    result = arr ** 2
    return result
```

### 3. Output Example

```
Line #    Mem usage    Increment  Line Contents
     3     50.0 MiB     50.0 MiB   arr = np.random.randn(1_000_000)
     4     57.6 MiB      7.6 MiB   result = arr ** 2
```


## Best Practices

Guidelines for effective profiling.

### 1. Profile First

Identify bottlenecks before optimizing.

### 2. Representative Data

Use realistic data sizes for meaningful results.

### 3. Multiple Runs

Average over multiple runs to reduce variance.

---

## Exercises

**Exercise 1.** Write a vectorized NumPy solution and a pure Python loop solution for the same computation. Measure and compare their performance using `time.perf_counter()`.

??? success "Solution to Exercise 1"
    ```python
    import numpy as np
    import time

    n = 1_000_000
    data = np.random.default_rng(42).random(n)

    # Python loop
    start = time.perf_counter()
    result_py = [x ** 2 for x in data]
    py_time = time.perf_counter() - start

    # NumPy vectorized
    start = time.perf_counter()
    result_np = data ** 2
    np_time = time.perf_counter() - start

    print(f"Python: {py_time:.4f}s, NumPy: {np_time:.6f}s")
    print(f"Speedup: {py_time / np_time:.0f}x")
    ```

---

**Exercise 2.** Identify a potential performance pitfall in the following code and rewrite it using NumPy vectorization:

```python
result = []
for i in range(len(data)):
    result.append(data[i] ** 2 + 2 * data[i] + 1)
```

??? success "Solution to Exercise 2"
    ```python
    import numpy as np

    data = np.random.default_rng(42).random(100000)

    # Vectorized (fast)
    result = data ** 2 + 2 * data + 1
    ```

    The loop version creates Python objects for each element and calls `append` repeatedly. The vectorized version computes everything in compiled C code on contiguous memory.

---

**Exercise 3.** Explain why NumPy vectorized operations are faster than Python loops. Reference memory layout, type checking overhead, and SIMD instructions in your answer.

??? success "Solution to Exercise 3"
    NumPy vectorized operations are faster because:

    1. **Contiguous memory**: NumPy arrays store elements in a contiguous block, enabling efficient CPU cache usage.
    2. **No type checking**: Python loops check types at each iteration; NumPy knows the dtype in advance.
    3. **Compiled C loops**: The actual computation runs in compiled C/Fortran code, not interpreted Python.
    4. **SIMD instructions**: Modern CPUs can process multiple array elements simultaneously using SIMD (Single Instruction, Multiple Data).

---

**Exercise 4.** Apply the concepts from this page to a practical problem: given a large array of temperatures in Celsius, convert them all to Fahrenheit and find the maximum. Compare vectorized and loop approaches.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    import time

    rng = np.random.default_rng(42)
    celsius = rng.uniform(-40, 50, 1_000_000)

    # Vectorized
    start = time.perf_counter()
    fahrenheit = celsius * 9/5 + 32
    max_f = fahrenheit.max()
    vec_time = time.perf_counter() - start

    # Loop
    start = time.perf_counter()
    max_f_loop = max(c * 9/5 + 32 for c in celsius)
    loop_time = time.perf_counter() - start

    print(f"Vectorized: {vec_time:.6f}s, max={max_f:.1f}F")
    print(f"Loop: {loop_time:.4f}s, max={max_f_loop:.1f}F")
    ```
