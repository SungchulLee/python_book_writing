# Async Iteration and Context Managers

Python supports asynchronous versions of `for` loops and `with` statements for working with async resources.

!!! tip "Mental Model"
    `async for` and `async with` are the async equivalents of their synchronous counterparts, designed for sources that produce items or manage resources over the network. Picture a streaming API where each item requires an `await` to arrive -- `async for` lets you loop over that stream naturally, while `async with` ensures connections and sessions are properly opened and closed even when pauses happen in between.

## async for - Asynchronous Iteration

### Async Iterators

An async iterator implements `__aiter__` and `__anext__`:

```python
import asyncio

class AsyncCounter:
    def __init__(self, stop):
        self.current = 0
        self.stop = stop
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.stop:
            raise StopAsyncIteration
        
        await asyncio.sleep(0.1)  # Simulate async operation
        self.current += 1
        return self.current

async def main():
    async for num in AsyncCounter(5):
        print(num)
    # 1, 2, 3, 4, 5 (with 0.1s delay between each)

asyncio.run(main())
```

### Async Generators (Simpler)

```python
async def async_range(stop):
    for i in range(stop):
        await asyncio.sleep(0.1)
        yield i

async def main():
    async for num in async_range(5):
        print(num)

asyncio.run(main())
```

### Practical Examples

#### 1. Streaming API Results

```python
async def fetch_pages(url, max_pages=10):
    """Yield pages as they're fetched."""
    page = 1
    while page <= max_pages:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{url}?page={page}") as resp:
                data = await resp.json()
                
                if not data['results']:
                    return
                
                yield data['results']
                page += 1

async def main():
    async for results in fetch_pages("https://api.example.com/items"):
        for item in results:
            process(item)
```

#### 2. Database Cursor

```python
async def fetch_rows(query, batch_size=100):
    """Yield rows from database in batches."""
    async with get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(query)
            
            while True:
                rows = await cursor.fetchmany(batch_size)
                if not rows:
                    break
                
                for row in rows:
                    yield row

async def main():
    async for row in fetch_rows("SELECT * FROM users"):
        print(row)
```

#### 3. WebSocket Messages

```python
async def read_messages(websocket):
    """Yield messages from WebSocket."""
    async for message in websocket:
        if message.type == aiohttp.WSMsgType.TEXT:
            yield message.data
        elif message.type == aiohttp.WSMsgType.ERROR:
            break

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('ws://example.com') as ws:
            async for msg in read_messages(ws):
                print(f"Received: {msg}")
```

#### 4. File Lines (with aiofiles)

```python
import aiofiles

async def read_lines(filename):
    async with aiofiles.open(filename) as f:
        async for line in f:
            yield line.strip()

async def main():
    async for line in read_lines("data.txt"):
        print(line)
```

### Async Comprehensions

```python
# Async list comprehension
async def main():
    results = [x async for x in async_range(5)]
    print(results)  # [0, 1, 2, 3, 4]

# With condition
    evens = [x async for x in async_range(10) if x % 2 == 0]
    print(evens)  # [0, 2, 4, 6, 8]

# Async generator expression
    gen = (x * 2 async for x in async_range(5))
    async for val in gen:
        print(val)
```

### Combining with await

```python
# await in comprehension
async def fetch(url):
    await asyncio.sleep(0.1)
    return f"data from {url}"

async def main():
    urls = ["url1", "url2", "url3"]
    
    # Sequential fetching
    results = [await fetch(url) for url in urls]
    
    # Both async for and await
    async def url_generator():
        for url in urls:
            await asyncio.sleep(0.1)
            yield url
    
    results = [await fetch(url) async for url in url_generator()]
```

## async with - Async Context Managers

### Async Context Manager Protocol

Implements `__aenter__` and `__aexit__`:

```python
class AsyncResource:
    async def __aenter__(self):
        print("Acquiring resource...")
        await asyncio.sleep(0.1)  # Simulate async setup
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Releasing resource...")
        await asyncio.sleep(0.1)  # Simulate async cleanup
        return False  # Don't suppress exceptions
    
    async def do_work(self):
        print("Working...")

async def main():
    async with AsyncResource() as resource:
        await resource.do_work()

asyncio.run(main())
```

### Using @asynccontextmanager

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def managed_resource(name):
    print(f"Setting up {name}")
    await asyncio.sleep(0.1)
    
    try:
        yield name
    finally:
        print(f"Cleaning up {name}")
        await asyncio.sleep(0.1)

async def main():
    async with managed_resource("database") as resource:
        print(f"Using {resource}")
```

### Practical Examples

#### 1. Database Connection

```python
class AsyncDBConnection:
    def __init__(self, dsn):
        self.dsn = dsn
        self.conn = None
    
    async def __aenter__(self):
        self.conn = await asyncpg.connect(self.dsn)
        return self.conn
    
    async def __aexit__(self, *args):
        await self.conn.close()

async def main():
    async with AsyncDBConnection("postgresql://...") as conn:
        result = await conn.fetch("SELECT * FROM users")
```

#### 2. HTTP Session

```python
import aiohttp

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.example.com') as response:
            data = await response.json()
            print(data)
