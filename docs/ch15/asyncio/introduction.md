# Asyncio Introduction

!!! tip "Mental Model"
    Asyncio is a single-threaded concurrency framework: one worker, many tasks. Like a receptionist who handles hundreds of phone calls by putting each on hold while waiting for a response, asyncio never truly does two things at once -- it just switches between tasks at `await` points so no time is wasted waiting.

## What is Asyncio?

**asyncio** is Python's built-in library for writing concurrent code using the **async/await** syntax. It provides a framework for managing asynchronous I/O operations, enabling thousands of concurrent connections with a single thread.

```python
import asyncio

async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

asyncio.run(main())
```

---

## Concurrency Models Comparison

| Model | Library | Best For | Parallelism |
|-------|---------|----------|-------------|
| Threading | `threading` | I/O-bound (simple) | Limited by GIL |
| Multiprocessing | `multiprocessing` | CPU-bound | True parallelism |
| **Asyncio** | `asyncio` | I/O-bound (many connections) | Single-threaded concurrency |

---

## When to Use Asyncio

### ✅ Good Use Cases

```python
# Network requests (HTTP clients)
async def fetch_all_urls(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# Web servers (FastAPI, aiohttp)
# Database queries (asyncpg, motor)
# WebSocket connections
# File I/O (aiofiles)
```

**Asyncio excels when**:
- Many concurrent I/O operations
- High number of connections (1000s)
- Network-bound applications
- Real-time applications (chat, streaming)

### ❌ Poor Use Cases

```python
# CPU-bound work - use multiprocessing instead
def compute_heavy():
    return sum(i * i for i in range(10_000_000))

# Simple scripts with few I/O operations
# Code that needs true parallelism
```

---

## Asyncio vs Threading

### Threading Approach

```python
import threading
import time

def fetch(url):
    time.sleep(1)  # Simulate I/O
    return f"Result from {url}"

# 10 threads for 10 URLs
threads = []
for url in urls:
    t = threading.Thread(target=fetch, args=(url,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

**Problems**:
- Thread overhead (memory, context switching)
- Limited scalability (100s of threads, not 1000s)
- Race conditions with shared state

### Asyncio Approach

```python
import asyncio

async def fetch(url):
    await asyncio.sleep(1)  # Simulate I/O
    return f"Result from {url}"

