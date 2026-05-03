# ThreadPoolExecutor

`ThreadPoolExecutor` manages a pool of worker threads for concurrent execution. Best suited for **I/O-bound tasks** where the GIL is released.

!!! tip "Mental Model"
    A ThreadPoolExecutor is a reusable team of threads that pick up jobs from a shared queue. You submit work, the pool assigns it to an idle thread, and you get a Future back. Because threads share memory and the GIL is released during I/O, this is the fastest way to parallelize network calls, file reads, and database queries without the overhead of spawning processes.

---

## Basic Usage

```python
from concurrent.futures import ThreadPoolExecutor
import time

def fetch_url(url):
    """Simulate fetching a URL."""
    print(f"Fetching {url}...")
    time.sleep(1)  # Simulate network delay
    return f"Content from {url}"

urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3",
]

# Sequential: ~3 seconds
start = time.perf_counter()
results = [fetch_url(url) for url in urls]
print(f"Sequential: {time.perf_counter() - start:.2f}s")

# Concurrent: ~1 second
start = time.perf_counter()
with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(fetch_url, urls))
print(f"Concurrent: {time.perf_counter() - start:.2f}s")
```

---

## Creating ThreadPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor

# Default workers: min(32, os.cpu_count() + 4)
executor = ThreadPoolExecutor()

# Explicit worker count
executor = ThreadPoolExecutor(max_workers=10)

# With thread naming
executor = ThreadPoolExecutor(
    max_workers=5,
    thread_name_prefix="Downloader"
)

# With initializer
executor = ThreadPoolExecutor(
    max_workers=5,
    initializer=setup_function,
    initargs=(arg1, arg2)
)
```

---

## Using map()

Apply a function to every item in an iterable:

```python
from concurrent.futures import ThreadPoolExecutor
import time

def process(item):
    time.sleep(0.5)
    return item.upper()

items = ["apple", "banana", "cherry", "date", "elderberry"]

with ThreadPoolExecutor(max_workers=5) as executor:
    # Results are returned in input order
    results = list(executor.map(process, items))
    print(results)  # ['APPLE', 'BANANA', 'CHERRY', 'DATE', 'ELDERBERRY']
```

### map() with Multiple Arguments

```python
from concurrent.futures import ThreadPoolExecutor

def power(base, exp):
    return base ** exp

bases = [2, 3, 4, 5]
exps = [3, 4, 5, 6]

with ThreadPoolExecutor() as executor:
    # Use zip for multiple iterables
    results = list(executor.map(power, bases, exps))
    print(results)  # [8, 81, 1024, 15625]
```

### map() with Timeout

```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import time

def slow_task(x):
    time.sleep(x)
    return x

with ThreadPoolExecutor() as executor:
    try:
        # Timeout applies to entire iteration
        results = list(executor.map(slow_task, [1, 5, 1], timeout=3))
    except TimeoutError:
        print("Operation timed out!")
```

---

## Using submit()

Submit individual tasks and get Future objects:

```python
from concurrent.futures import ThreadPoolExecutor
import time

def download(url):
    time.sleep(1)
    return f"Downloaded {url}"

with ThreadPoolExecutor(max_workers=3) as executor:
    # Submit returns Future immediately
    future1 = executor.submit(download, "https://site1.com")
    future2 = executor.submit(download, "https://site2.com")
    future3 = executor.submit(download, "https://site3.com")
    
    # Get results
    print(future1.result())
    print(future2.result())
    print(future3.result())
```

### Submitting Multiple Tasks

```python
from concurrent.futures import ThreadPoolExecutor

def process(x):
    return x ** 2

with ThreadPoolExecutor() as executor:
    # Submit all tasks
    futures = [executor.submit(process, i) for i in range(10)]
    
    # Collect results
    results = [f.result() for f in futures]
    print(results)
