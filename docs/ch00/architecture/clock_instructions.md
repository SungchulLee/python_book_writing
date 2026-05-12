

# Clock Speed and Instructions

!!! tip "Mental Model"
    Think of a CPU as a factory assembly line: clock speed is how fast the conveyor belt moves, while instructions per cycle (IPC) is how many workers are stationed along the belt. A faster belt helps, but adding more workers per cycle often matters more -- which is why modern CPUs focus on doing more useful work each tick rather than simply ticking faster.

CPU performance depends on two fundamental factors:

1. **Clock speed** — how frequently the processor advances its internal clock
2. **Instructions per cycle (IPC)** — how much work the processor completes during each cycle

Together these determine the **instruction throughput** of a processor.

Although clock speed is often highlighted in marketing materials, modern CPU performance depends far more on **how efficiently each cycle is used**.

---

## 1. Clock Speed

The **clock speed** (or **frequency**) of a CPU is the number of clock cycles the processor performs per second.

Clock speed is measured in **Hertz (Hz)**.

| Unit | Meaning                   |
| ---- | ------------------------- |
| MHz  | million cycles per second |
| GHz  | billion cycles per second |

For example:

```
4 GHz = 4,000,000,000 cycles per second
```

Each cycle lasts:

$$
\frac{1}{4,000,000,000}
=======================
0.25 \text{ nanoseconds}
$$

---

### Clock cycle visualization

```mermaid
flowchart LR
    A[Clock signal] --> B[Cycle 1]
    B --> C[Cycle 2]
    C --> D[Cycle 3]
```

Every CPU operation occurs within these clock cycles.

---

## 2. Instructions Per Cycle (IPC)

**Instructions per cycle (IPC)** measures how many instructions the processor completes during each clock cycle.

This value depends on the CPU’s microarchitecture and the nature of the workload.

---

## Instruction throughput

The approximate instruction throughput of a processor is:

[
\text{Throughput} \approx
\text{Clock Speed} \times \text{IPC}
]

---

### Example

Consider two processors:

| CPU   | Clock | IPC |
| ----- | ----- | --- |
| CPU A | 4 GHz | 2   |
| CPU B | 3 GHz | 4   |

Instruction throughput:

```
CPU A: 4 × 2 = 8 billion instructions/sec
CPU B: 3 × 4 = 12 billion instructions/sec
```

Despite having a lower clock speed, **CPU B is faster**.

This example shows why clock speed alone is not a reliable measure of performance.

---

## 3. Instruction Pipelining

Modern CPUs increase throughput using **instruction pipelines**.

Instead of executing one instruction completely before starting the next, the processor divides execution into stages and overlaps them.

Typical pipeline stages:

```
Fetch → Decode → Execute → Writeback
```

---

### Pipeline example

```
Cycle     Stage1   Stage2   Stage3   Stage4
1         I1
2         I2       I1
3         I3       I2       I1
4         I4       I3       I2       I1
```

Once the pipeline is filled, the processor can complete roughly **one instruction per cycle**.

---

### Pipeline visualization

```mermaid
flowchart LR
    A[Fetch] --> B[Decode]
    B --> C[Execute]
    C --> D[Writeback]
```

Pipelining increases throughput but introduces new challenges.

---

## 4. Superscalar Execution

Modern CPUs are **superscalar**, meaning they can execute multiple instructions simultaneously.

They contain several independent execution units such as:

* integer ALUs
* floating-point units
* load/store units
* vector units

This allows a processor to issue multiple instructions per cycle.

---

### Superscalar architecture

```mermaid
flowchart LR
    Decode --> ALU1
    Decode --> ALU2
    Decode --> FPU
```

Because multiple instructions may execute simultaneously, IPC can exceed 1.

High-performance processors often achieve IPC values between **2 and 6** depending on workload.

---

## 5. Out-of-Order Execution

Programs are written assuming instructions execute sequentially.

However, modern CPUs dynamically **reorder instructions** internally.

This technique is called **out-of-order execution**.

If one instruction stalls while waiting for memory, the processor can execute other independent instructions instead.

---

### Example

Original program order:

```
1: load A
2: add B
3: multiply C
```

If the load instruction stalls, the processor may execute instructions 2 or 3 first.

---

### Out-of-order execution visualization

```mermaid
flowchart LR
    A[Instruction Queue] --> B[Scheduler]
    B --> C[Execution Units]
```

This mechanism keeps execution units busy and improves IPC.

---

## 6. Branch Prediction

Conditional branches introduce uncertainty into the instruction pipeline.

