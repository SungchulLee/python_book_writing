# Process Basics

The `multiprocessing` module enables true parallel execution by running code in separate processes, each with its own Python interpreter and GIL.

!!! tip "Mental Model"
    Creating a `Process` is like launching a completely independent Python program that happens to run your function. The child gets a copy of all data at the moment of creation, but from then on parent and child live in separate memory worlds. Always guard process creation behind `if __name__ == "__main__":` to prevent infinite recursive spawning on platforms that re-import the module.

---

## Creating Processes

### Method 1: Using Process with target Function

```python
from multiprocessing import Process
import os
import time

def worker(name, delay):
    """Function to run in a separate process."""
    print(f"Process {os.getpid()}: {name} starting")
    time.sleep(delay)
    print(f"Process {os.getpid()}: {name} finished")

if __name__ == "__main__":
    # Create process
    p = Process(target=worker, args=("Worker-1", 2))
    
    # Start process
    p.start()
    
    print(f"Main process {os.getpid()}: started child")
    
    # Wait for process to complete
    p.join()
    
    print("Main process: child finished")
```

**Important**: Always use `if __name__ == "__main__":` guard to prevent recursive process spawning.

### Method 2: Subclassing Process

```python
from multiprocessing import Process
import os

class WorkerProcess(Process):
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value
    
    def run(self):
        """Override run() method."""
        print(f"Process {os.getpid()}: {self.name} computing...")
        result = self.value ** 2
        print(f"Process {os.getpid()}: result = {result}")

if __name__ == "__main__":
    p = WorkerProcess("Squarer", 10)
    p.start()
    p.join()
```

---

## Process Lifecycle

```
                    ┌─────────┐
                    │ Created │
                    └────┬────┘
                         │ start()
                         ▼
                    ┌─────────┐
                    │ Running │
                    └────┬────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
      completes     exception      terminate()
          │              │              │
          ▼              ▼              ▼
     ┌────────┐    ┌────────┐    ┌────────────┐
     │exitcode│    │exitcode│    │ Terminated │
     │   = 0  │    │  != 0  │    │            │
     └────────┘    └────────┘    └────────────┘
```

### Process States

```python
from multiprocessing import Process
import time

def worker():
    time.sleep(2)

if __name__ == "__main__":
    p = Process(target=worker)
    
    print(f"Created - is_alive: {p.is_alive()}")  # False
    print(f"PID: {p.pid}")  # None
    
    p.start()
    print(f"Started - is_alive: {p.is_alive()}")  # True
    print(f"PID: {p.pid}")  # Actual PID
    
    p.join()
    print(f"Joined - is_alive: {p.is_alive()}")   # False
    print(f"Exit code: {p.exitcode}")  # 0 (success)
```

---

## Multiple Processes

### Creating Multiple Processes

```python
from multiprocessing import Process
import os
import time

def worker(worker_id):
    print(f"Worker {worker_id} (PID {os.getpid()}): Starting")
    time.sleep(1)
    print(f"Worker {worker_id} (PID {os.getpid()}): Done")

if __name__ == "__main__":
    # Create processes
    processes = []
    for i in range(4):
        p = Process(target=worker, args=(i,))
        processes.append(p)
    
    # Start all processes
    for p in processes:
        p.start()
    
    # Wait for all processes
    for p in processes:
        p.join()
    
    print("All workers finished")
```

### Parallel Execution Demonstration

```python
from multiprocessing import Process
import os
import time

def cpu_bound_task(task_id, iterations):
    """CPU-intensive task."""
    print(f"Task {task_id} (PID {os.getpid()}): Starting")
    start = time.perf_counter()
    
    # CPU-bound work
    total = sum(i * i for i in range(iterations))
    
    elapsed = time.perf_counter() - start
    print(f"Task {task_id}: Completed in {elapsed:.2f}s")
    return total

if __name__ == "__main__":
    iterations = 10_000_000
    
    # Sequential
    print("Sequential execution:")
    start = time.perf_counter()
    for i in range(4):
        cpu_bound_task(i, iterations)
    seq_time = time.perf_counter() - start
    print(f"Sequential total: {seq_time:.2f}s\n")
    
    # Parallel
    print("Parallel execution:")
    start = time.perf_counter()
    processes = []
    for i in range(4):
        p = Process(target=cpu_bound_task, args=(i, iterations))
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()
    par_time = time.perf_counter() - start
    print(f"Parallel total: {par_time:.2f}s")
    print(f"Speedup: {seq_time/par_time:.1f}x")
```

