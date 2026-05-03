# System Bus

!!! tip "Mental Model"
    A bus is the highway system inside your computer. The address bus names the destination, the data bus carries the cargo, and the control bus acts as the traffic signals. Just like a real highway, bandwidth is finite and congestion creates bottlenecks -- understanding bus speeds tells you why some operations are inherently slower than others.

## What is a Bus?

A **bus** is a communication pathway that transfers data between computer components. Think of it as a highway system connecting different parts of the computer.

```
┌─────────────────────────────────────────────────────────────┐
│                        System Bus                           │
│  ═══════════════════════════════════════════════════════   │
│       │           │           │           │                 │
│   ┌───┴───┐   ┌───┴───┐   ┌───┴───┐   ┌───┴───┐           │
│   │  CPU  │   │  RAM  │   │  GPU  │   │  I/O  │           │
│   └───────┘   └───────┘   └───────┘   └───────┘           │
└─────────────────────────────────────────────────────────────┘
```

## Bus Components

A bus consists of three types of lines:

### 1. Address Bus

Specifies **where** to read/write data:

```
Address Bus (unidirectional: CPU → Memory)
┌─────┐                              ┌─────────┐
│ CPU │ ══════ Address Lines ══════▶ │ Memory  │
└─────┘    (e.g., 0x7FFF0000)        └─────────┘

Width determines addressable memory:
  32-bit address bus → 2³² = 4 GB addressable
  64-bit address bus → 2⁶⁴ = 16 EB addressable (theoretical)
```

### 2. Data Bus

Transfers **actual data** between components:

```
Data Bus (bidirectional)
┌─────┐                              ┌─────────┐
│ CPU │ ◀══════ Data Lines ═══════▶ │ Memory  │
└─────┘     (e.g., 64 bits wide)    └─────────┘

Width determines transfer size per cycle:
  32-bit data bus → 4 bytes per transfer
  64-bit data bus → 8 bytes per transfer
```

### 3. Control Bus

Carries **command signals**:

```
Control Bus (various directions)
┌─────┐                              ┌─────────┐
│ CPU │ ◀═══ Control Signals ══════▶ │ Memory  │
└─────┘                              └─────────┘

Signals include:
  - Read/Write
  - Clock
  - Interrupt
  - Bus Request/Grant
```

## Bus Operation

### Read Operation

```
CPU wants to read from address 0x1000:

1. CPU places 0x1000 on Address Bus      ────▶
2. CPU sets Read signal on Control Bus   ────▶
3. Memory reads data at 0x1000
4. Memory places data on Data Bus        ◀────
5. CPU reads data from Data Bus
```

### Write Operation

```
CPU wants to write 42 to address 0x1000:

1. CPU places 0x1000 on Address Bus      ────▶
2. CPU places 42 on Data Bus             ────▶
3. CPU sets Write signal on Control Bus  ────▶
4. Memory stores 42 at address 0x1000
```

## Bus Hierarchy

Modern computers have multiple buses at different speeds:

```
┌─────────────────────────────────────────────────────────────┐
│                          CPU                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                Internal Bus (fastest)                │   │
│  │         Registers ←→ ALU ←→ Cache                   │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              │     Front-Side Bus / QPI     │  (~25 GB/s)
              │     (CPU ↔ Memory Controller)│
              └──────────────┬──────────────┘
                             │
              ┌──────────────┴──────────────┐
              │        Memory Bus            │  (~50 GB/s)
              │       (DDR4/DDR5)            │
              └──────────────┬──────────────┘
                             │
                         ┌───┴───┐
                         │  RAM  │
                         └───────┘

              ┌──────────────────────────────┐
              │         PCIe Bus             │  (~32 GB/s per x16)
              │   (CPU ↔ GPU, NVMe, etc.)    │
              └──────────────────────────────┘
```

## Bus Speed and Bandwidth

### Calculating Bus Bandwidth

```
Bandwidth = Bus Width × Clock Speed × Transfers per Clock

Example DDR4-3200:
  Width: 64 bits = 8 bytes
  Speed: 1600 MHz (base clock)
  Transfers: 2 per clock (DDR = Double Data Rate)
  
  Bandwidth = 8 × 1600 × 2 = 25,600 MB/s ≈ 25 GB/s per channel
```

### Common Bus Bandwidths

