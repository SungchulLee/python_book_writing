# Local vs Remote Computation

!!! tip "Mental Model"
    Choosing local vs remote is a shipping problem: if moving data costs more time than the computation itself, keep it local; if the remote machine is dramatically faster, pay the transfer tax. The sweet spot is to move computation to data when data is large, and move data to computation when you need specialized hardware.

## The Fundamental Trade-off

Where should computation happen? Locally on your machine, or remotely on a server?

```
Local Computation:
┌─────────────────────────────────────────────────────────┐
│                     Your Machine                        │
│  ┌──────────┐    ┌───────────┐    ┌──────────┐        │
│  │   Data   │───▶│  Process  │───▶│  Result  │        │
│  └──────────┘    └───────────┘    └──────────┘        │
│                                                         │
│  + No network latency                                   │
│  + Data stays private                                   │
│  - Limited by local hardware                            │
└─────────────────────────────────────────────────────────┘

Remote Computation:
┌──────────────────┐                    ┌──────────────────┐
│   Your Machine   │                    │     Server       │
│  ┌──────────┐    │    Network         │  ┌───────────┐  │
│  │   Data   │────┼───────────────────▶│  │  Process  │  │
│  └──────────┘    │    (latency)       │  └───────────┘  │
│                  │                    │        │        │
│  ┌──────────┐    │◀───────────────────┼────────┘        │
│  │  Result  │◀───│    (latency)       │                 │
│  └──────────┘    │                    │  + Powerful HW  │
│                  │                    │  + Scalable     │
│  - Network overhead                   │  - Latency cost │
└──────────────────┘                    └──────────────────┘
```

## Decision Factors

### 1. Data Size vs Computation Intensity

```
Data Size vs Computation:

Heavy computation, small data → Remote (use powerful servers)
  Example: Training ML model on 1 MB dataset
  
Light computation, large data → Local (avoid transfer)
  Example: Sum of 100 GB array
  
Heavy computation, large data → Complex decision
  Example: Training on 1 TB dataset
```

### 2. Break-Even Analysis

```python
def should_use_remote(data_size_gb, compute_time_local_s, 
                       compute_time_remote_s, bandwidth_gbps=1):
    """Determine if remote computation is faster."""
    
    # Transfer time (upload + download result)
    transfer_time = data_size_gb / (bandwidth_gbps / 8) * 2
    
    # Total remote time
    total_remote = transfer_time + compute_time_remote_s
    
    print(f"Local time: {compute_time_local_s:.1f}s")
    print(f"Remote compute: {compute_time_remote_s:.1f}s")
    print(f"Transfer overhead: {transfer_time:.1f}s")
    print(f"Total remote: {total_remote:.1f}s")
    
    return total_remote < compute_time_local_s

# Example: ML training
# Local laptop: 2 hours, Remote GPU: 10 minutes
# Data: 10 GB, Bandwidth: 100 Mbps

should_use_remote(
    data_size_gb=10,
    compute_time_local_s=7200,      # 2 hours
    compute_time_remote_s=600,      # 10 minutes
    bandwidth_gbps=0.1              # 100 Mbps
)
# Transfer: ~26 minutes
# Total remote: ~36 minutes
# Local: 120 minutes
# → Remote wins!
```

## Scenarios and Recommendations

### Scenario 1: Data Analysis

```python
import pandas as pd
import numpy as np

# Small dataset analysis → Local
df = pd.read_csv('sales_100k.csv')  # 10 MB
result = df.groupby('region').sum()  # Fast locally

# Huge dataset → Consider remote or distributed
# 100 GB of data - transfer would take hours
# Options:
#   1. Remote SQL query (send query, not data)
#   2. Distributed processing (Spark, Dask)
#   3. Sample locally, full analysis on server
```

### Scenario 2: Machine Learning

```
Training Decision Matrix:

┌─────────────────────────────────────────────────────────────┐
│                Small Model    │    Large Model              │
├─────────────────────────────────────────────────────────────┤
│ Small Data   │ Local OK       │ Remote (need GPU)           │
│              │ (minutes)      │ (hours)                     │
├───────────────────────────────┼─────────────────────────────┤
│ Large Data   │ Remote         │ Cloud (distributed)         │
│              │ (data too big) │ (need cluster)              │
└─────────────────────────────────────────────────────────────┘
```

```python
# Local training - small model, small data
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train, y_train)  # Local CPU fine

# Remote training - large model
# Send training job to cloud GPU
# Download trained model weights (small)
```

### Scenario 3: API Services

```python
# Remote makes sense for:
# - Complex NLP (GPT, BERT inference)
# - Image generation
# - Real-time translation

import openai

# Why remote?
# - Model is 100+ GB (can't run locally)
# - Requires specialized hardware
# - Latency acceptable for this use case

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Scenario 4: Real-Time Processing

```
Low-latency requirements → Local

