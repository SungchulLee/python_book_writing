# Thread Basics

The `threading` module provides a way to run multiple threads (lightweight processes) within a single Python process.

!!! tip "Mental Model"
    A thread is a separate line of execution inside the same program, sharing all memory with the main thread. Creating one is like hiring an assistant who works at the same desk -- fast to start and can see all your files, but you need coordination to avoid stepping on each other. Use `start()` to launch, `join()` to wait for completion.

---

## Creating Threads

### Method 1: Using Thread with target Function

```python
import threading
import time

def worker(name, delay):
    """Function to run in a thread."""
    print(f"{name}: Starting")
    time.sleep(delay)
    print(f"{name}: Finished")

# Create thread
thread = threading.Thread(target=worker, args=("Thread-1", 2))

# Start thread
thread.start()

print("Main: Thread started")

# Wait for thread to complete
thread.join()

print("Main: Thread finished")
```

Output:
```
Thread-1: Starting
Main: Thread started
Thread-1: Finished
Main: Thread finished
```

### Method 2: Subclassing Thread

```python
import threading
import time

class WorkerThread(threading.Thread):
    def __init__(self, name, delay):
        super().__init__()
        self.name = name
        self.delay = delay
        self.result = None
    
    def run(self):
        """Override run() method."""
        print(f"{self.name}: Starting")
        time.sleep(self.delay)
        self.result = f"{self.name} completed"
        print(f"{self.name}: Finished")

# Create and start
thread = WorkerThread("Worker-1", 2)
thread.start()
thread.join()

print(f"Result: {thread.result}")
```

---

## Thread Lifecycle

```
                    ┌─────────┐
                    │ Created │
                    └────┬────┘
                         │ start()
                         ▼
                    ┌─────────┐
        ┌──────────│ Running │──────────┐
        │          └────┬────┘          │
        │               │               │
    wait/sleep      complete        exception
        │               │               │
        ▼               ▼               ▼
   ┌─────────┐    ┌──────────┐    ┌─────────┐
   │ Blocked │    │ Finished │    │ Finished│
   └────┬────┘    └──────────┘    └─────────┘
        │
    resume
        │
        └──────────► Running
```

### Thread States

```python
import threading
import time

def worker():
    time.sleep(1)

thread = threading.Thread(target=worker)

print(f"Created - is_alive: {thread.is_alive()}")  # False

thread.start()
print(f"Started - is_alive: {thread.is_alive()}")  # True

thread.join()
print(f"Joined - is_alive: {thread.is_alive()}")   # False
```

---

## Starting and Joining Threads

### start() — Begin Execution

```python
import threading

def task():
    print("Task running")

thread = threading.Thread(target=task)
thread.start()  # Returns immediately, thread runs in background

# Can only start a thread once
# thread.start()  # RuntimeError: threads can only be started once
```

### join() — Wait for Completion

```python
import threading
import time

def slow_task():
    time.sleep(2)
    print("Slow task done")

thread = threading.Thread(target=slow_task)
thread.start()

print("Waiting for thread...")
thread.join()  # Blocks until thread completes
print("Thread finished")

# With timeout
thread2 = threading.Thread(target=slow_task)
thread2.start()
thread2.join(timeout=1)  # Wait at most 1 second

if thread2.is_alive():
    print("Thread still running after timeout")
```

---

## Multiple Threads

### Creating Multiple Threads

```python
import threading
import time

def worker(worker_id):
    print(f"Worker {worker_id}: Starting")
    time.sleep(1)
    print(f"Worker {worker_id}: Done")

# Create threads
threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)

# Start all threads
for t in threads:
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()

print("All workers finished")
```

### Compact Pattern

```python
import threading

def worker(n):
    return n * 2

# Create, start, and collect threads
threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    t.start()
    threads.append(t)

# Wait for all
for t in threads:
    t.join()
```

---

## Thread Arguments

### Positional Arguments (args)

```python
import threading

def greet(name, greeting):
    print(f"{greeting}, {name}!")

# Pass as tuple
thread = threading.Thread(target=greet, args=("Alice", "Hello"))
thread.start()
thread.join()
```

