# Error Handling in Concurrent Code

Proper error handling is critical in concurrent programs where exceptions can occur in multiple threads or processes simultaneously.

!!! tip "Mental Model"
    In sequential code an exception stops everything immediately. In concurrent code, exceptions happen in worker threads or processes -- they are silently captured inside Futures and only re-raised when you call `result()`. If you never check, you never know something failed. Always retrieve results or attach error callbacks; otherwise failures vanish silently and corrupt your output.

---

## Challenges in Concurrent Error Handling

1. **Exceptions don't propagate automatically** across threads/processes
2. **Multiple failures** can occur simultaneously
3. **Partial completion** — some tasks succeed, others fail
4. **Resource cleanup** must happen even when errors occur
5. **Deadlocks** can occur if error handling isn't careful

---

## Error Handling with submit()

### Basic Exception Handling

```python
from concurrent.futures import ThreadPoolExecutor

def risky_task(x):
    if x == 5:
        raise ValueError(f"Cannot process {x}")
    return x ** 2

with ThreadPoolExecutor() as executor:
    future = executor.submit(risky_task, 5)
    
    try:
        result = future.result()  # Exception raised here
    except ValueError as e:
        print(f"Task failed: {e}")
```

### Check Exception Before Result

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor() as executor:
    future = executor.submit(risky_task, 5)
    
    # Wait without raising
    future.exception()  # Blocks until complete
    
    # Check if exception occurred
    exc = future.exception()
    if exc is not None:
        print(f"Exception: {exc}")
    else:
        print(f"Result: {future.result()}")
```

---

## Error Handling with map()

### First Exception Stops Iteration

```python
from concurrent.futures import ThreadPoolExecutor

def process(x):
    if x == 3:
        raise ValueError(f"Bad value: {x}")
    return x ** 2

with ThreadPoolExecutor() as executor:
    try:
        # Raises on first exception encountered in order
        results = list(executor.map(process, range(10)))
    except ValueError as e:
        print(f"Error: {e}")
        # But some tasks may have completed or are still running!
```

### Wrap Function for Safe map()

```python
from concurrent.futures import ThreadPoolExecutor

def safe_process(x):
    """Wrap function to catch exceptions."""
    try:
        if x == 3:
            raise ValueError(f"Bad value: {x}")
        return ("success", x ** 2)
    except Exception as e:
        return ("error", str(e))

with ThreadPoolExecutor() as executor:
    results = list(executor.map(safe_process, range(10)))
    
    successes = [r[1] for r in results if r[0] == "success"]
    errors = [r[1] for r in results if r[0] == "error"]
    
    print(f"Successes: {len(successes)}")
    print(f"Errors: {errors}")
```

---

## Error Handling with as_completed()

### Handle Each Future Individually

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def process(x):
    if x % 3 == 0:
        raise ValueError(f"Divisible by 3: {x}")
    return x ** 2

with ThreadPoolExecutor() as executor:
    futures = {executor.submit(process, x): x for x in range(10)}
    
    results = {}
    errors = {}
    
    for future in as_completed(futures):
        x = futures[future]
        try:
            results[x] = future.result()
        except Exception as e:
            errors[x] = str(e)
    
    print(f"Results: {results}")
    print(f"Errors: {errors}")
```

### Continue on Errors

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_data(url):
    import requests
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()

urls = [
    "https://api.example.com/data/1",
    "https://api.example.com/data/2",
    "https://invalid-url.com/fail",  # Will fail
    "https://api.example.com/data/3",
]

with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_url = {executor.submit(fetch_data, url): url for url in urls}
    
    successful_data = []
    failed_urls = []
    
    for future in as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
            successful_data.append(data)
        except Exception as e:
            failed_urls.append((url, str(e)))
            # Continue processing other results
    
    print(f"Fetched: {len(successful_data)}")
    print(f"Failed: {failed_urls}")
```

---

## Callbacks for Error Handling

### Error Callback with apply_async

```python
from multiprocessing import Pool

def task(x):
    if x < 0:
        raise ValueError("Negative!")
    return x ** 2

def on_success(result):
    print(f"Success: {result}")

def on_error(error):
    print(f"Error: {error}")

if __name__ == "__main__":
    with Pool() as pool:
        # With callbacks
        pool.apply_async(task, args=(5,), 
                        callback=on_success, 
                        error_callback=on_error)
        
        pool.apply_async(task, args=(-1,), 
                        callback=on_success, 
                        error_callback=on_error)
        
        pool.close()
        pool.join()
