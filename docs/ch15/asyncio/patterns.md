# Asyncio Patterns

!!! tip "Mental Model"
    Async patterns are recipes for coordinating coroutines that need to work together. Producer-consumer decouples data generation from processing, semaphores throttle concurrency to avoid overwhelming resources, and pipelines chain stages together. Each pattern solves a specific coordination problem that arises when many tasks share a single thread.

## Producer-Consumer Pattern

### Basic Queue

```python
import asyncio

async def producer(queue, n):
    """Produce n items."""
    for i in range(n):
        await asyncio.sleep(0.1)  # Simulate work
        await queue.put(f"item-{i}")
        print(f"Produced: item-{i}")
    
    # Signal completion
    await queue.put(None)

async def consumer(queue):
    """Consume items until None received."""
    while True:
        item = await queue.get()
        if item is None:
            break
        
        await asyncio.sleep(0.2)  # Simulate processing
        print(f"Consumed: {item}")
        queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=5)
    
    await asyncio.gather(
        producer(queue, 10),
        consumer(queue)
    )

asyncio.run(main())
```

### Multiple Consumers

```python
async def main():
    queue = asyncio.Queue()
    
    # Start multiple consumers
    consumers = [
        asyncio.create_task(consumer(queue, f"consumer-{i}"))
        for i in range(3)
    ]
    
    # Produce items
    await producer(queue, 20)
    
    # Wait for queue to be processed
    await queue.join()
    
    # Cancel consumers
    for c in consumers:
        c.cancel()
```

---

## Semaphore (Limiting Concurrency)

### Rate Limiting Requests

```python
import asyncio
import aiohttp

async def fetch(session, url, sem):
    async with sem:  # Acquire semaphore
        async with session.get(url) as response:
            return await response.text()

async def main():
    urls = [f"https://example.com/page{i}" for i in range(100)]
    
    # Limit to 10 concurrent requests
    sem = asyncio.Semaphore(10)
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, sem) for url in urls]
        results = await asyncio.gather(*tasks)
    
    return results
```

### Bounded Semaphore

```python
# BoundedSemaphore raises error if released more than acquired
sem = asyncio.BoundedSemaphore(10)

async def safe_operation(sem):
    async with sem:
        await do_work()
    # Automatically released
```

---

## Event (Signaling)

### Simple Signal

```python
async def waiter(event):
    print("Waiting for event...")
    await event.wait()
    print("Event received!")

async def setter(event):
    await asyncio.sleep(2)
    print("Setting event")
    event.set()

async def main():
    event = asyncio.Event()
    
    await asyncio.gather(
        waiter(event),
        waiter(event),
        setter(event)
    )

asyncio.run(main())
```

### Start Signal Pattern

```python
async def worker(event, worker_id):
    await event.wait()  # Wait for start signal
    print(f"Worker {worker_id} starting")
    await do_work()

async def main():
    start_event = asyncio.Event()
    
    # Create workers (they wait for event)
    workers = [
        asyncio.create_task(worker(start_event, i))
        for i in range(5)
    ]
    
    # Setup phase
    await setup()
    
    # Signal all workers to start
    start_event.set()
    
    await asyncio.gather(*workers)
```

---

## Lock (Mutual Exclusion)

### Protecting Shared State

```python
class Counter:
    def __init__(self):
        self.value = 0
        self.lock = asyncio.Lock()
    
    async def increment(self):
        async with self.lock:
            current = self.value
            await asyncio.sleep(0.01)  # Simulate delay
            self.value = current + 1

async def main():
    counter = Counter()
    
    # Without lock, final value would be wrong
    await asyncio.gather(*[counter.increment() for _ in range(100)])
    
    print(f"Final value: {counter.value}")  # 100

asyncio.run(main())
```

### Lock with Timeout

```python
async def acquire_with_timeout(lock, timeout):
    try:
        await asyncio.wait_for(lock.acquire(), timeout)
        try:
            await do_critical_work()
        finally:
            lock.release()
    except asyncio.TimeoutError:
        print("Could not acquire lock in time")
```

---

## Condition (Wait/Notify)

### Producer-Consumer with Condition