---

## Process Arguments

### Positional Arguments (args)

```python
from multiprocessing import Process

def greet(name, greeting):
    print(f"{greeting}, {name}!")

if __name__ == "__main__":
    p = Process(target=greet, args=("Alice", "Hello"))
    p.start()
    p.join()
```

### Keyword Arguments (kwargs)

```python
from multiprocessing import Process

def greet(name, greeting="Hi"):
    print(f"{greeting}, {name}!")

if __name__ == "__main__":
    p = Process(target=greet, kwargs={"name": "Bob", "greeting": "Hey"})
    p.start()
    p.join()
```

---

## Getting Results from Processes

Processes have **isolated memory** — you cannot simply return values or use shared variables like with threads.

### Method 1: Queue

```python
from multiprocessing import Process, Queue

def compute(x, result_queue):
    """Compute and put result in queue."""
    result = x ** 2
    result_queue.put((x, result))

if __name__ == "__main__":
    result_queue = Queue()
    processes = []
    
    for i in range(5):
        p = Process(target=compute, args=(i, result_queue))
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()
    
    # Collect results
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    
    print(results)  # [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)]
```

### Method 2: Pipe

```python
from multiprocessing import Process, Pipe

def compute(x, conn):
    """Compute and send result through pipe."""
    result = x ** 2
    conn.send((x, result))
    conn.close()

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    
    p = Process(target=compute, args=(10, child_conn))
    p.start()
    
    result = parent_conn.recv()
    print(f"Result: {result}")  # (10, 100)
    
    p.join()
```

### Method 3: Shared Value

```python
from multiprocessing import Process, Value

def compute(shared_value):
    """Modify shared value."""
    shared_value.value = 42

if __name__ == "__main__":
    # 'i' = signed integer, 'd' = double
    shared = Value('i', 0)
    
    p = Process(target=compute, args=(shared,))
    p.start()
    p.join()
    
    print(f"Result: {shared.value}")  # 42
```

### Method 4: Shared Array

```python
from multiprocessing import Process, Array

def fill_array(shared_array):
    """Fill shared array."""
    for i in range(len(shared_array)):
        shared_array[i] = i * 2

if __name__ == "__main__":
    # 'd' = double, 5 elements
    shared = Array('d', 5)
    
    p = Process(target=fill_array, args=(shared,))
    p.start()
    p.join()
    
    print(f"Result: {list(shared)}")  # [0.0, 2.0, 4.0, 6.0, 8.0]
```

---

## Process Properties

### Process Name and PID

```python
from multiprocessing import Process, current_process
import os

def show_info():
    proc = current_process()
    print(f"Name: {proc.name}")
    print(f"PID: {proc.pid}")
    print(f"os.getpid(): {os.getpid()}")
    print(f"Parent PID: {os.getppid()}")

if __name__ == "__main__":
    p = Process(target=show_info, name="MyWorker")
    p.start()
    p.join()
```

### Daemon Processes

Daemon processes are terminated when the main process exits:

```python
from multiprocessing import Process
import time

def background_task():
    while True:
        print("Background running...")
        time.sleep(1)

if __name__ == "__main__":
    # Daemon process
    p = Process(target=background_task, daemon=True)
    p.start()
    
    time.sleep(3)
    print("Main exiting...")
    # Daemon process is killed here
```

### Exit Codes

```python
from multiprocessing import Process
import sys

def success_task():
    pass  # Exit code 0

def failure_task():
    sys.exit(1)  # Exit code 1

def exception_task():
    raise ValueError("Error!")  # Exit code 1

if __name__ == "__main__":
    p1 = Process(target=success_task)
    p2 = Process(target=failure_task)
    p3 = Process(target=exception_task)
    
    for p in [p1, p2, p3]:
        p.start()
    
    for p in [p1, p2, p3]:
        p.join()
    
    print(f"Success exit code: {p1.exitcode}")   # 0
    print(f"Failure exit code: {p2.exitcode}")   # 1
    print(f"Exception exit code: {p3.exitcode}") # 1
```