```

### Done Callback with Future

```python
from concurrent.futures import ThreadPoolExecutor

def task(x):
    if x < 0:
        raise ValueError("Negative!")
    return x ** 2

def handle_completion(future):
    try:
        result = future.result()
        print(f"Success: {result}")
    except Exception as e:
        print(f"Failed: {e}")

with ThreadPoolExecutor() as executor:
    for x in [5, -1, 10, -5]:
        future = executor.submit(task, x)
        future.add_done_callback(handle_completion)
```

---

## Timeout Handling

### Single Task Timeout

```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import time

def slow_task():
    time.sleep(10)
    return "done"

with ThreadPoolExecutor() as executor:
    future = executor.submit(slow_task)
    
    try:
        result = future.result(timeout=2)
    except TimeoutError:
        print("Task timed out!")
        # Note: Task may still be running!
        # cancel() only works if task hasn't started
        future.cancel()
```

### Batch Timeout with as_completed

```python
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

def task(x):
    import time
    time.sleep(x)
    return x

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(task, i) for i in [1, 5, 2, 8, 1]]
    
    results = []
    timed_out = []
    
    try:
        for future in as_completed(futures, timeout=3):
            results.append(future.result())
    except TimeoutError:
        # Some futures didn't complete in time
        for future in futures:
            if not future.done():
                timed_out.append(future)
                future.cancel()
    
    print(f"Completed: {results}")
    print(f"Timed out: {len(timed_out)}")
```

---

## Exception Chaining

### Preserve Original Exception

```python
from concurrent.futures import ThreadPoolExecutor

def worker(x):
    raise ValueError("Original error")

def safe_worker(x):
    try:
        return worker(x)
    except Exception as e:
        raise RuntimeError(f"Worker {x} failed") from e

with ThreadPoolExecutor() as executor:
    future = executor.submit(safe_worker, 5)
    
    try:
        future.result()
    except RuntimeError as e:
        print(f"Error: {e}")
        print(f"Caused by: {e.__cause__}")
```

---

## Logging Errors

### Centralized Error Logging

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process(x):
    if x % 5 == 0:
        raise ValueError(f"Bad value: {x}")
    return x ** 2

def process_with_logging(x):
    try:
        result = process(x)
        logger.info(f"Task {x}: Success")
        return result
    except Exception as e:
        logger.error(f"Task {x}: Failed - {e}")
        raise

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_with_logging, x) for x in range(20)]
    
    for future in as_completed(futures):
        try:
            future.result()
        except Exception:
            pass  # Already logged
```

---

## Cleanup on Error

### Using try/finally

```python
from concurrent.futures import ThreadPoolExecutor

def task_with_cleanup(resource):
    try:
        # Do work
        result = process(resource)
        return result
    finally:
        # Always cleanup
        resource.close()

with ThreadPoolExecutor() as executor:
    resources = [open_resource(i) for i in range(10)]
    futures = [executor.submit(task_with_cleanup, r) for r in resources]
    
    # All resources will be cleaned up
    results = [f.result() for f in futures]
```

### Context Manager Pattern

```python
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    resource = acquire_resource(name)
    try:
        yield resource
    finally:
        release_resource(resource)

def task(name):
    with managed_resource(name) as resource:
        return process(resource)

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(task, f"resource_{i}") for i in range(10)]
    results = [f.result() for f in futures]
```

---

## Aggregating Multiple Errors

### Collect All Errors

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

class MultipleErrors(Exception):
    def __init__(self, errors):
        self.errors = errors
        super().__init__(f"{len(errors)} errors occurred")

def process_all(items, func, raise_on_error=True):
    """Process all items, optionally raising aggregated errors."""
    with ThreadPoolExecutor() as executor:
        future_to_item = {executor.submit(func, item): item for item in items}
        
        results = []
        errors = []
        
        for future in as_completed(future_to_item):
            item = future_to_item[future]
            try:
                results.append((item, future.result()))
            except Exception as e:
                errors.append((item, e))
        
        if errors and raise_on_error:
            raise MultipleErrors(errors)
        
        return results, errors

# Usage
try:
    results, errors = process_all(items, risky_func)
except MultipleErrors as e:
    print(f"Failed items: {len(e.errors)}")
    for item, error in e.errors:
        print(f"  {item}: {error}")
