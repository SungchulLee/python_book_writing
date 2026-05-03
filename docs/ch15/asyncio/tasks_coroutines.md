# Tasks and Coroutines

!!! tip "Mental Model"
    A coroutine is a recipe -- calling it creates an object that describes what to do, but doesn't do it yet. A Task is what actually runs that recipe by scheduling it on the event loop. You need `create_task()` to get true concurrency: without it, `await`-ing coroutines one by one runs them sequentially.

## Coroutines

A **coroutine** is a function defined with `async def`. When called, it returns a coroutine object that must be awaited or scheduled.

```python
async def my_coroutine():
    await asyncio.sleep(1)
    return "result"

# Calling creates a coroutine object (doesn't run it)
coro = my_coroutine()
print(type(coro))  # <class 'coroutine'>

# Must run it
result = asyncio.run(my_coroutine())
```

### Coroutine States

```
Created → Running → Suspended → Running → ... → Completed
           ↑           │
           └───────────┘
              (await)
```

---

## Tasks

A **Task** wraps a coroutine and schedules it for execution. Tasks enable concurrent execution.

```python
async def main():
    # Create a task - starts running immediately
    task = asyncio.create_task(my_coroutine())
    
    # Do other work while task runs...
    
    # Get the result when needed
    result = await task
```

### Coroutine vs Task

| Aspect | Coroutine | Task |
|--------|-----------|------|
| Created by | `async def` call | `asyncio.create_task()` |
| Starts running | When awaited | Immediately when created |
| Concurrent | No (sequential) | Yes |
| Can be cancelled | No | Yes |

---

## Creating Tasks

### asyncio.create_task() (Preferred)

```python
async def fetch(url):
    await asyncio.sleep(1)
    return f"Data from {url}"

async def main():
    # Create tasks - both start immediately
    task1 = asyncio.create_task(fetch("url1"))
    task2 = asyncio.create_task(fetch("url2"))
    
    # Tasks are running concurrently now
    print("Tasks created and running...")
    
    # Await results
    result1 = await task1
    result2 = await task2
    
    print(result1, result2)

asyncio.run(main())
```

### Named Tasks (Python 3.8+)

```python
task = asyncio.create_task(fetch("url"), name="fetch_task")
print(task.get_name())  # "fetch_task"
```

### asyncio.ensure_future() (Legacy)

```python
# Works but create_task() is preferred
task = asyncio.ensure_future(my_coroutine())
```

---

## Running Multiple Tasks

### asyncio.gather()

Run multiple coroutines concurrently and collect results:

```python
async def fetch(url):
    await asyncio.sleep(1)
    return f"Data from {url}"

async def main():
    # Run all concurrently, get results in order
    results = await asyncio.gather(
        fetch("url1"),
        fetch("url2"),
        fetch("url3")
    )
    print(results)  # ["Data from url1", "Data from url2", "Data from url3"]

asyncio.run(main())  # Takes ~1 second, not 3
```

#### Handling Exceptions in gather()

```python
async def might_fail(n):
    if n == 2:
        raise ValueError("Error!")
    return n

async def main():
    # Default: first exception cancels others
    try:
        results = await asyncio.gather(
            might_fail(1),
            might_fail(2),
            might_fail(3)
        )
    except ValueError as e:
        print(f"Caught: {e}")

    # With return_exceptions=True: exceptions returned as results
    results = await asyncio.gather(
        might_fail(1),
        might_fail(2),
        might_fail(3),
        return_exceptions=True
    )
    print(results)  # [1, ValueError("Error!"), 3]
```

### asyncio.wait()

More control over completion:

```python
async def main():
    tasks = [
        asyncio.create_task(fetch("url1")),
        asyncio.create_task(fetch("url2")),
        asyncio.create_task(fetch("url3"))
    ]
    
    # Wait for all
    done, pending = await asyncio.wait(tasks)
    
    for task in done:
        print(task.result())
```

#### Wait Options

```python
# Wait for first to complete
done, pending = await asyncio.wait(
    tasks, 
    return_when=asyncio.FIRST_COMPLETED
)

# Wait for first exception
done, pending = await asyncio.wait(
    tasks,
    return_when=asyncio.FIRST_EXCEPTION
)

# Wait with timeout
done, pending = await asyncio.wait(tasks, timeout=5.0)
```

### asyncio.as_completed()

Process results as they complete:

```python
async def main():
    tasks = [
        asyncio.create_task(fetch("slow", 3)),
        asyncio.create_task(fetch("fast", 1)),
        asyncio.create_task(fetch("medium", 2))
    ]
    
    # Yields tasks in completion order
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"Got result: {result}")

# Output (order by completion):
# Got result: Data from fast
# Got result: Data from medium
# Got result: Data from slow
```

---

## Task Cancellation

### Cancelling a Task

```python
async def long_running():
    try:
        await asyncio.sleep(10)
        return "completed"
    except asyncio.CancelledError:
        print("Task was cancelled!")
        raise  # Re-raise to properly cancel

async def main():
    task = asyncio.create_task(long_running())
    
    await asyncio.sleep(1)
    task.cancel()  # Request cancellation
    
    try:
        await task
    except asyncio.CancelledError:
        print("Caught cancellation")

asyncio.run(main())
```

### Handling Cancellation

```python
async def cleanup_on_cancel():
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        # Perform cleanup
        print("Cleaning up...")
        await save_state()
        raise  # Always re-raise CancelledError
```

### Shielding from Cancellation

```python
async def critical_operation():
    await asyncio.sleep(1)
    return "important result"

async def main():
    task = asyncio.create_task(critical_operation())
    
    # Shield prevents cancellation from propagating
    try:
        result = await asyncio.shield(task)
    except asyncio.CancelledError:
        # Original task continues running
        result = await task
```

---

## Task Introspection

### Task Properties

```python
async def main():
    task = asyncio.create_task(fetch("url"), name="my_fetch")
    
    print(task.get_name())       # "my_fetch"
    print(task.done())           # False
    print(task.cancelled())      # False
    
    await task
    
    print(task.done())           # True
    print(task.result())         # "Data from url"
```

### Getting All Tasks

```python
async def main():
    task1 = asyncio.create_task(fetch("url1"))
    task2 = asyncio.create_task(fetch("url2"))
    
    # Get all running tasks
    all_tasks = asyncio.all_tasks()
    print(f"Running tasks: {len(all_tasks)}")  # 3 (including main)
    
    # Get current task
    current = asyncio.current_task()
    print(f"Current: {current.get_name()}")
```

---

## Timeouts

### asyncio.wait_for()

```python
async def slow_operation():
    await asyncio.sleep(10)
    return "result"

async def main():
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=2.0)
    except asyncio.TimeoutError:
        print("Operation timed out!")

asyncio.run(main())
```

### asyncio.timeout() (Python 3.11+)

```python
async def main():
    async with asyncio.timeout(2.0):
        await slow_operation()  # Raises TimeoutError if > 2 seconds
```

### Timeout with Cleanup

```python
async def main():
    task = asyncio.create_task(slow_operation())
    
    try:
        result = await asyncio.wait_for(task, timeout=2.0)
    except asyncio.TimeoutError:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        print("Cleaned up after timeout")
```

---

## TaskGroup (Python 3.11+)

Modern way to manage multiple tasks with proper cleanup:

```python
async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch("url1"))
        task2 = tg.create_task(fetch("url2"))
        task3 = tg.create_task(fetch("url3"))
    
    # All tasks are done here
    # If any task raises, all others are cancelled
    print(task1.result(), task2.result(), task3.result())
```

### TaskGroup vs gather()

| Feature | TaskGroup | gather() |
|---------|-----------|----------|
| Python version | 3.11+ | 3.4+ |
| Exception handling | Cancels all on first error | Configurable |
| Context manager | Yes | No |
| Structured concurrency | Yes | No |

---

## Common Patterns

### Fire and Forget (Background Task)

```python
async def background_job():
    await asyncio.sleep(5)
    print("Background job done")

async def main():
    # Start task but don't await
    task = asyncio.create_task(background_job())
    
    # Continue with other work
    print("Main work...")
    
    # Optionally wait at the end
    await task
```

### Task with Callback

```python
def task_done_callback(task):
    if task.exception():
        print(f"Task failed: {task.exception()}")
    else:
        print(f"Task result: {task.result()}")

async def main():
    task = asyncio.create_task(fetch("url"))
    task.add_done_callback(task_done_callback)
    await task
```

### Limiting Concurrency