---

## Terminating Processes

### terminate() — Forceful Stop

```python
from multiprocessing import Process
import time

def long_task():
    print("Starting long task...")
    time.sleep(60)
    print("Long task done")  # Never reached

if __name__ == "__main__":
    p = Process(target=long_task)
    p.start()
    
    time.sleep(2)
    print("Terminating process...")
    p.terminate()  # Send SIGTERM
    p.join()
    
    print(f"Exit code: {p.exitcode}")  # -15 (SIGTERM)
```

### kill() — Immediate Stop (Python 3.7+)

```python
from multiprocessing import Process
import time

def stubborn_task():
    import signal
    signal.signal(signal.SIGTERM, signal.SIG_IGN)  # Ignore SIGTERM
    while True:
        time.sleep(1)

if __name__ == "__main__":
    p = Process(target=stubborn_task)
    p.start()
    
    time.sleep(1)
    p.kill()  # Send SIGKILL (cannot be ignored)
    p.join()
    
    print(f"Exit code: {p.exitcode}")  # -9 (SIGKILL)
```

---

## Start Methods

Different ways to start new processes:

```python
import multiprocessing as mp

# Check current method
print(mp.get_start_method())

# Set method (must be called before any process creation)
# mp.set_start_method('spawn')
```

| Method | Platforms | Description |
|--------|-----------|-------------|
| `spawn` | All | Start fresh Python interpreter (safest, default on Windows/macOS) |
| `fork` | Unix | Copy parent process (fast, default on Linux) |
| `forkserver` | Unix | Fork from a server process |

### spawn vs fork

```python
import multiprocessing as mp

# spawn: Safe, clean, but slower
# - New Python interpreter
# - Only picklable objects passed
# - No inherited state

# fork: Fast, but potential issues
# - Copies entire process memory
# - Can cause issues with threads
# - Inherits open file handles
```

---

## Exception Handling

### Exceptions in Child Processes

Exceptions in child processes don't propagate to parent:

```python
from multiprocessing import Process

def risky_task():
    raise ValueError("Something went wrong!")

if __name__ == "__main__":
    p = Process(target=risky_task)
    p.start()
    p.join()
    
    print(f"Exit code: {p.exitcode}")  # 1 (error)
    print("Main continues...")  # Parent not affected
```

### Capturing Exceptions

```python
from multiprocessing import Process, Queue
import traceback

def safe_task(func, args, result_queue):
    """Wrapper that captures exceptions."""
    try:
        result = func(*args)
        result_queue.put(("success", result))
    except Exception as e:
        result_queue.put(("error", str(e), traceback.format_exc()))

def risky_compute(x):
    if x < 0:
        raise ValueError("Negative not allowed")
    return x ** 2

if __name__ == "__main__":
    result_queue = Queue()
    
    # Test with valid input
    p1 = Process(target=safe_task, args=(risky_compute, (5,), result_queue))
    p1.start()
    p1.join()
    
    # Test with invalid input
    p2 = Process(target=safe_task, args=(risky_compute, (-1,), result_queue))
    p2.start()
    p2.join()
    
    # Check results
    while not result_queue.empty():
        result = result_queue.get()
        if result[0] == "success":
            print(f"Success: {result[1]}")
        else:
            print(f"Error: {result[1]}")
            print(result[2])
```

---

## CPU Count

```python
import multiprocessing as mp
import os

# Number of CPUs
print(f"multiprocessing.cpu_count(): {mp.cpu_count()}")
print(f"os.cpu_count(): {os.cpu_count()}")

# Rule of thumb for process count:
# CPU-bound: num_processes = cpu_count()
# I/O-bound with some CPU: num_processes = cpu_count() * 2
```

---

## Key Takeaways

