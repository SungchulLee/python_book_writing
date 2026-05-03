# Thread-Local Storage

`threading.local()` provides storage where each thread has its own independent copy of data.

!!! tip "Mental Model"
    `threading.local()` gives every thread its own private namespace that looks like a shared object. Each thread reads and writes the same attribute names, but they see different values -- like each employee having a personal desk drawer inside a shared desk. It is the simplest way to avoid sharing state without passing data through every function call.

## The Problem: Shared State

Without thread-local storage, all threads share the same global variables:

```python
import threading
import time

# Global variable - shared by all threads
request_id = None

def handle_request(req_id):
    global request_id
    request_id = req_id
    time.sleep(0.1)  # Simulate processing
    # BUG: request_id may have been overwritten by another thread!
    print(f"Processing request {request_id}")

threads = []
for i in range(5):
    t = threading.Thread(target=handle_request, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# Output might show wrong request IDs!
```

## Solution: threading.local()

Each thread gets its own copy of the data:

```python
import threading
import time

# Thread-local storage
local_data = threading.local()

def handle_request(req_id):
    local_data.request_id = req_id
    time.sleep(0.1)
    # Each thread sees its own request_id
    print(f"Thread {threading.current_thread().name}: request {local_data.request_id}")

threads = []
for i in range(5):
    t = threading.Thread(target=handle_request, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# Output: Each thread shows its correct request_id
```

## How It Works

```python
import threading

local = threading.local()

def show_value():
    thread_name = threading.current_thread().name
    if hasattr(local, 'value'):
        print(f"{thread_name}: value = {local.value}")
    else:
        print(f"{thread_name}: no value set")

def set_value(val):
    local.value = val
    show_value()

# Main thread
local.value = "main"
show_value()  # main: value = main

# Other threads don't see main's value
t1 = threading.Thread(target=show_value, name="Thread-1")
t1.start()
t1.join()  # Thread-1: no value set

# Each thread sets its own value
t2 = threading.Thread(target=set_value, args=("thread2",), name="Thread-2")
t2.start()
t2.join()  # Thread-2: value = thread2

# Main thread's value unchanged
show_value()  # main: value = main
```

## Practical Examples

### 1. Request Context in Web Server

```python
import threading
from contextlib import contextmanager

# Thread-local request context
_request_context = threading.local()

@contextmanager
def request_context(request_id, user_id):
    """Set request context for current thread."""
    _request_context.request_id = request_id
    _request_context.user_id = user_id
    try:
        yield
    finally:
        del _request_context.request_id
        del _request_context.user_id

def get_current_user():
    """Get user from current request context."""
    return getattr(_request_context, 'user_id', None)

def get_request_id():
    """Get current request ID."""
    return getattr(_request_context, 'request_id', None)

def process_data():
    user = get_current_user()
    req = get_request_id()
    print(f"Processing for user {user} (request {req})")

def handle_request(request_id, user_id):
    with request_context(request_id, user_id):
        process_data()

# Simulate concurrent requests
threads = []
for i in range(3):
    t = threading.Thread(target=handle_request, args=(f"req-{i}", f"user-{i}"))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

### 2. Database Connection Per Thread

```python
import threading
import sqlite3

class ThreadLocalDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self._local = threading.local()
    
    @property
    def connection(self):
        """Get connection for current thread, create if needed."""
        if not hasattr(self._local, 'conn'):
            self._local.conn = sqlite3.connect(self.db_path)
        return self._local.conn
    
    def execute(self, query, params=()):
        """Execute query on thread's connection."""
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    
    def close(self):
        """Close current thread's connection."""
        if hasattr(self._local, 'conn'):
            self._local.conn.close()
            del self._local.conn

# Usage
db = ThreadLocalDB('mydb.sqlite')

def worker(worker_id):
    # Each thread gets its own connection
    db.execute("INSERT INTO logs VALUES (?)", (f"worker-{worker_id}",))
    db.connection.commit()

threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

### 3. Logging Context