### Keyword Arguments (kwargs)

```python
import threading

def greet(name, greeting="Hi"):
    print(f"{greeting}, {name}!")

# Pass as dict
thread = threading.Thread(target=greet, kwargs={"name": "Bob", "greeting": "Hey"})
thread.start()
thread.join()

# Mixed
thread = threading.Thread(target=greet, args=("Charlie",), kwargs={"greeting": "Howdy"})
thread.start()
thread.join()
```

---

## Getting Results from Threads

### Method 1: Shared Variable

```python
import threading

results = {}
lock = threading.Lock()

def compute(task_id, value):
    result = value ** 2
    with lock:
        results[task_id] = result

threads = []
for i in range(5):
    t = threading.Thread(target=compute, args=(i, i + 10))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print(results)  # {0: 100, 1: 121, 2: 144, 3: 169, 4: 196}
```

### Method 2: Thread-Safe Queue

```python
import threading
import queue

def compute(value, result_queue):
    result = value ** 2
    result_queue.put((value, result))

result_queue = queue.Queue()
threads = []

for i in range(5):
    t = threading.Thread(target=compute, args=(i, result_queue))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

# Collect results
results = []
while not result_queue.empty():
    results.append(result_queue.get())

print(results)
```

### Method 3: Thread Subclass with Attribute

```python
import threading

class ComputeThread(threading.Thread):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.result = None
    
    def run(self):
        self.result = self.value ** 2

threads = [ComputeThread(i) for i in range(5)]

for t in threads:
    t.start()

for t in threads:
    t.join()

results = [t.result for t in threads]
print(results)  # [0, 1, 4, 9, 16]
```

---

## Thread Properties

### Thread Name

```python
import threading

def worker():
    print(f"Running in: {threading.current_thread().name}")

# Auto-generated name
t1 = threading.Thread(target=worker)
t1.start()  # "Thread-1"

# Custom name
t2 = threading.Thread(target=worker, name="MyWorker")
t2.start()  # "MyWorker"
```

### Daemon Threads

Daemon threads are automatically killed when the main program exits:

```python
import threading
import time

def background_task():
    while True:
        print("Background running...")
        time.sleep(1)

# Non-daemon (default): program waits for thread
t1 = threading.Thread(target=background_task)
t1.daemon = False  # Default
# t1.start()  # Program would never exit!

# Daemon: thread killed when main exits
t2 = threading.Thread(target=background_task, daemon=True)
t2.start()

time.sleep(3)
print("Main exiting...")
# Daemon thread is killed here
```

### Current Thread Info

```python
import threading

def show_info():
    current = threading.current_thread()
    print(f"Name: {current.name}")
    print(f"Ident: {current.ident}")
    print(f"Native ID: {current.native_id}")
    print(f"Daemon: {current.daemon}")
    print(f"Is alive: {current.is_alive()}")

thread = threading.Thread(target=show_info, name="InfoThread")
thread.start()
thread.join()

# Main thread info
print(f"\nMain thread: {threading.main_thread().name}")
print(f"Active threads: {threading.active_count()}")
print(f"All threads: {threading.enumerate()}")
```

---

## Exception Handling

### Exceptions in Threads

Exceptions in threads don't propagate to the main thread:

```python
import threading
import time

def risky_task():
    time.sleep(0.5)
    raise ValueError("Something went wrong!")

thread = threading.Thread(target=risky_task)
thread.start()
thread.join()

print("Main continues...")  # This still runs!
# Exception is printed but not raised in main thread
```

### Catching Exceptions

```python
import threading
import traceback

class SafeThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exception = None
    
    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        except Exception as e:
            self.exception = e
            self.traceback = traceback.format_exc()

def risky_task():
    raise ValueError("Error!")

thread = SafeThread(target=risky_task)
thread.start()
thread.join()

if thread.exception:
    print(f"Thread raised: {thread.exception}")
    print(thread.traceback)
```

---

## Practical Example: Parallel Downloads

