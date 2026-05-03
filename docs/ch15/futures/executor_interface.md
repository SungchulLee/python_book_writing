# Executor Interface

`concurrent.futures` provides a high-level interface for asynchronously executing callables. It's the **recommended approach** for most concurrent programming in Python.

!!! tip "Mental Model"
    The Executor is a universal job dispatcher: hand it a function and arguments, and it returns a Future (an IOU for the result). Whether the work runs in threads or processes is a one-line swap -- `ThreadPoolExecutor` vs `ProcessPoolExecutor` -- because both share the same `submit`/`map` interface. Start here for any concurrent task; drop down to raw threads or processes only when you need finer control.

---

## Why concurrent.futures?

### Before: Low-Level Threading/Multiprocessing

```python
import threading
import queue

# Manual thread management
result_queue = queue.Queue()

def worker(x, q):
    q.put(x ** 2)

threads = []
for i in range(10):
    t = threading.Thread(target=worker, args=(i, result_queue))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

results = [result_queue.get() for _ in range(10)]
```

### After: concurrent.futures

```python
from concurrent.futures import ThreadPoolExecutor

def square(x):
    return x ** 2

with ThreadPoolExecutor() as executor:
    results = list(executor.map(square, range(10)))
```

---

## The Executor Interface

Both `ThreadPoolExecutor` and `ProcessPoolExecutor` share the same interface:

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Same interface for both
executor = ThreadPoolExecutor(max_workers=4)
# or
executor = ProcessPoolExecutor(max_workers=4)

# Submit individual tasks
future = executor.submit(function, arg1, arg2)

# Map function over iterable
results = executor.map(function, iterable)

# Shutdown
executor.shutdown(wait=True)
```

---

## Core Methods

### submit() — Submit Single Task

```python
from concurrent.futures import ThreadPoolExecutor

def compute(x, y):
    return x + y

with ThreadPoolExecutor() as executor:
    # Returns Future immediately
    future = executor.submit(compute, 10, 20)
    
    # Get result (blocks until complete)
    result = future.result()
    print(result)  # 30
```

### map() — Apply Function to Iterable

```python
from concurrent.futures import ThreadPoolExecutor

def square(x):
    return x ** 2

with ThreadPoolExecutor() as executor:
    # Returns iterator of results (in order)
    results = executor.map(square, [1, 2, 3, 4, 5])
    print(list(results))  # [1, 4, 9, 16, 25]
```

### shutdown() — Stop Executor

```python
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

# Submit tasks...
future = executor.submit(lambda: 42)

# Shutdown options
executor.shutdown(wait=True)   # Wait for pending tasks (default)
executor.shutdown(wait=False)  # Return immediately
executor.shutdown(wait=True, cancel_futures=True)  # Cancel pending (Python 3.9+)
```

---

## Context Manager (Recommended)

```python
from concurrent.futures import ThreadPoolExecutor

def process(x):
    return x * 2

# Automatic shutdown when exiting context
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process, range(10)))

# executor is automatically shut down here
print(results)
```

---

## Switching Between Threads and Processes

The unified interface makes it easy to switch:

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def compute(x):
    return x ** 2

data = list(range(100))

# For I/O-bound tasks: use threads
with ThreadPoolExecutor(max_workers=10) as executor:
    thread_results = list(executor.map(compute, data))

# For CPU-bound tasks: use processes
with ProcessPoolExecutor(max_workers=4) as executor:
    process_results = list(executor.map(compute, data))
```

### Factory Pattern

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def get_executor(task_type, max_workers=None):
    """Get appropriate executor for task type."""
    if task_type == "io":
        return ThreadPoolExecutor(max_workers=max_workers or 20)
    elif task_type == "cpu":
        return ProcessPoolExecutor(max_workers=max_workers)
    else:
        raise ValueError(f"Unknown task type: {task_type}")

# Usage
with get_executor("io") as executor:
    results = executor.map(fetch_url, urls)

with get_executor("cpu") as executor:
    results = executor.map(heavy_computation, data)