```python
async def fetch_with_semaphore(sem, url):
    async with sem:  # Limit concurrent requests
        return await fetch(url)

async def main():
    sem = asyncio.Semaphore(10)  # Max 10 concurrent
    
    urls = [f"url{i}" for i in range(100)]
    tasks = [fetch_with_semaphore(sem, url) for url in urls]
    results = await asyncio.gather(*tasks)
```

---

## Summary

| Function | Purpose |
|----------|---------|
| `asyncio.create_task()` | Create task from coroutine |
| `asyncio.gather()` | Run multiple, collect results |
| `asyncio.wait()` | Run multiple, control completion |
| `asyncio.as_completed()` | Iterate in completion order |
| `asyncio.wait_for()` | Run with timeout |
| `asyncio.shield()` | Protect from cancellation |
| `task.cancel()` | Cancel a task |
| `task.result()` | Get task result |
| `asyncio.TaskGroup` | Structured concurrency (3.11+) |

**Key Takeaways**:

- Tasks enable concurrent execution of coroutines
- `create_task()` starts execution immediately
- `gather()` is the simplest way to run multiple tasks
- Always handle `CancelledError` in long-running tasks
- Use timeouts to prevent hanging
- TaskGroup (3.11+) provides structured concurrency

---

## Runnable Example: `coroutine_prime_filter_example.py`

```python
"""
Asyncio: Coroutines with asyncio.gather()

Demonstrates concurrent coroutines running cooperative tasks.
Two async tasks (prime filtering and square mapping) run
concurrently using asyncio.gather().

Topics covered:
- async/await syntax
- asyncio.gather() for concurrent coroutines
- yield from for delegation to sub-generators
- Cooperative multitasking with await asyncio.sleep()

Based on concepts from Python-100-Days example23 and ch14/asyncio materials.
"""

import asyncio
from math import sqrt


# =============================================================================
# Example 1: Helper Functions
# =============================================================================

def is_prime(num: int) -> bool:
    """Check if a number is prime."""
    if num < 2:
        return False
    for factor in range(2, int(sqrt(num)) + 1):
        if num % factor == 0:
            return False
    return True


def number_range(start: int, end: int):
    """Generator that yields numbers in range.

    Using 'yield from' to delegate to range().
    """
    yield from range(start, end + 1)


# =============================================================================
# Example 2: Concurrent Coroutines
# =============================================================================

async def prime_filter(start: int, end: int) -> tuple[int, ...]:
    """Async coroutine that filters prime numbers from a range.

    The await asyncio.sleep(0) call yields control to the event loop,
    allowing other coroutines to run. This is cooperative multitasking.
    """
    primes = []
    for n in number_range(start, end):
        if is_prime(n):
            primes.append(n)
        # Yield control to event loop periodically
        if n % 10 == 0:
            await asyncio.sleep(0)
    return tuple(primes)


async def square_mapper(start: int, end: int) -> list[int]:
    """Async coroutine that computes squares of numbers in a range."""
    squares = []
    for n in number_range(start, end):
        squares.append(n * n)
        if n % 10 == 0:
            await asyncio.sleep(0)
    return squares


# =============================================================================
# Example 3: Running Coroutines Concurrently
# =============================================================================

async def demo_gather():
    """Run multiple coroutines concurrently with asyncio.gather().

    gather() starts all coroutines at once and returns results
    in the same order as the coroutines were passed.
    """
    print("=== asyncio.gather() Demo ===")
    print("Running prime_filter and square_mapper concurrently...\n")

    # Both coroutines run concurrently (interleaved at await points)
    primes, squares = await asyncio.gather(
        prime_filter(2, 50),
        square_mapper(1, 10),
    )

    print(f"Primes (2-50):  {primes}")
    print(f"Squares (1-10): {squares}")
    print()


# =============================================================================
# Example 4: Progress Reporting with Async
# =============================================================================

async def prime_filter_with_progress(start: int, end: int) -> list[int]:
    """Prime filter that reports progress."""
    primes = []
    total = end - start + 1
    for i, n in enumerate(number_range(start, end)):
        if is_prime(n):
            primes.append(n)
        # Report progress every 25%
        if (i + 1) % (total // 4) == 0:
            pct = (i + 1) / total * 100
            print(f"  Prime filter: {pct:.0f}% complete ({len(primes)} found)")
            await asyncio.sleep(0)
    return primes


async def countdown(name: str, n: int) -> str:
    """Simple countdown coroutine (runs alongside prime filter)."""
    for i in range(n, 0, -1):
        print(f"  {name}: {i}")
        await asyncio.sleep(0.01)
    return f"{name} done"


async def demo_concurrent_progress():
    """Show interleaved execution of concurrent coroutines."""
    print("=== Concurrent Coroutines with Progress ===")

    results = await asyncio.gather(
        prime_filter_with_progress(2, 1000),
        countdown("Timer-A", 5),
        countdown("Timer-B", 3),
    )

    primes, msg_a, msg_b = results
    print(f"\nFound {len(primes)} primes between 2 and 1000")
    print(f"Messages: {msg_a}, {msg_b}")
    print()


# =============================================================================
# Example 5: gather() vs wait() Comparison
# =============================================================================

async def demo_comparison():
    """Compare gather() and wait() approaches."""
    print("=== gather() vs wait() ===")
    print("""
    asyncio.gather(*coroutines):
      - Returns results in ORDER (same as input)
      - Simple API: results = await gather(a, b, c)
      - Best for: getting all results together

    asyncio.wait(tasks):
      - Returns (done, pending) sets
      - Results in COMPLETION order (not input order)
      - Supports timeout and FIRST_COMPLETED
      - Best for: processing as tasks complete, timeouts
    """)

    # gather: ordered results
    results = await asyncio.gather(
        prime_filter(2, 30),
        square_mapper(1, 5),
    )
    print(f"gather results (ordered): {results}")
    print()

    # wait: done/pending sets
    tasks = [
        asyncio.create_task(prime_filter(2, 30)),
        asyncio.create_task(square_mapper(1, 5)),
    ]
    done, pending = await asyncio.wait(tasks)
    print(f"wait: {len(done)} done, {len(pending)} pending")
    for task in done:
        print(f"  Result: {task.result()}")


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    asyncio.run(demo_gather())
    asyncio.run(demo_concurrent_progress())
    asyncio.run(demo_comparison())
```

