# The Global Interpreter Lock (GIL)

The GIL is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecode simultaneously. Understanding the GIL is essential for effective concurrent programming in Python.

!!! tip "Mental Model"
    The GIL is a single microphone in a room full of speakers (threads). Only the thread holding the microphone can execute Python code; everyone else waits. This makes CPython's memory management safe but means threads cannot speed up CPU-heavy work. For true CPU parallelism, you must use separate processes, each with its own microphone.

---

## What is the GIL?

The **Global Interpreter Lock** is a lock that allows only one thread to execute Python bytecode at a time, even on multi-core systems.

```
Without GIL (hypothetical):
Thread 1: ████████████  (Core 1)
Thread 2: ████████████  (Core 2)
          Parallel execution

With GIL (CPython reality):
Thread 1: ██░░██░░██░░  (acquires GIL)
Thread 2: ░░██░░██░░██  (waits for GIL)
          Interleaved execution
```

---

## Why Does the GIL Exist?

### Memory Management Safety

CPython uses reference counting for memory management:

```python
import sys

a = []
print(sys.getrefcount(a))  # 2 (a + getrefcount's reference)

b = a
print(sys.getrefcount(a))  # 3

del b
print(sys.getrefcount(a))  # 2
```

Without the GIL, two threads could simultaneously modify reference counts, causing:
- Memory leaks (count never reaches 0)
- Use-after-free bugs (premature deallocation)

### Historical Simplicity

The GIL was introduced in Python's early days when:
- Multi-core processors were rare
- Single-threaded performance was priority
- C extensions needed simple integration

---

## GIL Impact Demonstration

### CPU-Bound: GIL Hurts Performance

```python
import time
import threading

def count(n):
    """CPU-bound task."""
    while n > 0:
        n -= 1

# Single-threaded
start = time.perf_counter()
count(100_000_000)
count(100_000_000)
single_time = time.perf_counter() - start
print(f"Single-threaded: {single_time:.2f}s")

# Multi-threaded (two threads)
start = time.perf_counter()
t1 = threading.Thread(target=count, args=(100_000_000,))
t2 = threading.Thread(target=count, args=(100_000_000,))
t1.start()
t2.start()
t1.join()
t2.join()
multi_time = time.perf_counter() - start
print(f"Multi-threaded: {multi_time:.2f}s")

# Results on 4-core machine:
# Single-threaded: 6.2s
# Multi-threaded:  6.5s  ← Slower due to GIL overhead!
```

### I/O-Bound: GIL Releases During I/O

```python
import time
import threading

def io_task(name):
    """I/O-bound task (simulated)."""
    print(f"{name} starting")
    time.sleep(2)  # GIL is released during sleep
    print(f"{name} done")

# Single-threaded
start = time.perf_counter()
io_task("Task 1")
io_task("Task 2")
single_time = time.perf_counter() - start
print(f"Single-threaded: {single_time:.2f}s")  # ~4 seconds

# Multi-threaded
start = time.perf_counter()
t1 = threading.Thread(target=io_task, args=("Task 1",))
t2 = threading.Thread(target=io_task, args=("Task 2",))
t1.start()
t2.start()
t1.join()
t2.join()
multi_time = time.perf_counter() - start
print(f"Multi-threaded: {multi_time:.2f}s")  # ~2 seconds ✓
```

---

## When is the GIL Released?

The GIL is released during:

| Operation | GIL Released? |
|-----------|---------------|
| `time.sleep()` | ✅ Yes |
| File I/O (`read`, `write`) | ✅ Yes |
| Network I/O (`socket`, `requests`) | ✅ Yes |
| NumPy array operations | ✅ Yes (C code) |
| Pure Python computation | ❌ No |
| Python object manipulation | ❌ No |

### C Extensions Can Release GIL

```c
// C extension code
Py_BEGIN_ALLOW_THREADS
// GIL released — can run in parallel
result = expensive_c_computation(data);
Py_END_ALLOW_THREADS
// GIL reacquired
```

This is why NumPy, SciPy, and other numerical libraries can achieve parallelism.

---

## Workarounds for the GIL

### 1. Use multiprocessing (Separate Processes)

Each process has its own Python interpreter and GIL:

```python
from multiprocessing import Pool

def cpu_bound(n):
    return sum(i * i for i in range(n))

# Each process has its own GIL — true parallelism
with Pool(4) as pool:
    results = pool.map(cpu_bound, [10_000_000] * 4)
```

