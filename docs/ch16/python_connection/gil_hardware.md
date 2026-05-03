# GIL and Hardware

!!! tip "Mental Model"
    The GIL is a single key to the Python interpreter room -- only one thread can hold it at a time. This means your 8-core CPU sits mostly idle when running multi-threaded Python code. The workaround is simple: use threads for I/O waits (the key is released during I/O), and use separate processes for CPU-bound work (each gets its own key).

## What is the GIL?

The **Global Interpreter Lock (GIL)** is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecode simultaneously.

```
Without GIL (hypothetical):
┌────────────────────────────────────────────────────────────┐
│ Thread 1: refcount++    Thread 2: refcount++              │
│                                                            │
│ Both read refcount = 1                                     │
│ Both compute 1 + 1 = 2                                     │
│ Both write refcount = 2                                    │
│                                                            │
│ Expected: 3, Got: 2 → Memory corruption!                  │
└────────────────────────────────────────────────────────────┘

With GIL:
┌────────────────────────────────────────────────────────────┐
│ Thread 1: [acquire GIL][refcount++][release GIL]          │
│ Thread 2:              [wait........][acquire GIL][ref++] │
│                                                            │
│ Operations are serialized → Safe, but not parallel         │
└────────────────────────────────────────────────────────────┘
```

## GIL and Multi-Core CPUs

Modern CPUs have multiple cores, but Python can only use one at a time for Python code:

```
8-Core CPU with Python Threads:

Core 0: [Python][Python][Python][Python][Python]  ← All Python here
Core 1: [idle ][idle ][idle ][idle ][idle ]
Core 2: [idle ][idle ][idle ][idle ][idle ]
Core 3: [idle ][idle ][idle ][idle ][idle ]
Core 4: [idle ][idle ][idle ][idle ][idle ]
Core 5: [idle ][idle ][idle ][idle ][idle ]
Core 6: [idle ][idle ][idle ][idle ][idle ]
Core 7: [idle ][idle ][idle ][idle ][idle ]

7 cores sitting idle despite multiple threads!
```

## Demonstrating the GIL

```python
import threading
import time

def cpu_bound_task(n):
    """CPU-intensive: count to n."""
    count = 0
    for _ in range(n):
        count += 1
    return count

n = 50_000_000

# Single-threaded
start = time.perf_counter()
cpu_bound_task(n)
single_time = time.perf_counter() - start
print(f"Single thread: {single_time:.2f}s")

# Two threads (should be 2x faster, right?)
start = time.perf_counter()
t1 = threading.Thread(target=cpu_bound_task, args=(n//2,))
t2 = threading.Thread(target=cpu_bound_task, args=(n//2,))
t1.start()
t2.start()
t1.join()
t2.join()
two_thread_time = time.perf_counter() - start
print(f"Two threads:   {two_thread_time:.2f}s")

print(f"Speedup: {single_time/two_thread_time:.2f}x")
```

Typical output:
```
Single thread: 2.50s
Two threads:   2.80s  ← Actually SLOWER!
Speedup: 0.89x
```

Two threads are slower due to GIL contention overhead!

## When the GIL is Released

The GIL is released during:

### 1. I/O Operations

```python
import threading
import time
import urllib.request

def download(url):
    """I/O bound: downloads URL."""
    urllib.request.urlopen(url).read()

urls = ['http://example.com'] * 4

# Sequential
start = time.perf_counter()
for url in urls:
    download(url)
sequential_time = time.perf_counter() - start

# Parallel (GIL released during network I/O)
start = time.perf_counter()
threads = [threading.Thread(target=download, args=(url,)) for url in urls]
for t in threads:
    t.start()
for t in threads:
    t.join()
parallel_time = time.perf_counter() - start

print(f"Sequential: {sequential_time:.2f}s")
print(f"Parallel:   {parallel_time:.2f}s")
print(f"Speedup:    {sequential_time/parallel_time:.2f}x")
```

```
Sequential: 2.00s
Parallel:   0.55s
Speedup:    3.64x  ← Threading works for I/O!
```

### 2. NumPy Operations

```python
import numpy as np
import threading
import time

def numpy_operation(arr):
    """NumPy releases GIL during computation."""
    for _ in range(100):
        np.dot(arr, arr)

arr = np.random.rand(1000, 1000)

# NumPy operations CAN run in parallel
# because NumPy releases the GIL
```

### 3. C Extensions That Release GIL

```c
// C extension code
Py_BEGIN_ALLOW_THREADS
// ... long computation without Python objects ...
Py_END_ALLOW_THREADS
```

## Working Around the GIL

### Solution 1: Multiprocessing

Use separate processes instead of threads:

```python
from multiprocessing import Pool
import time

def cpu_bound_task(n):
    count = 0
    for _ in range(n):
        count += 1
    return count

n = 50_000_000

# Single process
start = time.perf_counter()
cpu_bound_task(n)
single_time = time.perf_counter() - start

# Multiple processes (no GIL issue!)
start = time.perf_counter()
with Pool(4) as pool:
    pool.map(cpu_bound_task, [n//4] * 4)
multi_time = time.perf_counter() - start

print(f"Single process:    {single_time:.2f}s")
print(f"Four processes:    {multi_time:.2f}s")
print(f"Speedup:           {single_time/multi_time:.2f}x")
```

```
Single process:    2.50s
Four processes:    0.70s
Speedup:           3.57x  ← Real parallelism!
```