- **Processes** have isolated memory — bypass GIL for true parallelism
- Always use `if __name__ == "__main__":` guard
- Use `Queue` or `Pipe` to communicate between processes
- Use `Value` and `Array` for simple shared state
- `start()` creates the process, `join()` waits for completion
- Check `exitcode` for process result (0 = success)
- Use `terminate()` or `kill()` to stop processes forcefully
- Match process count to CPU cores for CPU-bound tasks
- Processes have more overhead than threads — use for CPU-bound work

---

## Runnable Example: `process_basics_tutorial.py`

```python
"""
Topic 45.3 - Multiprocessing with multiprocessing.Process

Complete guide to process-based parallelism in Python, which bypasses
the GIL and achieves true parallel execution on multiple CPU cores.

Learning Objectives:
- Create and manage processes
- Pass data to processes
- Retrieve results from processes
- Process synchronization
- Shared memory between processes
- Process vs Thread comparison

Author: Python Educator
Date: 2024
"""

import multiprocessing
import os
import time
import random
from multiprocessing import Process, Value, Array, Queue


# ============================================================================
# PART 1: BEGINNER - Creating and Managing Processes
# ============================================================================

def basic_process_creation():
    """
    Create a simple process - similar to threading but with true parallelism.
    Each process gets its own Python interpreter and memory space.
    """
    print("=" * 70)
    print("BEGINNER: Creating Your First Process")
    print("=" * 70)
    
    def worker():
        """Function that runs in a separate process"""
        # Each process has its own process ID
        print(f"  Worker process ID: {os.getpid()}")
        print(f"  Worker parent process ID: {os.getppid()}")
        time.sleep(1)
        print(f"  Worker process completed")
    
    print(f"\nMain process ID: {os.getpid()}")
    print("\n📝 Creating a process:")
    print("   process = multiprocessing.Process(target=worker)")
    print("   process.start()")
    
    # Create the process
    process = Process(target=worker)
    
    print("\nStarting worker process...")
    process.start()  # Start the process
    
    print("Main process continues while worker runs...")
    
    # Wait for process to complete
    process.join()
    
    print("Worker process has finished.")
    print("\n💡 Key Difference from Threading:")
    print("   Each process has its own memory space and Python interpreter")
    print("   Processes can run on different CPU cores simultaneously")
    
    print("\n" + "=" * 70 + "\n")


def process_with_arguments():
    """
    Pass arguments to processes using args and kwargs.
    """
    print("=" * 70)
    print("BEGINNER: Passing Arguments to Processes")
    print("=" * 70)
    
    def calculate_square(number, result_label="Result"):
        """
        Calculate square of a number in a separate process.
        
        Args:
            number: Number to square
            result_label: Label for the result
        """
        result = number ** 2
        pid = os.getpid()
        print(f"[PID {pid}] {result_label}: {number}² = {result}")
        time.sleep(0.5)
    
    print("\n📝 Method 1: Using args tuple")
    p1 = Process(target=calculate_square, args=(5,))
    p1.start()
    p1.join()
    
    print("\n📝 Method 2: Using kwargs dictionary")
    p2 = Process(
        target=calculate_square,
        kwargs={"number": 7, "result_label": "Calculation"}
    )
    p2.start()
    p2.join()
    
    print("\n📝 Method 3: Mixed args and kwargs")
    p3 = Process(
        target=calculate_square,
        args=(12,),
        kwargs={"result_label": "Final Result"}
    )
    p3.start()
    p3.join()
    
    print("\n" + "=" * 70 + "\n")


def multiple_processes_cpu_bound():
    """
    Demonstrate true parallelism with CPU-bound tasks.
    Unlike threading, multiprocessing achieves real speedup!
    """
    print("=" * 70)
    print("BEGINNER: Multiple Processes for CPU-Bound Tasks")
    print("=" * 70)
    
    def cpu_intensive_task(task_id, iterations):
        """
        CPU-intensive computation.
        
        Args:
            task_id: Task identifier
            iterations: Number of iterations
        """
        pid = os.getpid()
        print(f"[Task {task_id}, PID {pid}] Starting...")
        
        # Heavy computation
        total = 0
        for i in range(iterations):
            total += i ** 2
        
        print(f"[Task {task_id}, PID {pid}] Completed. Sum: {total}")
        return total
    
    iterations = 10_000_000
    num_processes = 4
    
    print(f"\n⏱️  Running {num_processes} CPU-intensive processes:\n")
    start_time = time.time()
    
    # Create multiple processes
    processes = []
    for i in range(num_processes):
        process = Process(
            target=cpu_intensive_task,
            args=(i, iterations // num_processes),
            name=f"Worker-{i}"
        )
        processes.append(process)
        process.start()
    
    # Wait for all processes
    for process in processes:
        process.join()
    
    elapsed = time.time() - start_time
    print(f"\n✓ All processes completed in {elapsed:.2f} seconds")
    
    # Check CPU count
    cpu_count = multiprocessing.cpu_count()
    print(f"\n💡 Your system has {cpu_count} CPU cores")
    print(f"   Using {num_processes} processes = true parallel execution!")
    
    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 2: INTERMEDIATE - Process Communication and Data Sharing
# ============================================================================

def process_with_queue():
    """
    Use Queue for safe inter-process communication.
    Queue is process-safe (unlike regular Python lists).
    """
    print("=" * 70)
    print("INTERMEDIATE: Process Communication with Queue")
    print("=" * 70)
    
    def producer(queue, num_items):
        """
        Produce items and put them in queue.
        
        Args:
            queue: Multiprocessing Queue
            num_items: Number of items to produce
        """
        pid = os.getpid()
        for i in range(num_items):
            item = f"Item-{i}"
            queue.put(item)
            print(f"[Producer PID {pid}] Produced: {item}")
            time.sleep(0.3)
        
        # Signal completion
        queue.put(None)
        print(f"[Producer PID {pid}] Finished")
    
    def consumer(queue):
        """
        Consume items from queue.
        
        Args:
            queue: Multiprocessing Queue
        """
        pid = os.getpid()
        while True:
            item = queue.get()
            if item is None:
                break
            
            print(f"[Consumer PID {pid}] Consumed: {item}")
            time.sleep(0.5)
        
        print(f"[Consumer PID {pid}] Finished")
    
    print("\n⚙️  Starting producer-consumer with processes:\n")
    
    # Create a multiprocessing Queue
    queue = Queue()
    
    # Create processes
    prod = Process(target=producer, args=(queue, 5))
    cons = Process(target=consumer, args=(queue,))
    
    # Start both
    prod.start()
    cons.start()
    
    # Wait for completion
    prod.join()
    cons.join()
    
    print("\n✓ Producer-consumer completed")
    print("\n💡 Queue is process-safe - no need for locks!")
    
    print("\n" + "=" * 70 + "\n")


def shared_memory_with_value_and_array():
    """
    Share simple data between processes using Value and Array.
    These are backed by shared memory and protected by locks.
    """
    print("=" * 70)
    print("INTERMEDIATE: Shared Memory with Value and Array")
    print("=" * 70)
    
    def increment_counter(counter, array, process_id):
        """
        Increment shared counter and modify shared array.
        
        Args:
            counter: Shared Value object
            array: Shared Array object
            process_id: Process identifier
        """
        pid = os.getpid()
        
        for i in range(5):
            # Access shared value (thread-safe)
            with counter.get_lock():
                counter.value += 1
                current = counter.value
            
            # Modify shared array
            with array.get_lock():
                array[process_id] += 1
            
            print(f"[Process {process_id}, PID {pid}] Counter: {current}")
            time.sleep(0.1)
    
    print("\n📝 Creating shared memory objects:")
    
    # Create shared Value (integer)
    counter = Value('i', 0)  # 'i' = integer
    print(f"   counter = Value('i', 0)")
    
    # Create shared Array (5 integers)
    array = Array('i', [0, 0, 0, 0, 0])  # 'i' = integer array
    print(f"   array = Array('i', [0, 0, 0, 0, 0])")
    
    print("\n⚙️  Starting processes with shared memory:\n")
    
    # Create multiple processes
    processes = []
    for i in range(5):
        p = Process(target=increment_counter, args=(counter, array, i))
        processes.append(p)
        p.start()
    
    # Wait for all
    for p in processes:
        p.join()
    
    # Read results
    print(f"\n📊 Final Results:")
    print(f"   Counter value: {counter.value}")
    print(f"   Array values: {list(array)}")
    
    print("\n💡 Value and Array provide:")
    print("   ✓ Shared memory between processes")
    print("   ✓ Built-in locking for thread safety")
    print("   ✓ Efficient for simple data types")
    
    print("\n" + "=" * 70 + "\n")


def process_properties_and_lifecycle():
    """
    Explore process properties and lifecycle management.
    """
    print("=" * 70)
    print("INTERMEDIATE: Process Properties and Lifecycle")
    print("=" * 70)
    
    def worker(duration):
        """Worker that sleeps for duration"""
        pid = os.getpid()
        print(f"  [Worker PID {pid}] Working for {duration}s...")
        time.sleep(duration)
        print(f"  [Worker PID {pid}] Done!")
    
    # Create process
    process = Process(target=worker, args=(2,), name="MyWorker")
    
    print("\n📊 Before Starting:")
    print(f"  Name: {process.name}")
    print(f"  PID: {process.pid}")  # None until started
    print(f"  Is alive: {process.is_alive()}")
    print(f"  Daemon: {process.daemon}")
    
    # Start process
    print("\n🚀 Starting process...")
    process.start()
    
    print("\n📊 After Starting:")
    print(f"  Name: {process.name}")
    print(f"  PID: {process.pid}")  # Now has a PID
    print(f"  Is alive: {process.is_alive()}")
    
    # Wait for it
    process.join()
    
    print("\n📊 After Completion:")
    print(f"  Is alive: {process.is_alive()}")
    print(f"  Exit code: {process.exitcode}")  # 0 = success
    
    print("\n💡 Exit Codes:")
    print("   0 = Success")
    print("   1 = Exception occurred")
    print("   -N = Killed by signal N")
    
    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 3: ADVANCED - Process Patterns and Best Practices
# ============================================================================

class WorkerProcess(Process):
    """
    Custom process class - inherits from multiprocessing.Process.
    Override run() to define process behavior.
    """
    
    def __init__(self, task_name, data, result_queue):
        """
        Initialize custom process.
        
        Args:
            task_name: Name of the task
            data: Input data
            result_queue: Queue to store results
        """
        super().__init__()
        self.task_name = task_name
        self.data = data
        self.result_queue = result_queue
    
    def run(self):
        """
        This is called when start() is invoked.
        """
        pid = os.getpid()
        print(f"[{self.name}, PID {pid}] Starting task: {self.task_name}")
        
        # Process the data
        result = sum(x ** 2 for x in self.data)
        
        # Put result in queue
        self.result_queue.put({
            'task': self.task_name,
            'pid': pid,
            'result': result
        })
        
        print(f"[{self.name}, PID {pid}] Completed: {self.task_name}")


def custom_process_class_example():
    """
    Demonstrate custom process class.
    """
    print("=" * 70)
    print("ADVANCED: Custom Process Class")
    print("=" * 70)
    
    print("\n⚙️  Creating custom process instances:\n")
    
    # Queue to collect results
    result_queue = Queue()
    
    # Create processes
    processes = []
    for i in range(3):
        data = list(range(i * 100, (i + 1) * 100))
        p = WorkerProcess(f"Task-{i}", data, result_queue)
        processes.append(p)
        p.start()
    
    # Wait for all
    for p in processes:
        p.join()
    
    # Collect results
    print("\n📊 Results:")
    while not result_queue.empty():
        result = result_queue.get()
        print(f"   {result['task']} (PID {result['pid']}): {result['result']}")
    
    print("\n💡 Custom process classes are useful for:")
    print("   ✓ Encapsulating complex logic")
    print("   ✓ Managing process state")
    print("   ✓ Reusable process patterns")
    
    print("\n" + "=" * 70 + "\n")


def process_synchronization_with_lock():
    """
    Use Lock for process synchronization when sharing resources.
    """
    print("=" * 70)
    print("ADVANCED: Process Synchronization with Lock")
    print("=" * 70)
    
    def critical_section_worker(lock, shared_counter, worker_id):
        """
        Worker that accesses shared resource with lock protection.
        
        Args:
            lock: Multiprocessing Lock
            shared_counter: Shared Value
            worker_id: Worker identifier
        """
        pid = os.getpid()
        
        for i in range(5):
            # Acquire lock before accessing shared resource
            lock.acquire()
            try:
                # Critical section - only one process at a time
                current = shared_counter.value
                print(f"[Worker {worker_id}, PID {pid}] Read: {current}")
                time.sleep(0.1)  # Simulate work
                shared_counter.value = current + 1
                print(f"[Worker {worker_id}, PID {pid}] Wrote: {shared_counter.value}")
            finally:
                # Always release the lock
                lock.release()
            
            time.sleep(0.05)
    
    print("\n⚙️  Starting synchronized processes:\n")
    
    # Create shared resources
    lock = multiprocessing.Lock()
    counter = Value('i', 0)
    
    # Create processes
    processes = []
    for i in range(3):
        p = Process(
            target=critical_section_worker,
            args=(lock, counter, i)
        )
        processes.append(p)
        p.start()
    
    # Wait for all
    for p in processes:
        p.join()
    
    print(f"\n📊 Final counter value: {counter.value}")
    print(f"   Expected: {3 * 5} (3 workers × 5 increments)")
    
    print("\n💡 Lock ensures:")
    print("   ✓ Only one process in critical section at a time")
    print("   ✓ No race conditions")
    print("   ✓ Consistent shared state")
    
    print("\n" + "=" * 70 + "\n")


def process_vs_thread_comparison():
    """
    Direct comparison of processes vs threads for different workloads.
    """
    print("=" * 70)
    print("ADVANCED: Process vs Thread Performance Comparison")
    print("=" * 70)
    
    import threading
    
    def cpu_work(n):
        """CPU-intensive work"""
        total = 0
        for i in range(n):
            total += i ** 2
        return total
    
    def io_work(n):
        """I/O-intensive work"""
        time.sleep(n)
    
    iterations = 5_000_000
    
    # Test 1: CPU-bound with processes
    print("\n⏱️  CPU-bound with 4 processes:")
    start = time.time()
    procs = [
        Process(target=cpu_work, args=(iterations // 4,))
        for _ in range(4)
    ]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    proc_time = time.time() - start
    print(f"   Time: {proc_time:.2f}s")
    
    # Test 2: CPU-bound with threads
    print("\n⏱️  CPU-bound with 4 threads:")
    start = time.time()
    threads = [
        threading.Thread(target=cpu_work, args=(iterations // 4,))
        for _ in range(4)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    thread_time = time.time() - start
    print(f"   Time: {thread_time:.2f}s")
    
    print(f"\n📊 CPU-bound Result:")
    print(f"   Processes: {proc_time:.2f}s")
    print(f"   Threads: {thread_time:.2f}s")
    print(f"   Winner: {'Processes' if proc_time < thread_time else 'Threads'}")
    print(f"   Speedup: {thread_time/proc_time:.2f}x with multiprocessing")
    
    print("\n💡 Recommendation:")
    print("   ✓ Use multiprocessing for CPU-bound tasks")
    print("   ✓ Use threading for I/O-bound tasks")
    print("   ✓ Profile your specific workload")
    
    print("\n" + "=" * 70 + "\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run all multiprocessing demonstrations."""
    print("\n" + "=" * 70)
    print(" " * 20 + "MULTIPROCESSING")
    print(" " * 15 + "multiprocessing.Process Tutorial")
    print("=" * 70 + "\n")
    
    # Beginner level
    basic_process_creation()
    process_with_arguments()
    multiple_processes_cpu_bound()
    
    # Intermediate level
    process_with_queue()
    shared_memory_with_value_and_array()
    process_properties_and_lifecycle()
    
    # Advanced level
    custom_process_class_example()
    process_synchronization_with_lock()
    process_vs_thread_comparison()
    
    print("\n" + "=" * 70)
    print("Multiprocessing Tutorial Complete!")
    print("=" * 70)
    print("\n💡 Key Takeaways:")
    print("1. Processes bypass the GIL - true parallel execution")
    print("2. Each process has its own memory space")
    print("3. Use Queue for inter-process communication")
    print("4. Value and Array provide shared memory")
    print("5. Locks prevent race conditions in shared memory")
    print("6. Multiprocessing is ideal for CPU-bound tasks")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    # IMPORTANT: This guard is required on Windows
    main()
```