### 2. Use ProcessPoolExecutor

```python
from concurrent.futures import ProcessPoolExecutor

def compute(n):
    return sum(i * i for i in range(n))

with ProcessPoolExecutor() as executor:
    results = list(executor.map(compute, [10_000_000] * 4))
```

### 3. Use NumPy/SciPy (Release GIL in C)

```python
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def numpy_operation(arr):
    # NumPy releases GIL during computation
    return np.sum(arr ** 2)

arrays = [np.random.rand(1_000_000) for _ in range(4)]

# Threads work because NumPy releases GIL
with ThreadPoolExecutor() as executor:
    results = list(executor.map(numpy_operation, arrays))
```

### 4. Use Cython with nogil

```cython
# mymodule.pyx
from cython.parallel import prange

def parallel_sum(double[:] arr):
    cdef double total = 0
    cdef int i
    
    with nogil:  # Release GIL
        for i in prange(len(arr)):
            total += arr[i]
    
    return total
```

### 5. Use Alternative Python Implementations

| Implementation | GIL? | Notes |
|----------------|------|-------|
| CPython | Yes | Standard Python |
| PyPy | Yes | Has GIL, but faster JIT |
| Jython | No | Runs on JVM |
| IronPython | No | Runs on .NET |
| GraalPy | No | Runs on GraalVM |

---

## GIL and Thread Safety

### GIL Does NOT Make Your Code Thread-Safe

The GIL prevents simultaneous bytecode execution, but compound operations are not atomic:

```python
import threading

counter = 0

def increment():
    global counter
    for _ in range(100_000):
        counter += 1  # Not atomic!
        # Bytecode:
        # 1. LOAD_GLOBAL counter
        # 2. LOAD_CONST 1
        # 3. BINARY_ADD
        # 4. STORE_GLOBAL counter
        # GIL can release between any of these!

threads = [threading.Thread(target=increment) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(counter)  # Often less than 1,000,000!
```

### Atomic Operations in Python

Some operations are atomic due to GIL:

```python
# Atomic (safe without locks)
L.append(x)          # Single bytecode
L.pop()              # Single bytecode
D[key] = value       # Single bytecode
x = L[i]             # Single bytecode

# NOT atomic (need locks)
counter += 1         # Multiple bytecodes
L[i] = L[i] + 1      # Multiple bytecodes
x = D.get(k, default)  # Multiple operations
```

### Always Use Proper Synchronization

```python
import threading

counter = 0
lock = threading.Lock()

def safe_increment():
    global counter
    for _ in range(100_000):
        with lock:
            counter += 1  # Now thread-safe

threads = [threading.Thread(target=safe_increment) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(counter)  # Always 1,000,000
```

---

## Future of the GIL

### PEP 703: Making the GIL Optional

Python 3.13+ introduces experimental GIL-free builds:

```bash
# Compile Python without GIL (experimental)
./configure --disable-gil
```

This is a work in progress and may take several Python versions to stabilize.

### Free-Threading Python

Future Python versions may offer:
- Optional GIL removal
- Per-interpreter GIL (subinterpreters)
- Better multicore support

---

## Summary: GIL Decision Guide

```
Is your code CPU-bound?
    │
    ├─ Yes
    │   │
    │   ├─ Can use NumPy/SciPy? → Threads OK (GIL released in C)
    │   │
    │   └─ Pure Python? → Use multiprocessing
    │
    └─ No (I/O-bound)
        │
        └─ Threads work fine (GIL released during I/O)
```

---

## Key Takeaways

- **GIL** allows only one thread to execute Python bytecode at a time
- **CPU-bound tasks**: GIL prevents parallel speedup with threads
- **I/O-bound tasks**: GIL is released during I/O, threads work well
- **Workarounds**: multiprocessing, NumPy, Cython, alternative implementations
- **GIL ≠ thread safety**: Still need locks for compound operations
- **Future**: GIL may become optional in Python 3.13+

---

## Runnable Example: `gil_tutorial.py`

