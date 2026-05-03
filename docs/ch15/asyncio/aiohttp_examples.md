# Async HTTP with aiohttp

`aiohttp` is the standard library for async HTTP in Python, supporting both client and server functionality.

!!! tip "Mental Model"
    Think of `aiohttp` as a post office that can send and receive thousands of letters simultaneously on a single desk. Instead of waiting for each reply before sending the next letter, it fires off requests and processes responses as they arrive, making it ideal for web scraping, API clients, and microservices that handle many network calls at once.

## Installation

```bash
pip install aiohttp
```

## Basic Client Usage

### Simple GET Request

```python
import asyncio
import aiohttp

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f"Status: {response.status}")
            return await response.text()

async def main():
    html = await fetch("https://example.com")
    print(html[:200])

asyncio.run(main())
```

### Session Best Practices

```python
# WRONG: Creating session per request (slow)
async def fetch_bad(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# CORRECT: Reuse session for multiple requests
async def fetch_many(urls):
    async with aiohttp.ClientSession() as session:
        results = []
        for url in urls:
            async with session.get(url) as response:
                results.append(await response.text())
        return results

# BEST: Pass session as parameter
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = ["https://example.com"] * 10
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
```

## Request Methods

```python
async def http_methods_example():
    async with aiohttp.ClientSession() as session:
        # GET
        async with session.get('https://api.example.com/items') as r:
            data = await r.json()
        
        # POST
        async with session.post('https://api.example.com/items', 
                                json={'name': 'item'}) as r:
            result = await r.json()
        
        # PUT
        async with session.put('https://api.example.com/items/1',
                               json={'name': 'updated'}) as r:
            result = await r.json()
        
        # DELETE
        async with session.delete('https://api.example.com/items/1') as r:
            print(r.status)
        
        # PATCH
        async with session.patch('https://api.example.com/items/1',
                                 json={'name': 'patched'}) as r:
            result = await r.json()
```

## Request Parameters

### Query Parameters

```python
async def with_params():
    async with aiohttp.ClientSession() as session:
        params = {'key': 'value', 'page': 1}
        async with session.get('https://api.example.com/search', 
                               params=params) as r:
            # URL becomes: https://api.example.com/search?key=value&page=1
            return await r.json()
```

### Headers

```python
async def with_headers():
    async with aiohttp.ClientSession() as session:
        headers = {
            'Authorization': 'Bearer token123',
            'Accept': 'application/json'
        }
        async with session.get('https://api.example.com', 
                               headers=headers) as r:
            return await r.json()

# Or set default headers for session
async def with_default_headers():
    headers = {'Authorization': 'Bearer token123'}
    async with aiohttp.ClientSession(headers=headers) as session:
        # All requests use these headers
        async with session.get('https://api.example.com') as r:
            return await r.json()
```

### POST Data

```python
async def post_data():
    async with aiohttp.ClientSession() as session:
        # JSON data
        async with session.post('https://api.example.com',
                                json={'key': 'value'}) as r:
            return await r.json()
        
        # Form data
        async with session.post('https://api.example.com',
                                data={'key': 'value'}) as r:
            return await r.text()
        
        # Form data with file
        data = aiohttp.FormData()
        data.add_field('file', open('file.txt', 'rb'),
                       filename='file.txt',
                       content_type='text/plain')
        async with session.post('https://api.example.com/upload',
                                data=data) as r:
            return await r.json()
```

## Response Handling

```python
async def handle_response():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.example.com') as r:
            # Status
            print(r.status)        # 200
            print(r.reason)        # 'OK'
            
            # Headers
            print(r.headers)
            print(r.headers['Content-Type'])
            
            # URL (after redirects)
            print(r.url)
            
            # Response body
            text = await r.text()          # As string
            data = await r.json()          # As JSON
            binary = await r.read()        # As bytes
            
            # Streaming
            async for chunk in r.content.iter_chunked(1024):
                process_chunk(chunk)
```

## Timeouts