```

---

## Best Practices

### 1. Always Handle Exceptions

```python
# Bad: Exceptions silently ignored
for future in futures:
    future.result()  # May raise!

# Good: Handle each exception
for future in futures:
    try:
        result = future.result()
    except Exception as e:
        handle_error(e)
```

### 2. Use Specific Exception Types

```python
# Bad: Catch everything
except Exception:
    pass

# Good: Catch specific exceptions
except (ConnectionError, TimeoutError) as e:
    retry_task(e)
except ValueError as e:
    log_invalid_input(e)
```

### 3. Don't Ignore Partial Results

```python
# Bad: All or nothing
try:
    results = list(executor.map(func, items))
except Exception:
    results = []

# Good: Collect partial results
results = []
errors = []
for future in as_completed(futures):
    try:
        results.append(future.result())
    except Exception as e:
        errors.append(e)
```

### 4. Set Timeouts

```python
# Bad: Wait forever
result = future.result()

# Good: Set reasonable timeout
result = future.result(timeout=30)
```

---

## Key Takeaways

- Exceptions in workers **don't propagate automatically**
- Use `future.result()` to get or raise exceptions
- `as_completed()` allows handling each task's error individually
- Wrap functions to capture exceptions without stopping `map()`
- Use callbacks for async error handling
- Always set timeouts for production code
- Log errors for debugging
- Ensure cleanup happens even on errors
- Collect partial results when some tasks fail

---

## Exercises

**Exercise 1.**
Use `ThreadPoolExecutor.submit()` and `as_completed()` to process 10 items where items 3, 6, and 9 raise a `ValueError`. Collect successful results and errors separately into two dictionaries mapping input to result/error. Print both dictionaries.

??? success "Solution to Exercise 1"
        ```python
        from concurrent.futures import ThreadPoolExecutor, as_completed

        def process(x):
            if x in (3, 6, 9):
                raise ValueError(f"Cannot process {x}")
            return x ** 2

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(process, x): x for x in range(10)}
            results = {}
            errors = {}

            for future in as_completed(futures):
                x = futures[future]
                try:
                    results[x] = future.result()
                except Exception as e:
                    errors[x] = str(e)

            print(f"Results: {dict(sorted(results.items()))}")
            print(f"Errors:  {dict(sorted(errors.items()))}")
        ```

---

**Exercise 2.**
Write a `safe_map(executor, func, items)` function that wraps each call so that exceptions are returned as `("error", str(e))` tuples instead of raising. Use `executor.map()` internally. Test it with a function that fails on negative inputs. Print the count of successes and errors.

??? success "Solution to Exercise 2"
        ```python
        from concurrent.futures import ThreadPoolExecutor

        def safe_map(executor, func, items):
            def safe_func(x):
                try:
                    return ("success", func(x))
                except Exception as e:
                    return ("error", str(e))
            return list(executor.map(safe_func, items))

        def process(x):
            if x < 0:
                raise ValueError(f"Negative: {x}")
            return x ** 2

        data = [3, -1, 5, -2, 7, 0, -4, 10]

        with ThreadPoolExecutor() as executor:
            results = safe_map(executor, process, data)

        successes = [(r[1]) for r in results if r[0] == "success"]
        errors = [(r[1]) for r in results if r[0] == "error"]
        print(f"Successes ({len(successes)}): {successes}")
        print(f"Errors ({len(errors)}): {errors}")
        ```

---

**Exercise 3.**
Implement a batch processor with timeout handling. Submit 8 tasks to a `ThreadPoolExecutor`, where each task sleeps for a random duration (0.1-2.0s). Use `as_completed(futures, timeout=1.0)` to collect results that finish within 1 second. Cancel remaining tasks and print how many completed, how many timed out, and the results of the completed ones.

??? success "Solution to Exercise 3"
        ```python
        import time
        import random
        from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

        def task(task_id):
            delay = random.uniform(0.1, 2.0)
            time.sleep(delay)
            return (task_id, delay)

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(task, i): i for i in range(8)}
            completed = []

            try:
                for future in as_completed(futures, timeout=1.0):
                    completed.append(future.result())
            except TimeoutError:
                pass

            timed_out = 0
            for future in futures:
                if not future.done():
                    future.cancel()
                    timed_out += 1

            print(f"Completed: {len(completed)}")
            print(f"Timed out: {timed_out}")
            for tid, delay in completed:
                print(f"  Task {tid}: {delay:.2f}s")
        ```
