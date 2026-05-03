# Sharing State Between Processes

Processes have isolated memory spaces. To share data between processes, you need special mechanisms provided by the `multiprocessing` module.

!!! tip "Mental Model"
    Because each process has its own memory, modifying a global variable in one process has no effect on another. To share state you must use explicitly shared objects -- `Value` and `Array` for simple data in shared memory, `Manager` for complex data structures proxied over a connection. The harder sharing is, the safer your program -- treat shared state as a last resort, not the default.

---

## The Challenge: Memory Isolation

```python
from multiprocessing import Process

# This does NOT work as expected!
counter = 0

def increment():
    global counter
    for _ in range(100000):
        counter += 1

if __name__ == "__main__":
    p1 = Process(target=increment)
    p2 = Process(target=increment)
    
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    
    print(f"Counter: {counter}")  # Still 0!
    # Each process has its own copy of counter
```

---

## Shared Value

For sharing simple scalar values between processes.

### Basic Usage

```python
from multiprocessing import Process, Value

def increment(shared_counter, n):
    for _ in range(n):
        shared_counter.value += 1

if __name__ == "__main__":
    # Type codes: 'i' = int, 'd' = double, 'c' = char
    counter = Value('i', 0)
    
    p1 = Process(target=increment, args=(counter, 100000))
    p2 = Process(target=increment, args=(counter, 100000))
    
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    
    print(f"Counter: {counter.value}")
    # May be less than 200000 — race condition!
```

### With Lock (Thread-Safe)

```python
from multiprocessing import Process, Value, Lock

def increment(shared_counter, lock, n):
    for _ in range(n):
        with lock:
            shared_counter.value += 1

if __name__ == "__main__":
    counter = Value('i', 0)
    lock = Lock()
    
    p1 = Process(target=increment, args=(counter, lock, 100000))
    p2 = Process(target=increment, args=(counter, lock, 100000))
    
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    
    print(f"Counter: {counter.value}")  # Always 200000
```

### Value with Built-in Lock

```python
from multiprocessing import Process, Value

def increment(shared_counter, n):
    for _ in range(n):
        with shared_counter.get_lock():
            shared_counter.value += 1

if __name__ == "__main__":
    counter = Value('i', 0)  # Has built-in lock
    
    p1 = Process(target=increment, args=(counter, 100000))
    p2 = Process(target=increment, args=(counter, 100000))
    
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    
    print(f"Counter: {counter.value}")  # Always 200000
```

### Type Codes

| Code | C Type | Python Type |
|------|--------|-------------|
| `'b'` | signed char | int |
| `'B'` | unsigned char | int |
| `'i'` | signed int | int |
| `'I'` | unsigned int | int |
| `'l'` | signed long | int |
| `'L'` | unsigned long | int |
| `'f'` | float | float |
| `'d'` | double | float |

---

## Shared Array

For sharing sequences of values.

### Basic Array

```python
from multiprocessing import Process, Array

def fill_array(shared_array, start_value):
    for i in range(len(shared_array)):
        shared_array[i] = start_value + i

if __name__ == "__main__":
    # 'd' = double, size 5
    arr = Array('d', 5)
    
    p = Process(target=fill_array, args=(arr, 10))
    p.start()
    p.join()
    
    print(list(arr))  # [10.0, 11.0, 12.0, 13.0, 14.0]
```

### Initialize with Values

```python
from multiprocessing import Array

# Initialize with values
arr1 = Array('i', [1, 2, 3, 4, 5])
print(list(arr1))  # [1, 2, 3, 4, 5]

# Initialize with size (zeros)
arr2 = Array('d', 10)
print(list(arr2))  # [0.0, 0.0, ..., 0.0]
```

### Concurrent Array Access

```python
from multiprocessing import Process, Array, Lock

def increment_array(arr, lock, amount):
    with lock:
        for i in range(len(arr)):
            arr[i] += amount

if __name__ == "__main__":
    arr = Array('i', [0, 0, 0, 0, 0])
    lock = Lock()
    
    processes = []
    for _ in range(10):
        p = Process(target=increment_array, args=(arr, lock, 1))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(list(arr))  # [10, 10, 10, 10, 10]
```

---

## Queue for Communication

`Queue` is the recommended way to pass data between processes.

### Basic Queue

```python
from multiprocessing import Process, Queue

def producer(q, items):
    for item in items:
        q.put(item)
        print(f"Produced: {item}")
    q.put(None)  # Sentinel

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        print(f"Consumed: {item}")

if __name__ == "__main__":
    q = Queue()
    
    p1 = Process(target=producer, args=(q, [1, 2, 3, 4, 5]))
    p2 = Process(target=consumer, args=(q,))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
```

### Collecting Results with Queue

```python
from multiprocessing import Process, Queue

def worker(task_id, q):
    result = task_id ** 2
    q.put((task_id, result))

if __name__ == "__main__":
    result_queue = Queue()
    processes = []
    
    for i in range(5):
        p = Process(target=worker, args=(i, result_queue))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    # Collect results
    results = {}
    while not result_queue.empty():
        task_id, result = result_queue.get()
        results[task_id] = result
    
    print(results)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

---

## Pipe for Two-Way Communication

`Pipe` creates a connection between two processes.

### Basic Pipe

```python
from multiprocessing import Process, Pipe

