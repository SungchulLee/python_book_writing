# Thread Communication

Threads need to communicate and share data safely. This page covers patterns for passing data between threads.

!!! tip "Mental Model"
    The safest way for threads to talk is through a `queue.Queue` -- a thread-safe pipe where one side puts data in and the other side takes data out. Queues eliminate the need for manual locking because all synchronization is built in. Think of it as a conveyor belt between workers: producers load items, consumers pick them up, and nobody's hands collide.

---

## Thread-Safe Queue

The `queue` module provides thread-safe queues — the recommended way for threads to communicate.

### Basic Queue Usage

```python
import threading
import queue
import time

q = queue.Queue()

def producer():
    for i in range(5):
        item = f"item-{i}"
        q.put(item)
        print(f"Produced: {item}")
        time.sleep(0.5)
    q.put(None)  # Sentinel to signal completion

def consumer():
    while True:
        item = q.get()  # Blocks until item available
        if item is None:
            break
        print(f"Consumed: {item}")
        q.task_done()

producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()
```

### Queue Methods

```python
import queue

q = queue.Queue()

# Put items
q.put("item1")              # Block until space available
q.put("item2", block=False) # Raise queue.Full if full
q.put("item3", timeout=1)   # Raise queue.Full after timeout

# Get items
item = q.get()              # Block until item available
item = q.get(block=False)   # Raise queue.Empty if empty
item = q.get(timeout=1)     # Raise queue.Empty after timeout

# Check state
q.empty()                   # True if empty (approximate)
q.full()                    # True if full (approximate)
q.qsize()                   # Approximate size

# Task tracking
q.task_done()               # Mark task as complete
q.join()                    # Block until all tasks done
```

### Queue with Size Limit

```python
import threading
import queue
import time

# Limited capacity queue
q = queue.Queue(maxsize=3)

def producer():
    for i in range(10):
        print(f"Producing item-{i}...")
        q.put(f"item-{i}")  # Blocks when queue is full
        print(f"Produced item-{i}")

def consumer():
    time.sleep(2)  # Slow consumer
    while True:
        try:
            item = q.get(timeout=3)
            print(f"Consumed: {item}")
            time.sleep(0.5)
            q.task_done()
        except queue.Empty:
            break

threading.Thread(target=producer).start()
threading.Thread(target=consumer).start()
```

---

## Queue Types

### FIFO Queue (Default)

```python
import queue

q = queue.Queue()  # First-In-First-Out
q.put(1)
q.put(2)
q.put(3)

print(q.get())  # 1
print(q.get())  # 2
print(q.get())  # 3
```

### LIFO Queue (Stack)

```python
import queue

q = queue.LifoQueue()  # Last-In-First-Out
q.put(1)
q.put(2)
q.put(3)

print(q.get())  # 3
print(q.get())  # 2
print(q.get())  # 1
```

### Priority Queue

```python
import queue

q = queue.PriorityQueue()
q.put((3, "low priority"))
q.put((1, "high priority"))
q.put((2, "medium priority"))

print(q.get())  # (1, 'high priority')
print(q.get())  # (2, 'medium priority')
print(q.get())  # (3, 'low priority')
```

---

## Producer-Consumer Pattern

### Single Producer, Single Consumer

```python
import threading
import queue
import time

def producer(q, num_items):
    for i in range(num_items):
        item = f"item-{i}"
        q.put(item)
        print(f"[Producer] Created {item}")
        time.sleep(0.1)
    q.put(None)  # Sentinel

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        print(f"[Consumer] Processing {item}")
        time.sleep(0.2)
        q.task_done()

q = queue.Queue()

producer_t = threading.Thread(target=producer, args=(q, 10))
consumer_t = threading.Thread(target=consumer, args=(q,))

producer_t.start()
consumer_t.start()

producer_t.join()
consumer_t.join()
```

### Multiple Producers, Multiple Consumers

