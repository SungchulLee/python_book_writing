# Process Pool

A `Pool` manages a collection of worker processes, providing a simple way to parallelize function execution across multiple inputs.

!!! tip "Mental Model"
    A `Pool` is a batch-processing factory: you feed it a function and a list of inputs, and it distributes the items across worker processes automatically. Think `map()` but parallel -- each worker grabs the next item, computes the result, and returns it. The pool handles process creation, work distribution, and result collection so you can focus on the computation itself.

---

## Creating a Pool

### Basic Pool Usage

```python
from multiprocessing import Pool
import os

def square(x):
    print(f"Process {os.getpid()}: computing {x}²")
    return x ** 2

if __name__ == "__main__":
    # Create pool with 4 worker processes
    with Pool(4) as pool:
        results = pool.map(square, [1, 2, 3, 4, 5])
    
    print(results)  # [1, 4, 9, 16, 25]
```

### Default Worker Count

```python
from multiprocessing import Pool, cpu_count

# Default: uses cpu_count() workers
with Pool() as pool:
    print(f"Workers: {pool._processes}")  # Number of CPUs

# Explicit count
with Pool(processes=8) as pool:
    pass
```

---

## Pool Methods

### map() — Parallel Map

Apply function to each item in iterable, return results in order:

```python
from multiprocessing import Pool
import time

def slow_square(x):
    time.sleep(0.5)
    return x ** 2

if __name__ == "__main__":
    numbers = list(range(10))
    
    # Sequential
    start = time.perf_counter()
    results = list(map(slow_square, numbers))
    print(f"Sequential: {time.perf_counter() - start:.2f}s")
    
    # Parallel
    start = time.perf_counter()
    with Pool(4) as pool:
        results = pool.map(slow_square, numbers)
    print(f"Parallel: {time.perf_counter() - start:.2f}s")
    
    print(results)
```

### map() with Chunksize

```python
from multiprocessing import Pool

def process(x):
    return x * 2

if __name__ == "__main__":
    data = list(range(1000))
    
    with Pool(4) as pool:
        # Default: pool divides work automatically
        results = pool.map(process, data)
        
        # Chunksize: send N items to each worker at a time
        # Larger chunks = less IPC overhead, but less load balancing
        results = pool.map(process, data, chunksize=100)
```

### starmap() — Multiple Arguments

```python
from multiprocessing import Pool

def power(base, exp):
    return base ** exp

if __name__ == "__main__":
    # starmap unpacks argument tuples
    args = [(2, 3), (3, 4), (4, 5), (5, 6)]
    
    with Pool(4) as pool:
        results = pool.starmap(power, args)
    
    print(results)  # [8, 81, 1024, 15625]
```

### imap() — Lazy Iterator

Returns results as they complete (memory efficient for large datasets):

```python
from multiprocessing import Pool
import time

def slow_process(x):
    time.sleep(0.5)
    return x ** 2

if __name__ == "__main__":
    with Pool(4) as pool:
        # imap returns iterator, not list
        results = pool.imap(slow_process, range(10))
        
        # Process results as they become available
        for result in results:
            print(f"Got result: {result}")
```

### imap_unordered() — Fastest Results First

Returns results in completion order (not input order):

```python
from multiprocessing import Pool
import time
import random

def variable_task(x):
    delay = random.uniform(0.1, 1.0)
    time.sleep(delay)
    return (x, delay)

if __name__ == "__main__":
    with Pool(4) as pool:
        # Results come in completion order
        for result in pool.imap_unordered(variable_task, range(10)):
            print(f"Completed: {result}")
```

### apply() — Single Function Call

```python
from multiprocessing import Pool

def compute(x, y, z):
    return x + y + z

if __name__ == "__main__":
    with Pool(4) as pool:
        # apply() blocks until result ready
        result = pool.apply(compute, args=(1, 2, 3))
        print(result)  # 6
```

### apply_async() — Asynchronous Single Call

```python
from multiprocessing import Pool
import time

def slow_compute(x):
    time.sleep(1)
    return x ** 2

if __name__ == "__main__":
    with Pool(4) as pool:
        # Submit task, get AsyncResult immediately
        async_result = pool.apply_async(slow_compute, args=(10,))
        
        print("Doing other work...")
        time.sleep(0.5)
        
        # Get result (blocks if not ready)
        result = async_result.get()
        print(f"Result: {result}")
```

### map_async() — Asynchronous Map

```python
from multiprocessing import Pool
import time

def process(x):
    time.sleep(0.5)
    return x ** 2

if __name__ == "__main__":
    with Pool(4) as pool:
        # Submit all tasks, get AsyncResult
        async_result = pool.map_async(process, range(10))
        
        print("Tasks submitted, doing other work...")
        
        # Check if ready
        while not async_result.ready():
            print("Still working...")
            time.sleep(0.3)
        
        # Get all results
        results = async_result.get()
        print(results)
```

---

## AsyncResult Object

Methods available on `AsyncResult` returned by async methods:

```python
from multiprocessing import Pool
import time

def slow_task(x):
    time.sleep(2)
    return x ** 2

if __name__ == "__main__":
    with Pool(4) as pool:
        async_result = pool.apply_async(slow_task, args=(10,))
        
        # Check if complete
        print(f"Ready: {async_result.ready()}")  # False
        
        # Wait with timeout
        async_result.wait(timeout=1)
        print(f"Ready after wait: {async_result.ready()}")  # Still False
        
        # Check if successful (blocks until complete)
        # print(f"Successful: {async_result.successful()}")
        
        # Get result (blocks until complete)
        result = async_result.get(timeout=5)
        print(f"Result: {result}")
```

---

## Error Handling in Pools

### Handling Exceptions