```
Multiprocessing vs Threading:

Threading:
┌──────────┐
│ Process  │
│ ┌──────┐ │   GIL
│ │Thread│◀┼───────────────────────▶ Only one runs Python
│ │Thread│ │
│ │Thread│ │
│ └──────┘ │
└──────────┘

Multiprocessing:
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Process  │ │ Process  │ │ Process  │
│ ┌──────┐ │ │ ┌──────┐ │ │ ┌──────┐ │
│ │ GIL  │ │ │ │ GIL  │ │ │ │ GIL  │ │  Each has own GIL
│ └──────┘ │ │ └──────┘ │ │ └──────┘ │
└──────────┘ └──────────┘ └──────────┘
     ▲             ▲             ▲
     └─────────────┼─────────────┘
              True parallelism!
```

### Solution 2: Use NumPy/SciPy

```python
import numpy as np
import time

n = 10_000_000

# Pure Python (GIL-bound)
data = list(range(n))
start = time.perf_counter()
result = sum(x**2 for x in data)
python_time = time.perf_counter() - start

# NumPy (releases GIL, uses SIMD)
arr = np.arange(n)
start = time.perf_counter()
result = np.sum(arr**2)
numpy_time = time.perf_counter() - start

print(f"Python: {python_time:.2f}s")
print(f"NumPy:  {numpy_time:.3f}s")
print(f"Speedup: {python_time/numpy_time:.0f}x")
```

### Solution 3: Numba with `nogil`

```python
from numba import jit, prange
import numpy as np
import time

@jit(nopython=True, parallel=True)
def parallel_sum_squares(arr):
    """Numba can release GIL and parallelize."""
    total = 0.0
    for i in prange(len(arr)):  # prange = parallel range
        total += arr[i] ** 2
    return total

arr = np.random.rand(10_000_000)

# Warm up JIT
parallel_sum_squares(arr)

# Benchmark
start = time.perf_counter()
result = parallel_sum_squares(arr)
elapsed = time.perf_counter() - start

print(f"Time: {elapsed:.4f}s")
```

## GIL and Hardware Utilization

```
Task Type           Threading    Multiprocessing    NumPy
────────────────────────────────────────────────────────────
CPU-bound Python    ✗ No gain    ✓ Full parallel    N/A
CPU-bound NumPy     ✓ Can help   ✓ Full parallel    ✓ Built-in
I/O-bound           ✓ Works      ✓ Works            N/A
Memory-bound        ✗ Limited    ✗ Limited          ✓ Optimized
```

## The Future: Free-threaded Python

Python 3.13+ introduces experimental GIL-free mode:

```bash
# Build Python with --disable-gil (experimental)
# Or use the free-threaded build
python3.13t script.py  # 't' suffix = free-threaded
```

```python
# In free-threaded Python, true parallelism is possible
import threading

# This will actually use multiple cores!
threads = [threading.Thread(target=cpu_task) for _ in range(4)]
```

## Summary

| Scenario | GIL Impact | Solution |
|----------|------------|----------|
| CPU-bound Python | Serialized | multiprocessing |
| I/O-bound | Released during I/O | threading works |
| NumPy computation | Released | threading can help |
| C extensions | Can release | depends on extension |

Key points:

- GIL prevents true threading parallelism for Python code
- GIL is released during I/O and many C extensions
- Use `multiprocessing` for CPU-bound parallelism
- Use `threading` for I/O-bound concurrency
- NumPy releases GIL, enabling parallel computation
- Free-threaded Python (3.13+) removes GIL (experimental)

```
Decision Tree:

Is your code CPU-bound?
├── Yes: Pure Python?
│   ├── Yes → Use multiprocessing
│   └── No (NumPy) → Threading may help, NumPy parallelizes internally
└── No (I/O-bound) → Use threading or asyncio
```


---

## Exercises

**Exercise 1.** Explain what the Global Interpreter Lock (GIL) is in CPython. How does it affect multi-threaded Python programs?

??? success "Solution to Exercise 1"
    ```python
    # Conceptual solution - see page content for details
    import sys
    import platform

    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
    ```

---

**Exercise 2.** Write Python code that demonstrates the GIL limitation: create two threads that each increment a counter 10 million times. Compare the runtime with a single-threaded version.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the hardware-software interaction and how it affects Python performance.

---

**Exercise 3.** Explain why the GIL does not affect I/O-bound programs. Write code showing that threads can speed up I/O-bound tasks.

??? success "Solution to Exercise 3"
    ```python
    import time

    # Simple benchmark
    n = 10_000_000
    start = time.perf_counter()
    total = sum(range(n))
    elapsed = time.perf_counter() - start
    print(f"Sum of {n} integers: {total}")
    print(f"Time: {elapsed:.4f} seconds")
    ```

---

**Exercise 4.** Describe three strategies to work around the GIL for CPU-bound tasks (multiprocessing, C extensions, subinterpreters).

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    import time

    n = 1_000_000
    # Python loop
    start = time.perf_counter()
    result_py = sum(i * i for i in range(n))
    time_py = time.perf_counter() - start

    # NumPy vectorized
    arr = np.arange(n)
    start = time.perf_counter()
    result_np = np.sum(arr * arr)
    time_np = time.perf_counter() - start

    print(f"Python: {time_py:.4f}s, NumPy: {time_np:.4f}s")
    print(f"Speedup: {time_py / time_np:.1f}x")
    ```