```python
import threading
import queue
import time
import random

def producer(q, producer_id, num_items):
    for i in range(num_items):
        item = f"P{producer_id}-item-{i}"
        q.put(item)
        print(f"[Producer {producer_id}] Created {item}")
        time.sleep(random.uniform(0.05, 0.15))

def consumer(q, consumer_id, stop_event):
    while not stop_event.is_set() or not q.empty():
        try:
            item = q.get(timeout=0.5)
            print(f"[Consumer {consumer_id}] Processing {item}")
            time.sleep(random.uniform(0.1, 0.3))
            q.task_done()
        except queue.Empty:
            continue

q = queue.Queue()
stop_event = threading.Event()

# Start 3 producers
producers = []
for i in range(3):
    t = threading.Thread(target=producer, args=(q, i, 5))
    t.start()
    producers.append(t)

# Start 2 consumers
consumers = []
for i in range(2):
    t = threading.Thread(target=consumer, args=(q, i, stop_event))
    t.start()
    consumers.append(t)

# Wait for producers to finish
for p in producers:
    p.join()

# Wait for queue to empty
q.join()

# Signal consumers to stop
stop_event.set()

# Wait for consumers
for c in consumers:
    c.join()

print("All done!")
```

---

## Worker Pool Pattern

### Thread Pool with Queue

```python
import threading
import queue
import time

class ThreadPool:
    def __init__(self, num_workers):
        self.tasks = queue.Queue()
        self.results = queue.Queue()
        self.workers = []
        
        for _ in range(num_workers):
            worker = threading.Thread(target=self._worker)
            worker.daemon = True
            worker.start()
            self.workers.append(worker)
    
    def _worker(self):
        while True:
            func, args, kwargs = self.tasks.get()
            if func is None:
                break
            try:
                result = func(*args, **kwargs)
                self.results.put(("success", result))
            except Exception as e:
                self.results.put(("error", e))
            finally:
                self.tasks.task_done()
    
    def submit(self, func, *args, **kwargs):
        self.tasks.put((func, args, kwargs))
    
    def wait(self):
        self.tasks.join()
    
    def get_results(self):
        results = []
        while not self.results.empty():
            results.append(self.results.get())
        return results
    
    def shutdown(self):
        for _ in self.workers:
            self.tasks.put((None, None, None))
        for w in self.workers:
            w.join()

# Usage
def process(x):
    time.sleep(0.1)
    return x * 2

pool = ThreadPool(4)

for i in range(20):
    pool.submit(process, i)

pool.wait()
results = pool.get_results()
print(results)

pool.shutdown()
```

---

## Sharing Data with Locks

### Thread-Safe Counter

```python
import threading

class ThreadSafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()
    
    def increment(self):
        with self._lock:
            self._value += 1
    
    def decrement(self):
        with self._lock:
            self._value -= 1
    
    @property
    def value(self):
        with self._lock:
            return self._value

counter = ThreadSafeCounter()

def worker():
    for _ in range(10000):
        counter.increment()

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(counter.value)  # Always 100000
```

### Thread-Safe Dictionary

```python
import threading

class ThreadSafeDict:
    def __init__(self):
        self._dict = {}
        self._lock = threading.RLock()
    
    def __setitem__(self, key, value):
        with self._lock:
            self._dict[key] = value
    
    def __getitem__(self, key):
        with self._lock:
            return self._dict[key]
    
    def __contains__(self, key):
        with self._lock:
            return key in self._dict
    
    def get(self, key, default=None):
        with self._lock:
            return self._dict.get(key, default)
    
    def items(self):
        with self._lock:
            return list(self._dict.items())

# Usage
d = ThreadSafeDict()

def writer(writer_id):
    for i in range(100):
        d[f"key-{writer_id}-{i}"] = i

threads = [threading.Thread(target=writer, args=(i,)) for i in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Total items: {len(d.items())}")  # 500
```

---

## Thread-Local Data

`threading.local()` provides data that is specific to each thread.