```python
from multiprocessing import Pool

def risky_task(x):
    if x == 3:
        raise ValueError(f"Cannot process {x}")
    return x ** 2

if __name__ == "__main__":
    with Pool(4) as pool:
        try:
            # Exception raised when iterating results
            results = pool.map(risky_task, [1, 2, 3, 4, 5])
        except ValueError as e:
            print(f"Error: {e}")
```

### Handling Exceptions with imap

```python
from multiprocessing import Pool

def risky_task(x):
    if x == 3:
        raise ValueError(f"Cannot process {x}")
    return x ** 2

if __name__ == "__main__":
    with Pool(4) as pool:
        results = pool.imap(risky_task, range(5))
        
        for i in range(5):
            try:
                result = next(results)
                print(f"Result: {result}")
            except ValueError as e:
                print(f"Error: {e}")
            except StopIteration:
                break
```

### Error Callback with apply_async

```python
from multiprocessing import Pool

def task(x):
    if x < 0:
        raise ValueError("Negative!")
    return x ** 2

def on_success(result):
    print(f"Success: {result}")

def on_error(error):
    print(f"Error: {error}")

if __name__ == "__main__":
    with Pool(4) as pool:
        # Success case
        pool.apply_async(task, args=(5,), callback=on_success, error_callback=on_error)
        
        # Error case
        pool.apply_async(task, args=(-1,), callback=on_success, error_callback=on_error)
        
        pool.close()
        pool.join()
```

---

## Pool Lifecycle

### Manual Management

```python
from multiprocessing import Pool

def task(x):
    return x ** 2

if __name__ == "__main__":
    pool = Pool(4)
    
    try:
        results = pool.map(task, range(10))
        print(results)
    finally:
        pool.close()  # No more tasks accepted
        pool.join()   # Wait for workers to finish
```

### Context Manager (Recommended)

```python
from multiprocessing import Pool

def task(x):
    return x ** 2

if __name__ == "__main__":
    with Pool(4) as pool:
        results = pool.map(task, range(10))
        print(results)
    # Pool automatically closed and joined
```

### terminate() vs close()

```python
from multiprocessing import Pool

def task(x):
    return x ** 2

if __name__ == "__main__":
    pool = Pool(4)
    
    # close(): No new tasks, wait for existing to finish
    pool.close()
    pool.join()
    
    # terminate(): Kill workers immediately
    pool2 = Pool(4)
    pool2.terminate()  # Don't wait for tasks
    pool2.join()
```

---

## Initializer Functions

Run setup code in each worker process:

```python
from multiprocessing import Pool
import os

# Global variable in worker processes
worker_data = None

def init_worker(shared_data):
    """Called once when each worker starts."""
    global worker_data
    worker_data = shared_data
    print(f"Worker {os.getpid()} initialized with {shared_data}")

def process_item(x):
    """Use initialized data."""
    return x * worker_data

if __name__ == "__main__":
    # Pass initializer and its arguments
    with Pool(4, initializer=init_worker, initargs=(10,)) as pool:
        results = pool.map(process_item, [1, 2, 3, 4, 5])
    
    print(results)  # [10, 20, 30, 40, 50]
```

### Database Connection per Worker

```python
from multiprocessing import Pool
import os

# Worker-local database connection
db_connection = None

def init_db():
    """Initialize database connection for this worker."""
    global db_connection
    db_connection = create_database_connection()
    print(f"Worker {os.getpid()}: DB connected")

def query(sql):
    """Use worker's database connection."""
    return db_connection.execute(sql)

if __name__ == "__main__":
    with Pool(4, initializer=init_db) as pool:
        queries = ["SELECT * FROM users", "SELECT * FROM orders"]
        results = pool.map(query, queries)
```

---

## Practical Examples

### Parallel File Processing

```python
from multiprocessing import Pool
from pathlib import Path

def process_file(filepath):
    """Process a single file."""
    content = Path(filepath).read_text()
    word_count = len(content.split())
    return (filepath, word_count)

if __name__ == "__main__":
    files = list(Path(".").glob("*.txt"))
    
    with Pool() as pool:
        results = pool.map(process_file, files)
    
    for filepath, count in results:
        print(f"{filepath}: {count} words")
```

### Parallel Image Processing

```python
from multiprocessing import Pool
from pathlib import Path
# from PIL import Image  # Uncomment if using PIL

def resize_image(args):
    """Resize a single image."""
    input_path, output_path, size = args
    # img = Image.open(input_path)
    # img = img.resize(size)
    # img.save(output_path)
    return f"Resized {input_path}"

if __name__ == "__main__":
    images = [
        ("img1.jpg", "out1.jpg", (100, 100)),
        ("img2.jpg", "out2.jpg", (100, 100)),
        ("img3.jpg", "out3.jpg", (100, 100)),
    ]
    
    with Pool() as pool:
        results = pool.map(resize_image, images)
    
    print(results)
```

### Parallel Web Scraping (I/O + CPU)

```python
from multiprocessing import Pool
import time

def fetch_and_parse(url):
    """Fetch URL and parse content."""
    # response = requests.get(url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # return len(soup.find_all('a'))
    time.sleep(0.5)  # Simulate
    return f"Parsed {url}"

if __name__ == "__main__":
    urls = [f"https://example.com/page{i}" for i in range(20)]
    
    with Pool(8) as pool:
        results = pool.map(fetch_and_parse, urls)
    
    print(results)
```

---

## Pool Method Summary

| Method | Blocking | Ordered | Use Case |
|--------|----------|---------|----------|
| `map()` | Yes | Yes | Simple parallel map |
| `starmap()` | Yes | Yes | Multiple arguments |
| `imap()` | Iterator | Yes | Memory efficient |
| `imap_unordered()` | Iterator | No | Fastest results first |
| `apply()` | Yes | N/A | Single function call |
| `apply_async()` | No | N/A | Async single call |
| `map_async()` | No | Yes | Async parallel map |

---

## Key Takeaways

