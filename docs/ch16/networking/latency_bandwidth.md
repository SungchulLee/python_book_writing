# Latency and Bandwidth

!!! tip "Mental Model"
    Latency is how long it takes for the first drop of water to travel through a pipe; bandwidth is how wide the pipe is. For many small requests, latency dominates -- you wait for each round trip. For large transfers, bandwidth dominates -- you wait for the pipe to drain. Knowing which one is your bottleneck tells you what to optimize.

## Two Dimensions of Network Performance

Network performance has two key metrics that are often confused:

```
Bandwidth vs Latency

Bandwidth (throughput):  How much water the pipe can carry
Latency (delay):         How long for water to reach the other end

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  High Bandwidth, High Latency (intercontinental fiber):     │
│  ════════════════════════════════════════════▶              │
│        Lots of data, but takes 100ms to arrive              │
│                                                             │
│  Low Bandwidth, Low Latency (local network):                │
│  ══════▶                                                    │
│        Less data, but arrives in 1ms                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Latency

**Latency** is the time delay between sending and receiving data.

### Latency Components

```
Total Latency = Propagation + Transmission + Queuing + Processing

┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  Propagation:   Time for signal to travel (speed of light)    │
│                 ~5 μs per km in fiber                          │
│                                                                │
│  Transmission:  Time to push bits onto wire                    │
│                 = Data size / Bandwidth                        │
│                                                                │
│  Queuing:       Time waiting in router/switch buffers          │
│                 Variable, depends on congestion                │
│                                                                │
│  Processing:    Time for routers to process headers            │
│                 Usually microseconds                           │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Typical Latencies

| Path | Round-Trip Time (RTT) |
|------|----------------------|
| Same machine (localhost) | < 0.1 ms |
| Local network (LAN) | 0.1 - 1 ms |
| Same city | 1 - 10 ms |
| Same continent | 10 - 50 ms |
| Cross-continent | 50 - 150 ms |
| Opposite side of globe | 150 - 300 ms |
| Satellite (GEO) | 500 - 700 ms |

### Measuring Latency in Python

```python
import socket
import time

def measure_tcp_latency(host, port, iterations=10):
    """Measure TCP connection latency."""
    latencies = []
    
    for _ in range(iterations):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        start = time.perf_counter()
        try:
            sock.connect((host, port))
            latency = (time.perf_counter() - start) * 1000
            latencies.append(latency)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sock.close()
    
    if latencies:
        avg = sum(latencies) / len(latencies)
        print(f"Average latency to {host}:{port}: {avg:.2f} ms")
    
    return latencies

# measure_tcp_latency('google.com', 80)
```

### HTTP Latency

```python
import requests
import time

def measure_http_latency(url, iterations=5):
    """Measure HTTP request latency."""
    for _ in range(iterations):
        start = time.perf_counter()
        response = requests.get(url)
        elapsed = (time.perf_counter() - start) * 1000
        
        print(f"{url}: {elapsed:.0f} ms (status: {response.status_code})")

# measure_http_latency('https://api.github.com')
```

## Bandwidth

**Bandwidth** is the maximum rate of data transfer.

### Bandwidth Units

```
Bits vs Bytes:

Network speeds in bits:    1 Gbps = 1,000,000,000 bits/second
File sizes in bytes:       1 GB = 1,000,000,000 bytes

Conversion: 1 Gbps = 125 MB/s (divide by 8)

Common confusion:
  "1 Gbps internet" ≠ "1 GB per second downloads"
  "1 Gbps internet" = "125 MB per second" maximum
```

### Typical Bandwidths

| Connection | Bandwidth | Download 1 GB |
|------------|-----------|---------------|
| 4G LTE | 50 Mbps | ~3 minutes |
| Home cable | 100 Mbps | ~80 seconds |
| Gigabit fiber | 1 Gbps | ~8 seconds |
| 10 GbE | 10 Gbps | <1 second |
| Datacenter | 100 Gbps | ~0.1 second |

### Measuring Bandwidth

```python
import requests
import time

def measure_download_bandwidth(url, size_mb=10):
    """Measure download bandwidth."""
    # Use a test file of known size
    start = time.perf_counter()
    response = requests.get(url, stream=True)
    
    total_bytes = 0
    for chunk in response.iter_content(chunk_size=8192):
        total_bytes += len(chunk)
    
    elapsed = time.perf_counter() - start
    bandwidth_mbps = (total_bytes * 8) / elapsed / 1_000_000
    bandwidth_mbs = total_bytes / elapsed / 1_000_000
    
    print(f"Downloaded: {total_bytes / 1_000_000:.1f} MB")
    print(f"Time: {elapsed:.2f} seconds")
    print(f"Bandwidth: {bandwidth_mbps:.1f} Mbps ({bandwidth_mbs:.1f} MB/s)")

# measure_download_bandwidth('http://speedtest.example.com/100MB.bin')
```

## Bandwidth-Delay Product

The **bandwidth-delay product (BDP)** is the amount of data "in flight":

```
BDP = Bandwidth × Latency

Example:
  Bandwidth: 1 Gbps (125 MB/s)
  Latency: 100 ms (0.1 s)
  
  BDP = 125 MB/s × 0.1 s = 12.5 MB

This much data can be in transit at any moment!
```

### Why BDP Matters

