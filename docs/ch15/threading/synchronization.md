# Thread Synchronization

When multiple threads access shared data, synchronization is essential to prevent race conditions and ensure data integrity.

!!! tip "Mental Model"
    Synchronization primitives are traffic signals for threads. A `Lock` is a single-occupancy bathroom door -- only one thread enters at a time. An `RLock` lets the same thread re-enter. A `Semaphore` is a parking garage with limited spots. An `Event` is a starting gun that all waiting threads hear at once. Pick the lightest primitive that solves your coordination problem.

---

## The Problem: Race Conditions

### Without Synchronization

```python
import threading

counter = 0

def increment():
    global counter
    for _ in range(100_000):
        counter += 1  # Not atomic!

# Create two threads
t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)

t1.start()
t2.start()
t1.join()
t2.join()

print(f"Expected: 200000")
print(f"Actual: {counter}")  # Often less than 200000!
```

### Why It Happens

`counter += 1` is not atomic — it's actually three operations:

```python
# What looks like one operation:
counter += 1

# Is actually:
temp = counter      # 1. Read current value
temp = temp + 1     # 2. Increment
counter = temp      # 3. Write back

# Thread 1: Read counter (0)
# Thread 2: Read counter (0)  ← Same value!
# Thread 1: Write counter (1)
# Thread 2: Write counter (1)  ← Overwrites Thread 1's work!
```

---

## Lock (Mutex)

A `Lock` ensures only one thread can execute a section of code at a time.

### Basic Lock Usage

```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100_000):
        lock.acquire()       # Get the lock
        try:
            counter += 1
        finally:
            lock.release()   # Always release!

t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)

t1.start()
t2.start()
t1.join()
t2.join()

print(f"Counter: {counter}")  # Always 200000
```

### Lock as Context Manager (Recommended)

```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100_000):
        with lock:           # Automatically acquires and releases
            counter += 1

t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)

t1.start()
t2.start()
t1.join()
t2.join()

print(f"Counter: {counter}")  # Always 200000
```

### Non-Blocking Lock Acquisition

```python
import threading
import time

lock = threading.Lock()

def try_acquire():
    if lock.acquire(blocking=False):
        try:
            print(f"{threading.current_thread().name}: Got lock")
            time.sleep(1)
        finally:
            lock.release()
    else:
        print(f"{threading.current_thread().name}: Lock busy, skipping")

# With timeout
def try_acquire_timeout():
    if lock.acquire(timeout=0.5):
        try:
            print(f"{threading.current_thread().name}: Got lock")
            time.sleep(1)
        finally:
            lock.release()
    else:
        print(f"{threading.current_thread().name}: Timeout")
```

---

## RLock (Reentrant Lock)

A regular `Lock` cannot be acquired twice by the same thread. `RLock` allows the same thread to acquire it multiple times.

### The Problem with Regular Lock

```python
import threading

lock = threading.Lock()

def outer():
    with lock:
        print("Outer acquired lock")
        inner()  # Deadlock! Lock already held

def inner():
    with lock:  # Blocks forever waiting for lock
        print("Inner acquired lock")

# This will deadlock with regular Lock
```

### RLock Solution

```python
import threading

rlock = threading.RLock()

def outer():
    with rlock:
        print("Outer acquired lock")
        inner()

def inner():
    with rlock:  # Same thread can acquire again
        print("Inner acquired lock")

outer()  # Works!
# Output:
# Outer acquired lock
# Inner acquired lock
```

### When to Use RLock

```python
import threading

class BankAccount:
    def __init__(self, balance):
        self.balance = balance
        self.lock = threading.RLock()  # Use RLock for recursive access
    
    def deposit(self, amount):
        with self.lock:
            self.balance += amount
    
    def withdraw(self, amount):
        with self.lock:
            if self.balance >= amount:
                self.balance -= amount
                return True
            return False
    
    def transfer(self, other, amount):
        with self.lock:  # First acquisition
            if self.withdraw(amount):  # Second acquisition (same lock)
                other.deposit(amount)
                return True
            return False
```

---

## Semaphore

A `Semaphore` allows a limited number of threads to access a resource simultaneously.

### Basic Semaphore