---

## Exercises

**Exercise 1.**
Create 4 processes that each compute the sum of squares in a non-overlapping range of 0 to 4,000,000. Use a `multiprocessing.Queue` to collect results. Print the partial sums and the total. Compare the wall-clock time against a single-process sequential version.

??? success "Solution to Exercise 1"
        ```python
        import time
        from multiprocessing import Process, Queue

        def partial_sum(start, end, q):
            total = sum(i * i for i in range(start, end))
            q.put((start, end, total))

        if __name__ == "__main__":
            N = 4_000_000
            chunk = N // 4
            q = Queue()

            # Parallel
            start_t = time.perf_counter()
            procs = []
            for i in range(4):
                s, e = i * chunk, (i + 1) * chunk
                p = Process(target=partial_sum, args=(s, e, q))
                p.start()
                procs.append(p)
            for p in procs:
                p.join()
            par_time = time.perf_counter() - start_t

            total = 0
            while not q.empty():
                s, e, partial = q.get()
                print(f"Range [{s}, {e}): {partial}")
                total += partial

            # Sequential
            start_t = time.perf_counter()
            seq_total = sum(i * i for i in range(N))
            seq_time = time.perf_counter() - start_t

            print(f"Total: {total} (check: {seq_total})")
            print(f"Parallel: {par_time:.2f}s, Sequential: {seq_time:.2f}s")
        ```

