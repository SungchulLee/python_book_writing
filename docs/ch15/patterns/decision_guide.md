# When to Use What

A practical guide for choosing the right concurrency approach in Python.

!!! tip "Mental Model"
    The decision boils down to two questions: Is the bottleneck CPU or I/O? And how many concurrent tasks do you need? CPU-bound work needs processes; moderate I/O-bound work is best served by a thread pool; and thousands of concurrent I/O connections call for asyncio. When in doubt, start with `concurrent.futures` -- it is the simplest on-ramp and lets you switch between threads and processes with a single line change.

---

## Quick Decision Flowchart

```
Start
  │
  ├─ Is your task CPU-intensive?
  │   │
  │   ├─ Yes ──────────────────────────► ProcessPoolExecutor
  │   │                                   (or multiprocessing.Pool)
  │   │
  │   └─ No (I/O-intensive or waiting)
  │       │
  │       ├─ Many concurrent connections (1000+)?
  │       │   │
  │       │   └─ Yes ──────────────────► asyncio
  │       │
  │       └─ Moderate concurrency (10-100)?
  │           │
  │           └─ Yes ──────────────────► ThreadPoolExecutor
  │                                      (or threading)
  │
  └─ Simple parallel map over data?
      │
      └─ Yes ──────────────────────────► concurrent.futures
                                          (easiest choice)
```

---

## Decision Matrix

| Task Type | Recommended Approach | Why |
|-----------|---------------------|-----|
| **CPU-bound computation** | `ProcessPoolExecutor` | Bypasses GIL, true parallelism |
| **File I/O** | `ThreadPoolExecutor` | GIL released during I/O |
| **Network requests** | `ThreadPoolExecutor` | GIL released during I/O |
| **Database queries** | `ThreadPoolExecutor` | GIL released during I/O |
| **Web scraping** | `ThreadPoolExecutor` | Mostly waiting for network |
| **Image processing** | `ProcessPoolExecutor` | CPU-intensive pixel operations |
| **Data transformation** | `ProcessPoolExecutor` | CPU-intensive computation |
| **API calls** | `ThreadPoolExecutor` | Network I/O dominant |
| **High-concurrency server** | `asyncio` | Handles thousands of connections |
| **Mixed I/O + CPU** | Both (pipeline) | Separate stages appropriately |

---

## Detailed Guidelines

### Use ThreadPoolExecutor When:

```python
from concurrent.futures import ThreadPoolExecutor

# ✅ Network requests
def fetch_url(url):
    return requests.get(url).text

with ThreadPoolExecutor(max_workers=20) as executor:
    results = executor.map(fetch_url, urls)

# ✅ File I/O
def read_file(path):
    return open(path).read()

with ThreadPoolExecutor(max_workers=10) as executor:
    contents = executor.map(read_file, file_paths)

# ✅ Database queries
def query_db(sql):
    return db.execute(sql)

with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(query_db, queries)
```

**Characteristics:**

- Task spends most time waiting (I/O)
- Low CPU usage per task
- Need shared memory/state
- Quick startup needed

### Use ProcessPoolExecutor When:

```python
from concurrent.futures import ProcessPoolExecutor

# ✅ Heavy computation
def compute(n):
    return sum(i**2 for i in range(n))

with ProcessPoolExecutor() as executor:
    results = executor.map(compute, large_numbers)

# ✅ Image/video processing
def process_image(image_path):
    img = load_image(image_path)
    return apply_filters(img)

with ProcessPoolExecutor() as executor:
    results = executor.map(process_image, image_paths)

# ✅ Data transformation
def transform(chunk):
    return chunk.apply(complex_operation)

with ProcessPoolExecutor() as executor:
    results = executor.map(transform, data_chunks)
```

**Characteristics:**

- Task is CPU-intensive
- High CPU usage per task
- Can tolerate memory copying overhead
- Objects are picklable

### Use asyncio When:

```python
import asyncio
import aiohttp

# ✅ Many concurrent connections
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

asyncio.run(main())
```

**Characteristics:**

- Very high concurrency (thousands)
- All I/O operations
- Need fine-grained control
- Single-threaded is acceptable

