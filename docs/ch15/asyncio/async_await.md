# async and await

!!! tip "Mental Model"
    `async def` declares a function that can pause, and `await` is where it pauses. When a coroutine hits `await`, it hands control back to the event loop so other work can proceed -- like a chef who starts boiling water and chops vegetables while waiting, rather than staring at the pot.

## The async Keyword

The `async` keyword defines a **coroutine function**. Calling it returns a coroutine object, not the result.

```python
async def greet(name):
    return f"Hello, {name}"

# Calling returns a coroutine object
coro = greet("Alice")
print(coro)  # <coroutine object greet at 0x...>

# Must run it to get the result
import asyncio
result = asyncio.run(greet("Alice"))
print(result)  # "Hello, Alice"
```

---

## The await Keyword

`await` suspends the coroutine until the awaited operation completes. It can only be used inside `async` functions.

```python
async def fetch_data():
    print("Starting fetch...")
    await asyncio.sleep(1)  # Suspend here, let other tasks run
    print("Fetch complete!")
    return {"data": 42}

async def main():
    result = await fetch_data()  # Wait for fetch_data to complete
    print(result)

asyncio.run(main())
```

Output:
```
Starting fetch...
Fetch complete!
{'data': 42}
```

---

## What Can Be Awaited?

Only **awaitable** objects can be used with `await`:

### 1. Coroutines

```python
async def my_coroutine():
    return "result"

async def main():
    result = await my_coroutine()  # ✅ Coroutine is awaitable
```

### 2. Tasks

```python
async def main():
    task = asyncio.create_task(my_coroutine())
    result = await task  # ✅ Task is awaitable
```

### 3. Futures

```python
async def main():
    future = asyncio.Future()
    # ... something sets future.set_result(value)
    result = await future  # ✅ Future is awaitable
```

### 4. Objects with `__await__`

```python
class MyAwaitable:
    def __await__(self):
        yield
        return "custom result"

async def main():
    result = await MyAwaitable()  # ✅ Has __await__
```

---

## Sequential vs Concurrent Execution

### Sequential (Slow)

```python
async def fetch(url):
    await asyncio.sleep(1)  # Simulate network delay
    return f"Data from {url}"

async def main():
    # Each await blocks until complete
    result1 = await fetch("url1")  # 1 second
    result2 = await fetch("url2")  # 1 second
    result3 = await fetch("url3")  # 1 second
    # Total: 3 seconds

asyncio.run(main())
```

### Concurrent (Fast)

```python
async def main():
    # Create tasks - starts all immediately
    task1 = asyncio.create_task(fetch("url1"))
    task2 = asyncio.create_task(fetch("url2"))
    task3 = asyncio.create_task(fetch("url3"))
    
    # Await results
    result1 = await task1
    result2 = await task2
    result3 = await task3
    # Total: ~1 second (parallel execution)

asyncio.run(main())
```

### Using gather (Preferred)

```python
async def main():
    results = await asyncio.gather(
        fetch("url1"),
        fetch("url2"),
        fetch("url3")
    )
    # results = ["Data from url1", "Data from url2", "Data from url3"]
    # Total: ~1 second

asyncio.run(main())
```

---

## Common Mistakes

### 1. Forgetting await

```python
async def main():
    result = fetch_data()  # ❌ Missing await - returns coroutine object
    print(result)  # <coroutine object fetch_data at 0x...>

async def main():
    result = await fetch_data()  # ✅ Correct
    print(result)  # Actual result
```

**Warning**: Python shows `RuntimeWarning: coroutine was never awaited`

### 2. Using await Outside async Function

```python
def main():
    result = await fetch_data()  # ❌ SyntaxError

async def main():
    result = await fetch_data()  # ✅ Must be inside async function
```

### 3. Blocking the Event Loop

```python
import time

async def bad_example():
    time.sleep(1)  # ❌ Blocks the entire event loop!
    return "done"

async def good_example():
    await asyncio.sleep(1)  # ✅ Yields control to event loop
    return "done"
```

### 4. Not Running Coroutines

```python
async def my_task():
    print("Running")

# ❌ Does nothing - coroutine created but never run
my_task()

# ✅ Actually runs the coroutine
asyncio.run(my_task())
```

---

## Async Context Managers

Use `async with` for async setup/cleanup:

```python
class AsyncConnection:
    async def __aenter__(self):
        print("Connecting...")
        await asyncio.sleep(0.1)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Disconnecting...")
        await asyncio.sleep(0.1)

async def main():
    async with AsyncConnection() as conn:
        print("Using connection")

asyncio.run(main())
```

Output:
```
Connecting...
Using connection
Disconnecting...
```

### Real-World Example

```python
import aiohttp

async def fetch(url):
    async with aiohttp.ClientSession() as session:  # Async context manager
        async with session.get(url) as response:    # Another one
            return await response.text()
```

---

## Async Iterators

Use `async for` to iterate over async iterables:

```python
class AsyncCounter:
    def __init__(self, stop):
        self.stop = stop
    
    def __aiter__(self):
        self.current = 0
        return self
    
    async def __anext__(self):
        if self.current >= self.stop:
            raise StopAsyncIteration
        await asyncio.sleep(0.1)
        self.current += 1
        return self.current

async def main():
    async for num in AsyncCounter(5):
        print(num)

asyncio.run(main())
```

### Async Generator (Simpler)

```python
async def async_counter(stop):
    for i in range(stop):
        await asyncio.sleep(0.1)
        yield i

async def main():
    async for num in async_counter(5):
        print(num)
```

---

## Async Comprehensions

```python
# Async list comprehension
async def main():
    results = [await fetch(url) async for url in async_url_generator()]

# Async generator expression
async def main():
    gen = (await fetch(url) async for url in async_url_generator())
```

---

## Summary

| Syntax | Purpose |
|--------|---------|
| `async def` | Define a coroutine function |
| `await` | Suspend until awaitable completes |
| `async with` | Async context manager |
| `async for` | Iterate over async iterable |
| `asyncio.run()` | Entry point to run async code |

**Key Rules**:

1. `await` can only be used inside `async` functions
2. Only awaitables can be awaited (coroutines, tasks, futures)
3. Don't use blocking calls (`time.sleep`, `requests.get`) in async code
4. Use `asyncio.gather()` for concurrent execution
5. Always `await` your coroutines or they won't run

---

## Runnable Example: `async_await_tutorial.py`