```python
import threading
import logging

class ContextFilter(logging.Filter):
    """Add thread-local context to log records."""
    
    def __init__(self):
        super().__init__()
        self._local = threading.local()
    
    def set_context(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self._local, key, value)
    
    def clear_context(self):
        self._local.__dict__.clear()
    
    def filter(self, record):
        for key, value in self._local.__dict__.items():
            setattr(record, key, value)
        return True

# Setup
context_filter = ContextFilter()
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '%(asctime)s [%(request_id)s] %(message)s'
))
handler.addFilter(context_filter)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def process_request(request_id):
    context_filter.set_context(request_id=request_id)
    try:
        logger.info("Starting request")
        # ... do work ...
        logger.info("Request completed")
    finally:
        context_filter.clear_context()
```

### 4. Transaction Scope

```python
import threading
from contextlib import contextmanager

class TransactionManager:
    def __init__(self):
        self._local = threading.local()
    
    @property
    def current_transaction(self):
        return getattr(self._local, 'transaction', None)
    
    @contextmanager
    def transaction(self):
        if self.current_transaction is not None:
            raise RuntimeError("Nested transactions not supported")
        
        self._local.transaction = Transaction()
        try:
            yield self._local.transaction
            self._local.transaction.commit()
        except Exception:
            self._local.transaction.rollback()
            raise
        finally:
            del self._local.transaction

class Transaction:
    def __init__(self):
        self.operations = []
    
    def add(self, op):
        self.operations.append(op)
    
    def commit(self):
        print(f"Committing {len(self.operations)} operations")
    
    def rollback(self):
        print("Rolling back")

# Usage
tm = TransactionManager()

def worker(worker_id):
    with tm.transaction() as txn:
        txn.add(f"operation from worker {worker_id}")

threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

## Subclassing threading.local

For initialization logic, subclass `threading.local`:

```python
import threading

class MyLocal(threading.local):
    def __init__(self, default_value):
        # Called once per thread when first accessed
        self.value = default_value
        self.initialized = True

local = MyLocal("default")

def show():
    print(f"{threading.current_thread().name}: {local.value}")

# Main thread
show()  # MainThread: default
local.value = "main"
show()  # MainThread: main

# New thread gets fresh default
t = threading.Thread(target=show)
t.start()
t.join()  # Thread-1: default
```

## Important Considerations

### Data is Thread-Specific, Not Task-Specific

Thread-local data persists for the lifetime of the thread:

```python
import threading
from concurrent.futures import ThreadPoolExecutor

local = threading.local()

def task(task_id):
    # May see leftover data from previous task on same thread!
    old = getattr(local, 'task_id', 'none')
    local.task_id = task_id
    return f"Task {task_id} (previous: {old})"

with ThreadPoolExecutor(max_workers=2) as executor:
    results = list(executor.map(task, range(10)))
    print(results)
# Tasks reuse threads, so they may see previous task's data
```

### Cleanup Pattern

```python
def task_with_cleanup(task_id):
    local.task_id = task_id
    try:
        # ... do work ...
        pass
    finally:
        del local.task_id  # Clean up
```

## threading.local vs contextvars

| Feature | threading.local | contextvars |
|---------|-----------------|-------------|
| Thread isolation | ✅ | ✅ |
| Async task isolation | ❌ | ✅ |
| Copy on task creation | ❌ | ✅ |
| Python version | 2.4+ | 3.7+ |

For async code, use `contextvars` instead.

## Key Takeaways

- `threading.local()` provides thread-isolated storage
- Each thread sees its own copy of attributes
- Useful for request context, connections, transactions
- Data persists for thread lifetime (clean up in thread pools)
- For async code, use `contextvars` instead
- Subclass for custom initialization logic

---

## Runnable Example: `thread_event_pattern.py`

```python
"""
TUTORIAL: Using threading.Event for Thread Coordination
========================================================

In this tutorial, you'll learn how to use threading.Event as a simple but
powerful synchronization mechanism for coordinating threads.

KEY CONCEPTS:
- threading.Event: A simple flag-like object for thread communication
- event.set() and event.wait(): Basic signaling mechanism
- Practical pattern: Using events to signal threads to stop gracefully
- Real-world example: Animated spinner that responds to task completion

CREDITS: Adapted from Michele Simionato's example in python-list:
https://mail.python.org/pipermail/python-list/2009-February/675659.html
"""

import itertools
import time
from threading import Thread, Event