### Use Raw threading/multiprocessing When:

```python
import threading
from multiprocessing import Process, Queue

# ✅ Long-running background tasks
def background_worker():
    while True:
        process_queue()

thread = threading.Thread(target=background_worker, daemon=True)
thread.start()

# ✅ Need fine-grained control over processes
def worker(queue):
    while True:
        item = queue.get()
        if item is None:
            break
        process(item)

queue = Queue()
processes = [Process(target=worker, args=(queue,)) for _ in range(4)]
```

**Characteristics:**

- Need long-running workers
- Custom synchronization required
- Complex communication patterns
- Pool pattern doesn't fit

---

## Anti-Patterns to Avoid

### ❌ Threads for CPU-Bound Work

```python
# Bad: No speedup due to GIL
with ThreadPoolExecutor() as executor:
    results = executor.map(heavy_computation, data)

# Good: Use processes
with ProcessPoolExecutor() as executor:
    results = executor.map(heavy_computation, data)
```

### ❌ Processes for Quick I/O Tasks

```python
# Bad: Process overhead dominates
with ProcessPoolExecutor() as executor:
    results = executor.map(quick_api_call, urls)

# Good: Use threads
with ThreadPoolExecutor() as executor:
    results = executor.map(quick_api_call, urls)
```

### ❌ Too Many Workers

```python
# Bad: Resource waste
with ThreadPoolExecutor(max_workers=1000) as executor:
    ...

# Good: Match to workload
# I/O-bound: 10-50 threads typically sufficient
# CPU-bound: os.cpu_count() processes
```

### ❌ Shared Mutable State Without Locks

```python
# Bad: Race condition
results = []
def worker(x):
    results.append(x ** 2)  # Not thread-safe!

# Good: Use thread-safe structures
from queue import Queue
result_queue = Queue()
def worker(x):
    result_queue.put(x ** 2)
```

---

## Performance Comparison

### Benchmark Template

```python
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def benchmark(name, executor_class, func, data, workers=None):
    start = time.perf_counter()
    with executor_class(max_workers=workers) as executor:
        list(executor.map(func, data))
    elapsed = time.perf_counter() - start
    print(f"{name}: {elapsed:.2f}s")

# Test your specific workload
data = [...]

# Sequential baseline
start = time.perf_counter()
results = [func(x) for x in data]
print(f"Sequential: {time.perf_counter() - start:.2f}s")

# Threads
benchmark("Threads", ThreadPoolExecutor, func, data, workers=10)

# Processes
benchmark("Processes", ProcessPoolExecutor, func, data)
```

### Typical Results

| Workload | Sequential | Threads | Processes |
|----------|------------|---------|-----------|
| CPU-bound (4 items) | 4.0s | 4.2s ❌ | 1.1s ✅ |
| I/O-bound (4 items) | 4.0s | 1.1s ✅ | 1.2s |
| Mixed (4 items) | 4.0s | 2.5s | 1.5s ✅ |

---

## Choosing Worker Count

### ThreadPoolExecutor

```python
import os

# I/O-bound: more threads than CPUs
# Most time waiting, not computing
max_workers = 20  # or even 50-100 for pure I/O

# Mixed workload
max_workers = os.cpu_count() * 2

# Default (Python 3.8+)
# min(32, os.cpu_count() + 4)
```

### ProcessPoolExecutor

```python
import os

# CPU-bound: match CPU cores
max_workers = os.cpu_count()

# Leave headroom for system
max_workers = max(1, os.cpu_count() - 1)

# Default
# os.cpu_count()
```

---

## Summary Table

| Approach | Best For | GIL | Overhead | Memory |
|----------|----------|-----|----------|--------|
| `ThreadPoolExecutor` | I/O-bound | Blocked | Low | Shared |
| `ProcessPoolExecutor` | CPU-bound | Bypassed | High | Isolated |
| `asyncio` | High concurrency I/O | Blocked | Lowest | Shared |
| Raw `threading` | Custom thread control | Blocked | Low | Shared |
| Raw `multiprocessing` | Custom process control | Bypassed | High | Isolated |