```python
import threading
import time

# Allow max 3 concurrent accesses
semaphore = threading.Semaphore(3)

def worker(worker_id):
    print(f"Worker {worker_id}: Waiting for semaphore")
    with semaphore:
        print(f"Worker {worker_id}: Acquired semaphore")
        time.sleep(2)  # Simulate work
        print(f"Worker {worker_id}: Releasing semaphore")

# Start 10 workers, but only 3 run at a time
threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

### Practical Example: Connection Pool

```python
import threading
import time
import random

class ConnectionPool:
    def __init__(self, max_connections):
        self.semaphore = threading.Semaphore(max_connections)
        self.connections = [f"conn_{i}" for i in range(max_connections)]
        self.lock = threading.Lock()
    
    def get_connection(self):
        self.semaphore.acquire()
        with self.lock:
            conn = self.connections.pop()
        return conn
    
    def release_connection(self, conn):
        with self.lock:
            self.connections.append(conn)
        self.semaphore.release()

pool = ConnectionPool(3)

def database_query(query_id):
    conn = pool.get_connection()
    try:
        print(f"Query {query_id}: Using {conn}")
        time.sleep(random.uniform(0.5, 1.5))
    finally:
        pool.release_connection(conn)
        print(f"Query {query_id}: Released {conn}")