```python
async def producer(condition, items):
    async with condition:
        items.append("new item")
        print("Produced item, notifying")
        condition.notify()

async def consumer(condition, items):
    async with condition:
        while not items:
            print("Waiting for items...")
            await condition.wait()
        
        item = items.pop()
        print(f"Consumed: {item}")

async def main():
    condition = asyncio.Condition()
    items = []
    
    # Start consumer first (waits)
    consumer_task = asyncio.create_task(consumer(condition, items))
    
    await asyncio.sleep(1)
    
    # Producer adds item and notifies
    await producer(condition, items)
    
    await consumer_task
```

---

## Retry Pattern

### Exponential Backoff

```python
async def fetch_with_retry(url, max_retries=3, base_delay=1):
    for attempt in range(max_retries):
        try:
            return await fetch(url)
        except aiohttp.ClientError as e:
            if attempt == max_retries - 1:
                raise
            
            delay = base_delay * (2 ** attempt)
            print(f"Attempt {attempt + 1} failed, retrying in {delay}s")
            await asyncio.sleep(delay)
```

### Retry Decorator

```python
def async_retry(max_retries=3, delay=1, exceptions=(Exception,)):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay * (2 ** attempt))
            raise last_exception
        return wrapper
    return decorator

@async_retry(max_retries=3, exceptions=(aiohttp.ClientError,))
async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

---

## Timeout Patterns

### Context Manager Timeout

```python
async def with_timeout(coro, timeout, default=None):
    try:
        return await asyncio.wait_for(coro, timeout)
    except asyncio.TimeoutError:
        return default

async def main():
    result = await with_timeout(slow_operation(), timeout=5, default="timed out")
```

### Per-Task Timeouts in Batch

```python
async def fetch_with_timeout(url, timeout=5):
    try:
        return await asyncio.wait_for(fetch(url), timeout)
    except asyncio.TimeoutError:
        return {"url": url, "error": "timeout"}

async def main():
    urls = ["url1", "url2", "url3"]
    results = await asyncio.gather(*[
        fetch_with_timeout(url) for url in urls
    ])
```

---

## Graceful Shutdown

### Signal Handling

```python
import signal

class Server:
    def __init__(self):
        self.running = True
    
    async def run(self):
        loop = asyncio.get_running_loop()
        
        # Setup signal handlers
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, self.shutdown)
        
        while self.running:
            await self.handle_request()
    
    def shutdown(self):
        print("Shutdown requested")
        self.running = False

async def main():
    server = Server()
    await server.run()
