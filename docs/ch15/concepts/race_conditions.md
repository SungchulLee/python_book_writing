# Race Conditions

A **race condition** occurs when the behavior of a program depends on the relative timing of events, such as the order in which threads execute.

!!! tip "Mental Model"
    A race condition is a bug that only appears when timing is unlucky. Picture two people editing the same spreadsheet cell at the same moment -- one overwrites the other without knowing. The fix is to make critical sections atomic: lock, read-modify-write, unlock, so no one else can interfere mid-operation.

## Classic Race Condition: Check-Then-Act

### The Problem

```python
import threading
import time

balance = 100

def withdraw(amount):
    global balance
    
    # CHECK: Is there enough?
    if balance >= amount:
        # Race window: another thread might withdraw here!
        time.sleep(0.001)  # Simulates processing delay
        
        # ACT: Withdraw
        balance -= amount
        print(f"Withdrew {amount}, balance: {balance}")
        return True
    else:
        print(f"Insufficient funds for {amount}")
        return False

# Two threads try to withdraw 80 from balance of 100
t1 = threading.Thread(target=withdraw, args=(80,))
t2 = threading.Thread(target=withdraw, args=(80,))

t1.start()
t2.start()
t1.join()
t2.join()

print(f"Final balance: {balance}")
# PROBLEM: Both may succeed, resulting in negative balance!
```

### What Happens

```
Time    Thread 1              Thread 2              Balance
──────────────────────────────────────────────────────────────
0       Check: 100 >= 80 ✓                           100
1                             Check: 100 >= 80 ✓     100
2       Withdraw 80                                   20
3                             Withdraw 80            -60  ← BUG!
```

### The Fix: Use Locks

```python
import threading

balance = 100
lock = threading.Lock()

def withdraw_safe(amount):
    global balance
    
    with lock:  # Atomic check-then-act
        if balance >= amount:
            balance -= amount
            print(f"Withdrew {amount}, balance: {balance}")
            return True
        else:
            print(f"Insufficient funds for {amount}")
            return False

# Now only one withdraw succeeds
t1 = threading.Thread(target=withdraw_safe, args=(80,))
t2 = threading.Thread(target=withdraw_safe, args=(80,))
t1.start()
t2.start()
t1.join()
t2.join()
# Final balance: 20 (correct!)
```

## Race Condition: Read-Modify-Write

### The Problem

```python
import threading

counter = 0

def increment():
    global counter
    for _ in range(100000):
        counter += 1  # Not atomic!

t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)

t1.start()
t2.start()
t1.join()
t2.join()

print(f"Counter: {counter}")
# Expected: 200000
# Actual: Often less (e.g., 134521)
```

### Why It Happens

`counter += 1` is three operations:

```python
# What looks atomic:
counter += 1

# Is actually:
temp = counter      # 1. READ
temp = temp + 1     # 2. MODIFY
counter = temp      # 3. WRITE

# Race condition timeline:
# Thread 1: READ counter (0)
# Thread 2: READ counter (0)  ← Same value!
# Thread 1: WRITE counter (1)
# Thread 2: WRITE counter (1)  ← Overwrites Thread 1's work!
```

### The Fix

```python
import threading

counter = 0
lock = threading.Lock()

def increment_safe():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1

# Now counter is always 200000
```

## Race Condition: Lazy Initialization

### The Problem (Singleton Pattern)

```python
import threading
import time

class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            # Race window!
            time.sleep(0.001)
            cls._instance = super().__new__(cls)
            cls._instance.value = 0
        return cls._instance

def create_singleton():
    s = Singleton()
    print(f"Got instance {id(s)}")
    return s

# Multiple threads may create multiple instances!
threads = [threading.Thread(target=create_singleton) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

### The Fix: Double-Checked Locking

```python
import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:  # First check (no lock)
            with cls._lock:
                if cls._instance is None:  # Second check (with lock)
                    cls._instance = super().__new__(cls)
                    cls._instance.value = 0
        return cls._instance
```

## Race Condition: Lost Update

### The Problem

```python
import threading

class Account:
    def __init__(self, balance):
        self.balance = balance