---

## Exercises

**Exercise 1.**
Create 5 tasks using `asyncio.create_task()`, each sleeping for a different duration (0.1s to 0.5s) and returning its task name. Use `asyncio.as_completed()` to print results in completion order. Verify that shorter tasks complete first.

??? success "Solution to Exercise 1"
        ```python
        import asyncio

        async def task(name, delay):
            await asyncio.sleep(delay)
            return name

        async def main():
            tasks = [
                asyncio.create_task(task(f"task-{i}", 0.1 * (i + 1)))
                for i in range(5)
            ]

            for coro in asyncio.as_completed(tasks):
                result = await coro
                print(f"Completed: {result}")

        asyncio.run(main())
        ```

---

**Exercise 2.**
Write a program that creates a long-running task (`await asyncio.sleep(10)`) and cancels it after 0.5 seconds. Catch `asyncio.CancelledError` in both the task and the caller. Print messages showing when the task starts, when it is cancelled, and when the caller handles the cancellation.

??? success "Solution to Exercise 2"
        ```python
        import asyncio

        async def long_running():
            try:
                print("Task: started")
                await asyncio.sleep(10)
                return "done"
            except asyncio.CancelledError:
                print("Task: cancelled, cleaning up")
                raise

        async def main():
            t = asyncio.create_task(long_running())
            await asyncio.sleep(0.5)
            t.cancel()

            try:
                await t
            except asyncio.CancelledError:
                print("Caller: handled cancellation")

        asyncio.run(main())
        ```

---

**Exercise 3.**
Use `asyncio.TaskGroup` (Python 3.11+) to run 4 tasks concurrently. Three tasks should succeed (returning their ID squared), and one should raise a `ValueError`. Catch the resulting `ExceptionGroup` and print both the successful results and the error message.

??? success "Solution to Exercise 3"
        ```python
        import asyncio

        async def compute(task_id):
            await asyncio.sleep(0.1)
            if task_id == 3:
                raise ValueError(f"Task {task_id} failed")
            return task_id ** 2

        async def main():
            try:
                async with asyncio.TaskGroup() as tg:
                    tasks = [tg.create_task(compute(i)) for i in range(1, 5)]
            except* ValueError as eg:
                print("Errors:")
                for exc in eg.exceptions:
                    print(f"  {exc}")

            print("Results from successful tasks:")
            for t in tasks:
                if not t.cancelled() and t.exception() is None:
                    print(f"  {t.result()}")

        asyncio.run(main())
        ```