async def main():
    tasks = [fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

asyncio.run(main())
```

**Benefits**:
- Single thread, no race conditions
- Minimal overhead per task
- Scales to 10,000s of concurrent operations
- Explicit yield points (`await`)

---

## Key Concepts Overview

### 1. Coroutines

Functions defined with `async def`:

```python
async def my_coroutine():
    return "Hello"

# Calling returns a coroutine object, not the result
coro = my_coroutine()  # <coroutine object>

# Must be awaited or run
result = asyncio.run(my_coroutine())  # "Hello"
```

### 2. await Keyword

Suspends coroutine until the awaited operation completes:

```python
async def fetch_data():
    result = await some_async_operation()  # Pause here
    return result                           # Resume when done
```

### 3. Event Loop

The central scheduler that runs coroutines:

```python
# Modern way (Python 3.7+)
asyncio.run(main())

# Manual control (rarely needed)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

### 4. Tasks

Wrap coroutines for concurrent execution:

```python
async def main():
    # Create tasks for concurrent execution
    task1 = asyncio.create_task(fetch("url1"))
    task2 = asyncio.create_task(fetch("url2"))
    
    # Both run concurrently
    result1 = await task1
    result2 = await task2
```

---

## Minimal Working Example

```python
import asyncio

async def say_after(delay, message):
    """Coroutine that waits then prints."""
    await asyncio.sleep(delay)
    print(message)

async def main():
    print(f"Started at {asyncio.get_event_loop().time():.2f}")
    
    # Sequential (3 seconds total)
    # await say_after(1, "Hello")
    # await say_after(2, "World")
    
    # Concurrent (2 seconds total)
    await asyncio.gather(
        say_after(1, "Hello"),
        say_after(2, "World")
    )
    
    print(f"Finished at {asyncio.get_event_loop().time():.2f}")

asyncio.run(main())
```

Output:
```
Started at 0.00
Hello
World
Finished at 2.00
```

---

## Common Async Libraries

| Category | Library | Description |
|----------|---------|-------------|
| HTTP Client | `aiohttp`, `httpx` | Async HTTP requests |
| Web Framework | `FastAPI`, `Starlette` | Async web servers |
| Database | `asyncpg`, `motor`, `aiosqlite` | Async database drivers |
| File I/O | `aiofiles` | Async file operations |
| Redis | `aioredis` | Async Redis client |

---

## Summary

| Concept | Description |
|---------|-------------|
| `asyncio` | Python's async I/O framework |
| `async def` | Defines a coroutine |
| `await` | Suspends until operation completes |
| Event loop | Scheduler that runs coroutines |
| Best for | High-concurrency I/O-bound tasks |

**Key Takeaways**:

- Asyncio provides single-threaded concurrency
- Use for I/O-bound tasks with many concurrent operations
- `async`/`await` makes async code readable
- Not a replacement for multiprocessing (CPU-bound work)
- Modern Python async ecosystem is mature and widely adopted

---

## Exercises

**Exercise 1.**
Write an async program that simulates fetching data from 5 URLs concurrently using `asyncio.gather()`. Each "fetch" should sleep for a random duration (0.2-1.0s) and return the URL with its simulated response time. Print all results and the total elapsed wall-clock time, demonstrating that it is significantly less than the sum of individual times.

??? success "Solution to Exercise 1"
        ```python
        import asyncio
        import random
        import time

        async def fetch(url):
            delay = random.uniform(0.2, 1.0)
            await asyncio.sleep(delay)
            return (url, delay)

        async def main():
            urls = [f"https://example.com/page{i}" for i in range(5)]
            start = time.perf_counter()
            results = await asyncio.gather(*[fetch(u) for u in urls])
            elapsed = time.perf_counter() - start

            total_individual = 0
            for url, delay in results:
                print(f"{url}: {delay:.2f}s")
                total_individual += delay

            print(f"\nTotal wall-clock time: {elapsed:.2f}s")
            print(f"Sum of individual times: {total_individual:.2f}s")
            print(f"Concurrency saved: {total_individual - elapsed:.2f}s")

        asyncio.run(main())
        ```

---

**Exercise 2.**
Write two versions of a function that processes 10 items: one sequential (using a regular `for` loop with `await asyncio.sleep(0.1)` per item) and one concurrent (using `asyncio.gather()`). Run both, print the elapsed time for each, and compute the speedup ratio.

??? success "Solution to Exercise 2"
        ```python
        import asyncio
        import time

        async def process_item(item):
            await asyncio.sleep(0.1)
            return item * 2

        async def sequential():
            results = []
            for i in range(10):
                results.append(await process_item(i))
            return results

        async def concurrent():
            return await asyncio.gather(*[process_item(i) for i in range(10)])

        async def main():
            start = time.perf_counter()
            seq_results = await sequential()
            seq_time = time.perf_counter() - start

            start = time.perf_counter()
            con_results = await concurrent()
            con_time = time.perf_counter() - start

            print(f"Sequential: {seq_time:.2f}s, results={seq_results}")
            print(f"Concurrent: {con_time:.2f}s, results={con_results}")
            print(f"Speedup: {seq_time / con_time:.1f}x")

        asyncio.run(main())
        ```

---

**Exercise 3.**
Create an async function `countdown(name, n)` that prints `"{name}: {i}"` for `i` from `n` down to 1, with an `await asyncio.sleep(0.1)` between each. Run three countdowns concurrently ("A" from 3, "B" from 5, "C" from 2) using `asyncio.gather()`, and observe the interleaved output.

??? success "Solution to Exercise 3"
        ```python
        import asyncio

        async def countdown(name, n):
            for i in range(n, 0, -1):
                print(f"{name}: {i}")
                await asyncio.sleep(0.1)
            print(f"{name}: done!")

        async def main():
            await asyncio.gather(
                countdown("A", 3),
                countdown("B", 5),
                countdown("C", 2),
            )

        asyncio.run(main())
        ```