```

---

## Executor Parameters

### ThreadPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(
    max_workers=10,           # Max threads (default: min(32, cpu_count + 4))
    thread_name_prefix="Worker",  # Prefix for thread names
    initializer=init_func,    # Called in each thread at start
    initargs=(arg1, arg2),    # Arguments for initializer
)
```

### ProcessPoolExecutor

```python
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

executor = ProcessPoolExecutor(
    max_workers=4,            # Max processes (default: cpu_count)
    mp_context=mp.get_context("spawn"),  # Start method
    initializer=init_func,    # Called in each process at start
    initargs=(arg1, arg2),    # Arguments for initializer
    max_tasks_per_child=100,  # Restart worker after N tasks (Python 3.11+)
)
```

---

## Initializer Functions

Run setup code in each worker:

```python
from concurrent.futures import ThreadPoolExecutor
import threading

# Thread-local storage
local = threading.local()

def init_worker(connection_string):
    """Initialize each worker thread."""
    local.db = create_connection(connection_string)
    print(f"Worker {threading.current_thread().name}: DB connected")

def query(sql):
    """Use worker's database connection."""
    return local.db.execute(sql)

with ThreadPoolExecutor(
    max_workers=4,
    initializer=init_worker,
    initargs=("postgresql://localhost/mydb",)
) as executor:
    queries = ["SELECT * FROM users", "SELECT * FROM orders"]
    results = list(executor.map(query, queries))
```

---

## Error Handling

### Exceptions in submit()

```python
from concurrent.futures import ThreadPoolExecutor

def risky_task(x):
    if x < 0:
        raise ValueError("Negative not allowed")
    return x ** 2

with ThreadPoolExecutor() as executor:
    future = executor.submit(risky_task, -5)
    
    try:
        result = future.result()  # Raises exception here
    except ValueError as e:
        print(f"Task failed: {e}")
```

### Exceptions in map()

```python
from concurrent.futures import ThreadPoolExecutor

def risky_task(x):
    if x == 3:
        raise ValueError(f"Cannot process {x}")
    return x ** 2

with ThreadPoolExecutor() as executor:
    try:
        # Exception raised when iterating
        results = list(executor.map(risky_task, range(5)))
    except ValueError as e:
        print(f"Error: {e}")
```

### Handling Errors Per Task

```python
from concurrent.futures import ThreadPoolExecutor

def safe_task(x):
    try:
        if x == 3:
            raise ValueError("Bad value")
        return ("success", x ** 2)
    except Exception as e:
        return ("error", str(e))

with ThreadPoolExecutor() as executor:
    results = list(executor.map(safe_task, range(5)))
    
    for status, value in results:
        if status == "success":
            print(f"Result: {value}")
        else:
            print(f"Error: {value}")
```

---

## Timeout Support

### result() with Timeout

```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import time

def slow_task():
    time.sleep(10)
    return "Done"

with ThreadPoolExecutor() as executor:
    future = executor.submit(slow_task)
    
    try:
        result = future.result(timeout=2)  # Wait max 2 seconds
    except TimeoutError:
        print("Task timed out!")
        future.cancel()  # Try to cancel (may not work if already running)
```

### map() with Timeout

```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError

def slow_task(x):
    import time
    time.sleep(x)
    return x

with ThreadPoolExecutor() as executor:
    try:
        # timeout applies to entire iteration
        results = list(executor.map(slow_task, [1, 2, 3], timeout=2))
    except TimeoutError:
        print("Map operation timed out!")
```

---

## Comparison: map() vs submit()

| Feature | map() | submit() |
|---------|-------|----------|
| **Input** | Iterable | Individual arguments |
| **Returns** | Iterator of results | Single Future |
| **Order** | Preserves input order | N/A |
| **Error handling** | First exception stops iteration | Per-task exception handling |
| **Flexibility** | Less (same function) | More (different functions) |
| **Memory** | Lazy (iterator) | Eager (all Futures at once) |

### When to Use map()

```python
# Same function applied to many inputs
results = executor.map(process, items)
```

### When to Use submit()

```python
# Different functions or complex handling
futures = []
futures.append(executor.submit(download, url))
futures.append(executor.submit(process, data))
futures.append(executor.submit(upload, result))
```