print("=" * 70)
print("THREADING.EVENT FOR THREAD COORDINATION")
print("=" * 70)
print()


# ============ EXAMPLE 1: Understanding threading.Event
# =====================================================

print("EXAMPLE 1: What is threading.Event?")
print("-" * 70)
print()
print("threading.Event is like a simple 'flag' that threads can use to")
print("communicate with each other. It has two states: set or unset.")
print()

event = Event()
print(f"• Created an event: {event}")
print(f"• Is it set? {event.is_set()}")
print()

# When we call event.set(), the flag becomes True
event.set()
print(f"After event.set():")
print(f"• Is it set now? {event.is_set()}")
print()

# When we call event.clear(), the flag becomes False again
event.clear()
print(f"After event.clear():")
print(f"• Is it set now? {event.is_set()}")
print()


# ============ EXAMPLE 2: The Spinner Function - Showing Activity
# ================================================================

print("EXAMPLE 2: Creating a Spinner Thread")
print("-" * 70)
print()
print("A spinner shows the user that work is happening. We use an Event")
print("to let the spinner know when the work is complete so it can stop.")
print()


def spin(msg: str, done: Event) -> None:
    """
    Display an animated spinner while work is being done.

    WHY THIS DESIGN:
    - itertools.cycle creates a never-ending loop of characters
    - done.wait(timeout) checks if work is finished every 0.1 seconds
    - Using \r (carriage return) overwrites the same line for animation
    - flush=True ensures output appears immediately

    Args:
        msg: The message to display next to the spinner
        done: An Event that signals when to stop spinning
    """
    print(f"\nStarting spinner with message: '{msg}'")
    print("(Watch the animation below - it's cycling through characters)")
    print()

    spinner_chars = r'\|/-'
    char_count = 0

    for char in itertools.cycle(spinner_chars):
        # WHY cycle()? It lets us loop through 4 characters infinitely.
        # When we reach the end, it automatically starts over.

        status = f'\r{char} {msg}'
        print(status, end='', flush=True)

        # done.wait(0.1) does two things:
        # 1. Waits up to 0.1 seconds for the event to be set
        # 2. Returns True if event was set, False if timeout occurred
        if done.wait(0.1):
            # The event was set! This means we should stop spinning.
            break

        char_count += 1

    # Clear the spinner line so it doesn't stay visible
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')

    print(f"Spinner stopped after {char_count} iterations")
    print()


def slow_task() -> int:
    """
    Simulate a long-running task that takes 3 seconds.

    WHY: This represents real work - downloading, processing, etc.
    We'll run the spinner while this happens.
    """
    print("Long task: Starting 3-second sleep...")
    time.sleep(3)
    print("Long task: Finished!")
    return 42


# ============ EXAMPLE 3: The Supervisor - Coordinating Threads
# ==============================================================

print("EXAMPLE 3: Coordinating Threads with an Event")
print("-" * 70)
print()
print("The supervisor orchestrates two things:")
print("1. A worker thread (spinner) showing progress")
print("2. The main thread doing the actual work")
print("Both use an Event to coordinate.")
print()


def supervisor() -> int:
    """
    Manage the spinner thread and the work.

    WHY THIS PATTERN:
    - done Event starts as unset (clear). This tells spinner: keep spinning!
    - We start() the spinner thread to run in parallel
    - Main thread calls slow_task() to do the actual work
    - When work is done, we call done.set() to stop the spinner
    - We join() to wait for the spinner thread to fully exit

    This is a clean, safe way to coordinate threads.
    """

    # Create an Event object. It starts in the "unset" state.
    done = Event()

    # Create a Thread object that will run the spin() function
    # We pass the message and the Event object
    spinner = Thread(target=spin, args=('thinking!', done))

    print(f"Created spinner thread: {spinner}")
    print()

    # Start the spinner thread. It now runs in parallel with this code.
    spinner.start()
    print("Spinner thread started (running in parallel now)")
    print()

    # Do the work. Meanwhile, the spinner thread is still animating.
    result = slow_task()

    # Now tell the spinner to stop by setting the event
    done.set()
    print("Main thread: Set the done event (telling spinner to stop)")
    print()

    # Wait for the spinner thread to fully finish
    spinner.join()
    print("Main thread: Joined with spinner thread (both are done now)")
    print()

    return result