```

---

## Processing Results as They Complete

### as_completed() — Results in Completion Order

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

def variable_task(task_id):
    delay = random.uniform(0.1, 1.0)
    time.sleep(delay)
    return (task_id, delay)

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(variable_task, i): i for i in range(10)}
    
    # Process results as they complete (fastest first)
    for future in as_completed(futures):
        task_id = futures[future]
        try:
            result = future.result()
            print(f"Task {task_id} completed: {result}")
        except Exception as e:
            print(f"Task {task_id} failed: {e}")
```

### as_completed() with Timeout

```python
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(slow_task, i) for i in range(10)]
    
    try:
        for future in as_completed(futures, timeout=5):
            print(future.result())
    except TimeoutError:
        print("Some tasks didn't complete in time")
```

### wait() — Wait for Specific Conditions

```python
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, ALL_COMPLETED
import time

def task(x):
    time.sleep(x)
    return x

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(task, i) for i in [3, 1, 2]]
    
    # Wait for first to complete
    done, not_done = wait(futures, return_when=FIRST_COMPLETED)
    print(f"First completed: {done.pop().result()}")
    
    # Wait for all to complete
    done, not_done = wait(futures, return_when=ALL_COMPLETED)
    print(f"All done: {[f.result() for f in done]}")
```

---

## Error Handling

### Per-Task Exception Handling

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def risky_task(x):
    if x == 5:
        raise ValueError(f"Cannot process {x}")
    return x ** 2

with ThreadPoolExecutor() as executor:
    futures = {executor.submit(risky_task, i): i for i in range(10)}
    
    results = []
    errors = []
    
    for future in as_completed(futures):
        task_id = futures[future]
        try:
            result = future.result()
            results.append((task_id, result))
        except Exception as e:
            errors.append((task_id, str(e)))
    
    print(f"Successes: {len(results)}")
    print(f"Failures: {errors}")
```

### Graceful Degradation

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_with_fallback(url):
    try:
        return fetch(url)
    except Exception:
        return fetch_from_cache(url)

with ThreadPoolExecutor() as executor:
    results = list(executor.map(fetch_with_fallback, urls))
```

---

## Practical Examples

### Web Scraping

```python
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

def scrape_page(url):
    """Fetch and parse a webpage."""
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title')
    return {
        'url': url,
        'title': title.text if title else 'No title',
        'links': len(soup.find_all('a'))
    }

urls = [
    "https://example.com",
    "https://python.org",
    "https://github.com",
]

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(scrape_page, urls))

for r in results:
    print(f"{r['url']}: {r['title']} ({r['links']} links)")
```

### Bulk API Requests

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

def fetch_user(user_id):
    """Fetch user data from API."""
    response = requests.get(
        f"https://api.example.com/users/{user_id}",
        timeout=5
    )
    return response.json()

user_ids = range(1, 101)

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(fetch_user, uid): uid for uid in user_ids}
    
    users = []
    for future in as_completed(futures):
        uid = futures[future]
        try:
            user = future.result()
            users.append(user)
        except Exception as e:
            print(f"Failed to fetch user {uid}: {e}")

print(f"Fetched {len(users)} users")
```

### File I/O

```python
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def read_file(filepath):
    """Read and return file contents."""
    return Path(filepath).read_text()

def process_file(filepath):
    """Read, process, and return result."""
    content = Path(filepath).read_text()
    return {
        'path': str(filepath),
        'lines': len(content.splitlines()),
        'chars': len(content)
    }

files = list(Path('.').glob('*.py'))

with ThreadPoolExecutor(max_workers=10) as executor:
    stats = list(executor.map(process_file, files))

for s in stats:
    print(f"{s['path']}: {s['lines']} lines, {s['chars']} chars")
```

### Database Operations

```python
from concurrent.futures import ThreadPoolExecutor
import threading

# Thread-local database connection
_local = threading.local()

def init_db_connection(connection_string):
    """Initialize database connection for each thread."""
    _local.conn = create_connection(connection_string)

def query_db(sql):
    """Execute query using thread's connection."""
    cursor = _local.conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