```python
import threading
import time
import random

def download_file(filename):
    """Simulate file download."""
    print(f"Downloading {filename}...")
    # Simulate varying download times
    time.sleep(random.uniform(0.5, 2.0))
    print(f"Completed {filename}")
    return f"{filename}: {random.randint(100, 1000)} bytes"

def download_sequential(files):
    """Download files one by one."""
    results = []
    for f in files:
        results.append(download_file(f))
    return results

def download_parallel(files):
    """Download files in parallel using threads."""
    results = []
    lock = threading.Lock()
    
    def download_and_store(filename):
        result = download_file(filename)
        with lock:
            results.append(result)
    
    threads = []
    for f in files:
        t = threading.Thread(target=download_and_store, args=(f,))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    return results

# Test
files = ["file1.zip", "file2.zip", "file3.zip", "file4.zip", "file5.zip"]

# Sequential
start = time.perf_counter()
download_sequential(files)
seq_time = time.perf_counter() - start
print(f"\nSequential: {seq_time:.2f}s")

# Parallel
start = time.perf_counter()
download_parallel(files)
par_time = time.perf_counter() - start
print(f"Parallel: {par_time:.2f}s")
print(f"Speedup: {seq_time/par_time:.1f}x")
```

---

## Key Takeaways

- Create threads with `threading.Thread(target=func, args=())`
- Call `start()` to begin execution, `join()` to wait for completion
- Threads share memory — use locks for safe access
- Get results via shared variables, queues, or thread subclass attributes
- Daemon threads are killed when main program exits
- Exceptions in threads don't propagate — handle them explicitly
- Best for I/O-bound tasks where GIL is released

---

## Runnable Example: `threading_basics_tutorial.py`

