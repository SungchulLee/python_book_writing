# GPU Clusters

!!! tip "Mental Model"
    A GPU cluster is a team of powerful machines, each packed with GPUs, connected by a fast network. The challenge is not raw compute -- individual GPUs are fast -- but coordination: synchronizing gradients across nodes costs time that grows with cluster size. Scaling efficiency is the gap between the parallelism you buy and the speedup you actually get.

## Why GPU Clusters?

Single GPUs have limits. Large-scale deep learning and scientific computing often require multiple GPUs across multiple machines.

```
GPU Scaling Journey:

Single GPU:           Multi-GPU (one machine):     GPU Cluster:
┌────────────┐        ┌────────────────────┐      ┌─────────┐ ┌─────────┐
│    GPU     │   →    │ GPU  GPU  GPU  GPU │  →   │ 8 GPUs  │ │ 8 GPUs  │
│  (8-80 GB) │        │ (connected via     │      │ Node 1  │ │ Node 2  │
└────────────┘        │  NVLink/PCIe)      │      └────┬────┘ └────┬────┘
                      └────────────────────┘           │          │
                                                       └────┬─────┘
                                                            │
                                                      ┌─────┴─────┐
                                                      │ Network   │
                                                      │(InfiniBand)│
                                                      └───────────┘
```

## GPU Cluster Architecture

### Typical Node Configuration

```
GPU Node (e.g., DGX A100):

┌─────────────────────────────────────────────────────────────┐
│                        GPU Node                             │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                    8 × A100 GPUs                       │ │
│  │   ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                     │ │
│  │   │ GPU │═│ GPU │═│ GPU │═│ GPU │                     │ │
│  │   │  0  │ │  1  │ │  2  │ │  3  │  NVLink: 600 GB/s   │ │
│  │   └──╪──┘ └──╪──┘ └──╪──┘ └──╪──┘                     │ │
│  │      ╪═══════╪═══════╪═══════╪                        │ │
│  │   ┌──╪──┐ ┌──╪──┐ ┌──╪──┐ ┌──╪──┐                     │ │
│  │   │ GPU │═│ GPU │═│ GPU │═│ GPU │                     │ │
│  │   │  4  │ │  5  │ │  6  │ │  7  │                     │ │
│  │   └─────┘ └─────┘ └─────┘ └─────┘                     │ │
│  └───────────────────────────────────────────────────────┘ │
│                           │                                 │
│  ┌───────────────────────┴───────────────────────────────┐ │
│  │          2 × CPU (AMD EPYC / Intel Xeon)              │ │
│  │                    1-2 TB RAM                          │ │
│  └───────────────────────────────────────────────────────┘ │
│                           │                                 │
│                    InfiniBand NIC                          │
│                     (200-400 Gbps)                         │
└─────────────────────────────────────────────────────────────┘
```

### Cluster Interconnect

```
GPU Cluster Network:

┌──────────┐     ┌──────────┐     ┌──────────┐
│  Node 1  │     │  Node 2  │     │  Node N  │
│  8 GPUs  │     │  8 GPUs  │     │  8 GPUs  │
└────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │
     │     InfiniBand Fabric           │
     │     (200-400 Gbps/node)         │
     └────────────────┴────────────────┘

Bandwidth Hierarchy:
  GPU Memory:        ~2000 GB/s
  NVLink (in-node):  ~600 GB/s
  InfiniBand:        ~50 GB/s (200 Gbps)
  Ethernet:          ~12 GB/s (100 Gbps)
```

## Distributed Training Strategies

### Data Parallelism

Each GPU has full model copy, different data:

```
Data Parallelism:

                    ┌─────────────┐
                    │ Full Dataset │
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
      ┌────────┐      ┌────────┐      ┌────────┐
      │Batch 1 │      │Batch 2 │      │Batch 3 │
      └────┬───┘      └────┬───┘      └────┬───┘
           │               │               │
      ┌────▼───┐      ┌────▼───┐      ┌────▼───┐
      │ GPU 0  │      │ GPU 1  │      │ GPU 2  │
      │ Model  │      │ Model  │      │ Model  │
      │ Copy   │      │ Copy   │      │ Copy   │
      └────┬───┘      └────┬───┘      └────┬───┘
           │               │               │
           └───────────────┼───────────────┘
                           ▼
                 ┌─────────────────┐
                 │ Sync Gradients  │
                 │   (AllReduce)   │
                 └─────────────────┘
```

### Model Parallelism

Model split across GPUs:

```
Model Parallelism:

Large Model (won't fit on one GPU):

┌─────────────────────────────────────────────────┐
│              Neural Network Layers              │
│  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐      │
│  │Layer 1│→│Layer 2│→│Layer 3│→│Layer 4│      │
│  └───────┘ └───────┘ └───────┘ └───────┘      │
└─────────────────────────────────────────────────┘

Split across GPUs:

┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  GPU 0  │───▶│  GPU 1  │───▶│  GPU 2  │───▶│  GPU 3  │
│ Layer 1 │    │ Layer 2 │    │ Layer 3 │    │ Layer 4 │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

### Pipeline Parallelism

Combine model parallelism with micro-batching:

```
Pipeline Parallelism:

Time →
       ┌─────┬─────┬─────┬─────┬─────┬─────┐
GPU 0: │ B1  │ B2  │ B3  │ B4  │     │     │
       └─────┴──┬──┴──┬──┴──┬──┴─────┴─────┘
                │     │     │
       ┌────────▼──┬──▼──┬──▼──┬─────┬─────┐
GPU 1: │     │ B1  │ B2  │ B3  │ B4  │     │
       └─────┴─────┴──┬──┴──┬──┴──┬──┴─────┘
                      │     │     │
       ┌──────────────▼──┬──▼──┬──▼──┬─────┐
GPU 2: │     │     │ B1  │ B2  │ B3  │ B4  │
       └─────┴─────┴─────┴─────┴─────┴─────┘

B1, B2, ... = Micro-batches
GPUs stay busy with different batches
```

## PyTorch Distributed Training

### Data Parallel (Single Node)

```python
import torch
import torch.nn as nn

# Simple DataParallel (single node, multiple GPUs)
model = MyModel()
model = nn.DataParallel(model)  # Wraps model
model = model.cuda()

# Training loop unchanged
for data, target in dataloader:
    data, target = data.cuda(), target.cuda()
    output = model(data)  # Automatically split across GPUs
    loss = criterion(output, target)
    loss.backward()
    optimizer.step()
```

### Distributed Data Parallel (Multi-Node)

```python
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

# Initialize distributed process group
dist.init_process_group(
    backend='nccl',  # NVIDIA Collective Communications Library
    init_method='env://',
    world_size=world_size,
    rank=rank
)

# Create model and wrap with DDP
model = MyModel().cuda()
model = DDP(model, device_ids=[local_rank])

# Use DistributedSampler for data
sampler = torch.utils.data.distributed.DistributedSampler(dataset)
dataloader = DataLoader(dataset, sampler=sampler, batch_size=32)

# Training loop
for epoch in range(num_epochs):
    sampler.set_epoch(epoch)  # Shuffle differently each epoch
    for data, target in dataloader:
        data, target = data.cuda(), target.cuda()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()  # Gradients automatically synchronized
        optimizer.step()
```

### Launch Script

```bash
# Launch across 4 nodes, 8 GPUs each
torchrun \
    --nnodes=4 \
    --nproc_per_node=8 \
    --rdzv_endpoint=master:29500 \
    train.py
```

## Scaling Efficiency

### Communication Overhead

```
Scaling Efficiency:

Perfect linear scaling (theoretical):
  1 GPU:  100 samples/sec
  8 GPUs: 800 samples/sec
  64 GPUs: 6400 samples/sec