| Bus Type | Bandwidth | Use |
|----------|-----------|-----|
| CPU Internal | ~1 TB/s | Register ↔ ALU |
| L1 Cache | ~500 GB/s | L1 ↔ CPU |
| L3 Cache | ~200 GB/s | L3 ↔ L2 |
| Memory (DDR4) | ~25 GB/s | RAM ↔ CPU |
| PCIe 4.0 x16 | ~32 GB/s | GPU ↔ CPU |
| SATA III | ~600 MB/s | SSD ↔ CPU |
| USB 3.0 | ~625 MB/s | Peripherals |

## PCIe: Modern Expansion Bus

**PCIe (Peripheral Component Interconnect Express)** is the primary expansion bus:

```
PCIe Lane Configuration

x1:  [──────]           ~2 GB/s (PCIe 4.0)
x4:  [──────────────]   ~8 GB/s
x8:  [──────────────────────────]  ~16 GB/s
x16: [──────────────────────────────────────────]  ~32 GB/s
```

### PCIe Generations

| Generation | Per-Lane Bandwidth | x16 Total |
|------------|-------------------|-----------|
| PCIe 3.0 | ~1 GB/s | ~16 GB/s |
| PCIe 4.0 | ~2 GB/s | ~32 GB/s |
| PCIe 5.0 | ~4 GB/s | ~64 GB/s |
| PCIe 6.0 | ~8 GB/s | ~128 GB/s |

## Bus Contention

When multiple components need the bus simultaneously:

```
Problem: Bus Contention

Time →
Device A: [Request]────[Wait]────[Wait]────[Transfer]
Device B: ─────────[Request]────[Wait]────[Wait]────[Transfer]
Device C: ─────────────────[Request]────[Wait]────[Wait]────[Transfer]

Only one device can use the bus at a time!
```

### Bus Arbitration

A **bus arbiter** decides who gets access:

```
Arbitration Methods:

1. Priority-based: Higher priority devices go first
2. Round-robin: Fair rotation among devices
3. First-come-first-served: Queue-based
```

## Python Perspective

### Why Bus Speed Matters

```python
import numpy as np
import time

# Memory bandwidth limits computation
def memory_bound_operation():
    # 1 GB array
    arr = np.random.rand(125_000_000)  # 1 GB of float64
    
    start = time.perf_counter()
    # Simple operation - limited by memory bus
    result = np.sum(arr)
    elapsed = time.perf_counter() - start
    
    bandwidth = arr.nbytes / elapsed / 1e9
    print(f"Achieved bandwidth: {bandwidth:.1f} GB/s")
    # Typically ~30-40 GB/s, limited by memory bus

memory_bound_operation()
```

### PCIe and GPU Operations

```python
import torch

# GPU data transfer goes over PCIe
data = torch.randn(1000, 1000)

# CPU → GPU (over PCIe)
start = time.perf_counter()
data_gpu = data.to('cuda')
torch.cuda.synchronize()
transfer_time = time.perf_counter() - start

bytes_transferred = data.numel() * 4  # float32
bandwidth = bytes_transferred / transfer_time / 1e9
print(f"CPU→GPU bandwidth: {bandwidth:.1f} GB/s")
# Typically ~12-15 GB/s (PCIe limited)
```

## Summary

| Component | Function | Direction |
|-----------|----------|-----------|
| **Address Bus** | Specifies memory location | CPU → Memory |
| **Data Bus** | Transfers actual data | Bidirectional |
| **Control Bus** | Command signals | Various |

Key points:

- Bus bandwidth often limits system performance
- Multiple bus levels with different speeds
- PCIe connects high-speed devices (GPU, NVMe)
- Bus contention can create bottlenecks
- Memory bandwidth (~50 GB/s) often limits Python/NumPy performance
- GPU transfer bandwidth (~15 GB/s) limits data movement


---

## Exercises

**Exercise 1.** Explain what a system bus is and name its three main components (data bus, address bus, control bus).

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

**Exercise 2.** Explain how bus bandwidth limits the rate at which data can move between the CPU and memory. How does this relate to the 'memory wall'?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the hardware-software interaction and how it affects Python performance.

---

**Exercise 3.** Write Python code that demonstrates the concept of bandwidth limitation by comparing the time to process data from memory versus from CPU cache (using small vs large arrays).

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

**Exercise 4.** Explain what DMA (Direct Memory Access) is and how it helps reduce CPU overhead during I/O operations.

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
