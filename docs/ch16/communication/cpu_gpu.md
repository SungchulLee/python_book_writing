# CPU-GPU Communication

!!! tip "Mental Model"
    Think of the CPU and GPU as two offices in different buildings connected by a narrow hallway (PCIe bus). Each office is fast internally, but passing documents between them is slow. The key to performance is minimizing trips through the hallway and carrying as much as possible each time.

## The CPU-GPU Boundary

CPUs and GPUs have separate memory spaces connected by the PCIe bus:

```
┌────────────────────────┐          ┌────────────────────────┐
│         CPU            │          │          GPU           │
│  ┌──────────────────┐  │          │  ┌──────────────────┐  │
│  │    CPU Cores     │  │          │  │   CUDA Cores     │  │
│  └────────┬─────────┘  │          │  └────────┬─────────┘  │
│           │            │          │           │            │
│  ┌────────┴─────────┐  │          │  ┌────────┴─────────┐  │
│  │    System RAM    │  │   PCIe   │  │   GPU Memory     │  │
│  │    (16-128 GB)   │◀═╬════════▶╬═▶│    (8-80 GB)     │  │
│  └──────────────────┘  │ ~32 GB/s │  └──────────────────┘  │
└────────────────────────┘          └────────────────────────┘
                              ▲
                              │
                    Major bottleneck!
```

## PCIe: The Connection

### PCIe Bandwidth

| Generation | Per-Lane | x16 Slot | Bidirectional |
|------------|----------|----------|---------------|
| PCIe 3.0 | ~1 GB/s | ~16 GB/s | ~32 GB/s |
| PCIe 4.0 | ~2 GB/s | ~32 GB/s | ~64 GB/s |
| PCIe 5.0 | ~4 GB/s | ~64 GB/s | ~128 GB/s |

### Bandwidth Comparison

```
GPU Internal Memory:    ████████████████████████████  ~1000 GB/s
System RAM:             ████████████                  ~50 GB/s
PCIe 4.0 x16:           █████                         ~32 GB/s

PCIe is 30-60x slower than GPU memory!
```

## Data Transfer Operations

### Basic Transfer Pattern

```python
import torch
import time

# Create data on CPU
cpu_tensor = torch.randn(10000, 10000)  # 400 MB

# Transfer to GPU (copy)
start = time.perf_counter()
gpu_tensor = cpu_tensor.to('cuda')
torch.cuda.synchronize()  # Wait for transfer to complete
h2d_time = time.perf_counter() - start

# Transfer back to CPU (copy)
start = time.perf_counter()
result = gpu_tensor.to('cpu')
torch.cuda.synchronize()
d2h_time = time.perf_counter() - start

size_gb = cpu_tensor.numel() * 4 / 1e9

print(f"Host→Device: {size_gb/h2d_time:.1f} GB/s")
print(f"Device→Host: {size_gb/d2h_time:.1f} GB/s")
```

Typical output:

```
Host→Device: 12.5 GB/s
Device→Host: 11.8 GB/s
```

### Why Measured < Theoretical?

```
PCIe 4.0 x16 theoretical: 32 GB/s

Actual achieved: 12-15 GB/s

Reasons for gap:
  - Protocol overhead
  - DMA setup time
  - Memory allocation
  - Driver overhead
  - System interrupts
```

## Transfer Methods

### Synchronous Transfer (Default)

```python
import torch

# Blocks until complete
gpu_data = cpu_data.to('cuda')  # CPU waits
result = gpu_data @ gpu_data    # Then compute
```

### Asynchronous Transfer

```python
import torch

# Non-blocking transfer with streams
stream = torch.cuda.Stream()

with torch.cuda.stream(stream):
    # Transfer happens asynchronously
    gpu_data = cpu_data.to('cuda', non_blocking=True)

# Can do other CPU work here...
cpu_work()

# Wait when you need the result
stream.synchronize()
result = gpu_data @ gpu_data
```

### Pinned (Page-Locked) Memory

```python
import torch

# Regular memory (pageable)
regular = torch.randn(10000, 10000)

# Pinned memory (faster transfers)
pinned = torch.randn(10000, 10000, pin_memory=True)

# Transfer comparison
def time_transfer(tensor):
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    
    start.record()
    gpu = tensor.to('cuda', non_blocking=True)
    end.record()
    torch.cuda.synchronize()
    
    return start.elapsed_time(end)

print(f"Regular: {time_transfer(regular):.1f} ms")
print(f"Pinned:  {time_transfer(pinned):.1f} ms")
```

### Why Pinned Memory is Faster