```python
import threading
import time

# Thread-local storage
local_data = threading.local()

def worker(name):
    # Each thread gets its own 'name' attribute
    local_data.name = name
    
    # Simulate work
    time.sleep(0.1)
    
    # Access thread-local data
    print(f"Thread {local_data.name}: processing")
    time.sleep(0.1)
    print(f"Thread {local_data.name}: done")

threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(f"Worker-{i}",))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
```

### Practical Example: Database Connection per Thread

```python
import threading

class DatabaseConnection:
    """Simulated database connection."""
    def __init__(self, thread_name):
        self.thread_name = thread_name
        print(f"Created connection for {thread_name}")
    
    def query(self, sql):
        return f"Result from {self.thread_name}"

# Thread-local connection
_connections = threading.local()

def get_connection():
    """Get or create connection for current thread."""
    if not hasattr(_connections, 'conn'):
        _connections.conn = DatabaseConnection(
            threading.current_thread().name
        )
    return _connections.conn

def worker():
    conn = get_connection()  # Each thread gets its own connection
    print(conn.query("SELECT * FROM users"))
    
    conn2 = get_connection()  # Same connection returned
    print(f"Same connection: {conn is conn2}")

threads = []
for i in range(3):
    t = threading.Thread(target=worker, name=f"Thread-{i}")
    t.start()
    threads.append(t)

for t in threads:
    t.join()
```

---

## Pipe Pattern with Queues

Chain multiple processing stages:

```python
import threading
import queue
import time

def stage1(input_q, output_q):
    """Read raw data, output preprocessed."""
    while True:
        item = input_q.get()
        if item is None:
            output_q.put(None)
            break
        result = f"preprocessed({item})"
        output_q.put(result)
        input_q.task_done()

def stage2(input_q, output_q):
    """Process preprocessed data."""
    while True:
        item = input_q.get()
        if item is None:
            output_q.put(None)
            break
        result = f"processed({item})"
        output_q.put(result)
        input_q.task_done()

def stage3(input_q, results):
    """Final stage, collect results."""
    while True:
        item = input_q.get()
        if item is None:
            break
        results.append(f"final({item})")
        input_q.task_done()

# Create queues for pipeline
q1 = queue.Queue()
q2 = queue.Queue()
q3 = queue.Queue()
results = []

# Start pipeline stages
threading.Thread(target=stage1, args=(q1, q2)).start()
threading.Thread(target=stage2, args=(q2, q3)).start()
threading.Thread(target=stage3, args=(q3, results)).start()

# Feed input
for i in range(5):
    q1.put(f"item-{i}")
q1.put(None)  # Sentinel

# Wait for completion
time.sleep(1)  # Allow pipeline to complete

print("Results:", results)
# ['final(processed(preprocessed(item-0)))', ...]
```

---

## Summary: Communication Patterns

| Pattern | Use Case | Module |
|---------|----------|--------|
| **Queue** | Producer-consumer, task distribution | `queue.Queue` |
| **Priority Queue** | Tasks with priorities | `queue.PriorityQueue` |
| **Shared variable + Lock** | Simple shared state | `threading.Lock` |
| **Thread-local** | Per-thread data (connections, context) | `threading.local()` |
| **Event** | Simple signaling | `threading.Event` |
| **Condition** | Complex waiting conditions | `threading.Condition` |

---

## Key Takeaways

- **Queue** is the safest way for threads to communicate
- Use `q.put()` / `q.get()` — they handle locking automatically
- Use sentinel values (`None`) to signal termination
- `threading.local()` for per-thread data (database connections, etc.)
- Protect shared mutable data with locks
- The producer-consumer pattern scales well with multiple workers
- `q.join()` waits for all `q.task_done()` calls to match `q.put()` calls
- Choose queue type based on ordering needs (FIFO, LIFO, Priority)

---

## Runnable Example: `bank_account_condition_example.py`