```

#### 3. Lock

```python
lock = asyncio.Lock()

async def critical_section():
    async with lock:
        # Only one coroutine at a time
        await do_protected_work()
```

#### 4. Semaphore for Rate Limiting

```python
semaphore = asyncio.Semaphore(10)

async def rate_limited_fetch(url):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()
```

#### 5. Transaction

```python
@asynccontextmanager
async def transaction(conn):
    await conn.execute("BEGIN")
    try:
        yield conn
        await conn.execute("COMMIT")
    except Exception:
        await conn.execute("ROLLBACK")
        raise

async def main():
    async with get_connection() as conn:
        async with transaction(conn):
            await conn.execute("INSERT INTO ...")
            await conn.execute("UPDATE ...")
```

#### 6. Timeout Context

```python
# Python 3.11+
async def main():
    async with asyncio.timeout(5.0):
        await long_running_operation()

# Pre-3.11
@asynccontextmanager
async def timeout(seconds):
    task = asyncio.current_task()
    loop = asyncio.get_running_loop()
    
    def cancel():
        task.cancel()
    
    handle = loop.call_later(seconds, cancel)
    try:
        yield
    finally:
        handle.cancel()
```

### Nested Async Context Managers

```python
async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.example.com') as response:
            async with aiofiles.open('output.json', 'w') as f:
                data = await response.text()
                await f.write(data)
```

### Multiple Context Managers

```python
# Using multiple managers
async def main():
    async with (
        get_database() as db,
        get_cache() as cache,
        get_queue() as queue
    ):
        await process(db, cache, queue)

# Or using asyncio.gather for parallel setup
async def main():
    db, cache, queue = await asyncio.gather(
        get_database().__aenter__(),
        get_cache().__aenter__(),
        get_queue().__aenter__()
    )
    # Note: cleanup is more complex this way
```

## Combining async for and async with

```python
@asynccontextmanager
async def open_stream(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            yield response

async def stream_lines(url):
    async with open_stream(url) as response:
        async for line in response.content:
            yield line.decode()

async def main():
    async for line in stream_lines("https://example.com/stream"):
        print(line)
```

## Common Patterns

### Async Resource Pool

```python
class AsyncPool:
    def __init__(self, factory, size):
        self.factory = factory
        self.pool = asyncio.Queue(maxsize=size)
        self.size = size
    
    async def initialize(self):
        for _ in range(self.size):
            resource = await self.factory()
            await self.pool.put(resource)
    
    @asynccontextmanager
    async def acquire(self):
        resource = await self.pool.get()
        try:
            yield resource
        finally:
            await self.pool.put(resource)

# Usage
pool = AsyncPool(create_connection, size=10)
await pool.initialize()

async with pool.acquire() as conn:
    await conn.execute(...)
```

## Key Takeaways

- `async for` iterates over async iterators/generators
- `async with` manages async context managers
- Use async generators for streaming data
- Use `@asynccontextmanager` for simpler context manager creation
- Common uses: HTTP sessions, database connections, locks, files
- Async comprehensions work with `async for` and `await`
- Always clean up async resources properly in `__aexit__`

---

## Exercises

**Exercise 1.**
Write an async generator `async_range_squared(n)` that yields the squares of numbers 0 through n-1, with a 0.05s delay between each. Collect the results using an async list comprehension and print them.

??? success "Solution to Exercise 1"
        ```python
        import asyncio

        async def async_range_squared(n):
            for i in range(n):
                await asyncio.sleep(0.05)
                yield i * i

        async def main():
            squares = [x async for x in async_range_squared(10)]
            print(f"Squares: {squares}")

        asyncio.run(main())
        ```

---

**Exercise 2.**
Create an async context manager class `ManagedResource` that prints "Acquired" on enter (after a 0.1s simulated setup) and "Released" on exit (after a 0.1s simulated teardown). The resource should provide a `do_work()` async method that prints "Working...". Demonstrate it with `async with`.

??? success "Solution to Exercise 2"
        ```python
        import asyncio

        class ManagedResource:
            async def __aenter__(self):
                await asyncio.sleep(0.1)
                print("Acquired")
                return self

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                await asyncio.sleep(0.1)
                print("Released")
                return False

            async def do_work(self):
                print("Working...")

        async def main():
            async with ManagedResource() as resource:
                await resource.do_work()

        asyncio.run(main())
        ```

---

**Exercise 3.**
Write an async generator `batched_counter(total, batch_size)` that yields lists of consecutive integers in batches. For example, `batched_counter(10, 3)` yields `[0,1,2]`, `[3,4,5]`, `[6,7,8]`, `[9]`. Add a 0.1s delay between batches. Collect all items into a flat list using `async for` and verify it equals `list(range(total))`.

??? success "Solution to Exercise 3"
        ```python
        import asyncio

        async def batched_counter(total, batch_size):
            for start in range(0, total, batch_size):
                await asyncio.sleep(0.1)
                yield list(range(start, min(start + batch_size, total)))

        async def main():
            flat = []
            async for batch in batched_counter(10, 3):
                print(f"Batch: {batch}")
                flat.extend(batch)

            assert flat == list(range(10))
            print(f"All items: {flat}")

        asyncio.run(main())
        ```