# ============ EXAMPLE 4: Running the Full Demo
# ==============================================

def main() -> None:
    """Run the complete demonstration."""
    print("EXAMPLE 4: Running the Full Demonstration")
    print("-" * 70)
    print()

    result = supervisor()

    print()
    print("=" * 70)
    print(f"RESULT: The answer is {result}")
    print("=" * 70)


# ============ EXAMPLE 5: Key Takeaways
# ======================================

print()
print("=" * 70)
print("KEY CONCEPTS TO REMEMBER:")
print("=" * 70)
print()
print("1. threading.Event is like a flag threads can check/set")
print()
print("2. event.set() signals 'True' - work is done, stop waiting")
print("3. event.wait(timeout) pauses until set or timeout, returns bool")
print()
print("4. This pattern is much safer than forcefully killing threads")
print()
print("5. Perfect for: progress indicators, graceful shutdown, signals")
print()
print("=" * 70)
print()


if __name__ == '__main__':
    main()
```

---

## Exercises

**Exercise 1.**
Demonstrate the difference between a global variable and `threading.local()`. Create a global `request_id` and a `threading.local()` with a `request_id` attribute. Spawn 5 threads that each set both to their thread number, sleep for 0.1 seconds, then print both values. Show that the global variable is overwritten while the thread-local variable retains the correct value.

??? success "Solution to Exercise 1"
        ```python
        import threading
        import time

        global_req_id = None
        local_data = threading.local()

        def worker(tid):
            global global_req_id
            global_req_id = tid
            local_data.request_id = tid
            time.sleep(0.1)
            print(f"Thread {tid}: global={global_req_id}, "
                  f"local={local_data.request_id}")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # global_req_id may show wrong value; local always correct
        ```

---

**Exercise 2.**
Implement a `ThreadLocalDB` class that lazily creates one `sqlite3` in-memory connection per thread. Write a method `execute(sql, params)` that uses the thread's connection. Spawn 3 threads that each create a table with a unique name, insert a row, and query it back. Verify each thread only sees its own table.

??? success "Solution to Exercise 2"
        ```python
        import threading
        import sqlite3

        class ThreadLocalDB:
            def __init__(self):
                self._local = threading.local()

            @property
            def connection(self):
                if not hasattr(self._local, 'conn'):
                    self._local.conn = sqlite3.connect(':memory:')
                return self._local.conn

            def execute(self, sql, params=()):
                cur = self.connection.cursor()
                cur.execute(sql, params)
                self.connection.commit()
                return cur.fetchall()

        db = ThreadLocalDB()

        def worker(wid):
            table = f"t_{wid}"
            db.execute(f"CREATE TABLE {table} (val TEXT)")
            db.execute(f"INSERT INTO {table} VALUES (?)", (f"data-{wid}",))
            rows = db.execute(f"SELECT * FROM {table}")
            print(f"Thread {wid}: {rows}")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        ```

---

**Exercise 3.**
Write a `request_context` context manager using `threading.local()` that stores `user_id` and `request_id`. Write helper functions `get_user()` and `get_request()` that read from the context. Spawn 4 threads that each enter a context with different values, call a `process()` function that reads and prints both values, then exit the context. Verify there is no cross-thread leakage.

??? success "Solution to Exercise 3"
        ```python
        import threading
        from contextlib import contextmanager

        _ctx = threading.local()

        @contextmanager
        def request_context(user_id, request_id):
            _ctx.user_id = user_id
            _ctx.request_id = request_id
            try:
                yield
            finally:
                del _ctx.user_id
                del _ctx.request_id

        def get_user():
            return getattr(_ctx, 'user_id', None)

        def get_request():
            return getattr(_ctx, 'request_id', None)

        def process():
            print(f"  [{threading.current_thread().name}] "
                  f"user={get_user()}, request={get_request()}")

        def handler(uid, rid):
            with request_context(uid, rid):
                process()
            assert get_user() is None  # cleaned up

        threads = [
            threading.Thread(target=handler, args=(f"user{i}", f"req{i}"))
            for i in range(4)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        print("No cross-thread leakage.")
        ```
