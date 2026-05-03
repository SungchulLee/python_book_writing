# Introduction to Concurrency

Concurrency is about dealing with multiple things at once. This chapter covers Python's tools for concurrent and parallel execution.

!!! tip "Mental Model"
    Concurrency means structuring a program to handle multiple tasks that overlap in time. Parallelism means actually executing them at the same instant on different cores. Python gives you both: threads and asyncio for concurrency (interleaving work), and processes for true parallelism (simultaneous computation).

---

## Why Concurrency?

### The Problem: Sequential Execution

```python
import time

def download_file(url):
    print(f"Downloading {url}...")
    time.sleep(2)  # Simulate network delay
    print(f"Finished {url}")

# Sequential: 6 seconds total
urls = ["file1.zip", "file2.zip", "file3.zip"]
for url in urls:
    download_file(url)
```

Each download waits for the previous one to complete. Total time: 6 seconds.

### The Solution: Concurrent Execution

```python
import time
from concurrent.futures import ThreadPoolExecutor

def download_file(url):
    print(f"Downloading {url}...")
    time.sleep(2)
    print(f"Finished {url}")

# Concurrent: ~2 seconds total
urls = ["file1.zip", "file2.zip", "file3.zip"]
with ThreadPoolExecutor() as executor:
    executor.map(download_file, urls)
```

All downloads happen simultaneously. Total time: ~2 seconds.

---

## Key Terminology

### Concurrency vs Parallelism

| Term | Definition | Analogy |
|------|------------|---------|
| **Concurrency** | Managing multiple tasks at once | One chef juggling multiple dishes |
| **Parallelism** | Executing multiple tasks simultaneously | Multiple chefs cooking simultaneously |

**Concurrency** is about structure — organizing code to handle multiple tasks.
**Parallelism** is about execution — actually running tasks at the same time.

```
Concurrency (single core):
Task A: ██░░██░░██
Task B: ░░██░░██░░
        Time →

Parallelism (multiple cores):
Task A: ██████████  (Core 1)
Task B: ██████████  (Core 2)
        Time →
```

### Threads vs Processes

| Aspect | Thread | Process |
|--------|--------|---------|
| Memory | Shared memory space | Separate memory space |
| Creation | Fast, lightweight | Slower, heavier |
| Communication | Easy (shared variables) | Requires IPC (queues, pipes) |
| GIL impact | Affected by GIL | Not affected by GIL |
| Best for | I/O-bound tasks | CPU-bound tasks |

### Synchronous vs Asynchronous

| Mode | Description |
|------|-------------|
| **Synchronous** | Wait for each operation to complete before starting next |
| **Asynchronous** | Start operations without waiting, handle results when ready |

---

## Python's Concurrency Tools

### Standard Library Modules

| Module | Purpose | Use Case |
|--------|---------|----------|
| `threading` | Thread-based concurrency | I/O-bound tasks |
| `multiprocessing` | Process-based parallelism | CPU-bound tasks |
| `concurrent.futures` | High-level interface | Both (recommended) |
| `asyncio` | Async I/O | High-concurrency I/O |
| `queue` | Thread-safe queues | Producer-consumer patterns |

### Which to Use?

```
Start here
    │
    ├─ Is the task CPU-intensive (computation)?
    │   │
    │   ├─ Yes → multiprocessing / ProcessPoolExecutor
    │   │
    │   └─ No → Continue
    │
    ├─ Is the task I/O-intensive (network, disk)?
    │   │
    │   ├─ Yes → threading / ThreadPoolExecutor
    │   │        or asyncio for very high concurrency
    │   │
    │   └─ No → Sequential is probably fine
    │
    └─ Simple parallel map over data?
        │
        └─ Yes → concurrent.futures (easiest)
```

---

## Real-World Examples

### I/O-Bound: Web Scraping

```python
import requests
from concurrent.futures import ThreadPoolExecutor

urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3",
]

def fetch(url):
    response = requests.get(url)
    return len(response.content)

# Threads work well — waiting for network I/O
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch, urls))
```

### CPU-Bound: Number Crunching

```python
from concurrent.futures import ProcessPoolExecutor

def compute_heavy(n):
    """CPU-intensive calculation."""
    return sum(i * i for i in range(n))

numbers = [10_000_000, 20_000_000, 30_000_000]

# Processes work well — true parallel computation
with ProcessPoolExecutor() as executor:
    results = list(executor.map(compute_heavy, numbers))
```

### Mixed: Data Pipeline

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def download_data(url):
    """I/O-bound: fetch from network."""
    import requests
    return requests.get(url).json()

def process_data(data):
    """CPU-bound: heavy computation."""
    return expensive_computation(data)

# Stage 1: Download (I/O-bound) — use threads
with ThreadPoolExecutor() as executor:
    raw_data = list(executor.map(download_data, urls))

# Stage 2: Process (CPU-bound) — use processes
with ProcessPoolExecutor() as executor:
    results = list(executor.map(process_data, raw_data))
