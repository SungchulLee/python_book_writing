# Single Machine vs Cluster

!!! tip "Mental Model"
    A single machine is like one strong worker -- simple to manage but limited by what one person can carry. A cluster is a team of workers that can share the load, but now you pay the cost of communication and coordination. Use one machine until you hit a hard wall (RAM, time, or availability), then distribute.

## When One Computer Isn't Enough

A single machine has hard limits. When you exceed them, you need multiple machines working together.

```
Single Machine Limits:

┌─────────────────────────────────────────────────────────────┐
│                    One Computer                             │
│                                                             │
│  CPU Cores:     Limited (4-128)                             │
│  RAM:           Limited (8 GB - 2 TB)                       │
│  Storage:       Limited (256 GB - 100 TB)                   │
│  GPU Memory:    Limited (8-80 GB per GPU)                   │
│  Availability:  Single point of failure                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Cluster of Machines:

┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Node 1   │  │ Node 2   │  │ Node 3   │  │ Node N   │
│ 64 cores │  │ 64 cores │  │ 64 cores │  │ 64 cores │
│ 256 GB   │  │ 256 GB   │  │ 256 GB   │  │ 256 GB   │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     └──────────────┴──────────────┴──────────────┘
                    Network Fabric
                    
Combined: 64N cores, 256N GB RAM, fault tolerant
```

## Scaling Strategies

### Vertical Scaling (Scale Up)

Get a bigger machine:

```
Vertical Scaling:

Before:           After:
┌──────────┐      ┌────────────────┐
│ 4 cores  │  →   │   64 cores     │
│ 16 GB    │      │   512 GB       │
│ 1 GPU    │      │   8 GPUs       │
└──────────┘      └────────────────┘

Pros:
  + Simple (no code changes)
  + No network overhead
  + Easy to manage

Cons:
  - Hard limits exist
  - Expensive at high end
  - Single point of failure
```

### Horizontal Scaling (Scale Out)

Add more machines:

```
Horizontal Scaling:

Before:                After:
┌──────────┐           ┌──────────┐ ┌──────────┐ ┌──────────┐
│ 4 cores  │    →      │ 4 cores  │ │ 4 cores  │ │ 4 cores  │
│ 16 GB    │           │ 16 GB    │ │ 16 GB    │ │ 16 GB    │
└──────────┘           └──────────┘ └──────────┘ └──────────┘

Pros:
  + Nearly unlimited scale
  + Fault tolerant
  + Cost-effective (commodity hardware)

Cons:
  - Code complexity
  - Network overhead
  - Coordination challenges
```

## When to Use a Cluster

### Decision Framework

```python
def need_cluster(
    data_size_gb,
    memory_required_gb,
    compute_hours_single,
    availability_requirement,
    local_machine_specs
):
    """Determine if a cluster is needed."""
    
    reasons = []
    
    # Memory constraint
    if memory_required_gb > local_machine_specs['ram_gb'] * 0.8:
        reasons.append(f"Data ({memory_required_gb} GB) exceeds RAM")
    
    # Time constraint
    if compute_hours_single > 24:
        reasons.append(f"Computation too slow ({compute_hours_single}h)")
    
    # Availability constraint
    if availability_requirement == '99.99%':
        reasons.append("High availability requires redundancy")
    
    # Storage constraint
    if data_size_gb > local_machine_specs['storage_gb'] * 0.8:
        reasons.append(f"Data exceeds storage capacity")
    
    if reasons:
        print("Cluster recommended:")
        for r in reasons:
            print(f"  - {r}")
        return True
    else:
        print("Single machine sufficient")
        return False
```

### Common Thresholds

| Constraint | Single Machine Limit | Cluster Benefit |
|------------|---------------------|-----------------|
| **RAM** | ~2 TB max | Aggregate memory |
| **Compute** | Hours/days | Parallel speedup |
| **Storage** | ~100 TB | Distributed storage |
| **Availability** | ~99% | Redundancy → 99.99%+ |
| **Throughput** | Limited I/O | Parallel I/O |

## Cluster Architectures

### Shared-Nothing Architecture

Each node is independent:

```
Shared-Nothing:

┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Node 1    │  │   Node 2    │  │   Node 3    │
│ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │
│ │   CPU   │ │  │ │   CPU   │ │  │ │   CPU   │ │
│ │   RAM   │ │  │ │   RAM   │ │  │ │   RAM   │ │
│ │  Disk   │ │  │ │  Disk   │ │  │ │  Disk   │ │
│ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       └─────────────────┴─────────────────┘
                   Network Only

Examples: Hadoop, Spark, Cassandra
Pros: Scales well, fault tolerant
Cons: Data must be partitioned
```