queries = [
    "SELECT * FROM users LIMIT 100",
    "SELECT * FROM orders LIMIT 100",
    "SELECT * FROM products LIMIT 100",
]

with ThreadPoolExecutor(
    max_workers=3,
    initializer=init_db_connection,
    initargs=("postgresql://localhost/mydb",)
) as executor:
    results = list(executor.map(query_db, queries))
```

---

## Best Practices

### 1. Choose Appropriate Worker Count

```python
# I/O-bound: more workers than CPUs
# Network requests, file I/O
executor = ThreadPoolExecutor(max_workers=20)

# Mixed workload: moderate count
executor = ThreadPoolExecutor(max_workers=10)

# Default is often reasonable
executor = ThreadPoolExecutor()  # min(32, cpu_count + 4)
```

### 2. Use Context Manager

```python
# Good: automatic cleanup
with ThreadPoolExecutor() as executor:
    results = executor.map(func, data)

# Avoid: manual management
executor = ThreadPoolExecutor()
try:
    results = executor.map(func, data)
finally:
    executor.shutdown()
```

### 3. Handle Timeouts

```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError

with ThreadPoolExecutor() as executor:
    future = executor.submit(potentially_slow_task)
    try:
        result = future.result(timeout=30)
    except TimeoutError:
        print("Task timed out")
```

### 4. Don't Use for CPU-Bound Tasks

```python
# Bad: GIL prevents parallelism
with ThreadPoolExecutor() as executor:
    results = executor.map(cpu_intensive_task, data)  # No speedup!

# Good: Use ProcessPoolExecutor for CPU-bound
with ProcessPoolExecutor() as executor:
    results = executor.map(cpu_intensive_task, data)
```

---

## Key Takeaways

- Use `ThreadPoolExecutor` for **I/O-bound tasks** (network, files, databases)
- GIL is released during I/O, allowing true concurrency
- `map()` for same function applied to many inputs
- `submit()` for individual tasks with Future objects
- `as_completed()` to process results as they finish
- Set `max_workers` based on workload (10-50 for I/O)
- Use initializer for per-thread setup (connections)
- Always use context manager for automatic cleanup
- **Not suitable for CPU-bound tasks** — use `ProcessPoolExecutor` instead

---

## Runnable Example: `threadpool_executor_map.py`

```python
"""
TUTORIAL: ThreadPoolExecutor.map() for Concurrent Execution
============================================================

In this tutorial, you'll learn how to use ThreadPoolExecutor.map() to run
multiple functions concurrently with a pool of worker threads.

KEY CONCEPTS:
- ThreadPoolExecutor: A pool of reusable worker threads
- executor.map(): Apply a function to multiple arguments concurrently
- Iterator pattern: Results are returned as an iterator
- Lazy evaluation: Results computed on-demand as you iterate
- Thread pooling: Reuses threads instead of creating new ones

WHY THIS MATTERS:
- Much faster than creating a new thread for each task
- Perfect for I/O-bound work (network, file operations)
- Cleaner API than managing individual threads manually
"""

from time import sleep, strftime
from concurrent import futures


print("=" * 70)
print("THREADPOOLEXECUTOR.MAP() FOR CONCURRENT EXECUTION")
print("=" * 70)
print()


# ============ HELPER FUNCTIONS FOR LOGGING
# ===========================================

def display(*args):
    """
    Print with a timestamp prefix.

    WHY: This helps us see exactly when each task starts and finishes.
    The [HH:MM:SS] prefix shows the precise timing of concurrent operations.
    """
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)


# ============ EXAMPLE 1: Understanding the Concurrent Task
# ==========================================================

print("EXAMPLE 1: The Task We'll Run Concurrently")
print("-" * 70)
print()
print("We'll create a function that simulates work by sleeping.")
print("This represents I/O-bound tasks like network requests.")
print()