```python
"""
Topic 45.2 - Threading Basics with threading.Thread

Complete guide to Python's threading module, covering thread creation,
management, and basic patterns.

Learning Objectives:
- Create and start threads
- Pass arguments to threads
- Wait for thread completion (join)
- Daemon threads
- Thread naming and identification
- Thread-local storage

Author: Python Educator
Date: 2024
"""

import threading
import time
import random
from queue import Queue


# ============================================================================
# PART 1: BEGINNER - Creating and Starting Threads
# ============================================================================

def basic_thread_creation():
    """
    The most fundamental way to create a thread: using threading.Thread
    with a target function.
    """
    print("=" * 70)
    print("BEGINNER: Creating Your First Thread")
    print("=" * 70)
    
    def worker():
        """Simple function that will run in a separate thread"""
        print(f"  Worker thread started: {threading.current_thread().name}")
        time.sleep(1)  # Simulate some work
        print(f"  Worker thread finished: {threading.current_thread().name}")
    
    print("\n📝 Creating a thread:")
    print("   thread = threading.Thread(target=worker)")
    print("   thread.start()")
    
    # Create the thread
    thread = threading.Thread(target=worker)
    
    print(f"\nMain thread: {threading.current_thread().name}")
    print("Starting worker thread...")
    
    # Start the thread (begins execution)
    thread.start()
    
    print("Main thread continues while worker runs...")
    
    # Wait for the thread to complete
    thread.join()
    
    print("Worker thread has finished. Main thread exiting.\n")
    print("=" * 70 + "\n")


def threads_with_arguments():
    """
    Pass arguments to thread functions using args and kwargs.
    """
    print("=" * 70)
    print("BEGINNER: Passing Arguments to Threads")
    print("=" * 70)
    
    def greet(name, greeting="Hello"):
        """
        Function that takes arguments - will be run in a thread.
        
        Args:
            name: Person's name
            greeting: Greeting message (default: "Hello")
        """
        thread_name = threading.current_thread().name
        print(f"[{thread_name}] {greeting}, {name}!")
        time.sleep(0.5)
    
    print("\n📝 Method 1: Using args tuple")
    # Pass arguments as tuple
    thread1 = threading.Thread(target=greet, args=("Alice",))
    thread1.start()
    thread1.join()
    
    print("\n📝 Method 2: Using kwargs dictionary")
    # Pass arguments as keyword arguments
    thread2 = threading.Thread(
        target=greet,
        kwargs={"name": "Bob", "greeting": "Hi"}
    )
    thread2.start()
    thread2.join()
    
    print("\n📝 Method 3: Both args and kwargs")
    # Mix positional and keyword arguments
    thread3 = threading.Thread(
        target=greet,
        args=("Charlie",),
        kwargs={"greeting": "Hey"}
    )
    thread3.start()
    thread3.join()
    
    print("\n" + "=" * 70 + "\n")


def multiple_threads_example():
    """
    Create and manage multiple threads simultaneously.
    """
    print("=" * 70)
    print("BEGINNER: Running Multiple Threads")
    print("=" * 70)
    
    def download_file(file_id, duration):
        """
        Simulate downloading a file.
        
        Args:
            file_id: File identifier
            duration: Download duration in seconds
        """
        thread = threading.current_thread().name
        print(f"[{thread}] Starting download of file {file_id}")
        time.sleep(duration)  # Simulate download time
        print(f"[{thread}] Completed download of file {file_id}")
    
    print("\n⏱️  Downloading 5 files concurrently...\n")
    start_time = time.time()
    
    # Create multiple threads
    threads = []
    for i in range(5):
        # Each download takes 1-2 seconds
        duration = random.uniform(1.0, 2.0)
        
        thread = threading.Thread(
            target=download_file,
            args=(i, duration),
            name=f"Downloader-{i}"  # Give thread a meaningful name
        )
        threads.append(thread)
        thread.start()  # Start immediately
    
    # Wait for all threads to complete
    print("Main thread waiting for all downloads to complete...")
    for thread in threads:
        thread.join()  # Block until this thread finishes
    
    elapsed = time.time() - start_time
    print(f"\n✓ All downloads completed in {elapsed:.2f} seconds")
    print("  (Sequential would have taken ~7.5 seconds)")
    
    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 2: INTERMEDIATE - Thread Management and Control
# ============================================================================

def daemon_threads_explained():
    """
    Daemon threads are background threads that don't prevent program exit.
    They're useful for background tasks that should stop when main exits.
    """
    print("=" * 70)
    print("INTERMEDIATE: Daemon Threads")
    print("=" * 70)
    
    def background_task(task_id):
        """
        Background task that runs indefinitely.
        
        Args:
            task_id: Task identifier
        """
        try:
            while True:
                print(f"  Background task {task_id} is running...")
                time.sleep(1)
        except Exception as e:
            print(f"  Task {task_id} interrupted: {e}")
    
    print("\n📝 Normal (Non-Daemon) Thread:")
    print("   Keeps program alive until it completes\n")
    
    # Create a normal thread (daemon=False is default)
    normal_thread = threading.Thread(
        target=lambda: print("  Normal thread: I'll complete my work"),
        daemon=False
    )
    normal_thread.start()
    normal_thread.join()  # Wait for it
    print("  ✓ Normal thread completed\n")
    
    print("📝 Daemon Thread:")
    print("   Automatically stops when main program exits\n")
    
    # Create a daemon thread
    daemon_thread = threading.Thread(
        target=background_task,
        args=(1,),
        daemon=True  # This makes it a daemon thread
    )
    
    print("  Starting daemon thread...")
    daemon_thread.start()
    
    # Let it run for a bit
    time.sleep(2.5)
    
    print("\n  Main thread exiting (daemon will stop automatically)")
    print("  Notice: daemon thread doesn't prevent program exit")
    
    print("\n💡 Use Cases for Daemon Threads:")
    print("  ✓ Background monitoring")
    print("  ✓ Periodic cleanup tasks")
    print("  ✓ Logging/metrics collection")
    print("  ✓ Keep-alive connections")
    
    print("\n" + "=" * 70 + "\n")


def thread_properties_and_methods():
    """
    Explore thread properties: name, ident, daemon status, alive status.
    """
    print("=" * 70)
    print("INTERMEDIATE: Thread Properties and Methods")
    print("=" * 70)
    
    def worker(duration):
        """Worker that sleeps for specified duration"""
        time.sleep(duration)
    
    # Create a thread
    thread = threading.Thread(
        target=worker,
        args=(2,),
        name="MyWorkerThread"
    )
    
    print("\n📊 Before Starting:")
    print(f"  Name: {thread.name}")
    print(f"  Daemon: {thread.daemon}")
    print(f"  Is alive: {thread.is_alive()}")
    print(f"  Ident: {thread.ident}")  # None until started
    
    # Start the thread
    thread.start()
    
    print("\n📊 After Starting:")
    print(f"  Name: {thread.name}")
    print(f"  Daemon: {thread.daemon}")
    print(f"  Is alive: {thread.is_alive()}")
    print(f"  Ident: {thread.ident}")  # Now has an ID
    
    # Wait for completion
    thread.join()
    
    print("\n📊 After Completion:")
    print(f"  Is alive: {thread.is_alive()}")
    print(f"  Ident: {thread.ident}")  # Still has ID
    
    # Current thread info
    print("\n📊 Current (Main) Thread:")
    current = threading.current_thread()
    print(f"  Name: {current.name}")
    print(f"  Ident: {current.ident}")
    
    # All active threads
    print("\n📊 All Active Threads:")
    for t in threading.enumerate():
        print(f"  - {t.name} (daemon={t.daemon}, alive={t.is_alive()})")
    
    print("\n" + "=" * 70 + "\n")


def thread_joining_patterns():
    """
    Different patterns for waiting on threads with join().
    """
    print("=" * 70)
    print("INTERMEDIATE: Thread Joining Patterns")
    print("=" * 70)
    
    def task(task_id, duration):
        """Task that takes specified time to complete"""
        print(f"  Task {task_id} started")
        time.sleep(duration)
        print(f"  Task {task_id} completed")
    
    # Pattern 1: Join with timeout
    print("\n📝 Pattern 1: Join with Timeout")
    thread = threading.Thread(target=task, args=(1, 2))
    thread.start()
    
    print("  Waiting up to 1 second...")
    thread.join(timeout=1.0)  # Wait max 1 second
    
    if thread.is_alive():
        print("  ⏱️  Timeout! Thread still running")
        print("  Continuing without waiting...")
        thread.join()  # Wait for actual completion
    
    # Pattern 2: Join all threads
    print("\n📝 Pattern 2: Join All Threads")
    threads = []
    for i in range(3):
        t = threading.Thread(target=task, args=(i+2, 1))
        threads.append(t)
        t.start()
    
    print("  Waiting for all threads...")
    for t in threads:
        t.join()
    print("  ✓ All threads completed")
    
    # Pattern 3: Non-blocking check
    print("\n📝 Pattern 3: Non-blocking Status Check")
    thread = threading.Thread(target=task, args=(5, 1.5))
    thread.start()
    
    while thread.is_alive():
        print("  Thread still running, doing other work...")
        time.sleep(0.5)
    
    print("  ✓ Thread finished")
    
    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 3: ADVANCED - Thread Classes and Local Storage
# ============================================================================

class WorkerThread(threading.Thread):
    """
    Advanced: Custom thread class by inheriting from threading.Thread.
    Override run() method to define thread behavior.
    """
    
    def __init__(self, task_name, iterations):
        """
        Initialize the custom thread.
        
        Args:
            task_name: Name of the task
            iterations: Number of iterations to perform
        """
        # IMPORTANT: Call parent __init__
        super().__init__()
        
        # Store instance variables
        self.task_name = task_name
        self.iterations = iterations
        self.result = None
    
    def run(self):
        """
        This method is called when start() is invoked.
        Override this to define what the thread does.
        """
        print(f"[{self.name}] Starting task: {self.task_name}")
        
        # Perform work
        total = 0
        for i in range(self.iterations):
            total += i
            if i % 100000 == 0:
                time.sleep(0.01)  # Simulate some I/O
        
        # Store result
        self.result = total
        
        print(f"[{self.name}] Completed task: {self.task_name}")
        print(f"[{self.name}] Result: {self.result}")


def custom_thread_class_example():
    """
    Demonstrate using a custom thread class.
    """
    print("=" * 70)
    print("ADVANCED: Custom Thread Class")
    print("=" * 70)
    
    print("\n📝 Creating custom thread instances:\n")
    
    # Create thread instances
    thread1 = WorkerThread("Calculate-A", 500000)
    thread2 = WorkerThread("Calculate-B", 300000)
    
    # Give them custom names
    thread1.name = "Calculator-1"
    thread2.name = "Calculator-2"
    
    # Start them
    thread1.start()
    thread2.start()
    
    # Wait for completion
    thread1.join()
    thread2.join()
    
    # Access results
    print(f"\n📊 Results:")
    print(f"  Thread 1 result: {thread1.result}")
    print(f"  Thread 2 result: {thread2.result}")
    
    print("\n💡 Benefits of Custom Thread Class:")
    print("  ✓ Encapsulate thread logic")
    print("  ✓ Store thread-specific data")
    print("  ✓ Easier to access results")
    print("  ✓ More object-oriented design")
    
    print("\n" + "=" * 70 + "\n")


def thread_local_storage_example():
    """
    Thread-local storage: Each thread gets its own copy of data.
    Useful for storing per-thread state without passing it around.
    """
    print("=" * 70)
    print("ADVANCED: Thread-Local Storage")
    print("=" * 70)
    
    # Create thread-local storage
    thread_local = threading.local()
    
    def worker(worker_id):
        """
        Each thread stores its own data in thread_local.
        
        Args:
            worker_id: Worker identifier
        """
        # Store thread-specific data
        thread_local.worker_id = worker_id
        thread_local.counter = 0
        thread_local.name = f"Worker-{worker_id}"
        
        print(f"[{thread_local.name}] Starting work")
        
        # Do some work
        for i in range(5):
            thread_local.counter += 1
            time.sleep(0.1)
            print(f"[{thread_local.name}] Counter: {thread_local.counter}")
        
        # Access thread-specific data
        print(f"[{thread_local.name}] Final state:")
        print(f"  Worker ID: {thread_local.worker_id}")
        print(f"  Counter: {thread_local.counter}")
    
    print("\n📝 Starting threads with thread-local storage:\n")
    
    threads = []
    for i in range(3):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()
    
    # Wait for all
    for thread in threads:
        thread.join()
    
    print("\n💡 Key Points:")
    print("  • Each thread has its own copy of thread_local data")
    print("  • No need for locks when accessing thread_local")
    print("  • Data automatically cleaned up when thread exits")
    print("  • Useful for database connections, request contexts, etc.")
    
    print("\n" + "=" * 70 + "\n")


def producer_consumer_basic():
    """
    Advanced pattern: Basic producer-consumer using threads.
    One thread produces items, another consumes them.
    """
    print("=" * 70)
    print("ADVANCED: Producer-Consumer Pattern")
    print("=" * 70)
    
    # Shared queue (thread-safe)
    queue = Queue(maxsize=5)
    
    def producer(num_items):
        """
        Produce items and put them in the queue.
        
        Args:
            num_items: Number of items to produce
        """
        for i in range(num_items):
            item = f"Item-{i}"
            print(f"Producer: Creating {item}")
            queue.put(item)  # Thread-safe put
            time.sleep(0.5)  # Simulate production time
        
        # Signal completion
        queue.put(None)  # Sentinel value
        print("Producer: Finished producing")
    
    def consumer():
        """
        Consume items from the queue until None is received.
        """
        while True:
            item = queue.get()  # Thread-safe get (blocks if empty)
            
            if item is None:
                print("Consumer: Received stop signal")
                break
            
            print(f"Consumer: Processing {item}")
            time.sleep(0.8)  # Simulate processing time
            queue.task_done()  # Mark as processed
        
        print("Consumer: Finished consuming")
    
    print("\n⚙️  Starting producer-consumer system:\n")
    
    # Create threads
    producer_thread = threading.Thread(target=producer, args=(8,))
    consumer_thread = threading.Thread(target=consumer)
    
    # Start both
    producer_thread.start()
    consumer_thread.start()
    
    # Wait for completion
    producer_thread.join()
    consumer_thread.join()
    
    print("\n✓ Producer-consumer completed")
    
    print("\n💡 This pattern is useful for:")
    print("  • Decoupling production and consumption rates")
    print("  • Buffering between fast and slow operations")
    print("  • Load balancing across multiple workers")
    
    print("\n" + "=" * 70 + "\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run all threading demonstrations."""
    print("\n" + "=" * 70)
    print(" " * 20 + "THREADING BASICS")
    print(" " * 15 + "threading.Thread Tutorial")
    print("=" * 70 + "\n")
    
    # Beginner level
    basic_thread_creation()
    threads_with_arguments()
    multiple_threads_example()
    
    # Intermediate level
    daemon_threads_explained()
    thread_properties_and_methods()
    thread_joining_patterns()
    
    # Advanced level
    custom_thread_class_example()
    thread_local_storage_example()
    producer_consumer_basic()
    
    print("\n" + "=" * 70)
    print("Threading Basics Tutorial Complete!")
    print("=" * 70)
    print("\n💡 Key Takeaways:")
    print("1. Use threading.Thread(target=func) to create threads")
    print("2. Call start() to begin execution, join() to wait")
    print("3. Daemon threads stop automatically when main exits")
    print("4. Use thread.name and thread.is_alive() for monitoring")
    print("5. Custom thread classes offer better encapsulation")
    print("6. Thread-local storage provides per-thread data")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
```