```python
"""
Beginner Tutorial 1: Introduction to async/await Syntax

This file introduces the fundamental async/await syntax in Python.
We'll learn:
- What makes a function "async"
- How to call async functions with "await"
- The difference between sync and async execution
- Basic asyncio.run() usage

Learning objectives:
1. Understand async def syntax
2. Learn when and how to use await
3. See the difference between blocking and non-blocking code
"""

import asyncio
import time


# ============================================================================
# PART 1: Understanding Synchronous vs Asynchronous
# ============================================================================

def synchronous_function():
    """
    A regular (synchronous) function.
    When called, it runs from start to finish without yielding control.
    """
    print("Starting synchronous function")
    time.sleep(1)  # This BLOCKS the entire program for 1 second
    print("Finished synchronous function")
    return "Sync result"


async def asynchronous_function():
    """
    An asynchronous function (coroutine).
    Defined with 'async def' instead of just 'def'.
    
    When called WITHOUT await, it returns a coroutine object.
    When called WITH await, it executes and returns the result.
    """
    print("Starting asynchronous function")
    # asyncio.sleep() is non-blocking - it yields control to event loop
    await asyncio.sleep(1)
    print("Finished asynchronous function")
    return "Async result"


# ============================================================================
# PART 2: Basic async/await Patterns
# ============================================================================

async def simple_async_example():
    """
    A simple async function demonstrating await.
    
    Key points:
    - async def creates a coroutine function
    - await pauses this function and lets other tasks run
    - await can only be used inside async functions
    """
    print("Step 1: Before await")
    
    # await pauses execution here and yields to event loop
    # Other tasks could run during this 1 second
    await asyncio.sleep(1)
    
    print("Step 2: After await")
    return "Complete!"


async def calling_async_functions():
    """
    Demonstrates how to call one async function from another.
    
    Important:
    - To get the result, you must use 'await'
    - Without 'await', you just get a coroutine object
    """
    print("\n--- Calling async functions ---")
    
    # WRONG: Without await, this just creates a coroutine object
    # It doesn't actually run the function!
    coro = asynchronous_function()
    print(f"Without await: {coro}")
    print(f"Type: {type(coro)}")
    
    # We need to clean up the coroutine we created
    coro.close()
    
    # CORRECT: With await, the function runs and we get the result
    result = await asynchronous_function()
    print(f"With await: {result}")
    
    return result


# ============================================================================
# PART 3: Sequential Async Execution
# ============================================================================

async def fetch_data(data_id: int, delay: float):
    """
    Simulates fetching data from a source (like a database or API).
    
    Args:
        data_id: Identifier for the data
        delay: How long the fetch takes (simulated)
    
    Returns:
        The fetched data
    """
    print(f"  Fetching data {data_id}...")
    await asyncio.sleep(delay)  # Simulate I/O operation
    print(f"  Data {data_id} retrieved!")
    return f"Data_{data_id}"


async def sequential_execution():
    """
    Demonstrates sequential async execution.
    
    Even though we're using async/await, if we await each operation
    one after another, they still run sequentially (one at a time).
    
    This is like having async superpowers but choosing not to use them!
    """
    print("\n--- Sequential Execution ---")
    start_time = time.time()
    
    # Each await blocks until the operation completes
    # Total time: 1 + 1 + 1 = 3 seconds
    data1 = await fetch_data(1, 1.0)
    data2 = await fetch_data(2, 1.0)
    data3 = await fetch_data(3, 1.0)
    
    elapsed = time.time() - start_time
    print(f"Sequential execution took {elapsed:.2f} seconds")
    print(f"Retrieved: {data1}, {data2}, {data3}")
    
    return [data1, data2, data3]


# ============================================================================
# PART 4: Understanding await Behavior
# ============================================================================

async def demonstrate_await_behavior():
    """
    Shows what happens during await - control is yielded to event loop.
    
    When you 'await' something:
    1. Current function pauses
    2. Control returns to event loop
    3. Event loop can run other tasks
    4. When awaited operation completes, function resumes
    """
    print("\n--- Await Behavior ---")
    
    print("Before first await")
    await asyncio.sleep(0.5)  # Pause for 0.5 seconds
    print("Between awaits")
    await asyncio.sleep(0.5)  # Pause for another 0.5 seconds
    print("After second await")
    
    # Multiple awaits in sequence
    results = []
    for i in range(3):
        print(f"  Iteration {i+1}")
        await asyncio.sleep(0.1)
        results.append(i)
    
    return results


# ============================================================================
# PART 5: Async Function Return Values
# ============================================================================

async def async_function_with_return():
    """
    Async functions can return values just like regular functions.
    The return value is accessed by awaiting the function call.
    """
    await asyncio.sleep(0.1)
    return {"status": "success", "value": 42}


async def async_function_with_error():
    """
    Async functions can raise exceptions.
    These exceptions are raised when the function is awaited.
    """
    await asyncio.sleep(0.1)
    raise ValueError("Something went wrong!")


async def handling_returns_and_errors():
    """
    Demonstrates returning values and handling errors in async functions.
    """
    print("\n--- Returns and Errors ---")
    
    # Getting return value
    result = await async_function_with_return()
    print(f"Received result: {result}")
    
    # Handling errors
    try:
        await async_function_with_error()
    except ValueError as e:
        print(f"Caught exception: {e}")


# ============================================================================
# PART 6: Common Mistakes and Gotchas
# ============================================================================

async def common_mistakes():
    """
    Demonstrates common mistakes when learning async/await.
    """
    print("\n--- Common Mistakes ---")
    
    # Mistake 1: Forgetting await
    print("Mistake 1: Forgetting await")
    coro = asyncio.sleep(1)  # This creates a coroutine but doesn't run it
    print(f"  Without await: {coro}")
    coro.close()  # Clean up
    
    # Correct way
    print("  Correct way with await:")
    await asyncio.sleep(0.1)
    print("  Sleep completed!")
    
    # Mistake 2: Using time.sleep instead of asyncio.sleep
    print("\nMistake 2: Using time.sleep (blocking)")
    print("  DON'T do this in async code:")
    print("  time.sleep(1)  # This blocks the entire event loop!")
    
    print("  DO this instead:")
    await asyncio.sleep(0.1)  # Non-blocking
    print("  asyncio.sleep completed!")
    
    # Mistake 3: Trying to await non-async functions
    print("\nMistake 3: Can't await regular functions")
    print("  Regular functions must be called normally")
    regular_result = synchronous_function()  # No await!
    print(f"  Result: {regular_result}")


# ============================================================================
# PART 7: Running Async Code
# ============================================================================

async def main():
    """
    Main async function that demonstrates all concepts.
    
    This is the entry point for our async program.
    asyncio.run() creates an event loop, runs this coroutine,
    and then closes the event loop.
    """
    print("=" * 70)
    print("ASYNC/AWAIT BASICS TUTORIAL")
    print("=" * 70)
    
    # Run basic example
    result = await simple_async_example()
    print(f"Result: {result}")
    
    # Call async functions
    await calling_async_functions()
    
    # Sequential execution
    await sequential_execution()
    
    # Await behavior
    await demonstrate_await_behavior()
    
    # Returns and errors
    await handling_returns_and_errors()
    
    # Common mistakes
    await common_mistakes()
    
    print("\n" + "=" * 70)
    print("Tutorial complete!")
    print("=" * 70)


# ============================================================================
# Running the code
# ============================================================================

if __name__ == "__main__":
    """
    asyncio.run() is the recommended way to run async programs.
    
    What it does:
    1. Creates a new event loop
    2. Runs the provided coroutine (main)
    3. Closes the event loop when done
    
    This should be called only once per program, at the top level.
    Don't call asyncio.run() inside async functions!
    """
    
    # This is the standard way to run async code
    asyncio.run(main())
    
    # Note: You can't do this in an async function:
    # async def some_function():
    #     asyncio.run(main())  # ❌ Error! Already in async context


"""
KEY TAKEAWAYS:

1. async def: Defines an asynchronous function (coroutine)
2. await: Pauses execution and yields control to event loop
3. asyncio.run(): Entry point to run async code (use once)
4. await can only be used inside async functions
5. Async functions return coroutines that must be awaited
6. Use asyncio.sleep(), not time.sleep() in async code

MENTAL MODEL:
- Think of async/await as a way to write concurrent code that looks synchronous
- 'await' is like saying "I'm going to wait here, you can do other stuff"
- The event loop is the conductor that switches between tasks

NEXT STEPS:
- Learn about coroutines in detail (02_first_coroutine.py)
- Understand the event loop (03_event_loop_basics.py)
- Run multiple tasks concurrently (04_multiple_coroutines.py)
"""
```