```python
"""
Topic 45.1 - Global Interpreter Lock (GIL) Explanation

The GIL is one of the most important concepts to understand when doing
concurrent programming in Python. This script provides a comprehensive
explanation with practical demonstrations.

Learning Objectives:
- Understand what the GIL is and why it exists
- See the GIL's impact on multi-threaded programs
- Learn when the GIL matters and when it doesn't
- Understand GIL-free alternatives

Author: Python Educator
Date: 2024
"""

import threading
import multiprocessing
import time
import sys


# ============================================================================
# PART 1: BEGINNER - Understanding the GIL
# ============================================================================

def explain_gil_basics():
    """
    The Global Interpreter Lock (GIL) is a mutex (lock) that protects access
    to Python objects, preventing multiple threads from executing Python
    bytecode at the same time.
    
    Key points:
    1. Only ONE thread can execute Python code at a time
    2. The GIL exists to protect internal Python memory management
    3. It simplifies CPython's implementation (reference counting)
    4. It affects CPU-bound tasks but NOT I/O-bound tasks
    """
    print("=" * 70)
    print("BEGINNER: What is the GIL?")
    print("=" * 70)
    
    print("\n📚 GIL Definition:")
    print("The GIL is a global lock that allows only ONE thread to execute")
    print("Python bytecode at a time, even on multi-core processors.\n")
    
    print("🔍 Why does the GIL exist?")
    print("1. Memory Management: Python uses reference counting for garbage")
    print("   collection. The GIL protects reference counts from race conditions.")
    print("2. Simplicity: The GIL makes CPython's implementation simpler")
    print("3. C Extensions: Many C extensions were written assuming GIL")
    
    print("\n💡 When the GIL matters:")
    print("❌ CPU-bound tasks (heavy computation) - GIL LIMITS performance")
    print("✓ I/O-bound tasks (network, disk) - GIL has MINIMAL impact")
    
    print("\n" + "=" * 70 + "\n")


def demonstrate_gil_with_cpu_bound():
    """
    Demonstrate how the GIL limits CPU-bound multi-threaded performance.
    With the GIL, multiple threads cannot truly execute in parallel.
    """
    print("=" * 70)
    print("BEGINNER: GIL Impact on CPU-Bound Tasks")
    print("=" * 70)
    
    # CPU-intensive function
    def count_down(n):
        """Count down from n to 0 (pure computation)"""
        while n > 0:
            n -= 1
    
    # Test with single thread
    print("\n⏱️  Single thread (baseline):")
    start = time.time()
    count_down(10_000_000)  # 10 million iterations
    single_time = time.time() - start
    print(f"Time taken: {single_time:.3f} seconds")
    
    # Test with two threads (should be slower or same due to GIL!)
    print("\n⏱️  Two threads (competing for GIL):")
    start = time.time()
    
    # Create two threads
    thread1 = threading.Thread(target=count_down, args=(5_000_000,))
    thread2 = threading.Thread(target=count_down, args=(5_000_000,))
    
    # Start both threads
    thread1.start()
    thread2.start()
    
    # Wait for completion
    thread1.join()
    thread2.join()
    
    multi_time = time.time() - start
    print(f"Time taken: {multi_time:.3f} seconds")
    
    # Analysis
    print(f"\n📊 Performance Ratio: {multi_time/single_time:.2f}x")
    if multi_time > single_time * 0.9:  # Within 10% means no benefit
        print("❌ Threading DIDN'T speed up CPU-bound task!")
        print("   Reason: GIL prevents true parallel execution")
    else:
        print("✓ Some speedup (GIL was released occasionally)")
    
    print("\n" + "=" * 70 + "\n")


def demonstrate_gil_with_io_bound():
    """
    Demonstrate how I/O-bound tasks CAN benefit from threading despite GIL.
    When a thread waits for I/O, it releases the GIL for other threads.
    """
    print("=" * 70)
    print("BEGINNER: GIL Impact on I/O-Bound Tasks")
    print("=" * 70)
    
    # I/O-bound function (simulated with sleep)
    def download_file(file_num):
        """Simulate downloading a file (I/O operation)"""
        # time.sleep() releases the GIL!
        time.sleep(0.5)  # Simulate 0.5 second download
        return f"File {file_num} downloaded"
    
    # Test with sequential execution
    print("\n⏱️  Sequential downloads:")
    start = time.time()
    for i in range(4):
        download_file(i)
    sequential_time = time.time() - start
    print(f"Time taken: {sequential_time:.3f} seconds")
    
    # Test with multi-threading
    print("\n⏱️  Concurrent downloads (4 threads):")
    start = time.time()
    
    threads = []
    for i in range(4):
        thread = threading.Thread(target=download_file, args=(i,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads
    for thread in threads:
        thread.join()
    
    threaded_time = time.time() - start
    print(f"Time taken: {threaded_time:.3f} seconds")
    
    # Analysis
    print(f"\n📊 Speedup: {sequential_time/threaded_time:.2f}x faster!")
    print("✓ Threading DOES help with I/O-bound tasks")
    print("  Reason: Threads release GIL during I/O operations")
    
    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 2: INTERMEDIATE - GIL Release and Acquisition
# ============================================================================

def explain_gil_release_patterns():
    """
    The GIL is not held continuously. It's released in certain situations,
    allowing other threads to run.
    """
    print("=" * 70)
    print("INTERMEDIATE: When is the GIL Released?")
    print("=" * 70)
    
    print("\n🔓 GIL Release Scenarios:")
    print("1. I/O Operations:")
    print("   - File read/write")
    print("   - Network operations")
    print("   - time.sleep()")
    print("   - Blocking system calls")
    
    print("\n2. Long-running Operations:")
    print("   - NumPy operations (often GIL-free)")
    print("   - Some C extensions")
    
    print("\n3. Bytecode Evaluation:")
    print("   - Every 'check interval' (default: 100 bytecode instructions)")
    print("   - This allows thread switching even in pure Python code")
    
    print("\n4. Explicit Release:")
    print("   - C extensions can manually release GIL")
    
    print("\n" + "=" * 70 + "\n")


def demonstrate_gil_with_mixed_workload():
    """
    Show how mixing CPU and I/O work affects GIL behavior.
    """
    print("=" * 70)
    print("INTERMEDIATE: Mixed Workload (CPU + I/O)")
    print("=" * 70)
    
    results = []
    results_lock = threading.Lock()
    
    def mixed_worker(worker_id, compute_amount, io_amount):
        """
        Worker that does both computation and I/O.
        
        Args:
            worker_id: Worker identifier
            compute_amount: Amount of CPU work
            io_amount: Amount of I/O work (seconds)
        """
        # CPU-bound phase (holds GIL)
        count = 0
        for _ in range(compute_amount):
            count += 1
        
        # I/O-bound phase (releases GIL)
        time.sleep(io_amount)
        
        # Store result (thread-safe)
        with results_lock:
            results.append((worker_id, count))
    
    print("\n⏱️  Running 3 workers with mixed CPU/I/O work...")
    start = time.time()
    
    threads = []
    for i in range(3):
        # Each worker does some computation and some I/O
        thread = threading.Thread(
            target=mixed_worker,
            args=(i, 1_000_000, 0.5)  # 1M iterations + 0.5s I/O
        )
        threads.append(thread)
        thread.start()
    
    # Wait for completion
    for thread in threads:
        thread.join()
    
    elapsed = time.time() - start
    print(f"Time taken: {elapsed:.3f} seconds")
    print(f"Workers completed: {len(results)}")
    
    print("\n💡 Analysis:")
    print("Threading helps during I/O phases (GIL released)")
    print("But CPU phases are still serialized (GIL held)")
    print(f"Total I/O time: ~0.5s (done in parallel)")
    print(f"Total CPU time: ~{elapsed - 0.5:.2f}s (mostly serialized)")
    
    print("\n" + "=" * 70 + "\n")


def measure_gil_switching_overhead():
    """
    Demonstrate the overhead of GIL acquisition/release with many threads.
    """
    print("=" * 70)
    print("INTERMEDIATE: GIL Switching Overhead")
    print("=" * 70)
    
    def worker(n):
        """Simple worker that increments a counter"""
        for _ in range(n):
            pass  # Minimal work
    
    iterations = 1_000_000
    
    # Test with different numbers of threads
    for num_threads in [1, 2, 4, 8]:
        start = time.time()
        
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(
                target=worker,
                args=(iterations // num_threads,)
            )
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        elapsed = time.time() - start
        print(f"{num_threads} thread(s): {elapsed:.3f}s")
    
    print("\n📊 Observation:")
    print("More threads = more GIL contention = potentially slower!")
    print("The overhead of thread switching can outweigh benefits")
    
    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 3: ADVANCED - Working Around the GIL
# ============================================================================

def compare_threading_vs_multiprocessing():
    """
    Direct comparison: threading (with GIL) vs multiprocessing (no GIL).
    This clearly shows when to use each approach.
    """
    print("=" * 70)
    print("ADVANCED: Threading vs Multiprocessing Comparison")
    print("=" * 70)
    
    def cpu_intensive_task(n):
        """Pure CPU work - affected by GIL"""
        total = 0
        for i in range(n):
            total += i ** 2
        return total
    
    iterations = 5_000_000
    num_workers = 4
    
    # TEST 1: Threading (limited by GIL for CPU tasks)
    print(f"\n⏱️  Threading with {num_workers} threads:")
    start = time.time()
    
    threads = []
    for _ in range(num_workers):
        thread = threading.Thread(
            target=cpu_intensive_task,
            args=(iterations // num_workers,)
        )
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    threading_time = time.time() - start
    print(f"Time: {threading_time:.3f}s")
    
    # TEST 2: Multiprocessing (true parallelism, no GIL)
    print(f"\n⏱️  Multiprocessing with {num_workers} processes:")
    start = time.time()
    
    processes = []
    for _ in range(num_workers):
        process = multiprocessing.Process(
            target=cpu_intensive_task,
            args=(iterations // num_workers,)
        )
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
    
    multiproc_time = time.time() - start
    print(f"Time: {multiproc_time:.3f}s")
    
    # Analysis
    print("\n📊 Results:")
    print(f"Threading: {threading_time:.3f}s")
    print(f"Multiprocessing: {multiproc_time:.3f}s")
    print(f"Speedup: {threading_time/multiproc_time:.2f}x faster with multiprocessing!")
    
    print("\n💡 Conclusion:")
    print("For CPU-bound tasks, multiprocessing bypasses the GIL")
    print("and achieves true parallelism across multiple cores.")
    
    print("\n" + "=" * 70 + "\n")


def explain_gil_free_alternatives():
    """
    Explain alternatives and future directions for GIL-free Python.
    """
    print("=" * 70)
    print("ADVANCED: GIL-Free Alternatives")
    print("=" * 70)
    
    print("\n🔧 Current Solutions:")
    print("1. multiprocessing - Separate Python interpreters (no shared GIL)")
    print("2. NumPy/SciPy - Release GIL for vectorized operations")
    print("3. Cython - Write GIL-releasing code with 'nogil' context")
    print("4. C Extensions - Manually release GIL with Py_BEGIN_ALLOW_THREADS")
    
    print("\n🚀 Future Directions:")
    print("1. PEP 703 - Making the GIL Optional (Python 3.13+)")
    print("2. Subinterpreters - Isolated interpreters in same process")
    print("3. Alternative Python Implementations:")
    print("   - Jython (JVM-based) - no GIL")
    print("   - IronPython (.NET-based) - no GIL")
    print("   - PyPy - still has GIL but faster")
    
    print("\n📚 Best Practices:")
    print("✓ Use threading for I/O-bound tasks")
    print("✓ Use multiprocessing for CPU-bound tasks")
    print("✓ Use async/await for high-concurrency I/O")
    print("✓ Use NumPy for numerical computations")
    print("✓ Profile before optimizing - measure the actual bottleneck")
    
    print("\n" + "=" * 70 + "\n")


def advanced_gil_introspection():
    """
    Advanced: Introspect and monitor GIL behavior (Python 3.9+).
    """
    print("=" * 70)
    print("ADVANCED: GIL Introspection")
    print("=" * 70)
    
    # Get interpreter configuration
    print("\n⚙️  Python Implementation:")
    print(f"Implementation: {sys.implementation.name}")
    print(f"Version: {sys.version_info.major}.{sys.version_info.minor}")
    
    # Check GIL switch interval
    try:
        interval = sys.getswitchinterval()
        print(f"\n🔄 GIL Switch Interval: {interval} seconds")
        print(f"   (GIL can be released every {interval}s to allow thread switching)")
    except AttributeError:
        print("\n⚠️  sys.getswitchinterval() not available")
    
    # Thread info
    print(f"\n🧵 Active threads: {threading.active_count()}")
    print(f"Main thread: {threading.current_thread().name}")
    
    print("\n💡 Tips:")
    print("- Lower switch interval = more responsive but higher overhead")
    print("- Higher switch interval = better throughput but less responsive")
    print("- Default (0.005s) is usually optimal")
    
    print("\n" + "=" * 70 + "\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run all demonstrations in sequence."""
    print("\n" + "=" * 70)
    print(" " * 15 + "GLOBAL INTERPRETER LOCK (GIL)")
    print(" " * 20 + "Complete Tutorial")
    print("=" * 70 + "\n")
    
    # Beginner level
    explain_gil_basics()
    demonstrate_gil_with_cpu_bound()
    demonstrate_gil_with_io_bound()
    
    # Intermediate level
    explain_gil_release_patterns()
    demonstrate_gil_with_mixed_workload()
    measure_gil_switching_overhead()
    
    # Advanced level
    compare_threading_vs_multiprocessing()
    explain_gil_free_alternatives()
    advanced_gil_introspection()
    
    print("\n" + "=" * 70)
    print("GIL Tutorial Complete!")
    print("=" * 70)
    print("\n💡 Key Takeaways:")
    print("1. GIL limits CPU-bound multi-threaded performance")
    print("2. GIL has minimal impact on I/O-bound tasks")
    print("3. Use multiprocessing for CPU-intensive parallel work")
    print("4. Use threading for I/O-intensive concurrent work")
    print("5. The GIL is a CPython implementation detail")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    # Note: multiprocessing requires this guard on Windows
    main()
```