- Use `Pool` for simple parallel function application
- `map()` is the most common method — parallel version of built-in `map()`
- `starmap()` for functions with multiple arguments
- `imap_unordered()` for best performance when order doesn't matter
- Use context manager (`with Pool() as pool:`) for automatic cleanup
- `initializer` sets up per-worker resources (database connections, etc.)
- Match pool size to CPU count for CPU-bound tasks
- Use `chunksize` to tune performance for large datasets

---

## Runnable Example: `pool_tutorial.py`

```python
"""
Topic 45.4 - Process Pools with multiprocessing.Pool

Complete guide to using process pools for efficient parallel task execution.
Pools manage a set of worker processes and distribute work automatically.

Learning Objectives:
- Create and use process pools
- Use map, imap, starmap for parallel execution
- Handle async operations with apply_async and map_async
- Manage pool lifecycle
- Error handling in pools
- Performance optimization

Author: Python Educator
Date: 2024
"""

import multiprocessing
from multiprocessing import Pool, cpu_count
import time
import random
import math


# ============================================================================
# PART 1: BEGINNER - Pool Basics and map()
# ============================================================================

def basic_pool_usage():
    """
    The simplest way to use a pool: map() a function over data.
    This is like built-in map() but runs in parallel across processes.
    """
    print("=" * 70)
    print("BEGINNER: Basic Pool with map()")
    print("=" * 70)
    
    def square(x):
        """
        Calculate square of a number.
        
        Args:
            x: Number to square
            
        Returns:
            Square of x
        """
        # Add delay to simulate real work
        time.sleep(0.1)
        return x ** 2
    
    # Input data
    numbers = list(range(10))
    
    print(f"\n📝 Input: {numbers}")
    print(f"   We want to square each number in parallel\n")
    
    # Method 1: Sequential (for comparison)
    print("⏱️  Sequential execution:")
    start = time.time()
    results_sequential = [square(x) for x in numbers]
    seq_time = time.time() - start
    print(f"   Time: {seq_time:.2f}s")
    print(f"   Results: {results_sequential}")
    
    # Method 2: Parallel with Pool
    print("\n⏱️  Parallel execution with Pool:")
    start = time.time()
    
    # Create a pool with 4 worker processes
    with Pool(processes=4) as pool:
        # Map the function over the data
        results_parallel = pool.map(square, numbers)
    
    parallel_time = time.time() - start
    print(f"   Time: {parallel_time:.2f}s")
    print(f"   Results: {results_parallel}")
    
    # Analysis
    print(f"\n📊 Speedup: {seq_time/parallel_time:.2f}x faster!")
    print(f"   4 workers can process multiple items simultaneously")
    
    print("\n💡 Pool.map() advantages:")
    print("   ✓ Automatic work distribution")
    print("   ✓ Process reuse (no startup overhead)")
    print("   ✓ Simple API (like built-in map)")
    print("   ✓ Handles all the complexity for you")
    
    print("\n" + "=" * 70 + "\n")


def pool_with_different_sizes():
    """
    Experiment with different pool sizes to find optimal performance.
    """
    print("=" * 70)
    print("BEGINNER: Choosing Pool Size")
    print("=" * 70)
    
    def cpu_task(x):
        """CPU-intensive task"""
        # Calculate factorial (CPU work)
        result = math.factorial(x % 15 + 5)
        time.sleep(0.05)  # Small delay
        return result % 1000
    
    numbers = list(range(40))
    
    print(f"\n🖥️  Your system has {cpu_count()} CPU cores")
    print(f"   Testing different pool sizes on {len(numbers)} tasks:\n")
    
    # Test different pool sizes
    for pool_size in [1, 2, 4, cpu_count(), cpu_count() * 2]:
        start = time.time()
        
        with Pool(processes=pool_size) as pool:
            results = pool.map(cpu_task, numbers)
        
        elapsed = time.time() - start
        print(f"   {pool_size:2d} processes: {elapsed:.3f}s")
    
    print("\n💡 Guidelines for pool size:")
    print("   • CPU-bound: pool_size = cpu_count()")
    print("   • I/O-bound: pool_size = cpu_count() * 2 or more")
    print("   • Mixed: Start with cpu_count() and experiment")
    print("   • Too many processes = overhead from context switching")
    
    print("\n" + "=" * 70 + "\n")


def pool_context_manager():
    """
    Demonstrate proper pool lifecycle management with context manager.
    """
    print("=" * 70)
    print("BEGINNER: Pool Lifecycle Management")
    print("=" * 70)
    
    def worker(x):
        """Simple worker function"""
        return x * 2
    
    print("\n📝 Recommended: Use context manager (with statement)")
    print("   with Pool(4) as pool:")
    print("       results = pool.map(worker, data)")
    print("   # Pool automatically closed and terminated")
    
    # Good practice: context manager
    with Pool(4) as pool:
        results = pool.map(worker, range(10))
        print(f"\n✓ Results: {results}")
    print("✓ Pool automatically cleaned up\n")
    
    print("📝 Alternative: Manual management")
    print("   pool = Pool(4)")
    print("   results = pool.map(worker, data)")
    print("   pool.close()  # No more tasks accepted")
    print("   pool.join()   # Wait for workers to finish")
    
    # Manual management (less preferred)
    pool = Pool(4)
    results = pool.map(worker, range(10, 20))
    print(f"\n✓ Results: {results}")
    pool.close()  # Stop accepting new tasks
    pool.join()   # Wait for completion
    print("✓ Pool manually cleaned up")
    
    print("\n💡 Best Practice:")
    print("   Always use 'with Pool() as pool:' for automatic cleanup")
    
    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 2: INTERMEDIATE - Advanced Mapping Functions
# ============================================================================

def pool_starmap_multiple_arguments():
    """
    Use starmap() when your function takes multiple arguments.
    starmap unpacks argument tuples for you.
    """
    print("=" * 70)
    print("INTERMEDIATE: starmap() for Multiple Arguments")
    print("=" * 70)
    
    def calculate_power(base, exponent):
        """
        Calculate base raised to exponent.
        
        Args:
            base: Base number
            exponent: Exponent
            
        Returns:
            base ** exponent
        """
        time.sleep(0.1)
        return base ** exponent
    
    # Data: list of (base, exponent) tuples
    tasks = [
        (2, 3),   # 2^3 = 8
        (3, 4),   # 3^4 = 81
        (5, 2),   # 5^2 = 25
        (10, 3),  # 10^3 = 1000
        (7, 2),   # 7^2 = 49
    ]
    
    print(f"\n📝 Tasks: {tasks}")
    print("   Each tuple is (base, exponent)\n")
    
    # Use starmap to unpack tuples
    with Pool(3) as pool:
        results = pool.starmap(calculate_power, tasks)
    
    print("📊 Results:")
    for (base, exp), result in zip(tasks, results):
        print(f"   {base}^{exp} = {result}")
    
    print("\n💡 starmap vs map:")
    print("   map(f, [x1, x2])     → f(x1), f(x2)")
    print("   starmap(f, [(a,b)])  → f(a, b)  # unpacks tuple")
    
    print("\n" + "=" * 70 + "\n")


def pool_imap_lazy_iteration():
    """
    Use imap() for lazy iteration over results.
    Unlike map(), imap() returns results as they complete.
    """
    print("=" * 70)
    print("INTERMEDIATE: imap() for Lazy Results")
    print("=" * 70)
    
    def slow_square(x):
        """Square with variable delay"""
        delay = random.uniform(0.5, 1.5)
        time.sleep(delay)
        return x ** 2, delay
    
    numbers = list(range(8))
    
    print(f"\n📝 Processing {len(numbers)} items with variable delays\n")
    
    # Method 1: map() - waits for ALL results
    print("⏱️  Using map() (blocks until all complete):")
    start = time.time()
    with Pool(4) as pool:
        results = pool.map(slow_square, numbers)
    elapsed = time.time() - start
    print(f"   Got all results after {elapsed:.2f}s")
    print(f"   Results: {[r[0] for r in results]}")
    
    # Method 2: imap() - yields results as they arrive
    print("\n⏱️  Using imap() (yields results incrementally):")
    start = time.time()
    with Pool(4) as pool:
        # imap returns an iterator
        for i, (result, delay) in enumerate(pool.imap(slow_square, numbers)):
            elapsed = time.time() - start
            print(f"   [{elapsed:.2f}s] Got result #{i}: {result} (took {delay:.2f}s)")
    
    print("\n💡 When to use imap():")
    print("   ✓ Process results as they complete")
    print("   ✓ Show progress updates")
    print("   ✓ Lower memory usage (streaming)")
    print("   ✓ Start processing early results while others compute")
    
    print("\n" + "=" * 70 + "\n")


def pool_imap_unordered():
    """
    Use imap_unordered() when result order doesn't matter.
    This can be faster as it returns results immediately.
    """
    print("=" * 70)
    print("INTERMEDIATE: imap_unordered() for Faster Results")
    print("=" * 70)
    
    def process_item(x):
        """Process with random delay"""
        delay = random.uniform(0.1, 1.0)
        time.sleep(delay)
        return x, delay
    
    numbers = list(range(12))
    
    print(f"\n📝 Processing {len(numbers)} items\n")
    
    # Ordered iteration
    print("⏱️  imap() - Maintains order:")
    with Pool(4) as pool:
        start = time.time()
        for i, (num, delay) in enumerate(pool.imap(process_item, numbers)):
            elapsed = time.time() - start
            print(f"   [{elapsed:.2f}s] Position {i}: item {num}")
    
    # Unordered iteration
    print("\n⏱️  imap_unordered() - Returns as completed:")
    with Pool(4) as pool:
        start = time.time()
        for i, (num, delay) in enumerate(pool.imap_unordered(process_item, numbers)):
            elapsed = time.time() - start
            print(f"   [{elapsed:.2f}s] Completed #{i}: item {num}")
    
    print("\n💡 imap_unordered() advantages:")
    print("   ✓ Faster - returns results immediately")
    print("   ✓ No waiting for slow tasks to maintain order")
    print("   ✓ Good for independent tasks")
    
    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 3: ADVANCED - Async Operations and Error Handling
# ============================================================================

def pool_apply_async():
    """
    Use apply_async() for single tasks with callbacks.
    More flexible than map, but requires manual result handling.
    """
    print("=" * 70)
    print("ADVANCED: apply_async() with Callbacks")
    print("=" * 70)
    
    def compute_factorial(n):
        """Compute factorial of n"""
        time.sleep(0.5)
        result = math.factorial(n)
        return n, result
    
    def success_callback(result):
        """Called when task completes successfully"""
        n, factorial = result
        print(f"   ✓ Success: {n}! = {factorial}")
    
    def error_callback(error):
        """Called when task raises exception"""
        print(f"   ✗ Error: {error}")
    
    print("\n⚙️  Submitting async tasks with callbacks:\n")
    
    with Pool(3) as pool:
        # Submit multiple async tasks
        async_results = []
        
        for n in [5, 10, 15, 20]:
            result = pool.apply_async(
                compute_factorial,
                args=(n,),
                callback=success_callback,
                error_callback=error_callback
            )
            async_results.append(result)
        
        # Wait for all tasks
        pool.close()
        pool.join()
    
    print("\n💡 apply_async() features:")
    print("   ✓ Submit individual tasks")
    print("   ✓ Callbacks for success/error")
    print("   ✓ Non-blocking submission")
    print("   ✓ Flexible task management")
    
    print("\n" + "=" * 70 + "\n")


def pool_map_async_with_progress():
    """
    Use map_async() for non-blocking batch operations with progress tracking.
    """
    print("=" * 70)
    print("ADVANCED: map_async() with Progress Tracking")
    print("=" * 70)
    
    def heavy_computation(x):
        """CPU-intensive task"""
        time.sleep(0.3)
        return x ** 3
    
    numbers = list(range(20))
    
    print(f"\n⚙️  Processing {len(numbers)} items asynchronously...\n")
    
    with Pool(4) as pool:
        # Submit all tasks at once (non-blocking)
        result = pool.map_async(heavy_computation, numbers)
        
        # Do other work while tasks execute
        while not result.ready():
            remaining = result._number_left
            print(f"   Tasks remaining: {remaining}")
            time.sleep(0.5)
        
        # Get final results (will wait if not ready)
        final_results = result.get()
    
    print(f"\n✓ All tasks completed!")
    print(f"   First 5 results: {final_results[:5]}")
    
    print("\n💡 map_async() advantages:")
    print("   ✓ Non-blocking submission")
    print("   ✓ Can check progress with ready()")
    print("   ✓ Can track remaining tasks")
    print("   ✓ Main thread free for other work")
    
    print("\n" + "=" * 70 + "\n")


def pool_error_handling():
    """
    Handle errors in pool tasks gracefully.
    """
    print("=" * 70)
    print("ADVANCED: Error Handling in Pools")
    print("=" * 70)
    
    def risky_division(args):
        """
        Division that might fail.
        
        Args:
            args: (numerator, denominator) tuple
            
        Returns:
            Result of division
            
        Raises:
            ZeroDivisionError: If denominator is 0
        """
        numerator, denominator = args
        time.sleep(0.1)
        
        # This will raise exception for denominator=0
        return numerator / denominator
    
    # Some operations will fail
    tasks = [
        (10, 2),   # OK: 5.0
        (20, 4),   # OK: 5.0
        (15, 0),   # ERROR: division by zero
        (30, 6),   # OK: 5.0
        (25, 0),   # ERROR: division by zero
    ]
    
    print("\n📝 Method 1: Let exceptions propagate (default)")
    try:
        with Pool(2) as pool:
            # This will raise exception when it encounters error
            results = pool.starmap(risky_division, tasks)
    except Exception as e:
        print(f"   ✗ Caught exception: {type(e).__name__}: {e}")
    
    print("\n📝 Method 2: Handle errors individually")
    
    def safe_division(args):
        """Wrap risky function with error handling"""
        try:
            return risky_division(args), None
        except Exception as e:
            return None, str(e)
    
    with Pool(2) as pool:
        results = pool.starmap(safe_division, tasks)
    
    print("\n📊 Results:")
    for (num, denom), (result, error) in zip(tasks, results):
        if error:
            print(f"   {num}/{denom}: ✗ Error: {error}")
        else:
            print(f"   {num}/{denom}: ✓ {result}")
    
    print("\n💡 Error handling strategies:")
    print("   1. Try-except around pool.map() - stops on first error")
    print("   2. Wrap worker in try-except - continue on errors")
    print("   3. Use error_callback in apply_async()")
    
    print("\n" + "=" * 70 + "\n")


def pool_chunksize_optimization():
    """
    Optimize performance with chunksize parameter.
    """
    print("=" * 70)
    print("ADVANCED: Chunksize Optimization")
    print("=" * 70)
    
    def quick_task(x):
        """Very quick task"""
        return x * 2
    
    # Many small tasks
    numbers = list(range(1000))
    
    print(f"\n⏱️  Processing {len(numbers)} quick tasks:")
    print("   Testing different chunksizes...\n")
    
    # Test different chunksizes
    for chunksize in [1, 10, 50, 100]:
        start = time.time()
        
        with Pool(4) as pool:
            results = pool.map(quick_task, numbers, chunksize=chunksize)
        
        elapsed = time.time() - start
        print(f"   Chunksize {chunksize:3d}: {elapsed:.4f}s")
    
    print("\n💡 Chunksize guidelines:")
    print("   • Default: chunksize = len(data) / (processes * 4)")
    print("   • Many quick tasks: larger chunksize (less overhead)")
    print("   • Few slow tasks: smaller chunksize (better distribution)")
    print("   • Experiment to find optimal value")
    
    print("\n" + "=" * 70 + "\n")


def real_world_example_image_processing():
    """
    Realistic example: Parallel image processing simulation.
    """
    print("=" * 70)
    print("ADVANCED: Real-World Example - Batch Processing")
    print("=" * 70)
    
    def process_image(image_id):
        """
        Simulate image processing.
        
        Args:
            image_id: Image identifier
            
        Returns:
            Processing result
        """
        # Simulate different processing times
        time.sleep(random.uniform(0.2, 0.8))
        
        # Simulate processing operations
        operations = ["resize", "filter", "compress"]
        
        return {
            'id': image_id,
            'operations': operations,
            'size_mb': random.uniform(1.0, 5.0),
            'status': 'success'
        }
    
    # Simulate 50 images to process
    image_ids = [f"IMG_{i:04d}" for i in range(50)]
    
    print(f"\n📷 Processing {len(image_ids)} images...\n")
    
    start = time.time()
    
    # Process with pool
    with Pool(cpu_count()) as pool:
        # Use imap_unordered for best performance
        results = list(pool.imap_unordered(
            process_image,
            image_ids,
            chunksize=5  # Process 5 images per worker at a time
        ))
    
    elapsed = time.time() - start
    
    # Statistics
    total_size = sum(r['size_mb'] for r in results)
    avg_size = total_size / len(results)
    
    print(f"✓ Processed {len(results)} images in {elapsed:.2f}s")
    print(f"  Total size: {total_size:.1f} MB")
    print(f"  Average size: {avg_size:.2f} MB")
    print(f"  Throughput: {len(results)/elapsed:.1f} images/sec")
    
    print("\n💡 This pattern works for:")
    print("   • Image/video processing")
    print("   • Data transformation")
    print("   • File conversion")
    print("   • API requests")
    print("   • Report generation")
    
    print("\n" + "=" * 70 + "\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run all pool demonstrations."""
    print("\n" + "=" * 70)
    print(" " * 20 + "PROCESS POOLS")
    print(" " * 15 + "multiprocessing.Pool Tutorial")
    print("=" * 70 + "\n")
    
    # Beginner level
    basic_pool_usage()
    pool_with_different_sizes()
    pool_context_manager()
    
    # Intermediate level
    pool_starmap_multiple_arguments()
    pool_imap_lazy_iteration()
    pool_imap_unordered()
    
    # Advanced level
    pool_apply_async()
    pool_map_async_with_progress()
    pool_error_handling()
    pool_chunksize_optimization()
    real_world_example_image_processing()
    
    print("\n" + "=" * 70)
    print("Process Pools Tutorial Complete!")
    print("=" * 70)
    print("\n💡 Key Takeaways:")
    print("1. Pool manages worker processes automatically")
    print("2. map() is simplest - like built-in map")
    print("3. starmap() for functions with multiple arguments")
    print("4. imap() yields results incrementally")
    print("5. imap_unordered() returns results faster")
    print("6. apply_async() for fine-grained control")
    print("7. Use chunksize to optimize performance")
    print("8. Always use context manager for cleanup")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    # IMPORTANT: This guard is required on Windows
    main()
```