def sender(conn):
    conn.send("Hello from sender!")
    conn.send([1, 2, 3])
    conn.close()

def receiver(conn):
    msg1 = conn.recv()
    msg2 = conn.recv()
    print(f"Received: {msg1}")
    print(f"Received: {msg2}")

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    
    p1 = Process(target=sender, args=(child_conn,))
    p2 = Process(target=receiver, args=(parent_conn,))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
```

### Bidirectional Pipe

```python
from multiprocessing import Process, Pipe

def ping_pong(conn, name):
    for i in range(3):
        msg = conn.recv()
        print(f"{name} received: {msg}")
        conn.send(f"{name} reply {i}")
    conn.close()

if __name__ == "__main__":
    conn1, conn2 = Pipe()
    
    p = Process(target=ping_pong, args=(conn2, "Worker"))
    p.start()
    
    # Main process
    for i in range(3):
        conn1.send(f"Main message {i}")
        reply = conn1.recv()
        print(f"Main received: {reply}")
    
    p.join()
```

---

## Manager for Complex Objects

`Manager` provides a way to share complex Python objects (lists, dicts) between processes.

### Shared List

```python
from multiprocessing import Process, Manager

def worker(shared_list, item):
    shared_list.append(item)

if __name__ == "__main__":
    with Manager() as manager:
        shared_list = manager.list()
        
        processes = []
        for i in range(5):
            p = Process(target=worker, args=(shared_list, i))
            processes.append(p)
            p.start()
        
        for p in processes:
            p.join()
        
        print(list(shared_list))  # [0, 1, 2, 3, 4] (order may vary)
```

### Shared Dictionary

```python
from multiprocessing import Process, Manager

def worker(shared_dict, key, value):
    shared_dict[key] = value

if __name__ == "__main__":
    with Manager() as manager:
        shared_dict = manager.dict()
        
        processes = []
        for i in range(5):
            p = Process(target=worker, args=(shared_dict, f"key_{i}", i ** 2))
            processes.append(p)
            p.start()
        
        for p in processes:
            p.join()
        
        print(dict(shared_dict))
        # {'key_0': 0, 'key_1': 1, 'key_2': 4, 'key_3': 9, 'key_4': 16}
```

### Shared Namespace

```python
from multiprocessing import Process, Manager

def worker(ns):
    ns.x += 1
    ns.items.append(ns.x)

if __name__ == "__main__":
    with Manager() as manager:
        ns = manager.Namespace()
        ns.x = 0
        ns.items = manager.list()
        
        processes = []
        for _ in range(5):
            p = Process(target=worker, args=(ns,))
            processes.append(p)
            p.start()
        
        for p in processes:
            p.join()
        
        print(f"x = {ns.x}")
        print(f"items = {list(ns.items)}")
```

### Manager Performance Warning

`Manager` objects are **slower** than `Value`/`Array` because they use a separate server process for synchronization:

```python
# Fast: Direct shared memory
counter = Value('i', 0)  # Direct memory access

# Slower: Proxy through manager process
with Manager() as manager:
    counter = manager.Value('i', 0)  # Proxied access
```

---

## Shared Memory (Python 3.8+)

`SharedMemory` provides raw shared memory for high-performance data sharing.

### Basic SharedMemory

```python
from multiprocessing import Process
from multiprocessing.shared_memory import SharedMemory
import numpy as np

def worker(shm_name, shape, dtype):
    # Attach to existing shared memory
    existing_shm = SharedMemory(name=shm_name)
    array = np.ndarray(shape, dtype=dtype, buffer=existing_shm.buf)
    
    # Modify array
    array[:] = array * 2
    
    existing_shm.close()

if __name__ == "__main__":
    # Create array in shared memory
    arr = np.array([1, 2, 3, 4, 5], dtype=np.float64)
    
    shm = SharedMemory(create=True, size=arr.nbytes)
    shared_arr = np.ndarray(arr.shape, dtype=arr.dtype, buffer=shm.buf)
    shared_arr[:] = arr[:]  # Copy data
    
    print(f"Before: {shared_arr}")
    
    p = Process(target=worker, args=(shm.name, arr.shape, arr.dtype))
    p.start()
    p.join()
    
    print(f"After: {shared_arr}")
    
    shm.close()
    shm.unlink()  # Clean up
```

### SharedMemory with NumPy

```python
from multiprocessing import Process
from multiprocessing.shared_memory import SharedMemory
import numpy as np

def compute_in_place(shm_name, shape, dtype, start, end):
    """Process a slice of shared array."""
    shm = SharedMemory(name=shm_name)
    arr = np.ndarray(shape, dtype=dtype, buffer=shm.buf)
    
    arr[start:end] = arr[start:end] ** 2
    
    shm.close()