threads = [threading.Thread(target=database_query, args=(i,)) for i in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

### BoundedSemaphore

Raises error if released more times than acquired:

```python
import threading

# Regular semaphore: no error on extra release
sem = threading.Semaphore(2)
sem.release()
sem.release()
sem.release()  # No error, but counter is now 5!

# BoundedSemaphore: catches bugs
bsem = threading.BoundedSemaphore(2)
bsem.release()  # ValueError: Semaphore released too many times
```

---

## Event

An `Event` is a simple flag that threads can wait on.

### Basic Event Usage

```python
import threading
import time

event = threading.Event()

def waiter(name):
    print(f"{name}: Waiting for event...")
    event.wait()  # Block until event is set
    print(f"{name}: Event received!")

def setter():
    print("Setter: Preparing...")
    time.sleep(2)
    print("Setter: Setting event")
    event.set()

# Start waiters
for i in range(3):
    threading.Thread(target=waiter, args=(f"Waiter-{i}",)).start()

# Start setter
threading.Thread(target=setter).start()
```

### Event Methods

```python
import threading

event = threading.Event()

# Check if set
print(event.is_set())  # False

# Wait with timeout
result = event.wait(timeout=1.0)  # Returns True if set, False on timeout

# Set the event (wake all waiting threads)
event.set()
print(event.is_set())  # True

# Clear the event
event.clear()
print(event.is_set())  # False
```

### Practical Example: Startup Coordination

```python
import threading
import time

db_ready = threading.Event()
cache_ready = threading.Event()

def init_database():
    print("Database: Initializing...")
    time.sleep(2)
    print("Database: Ready")
    db_ready.set()

def init_cache():
    print("Cache: Waiting for database...")
    db_ready.wait()  # Cache depends on database
    print("Cache: Initializing...")
    time.sleep(1)
    print("Cache: Ready")
    cache_ready.set()

def main_app():
    print("App: Waiting for all services...")
    db_ready.wait()
    cache_ready.wait()
    print("App: All services ready, starting...")

threading.Thread(target=init_database).start()
threading.Thread(target=init_cache).start()
threading.Thread(target=main_app).start()
```

---

## Condition

A `Condition` combines a lock with the ability to wait for a condition to be true.

### Basic Condition Usage

```python
import threading
import time

condition = threading.Condition()
items = []

def producer():
    for i in range(5):
        time.sleep(0.5)
        with condition:
            items.append(f"item-{i}")
            print(f"Produced: item-{i}")
            condition.notify()  # Wake up one waiting consumer

def consumer():
    while True:
        with condition:
            while not items:  # Wait until items available
                print("Consumer: Waiting...")
                condition.wait()
            item = items.pop(0)
            print(f"Consumed: {item}")
        
        if item == "item-4":
            break

threading.Thread(target=producer).start()
threading.Thread(target=consumer).start()
```

### Producer-Consumer Pattern

```python
import threading
import time
import random

class BoundedBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = []
        self.condition = threading.Condition()
    
    def put(self, item):
        with self.condition:
            while len(self.buffer) >= self.capacity:
                print(f"Buffer full, producer waiting...")
                self.condition.wait()
            
            self.buffer.append(item)
            print(f"Produced: {item}, buffer size: {len(self.buffer)}")
            self.condition.notify_all()
    
    def get(self):
        with self.condition:
            while len(self.buffer) == 0:
                print(f"Buffer empty, consumer waiting...")
                self.condition.wait()
            
            item = self.buffer.pop(0)
            print(f"Consumed: {item}, buffer size: {len(self.buffer)}")
            self.condition.notify_all()
            return item

buffer = BoundedBuffer(capacity=3)

def producer(producer_id):
    for i in range(5):
        time.sleep(random.uniform(0.1, 0.5))
        buffer.put(f"P{producer_id}-{i}")

def consumer(consumer_id):
    for _ in range(5):
        time.sleep(random.uniform(0.1, 0.5))
        buffer.get()

# 2 producers, 2 consumers
threads = []
for i in range(2):
    threads.append(threading.Thread(target=producer, args=(i,)))
    threads.append(threading.Thread(target=consumer, args=(i,)))

for t in threads:
    t.start()
for t in threads:
    t.join()
```

---

## Barrier

A `Barrier` synchronizes a fixed number of threads at a certain point.

```python
import threading
import time
import random

barrier = threading.Barrier(3)

def worker(worker_id):
    # Phase 1: Each thread does independent work
    work_time = random.uniform(0.5, 2.0)
    print(f"Worker {worker_id}: Working for {work_time:.1f}s")
    time.sleep(work_time)
    
    # Synchronization point
    print(f"Worker {worker_id}: Reached barrier, waiting...")
    barrier.wait()  # All threads must reach here before any continue
    
    # Phase 2: Continue after all threads synchronized
    print(f"Worker {worker_id}: Continuing after barrier")

threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

---

## Summary: Synchronization Primitives

| Primitive | Purpose | Use Case |
|-----------|---------|----------|
| **Lock** | Mutual exclusion | Protect shared data |
| **RLock** | Reentrant mutual exclusion | Recursive functions with locks |
| **Semaphore** | Limit concurrent access | Connection pools, rate limiting |
| **Event** | Simple signaling | Start/stop signals, coordination |
| **Condition** | Wait for complex conditions | Producer-consumer, state changes |
| **Barrier** | Synchronize multiple threads | Phased computation |

---

## Key Takeaways

- **Always** use synchronization when multiple threads access shared mutable data
- Use `with lock:` syntax for automatic acquisition and release
- `Lock` for simple mutual exclusion, `RLock` for recursive access
- `Semaphore` to limit concurrent resource access
- `Event` for simple signaling between threads
- `Condition` for complex waiting conditions (producer-consumer)
- `Barrier` to synchronize threads at specific points
- Avoid holding locks longer than necessary to prevent contention

---

## Runnable Example: `thread_safety_tutorial.py`

```python
"""
Topic 45.5 - Thread Safety and Synchronization

Complete guide to making your code thread-safe using locks, semaphores,
events, and other synchronization primitives.

Learning Objectives:
- Understand race conditions
- Use Locks and RLocks for mutual exclusion
- Apply Semaphores for resource limiting
- Use Events for signaling
- Implement Conditions for complex coordination
- Understand Barriers for synchronization points
- Thread-safe data structures

Author: Python Educator
Date: 2024
"""

import threading
import time
import random
from queue import Queue
from threading import Lock, RLock, Semaphore, Event, Condition, Barrier


# ============================================================================
# PART 1: BEGINNER - Race Conditions and Locks
# ============================================================================

def demonstrate_race_condition():
    """
    Show what happens WITHOUT thread safety - race conditions occur!
    """
    print("=" * 70)
    print("BEGINNER: Understanding Race Conditions")
    print("=" * 70)
    
    # Shared counter (NOT thread-safe!)
    counter = 0
    
    def increment_counter():
        """Increment shared counter 100,000 times"""
        nonlocal counter
        for _ in range(100000):
            # This is NOT atomic! It's actually:
            # 1. Read counter
            # 2. Add 1
            # 3. Write back
            # Threads can interleave between these steps!
            counter += 1
    
    print("\n❌ WITHOUT synchronization:")
    print("   Running 5 threads, each incrementing counter 100,000 times")
    print("   Expected final value: 500,000\n")
    
    # Reset counter
    counter = 0
    
    # Create threads
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=increment_counter)
        threads.append(thread)
        thread.start()
    
    # Wait for all
    for thread in threads:
        thread.join()
    
    print(f"   Actual final value: {counter}")
    
    if counter != 500000:
        print(f"   ⚠️  Lost updates! {500000 - counter} increments were lost!")
        print("   This is a RACE CONDITION - multiple threads racing to update")
    else:
        print("   ✓ Got lucky this time, but this is still unsafe!")
    
    print("\n💡 What went wrong:")
    print("   Thread A: reads 100, adds 1, writes 101")
    print("   Thread B: reads 100 (before A wrote!), adds 1, writes 101")
    print("   Result: Only increased by 1 instead of 2!")
    
    print("\n" + "=" * 70 + "\n")