---

**Exercise 2.**
Write a `WorkerProcess` subclass that takes a list of numbers as input and computes their mean and standard deviation. Use a `Queue` to return the results. Create 3 instances with different data, start and join them all, then print each worker's statistics.

??? success "Solution to Exercise 2"
        ```python
        import statistics
        from multiprocessing import Process, Queue

        class WorkerProcess(Process):
            def __init__(self, name, data, result_queue):
                super().__init__()
                self.worker_name = name
                self.data = data
                self.result_queue = result_queue

            def run(self):
                mean = statistics.mean(self.data)
                stdev = statistics.stdev(self.data) if len(self.data) > 1 else 0
                self.result_queue.put((self.worker_name, mean, stdev))

        if __name__ == "__main__":
            q = Queue()
            datasets = {
                "A": [10, 20, 30, 40, 50],
                "B": [100, 200, 300],
                "C": [1.5, 2.5, 3.5, 4.5],
            }

            workers = [WorkerProcess(n, d, q) for n, d in datasets.items()]
            for w in workers:
                w.start()
            for w in workers:
                w.join()

            while not q.empty():
                name, mean, stdev = q.get()
                print(f"{name}: mean={mean:.2f}, stdev={stdev:.2f}")
        ```

---

**Exercise 3.**
Demonstrate process isolation by having two processes each modify a global variable `counter` by incrementing it 100,000 times. Print the main process's `counter` after both finish (it should still be 0). Then fix it using `multiprocessing.Value` with proper locking to get the correct total of 200,000.

??? success "Solution to Exercise 3"
        ```python
        from multiprocessing import Process, Value, Lock

        counter = 0  # global — not shared across processes

        def increment_global():
            global counter
            for _ in range(100_000):
                counter += 1

        def increment_shared(shared, lock):
            for _ in range(100_000):
                with lock:
                    shared.value += 1

        if __name__ == "__main__":
            # Isolated version
            p1 = Process(target=increment_global)
            p2 = Process(target=increment_global)
            p1.start(); p2.start()
            p1.join(); p2.join()
            print(f"Global counter (isolated): {counter}")  # 0

            # Shared version
            shared = Value('i', 0)
            lock = Lock()
            p3 = Process(target=increment_shared, args=(shared, lock))
            p4 = Process(target=increment_shared, args=(shared, lock))
            p3.start(); p4.start()
            p3.join(); p4.join()
            print(f"Shared counter: {shared.value}")  # 200000
        ```