```

### Cleanup All Tasks

```python
async def shutdown(loop, signal=None):
    if signal:
        print(f"Received signal {signal.name}")
    
    print("Cancelling outstanding tasks...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    
    for task in tasks:
        task.cancel()
    
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
```

---

## Connection Pool Pattern

```python
class ConnectionPool:
    def __init__(self, max_connections=10):
        self.semaphore = asyncio.Semaphore(max_connections)
        self.connections = asyncio.Queue()
        
    async def get_connection(self):
        await self.semaphore.acquire()
        
        try:
            return self.connections.get_nowait()
        except asyncio.QueueEmpty:
            return await create_connection()
    
    async def release_connection(self, conn):
        await self.connections.put(conn)
        self.semaphore.release()
    
    async def __aenter__(self):
        self.conn = await self.get_connection()
        return self.conn
    
    async def __aexit__(self, *args):
        await self.release_connection(self.conn)

# Usage
pool = ConnectionPool(max_connections=10)

async def query(sql):
    async with pool as conn:
        return await conn.execute(sql)
```

---

## Batch Processing

### Chunked Processing

```python
async def process_batch(items, batch_size=10):
    results = []
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batch_results = await asyncio.gather(*[
            process_item(item) for item in batch
        ])
        results.extend(batch_results)
        
        # Optional: delay between batches
        await asyncio.sleep(0.1)
    
    return results
```

### Async Iterator Processing

```python
async def process_stream(async_iterator, concurrency=10):
    sem = asyncio.Semaphore(concurrency)
    
    async def bounded_process(item):
        async with sem:
            return await process_item(item)
    
    tasks = []
    async for item in async_iterator:
        tasks.append(asyncio.create_task(bounded_process(item)))
    
    return await asyncio.gather(*tasks)
```

---

## Error Handling Patterns

### Collect All Errors

```python
async def process_all(items):
    results = []
    errors = []
    
    for coro in asyncio.as_completed([process(item) for item in items]):
        try:
            result = await coro
            results.append(result)
        except Exception as e:
            errors.append(e)
    
    if errors:
        print(f"Completed with {len(errors)} errors")
    
    return results, errors
```

### Circuit Breaker

```python
class CircuitBreaker:
    def __init__(self, max_failures=5, reset_timeout=60):
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
    
    async def call(self, coro):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is open")
        
        try:
            result = await coro
            self.failures = 0
            self.state = "closed"
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            
            if self.failures >= self.max_failures:
                self.state = "open"
            
            raise
```

---

## Summary

| Pattern | Use Case |
|---------|----------|
| Queue | Producer-consumer workflows |
| Semaphore | Limit concurrent operations |
| Event | Signal between coroutines |
| Lock | Protect shared state |
| Condition | Wait/notify coordination |
| Retry | Handle transient failures |
| Timeout | Prevent hanging operations |
| Connection Pool | Reuse expensive resources |
| Batch Processing | Handle large datasets |
| Circuit Breaker | Fail fast on repeated errors |

**Key Takeaways**:

- Use `asyncio.Queue` for producer-consumer patterns
- Use `Semaphore` to limit concurrency (rate limiting)
- Always implement timeouts for external calls
- Handle graceful shutdown with signal handlers
- Use retry with exponential backoff for reliability
- Batch operations to manage resource usage

---

## Exercises

**Exercise 1.**
Implement an async producer-consumer pipeline with `asyncio.Queue(maxsize=5)`. The producer generates 15 items (with 0.05s per item). Two consumers each process items (with 0.1s per item). Use a sentinel value `None` to signal each consumer to stop. Print which consumer handled each item.

??? success "Solution to Exercise 1"
        ```python
        import asyncio

        async def producer(queue, n):
            for i in range(n):
                await asyncio.sleep(0.05)
                await queue.put(i)
                print(f"Produced: {i}")
            await queue.put(None)
            await queue.put(None)

        async def consumer(queue, name):
            while True:
                item = await queue.get()
                if item is None:
                    break
                await asyncio.sleep(0.1)
                print(f"{name} consumed: {item}")
                queue.task_done()

        async def main():
            queue = asyncio.Queue(maxsize=5)
            await asyncio.gather(
                producer(queue, 15),
                consumer(queue, "Consumer-A"),
                consumer(queue, "Consumer-B"),
            )

        asyncio.run(main())
        ```

---

**Exercise 2.**
Write an `async_retry` decorator that retries an async function up to 3 times with exponential backoff (delays of 0.1s, 0.2s, 0.4s). Test it with a function that fails twice then succeeds on the third attempt, printing each attempt number.

??? success "Solution to Exercise 2"
        ```python
        import asyncio
        import functools

        def async_retry(max_retries=3, base_delay=0.1):
            def decorator(func):
                @functools.wraps(func)
                async def wrapper(*args, **kwargs):
                    for attempt in range(1, max_retries + 1):
                        try:
                            print(f"  Attempt {attempt}")
                            return await func(*args, **kwargs)
                        except Exception as e:
                            if attempt == max_retries:
                                raise
                            delay = base_delay * (2 ** (attempt - 1))
                            await asyncio.sleep(delay)
                return wrapper
            return decorator

        call_count = 0

        @async_retry(max_retries=3, base_delay=0.1)
        async def flaky_operation():
            global call_count
            call_count += 1
            if call_count < 3:
                raise RuntimeError(f"Fail #{call_count}")
            return "success"

        async def main():
            result = await flaky_operation()
            print(f"Result: {result}")

        asyncio.run(main())
        ```

---

**Exercise 3.**
Use `asyncio.Semaphore(3)` to limit concurrency when processing 10 tasks. Each task should print when it starts and finishes, sleeping for 0.2s. Verify from the output that at most 3 tasks run simultaneously by checking the timestamps.

??? success "Solution to Exercise 3"
        ```python
        import asyncio
        import time

        async def limited_task(sem, task_id):
            async with sem:
                start = time.perf_counter()
                print(f"Task {task_id}: started  at {start:.2f}")
                await asyncio.sleep(0.2)
                end = time.perf_counter()
                print(f"Task {task_id}: finished at {end:.2f}")

        async def main():
            sem = asyncio.Semaphore(3)
            await asyncio.gather(
                *[limited_task(sem, i) for i in range(10)]
            )

        asyncio.run(main())
        ```