def fixing_with_lock():
    """
    Fix race conditions using a Lock for mutual exclusion.
    """
    print("=" * 70)
    print("BEGINNER: Fixing Race Conditions with Lock")
    print("=" * 70)
    
    # Shared counter with lock
    counter = 0
    counter_lock = Lock()  # Create a lock
    
    def increment_counter_safe():
        """Increment counter safely using lock"""
        nonlocal counter
        for _ in range(100000):
            # Acquire lock before accessing shared resource
            counter_lock.acquire()
            try:
                counter += 1  # Only one thread can be here at a time
            finally:
                # ALWAYS release the lock
                counter_lock.release()
    
    print("\n✓ WITH Lock synchronization:")
    print("   Running 5 threads, each incrementing counter 100,000 times")
    print("   Expected final value: 500,000\n")
    
    # Create threads
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=increment_counter_safe)
        threads.append(thread)
        thread.start()
    
    # Wait for all
    for thread in threads:
        thread.join()
    
    print(f"   Final value: {counter}")
    
    if counter == 500000:
        print("   ✓ Perfect! Lock prevented race conditions")
    
    print("\n💡 How Lock works:")
    print("   • Only ONE thread can hold the lock at a time")
    print("   • Other threads WAIT until lock is released")
    print("   • Ensures mutual exclusion (mutex)")
    
    print("\n" + "=" * 70 + "\n")


