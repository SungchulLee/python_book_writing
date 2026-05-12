# ProcessPoolExecutor

`ProcessPoolExecutor` manages a pool of worker processes for parallel execution. Best suited for **CPU-bound tasks** that need to bypass the GIL.

!!! tip "Mental Model"
    A ProcessPoolExecutor is a team of independent workers, each with their own Python interpreter and GIL. Because they run in separate processes, they achieve true CPU parallelism -- but communication between them requires serialization (pickling). Use it when the computation per task is heavy enough to justify the overhead of copying data across process boundaries.

---

## Basic Usage

```python
from concurrent.futures import ProcessPoolExecutor
import time

def compute_heavy(n):
    """CPU-intensive computation."""
    return sum(i * i for i in range(n))

if __name__ == "__main__":
    numbers = [10_000_000, 20_000_000, 30_000_000, 40_000_000]
    
    # Sequential
    start = time.perf_counter()
    results = [compute_heavy(n) for n in numbers]
    print(f"Sequential: {time.perf_counter() - start:.2f}s")
    
    # Parallel with processes
    start = time.perf_counter()
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(compute_heavy, numbers))
    print(f"Parallel: {time.perf_counter() - start:.2f}s")
```

**Important**: Always use `if __name__ == "__main__":` guard with `ProcessPoolExecutor`.

---

## Creating ProcessPoolExecutor

```python
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

# Default workers: os.cpu_count()
executor = ProcessPoolExecutor()

# Explicit worker count
executor = ProcessPoolExecutor(max_workers=4)

# With specific start method
executor = ProcessPoolExecutor(
    max_workers=4,
    mp_context=mp.get_context("spawn")
)

# With initializer
executor = ProcessPoolExecutor(
    max_workers=4,
    initializer=setup_function,
    initargs=(arg1, arg2)
)

# Restart workers periodically (Python 3.11+)
executor = ProcessPoolExecutor(
    max_workers=4,
    max_tasks_per_child=100  # Restart after 100 tasks
)
```

---

## Using map()

```python
from concurrent.futures import ProcessPoolExecutor

def square(x):
    return x ** 2

if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(square, range(10)))
        print(results)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

### map() with Chunksize

For large datasets, chunksize reduces IPC overhead:

```python
from concurrent.futures import ProcessPoolExecutor

def process(x):
    return x ** 2

if __name__ == "__main__":
    data = list(range(100_000))
    
    with ProcessPoolExecutor() as executor:
        # Without chunksize: many small transfers
        results1 = list(executor.map(process, data))
        
        # With chunksize: fewer, larger transfers
        results2 = list(executor.map(process, data, chunksize=1000))
```

### map() with Multiple Arguments

```python
from concurrent.futures import ProcessPoolExecutor

def power(base, exp):
    return base ** exp

if __name__ == "__main__":
    bases = [2, 3, 4, 5]
    exps = [10, 10, 10, 10]
    
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(power, bases, exps))
        print(results)  # [1024, 59049, 1048576, 9765625]
```

---

## Using submit()

```python
from concurrent.futures import ProcessPoolExecutor

def compute(x):
    return x ** 2

if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        # Submit individual tasks
        future1 = executor.submit(compute, 10)
        future2 = executor.submit(compute, 20)
        future3 = executor.submit(compute, 30)
        
        print(future1.result())  # 100
        print(future2.result())  # 400
        print(future3.result())  # 900
```

---

## Processing Results as They Complete

```python
from concurrent.futures import ProcessPoolExecutor, as_completed
import random

def variable_computation(task_id):
    """Computation with variable duration."""
    iterations = random.randint(1_000_000, 10_000_000)
    result = sum(i for i in range(iterations))
    return (task_id, iterations, result)

if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(variable_computation, i): i for i in range(10)}
        
        for future in as_completed(futures):
            task_id = futures[future]
            try:
                tid, iters, result = future.result()
                print(f"Task {tid}: {iters:,} iterations")
            except Exception as e:
                print(f"Task {task_id} failed: {e}")
```

---

## Initializer for Worker Setup

```python
from concurrent.futures import ProcessPoolExecutor
import os

# Global variable in each worker
model = None

def init_worker(model_path):
    """Load model once per worker process."""
    global model
    model = load_model(model_path)
    print(f"Worker {os.getpid()}: Model loaded")

def predict(data):
    """Use pre-loaded model."""
    return model.predict(data)

