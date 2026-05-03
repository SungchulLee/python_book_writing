# Future Objects

A `Future` represents the result of an asynchronous operation. It's returned by `executor.submit()` and provides methods to check status, get results, and handle completion.

!!! tip "Mental Model"
    A Future is a claim ticket for work being done elsewhere. When you call `submit()`, you get the ticket immediately and can keep doing other things. Call `result()` to redeem the ticket -- if the work is done you get the answer instantly, otherwise you block until it is ready. You can also check `done()`, set timeouts, or attach callbacks to be notified automatically.

---

## What is a Future?

A `Future` is a **placeholder for a result** that will be available later:

```python
from concurrent.futures import ThreadPoolExecutor
import time

def slow_computation(x):
    time.sleep(2)
    return x ** 2

with ThreadPoolExecutor() as executor:
    # submit() returns Future immediately
    future = executor.submit(slow_computation, 10)
    
    print(f"Future created: {future}")
    print(f"Done: {future.done()}")  # False (still running)
    
    # Do other work while waiting...
    
    result = future.result()  # Blocks until complete
    print(f"Result: {result}")  # 100
```

---

## Future Methods

### result() — Get the Result

```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import time

def slow_task():
    time.sleep(2)
    return 42

with ThreadPoolExecutor() as executor:
    future = executor.submit(slow_task)
    
    # Blocks until result ready
    result = future.result()
    print(result)  # 42
    
    # With timeout
    future2 = executor.submit(slow_task)
    try:
        result = future2.result(timeout=1)  # Wait max 1 second
    except TimeoutError:
        print("Timed out!")
```

### exception() — Get Exception

```python
from concurrent.futures import ThreadPoolExecutor

def failing_task():
    raise ValueError("Something went wrong!")

with ThreadPoolExecutor() as executor:
    future = executor.submit(failing_task)
    
    # Wait for completion
    future.result()  # This would raise the exception
    
    # Or check exception directly
    exc = future.exception()  # Returns ValueError or None
    if exc:
        print(f"Task failed: {exc}")
```

### done() — Check if Complete

```python
from concurrent.futures import ThreadPoolExecutor
import time

def slow_task():
    time.sleep(2)
    return "done"

with ThreadPoolExecutor() as executor:
    future = executor.submit(slow_task)
    
    while not future.done():
        print("Still working...")
        time.sleep(0.5)
    
    print(f"Result: {future.result()}")
```

### running() — Check if Running

```python
from concurrent.futures import ThreadPoolExecutor
import time

def task():
    time.sleep(1)
    return "done"

with ThreadPoolExecutor(max_workers=1) as executor:
    future1 = executor.submit(task)
    future2 = executor.submit(task)  # Queued, not running yet
    
    print(f"Future1 running: {future1.running()}")  # True
    print(f"Future2 running: {future2.running()}")  # False (queued)
```

### cancelled() — Check if Cancelled

```python
from concurrent.futures import ThreadPoolExecutor
import time

def task():
    time.sleep(5)
    return "done"

with ThreadPoolExecutor(max_workers=1) as executor:
    future1 = executor.submit(task)  # Starts immediately
    future2 = executor.submit(task)  # Queued
    
    # Try to cancel (only works if not yet started)
    cancelled = future2.cancel()
    print(f"Cancel succeeded: {cancelled}")
    print(f"Future2 cancelled: {future2.cancelled()}")
```

### cancel() — Try to Cancel

```python
from concurrent.futures import ThreadPoolExecutor
import time

def long_task():
    time.sleep(10)
    return "done"

with ThreadPoolExecutor(max_workers=1) as executor:
    future1 = executor.submit(long_task)  # Running
    future2 = executor.submit(long_task)  # Queued
    future3 = executor.submit(long_task)  # Queued
    
    # Can't cancel running task
    print(future1.cancel())  # False
    
    # Can cancel queued task
    print(future2.cancel())  # True
    print(future3.cancel())  # True
```

---

## Adding Callbacks

Execute a function when the Future completes:

```python
from concurrent.futures import ThreadPoolExecutor
import time

def compute(x):
    time.sleep(1)
    return x ** 2

def on_complete(future):
    """Called when future completes."""
    try:
        result = future.result()
        print(f"Computation finished: {result}")
    except Exception as e:
        print(f"Computation failed: {e}")

with ThreadPoolExecutor() as executor:
    future = executor.submit(compute, 10)
    future.add_done_callback(on_complete)
    
    print("Doing other work...")
    time.sleep(2)
```