```

---

## Performance Comparison

### Benchmark: I/O-Bound Task

```python
import time
import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def fetch_url(url):
    requests.get(url)
    return url

urls = ["https://httpbin.org/delay/1"] * 5

# Sequential: ~5 seconds
# ThreadPool: ~1 second  ✓ Best
# ProcessPool: ~1.5 seconds (overhead)
```

### Benchmark: CPU-Bound Task

```python
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def compute(n):
    return sum(i ** 2 for i in range(n))

numbers = [5_000_000] * 4

# Sequential: ~4 seconds (on 4-core machine)
# ThreadPool: ~4 seconds (GIL blocks parallelism)
# ProcessPool: ~1 second  ✓ Best
```

---

## Common Pitfalls

### 1. Using Threads for CPU-Bound Work

```python
# Bad: Threads don't help with CPU-bound tasks
with ThreadPoolExecutor() as executor:
    results = executor.map(heavy_computation, data)  # No speedup!

# Good: Use processes for CPU-bound tasks
with ProcessPoolExecutor() as executor:
    results = executor.map(heavy_computation, data)  # Real parallelism
```

### 2. Too Many Workers

```python
# Bad: 1000 threads/processes is wasteful
with ThreadPoolExecutor(max_workers=1000) as executor:
    ...

# Good: Match workers to task type
# I/O-bound: 10-50 threads typically sufficient
# CPU-bound: Match CPU cores
import os
with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
    ...
```

### 3. Shared State Without Synchronization

```python
# Bad: Race condition
counter = 0
def increment():
    global counter
    counter += 1  # Not thread-safe!

# Good: Use synchronization
import threading
counter = 0
lock = threading.Lock()
def increment():
    global counter
    with lock:
        counter += 1
```

---

## Chapter Overview

This chapter covers:

1. **Concurrency Concepts** — GIL, CPU vs I/O bound, threads vs processes
2. **threading Module** — Creating threads, synchronization, communication
3. **multiprocessing Module** — Processes, pools, sharing state
4. **concurrent.futures** — Modern, high-level API (recommended)
5. **Practical Patterns** — Decision guide, common patterns, error handling

---

## Key Takeaways

- **Concurrency** = managing multiple tasks; **Parallelism** = running simultaneously
- **Threads** share memory, affected by GIL — best for I/O-bound tasks
- **Processes** have separate memory, bypass GIL — best for CPU-bound tasks
- **concurrent.futures** provides the cleanest API for most use cases
- Match your concurrency strategy to your task type
- Always consider synchronization when sharing state

---

## Exercises

**Exercise 1.**
Write a program that creates two threads: one prints "Hello" 5 times with a 0.1s delay, and the other prints "World" 5 times with a 0.15s delay. Use `threading.Thread` to run them concurrently and `join()` to wait for both. Observe the interleaved output.

??? success "Solution to Exercise 1"
        ```python
        import threading
        import time

        def say_hello():
            for _ in range(5):
                print("Hello")
                time.sleep(0.1)

        def say_world():
            for _ in range(5):
                print("World")
                time.sleep(0.15)

        t1 = threading.Thread(target=say_hello)
        t2 = threading.Thread(target=say_world)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print("Both threads finished.")
        ```

---

**Exercise 2.**
Write a function that runs a simulated I/O task (`time.sleep(0.5)`) both sequentially (4 times) and concurrently using `ThreadPoolExecutor` with 4 workers. Measure and print the elapsed time for each approach and compute the speedup.

??? success "Solution to Exercise 2"
        ```python
        import time
        from concurrent.futures import ThreadPoolExecutor

        def io_task(n):
            time.sleep(0.5)
            return n

        # Sequential
        start = time.perf_counter()
        for i in range(4):
            io_task(i)
        seq_time = time.perf_counter() - start

        # Concurrent
        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=4) as executor:
            list(executor.map(io_task, range(4)))
        conc_time = time.perf_counter() - start

        print(f"Sequential: {seq_time:.2f}s")
        print(f"Concurrent: {conc_time:.2f}s")
        print(f"Speedup: {seq_time / conc_time:.2f}x")
        ```

---

**Exercise 3.**
Demonstrate the difference between threads and processes by running a CPU-bound function (sum of squares up to 5,000,000) four times using `ThreadPoolExecutor` and four times using `ProcessPoolExecutor`. Compare the elapsed times and explain which is faster and why.

??? success "Solution to Exercise 3"
        ```python
        import time
        from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

        def cpu_task(n):
            return sum(i * i for i in range(n))

        if __name__ == "__main__":
            args = [5_000_000] * 4

            start = time.perf_counter()
            with ThreadPoolExecutor(max_workers=4) as ex:
                list(ex.map(cpu_task, args))
            thread_time = time.perf_counter() - start

            start = time.perf_counter()
            with ProcessPoolExecutor(max_workers=4) as ex:
                list(ex.map(cpu_task, args))
            proc_time = time.perf_counter() - start

            print(f"Threads: {thread_time:.2f}s")
            print(f"Processes: {proc_time:.2f}s")
            print(f"Processes are faster because they bypass the GIL.")
        ```