---

## Runnable Example: `prime_validation_pool.py`

```python
"""
Prime Number Validation: Serial vs Multiprocessing Pool

This tutorial demonstrates how to use multiprocessing for CPU-bound tasks.

WHAT IS CPU-BOUND WORK?
Tasks that spend most time doing computation (not waiting for I/O).
Examples: prime checking, calculations, data processing, compression.

WHY MULTIPROCESSING HELPS:
- Python's GIL (Global Interpreter Lock) prevents true parallelism with threads
- Multiprocessing creates separate processes (each has own GIL)
- On multi-core CPUs, processes can run truly in parallel
- Can achieve near-linear speedup with N cores

THE TASK:
Check if large numbers are prime. This is computationally expensive:
- Even with optimization, checking a large number takes millions of divisions
- No I/O involved, so it's pure CPU work
- Perfect for multiprocessing!

TECHNIQUES:
1. Serial: Check primes one at a time in main process
2. Pool: Use multiprocessing.Pool to distribute work across cores

Learning Goals:
- Understand when multiprocessing is appropriate
- Learn to use multiprocessing.Pool
- See real speedup from parallelization
- Understand the overhead involved
"""

import math
import time
from multiprocessing import Pool, cpu_count

if __name__ == "__main__":


    print("=" * 70)
    print("PRIME VALIDATION: SERIAL vs MULTIPROCESSING")
    print("=" * 70)


    # ============ EXAMPLE 1: Understanding Prime Checking ============
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Understanding Prime Number Checking")
    print("=" * 70)

    print("""
    A prime number is only divisible by 1 and itself.

    NAIVE APPROACH: Check all numbers up to n
        Too slow! For n = 10^18, this would take forever.

    OPTIMIZED APPROACH (used here):
    1. If n is even, it's not prime (except 2)
    2. Only check odd divisors from 3 to sqrt(n)
    3. If no divisor found, n is prime

    WHY ONLY UP TO sqrt(n)?
    If n = a * b where a <= b, then a <= sqrt(n).
    So if n has a factor, we'll find one <= sqrt(n).

    Example: Is 97 prime?
    - sqrt(97) ≈ 9.8
    - Check: 97 % 3, 97 % 5, 97 % 7, 97 % 9
    - None divide evenly, so 97 is prime!

    Example: Is 99 prime?
    - sqrt(99) ≈ 9.9
    - Check: 99 % 3 = 0, so 99 = 3 * 33, not prime!

    Even with this optimization, checking large primes (15+ digits) takes
    significant CPU time. This is why it's good for demonstrating multiprocessing.
    """)


    # ============ EXAMPLE 2: Prime Checking Function ============
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Implement Prime Checking Function")
    print("=" * 70)

    def check_prime(n):
        """
        Check if n is a prime number.

        Algorithm:
        1. Even numbers (except 2) are not prime
        2. Check odd divisors from 3 to sqrt(n)
        3. Use step of 2 to skip even numbers

        This is CPU-bound work: pure computation, no I/O.

        Time complexity: O(sqrt(n))
        For n ~ 10^18, sqrt(n) ~ 10^9, so millions of checks.
        """
        if n % 2 == 0:
            return False

        # Only need to check up to sqrt(n)
        from_i = 3
        to_i = math.sqrt(n) + 1

        # Check odd numbers only (step by 2)
        for i in range(from_i, int(to_i), 2):
            if n % i == 0:
                return False

        return True


    # Test with some examples
    test_numbers = [
        (2, True),
        (97, True),
        (100, False),
        (10007, True),
    ]

    print("\nTesting check_prime():")
    for num, expected in test_numbers:
        result = check_prime(num)
        status = "PASS" if result == expected else "FAIL"
        print(f"  check_prime({num:6}) = {result:5} (expected {expected:5}) [{status}]")


    # ============ EXAMPLE 3: Expensive Test Numbers ============
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Test with Large Numbers")
    print("=" * 70)

    print("""
    We'll test with large numbers that take significant time to check.

    These are actual large primes and non-primes from cryptography:
    - Large primes are expensive to verify
    - Large composites are also expensive (must check many divisors before confirming)

    Expected checking times (on modern CPU):
    - 12-15 digit numbers: milliseconds
    - 18 digit numbers: seconds
    - 20+ digit numbers: tens of seconds
    """)

    # Test numbers - these are real cryptographic numbers
    test_cases = [
        ("trivial non-prime", 112272535095295),
        ("15-digit composite", 100109100129100369),
        ("15-digit composite 2", 100109100129101027),
        ("18-digit prime", 100109100129100151),
        ("18-digit prime 2", 100109100129162907),
    ]

    print(f"\nQuick validation on one number:")
    num, label = test_cases[0]
    print(f"  Testing {label}: {num}")
    start = time.time()
    is_prime = check_prime(num)
    elapsed = time.time() - start
    print(f"  Result: {is_prime} (checked in {elapsed:.4f}s)")


    # ============ EXAMPLE 4: Serial Processing ============
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Serial Processing (One at a time)")
    print("=" * 70)

    print("""
    Process each number one at a time in the main process.

    WHY IT'S SLOW:
    - CPU can only do one thing at a time
    - No parallelism at all
    - Wastes cores on multi-core machines

    Complexity:
    - 4 numbers, each taking 1-2 seconds
    - Total: ~4-8 seconds
    - Only using 1 of your N cores
    """)

    print(f"\nProcessing {len(test_cases)} numbers serially:")
    print(f"Current CPU count: {cpu_count()} cores\n")

    results_serial = []
    start_total = time.time()

    for label, number in test_cases:
        start = time.time()
        is_prime = check_prime(number)
        elapsed = time.time() - start
        results_serial.append((label, number, is_prime, elapsed))
        print(f"  {label:20} ({number}): {is_prime:5} ({elapsed:.4f}s)")

    elapsed_total_serial = time.time() - start_total
    print(f"\nTotal serial time: {elapsed_total_serial:.4f}s")
    print(f"Average per number: {elapsed_total_serial/len(test_cases):.4f}s")


    # ============ EXAMPLE 5: Multiprocessing Pool ============
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Multiprocessing Pool (Parallel)")
    print("=" * 70)

    print("""
    Use multiprocessing.Pool to distribute work across multiple processes.

    HOW IT WORKS:
    1. Create a Pool with N worker processes (default: CPU count)
    2. Submit jobs using pool.apply_async() or pool.map()
    3. Each worker process runs jobs in parallel
    4. Collect results

    WHY IT'S FASTER:
    - Each process runs on a separate CPU core
    - True parallelism (not limited by GIL)
    - Can check multiple numbers simultaneously
    - Speedup approximately = min(num_jobs, num_cores)

    OVERHEAD:
    - Creating processes takes time (~0.1s each)
    - Serializing data to pass to processes (pickling)
    - For small jobs, overhead might exceed speedup!
    - For large jobs, speedup dominates

    In this case:
    - Each job takes 1-2 seconds
    - Process creation overhead (~0.5s total) is small
    - Clear speedup expected
    """)

    print(f"\nProcessing {len(test_cases)} numbers with multiprocessing Pool:")

    start_total = time.time()

    # Create a Pool with default number of workers (CPU count)
    with Pool() as pool:
        # Use map() to apply check_prime to each number
        # Returns results in same order as input
        numbers = [num for label, num in test_cases]
        results_list = pool.map(check_prime, numbers)

    elapsed_total_parallel = time.time() - start_total

    # Print results
    for (label, number), is_prime in zip(test_cases, results_list):
        print(f"  {label:20} ({number}): {is_prime:5}")

    print(f"\nTotal parallel time: {elapsed_total_parallel:.4f}s")
    print(f"Average per number: {elapsed_total_parallel/len(test_cases):.4f}s")


    # ============ EXAMPLE 6: Performance Comparison ============
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Performance Comparison")
    print("=" * 70)

    speedup = elapsed_total_serial / elapsed_total_parallel
    num_cores = cpu_count()

    print(f"\nSpeedup Analysis:")
    print(f"  Serial time:     {elapsed_total_serial:.4f}s")
    print(f"  Parallel time:   {elapsed_total_parallel:.4f}s")
    print(f"  Speedup:         {speedup:.2f}x")
    print(f"  CPU cores:       {num_cores}")
    print(f"  Efficiency:      {speedup/num_cores*100:.1f}% (speedup / cores)")

    print(f"\nInterpretation:")
    if speedup > 1:
        print(f"  Multiprocessing is {speedup:.1f}x faster!")
        if speedup > num_cores * 0.8:
            print(f"  Good efficiency: Using cores well (>80%)")
        else:
            print(f"  Okay efficiency: Using cores okay (overhead present)")
    else:
        print(f"  Serial is faster (overhead > benefit)")
        print(f"  This can happen with small jobs or I/O-bound work")

    print(f"\n{'*' * 70}")
    print("WHEN MULTIPROCESSING HELPS")
    print("{'*' * 70}")

    print(f"""
    GOOD FOR MULTIPROCESSING:
    - CPU-bound tasks (pure computation)
    - Long-running jobs (seconds or more)
    - Many independent items to process
    - Available CPU cores to distribute to

    BAD FOR MULTIPROCESSING:
    - I/O-bound tasks (use threading or async instead)
    - Quick jobs (overhead > benefit)
    - Need to share mutable state
    - On single-core machines

    FOR THIS TASK (prime checking):
    - Job time: 1-2 seconds each (large numbers)
    - CPU-bound: Pure math, no I/O
    - Independent: Each number is independent
    - Result: Multiprocessing is clearly beneficial
    """)


    # ============ EXAMPLE 7: Advanced Pool Usage ============
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Advanced Pool Usage - apply_async()")
    print("=" * 70)

    print("""
    Different ways to use Pool:

    1. pool.map(func, iterable)
       - Apply func to each item
       - Blocks until all results ready
       - Returns list of results

    2. pool.apply_async(func, args)
       - Submit single job
       - Returns immediately with AsyncResult object
       - Get result later with .get()

    3. pool.imap(func, iterable)
       - Like map, but returns iterator
       - Results available as they complete

    For this example, map() is fine. For more complex scenarios,
    async methods let you submit jobs without waiting.
    """)

    print(f"\nDemonstration with apply_async():")

    start_total = time.time()

    with Pool() as pool:
        # Submit all jobs without waiting
        async_results = []
        for label, number in test_cases:
            async_result = pool.apply_async(check_prime, (number,))
            async_results.append((label, number, async_result))

        # Collect results as they complete
        print("Jobs submitted, waiting for results...\n")

        for label, number, async_result in async_results:
            is_prime = async_result.get()  # Blocks until this specific job completes
            print(f"  {label:20} ({number}): {is_prime:5}")

    elapsed_async = time.time() - start_total
    print(f"\nTotal time with async: {elapsed_async:.4f}s")


    # ============ EXAMPLE 8: Overhead Analysis ============
    print("\n" + "=" * 70)
    print("EXAMPLE 8: Understanding Multiprocessing Overhead")
    print("=" * 70)

    print("""
    Multiprocessing has overhead:

    1. PROCESS CREATION: ~0.1-0.2s per process
       - Creating processes is expensive
       - Pool reuses processes to amortize this

    2. PICKLING/SERIALIZATION: Time to send data to processes
       - Data must be converted to bytes and sent via IPC
       - Getting results back has same cost
       - Small data: negligible
       - Large data: can be significant

    3. CONTEXT SWITCHING: OS switching between processes
       - Not a huge factor on modern systems

    WHEN OVERHEAD DOMINATES:
    - Small jobs (microseconds)
    - Frequent small submissions
    - Large data to transfer

    WHEN SPEEDUP DOMINATES:
    - Long jobs (seconds+)
    - Batch submissions
    - Small data transfer

    FOR THIS TASK:
    - Process creation: ~0.5s total (5 processes, once at start)
    - Per-job overhead: Negligible (just int, bool transfer)
    - Job time: 1-2 seconds each
    - Result: Overhead is <20% of time, speedup dominates!
    """)


    print("\n" + "=" * 70)
    print("KEY TAKEAWAY")
    print("=" * 70)
    print(f"""
    Multiprocessing provides {speedup:.1f}x speedup for this CPU-bound task.

    USE MULTIPROCESSING WHEN:
    1. Task is CPU-bound (computation, not I/O)
    2. Jobs take significant time (seconds+)
    3. You have multiple cores available
    4. Data transfer overhead is small

    USE THREADING FOR:
    - I/O-bound tasks (network, disk, databases)
    - Quick tasks with frequent context switches

    USE ASYNCIO FOR:
    - I/O-bound tasks with many concurrent operations
    - Modern, efficient I/O multiplexing

    FOR PEAK PERFORMANCE:
    1. Profile to confirm it's worth optimizing
    2. Start with simple Pool.map() approach
    3. Use apply_async() for more control if needed
    4. Consider process count (default: CPU count)
    5. Measure actual speedup vs single-threaded baseline

    Remember: Don't optimize prematurely! Use multiprocessing
    only when profiling shows it's needed for CPU-bound work.
    """)
```