---

## Exercises

**Exercise 1.**
Create a `SquareThread` class that subclasses `threading.Thread`. Its constructor takes a number, and its `run` method computes and stores the square. Create 5 instances (for numbers 1 through 5), start them all, join them all, and print each thread's result.

??? success "Solution to Exercise 1"
        ```python
        import threading

        class SquareThread(threading.Thread):
            def __init__(self, number):
                super().__init__()
                self.number = number
                self.result = None

            def run(self):
                self.result = self.number ** 2

        threads = [SquareThread(i) for i in range(1, 6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        for t in threads:
            print(f"{t.number}^2 = {t.result}")
        ```

---

**Exercise 2.**
Write a program that simulates downloading 8 files concurrently. Each "download" sleeps for a random duration between 0.5 and 1.5 seconds and returns the file name and byte count (a random integer). Use a `queue.Queue` to collect results from threads. After all threads finish, print the results sorted by file name.

??? success "Solution to Exercise 2"
        ```python
        import threading
        import queue
        import time
        import random

        def download(file_name, result_queue):
            duration = random.uniform(0.5, 1.5)
            time.sleep(duration)
            byte_count = random.randint(1000, 100_000)
            result_queue.put((file_name, byte_count))

        result_queue = queue.Queue()
        files = [f"file_{i}.dat" for i in range(8)]
        threads = []
        for f in files:
            t = threading.Thread(target=download, args=(f, result_queue))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        results = []
        while not result_queue.empty():
            results.append(result_queue.get())

        for name, size in sorted(results):
            print(f"{name}: {size} bytes")
        ```

---

**Exercise 3.**
Implement a `SafeThread` wrapper class that catches exceptions raised inside thread targets and stores them. Launch 5 threads where some succeed and some raise `ValueError`. After joining, iterate over the threads and print which succeeded and which failed (with the exception message).

??? success "Solution to Exercise 3"
        ```python
        import threading

        class SafeThread(threading.Thread):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.exception = None

            def run(self):
                try:
                    if self._target:
                        self._target(*self._args, **self._kwargs)
                except Exception as e:
                    self.exception = e

        def task(task_id):
            if task_id % 2 == 0:
                raise ValueError(f"Task {task_id} failed!")
            return task_id

        threads = [SafeThread(target=task, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        for i, t in enumerate(threads):
            if t.exception:
                print(f"Thread {i}: FAILED — {t.exception}")
            else:
                print(f"Thread {i}: succeeded")
        ```