```python
"""
Thread Synchronization: Bank Account with Condition Variables

A practical example of thread coordination using threading.Condition.
Multiple depositor and withdrawer threads operate on a shared bank
account, with withdrawals waiting until sufficient funds are available.

Topics covered:
- threading.Condition for wait/notify coordination
- Producer-consumer pattern (depositors produce, withdrawers consume)
- threading.Lock for mutual exclusion
- ThreadPoolExecutor for managing thread pools
- Thread-safe balance updates

Based on concepts from Python-100-Days example21 and ch14/threading materials.
"""

import threading
from concurrent.futures import ThreadPoolExecutor
from random import randint
from time import sleep


# =============================================================================
# Example 1: Thread-Safe Bank Account
# =============================================================================

class BankAccount:
    """A bank account with thread-safe deposit and withdrawal.

    Uses threading.Condition (which wraps a Lock) to coordinate:
    - Deposits: add money and notify waiting withdrawals
    - Withdrawals: wait until sufficient balance is available
    """

    def __init__(self, initial_balance: float = 0.0):
        self._balance = initial_balance
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        """Deposit money and notify any waiting withdrawals.

        After depositing, notify_all() wakes up threads that
        are waiting in withdraw() so they can re-check balance.
        """
        with self._condition:
            self._balance += amount
            self._condition.notify_all()  # Wake up waiting withdrawers

    def withdraw(self, amount: float) -> None:
        """Withdraw money, waiting if balance is insufficient.

        The while loop re-checks the condition after being notified,
        because another thread might have consumed the funds first
        (spurious wakeup protection).
        """
        with self._condition:
            while amount > self._balance:
                self._condition.wait()  # Release lock and wait
            self._balance -= amount


# =============================================================================
# Example 2: Depositor and Withdrawer Workers
# =============================================================================

def depositor(account: BankAccount, name: str, rounds: int = 5) -> None:
    """Worker that makes random deposits."""
    for i in range(rounds):
        amount = randint(50, 200)
        account.deposit(amount)
        print(f"  {name} deposited ${amount:>3} -> balance: ${account.balance:.0f}")
        sleep(0.1)


def withdrawer(account: BankAccount, name: str, rounds: int = 3) -> None:
    """Worker that makes random withdrawals (waits if insufficient funds)."""
    for i in range(rounds):
        amount = randint(100, 300)
        print(f"  {name} wants to withdraw ${amount}...")
        account.withdraw(amount)
        print(f"  {name} withdrew  ${amount:>3} -> balance: ${account.balance:.0f}")
        sleep(0.2)


# =============================================================================
# Example 3: Running the Simulation
# =============================================================================

def run_simulation():
    """Run the bank account simulation with multiple threads."""
    print("=== Bank Account Thread Simulation ===")
    print("3 depositors (5 rounds each) + 3 withdrawers (3 rounds each)")
    print()

    account = BankAccount(initial_balance=100)
    print(f"Initial balance: ${account.balance:.0f}")
    print()

    with ThreadPoolExecutor(max_workers=6) as pool:
        # Submit depositor tasks
        for i in range(3):
            pool.submit(depositor, account, f"Depositor-{i+1}")
        # Submit withdrawer tasks
        for i in range(3):
            pool.submit(withdrawer, account, f"Withdrawer-{i+1}")

    print(f"\nFinal balance: ${account.balance:.0f}")
    print()


# =============================================================================
# Example 4: Understanding Condition vs Lock
# =============================================================================

def demo_condition_vs_lock():
    """Explain when to use Condition vs plain Lock."""
    print("=== Condition vs Lock ===")
    print("""
    threading.Lock:
      - Mutual exclusion only
      - One thread at a time in critical section
      - Use when: protecting shared data from concurrent access

    threading.Condition:
      - Mutual exclusion + wait/notify
      - Threads can WAIT for a condition to become true
      - Other threads NOTIFY when condition might have changed
      - Use when: threads need to coordinate (producer-consumer)

    Pattern:
      # Waiting thread:
      with condition:
          while not ready:      # Always use while (not if)
              condition.wait()  # Releases lock, blocks, reacquires lock
          # ... proceed ...

      # Notifying thread:
      with condition:
          # ... make changes ...
          condition.notify_all()  # Wake up waiting threads
    """)


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    run_simulation()
    demo_condition_vs_lock()
```