---

## Key Takeaways

1. **I/O-bound** (network, files, database) → **Threads**
2. **CPU-bound** (computation, processing) → **Processes**
3. **Very high concurrency** (10,000+ connections) → **asyncio**
4. **Simple parallel map** → **concurrent.futures** (start here)
5. **Mixed workloads** → Pipeline with appropriate executor per stage
6. **When in doubt** → Start with `ThreadPoolExecutor`, measure, adjust
7. **Always measure** your specific workload before deciding

---

## Runnable Example: `decision_guide_tutorial.py`

```python
"""
Topic 45.6 - When to Use Threading vs Multiprocessing

Complete decision guide with practical examples and benchmarks to help
you choose the right concurrency approach for your specific use case.

Learning Objectives:
- Decision criteria for threading vs multiprocessing
- Performance characteristics of each approach
- Common use cases and patterns
- Hybrid approaches
- Real-world examples

Author: Python Educator
Date: 2024
"""

import threading
import multiprocessing
import time
import requests
import json
from queue import Queue
from multiprocessing import Pool, cpu_count


# ============================================================================
# PART 1: BEGINNER - Core Decision Criteria
# ============================================================================

def explain_core_differences():
    """
    Fundamental differences between threading and multiprocessing.
    """
    print("=" * 70)
    print("BEGINNER: Core Differences")
    print("=" * 70)
    
    print("\n" + "─" * 70)
    print("│ ASPECT              │ THREADING      │ MULTIPROCESSING  │")
    print("─" * 70)
    print("│ GIL Impact          │ Limited by GIL │ No GIL!          │")
    print("│ Memory              │ Shared         │ Separate copies  │")
    print("│ Startup Cost        │ Fast (~1ms)    │ Slow (~10-50ms)  │")
    print("│ Communication       │ Easy (shared)  │ IPC required     │")
    print("│ CPU-Bound Tasks     │ ❌ Bad         │ ✓ Excellent      │")
    print("│ I/O-Bound Tasks     │ ✓ Excellent    │ ✓ Good           │")
    print("│ Debugging           │ Easier         │ Harder           │")
    print("│ Resource Usage      │ Light          │ Heavy            │")
    print("─" * 70)
    
    print("\n📚 KEY RULE OF THUMB:")
    print("   • CPU-Bound (computation) → MULTIPROCESSING")
    print("   • I/O-Bound (waiting) → THREADING or ASYNCIO")
    
    print("\n💡 CPU-Bound Examples:")
    print("   - Mathematical calculations")
    print("   - Data processing and analysis")
    print("   - Image/video processing")
    print("   - Machine learning training")
    print("   - Compression/encryption")
    
    print("\n💡 I/O-Bound Examples:")
    print("   - Network requests (API calls)")
    print("   - File operations (read/write)")
    print("   - Database queries")
    print("   - Web scraping")
    print("   - User input waiting")
    
    print("\n" + "=" * 70 + "\n")


def cpu_bound_comparison():
    """
    Direct comparison: CPU-bound task with threading vs multiprocessing.
    """
    print("=" * 70)
    print("BEGINNER: CPU-Bound Task Comparison")
    print("=" * 70)
    
    def compute_fibonacci(n):
        """
        CPU-intensive recursive Fibonacci.
        
        Args:
            n: Fibonacci number to compute
            
        Returns:
            nth Fibonacci number
        """
        if n <= 1:
            return n
        return compute_fibonacci(n - 1) + compute_fibonacci(n - 2)
    
    numbers = [35, 35, 35, 35]  # 4 heavy computations
    
    # Sequential baseline
    print("\n⏱️  Sequential (baseline):")
    start = time.time()
    results_seq = [compute_fibonacci(n) for n in numbers]
    seq_time = time.time() - start
    print(f"   Time: {seq_time:.2f}s")
    
    # Threading (limited by GIL)
    print("\n⏱️  Threading (4 threads):")
    start = time.time()
    
    results_threading = []
    threads = []
    
    def worker(n, index, results):
        results[index] = compute_fibonacci(n)
    
    results_threading = [None] * len(numbers)
    for i, n in enumerate(numbers):
        thread = threading.Thread(target=worker, args=(n, i, results_threading))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    threading_time = time.time() - start
    print(f"   Time: {threading_time:.2f}s")
    print(f"   Speedup: {seq_time/threading_time:.2f}x")
    
    # Multiprocessing (true parallelism)
    print("\n⏱️  Multiprocessing (4 processes):")
    start = time.time()
    
    with Pool(4) as pool:
        results_mp = pool.map(compute_fibonacci, numbers)
    
    mp_time = time.time() - start
    print(f"   Time: {mp_time:.2f}s")
    print(f"   Speedup: {seq_time/mp_time:.2f}x")
    
    # Analysis
    print("\n📊 Summary:")
    print(f"   Sequential:      {seq_time:.2f}s (1.00x)")
    print(f"   Threading:       {threading_time:.2f}s ({seq_time/threading_time:.2f}x)")
    print(f"   Multiprocessing: {mp_time:.2f}s ({seq_time/mp_time:.2f}x)")
    
    print("\n✓ Winner: MULTIPROCESSING")
    print("   Threading showed minimal improvement due to GIL")
    print("   Multiprocessing achieved near-linear speedup")
    
    print("\n" + "=" * 70 + "\n")


def io_bound_comparison():
    """
    Direct comparison: I/O-bound task with threading vs multiprocessing.
    """
    print("=" * 70)
    print("BEGINNER: I/O-Bound Task Comparison")
    print("=" * 70)
    
    def simulate_io_operation(task_id):
        """
        Simulate I/O operation (network request, file read, etc).
        
        Args:
            task_id: Task identifier
            
        Returns:
            Task result
        """
        # Simulate I/O wait (GIL is released during sleep!)
        time.sleep(0.5)
        return f"Task {task_id} completed"
    
    task_ids = list(range(20))  # 20 I/O operations
    
    # Sequential baseline
    print("\n⏱️  Sequential (baseline):")
    start = time.time()
    results_seq = [simulate_io_operation(tid) for tid in task_ids]
    seq_time = time.time() - start
    print(f"   Time: {seq_time:.2f}s")
    
    # Threading
    print("\n⏱️  Threading (10 threads):")
    start = time.time()
    
    results_threading = []
    threads = []
    
    def worker(tid, results, lock):
        result = simulate_io_operation(tid)
        with lock:
            results.append(result)
    
    results_threading = []
    lock = threading.Lock()
    
    for tid in task_ids:
        thread = threading.Thread(target=worker, args=(tid, results_threading, lock))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    threading_time = time.time() - start
    print(f"   Time: {threading_time:.2f}s")
    print(f"   Speedup: {seq_time/threading_time:.2f}x")
    
    # Multiprocessing
    print("\n⏱️  Multiprocessing (10 processes):")
    start = time.time()
    
    with Pool(10) as pool:
        results_mp = pool.map(simulate_io_operation, task_ids)
    
    mp_time = time.time() - start
    print(f"   Time: {mp_time:.2f}s")
    print(f"   Speedup: {seq_time/mp_time:.2f}x")
    
    # Analysis
    print("\n📊 Summary:")
    print(f"   Sequential:      {seq_time:.2f}s (1.00x)")
    print(f"   Threading:       {threading_time:.2f}s ({seq_time/threading_time:.2f}x)")
    print(f"   Multiprocessing: {mp_time:.2f}s ({seq_time/mp_time:.2f}x)")
    
    print("\n✓ Winner: THREADING")
    print("   Both achieved similar speedup")
    print("   Threading has lower overhead and is preferred for I/O")
    
    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 2: INTERMEDIATE - Real-World Use Cases
# ============================================================================

def use_case_web_scraping():
    """
    Web scraping: I/O-bound → Use Threading
    """
    print("=" * 70)
    print("INTERMEDIATE: Use Case - Web Scraping")
    print("=" * 70)
    
    def fetch_url_simulation(url):
        """
        Simulate fetching URL content.
        
        Args:
            url: URL to fetch
            
        Returns:
            Simulated response
        """
        # Simulate network delay
        time.sleep(0.3)
        return {"url": url, "status": 200, "size": 1024}
    
    urls = [f"https://example.com/page{i}" for i in range(20)]
    
    print(f"\n📝 Task: Scrape {len(urls)} web pages")
    print("   Characteristic: I/O-bound (network requests)")
    print("   Recommendation: THREADING\n")
    
    # Threading approach
    print("⏱️  Using Threading:")
    start = time.time()
    
    results = []
    threads = []
    lock = threading.Lock()
    
    def fetch_worker(url):
        result = fetch_url_simulation(url)
        with lock:
            results.append(result)
    
    for url in urls:
        thread = threading.Thread(target=fetch_worker, args=(url,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    elapsed = time.time() - start
    
    print(f"   Fetched {len(results)} pages in {elapsed:.2f}s")
    print(f"   Throughput: {len(results)/elapsed:.1f} pages/sec")
    
    print("\n💡 Why Threading?")
    print("   ✓ Threads released GIL during network I/O")
    print("   ✓ Low overhead (can handle 100+ threads)")
    print("   ✓ Easy to share results")
    print("   ✗ Multiprocessing would add unnecessary overhead")
    
    print("\n" + "=" * 70 + "\n")


def use_case_image_processing():
    """
    Image processing: CPU-bound → Use Multiprocessing
    """
    print("=" * 70)
    print("INTERMEDIATE: Use Case - Image Processing")
    print("=" * 70)
    
    def process_image_simulation(image_id):
        """
        Simulate CPU-intensive image processing.
        
        Args:
            image_id: Image identifier
            
        Returns:
            Processed image info
        """
        # Simulate CPU-intensive operations
        total = 0
        for i in range(1_000_000):
            total += i ** 2
        
        return {
            "image_id": image_id,
            "processed": True,
            "checksum": total % 10000
        }
    
    image_ids = list(range(20))
    
    print(f"\n📝 Task: Process {len(image_ids)} images")
    print("   Operations: Resize, filter, compress (CPU-intensive)")
    print("   Recommendation: MULTIPROCESSING\n")
    
    # Multiprocessing approach
    print("⏱️  Using Multiprocessing:")
    start = time.time()
    
    with Pool(cpu_count()) as pool:
        results = pool.map(process_image_simulation, image_ids)
    
    elapsed = time.time() - start
    
    print(f"   Processed {len(results)} images in {elapsed:.2f}s")
    print(f"   Throughput: {len(results)/elapsed:.1f} images/sec")
    print(f"   Using {cpu_count()} CPU cores")
    
    print("\n💡 Why Multiprocessing?")
    print("   ✓ True parallel execution on multiple cores")
    print("   ✓ No GIL interference")
    print("   ✓ Scales with CPU count")
    print("   ✗ Threading would be serialized by GIL")
    
    print("\n" + "=" * 70 + "\n")


def use_case_database_operations():
    """
    Database operations: I/O-bound → Use Threading
    """
    print("=" * 70)
    print("INTERMEDIATE: Use Case - Database Operations")
    print("=" * 70)
    
    def execute_query_simulation(query_id):
        """
        Simulate database query execution.
        
        Args:
            query_id: Query identifier
            
        Returns:
            Query result
        """
        # Simulate database I/O
        time.sleep(0.2)
        return {
            "query_id": query_id,
            "rows": 100,
            "duration_ms": 200
        }
    
    queries = list(range(30))
    
    print(f"\n📝 Task: Execute {len(queries)} database queries")
    print("   Characteristic: I/O-bound (waiting for DB)")
    print("   Recommendation: THREADING\n")
    
    print("⏱️  Using Threading with connection pool:")
    start = time.time()
    
    # Simulate connection pool with 5 connections
    semaphore = threading.Semaphore(5)
    results = []
    threads = []
    lock = threading.Lock()
    
    def query_worker(qid):
        with semaphore:  # Limit concurrent connections
            result = execute_query_simulation(qid)
            with lock:
                results.append(result)
    
    for qid in queries:
        thread = threading.Thread(target=query_worker, args=(qid,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    elapsed = time.time() - start
    
    print(f"   Executed {len(results)} queries in {elapsed:.2f}s")
    print(f"   Throughput: {len(results)/elapsed:.1f} queries/sec")
    
    print("\n💡 Why Threading?")
    print("   ✓ Database I/O releases GIL")
    print("   ✓ Can use connection pool (Semaphore)")
    print("   ✓ Lower memory overhead")
    print("   ✓ Easier to manage shared state")
    
    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 3: ADVANCED - Hybrid Approaches and Edge Cases
# ============================================================================

def hybrid_approach_example():
    """
    Combine threading and multiprocessing for complex workloads.
    """
    print("=" * 70)
    print("ADVANCED: Hybrid Approach (Threading + Multiprocessing)")
    print("=" * 70)
    
    def fetch_data(url_id):
        """I/O-bound: Fetch data from network"""
        time.sleep(0.2)  # Network I/O
        return list(range(100))  # Simulated data
    
    def process_data(data):
        """CPU-bound: Process the fetched data"""
        # Heavy computation
        return sum(x ** 2 for x in data)
    
    num_tasks = 8
    
    print(f"\n📝 Task: Fetch data (I/O) then process it (CPU)")
    print(f"   {num_tasks} tasks total")
    print("   Strategy: Threading for I/O, then Multiprocessing for CPU\n")
    
    start = time.time()
    
    # Phase 1: Fetch data with threading
    print("⏱️  Phase 1: Fetching data with threading...")
    fetch_start = time.time()
    
    fetched_data = []
    threads = []
    lock = threading.Lock()
    
    def fetch_worker(url_id):
        data = fetch_data(url_id)
        with lock:
            fetched_data.append(data)
    
    for i in range(num_tasks):
        thread = threading.Thread(target=fetch_worker, args=(i,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    fetch_time = time.time() - fetch_start
    print(f"   Fetched {len(fetched_data)} datasets in {fetch_time:.2f}s")
    
    # Phase 2: Process data with multiprocessing
    print("\n⏱️  Phase 2: Processing data with multiprocessing...")
    process_start = time.time()
    
    with Pool(cpu_count()) as pool:
        results = pool.map(process_data, fetched_data)
    
    process_time = time.time() - process_start
    print(f"   Processed {len(results)} datasets in {process_time:.2f}s")
    
    total_time = time.time() - start
    
    print(f"\n📊 Performance:")
    print(f"   Fetch time:    {fetch_time:.2f}s (threading)")
    print(f"   Process time:  {process_time:.2f}s (multiprocessing)")
    print(f"   Total time:    {total_time:.2f}s")
    
    print("\n💡 Hybrid Approach Benefits:")
    print("   ✓ Use best tool for each phase")
    print("   ✓ Maximize resource utilization")
    print("   ✓ Common in data pipelines")
    print("   ✓ ETL workflows, ML pipelines")
    
    print("\n" + "=" * 70 + "\n")


def decision_flowchart():
    """
    Interactive decision flowchart for choosing approach.
    """
    print("=" * 70)
    print("ADVANCED: Decision Flowchart")
    print("=" * 70)
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║                  THREADING vs MULTIPROCESSING                  ║
║                        DECISION GUIDE                          ║
╚════════════════════════════════════════════════════════════════╝

START: What kind of task do you have?
  │
  ├─► CPU-Bound (computation, data processing)
  │     │
  │     ├─► Many independent tasks?
  │     │     YES → Use multiprocessing.Pool
  │     │     NO  → Use multiprocessing.Process
  │     │
  │     └─► Need shared state?
  │           Consider threading if updates are rare
  │           Otherwise use multiprocessing with Manager
  │
  └─► I/O-Bound (network, disk, database)
        │
        ├─► Simple parallel operations?
        │     YES → Use threading.Thread or ThreadPoolExecutor
        │
        ├─► High concurrency (100+ operations)?
        │     YES → Consider asyncio (async/await)
        │
        └─► Need blocking I/O with simple code?
              YES → Use threading

SPECIAL CASES:

• Mixed workload (I/O + CPU)
  → Hybrid: Threading for I/O, Multiprocessing for CPU

• Real-time requirements
  → Threading (lower latency)

• Memory constraints
  → Threading (shared memory)

• Need true parallelism + I/O
  → Multiprocessing

• Complex state management
  → Threading (easier synchronization)

• Maximum performance on multi-core
  → Multiprocessing (no GIL)

• Quick prototyping
  → Threading (simpler debugging)
""")
    
    print("=" * 70 + "\n")


def performance_characteristics_summary():
    """
    Comprehensive performance characteristics table.
    """
    print("=" * 70)
    print("ADVANCED: Performance Characteristics Summary")
    print("=" * 70)
    
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                    DETAILED COMPARISON TABLE                          ║
╚═══════════════════════════════════════════════════════════════════════╝

┌───────────────────┬────────────────────┬───────────────────────────┐
│ METRIC            │ THREADING          │ MULTIPROCESSING           │
├───────────────────┼────────────────────┼───────────────────────────┤
│ Startup Time      │ ~1 ms              │ ~10-50 ms (spawn)         │
│                   │                    │ ~2-5 ms (fork on Unix)    │
├───────────────────┼────────────────────┼───────────────────────────┤
│ Memory Overhead   │ ~50 KB per thread  │ ~10 MB per process        │
├───────────────────┼────────────────────┼───────────────────────────┤
│ Communication     │ Instant (shared)   │ Serialization overhead    │
│                   │                    │ (pickle + IPC)            │
├───────────────────┼────────────────────┼───────────────────────────┤
│ Max Workers       │ 100-1000+          │ Usually ≤ CPU count × 2   │
├───────────────────┼────────────────────┼───────────────────────────┤
│ CPU Usage         │ Limited by GIL     │ Full multi-core usage     │
│                   │ (one core max)     │                           │
├───────────────────┼────────────────────┼───────────────────────────┤
│ I/O Performance   │ Excellent          │ Good                      │
├───────────────────┼────────────────────┼───────────────────────────┤
│ CPU Performance   │ Poor (GIL)         │ Excellent                 │
├───────────────────┼────────────────────┼───────────────────────────┤
│ Debugging         │ Easier             │ Harder                    │
│                   │ (single process)   │ (multiple processes)      │
├───────────────────┼────────────────────┼───────────────────────────┤
│ Crash Impact      │ Crashes all        │ Isolated per process      │
└───────────────────┴────────────────────┴───────────────────────────┘

PERFORMANCE RANGES (approximate):

Threading Speedup:
  • CPU-bound:    1.0x - 1.2x  (GIL limited)
  • I/O-bound:    Nx (N = number of threads, up to 100+)

Multiprocessing Speedup:
  • CPU-bound:    Nx (N = CPU cores, near linear)
  • I/O-bound:    Nx (but higher overhead)

RECOMMENDATIONS BY TASK SIZE:

┌──────────────────────┬───────────────┬─────────────────────┐
│ Task Duration        │ Task Count    │ Best Choice         │
├──────────────────────┼───────────────┼─────────────────────┤
│ < 1ms (very quick)   │ Many          │ Sequential          │
│ 1-10ms               │ Many          │ Threading (chunked) │
│ 10-100ms             │ 10-100        │ Threading           │
│ > 100ms (I/O)        │ Any           │ Threading           │
│ > 100ms (CPU)        │ Any           │ Multiprocessing     │
│ > 1s (I/O)           │ Many          │ Async/Threading     │
│ > 1s (CPU)           │ Few           │ Multiprocessing     │
└──────────────────────┴───────────────┴─────────────────────┘
""")
    
    print("=" * 70 + "\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print(" " * 12 + "THREADING vs MULTIPROCESSING")
    print(" " * 20 + "Decision Guide")
    print("=" * 70 + "\n")
    
    # Beginner level
    explain_core_differences()
    cpu_bound_comparison()
    io_bound_comparison()
    
    # Intermediate level
    use_case_web_scraping()
    use_case_image_processing()
    use_case_database_operations()
    
    # Advanced level
    hybrid_approach_example()
    decision_flowchart()
    performance_characteristics_summary()
    
    print("\n" + "=" * 70)
    print("Decision Guide Complete!")
    print("=" * 70)
    print("\n💡 Quick Decision Rules:")
    print("1. CPU-intensive → Multiprocessing")
    print("2. I/O-intensive → Threading")
    print("3. Mixed workload → Hybrid approach")
    print("4. High concurrency I/O → asyncio")
    print("5. Simple tasks → ThreadPoolExecutor or Pool")
    print("6. When in doubt → Profile and measure!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
```