```
Regular (Pageable) Memory Transfer:
┌────────────────┐    ┌────────────────┐    ┌──────────────┐
│ User Buffer    │ →  │ Pinned Buffer  │ →  │ GPU Memory   │
│ (may be paged) │    │ (DMA staging)  │    │              │
└────────────────┘    └────────────────┘    └──────────────┘
     Extra copy needed!

Pinned Memory Transfer:
┌────────────────┐                         ┌──────────────┐
│ Pinned Buffer  │ ──────── DMA ────────→ │ GPU Memory   │
│ (always in RAM)│                         │              │
└────────────────┘                         └──────────────┘
     Direct transfer!
```

## Minimizing Transfer Overhead

### Strategy 1: Batch Transfers

```python
# Bad: Transfer every iteration
for epoch in range(100):
    for batch in dataloader:
        batch_gpu = batch.to('cuda')  # Transfer every batch!
        result = model(batch_gpu)

# Good: Use DataLoader with pin_memory
dataloader = DataLoader(dataset, pin_memory=True, num_workers=4)

for epoch in range(100):
    for batch in dataloader:
        # Transfer overlaps with previous batch processing
        batch_gpu = batch.to('cuda', non_blocking=True)
        result = model(batch_gpu)
```

### Strategy 2: Keep Data on GPU

```python
# Bad: Round-trip every operation
x_gpu = x_cpu.to('cuda')
y = model(x_gpu)
y_cpu = y.to('cpu')  # Why transfer back?
z_gpu = y_cpu.to('cuda')  # Just to transfer again?

# Good: Stay on GPU
x_gpu = x_cpu.to('cuda')
y_gpu = model(x_gpu)
z_gpu = another_model(y_gpu)  # Stay on GPU
final = z_gpu.to('cpu')  # Transfer only at the end
```

### Strategy 3: Overlap Transfer and Compute

```python
import torch

# Use multiple streams to overlap
stream1 = torch.cuda.Stream()
stream2 = torch.cuda.Stream()

# While computing on batch N, transfer batch N+1
for i in range(num_batches):
    with torch.cuda.stream(stream1):
        # Transfer next batch
        next_batch = batches[i+1].to('cuda', non_blocking=True)
    
    with torch.cuda.stream(stream2):
        # Compute on current batch
        result = model(current_batch)
    
    current_batch = next_batch
    torch.cuda.synchronize()
```

## Unified Memory (CUDA Managed Memory)

CUDA can automatically manage CPU-GPU transfers:

```python
import cupy as cp

# Managed memory - system handles transfers
managed = cp.cuda.managed_memory.alloc(size)

# Data migrates on demand between CPU and GPU
# Simpler but less control over performance
```

### Trade-offs

| Approach | Performance | Complexity |
|----------|-------------|------------|
| Manual Transfers | Best (with optimization) | High |
| Pinned Memory | Very Good | Medium |
| Managed Memory | Good | Low |

## NVLink: High-Speed GPU Connection

Some systems have NVLink for faster GPU-GPU communication:

```
PCIe (CPU ↔ GPU):     ~32 GB/s
NVLink (GPU ↔ GPU):   ~600 GB/s (per link)

┌───────────┐           ┌───────────┐
│   GPU 0   │◀═══════▶│   GPU 1   │
│           │  NVLink   │           │
└─────┬─────┘  600 GB/s └─────┬─────┘
      │                       │
      │         PCIe          │
      └───────────┬───────────┘
                  │
              ┌───┴───┐
              │  CPU  │
              └───────┘
```

## Summary

| Concept | Description |
|---------|-------------|
| **PCIe** | Bus connecting CPU and GPU (~32 GB/s) |
| **Host→Device** | CPU to GPU transfer (H2D) |
| **Device→Host** | GPU to CPU transfer (D2H) |
| **Pinned Memory** | Page-locked RAM for faster transfers |
| **Async Transfer** | Non-blocking transfers with streams |
| **NVLink** | High-speed GPU-GPU interconnect |

Key optimization strategies:

1. **Minimize transfers**: Keep data on GPU as long as possible
2. **Use pinned memory**: 1.5-2x faster transfers
3. **Batch operations**: Transfer large chunks, not small pieces
4. **Overlap compute and transfer**: Use async operations
5. **Profile transfer time**: Often dominates total time for small operations

```python
# Rule of thumb for GPU benefit:
compute_time = time_on_gpu(operation)
transfer_time = data_size / 12e9  # ~12 GB/s practical

if compute_time > transfer_time:
    print("GPU beneficial")
else:
    print("Transfer overhead too high")
```


---

## Exercises

**Exercise 1.** Explain the fundamental difference between CPU and GPU architectures. Why are GPUs better for parallel workloads?

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

**Exercise 2.** Write Python code using `numpy` to perform a large matrix multiplication, and explain why a GPU would be faster for this operation.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the hardware-software interaction and how it affects Python performance.

---

**Exercise 3.** Explain what data transfer overhead between CPU and GPU means. Why is it important to minimize transfers?

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

**Exercise 4.** Describe a scenario where running a computation on the CPU would be faster than transferring data to the GPU, computing, and transferring back.

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