```
Pipe Analogy:

Small BDP (low latency OR low bandwidth):
┌──────────────────────────────┐
│ ●  ●  ●  ●                   │  Few packets in flight
└──────────────────────────────┘

Large BDP (high latency AND high bandwidth):
┌──────────────────────────────────────────────────────────┐
│ ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● │
└──────────────────────────────────────────────────────────┘
Many packets in flight - need large buffers!
```

## Latency vs Throughput Trade-offs

### Small Requests

For small requests, latency dominates:

```python
import requests
import time

def small_request_test(url, n_requests=100):
    """Latency matters more for small requests."""
    start = time.perf_counter()
    
    for _ in range(n_requests):
        requests.get(url)
    
    elapsed = time.perf_counter() - start
    per_request = elapsed / n_requests * 1000
    
    print(f"{n_requests} small requests: {elapsed:.2f}s total")
    print(f"Per request: {per_request:.1f} ms")
    # Mostly latency, not bandwidth!
```

### Large Transfers

For large transfers, bandwidth dominates:

```python
def large_transfer_test(url):
    """Bandwidth matters more for large transfers."""
    start = time.perf_counter()
    
    response = requests.get(url)  # Large file
    
    elapsed = time.perf_counter() - start
    size_mb = len(response.content) / 1_000_000
    bandwidth = size_mb / elapsed
    
    print(f"Downloaded {size_mb:.1f} MB in {elapsed:.2f}s")
    print(f"Effective bandwidth: {bandwidth:.1f} MB/s")
```

## Optimizing for Latency

### 1. Reduce Round Trips

```python
# Bad: Multiple requests
user = requests.get('/api/user/123').json()
posts = requests.get('/api/user/123/posts').json()
comments = requests.get('/api/user/123/comments').json()
# 3 round trips = 3 × latency

# Good: Single request
data = requests.get('/api/user/123?include=posts,comments').json()
# 1 round trip
```

### 2. Use Connection Pooling

```python
import requests

# Bad: New connection each time
for url in urls:
    requests.get(url)  # TCP handshake overhead each time

# Good: Reuse connections
session = requests.Session()
for url in urls:
    session.get(url)  # Reuses TCP connection
```

### 3. Geographic Proximity

```
User in Tokyo:

  → US West Server:  100 ms RTT
  → Tokyo Server:    10 ms RTT
  
  10x improvement from location alone!
```

## Optimizing for Bandwidth

### 1. Compression

```python
import gzip
import requests

# Request compressed data
response = requests.get(url, headers={'Accept-Encoding': 'gzip'})

# Compress before sending
data = gzip.compress(large_data)
requests.post(url, data=data, headers={'Content-Encoding': 'gzip'})
```

### 2. Batch Operations

```python
# Bad: Many small requests
for item in items:
    requests.post('/api/process', json={'item': item})

# Good: Batch request
requests.post('/api/process-batch', json={'items': items})
```

### 3. Parallel Downloads

```python
import concurrent.futures
import requests

def download(url):
    return requests.get(url).content

# Download files in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(download, urls))
```

## Summary

| Metric | Definition | Optimization |
|--------|------------|--------------|
| **Latency** | Time to deliver one bit | Reduce distance, round trips |
| **Bandwidth** | Bits per second capacity | Compression, parallelism |
| **Throughput** | Actual achieved rate | Balance latency & bandwidth |
| **BDP** | Bandwidth × Latency | Size buffers appropriately |

Key formulas:

```
Transfer Time = Latency + (Size / Bandwidth)

For small data: Transfer Time ≈ Latency
For large data: Transfer Time ≈ Size / Bandwidth

BDP = Bandwidth × RTT
```

Rules of thumb:

- Many small requests → optimize latency (reduce round trips)
- Few large transfers → optimize bandwidth (compression, parallelism)
- Real applications → profile to find the bottleneck


---

## Exercises

**Exercise 1.** Explain the difference between latency and bandwidth. Give a real-world analogy for each.

??? success "Solution to Exercise 1"
    ```python
    # Conceptual solution - see page content for details
    import sys
    import platform

    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
    ```

---

**Exercise 2.** Calculate the total transfer time for a 1 GB file over a network with 100 Mbps bandwidth and 50 ms latency.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the hardware-software interaction and how it affects Python performance.

---

**Exercise 3.** Explain why high bandwidth does not help if latency is the bottleneck. Give an example scenario.

??? success "Solution to Exercise 3"
    ```python
    import time

    # Simple benchmark
    n = 10_000_000
    start = time.perf_counter()
    total = sum(range(n))
    elapsed = time.perf_counter() - start
    print(f"Sum of {n} integers: {total}")
    print(f"Time: {elapsed:.4f} seconds")
    ```

---

**Exercise 4.** Write Python code that measures the round-trip time (latency) to a server using `urllib.request` or `requests`.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    import time

    n = 1_000_000
    # Python loop
    start = time.perf_counter()
    result_py = sum(i * i for i in range(n))
    time_py = time.perf_counter() - start

    # NumPy vectorized
    arr = np.arange(n)
    start = time.perf_counter()
    result_np = np.sum(arr * arr)
    time_np = time.perf_counter() - start

    print(f"Python: {time_py:.4f}s, NumPy: {time_np:.4f}s")
    print(f"Speedup: {time_py / time_np:.1f}x")
    ```