if __name__ == "__main__":
    size = 1000000
    arr = np.arange(size, dtype=np.float64)
    
    # Create shared memory
    shm = SharedMemory(create=True, size=arr.nbytes)
    shared_arr = np.ndarray(arr.shape, dtype=arr.dtype, buffer=shm.buf)
    shared_arr[:] = arr
    
    # Process in parallel
    num_workers = 4
    chunk_size = size // num_workers
    
    processes = []
    for i in range(num_workers):
        start = i * chunk_size
        end = start + chunk_size if i < num_workers - 1 else size
        p = Process(target=compute_in_place, 
                   args=(shm.name, arr.shape, arr.dtype, start, end))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(f"First 10: {shared_arr[:10]}")
    
    shm.close()
    shm.unlink()
```

---

## Comparison of Sharing Methods

| Method | Speed | Use Case | Complexity |
|--------|-------|----------|------------|
| `Value` | Fast | Single scalar | Simple |
| `Array` | Fast | Fixed-size arrays | Simple |
| `Queue` | Medium | Message passing | Simple |
| `Pipe` | Medium | Two-process communication | Simple |
| `Manager` | Slow | Complex objects (list, dict) | Medium |
| `SharedMemory` | Fastest | Large arrays, NumPy | Complex |

---

## Best Practices

### 1. Prefer Message Passing (Queue)

```python
# Good: Clear data flow
result_queue = Queue()
p = Process(target=worker, args=(data, result_queue))
```

### 2. Use Locks for Shared State

```python
# Good: Protected access
with shared_value.get_lock():
    shared_value.value += 1
```

### 3. Minimize Shared State

```python
# Better: Pass data, return results
def worker(input_data, result_queue):
    result = process(input_data)
    result_queue.put(result)
```

### 4. Clean Up SharedMemory

```python
# Always unlink shared memory
try:
    # ... use shared memory ...
finally:
    shm.close()
    shm.unlink()
```

---

## Key Takeaways

- Processes have **isolated memory** — global variables aren't shared
- Use `Value` and `Array` for simple shared data (fast)
- Use `Queue` for message passing between processes (recommended)
- Use `Pipe` for two-way communication between two processes
- Use `Manager` for complex objects like lists and dicts (slower)
- Use `SharedMemory` for high-performance NumPy array sharing
- **Always use locks** when multiple processes modify shared data
- Prefer message passing over shared state when possible

---

## Exercises

**Exercise 1.**
Use `multiprocessing.Value` and a `Lock` to implement a shared counter that 4 processes each increment 50,000 times. Verify the final value is exactly 200,000. Then remove the lock and show that the result is often incorrect.

??? success "Solution to Exercise 1"
        ```python
        from multiprocessing import Process, Value, Lock

        def increment_with_lock(counter, lock):
            for _ in range(50_000):
                with lock:
                    counter.value += 1

        def increment_no_lock(counter):
            for _ in range(50_000):
                counter.value += 1

        if __name__ == "__main__":
            # With lock
            c1 = Value('i', 0)
            lock = Lock()
            procs = [Process(target=increment_with_lock, args=(c1, lock)) for _ in range(4)]
            for p in procs: p.start()
            for p in procs: p.join()
            print(f"With lock: {c1.value} (expected 200000)")

            # Without lock
            c2 = Value('i', 0)
            procs = [Process(target=increment_no_lock, args=(c2,)) for _ in range(4)]
            for p in procs: p.start()
            for p in procs: p.join()
            print(f"Without lock: {c2.value} (may be < 200000)")
        ```

---

**Exercise 2.**
Use a `multiprocessing.Manager` to share a dictionary between 5 processes. Each process writes 10 key-value pairs of the form `f"proc{pid}_key{i}"`. After all processes finish, print the dictionary and verify it has exactly 50 entries.

??? success "Solution to Exercise 2"
        ```python
        import os
        from multiprocessing import Process, Manager

        def writer(shared_dict, pid):
            for i in range(10):
                shared_dict[f"proc{pid}_key{i}"] = i * pid

        if __name__ == "__main__":
            with Manager() as manager:
                d = manager.dict()
                procs = [Process(target=writer, args=(d, i)) for i in range(5)]
                for p in procs: p.start()
                for p in procs: p.join()
                result = dict(d)

            print(f"Total entries: {len(result)} (expected 50)")
            for k in sorted(result)[:5]:
                print(f"  {k}: {result[k]}")
            print("  ...")
        ```

---

**Exercise 3.**
Use `multiprocessing.Pipe` to implement a simple request-response pattern. The main process sends 5 computation requests (a number to square) through the pipe; a child process reads each request, computes the square, and sends the result back. The main process collects and prints all results.

??? success "Solution to Exercise 3"
        ```python
        from multiprocessing import Process, Pipe

        def compute_worker(conn):
            while True:
                msg = conn.recv()
                if msg is None:
                    break
                conn.send(msg ** 2)
            conn.close()

        if __name__ == "__main__":
            parent_conn, child_conn = Pipe()
            p = Process(target=compute_worker, args=(child_conn,))
            p.start()

            for num in [3, 7, 11, 15, 20]:
                parent_conn.send(num)
                result = parent_conn.recv()
                print(f"{num}^2 = {result}")

            parent_conn.send(None)  # shutdown signal
            p.join()
        ```
