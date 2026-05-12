# Why Python is Slow

!!! tip "Mental Model"
    In a tight Python loop, less than 1% of CPU time goes to actual arithmetic -- the rest is spent on type checking, object creation, dictionary lookups, and reference counting. Python is not slow because your CPU is slow; it is slow because it does enormous bookkeeping for every operation. The fix is to push hot loops into compiled code (NumPy, C extensions) and let Python orchestrate.

## The Performance Gap

Python is often 10-100x slower than C for computational tasks. Understanding why helps you write faster Python code.

```
Performance Comparison (sum of 10 million integers):

C:        ████                               0.01s
Java:     ████████                           0.02s
JavaScript: ████████████                     0.03s
Python:   ████████████████████████████████████████  0.85s

Python is ~85x slower than C for this task!
```

## The Five Reasons Python is Slow

### 1. Dynamic Typing

Python checks types at runtime, not compile time:

```python
# Python doesn't know what 'x' is until runtime
def add(x, y):
    return x + y

add(1, 2)        # int + int
add("a", "b")    # str + str
add([1], [2])    # list + list

# Each call requires:
# 1. Check type of x
# 2. Check type of y
# 3. Find appropriate __add__ method
# 4. Call it
```

**C equivalent:**
```c
// Type known at compile time - no runtime checks
int add(int x, int y) {
    return x + y;  // Just one CPU instruction
}
```

### 2. Everything is an Object

In Python, even simple integers are full objects:

```python
import sys

x = 42
print(sys.getsizeof(x))  # 28 bytes!

# A Python int contains:
# - Reference count (8 bytes)
# - Type pointer (8 bytes)
# - Value size (8 bytes)
# - Actual value (variable)
```

```
Python int object (28 bytes):
┌────────────────────────────────┐
│  Reference Count    (8 bytes) │
├────────────────────────────────┤
│  Type Pointer       (8 bytes) │  → points to int type
├────────────────────────────────┤
│  Object Size        (8 bytes) │
├────────────────────────────────┤
│  Actual Value       (4 bytes) │  ← the number 42
└────────────────────────────────┘

C int (4 bytes):
┌────────────────────────────────┐
│  Actual Value       (4 bytes) │  ← the number 42
└────────────────────────────────┘

7x more memory, plus indirection overhead!
```

### 3. Interpreted Execution

Python bytecode runs on a virtual machine:

```python
import dis

def simple_loop():
    total = 0
    for i in range(1000):
        total += i
    return total

dis.dis(simple_loop)
```

Output:
```
  2           0 LOAD_CONST               1 (0)
              2 STORE_FAST               0 (total)

  3           4 LOAD_GLOBAL              0 (range)
              6 LOAD_CONST               2 (1000)
              8 CALL_FUNCTION            1
             10 GET_ITER
        >>   12 FOR_ITER                 6 (to 26)
             14 STORE_FAST               1 (i)

  4          16 LOAD_FAST                0 (total)
             18 LOAD_FAST                1 (i)
             20 INPLACE_ADD
             22 STORE_FAST               0 (total)
             24 JUMP_ABSOLUTE            6 (to 12)

  5     >>   26 LOAD_FAST                0 (total)
             28 RETURN_VALUE
```

Each bytecode instruction involves:

1. Fetch instruction
2. Decode instruction
3. Dispatch to handler
4. Execute handler
5. Repeat

### 4. Memory Indirection

Python lists store references, not values:

```
Python List of integers:
┌─────────────────┐
│   List Object   │
│  ┌───────────┐  │
│  │  ref[0] ──┼──┼──▶ [PyInt: 1] (somewhere in heap)
│  │  ref[1] ──┼──┼──▶ [PyInt: 2] (somewhere else)
│  │  ref[2] ──┼──┼──▶ [PyInt: 3] (somewhere else)
│  └───────────┘  │
└─────────────────┘

Each access:
  1. Load list pointer
  2. Load reference from list
  3. Follow reference to object
  4. Check object type
  5. Extract value from object

C Array:
┌─────────────────┐
│  1  │  2  │  3  │   Contiguous in memory
└─────────────────┘

Each access:
  1. Calculate offset
  2. Load value
```

### 5. Global Interpreter Lock (GIL)

Python can't truly parallelize CPU-bound threads:

```python
import threading
import time

counter = 0

def increment():
    global counter
    for _ in range(1_000_000):
        counter += 1

# Two threads
t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)

start = time.perf_counter()
t1.start()
t2.start()
t1.join()
t2.join()
elapsed = time.perf_counter() - start

print(f"Time: {elapsed:.2f}s")
print(f"Counter: {counter}")  # Likely not 2,000,000!

# Two threads are NOT faster than one
# because GIL prevents parallel execution
```

## Quantifying the Overhead

```python
import time
import numpy as np

def benchmark_overhead():
    n = 10_000_000
    
    # Pure Python loop
    start = time.perf_counter()
    total = 0
    for i in range(n):
        total += i
    python_time = time.perf_counter() - start
    
    # Python with list
    data = list(range(n))
    start = time.perf_counter()
    total = sum(data)
    builtin_time = time.perf_counter() - start
    
    # NumPy (C code)
    arr = np.arange(n)
    start = time.perf_counter()
    total = np.sum(arr)
    numpy_time = time.perf_counter() - start
    
    print(f"Python loop:     {python_time:.3f}s (1.0x)")
    print(f"Python sum():    {builtin_time:.3f}s ({python_time/builtin_time:.1f}x)")
    print(f"NumPy sum():     {numpy_time:.3f}s ({python_time/numpy_time:.1f}x)")

benchmark_overhead()
```

Typical output:
```
Python loop:     0.850s (1.0x)
Python sum():    0.120s (7.1x)
NumPy sum():     0.008s (106.3x)
```

## Where Does the Time Go?

```
Time breakdown for Python loop (x += 1):

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Bytecode dispatch:     ████████████████  30%              │
│  Type checking:         ████████████      25%              │
│  Object creation:       ██████████        20%              │
│  Dictionary lookups:    ██████            15%              │
│  Reference counting:    ████              10%              │
│  Actual computation:    █                 <1%              │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Most time is overhead, not actual computation!
```

## When Python is "Fast Enough"

Python's slowness often doesn't matter:

```python
# I/O bound - Python speed doesn't matter
response = requests.get(url)    # Network is bottleneck
data = f.read()                 # Disk is bottleneck

# Human interaction - Python speed doesn't matter
user_input = input("Enter: ")   # Human is bottleneck

# Calling fast libraries - Python is just orchestrating
result = np.dot(huge_matrix_a, huge_matrix_b)  # NumPy does work

# One-time scripts - Development time matters more
df = pd.read_csv('data.csv').groupby('x').mean()
```

## Strategies to Speed Up Python

### 1. Use Built-in Functions

```python
# Slow
total = 0
for x in data:
    total += x

# Fast (built-in is C)
total = sum(data)
```

### 2. Use NumPy/Pandas

```python
# Slow
result = [x * 2 for x in data]

# Fast
result = np.array(data) * 2
```

### 3. Use List Comprehensions

```python
# Slower
result = []
for x in data:
    result.append(x * 2)

# Faster (optimized bytecode)
result = [x * 2 for x in data]
```

### 4. Avoid Global Variables

```python
# Slower (global lookup each iteration)
multiplier = 2
def slow():
    return [x * multiplier for x in range(1000000)]

# Faster (local lookup)
def fast():
    mult = 2  # Local variable
    return [x * mult for x in range(1000000)]
```

### 5. Use Appropriate Data Structures

```python
# Slow (O(n) lookup)
if item in large_list:
    pass

# Fast (O(1) lookup)
if item in large_set:
    pass
```

## Summary

| Overhead Source | Impact | Mitigation |
|----------------|--------|------------|
| **Dynamic typing** | Type checks every operation | Use NumPy (typed arrays) |
| **Object overhead** | Memory and indirection | Use NumPy (raw data) |
| **Interpretation** | Bytecode dispatch | Use compiled extensions |
| **Memory layout** | Cache misses | Use contiguous arrays |
| **GIL** | No CPU parallelism | Use multiprocessing |

Key insight:

Python is slow for **tight computational loops**. The solution isn't to avoid Python—it's to move the hot loops into compiled code (NumPy, Cython, C extensions) while keeping Python for orchestration and glue code.


---

## Exercises

**Exercise 1.** List three reasons why Python is slower than compiled languages like C or Rust for numerical computation.

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

**Exercise 2.** Explain what dynamic typing costs at runtime. How does it affect performance compared to static typing?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the hardware-software interaction and how it affects Python performance.

---

**Exercise 3.** Write Python code that benchmarks a pure Python loop versus an equivalent NumPy operation, and calculate the speedup factor.

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

**Exercise 4.** Explain the concept of 'boxing' and 'unboxing' in Python. How does it contribute to Python's overhead for numerical operations?

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