Gaming:     Local (5ms latency max)
Video:      Local decode, remote stream
Trading:    Co-located (microseconds matter)
```

## Hybrid Approaches

### Edge Computing

Process close to data source, aggregate centrally:

```
Edge Computing Architecture:

┌─────────────────────────────────────────────────────────────┐
│                        Cloud                                │
│  ┌────────────────────────────────────────────────────┐    │
│  │           Central Aggregation & Storage            │    │
│  └────────────────────────────────────────────────────┘    │
│              ▲              ▲              ▲                │
└──────────────┼──────────────┼──────────────┼────────────────┘
               │              │              │
     ┌─────────┴───┐   ┌──────┴────┐   ┌────┴──────┐
     │   Edge      │   │   Edge    │   │   Edge    │
     │  Node 1     │   │  Node 2   │   │  Node 3   │
     └──────┬──────┘   └─────┬─────┘   └─────┬─────┘
            │                │               │
     ┌──────┴──────┐   ┌─────┴─────┐   ┌─────┴─────┐
     │   Sensors   │   │  Sensors  │   │  Sensors  │
     │ (local proc)│   │           │   │           │
     └─────────────┘   └───────────┘   └───────────┘

- Preprocess/filter locally
- Send summaries to cloud
- Reduces bandwidth by 10-100x
```

### Data Locality

Move computation to data, not data to computation:

```python
# Bad: Download all data, process locally
huge_data = remote_db.download_all()  # 1 TB!
result = process(huge_data)

# Good: Run query on remote database
result = remote_db.query("""
    SELECT region, SUM(sales)
    FROM transactions
    GROUP BY region
""")
# Only result transferred (kilobytes)
```

### Tiered Processing

```
Tiered Architecture:

User Request
     │
     ▼
┌─────────────────┐
│  Local Cache    │  ← Check local first (fastest)
│  (in-memory)    │
└────────┬────────┘
         │ Miss
         ▼
┌─────────────────┐
│   Edge Server   │  ← Check nearby server
│   (regional)    │
└────────┬────────┘
         │ Miss
         ▼
┌─────────────────┐
│  Origin Server  │  ← Full computation
│   (central)     │
└─────────────────┘
```

## Cost Considerations

```
Cost Trade-offs:

Local:
  + No network costs
  + No cloud fees
  - Hardware investment
  - Power and cooling
  - Maintenance

Remote:
  + No hardware investment
  + Elastic scaling
  + Latest hardware
  - Per-use charges
  - Data transfer costs
  - Vendor dependency

Typical break-even:
  Occasional use → Remote (pay-per-use)
  Constant use → Local/dedicated (amortized cost)
```

## Decision Framework

```python
def choose_computation_location(
    data_size_gb,
    compute_intensity,  # 'low', 'medium', 'high'
    latency_requirement_ms,
    privacy_sensitive,
    frequency  # 'one-time', 'daily', 'continuous'
):
    """Framework for local vs remote decision."""
    
    # Hard constraints
    if latency_requirement_ms < 10:
        return "LOCAL (latency requirement)"
    
    if privacy_sensitive and not compliant_remote_available():
        return "LOCAL (privacy requirement)"
    
    # Data size considerations
    if data_size_gb > 100 and compute_intensity == 'low':
        return "LOCAL (transfer cost too high)"
    
    if data_size_gb < 1 and compute_intensity == 'high':
        return "REMOTE (leverage powerful hardware)"
    
    # Frequency considerations  
    if frequency == 'continuous':
        if local_hardware_sufficient():
            return "LOCAL (avoid ongoing costs)"
        else:
            return "DEDICATED REMOTE (reserved instances)"
    
    # Default for occasional, moderate workloads
    return "REMOTE (flexibility)"
```

## Summary

| Factor | Favors Local | Favors Remote |
|--------|--------------|---------------|
| **Data Size** | Large (transfer cost) | Small |
| **Computation** | Light | Heavy |
| **Latency** | Critical (<10ms) | Tolerant |
| **Hardware** | Sufficient locally | Need special (GPU) |
| **Privacy** | Sensitive | Not critical |
| **Frequency** | Continuous | Occasional |
| **Cost** | Owned hardware | Pay-per-use |

Key principles:

1. **Move computation to data** when data is large
2. **Move data to computation** when data is small and compute is specialized
3. **Cache aggressively** to avoid repeated transfers
4. **Consider hybrid** approaches for complex workloads
5. **Profile actual performance** before deciding


---

## Exercises

**Exercise 1.** Explain the performance difference between accessing data locally (on disk) versus remotely (over a network). What are the typical latencies?

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

**Exercise 2.** Describe the trade-offs of storing data locally versus in the cloud for a data science project.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the hardware-software interaction and how it affects Python performance.

---

**Exercise 3.** Write Python code that measures the time to read a local file versus downloading a similar-sized file from the internet.

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

**Exercise 4.** Explain what edge computing is and how it addresses the latency problem of cloud computing.

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