if __name__ == "__main__":
    with ProcessPoolExecutor(
        max_workers=4,
        initializer=init_worker,
        initargs=("model.pkl",)
    ) as executor:
        predictions = list(executor.map(predict, test_data))
```

---

## Practical Examples

### Parallel Number Crunching

```python
from concurrent.futures import ProcessPoolExecutor
import math

def is_prime(n):
    """Check if n is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def count_primes(start, end):
    """Count primes in range."""
    return sum(1 for n in range(start, end) if is_prime(n))

if __name__ == "__main__":
    # Split range into chunks
    ranges = [
        (0, 250_000),
        (250_000, 500_000),
        (500_000, 750_000),
        (750_000, 1_000_000),
    ]
    
    with ProcessPoolExecutor() as executor:
        counts = list(executor.starmap(count_primes, ranges))
    
    print(f"Total primes: {sum(counts)}")
```

### Parallel Image Processing

```python
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
# from PIL import Image  # Uncomment for real usage

def process_image(image_path):
    """Resize and convert image."""
    # img = Image.open(image_path)
    # img = img.resize((256, 256))
    # output_path = image_path.with_stem(image_path.stem + "_thumb")
    # img.save(output_path)
    return f"Processed {image_path}"

if __name__ == "__main__":
    images = list(Path("images").glob("*.jpg"))
    
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_image, images))
    
    print(f"Processed {len(results)} images")
```

### Parallel Data Processing

```python
from concurrent.futures import ProcessPoolExecutor
import pandas as pd

def process_chunk(chunk_data):
    """Process a chunk of data."""
    # Heavy computation on chunk
    result = chunk_data.apply(expensive_transformation)
    return result.sum()

if __name__ == "__main__":
    # Load and split data
    df = pd.read_csv("large_data.csv")
    chunks = np.array_split(df, 8)  # Split into 8 chunks
    
    with ProcessPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(process_chunk, chunks))
    
    total = sum(results)
```

### Monte Carlo Simulation

```python
from concurrent.futures import ProcessPoolExecutor
import random

def monte_carlo_pi(num_samples):
    """Estimate pi using Monte Carlo method."""
    inside = 0
    for _ in range(num_samples):
        x, y = random.random(), random.random()
        if x*x + y*y <= 1:
            inside += 1
    return inside

if __name__ == "__main__":
    num_workers = 8
    samples_per_worker = 10_000_000
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(
            monte_carlo_pi,
            [samples_per_worker] * num_workers
        ))
    
    total_inside = sum(results)
    total_samples = samples_per_worker * num_workers
    pi_estimate = 4 * total_inside / total_samples
    print(f"Pi estimate: {pi_estimate}")
```

---

## Serialization Requirements

Objects passed to/from processes must be **picklable**:

```python
from concurrent.futures import ProcessPoolExecutor

# Works: regular functions, basic types
def square(x):
    return x ** 2

# Fails: lambda functions
# executor.map(lambda x: x**2, data)  # PicklingError!

# Fails: local classes
class Local:
    pass
# executor.submit(func, Local())  # PicklingError!

# Works: module-level classes
class ModuleLevel:
    pass

if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(square, [1, 2, 3]))
```

### Common Pickling Issues

```python
# Problem: Lambda functions can't be pickled
bad = lambda x: x ** 2

# Solution: Use regular function
def good(x):
    return x ** 2

# Problem: Instance methods need care
class Processor:
    def process(self, x):
        return x ** 2

# Solution: Use module-level function or staticmethod
def process_item(x):
    return x ** 2
```

---

## Error Handling

```python
from concurrent.futures import ProcessPoolExecutor, as_completed

def risky_task(x):
    if x == 5:
        raise ValueError(f"Cannot process {x}")
    return x ** 2

if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(risky_task, i): i for i in range(10)}
        
        for future in as_completed(futures):
            task_id = futures[future]
            try:
                result = future.result()
                print(f"Task {task_id}: {result}")
            except Exception as e:
                print(f"Task {task_id} failed: {e}")
```

---

## Performance Considerations

### Worker Count

```python
import os

# CPU-bound: match CPU cores
executor = ProcessPoolExecutor(max_workers=os.cpu_count())

# Leave some CPUs free
executor = ProcessPoolExecutor(max_workers=max(1, os.cpu_count() - 2))
```

### Chunksize for map()

```python
# Small data: default is fine
executor.map(func, small_list)

# Large data: set chunksize
# Rule of thumb: len(data) // (workers * 4)
executor.map(func, large_list, chunksize=1000)
```

### Startup Overhead

Process creation is slow. Avoid for:

- Very short tasks
- Small datasets
- Tasks that run once

```python
# Bad: Overhead dominates
with ProcessPoolExecutor() as executor:
    result = executor.submit(lambda: 1 + 1).result()

# Good: Amortize overhead with batch processing
with ProcessPoolExecutor() as executor:
    results = list(executor.map(compute, large_dataset))
```

---

## Comparison with ThreadPoolExecutor

| Aspect | ProcessPoolExecutor | ThreadPoolExecutor |
|--------|--------------------|--------------------|
| **Best for** | CPU-bound | I/O-bound |
| **GIL** | Bypassed | Affected |
| **Memory** | Isolated (copies) | Shared |
| **Overhead** | Higher | Lower |
| **Serialization** | Required (pickle) | Not required |
| **Startup** | Slower | Faster |
| **Max workers** | ~CPU count | 10-50+ |

---

## Key Takeaways

- Use `ProcessPoolExecutor` for **CPU-bound tasks**
- Always use `if __name__ == "__main__":` guard
- Match worker count to CPU cores
- Use `chunksize` for large datasets to reduce overhead
- Objects must be **picklable** (no lambdas, local classes)
- Use `initializer` for expensive per-worker setup
- Process overhead is higher than threads — batch work
- Use context manager for automatic cleanup
- For I/O-bound tasks, use `ThreadPoolExecutor` instead

---

## Exercises

**Exercise 1.**
Use `ProcessPoolExecutor.map()` with `chunksize=100` to compute the sum of cubes for each number in `range(10_000)`. Compare the elapsed time with `chunksize=1` and `chunksize=100`. Print both times and the speedup.

??? success "Solution to Exercise 1"
        ```python
        import time
        from concurrent.futures import ProcessPoolExecutor

        def sum_cubes(n):
            return sum(i ** 3 for i in range(n))

        if __name__ == "__main__":
            data = list(range(10_000))

            for cs in [1, 100]:
                start = time.perf_counter()
                with ProcessPoolExecutor() as ex:
                    list(ex.map(sum_cubes, data, chunksize=cs))
                elapsed = time.perf_counter() - start
                print(f"chunksize={cs:3d}: {elapsed:.2f}s")
        ```

---

**Exercise 2.**
Write a Monte Carlo estimation of pi using `ProcessPoolExecutor`. Each of 8 workers generates 1,000,000 random `(x, y)` points and counts how many fall inside the unit circle. Combine results to estimate pi and print the estimate with the elapsed time.

??? success "Solution to Exercise 2"
        ```python
        import time
        import random
        from concurrent.futures import ProcessPoolExecutor

        def monte_carlo(n_samples):
            inside = 0
            for _ in range(n_samples):
                x, y = random.random(), random.random()
                if x * x + y * y <= 1:
                    inside += 1
            return inside

        if __name__ == "__main__":
            workers = 8
            samples = 1_000_000

            start = time.perf_counter()
            with ProcessPoolExecutor(max_workers=workers) as ex:
                counts = list(ex.map(monte_carlo, [samples] * workers))
            elapsed = time.perf_counter() - start

            pi = 4 * sum(counts) / (workers * samples)
            print(f"Pi estimate: {pi:.6f} (elapsed {elapsed:.2f}s)")
        ```

---

**Exercise 3.**
Use `ProcessPoolExecutor` with `submit()` and `as_completed()` to factorize 10 large numbers. Map each future back to its input using a dictionary. Print results in completion order, showing the input number and its smallest factor (or "prime" if none found below its square root).

??? success "Solution to Exercise 3"
        ```python
        import math
        from concurrent.futures import ProcessPoolExecutor, as_completed

        def smallest_factor(n):
            if n < 2:
                return (n, None)
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    return (n, i)
            return (n, None)

        if __name__ == "__main__":
            numbers = [
                104729, 1000003, 999983, 7919 * 7919,
                1299827, 15485863, 49979687, 67867979,
                104395303, 982451653,
            ]

            with ProcessPoolExecutor() as ex:
                futs = {ex.submit(smallest_factor, n): n for n in numbers}
                for f in as_completed(futs):
                    n, factor = f.result()
                    if factor:
                        print(f"{n}: smallest factor = {factor}")
                    else:
                        print(f"{n}: prime")
        ```