### Multiple Callbacks

```python
from concurrent.futures import ThreadPoolExecutor

def task():
    return 42

def callback1(future):
    print(f"Callback 1: {future.result()}")

def callback2(future):
    print(f"Callback 2: {future.result()}")

def callback3(future):
    print(f"Callback 3: {future.result()}")

with ThreadPoolExecutor() as executor:
    future = executor.submit(task)
    
    # Multiple callbacks (called in order added)
    future.add_done_callback(callback1)
    future.add_done_callback(callback2)
    future.add_done_callback(callback3)
```

---

## Working with Multiple Futures

### as_completed() — Process in Completion Order

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

def task(task_id):
    delay = random.uniform(0.5, 2.0)
    time.sleep(delay)
    return (task_id, delay)

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(task, i) for i in range(10)]
    
    # Process results as they complete
    for future in as_completed(futures):
        task_id, delay = future.result()
        print(f"Task {task_id} completed (took {delay:.2f}s)")
```

### wait() — Wait for Conditions

```python
from concurrent.futures import ThreadPoolExecutor, wait
from concurrent.futures import FIRST_COMPLETED, FIRST_EXCEPTION, ALL_COMPLETED
import time

def task(x):
    time.sleep(x)
    return x

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(task, i) for i in [3, 1, 2]]
    
    # Wait for first completion
    done, not_done = wait(futures, return_when=FIRST_COMPLETED)
    print(f"First done: {done.pop().result()}")
    
    # Wait for all
    done, not_done = wait(futures, return_when=ALL_COMPLETED)
    print(f"All results: {[f.result() for f in done]}")
```

### Collecting Results with Mapping

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def process(x):
    return x ** 2

with ThreadPoolExecutor() as executor:
    # Map futures to their input
    future_to_input = {executor.submit(process, x): x for x in range(10)}
    
    results = {}
    for future in as_completed(future_to_input):
        input_val = future_to_input[future]
        try:
            results[input_val] = future.result()
        except Exception as e:
            results[input_val] = f"Error: {e}"
    
    print(results)
```

---

## Error Handling with Futures

### Exception in result()

```python
from concurrent.futures import ThreadPoolExecutor

def risky_task(x):
    if x < 0:
        raise ValueError("Negative not allowed")
    return x ** 2

with ThreadPoolExecutor() as executor:
    future = executor.submit(risky_task, -5)
    
    try:
        result = future.result()
    except ValueError as e:
        print(f"Task failed: {e}")
```

### Check Exception First

```python
from concurrent.futures import ThreadPoolExecutor

def risky_task(x):
    if x < 0:
        raise ValueError("Negative!")
    return x ** 2

with ThreadPoolExecutor() as executor:
    future = executor.submit(risky_task, -5)
    
    # Wait for completion
    while not future.done():
        pass
    
    # Check for exception without raising
    exc = future.exception()
    if exc:
        print(f"Failed: {exc}")
    else:
        print(f"Success: {future.result()}")
```

### Error Handling in Callbacks

```python
from concurrent.futures import ThreadPoolExecutor

def task():
    raise RuntimeError("Oops!")

def handle_result(future):
    try:
        result = future.result()
        print(f"Success: {result}")
    except Exception as e:
        print(f"Failed: {e}")

with ThreadPoolExecutor() as executor:
    future = executor.submit(task)
    future.add_done_callback(handle_result)
```

---

## Practical Patterns

### Progress Tracking

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def task(x):
    time.sleep(0.5)
    return x ** 2

items = list(range(20))
total = len(items)

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(task, x) for x in items]
    
    completed = 0
    for future in as_completed(futures):
        completed += 1
        print(f"Progress: {completed}/{total} ({100*completed/total:.0f}%)")
```

### Timeout with Cancellation

```python
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import time

def slow_task(x):
    time.sleep(x)
    return x

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(slow_task, i) for i in [1, 5, 2, 8, 1]]
    
    completed_results = []
    try:
        for future in as_completed(futures, timeout=3):
            completed_results.append(future.result())
    except TimeoutError:
        print("Timeout! Cancelling remaining tasks...")
        for future in futures:
            future.cancel()
    
    print(f"Completed: {completed_results}")
```

### Chaining Futures (Manual)

```python
from concurrent.futures import ThreadPoolExecutor

def step1(x):
    return x + 1

def step2(x):
    return x * 2