---

## Practical Example

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

def fetch_data(url):
    """I/O-bound: fetch from URL."""
    time.sleep(0.5)  # Simulate network
    return f"Data from {url}"

def process_data(data):
    """CPU-bound: process data."""
    time.sleep(0.1)  # Simulate computation
    return f"Processed: {data}"

urls = [f"https://api.example.com/data/{i}" for i in range(10)]

# Stage 1: Fetch (I/O-bound) — use threads
with ThreadPoolExecutor(max_workers=10) as executor:
    raw_data = list(executor.map(fetch_data, urls))
print(f"Fetched {len(raw_data)} items")

# Stage 2: Process (CPU-bound) — use processes
with ProcessPoolExecutor() as executor:
    processed = list(executor.map(process_data, raw_data))
print(f"Processed {len(processed)} items")
```

---

## Key Takeaways

- `concurrent.futures` provides **unified interface** for threads and processes
- Use **context manager** (`with`) for automatic cleanup
- `submit()` for individual tasks, returns `Future`
- `map()` for applying function to iterable, returns iterator
- **Same code works** with both `ThreadPoolExecutor` and `ProcessPoolExecutor`
- Switch between threads (I/O-bound) and processes (CPU-bound) easily
- Use `initializer` for per-worker setup (database connections, etc.)
- Handle exceptions via `future.result()` or wrap in try/except

---

## Exercises

**Exercise 1.**
Write a program that uses `executor.map()` with `ThreadPoolExecutor` to convert a list of 10 strings to uppercase, with a 0.3-second simulated delay per item. Then switch to `ProcessPoolExecutor` without changing any other code. Print both sets of results and verify they are identical.

??? success "Solution to Exercise 1"
        ```python
        import time
        from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

        def slow_upper(s):
            time.sleep(0.3)
            return s.upper()

        strings = [f"item_{i}" for i in range(10)]

        with ThreadPoolExecutor(max_workers=5) as ex:
            thread_results = list(ex.map(slow_upper, strings))

        with ProcessPoolExecutor(max_workers=5) as ex:
            proc_results = list(ex.map(slow_upper, strings))

        print(f"Thread results: {thread_results}")
        print(f"Process results: {proc_results}")
        assert thread_results == proc_results
        ```

---

**Exercise 2.**
Use `executor.submit()` to submit 5 tasks that each return the square of their argument. Collect the `Future` objects into a list, then use `as_completed()` to print results in completion order. Use random sleep (0.1-1.0s) in the worker to make completion order differ from submission order.

??? success "Solution to Exercise 2"
        ```python
        import time
        import random
        from concurrent.futures import ThreadPoolExecutor, as_completed

        def slow_square(x):
            time.sleep(random.uniform(0.1, 1.0))
            return x ** 2

        with ThreadPoolExecutor(max_workers=3) as ex:
            futures = {ex.submit(slow_square, i): i for i in range(5)}
            for future in as_completed(futures):
                inp = futures[future]
                print(f"Input {inp} -> {future.result()}")
        ```

---

**Exercise 3.**
Create an `Executor` factory function that accepts a string `"io"` or `"cpu"` and returns the appropriate executor. Write a two-stage pipeline: stage 1 uses the I/O executor to "download" 6 items (simulated with `time.sleep(0.5)`), stage 2 uses the CPU executor to "process" the downloaded items (sum of squares up to 1,000,000). Print the total elapsed time.

??? success "Solution to Exercise 3"
        ```python
        import time
        from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

        def get_executor(kind):
            if kind == "io":
                return ThreadPoolExecutor(max_workers=6)
            return ProcessPoolExecutor()

        def download(item_id):
            time.sleep(0.5)
            return f"data_{item_id}"

        def process(data):
            return sum(i * i for i in range(1_000_000))

        if __name__ == "__main__":
            start = time.perf_counter()

            with get_executor("io") as ex:
                raw = list(ex.map(download, range(6)))

            with get_executor("cpu") as ex:
                results = list(ex.map(process, raw))

            elapsed = time.perf_counter() - start
            print(f"Processed {len(results)} items in {elapsed:.2f}s")
        ```