```python
async def with_timeout():
    # Per-request timeout
    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get('https://slow-api.example.com') as r:
                return await r.json()
        except asyncio.TimeoutError:
            print("Request timed out")

# More granular timeouts
timeout = aiohttp.ClientTimeout(
    total=60,        # Total timeout
    connect=10,      # Connection timeout
    sock_read=30,    # Read timeout
    sock_connect=10  # Socket connect timeout
)
```

## Error Handling

```python
async def safe_fetch(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()  # Raise on 4xx/5xx
                return await response.json()
                
        except aiohttp.ClientConnectionError:
            print("Connection failed")
        except aiohttp.ClientResponseError as e:
            print(f"HTTP error: {e.status}")
        except aiohttp.ClientError as e:
            print(f"Client error: {e}")
        except asyncio.TimeoutError:
            print("Request timed out")
```

## Concurrent Requests

### Using gather()

```python
async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        async def fetch_one(url):
            async with session.get(url) as r:
                return await r.json()
        
        tasks = [fetch_one(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)

async def main():
    urls = [f"https://api.example.com/item/{i}" for i in range(100)]
    results = await fetch_all(urls)
```

### Rate Limiting with Semaphore

```python
async def fetch_with_rate_limit(urls, max_concurrent=10):
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def fetch_one(session, url):
        async with semaphore:
            async with session.get(url) as r:
                return await r.json()
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

### With Retry Logic

```python
async def fetch_with_retry(session, url, max_retries=3, backoff=1.0):
    for attempt in range(max_retries):
        try:
            async with session.get(url) as r:
                r.raise_for_status()
                return await r.json()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            if attempt == max_retries - 1:
                raise
            
            wait = backoff * (2 ** attempt)
            print(f"Retry {attempt + 1} in {wait}s: {e}")
            await asyncio.sleep(wait)
```

## Practical Examples

### 1. API Client Class

```python
class APIClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={'Authorization': f'Bearer {self.api_key}'}
        )
        return self
    
    async def __aexit__(self, *args):
        await self.session.close()
    
    async def get(self, endpoint, **params):
        url = f"{self.base_url}/{endpoint}"
        async with self.session.get(url, params=params) as r:
            r.raise_for_status()
            return await r.json()
    
    async def post(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        async with self.session.post(url, json=data) as r:
            r.raise_for_status()
            return await r.json()

# Usage
async def main():
    async with APIClient("https://api.example.com", "secret") as client:
        users = await client.get("users", page=1)
        new_user = await client.post("users", {"name": "Alice"})
```

### 2. Parallel API Fetcher

```python
async def parallel_api_fetch(endpoints, base_url, max_concurrent=5):
    semaphore = asyncio.Semaphore(max_concurrent)
    results = {}
    
    async def fetch_endpoint(session, endpoint):
        async with semaphore:
            try:
                async with session.get(f"{base_url}/{endpoint}") as r:
                    results[endpoint] = await r.json()
            except Exception as e:
                results[endpoint] = {"error": str(e)}
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_endpoint(session, ep) for ep in endpoints]
        await asyncio.gather(*tasks)
    
    return results

# Usage
async def main():
    endpoints = ["users", "posts", "comments", "todos"]
    data = await parallel_api_fetch(endpoints, "https://jsonplaceholder.typicode.com")
    print(data)
```

### 3. Streaming Download

```python
async def download_file(url, filepath, chunk_size=8192):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(filepath, 'wb') as f:
                async for chunk in response.content.iter_chunked(chunk_size):
                    f.write(chunk)