---

## Exercises

**Exercise 1.**
Write a program that starts 10 threads, each incrementing a shared global counter 100,000 times without a lock. Run it several times and observe that the final counter is less than 1,000,000. Then add a `threading.Lock` and verify the result is always exactly 1,000,000. Print the result for both versions.

??? success "Solution to Exercise 1"
        ```python
        import threading

        # Without lock
        counter = 0
        def increment_unsafe():
            global counter
            for _ in range(100_000):
                counter += 1

        threads = [threading.Thread(target=increment_unsafe) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        print(f"Without lock: {counter} (expected 1000000)")

        # With lock
        counter = 0
        lock = threading.Lock()
        def increment_safe():
            global counter
            for _ in range(100_000):
                with lock:
                    counter += 1

        threads = [threading.Thread(target=increment_safe) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        print(f"With lock: {counter} (expected 1000000)")
        ```

---

**Exercise 2.**
Demonstrate the GIL's impact by running a pure-Python countdown function (`while n > 0: n -= 1` starting from 50,000,000) in: (a) a single thread, and (b) two threads each counting down 25,000,000. Measure wall-clock time for both and print the results. Explain why the two-thread version is not faster.

??? success "Solution to Exercise 2"
        ```python
        import threading
        import time

        def countdown(n):
            while n > 0:
                n -= 1

        N = 50_000_000

        # Single thread
        start = time.perf_counter()
        countdown(N)
        single = time.perf_counter() - start

        # Two threads
        start = time.perf_counter()
        t1 = threading.Thread(target=countdown, args=(N // 2,))
        t2 = threading.Thread(target=countdown, args=(N // 2,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        multi = time.perf_counter() - start

        print(f"Single thread: {single:.2f}s")
        print(f"Two threads:   {multi:.2f}s")
        print("Two threads are not faster (may be slower) because the GIL "
              "prevents parallel execution of pure Python bytecode.")
        ```

---

**Exercise 3.**
Show that NumPy operations can achieve true thread-level parallelism despite the GIL. Create 4 large NumPy arrays (1,000,000 elements each) and compute `np.sum(arr ** 2)` for each using `ThreadPoolExecutor` with 4 workers. Compare the wall-clock time against a sequential loop. Print both times and the speedup factor.

??? success "Solution to Exercise 3"
        ```python
        import time
        import numpy as np
        from concurrent.futures import ThreadPoolExecutor

        def compute(arr):
            return np.sum(arr ** 2)

        arrays = [np.random.rand(1_000_000) for _ in range(4)]

        # Sequential
        start = time.perf_counter()
        seq_results = [compute(a) for a in arrays]
        seq_time = time.perf_counter() - start

        # Threaded
        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=4) as ex:
            thr_results = list(ex.map(compute, arrays))
        thr_time = time.perf_counter() - start

        print(f"Sequential: {seq_time:.4f}s")
        print(f"Threaded:   {thr_time:.4f}s")
        print(f"Speedup:    {seq_time / thr_time:.2f}x")
        print("NumPy releases the GIL during C-level computation, "
              "enabling true parallelism with threads.")
        ```