def loiter(n):
    """
    Simulate work that takes n seconds.

    WHY THIS DESIGN:
    - Sleeping simulates network I/O or file operations
    - The function takes n seconds and returns n*10
    - With threads, all these can run in parallel!

    Args:
        n: Number of seconds to sleep (simulating work)

    Returns:
        n * 10 (a processed result)
    """

    msg = '{}loiter({}): doing nothing for {}s...'
    # \t adds indentation proportional to n - helps visualize which task
    display(msg.format('\t' * n, n, n))

    # Sleep to simulate I/O-bound work
    sleep(n)

    msg = '{}loiter({}): done.'
    display(msg.format('\t' * n, n))

    return n * 10


print("Function loiter(n) defined:")
print("• Takes n seconds (simulates I/O)")
print("• Returns n * 10")
print()
print("About to call loiter(1), loiter(2), loiter(3), loiter(4), loiter(5)")
print()


# ============ EXAMPLE 2: Sequential vs Concurrent Timing
# ========================================================

print("EXAMPLE 2: Understanding the Difference")
print("-" * 70)
print()
print("SEQUENTIAL APPROACH (without threading):")
print("  loiter(1): 1 second")
print("  loiter(2): 2 seconds")
print("  loiter(3): 3 seconds")
print("  loiter(4): 4 seconds")
print("  loiter(5): 5 seconds")
print("  Total: 15 seconds (everything waits for the previous task)")
print()
print("CONCURRENT APPROACH (with ThreadPoolExecutor):")
print("  All tasks run in parallel!")
print("  Total: ~5 seconds (longest task determines total time)")
print()
print("Watch the timestamps below - you'll see multiple tasks running")
print("at the SAME TIME when we use executor.map():")
print()


# ============ EXAMPLE 3: Using ThreadPoolExecutor.map()
# ======================================================

def main():
    """
    Demonstrate ThreadPoolExecutor.map() for concurrent execution.
    """

    print("=" * 70)
    print("STARTING CONCURRENT EXECUTION")
    print("=" * 70)
    print()

    # Record the start time to see total elapsed time
    display('Script starting.')
    print()

    # Create a ThreadPoolExecutor with 3 worker threads
    # WHY 3 workers?
    # - With max_workers=3, we can run 3 tasks in parallel
    # - Task 1,2,3 start immediately
    # - When task 1 finishes, task 4 starts
    # - When task 2 finishes, task 5 starts
    # - This is much more efficient than 5 threads!
    executor = futures.ThreadPoolExecutor(max_workers=3)

    print(f"Created ThreadPoolExecutor with max_workers=3")
    print()
    print("executor.map(loiter, range(5)) will:")
    print("  • Create 5 tasks: loiter(0), loiter(1), loiter(2), loiter(3), loiter(4)")
    print("  • Run them across 3 worker threads concurrently")
    print("  • Return an iterator of results")
    print()

    # Execute all the tasks concurrently
    # WHY map()? It applies loiter() to each number in range(5)
    # and returns an iterator of results
    results = executor.map(loiter, range(5))

    # Important: results is an ITERATOR, not a list!
    # WHY? Because results haven't been computed yet.
    # They're computed lazily as we iterate over them below.
    display('results:', results)
    print()
    print("Note: 'results' is an iterator, not a list of values yet")
    print("The actual computation hasn't happened - it starts when we")
    print("iterate over the results below!")
    print()

    # Now iterate over the results
    # WHY iterate instead of just accessing results?
    # 1. Lets us get results as they complete (lazy evaluation)
    # 2. Blocks until each result is ready
    # 3. Respects the order of the original tasks
    display('Waiting for individual results:')
    print()

    for i, result in enumerate(results):
        # Each iteration here blocks until that result is ready
        # Result 0 finishes first (loiter(0) is instant)
        # Then results appear in order as they complete
        display(f'result {i}: {result}')

    print()
    print("=" * 70)
    print("All tasks completed!")
    print("=" * 70)


# ============ EXAMPLE 4: Key Concepts Explained
# ==============================================