---

## Exercises

**Exercise 1.**
Build a 3-stage pipeline using `queue.Queue`. Stage 1 reads integers 0-9 and doubles them. Stage 2 takes the doubled values and adds 10. Stage 3 collects final results into a list. Use `None` as a sentinel to signal each stage to shut down. Print the final list of results.

??? success "Solution to Exercise 1"
        ```python
        import threading
        import queue

        q1 = queue.Queue()
        q2 = queue.Queue()
        results = []

        def stage1(in_q, out_q):
            while True:
                item = in_q.get()
                if item is None:
                    out_q.put(None)
                    break
                out_q.put(item * 2)

        def stage2(in_q, out_q):
            while True:
                item = in_q.get()
                if item is None:
                    out_q.put(None)
                    break
                out_q.put(item + 10)

        def stage3(in_q, result_list):
            while True:
                item = in_q.get()
                if item is None:
                    break
                result_list.append(item)

        q_a = queue.Queue()
        q_b = queue.Queue()
        q_c = queue.Queue()

        t1 = threading.Thread(target=stage1, args=(q_a, q_b))
        t2 = threading.Thread(target=stage2, args=(q_b, q_c))
        t3 = threading.Thread(target=stage3, args=(q_c, results))

        t1.start(); t2.start(); t3.start()

        for i in range(10):
            q_a.put(i)
        q_a.put(None)

        t1.join(); t2.join(); t3.join()
        print(f"Results: {results}")
        # Expected: [10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
        ```

---

**Exercise 2.**
Implement a `PriorityQueue`-based task scheduler. Create 3 producer threads that each submit 5 tasks with random priorities (1-10, where 1 is highest). A single consumer thread processes tasks in priority order, printing each task's priority and content. Use a sentinel with priority 999 to signal termination.

??? success "Solution to Exercise 2"
        ```python
        import threading
        import queue
        import random

        pq = queue.PriorityQueue()
        num_producers = 3

        def producer(pid):
            for i in range(5):
                priority = random.randint(1, 10)
                task = f"P{pid}-Task{i}"
                pq.put((priority, task))
                print(f"[Producer {pid}] submitted {task} (priority {priority})")

        def consumer():
            sentinels = 0
            while sentinels < num_producers:
                priority, task = pq.get()
                if priority == 999:
                    sentinels += 1
                    continue
                print(f"[Consumer] processing {task} (priority {priority})")

        threads = []
        for i in range(num_producers):
            t = threading.Thread(target=producer, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Send sentinels after all producers finish
        for _ in range(num_producers):
            pq.put((999, "STOP"))

        ct = threading.Thread(target=consumer)
        ct.start()
        ct.join()
        print("All tasks processed.")
        ```

---

**Exercise 3.**
Write a `ThreadSafeCounter` class that supports `increment()`, `decrement()`, and `value` (property). Spawn 10 threads that each increment 10,000 times and 10 threads that each decrement 10,000 times. Verify the final value is 0.

??? success "Solution to Exercise 3"
        ```python
        import threading

        class ThreadSafeCounter:
            def __init__(self):
                self._value = 0
                self._lock = threading.Lock()

            def increment(self):
                with self._lock:
                    self._value += 1

            def decrement(self):
                with self._lock:
                    self._value -= 1

            @property
            def value(self):
                with self._lock:
                    return self._value

        counter = ThreadSafeCounter()

        def inc_worker():
            for _ in range(10_000):
                counter.increment()

        def dec_worker():
            for _ in range(10_000):
                counter.decrement()

        threads = []
        for _ in range(10):
            threads.append(threading.Thread(target=inc_worker))
            threads.append(threading.Thread(target=dec_worker))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        print(f"Final value: {counter.value}")
        assert counter.value == 0
        ```