---

## Exercises

**Exercise 1.**
Use `Pool.map()` with 4 workers to compute the factorial of numbers 1 through 20. Print each result. Compare the wall-clock time of the pool version against the sequential `map(math.factorial, range(1, 21))`.

??? success "Solution to Exercise 1"
        ```python
        import math
        import time
        from multiprocessing import Pool

        if __name__ == "__main__":
            nums = list(range(1, 21))

            # Sequential
            start = time.perf_counter()
            seq = list(map(math.factorial, nums))
            seq_t = time.perf_counter() - start

            # Parallel
            start = time.perf_counter()
            with Pool(4) as pool:
                par = pool.map(math.factorial, nums)
            par_t = time.perf_counter() - start

            for n, f in zip(nums, par):
                print(f"{n}! = {f}")

            print(f"\nSequential: {seq_t:.4f}s")
            print(f"Pool:       {par_t:.4f}s")
        ```

---

**Exercise 2.**
Use `Pool.starmap()` to compute `base ** exponent` for 10 `(base, exponent)` pairs. Include a 0.2-second sleep in the worker to simulate heavy computation. Print each result and the total elapsed time.

??? success "Solution to Exercise 2"
        ```python
        import time
        from multiprocessing import Pool

        def power(base, exp):
            time.sleep(0.2)
            return base ** exp

        if __name__ == "__main__":
            pairs = [(2, 10), (3, 5), (5, 3), (7, 4), (10, 6),
                     (2, 20), (3, 10), (4, 8), (6, 5), (9, 3)]

            start = time.perf_counter()
            with Pool(4) as pool:
                results = pool.starmap(power, pairs)
            elapsed = time.perf_counter() - start

            for (b, e), r in zip(pairs, results):
                print(f"{b}^{e} = {r}")
            print(f"\nElapsed: {elapsed:.2f}s")
        ```

---

**Exercise 3.**
Write an error-tolerant pool pipeline. Define a `safe_divide(a, b)` function that returns `(result, None)` on success and `(None, error_message)` on failure. Use `Pool.starmap()` on a list of 10 `(a, b)` pairs where some have `b=0`. Print successes and failures separately, and report the count of each.

??? success "Solution to Exercise 3"
        ```python
        from multiprocessing import Pool

        def safe_divide(a, b):
            try:
                return (a / b, None)
            except ZeroDivisionError as e:
                return (None, str(e))

        if __name__ == "__main__":
            pairs = [(10, 2), (20, 0), (30, 5), (40, 0), (50, 10),
                     (60, 3), (70, 0), (80, 4), (90, 9), (100, 0)]

            with Pool(4) as pool:
                results = pool.starmap(safe_divide, pairs)

            successes = 0
            failures = 0
            for (a, b), (result, error) in zip(pairs, results):
                if error:
                    print(f"  {a}/{b}: FAIL — {error}")
                    failures += 1
                else:
                    print(f"  {a}/{b}: OK — {result}")
                    successes += 1

            print(f"\nSuccesses: {successes}, Failures: {failures}")
        ```