account = Account(1000)

def update_balance():
    # Read
    current = account.balance
    
    # Modify (simulate computation)
    new_balance = current + 100
    
    # Write
    account.balance = new_balance

threads = [threading.Thread(target=update_balance) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Balance: {account.balance}")
# Expected: 2000 (1000 + 10*100)
# Actual: Often 1100 or similar (updates lost)
```

### The Fix

```python
import threading

class Account:
    def __init__(self, balance):
        self.balance = balance
        self.lock = threading.Lock()
    
    def deposit(self, amount):
        with self.lock:
            self.balance += amount
```

## Race Condition: File Operations

### The Problem

```python
import threading
import os

def write_if_not_exists(filename, content):
    # CHECK
    if not os.path.exists(filename):
        # Race window: another thread may create file here!
        with open(filename, 'w') as f:
            f.write(content)
        return True
    return False

# Both threads may write!
t1 = threading.Thread(target=write_if_not_exists, args=("data.txt", "from thread 1"))
t2 = threading.Thread(target=write_if_not_exists, args=("data.txt", "from thread 2"))
```

### The Fix: Atomic File Operations

```python
import os
import tempfile

def write_if_not_exists_safe(filename, content):
    # Write to temp file first
    fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(filename))
    try:
        os.write(fd, content.encode())
        os.close(fd)
        
        # Atomic rename (fails if target exists on some systems)
        try:
            os.link(temp_path, filename)
            return True
        except FileExistsError:
            return False
    finally:
        os.unlink(temp_path)
```

## Race Condition: List Operations

### The Problem

```python
import threading

items = []

def append_items(start):
    for i in range(start, start + 100):
        items.append(i)  # Append is atomic in CPython, but...
        
        if len(items) > 50:  # Check-then-act race!
            # Another thread might append between check and here
            item = items.pop()  # Might pop wrong item

# Lists are not thread-safe for compound operations
```

### The Fix: Use Queue or Lock

```python
import threading
import queue

# Option 1: Use thread-safe queue
q = queue.Queue()

def safe_append(item):
    q.put(item)

def safe_pop():
    return q.get()

# Option 2: Lock for list operations
items = []
lock = threading.Lock()

def safe_list_operation():
    with lock:
        items.append("item")
        if len(items) > 50:
            items.pop()
```

## Race Condition: Dictionary Operations

### The Problem

```python
import threading

cache = {}

def get_or_compute(key):
    # CHECK
    if key not in cache:
        # Race: another thread may compute same value!
        result = expensive_computation(key)
        cache[key] = result
    return cache[key]
```

### The Fix

```python
import threading

cache = {}
cache_lock = threading.Lock()

def get_or_compute_safe(key):
    # First check without lock (optimization)
    if key in cache:
        return cache[key]
    
    with cache_lock:
        # Second check with lock
        if key not in cache:
            cache[key] = expensive_computation(key)
        return cache[key]
```

## Detecting Race Conditions

### 1. ThreadSanitizer (TSan)

For C extensions or when available:

```bash
# Compile Python with TSan support
./configure --with-thread-sanitizer
```

### 2. Stress Testing

```python
import threading
import random