print()
print("=" * 70)
print("KEY CONCEPTS:")
print("=" * 70)
print()
print("1. ThreadPoolExecutor: Manages a fixed number of worker threads")
print()
print("2. executor.map(func, iterable):")
print("   • Applies func to each item in iterable")
print("   • Returns an ITERATOR of results (computed lazily)")
print("   • Maintains order of results (even if tasks finish out of order)")
print()
print("3. max_workers:")
print("   • Number of threads in the pool")
print("   • Use max_workers=3 for 5 tasks = efficient reuse")
print("   • Don't use max_workers=5 for 5 tasks (wastes resources)")
print()
print("4. Lazy Evaluation:")
print("   • Results iterator doesn't compute anything until you iterate")
print("   • Each iteration blocks until that specific result is ready")
print("   • This saves memory and allows result streaming")
print()
print("5. When to Use ThreadPoolExecutor:")
print("   • I/O-bound tasks (network, file, database operations)")
print("   • NOT CPU-bound tasks (use multiprocessing.Pool instead)")
print()
print("=" * 70)
print()


if __name__ == '__main__':
    main()
```

---

## Exercises

**Exercise 1.**
Use `ThreadPoolExecutor` with 5 workers to concurrently simulate fetching 10 URLs (each `time.sleep(0.5)` returning the URL string). Measure the elapsed time and verify it is approximately 1 second (two batches of 5), not 5 seconds.

??? success "Solution to Exercise 1"
        ```python
        import time
        from concurrent.futures import ThreadPoolExecutor

        def fetch(url):
            time.sleep(0.5)
            return url

        urls = [f"https://example.com/page{i}" for i in range(10)]

        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=5) as ex:
            results = list(ex.map(fetch, urls))
        elapsed = time.perf_counter() - start

        print(f"Fetched {len(results)} URLs in {elapsed:.2f}s")
        assert elapsed < 2.0, "Should be ~1s, not 5s"
        ```

---

**Exercise 2.**
Use `submit()` and `as_completed()` to process 15 tasks with random delays (0.1-0.8s). Map each future to its task ID using a dictionary. Print results in completion order, showing the task ID and result. Count how many completed in under 0.5 seconds.

??? success "Solution to Exercise 2"
        ```python
        import time
        import random
        from concurrent.futures import ThreadPoolExecutor, as_completed

        def task(tid):
            delay = random.uniform(0.1, 0.8)
            time.sleep(delay)
            return tid, delay

        fast_count = 0
        with ThreadPoolExecutor(max_workers=5) as ex:
            futs = {ex.submit(task, i): i for i in range(15)}
            for f in as_completed(futs):
                tid, delay = f.result()
                print(f"Task {tid}: {delay:.2f}s")
                if delay < 0.5:
                    fast_count += 1

        print(f"\n{fast_count}/15 completed in under 0.5s")
        ```

---

**Exercise 3.**
Implement a retry wrapper. Write a `fetch_with_retry(url, max_retries=3)` function that simulates a flaky network call (randomly raises `ConnectionError` 50% of the time). Use `ThreadPoolExecutor` to fetch 8 URLs concurrently. Print which URLs succeeded, which exhausted retries, and the total elapsed time.

??? success "Solution to Exercise 3"
        ```python
        import time
        import random
        from concurrent.futures import ThreadPoolExecutor

        def fetch_with_retry(url, max_retries=3):
            for attempt in range(max_retries):
                if random.random() > 0.5:
                    return f"OK: {url}"
                time.sleep(0.1)
            return f"FAIL: {url}"

        urls = [f"https://api.example.com/{i}" for i in range(8)]

        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=4) as ex:
            results = list(ex.map(fetch_with_retry, urls))
        elapsed = time.perf_counter() - start

        ok = sum(1 for r in results if r.startswith("OK"))
        fail = sum(1 for r in results if r.startswith("FAIL"))
        for r in results:
            print(f"  {r}")
        print(f"\nSucceeded: {ok}, Failed: {fail}, Time: {elapsed:.2f}s")
        ```