---

## Exercises

**Exercise 1.**
Write an async function `timed_greet(name, delay)` that waits `delay` seconds, then returns `"Hello, {name}"`. Call it three times sequentially and measure the total time. Then call it three times concurrently with `asyncio.gather()` and measure again. Print both elapsed times to confirm the concurrent version is faster.

??? success "Solution to Exercise 1"
        ```python
        import asyncio
        import time

        async def timed_greet(name, delay):
            await asyncio.sleep(delay)
            return f"Hello, {name}"

        async def main():
            names = [("Alice", 0.3), ("Bob", 0.5), ("Carol", 0.2)]

            # Sequential
            start = time.perf_counter()
            for name, delay in names:
                await timed_greet(name, delay)
            seq_time = time.perf_counter() - start

            # Concurrent
            start = time.perf_counter()
            results = await asyncio.gather(
                *[timed_greet(n, d) for n, d in names]
            )
            con_time = time.perf_counter() - start

            print(f"Sequential: {seq_time:.2f}s")
            print(f"Concurrent: {con_time:.2f}s")
            print(f"Results: {results}")

        asyncio.run(main())
        ```

---

**Exercise 2.**
Create an async context manager class `Timer` that records the wall-clock time between `__aenter__` and `__aexit__` and prints the elapsed duration on exit. Use it with `async with Timer(): ...` around a block that awaits `asyncio.sleep(0.5)`.

??? success "Solution to Exercise 2"
        ```python
        import asyncio
        import time

        class Timer:
            async def __aenter__(self):
                self.start = time.perf_counter()
                return self

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                elapsed = time.perf_counter() - self.start
                print(f"Elapsed: {elapsed:.3f}s")
                return False

        async def main():
            async with Timer():
                await asyncio.sleep(0.5)

        asyncio.run(main())
        ```

---

**Exercise 3.**
Write an async generator `async_fibonacci(n)` that yields the first `n` Fibonacci numbers, with an `await asyncio.sleep(0.05)` between each yield to simulate asynchronous computation. Collect the results using an `async for` loop and print them.

??? success "Solution to Exercise 3"
        ```python
        import asyncio

        async def async_fibonacci(n):
            a, b = 0, 1
            for _ in range(n):
                yield a
                a, b = b, a + b
                await asyncio.sleep(0.05)

        async def main():
            fibs = []
            async for num in async_fibonacci(10):
                fibs.append(num)
            print(f"First 10 Fibonacci numbers: {fibs}")

        asyncio.run(main())
        ```