def stress_test(target_func, num_threads=100, iterations=1000):
    """Run function from many threads to expose race conditions."""
    errors = []
    
    def worker():
        for _ in range(iterations):
            try:
                target_func()
            except Exception as e:
                errors.append(e)
            
            # Random sleep to vary timing
            if random.random() < 0.01:
                time.sleep(0.001)
    
    threads = [threading.Thread(target=worker) for _ in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    return errors
```

### 3. Adding Delays to Expose Races

```python
import threading
import time
import os

DEBUG_RACES = os.environ.get('DEBUG_RACES', False)

def potentially_racy_operation():
    check_condition()
    
    if DEBUG_RACES:
        time.sleep(0.1)  # Expose race window
    
    perform_action()
```

## Common Patterns to Avoid Races

### 1. Immutable Data

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    host: str
    port: int

# Can safely share across threads
config = Config("localhost", 8080)
```

### 2. Thread Confinement

```python
# Each thread works with its own data
def worker(data):
    # data is private to this thread
    process(data)
    return result

# Divide work, don't share
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor() as executor:
    results = executor.map(worker, data_chunks)
```

### 3. Message Passing

```python
import queue

# Instead of shared state, pass messages
work_queue = queue.Queue()
result_queue = queue.Queue()

def worker():
    while True:
        item = work_queue.get()
        if item is None:
            break
        result = process(item)
        result_queue.put(result)
```

## Key Takeaways

- Race conditions occur when timing affects correctness
- Common patterns: check-then-act, read-modify-write, lazy init
- **Fix**: Use locks to make compound operations atomic
- Prefer immutable data and message passing over shared mutable state
- Test with many threads and random delays to expose races
- Python's GIL doesn't prevent all race conditions
- When in doubt, use locks or thread-safe data structures

---

## Exercises

**Exercise 1.**
Create a shared counter and spawn 10 threads that each increment it 50,000 times without any lock. Run the program, print the final counter, and verify it is less than 500,000. Then add a `threading.Lock` to make the increment atomic and confirm the result is exactly 500,000.

??? success "Solution to Exercise 1"
        ```python
        import threading

        counter = 0

        def increment_unsafe():
            global counter
            for _ in range(50_000):
                counter += 1

        threads = [threading.Thread(target=increment_unsafe) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        print(f"Without lock: {counter} (expected 500000)")

        counter = 0
        lock = threading.Lock()

        def increment_safe():
            global counter
            for _ in range(50_000):
                with lock:
                    counter += 1

        threads = [threading.Thread(target=increment_safe) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        print(f"With lock: {counter} (expected 500000)")
        ```

---

**Exercise 2.**
Implement a thread-safe `BankAccount` class with `deposit(amount)` and `withdraw(amount)` methods that use a lock. Write a stress test that spawns 5 deposit threads (each depositing 1,000 times) and 5 withdrawal threads (each withdrawing 1,000 times) for the same amount. Verify that the final balance equals the initial balance.

??? success "Solution to Exercise 2"
        ```python
        import threading

        class BankAccount:
            def __init__(self, balance):
                self.balance = balance
                self.lock = threading.Lock()

            def deposit(self, amount):
                with self.lock:
                    self.balance += amount

            def withdraw(self, amount):
                with self.lock:
                    self.balance -= amount

        account = BankAccount(10_000)
        amount = 10

        def deposit_loop():
            for _ in range(1_000):
                account.deposit(amount)

        def withdraw_loop():
            for _ in range(1_000):
                account.withdraw(amount)

        threads = []
        for _ in range(5):
            threads.append(threading.Thread(target=deposit_loop))
            threads.append(threading.Thread(target=withdraw_loop))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        print(f"Final balance: {account.balance}")
        assert account.balance == 10_000, "Balance mismatch!"
        ```

---

**Exercise 3.**
Write a thread-safe lazy-initialized cache using double-checked locking. The `CachedComputation` class should have a method `get(key)` that computes and stores the result of a slow function on first access and returns the cached value thereafter. Verify with multiple threads that each key's function is computed exactly once by counting invocations with a `threading.Lock`-protected counter.

??? success "Solution to Exercise 3"
        ```python
        import threading
        import time

        class CachedComputation:
            def __init__(self, func):
                self._func = func
                self._cache = {}
                self._lock = threading.Lock()
                self.call_count = 0
                self._count_lock = threading.Lock()

            def get(self, key):
                if key in self._cache:
                    return self._cache[key]
                with self._lock:
                    if key not in self._cache:
                        with self._count_lock:
                            self.call_count += 1
                        self._cache[key] = self._func(key)
                return self._cache[key]

        def slow_square(x):
            time.sleep(0.01)
            return x * x

        cache = CachedComputation(slow_square)

        def worker(keys):
            for k in keys:
                cache.get(k)

        keys = list(range(10)) * 5  # each key requested 5 times
        threads = [threading.Thread(target=worker, args=(keys,)) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        print(f"Total computations: {cache.call_count} (expected 10)")
        assert cache.call_count == 10
        ```