def lock_with_context_manager():
    """
    Use 'with' statement for automatic lock management.
    This is the recommended way to use locks!
    """
    print("=" * 70)
    print("BEGINNER: Lock with Context Manager (Best Practice)")
    print("=" * 70)
    
    # Shared resource
    balance = 1000
    balance_lock = Lock()
    
    def withdraw_money(amount):
        """Safely withdraw money from balance"""
        nonlocal balance
        
        # Context manager automatically acquires and releases lock
        with balance_lock:
            # Critical section
            if balance >= amount:
                print(f"  [{threading.current_thread().name}] "
                      f"Withdrawing ${amount}")
                time.sleep(0.1)  # Simulate processing
                balance -= amount
                print(f"  [{threading.current_thread().name}] "
                      f"Remaining: ${balance}")
                return True
            else:
                print(f"  [{threading.current_thread().name}] "
                      f"Insufficient funds!")
                return False
        # Lock automatically released here!
    
    print(f"\n💰 Initial balance: ${balance}")
    print("   Multiple threads trying to withdraw...\n")
    
    # Multiple threads try to withdraw
    threads = []
    for i in range(5):
        thread = threading.Thread(
            target=withdraw_money,
            args=(300,),
            name=f"Customer-{i+1}"
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all
    for thread in threads:
        thread.join()
    
    print(f"\n💰 Final balance: ${balance}")
    
    print("\n💡 Context Manager Benefits:")
    print("   ✓ Lock automatically released (even if exception occurs)")
    print("   ✓ Cleaner, more readable code")
    print("   ✓ Can't forget to release lock")
    print("   ✓ ALWAYS use 'with lock:' instead of acquire/release")
    
    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 2: INTERMEDIATE - Advanced Synchronization Primitives
# ============================================================================

def reentrant_lock_example():
    """
    RLock (Reentrant Lock) can be acquired multiple times by same thread.
    Useful for recursive functions or nested lock acquisitions.
    """
    print("=" * 70)
    print("INTERMEDIATE: RLock (Reentrant Lock)")
    print("=" * 70)
    
    # Regular Lock vs RLock
    regular_lock = Lock()
    rlock = RLock()
    
    print("\n📝 Regular Lock - DEADLOCK if acquired twice:")
    
    def bad_recursive(n):
        """This will deadlock with regular Lock!"""
        with regular_lock:
            if n > 0:
                # Can't acquire lock again - deadlock!
                # Uncomment to see deadlock:
                # with regular_lock:  
                #     bad_recursive(n - 1)
                pass
    
    print("   (Commented out to avoid deadlock)")
    
    print("\n📝 RLock - OK to acquire multiple times:")
    
    def good_recursive(n):
        """Works fine with RLock"""
        with rlock:
            if n > 0:
                print(f"  Recursion level {n} (lock acquired {4-n+1} times)")
                good_recursive(n - 1)
    
    good_recursive(3)
    
    print("\n💡 When to use RLock:")
    print("   ✓ Recursive functions that need locking")
    print("   ✓ Methods that call other locked methods")
    print("   ✓ Same thread needs to acquire lock multiple times")
    print("   ✗ Slightly slower than regular Lock")
    
    print("\n" + "=" * 70 + "\n")


def semaphore_resource_limiting():
    """
    Semaphore limits concurrent access to a resource.
    Like a lock, but allows N threads instead of just 1.
    """
    print("=" * 70)
    print("INTERMEDIATE: Semaphore for Resource Limiting")
    print("=" * 70)
    
    # Allow max 3 concurrent database connections
    db_connections = Semaphore(3)
    
    def access_database(user_id):
        """
        Simulate database access with limited connections.
        
        Args:
            user_id: User identifier
        """
        print(f"  User {user_id}: Requesting database access...")
        
        with db_connections:  # Acquire one permit
            print(f"  User {user_id}: ✓ Connected to database")
            time.sleep(random.uniform(1.0, 2.0))  # Simulate query
            print(f"  User {user_id}: Disconnected")
        # Permit automatically released
    
    print("\n⚙️  10 users trying to access database")
    print("   (Only 3 concurrent connections allowed)\n")
    
    threads = []
    for i in range(10):
        thread = threading.Thread(target=access_database, args=(i+1,))
        threads.append(thread)
        thread.start()
        time.sleep(0.2)  # Stagger requests
    
    # Wait for all
    for thread in threads:
        thread.join()
    
    print("\n💡 Semaphore use cases:")
    print("   ✓ Limit concurrent API calls")
    print("   ✓ Database connection pool")
    print("   ✓ Rate limiting")
    print("   ✓ Resource pool management")
    
    print("\n" + "=" * 70 + "\n")


def event_signaling():
    """
    Event allows threads to signal each other.
    One thread waits for an event, another thread sets it.
    """
    print("=" * 70)
    print("INTERMEDIATE: Event for Thread Signaling")
    print("=" * 70)
    
    # Event starts as "not set"
    ready_event = Event()
    data_ready = Event()
    
    def producer():
        """Produce data and signal when ready"""
        print("  [Producer] Preparing data...")
        time.sleep(2)  # Simulate preparation
        
        print("  [Producer] Data ready! Signaling consumers...")
        data_ready.set()  # Signal that data is ready
        
        # Wait for consumers to be ready for next batch
        ready_event.wait()
        print("  [Producer] Consumers ready for next batch")
    
    def consumer(consumer_id):
        """Wait for data, then process it"""
        print(f"  [Consumer {consumer_id}] Waiting for data...")
        
        # Wait for data_ready event
        data_ready.wait()
        
        print(f"  [Consumer {consumer_id}] Got data! Processing...")
        time.sleep(1)
        print(f"  [Consumer {consumer_id}] Done processing")
        
        # Signal ready for next batch
        if consumer_id == 3:  # Last consumer signals
            ready_event.set()
    
    print("\n⚙️  Starting producer-consumer with Event:\n")
    
    # Start producer
    prod_thread = threading.Thread(target=producer)
    prod_thread.start()
    
    # Start consumers
    cons_threads = []
    for i in range(3):
        thread = threading.Thread(target=consumer, args=(i+1,))
        cons_threads.append(thread)
        thread.start()
    
    # Wait for all
    prod_thread.join()
    for thread in cons_threads:
        thread.join()
    
    print("\n💡 Event methods:")
    print("   • set() - Signal the event (wake waiters)")
    print("   • clear() - Reset the event")
    print("   • wait() - Block until event is set")
    print("   • is_set() - Check if event is set")
    
    print("\n" + "=" * 70 + "\n")


def condition_variable_example():
    """
    Condition allows complex wait conditions with notify.
    More powerful than Event for producer-consumer patterns.
    """
    print("=" * 70)
    print("INTERMEDIATE: Condition for Complex Coordination")
    print("=" * 70)
    
    # Shared data with condition
    buffer = []
    max_size = 5
    condition = Condition()
    
    def producer(items):
        """Produce items when buffer has space"""
        for item in items:
            with condition:
                # Wait while buffer is full
                while len(buffer) >= max_size:
                    print(f"  [Producer] Buffer full, waiting...")
                    condition.wait()  # Release lock and wait
                
                # Add item
                buffer.append(item)
                print(f"  [Producer] Added {item}. Buffer: {len(buffer)}")
                
                # Notify consumers
                condition.notify()  # Wake one waiting thread
        
        print("  [Producer] Finished")
    
    def consumer(num_items):
        """Consume items when buffer has data"""
        consumed = 0
        while consumed < num_items:
            with condition:
                # Wait while buffer is empty
                while len(buffer) == 0:
                    print(f"  [Consumer] Buffer empty, waiting...")
                    condition.wait()
                
                # Remove item
                item = buffer.pop(0)
                consumed += 1
                print(f"  [Consumer] Got {item}. Buffer: {len(buffer)}")
                
                # Notify producers
                condition.notify()  # Wake one waiting thread
        
        print("  [Consumer] Finished")
    
    print("\n⚙️  Producer-Consumer with Condition:\n")
    
    # Start threads
    items_to_produce = [f"Item-{i}" for i in range(15)]
    
    prod = threading.Thread(target=producer, args=(items_to_produce,))
    cons = threading.Thread(target=consumer, args=(len(items_to_produce),))
    
    cons.start()
    time.sleep(0.5)  # Let consumer start waiting
    prod.start()
    
    prod.join()
    cons.join()
    
    print("\n💡 Condition advantages:")
    print("   ✓ Efficient waiting (no busy polling)")
    print("   ✓ notify() to wake specific waiters")
    print("   ✓ notify_all() to wake all waiters")
    print("   ✓ Perfect for producer-consumer with bounded buffer")
    
    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 3: ADVANCED - Complex Synchronization Patterns
# ============================================================================

def barrier_synchronization():
    """
    Barrier ensures all threads reach a certain point before continuing.
    Useful for phases of parallel algorithms.
    """
    print("=" * 70)
    print("ADVANCED: Barrier for Synchronization Points")
    print("=" * 70)
    
    num_workers = 4
    barrier = Barrier(num_workers)
    
    def parallel_phase_worker(worker_id):
        """
        Worker that goes through multiple synchronized phases.
        
        Args:
            worker_id: Worker identifier
        """
        # Phase 1: Data loading
        print(f"  [Worker {worker_id}] Phase 1: Loading data...")
        time.sleep(random.uniform(0.5, 1.5))
        print(f"  [Worker {worker_id}] Data loaded")
        
        # Wait for all workers to finish Phase 1
        barrier.wait()
        print(f"  [Worker {worker_id}] ✓ Phase 1 complete for all")
        
        # Phase 2: Processing
        print(f"  [Worker {worker_id}] Phase 2: Processing...")
        time.sleep(random.uniform(0.5, 1.5))
        print(f"  [Worker {worker_id}] Processing done")
        
        # Wait for all workers to finish Phase 2
        barrier.wait()
        print(f"  [Worker {worker_id}] ✓ Phase 2 complete for all")
        
        # Phase 3: Saving results
        print(f"  [Worker {worker_id}] Phase 3: Saving results...")
        time.sleep(random.uniform(0.3, 0.8))
        print(f"  [Worker {worker_id}] Results saved")
        
        # Final barrier
        barrier.wait()
        print(f"  [Worker {worker_id}] ✓ All phases complete!")
    
    print(f"\n⚙️  Running {num_workers} workers through 3 phases:\n")
    
    threads = []
    for i in range(num_workers):
        thread = threading.Thread(target=parallel_phase_worker, args=(i+1,))
        threads.append(thread)
        thread.start()
    
    # Wait for all
    for thread in threads:
        thread.join()
    
    print("\n💡 Barrier use cases:")
    print("   ✓ Parallel algorithms with phases")
    print("   ✓ Map-reduce operations")
    print("   ✓ Distributed computing checkpoints")
    print("   ✓ Game loop synchronization")
    
    print("\n" + "=" * 70 + "\n")


def thread_safe_singleton_pattern():
    """
    Implement thread-safe Singleton pattern with double-checked locking.
    """
    print("=" * 70)
    print("ADVANCED: Thread-Safe Singleton Pattern")
    print("=" * 70)
    
    class DatabaseConnection:
        """Thread-safe singleton database connection"""
        
        _instance = None
        _lock = Lock()
        
        def __new__(cls):
            # First check (without lock for performance)
            if cls._instance is None:
                # Acquire lock
                with cls._lock:
                    # Second check (with lock for safety)
                    if cls._instance is None:
                        print("  Creating NEW database connection...")
                        time.sleep(0.5)  # Simulate slow initialization
                        cls._instance = super().__new__(cls)
                        cls._instance.connection_id = random.randint(1000, 9999)
            
            return cls._instance
        
        def query(self, sql):
            """Execute a query"""
            return f"Query result from connection {self.connection_id}"
    
    def worker(worker_id):
        """Worker that gets database connection"""
        print(f"  [Worker {worker_id}] Getting database connection...")
        db = DatabaseConnection()
        print(f"  [Worker {worker_id}] Got connection: {db.connection_id}")
        
        # Use connection
        result = db.query("SELECT * FROM users")
        print(f"  [Worker {worker_id}] {result}")
    
    print("\n⚙️  Multiple threads requesting singleton:\n")
    
    threads = []
    for i in range(5):
        thread = threading.Thread(target=worker, args=(i+1,))
        threads.append(thread)
        thread.start()
    
    # Wait for all
    for thread in threads:
        thread.join()
    
    print("\n💡 Double-checked locking:")
    print("   ✓ First check avoids lock overhead")
    print("   ✓ Second check ensures thread safety")
    print("   ✓ Only one instance created despite concurrent access")
    
    print("\n" + "=" * 70 + "\n")


def deadlock_example_and_prevention():
    """
    Demonstrate deadlock and how to prevent it.
    """
    print("=" * 70)
    print("ADVANCED: Deadlock and Prevention")
    print("=" * 70)
    
    lock_a = Lock()
    lock_b = Lock()
    
    def thread1_bad():
        """Can cause deadlock"""
        with lock_a:
            print("  Thread1: Acquired Lock A")
            time.sleep(0.1)
            # Trying to acquire lock B while holding A
            with lock_b:
                print("  Thread1: Acquired Lock B")
    
    def thread2_bad():
        """Can cause deadlock"""
        with lock_b:
            print("  Thread2: Acquired Lock B")
            time.sleep(0.1)
            # Trying to acquire lock A while holding B
            with lock_a:
                print("  Thread2: Acquired Lock A")
    
    print("\n❌ Deadlock scenario (NOT executed to avoid hanging):")
    print("   Thread 1: locks A, waits for B")
    print("   Thread 2: locks B, waits for A")
    print("   → Both threads wait forever!")
    
    # Good: Always acquire locks in same order
    def thread1_good():
        """Deadlock-free version"""
        with lock_a:  # Always lock A first
            print("  Thread1: Acquired Lock A")
            time.sleep(0.1)
            with lock_b:  # Then lock B
                print("  Thread1: Acquired Lock B")
                print("  Thread1: ✓ Completed safely")
    
    def thread2_good():
        """Deadlock-free version"""
        with lock_a:  # Always lock A first (same order!)
            print("  Thread2: Acquired Lock A")
            time.sleep(0.1)
            with lock_b:  # Then lock B
                print("  Thread2: Acquired Lock B")
                print("  Thread2: ✓ Completed safely")
    
    print("\n✓ Deadlock-free execution (same lock order):\n")
    
    t1 = threading.Thread(target=thread1_good)
    t2 = threading.Thread(target=thread2_good)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    print("\n💡 Deadlock prevention strategies:")
    print("   1. Always acquire locks in the same order")
    print("   2. Use timeout on lock acquisition")
    print("   3. Use a single lock instead of multiple")
    print("   4. Avoid nested locking when possible")
    print("   5. Use higher-level abstractions (Queue, etc.)")
    
    print("\n" + "=" * 70 + "\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run all thread safety demonstrations."""
    print("\n" + "=" * 70)
    print(" " * 18 + "THREAD SAFETY")
    print(" " * 12 + "Synchronization and Race Conditions")
    print("=" * 70 + "\n")
    
    # Beginner level
    demonstrate_race_condition()
    fixing_with_lock()
    lock_with_context_manager()
    
    # Intermediate level
    reentrant_lock_example()
    semaphore_resource_limiting()
    event_signaling()
    condition_variable_example()
    
    # Advanced level
    barrier_synchronization()
    thread_safe_singleton_pattern()
    deadlock_example_and_prevention()
    
    print("\n" + "=" * 70)
    print("Thread Safety Tutorial Complete!")
    print("=" * 70)
    print("\n💡 Key Takeaways:")
    print("1. Always use locks for shared mutable state")
    print("2. Use 'with lock:' for automatic release")
    print("3. RLock for recursive/nested locking")
    print("4. Semaphore for limiting concurrent access")
    print("5. Event for simple signaling")
    print("6. Condition for complex coordination")
    print("7. Barrier for phase synchronization")
    print("8. Prevent deadlocks with consistent lock ordering")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
```

---

## Exercises

**Exercise 1.**
Create a `BoundedSemaphore(3)` that limits access to a simulated resource. Spawn 10 threads that each acquire the semaphore, print their worker ID and a timestamp, sleep for 0.5 seconds, then release. Verify (by inspecting timestamps) that no more than 3 workers are active simultaneously.

??? success "Solution to Exercise 1"
        ```python
        import threading
        import time

        sem = threading.BoundedSemaphore(3)

        def worker(wid):
            sem.acquire()
            try:
                print(f"Worker {wid} entered at {time.perf_counter():.2f}")
                time.sleep(0.5)
                print(f"Worker {wid} leaving at {time.perf_counter():.2f}")
            finally:
                sem.release()

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        print("All workers done.")
        ```

---

**Exercise 2.**
Use a `threading.Barrier(4)` to coordinate 4 worker threads that each go through two phases: (1) "data loading" (random sleep 0.5-1.5s), barrier wait, (2) "processing" (random sleep 0.3-1.0s), barrier wait. Print start and finish messages for each phase so you can confirm all workers synchronize between phases.

??? success "Solution to Exercise 2"
        ```python
        import threading
        import time
        import random

        barrier = threading.Barrier(4)

        def worker(wid):
            # Phase 1
            print(f"Worker {wid}: loading data...")
            time.sleep(random.uniform(0.5, 1.5))
            print(f"Worker {wid}: data loaded, waiting at barrier")
            barrier.wait()
            print(f"Worker {wid}: Phase 1 complete for all")

            # Phase 2
            print(f"Worker {wid}: processing...")
            time.sleep(random.uniform(0.3, 1.0))
            print(f"Worker {wid}: processing done, waiting at barrier")
            barrier.wait()
            print(f"Worker {wid}: Phase 2 complete for all")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        print("All phases done.")
        ```

---

**Exercise 3.**
Implement a thread-safe bounded buffer using `threading.Condition`. The buffer has a maximum size of 5. Write a producer that inserts 20 items and a consumer that removes 20 items. The producer waits when the buffer is full; the consumer waits when the buffer is empty. Print the buffer size after each operation and verify no items are lost.

??? success "Solution to Exercise 3"
        ```python
        import threading
        import time

        class BoundedBuffer:
            def __init__(self, capacity):
                self.capacity = capacity
                self.buffer = []
                self.condition = threading.Condition()

            def put(self, item):
                with self.condition:
                    while len(self.buffer) >= self.capacity:
                        self.condition.wait()
                    self.buffer.append(item)
                    print(f"  Produced {item}, size={len(self.buffer)}")
                    self.condition.notify()

            def get(self):
                with self.condition:
                    while len(self.buffer) == 0:
                        self.condition.wait()
                    item = self.buffer.pop(0)
                    print(f"  Consumed {item}, size={len(self.buffer)}")
                    self.condition.notify()
                    return item

        buf = BoundedBuffer(5)

        def producer():
            for i in range(20):
                buf.put(i)
                time.sleep(0.02)

        def consumer():
            for _ in range(20):
                buf.get()
                time.sleep(0.03)

        t1 = threading.Thread(target=producer)
        t2 = threading.Thread(target=consumer)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print(f"Buffer empty: {len(buf.buffer) == 0}")
        ```