Example:

```python
if x > 0:
    do_A()
else:
    do_B()
```

The processor does not immediately know which path will execute.

To avoid stalling the pipeline, the CPU uses **branch prediction**.

---

## Speculative execution

The CPU predicts which path will be taken and begins executing instructions along that path.

If the prediction is correct, execution continues normally.

If the prediction is wrong, the pipeline must be **flushed**, and execution restarts.

---

### Branch prediction visualization

```mermaid
flowchart TD
    A[Branch Instruction] --> B{Prediction}
    B -->|Path A| C[Execute A]
    B -->|Path B| D[Execute B]
```

Pipeline flush penalties typically cost **10–20 cycles**.

Modern predictors achieve **over 95% accuracy** for typical workloads.

---

## 7. Memory Latency and CPU Stalls

Even with high IPC, CPUs frequently stall waiting for data from memory.

Consider a processor running at **4 GHz**.

Cycle time:

```
0.25 ns
```

Typical RAM latency:

```
~60 ns
```

Equivalent cycles:

[
60 / 0.25 = 240 \text{ cycles}
]

During this time the CPU may be unable to execute dependent instructions.

---

### Memory latency comparison

| Memory Level | Latency        |
| ------------ | -------------- |
| L1 Cache     | 3–5 cycles     |
| L2 Cache     | 10–15 cycles   |
| L3 Cache     | 30–50 cycles   |
| RAM          | 200–400 cycles |

This is why **cache locality is often more important than clock speed**.

---

### Memory latency visualization

```mermaid
flowchart LR
    CPU --> L1
    L1 --> L2
    L2 --> L3
    L3 --> RAM
```

Each step away from the CPU increases latency.

---

## 8. Measuring CPU Throughput

Floating-point performance is often measured using **FLOPS (floating-point operations per second)**.

Matrix multiplication is commonly used as a benchmark because it performs a large number of arithmetic operations.

---

### Example: estimating GFLOPS

```python
import numpy as np
import time

def estimate_gflops():
    n = 2048
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)

    flops = 2 * n**3
    start = time.perf_counter()
    C = A @ B
    elapsed = time.perf_counter() - start

    gflops = (flops / elapsed) / 1e9
    print(f"{gflops:.1f} GFLOPS")

estimate_gflops()
```

Optimized BLAS libraries can reach **100–500 GFLOPS** on modern CPUs.

---

## 9. Measuring Python-Level Overhead

The cost of Python operations can be measured using `timeit`.

```python
import timeit

result = timeit.timeit(
    'sum(range(1000))',
    number=10000
)

print(result)
```

This measurement includes:

* interpreter overhead
* object allocation
* dynamic type checks

These factors explain why Python arithmetic is slower than compiled code.

---

## 10. Practical Performance Insights

Several factors determine real-world performance.

---

## Clock speed

Higher frequency increases potential throughput.

However, it is not the dominant factor.

---

## IPC

Modern CPUs improve IPC using:

* pipelining
* superscalar execution
* out-of-order scheduling
* branch prediction

---

## Memory behavior

Many programs are limited by **memory latency and bandwidth**, not computation.

Efficient programs:

* maximize cache locality
* minimize memory traffic
* reuse data when possible

---

## 11. Worked Examples

### Example 1

Compute cycle time of a 3 GHz processor.

[
1 / 3,000,000,000 = 0.33 \text{ ns}
]

---

### Example 2

If IPC = 4 and clock speed = 3 GHz:

```
Throughput = 12 billion instructions/sec
```

---

### Example 3

Why can RAM latency dominate performance?

Because a single memory access may cost **hundreds of CPU cycles**.

---

## 12. Exercises

**Exercise 1.**
CPU A runs at 4 GHz with an average IPC of 2. CPU B runs at 3 GHz with an average IPC of 4.

(a) How many instructions per second does each CPU complete?
(b) Which CPU has higher instruction throughput despite lower clock speed?
(c) Why is clock speed alone a misleading measure of performance?

??? success "Solution to Exercise 1"
    **(a)** Throughput = Clock speed * IPC.

    - CPU A: 4 GHz * 2 IPC = 8 billion instructions/second
    - CPU B: 3 GHz * 4 IPC = 12 billion instructions/second

    **(b)** CPU B has 50% higher throughput despite 25% lower clock speed, because its higher IPC more than compensates.

    **(c)** Clock speed only measures how fast the clock ticks, not how much useful work is done per tick. A CPU with high IPC (through better pipelining, wider execution units, better branch prediction, and smarter caching) can outperform a higher-clocked CPU with lower IPC. This is why modern CPUs focus on improving IPC rather than increasing clock speed (which is limited by power consumption and heat).

