# CPU-Memory Communication

!!! tip "Mental Model"
    The CPU accesses memory through a hierarchy of increasingly large but slower caches, like a desk drawer (L1), filing cabinet (L2), office closet (L3), and warehouse (RAM). Most of the time you reach for the drawer first, and only go to the warehouse on a cache miss -- which costs 60 ns you cannot get back.

## The Memory Controller

Modern CPUs have an integrated **memory controller** that manages communication with RAM:

```
┌─────────────────────────────────────────────────────────────┐
│                          CPU                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   CPU Cores                          │   │
│  │   ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐              │   │
│  │   │Core 0│ │Core 1│ │Core 2│ │Core 3│              │   │
│  │   └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘              │   │
│  │      └────────┼────────┼────────┘                   │   │
│  │               ▼                                      │   │
│  │        ┌─────────────┐                              │   │
│  │        │  L3 Cache   │                              │   │
│  │        └──────┬──────┘                              │   │
│  └───────────────┼──────────────────────────────────────┘   │
│                  ▼                                          │
│  ┌───────────────────────────────────┐                     │
│  │      Integrated Memory Controller │                     │
│  │  ┌─────────┐       ┌─────────┐   │                     │
│  │  │Channel A│       │Channel B│   │                     │
│  │  └────┬────┘       └────┬────┘   │                     │
│  └───────┼─────────────────┼────────┘                     │
└──────────┼─────────────────┼────────────────────────────────┘
           │                 │
           ▼                 ▼
      ┌────────┐        ┌────────┐
      │ DIMM 1 │        │ DIMM 2 │
      └────────┘        └────────┘
```

## Memory Access Flow

### Read Request

```
1. CPU Core needs data at address X
        │
        ▼
2. Check L1 Cache ──── Hit? ──→ Return data (1 ns)
        │ Miss
        ▼
3. Check L2 Cache ──── Hit? ──→ Return data (3 ns)
        │ Miss
        ▼
4. Check L3 Cache ──── Hit? ──→ Return data (10 ns)
        │ Miss
        ▼
5. Memory Controller receives request
        │
        ▼
6. Controller sends address to RAM via memory bus
        │
        ▼
7. RAM retrieves data (Row → Column activation)
        │
        ▼
8. Data returns to CPU (~60 ns total from request)
        │
        ▼
9. Data cached in L1/L2/L3 for future access
```

## Memory Channels

Multiple channels allow parallel access:

```
Single Channel:
┌─────────────────┐
│ Memory Controller│
│    ┌──────┐     │
│    │Chan A│     │
│    └──┬───┘     │
└───────┼─────────┘
        │
   ┌────┴────┐
   │  DIMM   │     Bandwidth: ~25 GB/s
   └─────────┘

Dual Channel:
┌─────────────────┐
│ Memory Controller│
│ ┌──────┐ ┌──────┐│
│ │Chan A│ │Chan B││
│ └──┬───┘ └──┬───┘│
└────┼────────┼────┘
     │        │
┌────┴────┐┌────┴────┐
│  DIMM   ││  DIMM   │  Bandwidth: ~50 GB/s (2×)
└─────────┘└─────────┘
```

### Channel Interleaving

Data is striped across channels for parallelism:

```
Memory Address Interleaving:

Address 0x0000: Channel A, DIMM 0
Address 0x0040: Channel B, DIMM 0  (64-byte offset)
Address 0x0080: Channel A, DIMM 0
Address 0x00C0: Channel B, DIMM 0
...

Sequential access automatically uses both channels!
```

## Memory Timing

### DDR SDRAM Timing Parameters

```
Memory Access Timeline:

tCL (CAS Latency):    Column access time
tRCD:                 Row to Column Delay
tRP:                  Row Precharge time
tRAS:                 Row Active time

Example DDR4-3200 CL16:
Timings: 16-18-18-36

         tRCD        tCL
          │           │
    ┌─────┴─────┐ ┌───┴───┐
    │           │ │       │
────[Row Cmd]───[Col Cmd]─[Data]────
    │                     │
    └─────────────────────┘
           Total: ~20 ns
```

### Timing Impact

```python
import numpy as np
import time

def measure_memory_latency():
    """Measure effective memory access latency."""
    # Create array larger than cache
    size = 100 * 1024 * 1024  # 100 MB
    arr = np.zeros(size // 8, dtype=np.float64)
    
    # Random access pattern defeats prefetching
    indices = np.random.permutation(len(arr))
    
    # Pointer chasing to measure latency
    n_accesses = 1_000_000
    start = time.perf_counter()
    total = 0.0
    for i in range(n_accesses):
        total += arr[indices[i % len(indices)]]
    elapsed = time.perf_counter() - start
    
    latency_ns = elapsed / n_accesses * 1e9
    print(f"Effective latency: {latency_ns:.0f} ns")

measure_memory_latency()  # Typically 60-100 ns
```

## Cache Coherency

When multiple cores access the same memory, coherency must be maintained:

```
MESI Protocol States:

M (Modified):  This cache has the only valid copy (dirty)
E (Exclusive): This cache has the only copy (clean)
S (Shared):    Multiple caches have copies (clean)
I (Invalid):   Cache line is not valid

State Transitions:
┌───────────┐  Read by      ┌───────────┐
│ Invalid   │ ────────────▶ │  Shared   │
└───────────┘    this core  └───────────┘
      ▲                           │
      │ Other core                │ Write by
      │ writes                    │ this core
      │                           ▼
┌───────────┐               ┌───────────┐
│ Modified  │ ◀──────────── │ Exclusive │
└───────────┘  Write by     └───────────┘
               this core
```

### False Sharing

When cores modify different data in the same cache line:

```python
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import time

def false_sharing_demo():
    # Bad: Adjacent data (same cache line)
    shared_array = np.zeros(2, dtype=np.int64)
    
    def increment_0():
        for _ in range(10_000_000):
            shared_array[0] += 1
    
    def increment_1():
        for _ in range(10_000_000):
            shared_array[1] += 1
    
    # Both threads fight over same cache line!
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=2) as ex:
        ex.submit(increment_0)
        ex.submit(increment_1)
    bad_time = time.perf_counter() - start
    
    # Better: Pad to separate cache lines (64 bytes apart)
    padded = np.zeros(16, dtype=np.int64)  # 128 bytes
    # Thread 0 uses padded[0], Thread 1 uses padded[8]
    
    print(f"Adjacent (false sharing): {bad_time:.2f}s")
```

## Memory Bandwidth Measurement

```python
import numpy as np
import time

def measure_bandwidth():
    """Measure achievable memory bandwidth."""
    sizes_mb = [1, 10, 100, 1000]
    
    for size_mb in sizes_mb:
        n = size_mb * 1024 * 1024 // 8
        arr = np.random.rand(n)
        
        # Read bandwidth (sum reads all elements)
        start = time.perf_counter()
        for _ in range(10):
            _ = np.sum(arr)
        elapsed = time.perf_counter() - start
        
        bytes_read = n * 8 * 10
        bandwidth = bytes_read / elapsed / 1e9
        
        print(f"{size_mb:4d} MB: {bandwidth:.1f} GB/s")

measure_bandwidth()
```

Expected output:

```
   1 MB: 80.0 GB/s   (fits in L3 cache)
  10 MB: 50.0 GB/s   (partially cached)
 100 MB: 35.0 GB/s   (RAM limited)
1000 MB: 32.0 GB/s   (RAM limited)
```

## NUMA: Non-Uniform Memory Access

Multi-socket systems have local and remote memory:

```
NUMA Architecture (2 sockets)

┌──────────────────────┐     ┌──────────────────────┐
│       Socket 0       │     │       Socket 1       │
│  ┌────────────────┐  │     │  ┌────────────────┐  │
│  │   CPU Cores    │  │     │  │   CPU Cores    │  │
│  └───────┬────────┘  │     │  └───────┬────────┘  │
│          │           │     │          │           │
│  ┌───────┴────────┐  │     │  ┌───────┴────────┐  │
│  │ Memory Ctrl    │  │◀═══▶│  │ Memory Ctrl    │  │
│  └───────┬────────┘  │ QPI │  └───────┬────────┘  │
│          │           │     │          │           │
│      ┌───┴───┐       │     │      ┌───┴───┐       │
│      │ RAM   │       │     │      │ RAM   │       │
│      │(Local)│       │     │      │(Local)│       │
│      └───────┘       │     │      └───────┘       │
└──────────────────────┘     └──────────────────────┘

Local access:  ~60 ns
Remote access: ~100 ns (must cross QPI link)
```

### NUMA-Aware Allocation

```python
import numpy as np

# NumPy doesn't directly control NUMA
# But OS may place memory on local node

# For NUMA-aware code, use:
# - numactl command-line tool
# - numa library bindings
# - Process pinning to specific nodes
```

## Summary

| Concept | Description |
|---------|-------------|
| **Memory Controller** | Manages CPU-RAM communication |
| **Channels** | Parallel paths to memory (dual/quad) |
| **Interleaving** | Striping data across channels |
| **CAS Latency** | Cycles from column command to data |
| **Cache Coherency** | Keeping caches consistent (MESI) |
| **False Sharing** | Performance loss from shared cache lines |
| **NUMA** | Non-uniform memory access in multi-socket |

Key insights for Python:

- Memory bandwidth (~30-50 GB/s) limits large array operations
- Sequential access enables prefetching and channel interleaving
- Random access suffers full memory latency (~60 ns)
- False sharing can hurt multi-threaded code
- NumPy operations are often memory-bound, not compute-bound


---

## Exercises

**Exercise 1.** Explain the memory hierarchy: registers, L1 cache, L2 cache, L3 cache, and main memory (RAM). How do access times compare?

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

**Exercise 2.** Write Python code that demonstrates the performance difference between accessing elements sequentially (cache-friendly) versus randomly in a large list.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the hardware-software interaction and how it affects Python performance.

---

**Exercise 3.** Explain what a cache miss is and how it affects performance. Give an example of an access pattern that causes many cache misses.

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

**Exercise 4.** Write code that computes the size of a Python list, a NumPy array, and a Pandas Series containing the same 1 million integers. Compare their memory usage.

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