def step3(x):
    return x ** 2

with ThreadPoolExecutor() as executor:
    # Chain: step1 -> step2 -> step3
    future1 = executor.submit(step1, 5)
    
    def chain_step2(future):
        result = future.result()
        future2 = executor.submit(step2, result)
        future2.add_done_callback(chain_step3)
    
    def chain_step3(future):
        result = future.result()
        future3 = executor.submit(step3, result)
        future3.add_done_callback(lambda f: print(f"Final: {f.result()}"))
    
    future1.add_done_callback(chain_step2)
    
    # Wait for completion
    import time
    time.sleep(1)
```

---

## Future State Diagram

```
                    ┌──────────────┐
                    │   PENDING    │
                    │   (queued)   │
                    └──────┬───────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
        cancel()       start()         cancel()
        (success)                      (fails)
           │               │               │
           ▼               ▼               │
    ┌──────────────┐ ┌──────────────┐     │
    │  CANCELLED   │ │   RUNNING    │     │
    └──────────────┘ └──────┬───────┘     │
                           │               │
                ┌──────────┴──────────┐   │
                │                     │   │
            complete()            exception()
                │                     │
                ▼                     ▼
         ┌──────────────┐     ┌──────────────┐
         │   FINISHED   │     │   FINISHED   │
         │  (success)   │     │   (error)    │
         └──────────────┘     └──────────────┘
```

---

## Key Takeaways

- `Future` represents a pending result from `executor.submit()`
- `result()` blocks until complete (or timeout)
- `done()` checks completion without blocking
- `cancel()` only works for **queued** tasks, not running ones
- `add_done_callback()` for async result handling
- `as_completed()` processes futures in completion order
- `wait()` waits for specific conditions (first, all, exception)
- Always handle exceptions in `result()` or use `exception()`
- Map futures to inputs for result tracking

---

## Exercises

**Exercise 1.**
Submit 10 tasks using `executor.submit()` where each task sleeps for a random duration (0.1-1.0s) and returns its task ID. Add a `done_callback` to each future that prints a message when the task completes. Use `as_completed()` to collect and print all results in completion order.

??? success "Solution to Exercise 1"
        ```python
        import time
        import random
        from concurrent.futures import ThreadPoolExecutor, as_completed

        def task(tid):
            time.sleep(random.uniform(0.1, 1.0))
            return tid

        def on_done(future):
            print(f"  Callback: task {future.result()} finished")

        with ThreadPoolExecutor(max_workers=4) as ex:
            futures = {}
            for i in range(10):
                f = ex.submit(task, i)
                f.add_done_callback(on_done)
                futures[f] = i

            for f in as_completed(futures):
                print(f"  Completed: task {f.result()}")
        ```

---

**Exercise 2.**
Write a progress tracker. Submit 20 tasks to a `ThreadPoolExecutor` (each sleeping 0.2-0.8s). Use `as_completed()` to print progress like "5/20 complete (25%)" as each task finishes.

??? success "Solution to Exercise 2"
        ```python
        import time
        import random
        from concurrent.futures import ThreadPoolExecutor, as_completed

        def work(x):
            time.sleep(random.uniform(0.2, 0.8))
            return x

        total = 20
        with ThreadPoolExecutor(max_workers=5) as ex:
            futs = [ex.submit(work, i) for i in range(total)]
            done_count = 0
            for f in as_completed(futs):
                done_count += 1
                pct = 100 * done_count / total
                print(f"{done_count}/{total} complete ({pct:.0f}%)")
        ```

---

**Exercise 3.**
Demonstrate `future.cancel()`. Submit 5 tasks to an executor with `max_workers=1` (so only 1 runs at a time, others are queued). Immediately try to cancel the last 3. Print which cancellations succeeded, then collect results for the tasks that ran.

??? success "Solution to Exercise 3"
        ```python
        import time
        from concurrent.futures import ThreadPoolExecutor

        def slow(x):
            time.sleep(1)
            return x * 10

        with ThreadPoolExecutor(max_workers=1) as ex:
            futures = [ex.submit(slow, i) for i in range(5)]

            for i in range(2, 5):
                ok = futures[i].cancel()
                print(f"Cancel task {i}: {'success' if ok else 'failed'}")

            for i, f in enumerate(futures):
                if f.cancelled():
                    print(f"Task {i}: cancelled")
                else:
                    print(f"Task {i}: result = {f.result()}")
        ```