---

## Exercises

**Exercise 1.**
Write a benchmark that compares `ThreadPoolExecutor` and `ProcessPoolExecutor` on a CPU-bound task (sum of squares up to 5,000,000, repeated 4 times). Print the elapsed time for sequential, threaded, and process-based execution, along with the speedup ratios. Verify that processes outperform threads for this workload.

??? success "Solution to Exercise 1"
        ```python
        import time
        from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

        def cpu_task(n):
            return sum(i * i for i in range(n))

        data = [5_000_000] * 4

        # Sequential
        start = time.perf_counter()
        [cpu_task(n) for n in data]
        seq = time.perf_counter() - start

        # Threads
        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=4) as ex:
            list(ex.map(cpu_task, data))
        thr = time.perf_counter() - start

        # Processes
        start = time.perf_counter()
        with ProcessPoolExecutor(max_workers=4) as ex:
            list(ex.map(cpu_task, data))
        proc = time.perf_counter() - start

        print(f"Sequential: {seq:.2f}s (1.0x)")
        print(f"Threads:    {thr:.2f}s ({seq/thr:.2f}x)")
        print(f"Processes:  {proc:.2f}s ({seq/proc:.2f}x)")
        ```

---

**Exercise 2.**
Write a benchmark for an I/O-bound task: simulate 20 network requests (each `time.sleep(0.3)`). Compare sequential, `ThreadPoolExecutor(max_workers=10)`, and `ProcessPoolExecutor(max_workers=4)`. Print times and confirm threads are the best choice.