# With progress
async def download_with_progress(url, filepath):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            total = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                async for chunk in response.content.iter_chunked(8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress = (downloaded / total * 100) if total else 0
                    print(f"\rProgress: {progress:.1f}%", end='')
```

### 4. WebSocket Client

```python
async def websocket_client():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('wss://echo.websocket.org') as ws:
            # Send message
            await ws.send_str('Hello!')
            
            # Receive messages
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    print(f"Received: {msg.data}")
                    if msg.data == 'close':
                        await ws.close()
                        break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
```

## Connection Pooling

```python
# Configure connector for connection pooling
connector = aiohttp.TCPConnector(
    limit=100,           # Total connection limit
    limit_per_host=10,   # Per-host limit
    ttl_dns_cache=300,   # DNS cache TTL
    keepalive_timeout=30 # Keep-alive timeout
)

async with aiohttp.ClientSession(connector=connector) as session:
    # All requests share the connection pool
    pass
```

## Key Takeaways

- Always use `async with` for sessions and responses
- Reuse sessions across multiple requests
- Use semaphores for rate limiting
- Implement retry logic for reliability
- Handle timeouts and errors gracefully
- Use connection pooling for high-throughput applications
- Stream large responses with `iter_chunked()`

---

## Exercises

**Exercise 1.**
Write an async function that simulates fetching 10 URLs concurrently using a shared `aiohttp.ClientSession`. Use `asyncio.Semaphore(3)` to limit concurrency to 3 simultaneous requests. Each "fetch" should simulate a network delay with `asyncio.sleep(0.2)` and return the URL with its status. Print all results.

??? success "Solution to Exercise 1"
        ```python
        import asyncio

        async def fetch(sem, url):
            async with sem:
                await asyncio.sleep(0.2)
                return (url, 200)

        async def main():
            sem = asyncio.Semaphore(3)
            urls = [f"https://example.com/page{i}" for i in range(10)]

            tasks = [fetch(sem, url) for url in urls]
            results = await asyncio.gather(*tasks)

            for url, status in results:
                print(f"{url}: {status}")

        asyncio.run(main())
        ```

---

**Exercise 2.**
Create an `APIClient` class that uses `async with` for session lifecycle (`__aenter__`/`__aexit__`). It should have a `get(endpoint)` method that simulates a GET request and a `post(endpoint, data)` method. Include a retry mechanism that retries up to 2 times on failure. Demonstrate usage with `async with APIClient(...) as client:`.

??? success "Solution to Exercise 2"
        ```python
        import asyncio

        class APIClient:
            def __init__(self, base_url):
                self.base_url = base_url

            async def __aenter__(self):
                print(f"Session opened for {self.base_url}")
                return self

            async def __aexit__(self, *args):
                print("Session closed")

            async def _request(self, method, endpoint, **kwargs):
                url = f"{self.base_url}/{endpoint}"
                for attempt in range(3):
                    try:
                        await asyncio.sleep(0.1)
                        if attempt < 1:
                            raise ConnectionError("Simulated failure")
                        return {"url": url, "method": method, "status": 200}
                    except ConnectionError:
                        if attempt == 2:
                            raise
                        await asyncio.sleep(0.1 * (attempt + 1))

            async def get(self, endpoint):
                return await self._request("GET", endpoint)

            async def post(self, endpoint, data):
                return await self._request("POST", endpoint, data=data)

        async def main():
            async with APIClient("https://api.example.com") as client:
                result = await client.get("users")
                print(f"GET: {result}")
                result = await client.post("users", {"name": "Alice"})
                print(f"POST: {result}")

        asyncio.run(main())
        ```

---

**Exercise 3.**
Write a function `fetch_with_timeout(urls, timeout)` that uses `asyncio.wait()` with a timeout. For each completed task, print the result. For each timed-out (pending) task, cancel it and print a timeout message. Test with 5 URLs where delays vary from 0.1s to 0.5s and a timeout of 0.3s.

??? success "Solution to Exercise 3"
        ```python
        import asyncio

        async def fetch(url, delay):
            await asyncio.sleep(delay)
            return f"Data from {url}"

        async def fetch_with_timeout(urls_and_delays, timeout):
            tasks = {
                asyncio.create_task(fetch(url, delay)): url
                for url, delay in urls_and_delays
            }

            done, pending = await asyncio.wait(tasks.keys(), timeout=timeout)

            for t in done:
                url = tasks[t]
                print(f"Completed: {url} -> {t.result()}")

            for t in pending:
                url = tasks[t]
                t.cancel()
                print(f"Timed out: {url}")

            await asyncio.gather(*pending, return_exceptions=True)

        async def main():
            urls = [
                (f"https://example.com/{i}", 0.1 * (i + 1))
                for i in range(5)
            ]
            await fetch_with_timeout(urls, timeout=0.3)

        asyncio.run(main())
        ```