Actual (with communication overhead):
  1 GPU:  100 samples/sec
  8 GPUs: 700 samples/sec (87.5% efficiency)
  64 GPUs: 4000 samples/sec (62.5% efficiency)

Efficiency drops as:
  - More GPUs = more synchronization
  - Smaller batches = higher communication ratio
  - Slower interconnect = longer waits
```

### Batch Size Considerations

```python
# Effective batch size = per_gpu_batch × num_gpus

# Single GPU: batch_size = 32
# 8 GPUs: effective_batch = 32 × 8 = 256
# 64 GPUs: effective_batch = 32 × 64 = 2048

# May need to adjust learning rate
# Linear scaling rule: lr_new = lr_base × num_gpus
learning_rate = base_lr * world_size
```

## Frameworks for GPU Clusters

| Framework | Use Case | Complexity |
|-----------|----------|------------|
| **PyTorch DDP** | General distributed training | Medium |
| **DeepSpeed** | Large model training | Medium-High |
| **Megatron-LM** | Massive language models | High |
| **Horovod** | Framework-agnostic | Medium |
| **Ray** | General distributed ML | Medium |

### DeepSpeed Example

```python
import deepspeed

# Config for ZeRO optimization
ds_config = {
    "train_batch_size": 256,
    "gradient_accumulation_steps": 4,
    "fp16": {"enabled": True},
    "zero_optimization": {
        "stage": 2,  # Partition gradients and optimizer states
        "offload_optimizer": {"device": "cpu"}
    }
}

# Initialize DeepSpeed
model, optimizer, _, _ = deepspeed.initialize(
    model=model,
    config=ds_config,
    model_parameters=model.parameters()
)

# Training loop
for batch in dataloader:
    outputs = model(batch)
    loss = compute_loss(outputs)
    model.backward(loss)
    model.step()
```

## Cost Considerations

```
GPU Cluster Costs (Cloud):

┌─────────────────────────────────────────────────────────────┐
│  Configuration          │ Hourly Cost │ Monthly (24/7)     │
├─────────────────────────┼─────────────┼────────────────────┤
│  1 × A100 (40GB)        │    ~\$3      │    ~\$2,200         │
│  8 × A100 (one node)    │    ~\$25     │    ~\$18,000        │
│  64 × A100 (8 nodes)    │    ~\$200    │    ~\$144,000       │
│  512 × A100 (64 nodes)  │    ~\$1,600  │    ~\$1,150,000     │
└─────────────────────────┴─────────────┴────────────────────┘

Cost optimization:
  - Spot instances (60-70% cheaper, can be interrupted)
  - Reserved capacity (30-40% cheaper, commitment)
  - Right-size your cluster (don't over-provision)
```

## Summary

| Aspect | Single GPU | Multi-GPU Node | GPU Cluster |
|--------|------------|----------------|-------------|
| **Memory** | 8-80 GB | 64-640 GB | Terabytes |
| **Interconnect** | N/A | NVLink (600 GB/s) | InfiniBand (50 GB/s) |
| **Complexity** | Simple | Medium | High |
| **Use Case** | Development, small models | Medium models | Large models, fast training |

Key points:

- GPU clusters enable training models too large for single GPUs
- Data parallelism is simplest; model parallelism for huge models
- Communication overhead limits scaling efficiency
- NVLink (intra-node) >> InfiniBand (inter-node) >> Ethernet
- Choose cluster size based on model size and time constraints
- Cost scales roughly linearly; efficiency doesn't


---

## Exercises

**Exercise 1.** Explain the difference between data parallelism and model parallelism in distributed GPU training.

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

**Exercise 2.** Explain what CUDA is and why it is important for GPU computing. Can Python code use CUDA?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the hardware-software interaction and how it affects Python performance.

---

**Exercise 3.** Describe the role of NCCL (NVIDIA Collective Communication Library) in multi-GPU training.

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

**Exercise 4.** Explain what GPU memory (VRAM) is and why running out of VRAM is a common issue in deep learning. What strategies help mitigate this?

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