### Shared-Storage Architecture

Nodes share a storage layer:

```
Shared-Storage:

┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Node 1    │  │   Node 2    │  │   Node 3    │
│ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │
│ │   CPU   │ │  │ │   CPU   │ │  │ │   CPU   │ │
│ │   RAM   │ │  │ │   RAM   │ │  │ │   RAM   │ │
│ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       └─────────────────┴─────────────────┘
                        │
              ┌─────────┴─────────┐
              │  Shared Storage   │
              │   (SAN / NFS)     │
              └───────────────────┘

Examples: Traditional databases, HPC
Pros: Simpler data management
Cons: Storage can be bottleneck
```

## Data Parallelism

### Partition Data Across Nodes

```
Data Parallelism (MapReduce pattern):

Original Data: [A B C D E F G H I J K L]

Partition:
  Node 1: [A B C D]
  Node 2: [E F G H]
  Node 3: [I J K L]

Process in parallel:
  Node 1: process([A B C D]) → result1
  Node 2: process([E F G H]) → result2
  Node 3: process([I J K L]) → result3

Combine:
  final_result = combine(result1, result2, result3)
```

### Python with Dask

```python
import dask.dataframe as dd

# Single machine pandas - limited by RAM
# import pandas as pd
# df = pd.read_csv('huge_file.csv')  # Fails if > RAM

# Dask - works across cluster
df = dd.read_csv('huge_file.csv')  # Lazy, partitioned

# Same pandas API, distributed execution
result = df.groupby('category').sum().compute()
```

### Python with PySpark

```python
from pyspark.sql import SparkSession

# Create Spark session (connects to cluster)
spark = SparkSession.builder \
    .appName("MyApp") \
    .master("spark://cluster:7077") \
    .getOrCreate()

# Load distributed dataset
df = spark.read.csv("hdfs://cluster/huge_file.csv")

# Operations distributed across cluster
result = df.groupBy("category").sum().collect()
```

## Challenges of Distributed Computing

### 1. Network Overhead

```
Single Machine:
  Memory access: ~60 ns

Cluster:
  Network access: ~100,000 ns (100 μs)
                  ~1,000,000 ns (1 ms) across datacenter

Network is 1000-10000x slower than memory!
```

### 2. Partial Failures

```
Single Machine:
  Either works or doesn't

Cluster:
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │ Node 1   │  │ Node 2   │  │ Node 3   │
  │   OK     │  │  FAILED  │  │   OK     │
  └──────────┘  └──────────┘  └──────────┘
  
  What happens to Node 2's work?
  Need: Retry, redundancy, checkpointing
```

### 3. Coordination

```
Problems that arise:
  - Which node handles which data?
  - How to synchronize results?
  - What if nodes disagree?
  - How to handle stragglers?

Solutions:
  - Consensus protocols (Paxos, Raft)
  - Distributed coordination (ZooKeeper)
  - Idempotent operations
  - Speculative execution
```

## Comparison Summary

| Aspect | Single Machine | Cluster |
|--------|----------------|---------|
| **Setup** | Simple | Complex |
| **Scaling** | Limited | Nearly unlimited |
| **Latency** | Nanoseconds | Microseconds-milliseconds |
| **Fault tolerance** | None | Built-in |
| **Cost** | Lower initially | Higher, but scales better |
| **Code complexity** | Simple | Distributed algorithms |
| **Debugging** | Easy | Hard |

## Decision Checklist

```
Use Single Machine when:
  □ Data fits in memory (with headroom)
  □ Computation completes in acceptable time
  □ Downtime is acceptable
  □ Simpler is better

Use Cluster when:
  □ Data exceeds single machine capacity
  □ Need faster results (parallel speedup)
  □ Require high availability
  □ Workload is embarrassingly parallel
  □ Already using distributed frameworks
```

## Starting Point Recommendations

```
Data Size        Recommended Approach
─────────────────────────────────────────────
< 10 GB          Single machine, pandas
10-100 GB        Single machine, chunked processing
100 GB - 1 TB    Consider Dask (single or cluster)
1-10 TB          Spark cluster
> 10 TB          Dedicated big data infrastructure
```


---

## Exercises

**Exercise 1.** Explain the advantages and disadvantages of using a single powerful machine versus a cluster of machines for computation.

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

**Exercise 2.** Describe Amdahl's Law and explain how it limits the speedup from parallelization.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the hardware-software interaction and how it affects Python performance.

---

**Exercise 3.** Write Python code using the `multiprocessing` module to parallelize a simple computation across multiple CPU cores.

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

**Exercise 4.** Explain the communication overhead in distributed computing. Why doesn't doubling the number of machines always halve the computation time?

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