??? success "Solution to Exercise 2"
        ```python
        import time
        from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

        def io_task(task_id):
            time.sleep(0.3)
            return task_id

        data = list(range(20))

        start = time.perf_counter()
        [io_task(x) for x in data]
        seq = time.perf_counter() - start

        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=10) as ex:
            list(ex.map(io_task, data))
        thr = time.perf_counter() - start

        start = time.perf_counter()
        with ProcessPoolExecutor(max_workers=4) as ex:
            list(ex.map(io_task, data))
        proc = time.perf_counter() - start

        print(f"Sequential: {seq:.2f}s")
        print(f"Threads:    {thr:.2f}s ({seq/thr:.1f}x)")
        print(f"Processes:  {proc:.2f}s ({seq/proc:.1f}x)")
        ```

---

**Exercise 3.**
Implement a hybrid two-stage pipeline. Stage 1 (I/O-bound): use `ThreadPoolExecutor` to "fetch" 8 items (each `time.sleep(0.3)`). Stage 2 (CPU-bound): use `ProcessPoolExecutor` to process the fetched data (compute `sum(i*i for i in range(500_000))` per item). Print the time for each stage and the total.

??? success "Solution to Exercise 3"
        ```python
        import time
        from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

        def fetch(item_id):
            time.sleep(0.3)
            return item_id

        def process(item):
            return sum(i * i for i in range(500_000))

        if __name__ == "__main__":
            total_start = time.perf_counter()

            # Stage 1: I/O with threads
            start = time.perf_counter()
            with ThreadPoolExecutor(max_workers=8) as ex:
                fetched = list(ex.map(fetch, range(8)))
            stage1 = time.perf_counter() - start

            # Stage 2: CPU with processes
            start = time.perf_counter()
            with ProcessPoolExecutor() as ex:
                results = list(ex.map(process, fetched))
            stage2 = time.perf_counter() - start

            total = time.perf_counter() - total_start
            print(f"Stage 1 (I/O, threads):   {stage1:.2f}s")
            print(f"Stage 2 (CPU, processes): {stage2:.2f}s")
            print(f"Total:                    {total:.2f}s")
        ```