---

**Exercise 2.**
A 5-stage pipeline (Fetch, Decode, Execute, Memory, Writeback) is processing a stream of instructions. After the pipeline fills, one instruction completes per cycle. However, a branch misprediction flushes the pipeline, wasting cycles.

(a) If a program has 1000 instructions and 10% are branches with 80% prediction accuracy, how many pipeline flushes occur?
(b) Each flush wastes 4 cycles (to refill the pipeline). How many extra cycles does this add?
(c) What is the effective IPC if the ideal IPC is 1.0?

??? success "Solution to Exercise 2"
    **(a)** Branches: 1000 * 10% = 100 branches. Mispredictions: 100 * (1 - 0.80) = **20 pipeline flushes**.

    **(b)** Extra cycles: 20 * 4 = **80 extra cycles**.

    **(c)** Without mispredictions: 1000 cycles for 1000 instructions. With mispredictions: 1000 + 80 = 1080 cycles. Effective IPC = 1000 / 1080 = **~0.93**. Branch mispredictions reduced performance by about 7%.

    In real programs with more branches and deeper pipelines (15-20 stages in modern CPUs), misprediction penalties are much more severe. This is why branch prediction accuracy of 95%+ is critical for modern CPUs.

---

**Exercise 3.**
A program runs 1 billion instructions. 30% are memory accesses, and 70% of memory accesses hit the L1 cache (4 cycles). The remaining 30% miss L1 and go to RAM (200 cycles). Non-memory instructions take 1 cycle each.

(a) Calculate the total cycles for non-memory instructions.
(b) Calculate the total cycles for memory instructions (L1 hits + L1 misses).
(c) What is the average CPI (cycles per instruction)?
(d) On a 3 GHz CPU, how long does the program take to run?

??? success "Solution to Exercise 3"
    **(a)** Non-memory instructions: 1,000,000,000 * 0.70 = 700,000,000 instructions * 1 cycle = **700,000,000 cycles**.

    **(b)** Memory instructions: 300,000,000 total.

    - L1 hits: 300,000,000 * 0.70 = 210,000,000 * 4 cycles = 840,000,000 cycles
    - L1 misses: 300,000,000 * 0.30 = 90,000,000 * 200 cycles = 18,000,000,000 cycles
    - Total memory cycles: 840,000,000 + 18,000,000,000 = **18,840,000,000 cycles**

    **(c)** Total cycles: 700,000,000 + 18,840,000,000 = 19,540,000,000. Average CPI = 19,540,000,000 / 1,000,000,000 = **~19.5 cycles per instruction**.

    **(d)** Runtime = 19,540,000,000 / 3,000,000,000 = **~6.5 seconds**.

    The L1 misses (only 9% of instructions) account for 92% of total cycles. This dramatically illustrates why memory access patterns dominate performance -- optimizing cache behavior is often more impactful than optimizing computation.

## 13. Summary

| Concept                | Description                       |
| ---------------------- | --------------------------------- |
| Clock Speed            | number of cycles per second       |
| IPC                    | instructions completed per cycle  |
| Throughput             | clock speed × IPC                 |
| Pipelining             | overlapping instruction stages    |
| Superscalar            | multiple instructions per cycle   |
| Out-of-order execution | dynamic instruction reordering    |
| Branch prediction      | speculative execution of branches |
| Memory latency         | major cause of CPU stalls         |

Modern CPU performance results from the interaction of **clock frequency, instruction throughput, and memory behavior**.

In practice, programs often run slowly not because CPUs are slow, but because **memory latency and inefficient instruction scheduling limit performance**.

## Exercises

**Exercise 1.** If a CPU has a clock speed of 3 GHz, how many clock cycles occur per second? How many nanoseconds does one cycle take.

??? success "Solution to Exercise 1"
    A 3 GHz clock produces 3 billion cycles per second. One cycle takes 1/3,000,000,000 seconds = approximately 0.33 nanoseconds.

---

**Exercise 2.** Explain why a higher clock speed does not always mean faster program execution.

??? success "Solution to Exercise 2"
    Performance depends on instructions per cycle (IPC) as well as clock speed. A CPU with lower clock speed but higher IPC (due to better architecture, wider execution units, or better branch prediction) can outperform a higher-clocked CPU. Memory latency, cache behavior, and instruction-level parallelism all affect real-world performance.

