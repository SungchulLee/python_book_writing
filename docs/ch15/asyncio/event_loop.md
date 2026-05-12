# Event Loop

## What is the Event Loop?

The **event loop** is the core of asyncio. It:

- Schedules and runs coroutines
- Handles I/O events
- Manages callbacks and timers
- Coordinates all async operations

Think of it as a central dispatcher that decides which coroutine runs next.

```
┌─────────────────────────────────────────┐
│              Event Loop                 │
│  ┌─────────────────────────────────┐    │
│  │  Ready Queue: [task1, task2]    │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │  Waiting: {task3: I/O, task4}   │    │
│  └─────────────────────────────────┘    │
│                                         │
│  Loop: Pick ready task → Run until      │
│        await → Check I/O → Repeat       │
└─────────────────────────────────────────┘
```

---

## Running the Event Loop

### Modern Way: `asyncio.run()` (Python 3.7+)

```python
import asyncio

async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

# Recommended approach
asyncio.run(main())
```

`asyncio.run()`:

- Creates a new event loop
- Runs the coroutine until complete
- Closes the loop when done
- Handles cleanup automatically

### Manual Control (Rarely Needed)

```python
async def main():
    return "result"

# Get or create event loop
loop = asyncio.get_event_loop()

# Run until coroutine completes
result = loop.run_until_complete(main())

# Clean up
loop.close()
```

### Running Forever (Servers)

```python
async def server():
    while True:
        await handle_connection()

loop = asyncio.get_event_loop()
loop.run_forever()  # Runs until loop.stop() is called
```

---

## Event Loop Lifecycle

```python
import asyncio

async def task(name, delay):
    print(f"{name}: starting")
    await asyncio.sleep(delay)
    print(f"{name}: done")
    return name

async def main():
    # Event loop is running here
    print("Main: creating tasks")
    
    t1 = asyncio.create_task(task("A", 2))
    t2 = asyncio.create_task(task("B", 1))
    
    print("Main: waiting for tasks")
    await t1
    await t2
    print("Main: all done")

# Event loop: created → running → closed
asyncio.run(main())
```

Output:
```
Main: creating tasks
Main: waiting for tasks
A: starting
B: starting
B: done
A: done
Main: all done
```

---

## Getting the Current Loop

### Inside Async Code

```python
async def my_coroutine():
    loop = asyncio.get_running_loop()  # ✅ Use this inside async
    print(f"Running on loop: {loop}")
```

### Outside Async Code

```python
def setup():
    loop = asyncio.get_event_loop()  # Gets or creates loop
    # Schedule work...
```

### Difference

| Function | Context | Behavior |
|----------|---------|----------|
| `get_running_loop()` | Inside async | Returns current loop or raises |
| `get_event_loop()` | Anywhere | Gets/creates loop (deprecated pattern) |

---

## Scheduling Callbacks

### Call Soon (Next Iteration)

```python
def callback(message):
    print(f"Callback: {message}")

async def main():
    loop = asyncio.get_running_loop()
    
    loop.call_soon(callback, "Hello")
    print("Scheduled callback")
    
    await asyncio.sleep(0)  # Let loop process callbacks
    print("After sleep")

asyncio.run(main())
```

Output:
```
Scheduled callback
Callback: Hello
After sleep
```

### Call Later (Delayed)

```python
async def main():
    loop = asyncio.get_running_loop()
    
    # Call after 1 second
    loop.call_later(1.0, callback, "Delayed")
    
    print("Waiting...")
    await asyncio.sleep(2)

asyncio.run(main())
```

### Call At (Specific Time)

```python
async def main():
    loop = asyncio.get_running_loop()
    
    # Call at loop time + 1 second
    when = loop.time() + 1.0
    loop.call_at(when, callback, "At specific time")
    
    await asyncio.sleep(2)
```

---

## Running Blocking Code

### Problem: Blocking Calls

```python
import time

async def bad():
    time.sleep(5)  # ❌ Blocks entire event loop!
    return "done"
```

### Solution: run_in_executor

```python
import asyncio
import time

def blocking_io():
    """Blocking function (e.g., file I/O, legacy code)"""
    time.sleep(1)
    return "Blocking operation complete"

async def main():
    loop = asyncio.get_running_loop()
    
    # Run in default thread pool executor
    result = await loop.run_in_executor(None, blocking_io)
    print(result)

asyncio.run(main())
```

### Custom Executor

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

async def main():
    loop = asyncio.get_running_loop()
    
    # Thread pool for I/O-bound blocking code
    with ThreadPoolExecutor(max_workers=4) as pool:
        result = await loop.run_in_executor(pool, blocking_io)
    
    # Process pool for CPU-bound code
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cpu_heavy_task)
```

---

## Event Loop Methods

### Time

```python
async def main():
    loop = asyncio.get_running_loop()
    
    # Current loop time (monotonic)
    now = loop.time()
    print(f"Loop time: {now}")
```

### Debug Mode

```python
# Enable debug mode
asyncio.run(main(), debug=True)

# Or via environment variable
# PYTHONASYNCIODEBUG=1 python script.py
```

Debug mode:

- Warns about unawaited coroutines
- Logs slow callbacks (>100ms)
- Enables additional checks

---

## Multiple Event Loops (Advanced)

### Different Threads, Different Loops

```python
import asyncio
import threading

def run_in_thread():
    # Create new loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def task():
        return "From thread"
    
    result = loop.run_until_complete(task())
    loop.close()
    return result

# Main thread has its own loop
thread = threading.Thread(target=run_in_thread)
thread.start()
thread.join()
```

### Nested Loops (Avoid!)

```python
async def outer():
    asyncio.run(inner())  # ❌ RuntimeError: cannot run nested

# Use create_task or gather instead
async def outer():
    await inner()  # ✅ Just await it
```

---

## Common Patterns

### Graceful Shutdown

```python
import signal

async def main():
    loop = asyncio.get_running_loop()
    
    # Handle shutdown signals
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown()))

async def shutdown():
    print("Shutting down...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)
    asyncio.get_event_loop().stop()
```

### Event Loop in Class

```python
class AsyncService:
    def __init__(self):
        self._loop = None
    
    async def start(self):
        self._loop = asyncio.get_running_loop()
        # Initialize async resources
    
    async def stop(self):
        # Cleanup async resources
        pass
```

---

## Summary

| Function | Purpose |
|----------|---------|
| `asyncio.run(coro)` | Run coroutine (main entry point) |
| `asyncio.get_running_loop()` | Get loop inside async code |
| `asyncio.get_event_loop()` | Get/create loop (sync code) |
| `loop.run_until_complete()` | Run until coroutine finishes |
| `loop.run_forever()` | Run until `stop()` called |
| `loop.run_in_executor()` | Run blocking code in thread/process |
| `loop.call_soon()` | Schedule callback for next iteration |
| `loop.call_later()` | Schedule delayed callback |
| `loop.time()` | Get current loop time |

**Key Takeaways**:

- Use `asyncio.run()` for most applications
- One event loop per thread
- Don't block the event loop — use `run_in_executor`
- Debug mode helps find common mistakes
- The event loop handles all scheduling automatically

---

## Runnable Example: `event_loop_tutorial.py`

```python
"""
Beginner Tutorial 3: Understanding the Event Loop

This file explains the event loop - the heart of asyncio that makes
async programming possible.

Topics covered:
- What is the event loop?
- How the event loop works
- Event loop operations
- Running and managing the event loop
- Event loop debugging

Learning objectives:
1. Understand what the event loop does
2. Learn how tasks are scheduled and executed
3. See how control flows between coroutines
4. Access and interact with the event loop
"""

import asyncio
import time
from typing import List


# ============================================================================
# PART 1: What is the Event Loop?
# ============================================================================

async def explain_event_loop():
    """
    The event loop is the core of asyncio.
    
    Think of it as a task manager that:
    1. Keeps track of all async tasks
    2. Decides which task to run next
    3. Switches between tasks when they hit 'await'
    4. Handles I/O operations efficiently
    
    Without the event loop, async/await would be just syntax.
    The event loop is what makes it actually work!
    """
    print("\n--- What is the Event Loop? ---")
    print("""
    The Event Loop is like a conductor of an orchestra:
    - It knows about all the musicians (coroutines)
    - It tells each when to play (schedule)
    - It switches between them smoothly (context switching)
    - It handles pauses and timing (await, sleep)
    
    Key responsibilities:
    1. Schedule coroutines and callbacks
    2. Perform network I/O operations
    3. Run subprocesses
    4. Handle OS signals
    5. Manage timers and delays
    """)


# ============================================================================
# PART 2: Event Loop in Action
# ============================================================================

async def task_a():
    """First task that will be scheduled on the event loop"""
    print("  Task A: Starting")
    print("  Task A: About to await (yielding control)")
    await asyncio.sleep(1)  # Control goes back to event loop here
    print("  Task A: Resumed after sleep")
    print("  Task A: Finishing")
    return "A complete"


async def task_b():
    """Second task that will be scheduled on the event loop"""
    print("    Task B: Starting")
    print("    Task B: About to await (yielding control)")
    await asyncio.sleep(0.5)  # Shorter sleep than task_a
    print("    Task B: Resumed after sleep")
    print("    Task B: Finishing")
    return "B complete"


async def visualize_event_loop():
    """
    Demonstrates how the event loop schedules and runs tasks.
    
    What happens:
    1. Event loop starts task_a
    2. task_a hits await, yields control
    3. Event loop starts task_b
    4. task_b hits await, yields control
    5. Event loop waits for I/O (both sleeping)
    6. task_b's sleep finishes first (0.5s)
    7. Event loop resumes task_b, which completes
    8. task_a's sleep finishes (1s)
    9. Event loop resumes task_a, which completes
    """
    print("\n--- Event Loop in Action ---")
    print("Watch how the event loop switches between tasks:\n")
    
    # Create tasks (we'll learn more about tasks later)
    # Tasks are scheduled on the event loop immediately
    task1 = asyncio.create_task(task_a())
    task2 = asyncio.create_task(task_b())
    
    print("Both tasks created and scheduled on event loop\n")
    
    # Wait for both to complete
    result_a = await task1
    result_b = await task2
    
    print(f"\nResults: {result_a}, {result_b}")
    
    print("""
    Notice the execution order:
    1. Task A starts
    2. Task A awaits (yields to event loop)
    3. Task B starts
    4. Task B awaits (yields to event loop)
    5. Task B finishes first (shorter sleep)
    6. Task A finishes second (longer sleep)
    
    The event loop efficiently managed both tasks!
    """)


# ============================================================================
# PART 3: Accessing the Event Loop
# ============================================================================

async def access_event_loop():
    """
    Shows how to access and interact with the event loop.
    
    In Python 3.10+, you typically don't need to access the event loop
    directly, but it's good to understand how.
    """
    print("\n--- Accessing the Event Loop ---")
    
    # Get the currently running event loop
    loop = asyncio.get_running_loop()
    
    print(f"Event loop type: {type(loop)}")
    print(f"Event loop: {loop}")
    
    # Check if loop is running
    print(f"Is running: {loop.is_running()}")
    
    # Get current time according to the loop
    loop_time = loop.time()
    print(f"Loop time: {loop_time:.2f}")
    
    # Schedule a callback (advanced - usually not needed)
    def callback():
        print("  Callback executed by event loop!")
    
    # Call callback after 0.1 seconds
    loop.call_later(0.1, callback)
    await asyncio.sleep(0.2)  # Wait for callback to execute


# ============================================================================
# PART 4: Event Loop Lifecycle
# ============================================================================

def demonstrate_event_loop_lifecycle():
    """
    Shows the lifecycle of an event loop (non-async function).
    
    Lifecycle:
    1. Create loop
    2. Run tasks on loop
    3. Close loop
    
    Note: With asyncio.run(), this is all handled automatically!
    """
    print("\n--- Event Loop Lifecycle ---")
    
    async def simple_task():
        print("  Task running on event loop")
        await asyncio.sleep(0.1)
        return "Done"
    
    print("Manual event loop management (rarely needed):")
    
    # Method 1: Using asyncio.run() (RECOMMENDED)
    print("\n1. Using asyncio.run() (recommended):")
    result = asyncio.run(simple_task())
    print(f"   Result: {result}")
    print("   Loop automatically created and closed!")
    
    # Method 2: Manual (for understanding only)
    print("\n2. Manual loop management (advanced):")
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # try:
    #     result = loop.run_until_complete(simple_task())
    #     print(f"   Result: {result}")
    # finally:
    #     loop.close()
    print("   (Commented out - asyncio.run() is better!)")
    
    print("\n✓ Always use asyncio.run() for simple programs")
    print("✓ Manual loop management is for special cases only")


# ============================================================================
# PART 5: How the Event Loop Schedules Tasks
# ============================================================================

async def demonstrate_scheduling():
    """
    Shows how tasks are scheduled and executed by the event loop.
    
    The event loop uses a queue-like structure to manage tasks:
    1. Tasks ready to run are in the "ready" queue
    2. Tasks waiting on I/O are registered with the I/O selector
    3. The loop alternates between running ready tasks and checking I/O
    """
    print("\n--- Event Loop Scheduling ---")
    
    async def numbered_task(number: int, delay: float):
        print(f"  Task {number}: Starting")
        await asyncio.sleep(delay)
        print(f"  Task {number}: Finished after {delay}s")
        return number
    
    print("Creating 5 tasks with different delays:")
    print("(Watch the order of completion)\n")
    
    # Create tasks with various delays
    tasks = [
        asyncio.create_task(numbered_task(1, 0.3)),
        asyncio.create_task(numbered_task(2, 0.1)),
        asyncio.create_task(numbered_task(3, 0.2)),
        asyncio.create_task(numbered_task(4, 0.4)),
        asyncio.create_task(numbered_task(5, 0.15)),
    ]
    
    # Wait for all tasks
    results = await asyncio.gather(*tasks)
    
    print(f"\nResults in order created: {results}")
    print("Notice they finished in order of delay, not creation order!")


# ============================================================================
# PART 6: Event Loop Performance
# ============================================================================

async def compare_sequential_vs_concurrent():
    """
    Demonstrates the performance benefit of the event loop.
    
    Sequential: Tasks run one after another
    Concurrent: Event loop switches between tasks during I/O waits
    """
    print("\n--- Event Loop Performance ---")
    
    async def io_operation(task_id: int):
        """Simulates an I/O operation (network request, file read, etc.)"""
        await asyncio.sleep(0.5)  # Simulate I/O delay
        return f"Result_{task_id}"
    
    # Sequential execution
    print("Sequential execution (one at a time):")
    start_time = time.time()
    
    results = []
    for i in range(5):
        result = await io_operation(i)
        results.append(result)
    
    sequential_time = time.time() - start_time
    print(f"  Time: {sequential_time:.2f}s (5 tasks × 0.5s each)")
    
    # Concurrent execution
    print("\nConcurrent execution (event loop manages):")
    start_time = time.time()
    
    # Create all tasks at once - event loop handles them
    tasks = [io_operation(i) for i in range(5)]
    results = await asyncio.gather(*tasks)
    
    concurrent_time = time.time() - start_time
    print(f"  Time: {concurrent_time:.2f}s (all 5 tasks overlap)")
    
    # Show improvement
    speedup = sequential_time / concurrent_time
    print(f"\nSpeedup: {speedup:.1f}x faster!")
    print("This is the power of the event loop!")


# ============================================================================
# PART 7: Event Loop Debugging
# ============================================================================

async def debug_event_loop():
    """
    Shows debugging techniques for event loop issues.
    
    Common issues:
    - Blocking the event loop with CPU-intensive work
    - Forgetting to await
    - Long-running tasks starving others
    """
    print("\n--- Event Loop Debugging ---")
    
    # Enable debug mode
    loop = asyncio.get_running_loop()
    original_debug = loop.get_debug()
    
    print(f"Debug mode: {original_debug}")
    print("\nDebug mode helps detect:")
    print("  - Coroutines that weren't awaited")
    print("  - Tasks taking too long")
    print("  - Resources not properly closed")
    
    # You can enable debug mode when running:
    # asyncio.run(main(), debug=True)
    
    async def good_task():
        """Properly written async task"""
        await asyncio.sleep(0.1)
        return "Good"
    
    async def bad_task_example():
        """Example of what NOT to do"""
        # ❌ BAD: This blocks the event loop!
        # time.sleep(1)  # Don't do this!
        
        # ✅ GOOD: This yields to event loop
        await asyncio.sleep(0.1)
        return "Fixed"
    
    result = await good_task()
    print(f"\nGood task result: {result}")


# ============================================================================
# PART 8: Event Loop Best Practices
# ============================================================================

async def event_loop_best_practices():
    """
    Summarizes best practices for working with the event loop.
    """
    print("\n--- Event Loop Best Practices ---")
    
    print("""
    DO:
    ✓ Use asyncio.run() to start your program
    ✓ Use await with all async operations
    ✓ Let the event loop handle task scheduling
    ✓ Use async libraries (aiohttp, not requests)
    ✓ Keep individual tasks small and focused
    
    DON'T:
    ✗ Block the event loop with CPU-intensive work
    ✗ Use time.sleep() - use asyncio.sleep()
    ✗ Use blocking I/O (regular file operations, requests)
    ✗ Manually manage the event loop (unless necessary)
    ✗ Create multiple event loops in one thread
    
    REMEMBER:
    - The event loop is single-threaded
    - It can only run one task at a time
    - Concurrency comes from switching during I/O waits
    - For CPU-bound work, use multiprocessing
    """)


# ============================================================================
# PART 9: Event Loop Mental Models
# ============================================================================

async def event_loop_mental_models():
    """
    Provides mental models for understanding the event loop.
    """
    print("\n--- Event Loop Mental Models ---")
    
    print("""
    Mental Model 1: Restaurant Kitchen
    - Event loop = Head chef
    - Coroutines = Dishes being prepared
    - await = Waiting for oven/ingredient
    - The chef switches between dishes when each is waiting
    
    Mental Model 2: Single-Lane Highway
    - Event loop = The single lane
    - Tasks = Cars on the highway
    - await = Car pulls over (rest stop, gas)
    - Other cars can pass while one is stopped
    
    Mental Model 3: Juggler
    - Event loop = The juggler
    - Tasks = Balls in the air
    - await = Ball is in the air (not in hand)
    - Juggler catches/throws other balls while each is airborne
    
    Key Insight: 
    The event loop doesn't make things happen in parallel.
    It efficiently switches between tasks when they're waiting.
    This is called COOPERATIVE MULTITASKING.
    """)


# ============================================================================
# MAIN FUNCTION
# ============================================================================

async def main():
    """
    Main coroutine demonstrating event loop concepts.
    """
    print("=" * 70)
    print("EVENT LOOP TUTORIAL")
    print("=" * 70)
    
    # Part 1: Explanation
    await explain_event_loop()
    
    # Part 2: Visualization
    await visualize_event_loop()
    
    # Part 3: Access
    await access_event_loop()
    
    # Part 4: Lifecycle
    demonstrate_event_loop_lifecycle()
    
    # Part 5: Scheduling
    await demonstrate_scheduling()
    
    # Part 6: Performance
    await compare_sequential_vs_concurrent()
    
    # Part 7: Debugging
    await debug_event_loop()
    
    # Part 8: Best practices
    await event_loop_best_practices()
    
    # Part 9: Mental models
    await event_loop_mental_models()
    
    print("\n" + "=" * 70)
    print("Tutorial complete!")
    print("=" * 70)


if __name__ == "__main__":
    # This is how you start the event loop!
    asyncio.run(main())


"""
KEY TAKEAWAYS:

1. EVENT LOOP: The engine that runs async code
   - Schedules and executes coroutines
   - Handles I/O operations efficiently
   - Single-threaded, cooperative multitasking

2. HOW IT WORKS:
   - Keeps a queue of ready tasks
   - Runs one task until it hits 'await'
   - Switches to next ready task
   - Checks for completed I/O operations
   - Resumes tasks when their I/O completes

3. PERFORMANCE:
   - Efficient for I/O-bound operations
   - Can handle thousands of concurrent connections
   - Much lighter than threads
   - Doesn't help with CPU-bound work

4. BEST PRACTICES:
   - Use asyncio.run() to start programs
   - Never block the event loop
   - Use async libraries
   - Keep tasks small and focused

5. COMMON MISTAKES:
   - Using time.sleep() instead of asyncio.sleep()
   - Blocking I/O operations
   - CPU-intensive calculations
   - Not awaiting async calls

MENTAL MODEL:
Event loop = Traffic controller at intersection
- Manages multiple flows (tasks)
- Gives each the green light (runs task)
- When one waits (red light/await), switches to another
- Keeps everything moving efficiently

ANALOGY:
Traditional programming: Assembly line (one task at a time)
Event loop: Kitchen with multiple dishes cooking simultaneously
  - Stir pot A → Check oven B → Chop for C → Back to A
  - Efficient because there's always something to do

NEXT STEPS:
- Learn to run multiple coroutines (04_multiple_coroutines.py)
- Master asyncio.gather() (05_async_gather_intro.py)
- Explore concurrent patterns (intermediate/)
"""
```

---

## Exercises

**Exercise 1.**
Write an async program that uses `loop.call_later()` to schedule three callbacks at 0.1s, 0.2s, and 0.3s. Each callback should append its scheduled time to a shared list. After sleeping long enough for all callbacks to fire, print the list to confirm the order.

??? success "Solution to Exercise 1"
        ```python
        import asyncio

        async def main():
            loop = asyncio.get_running_loop()
            results = []

            loop.call_later(0.1, lambda: results.append("0.1s"))
            loop.call_later(0.2, lambda: results.append("0.2s"))
            loop.call_later(0.3, lambda: results.append("0.3s"))

            await asyncio.sleep(0.5)
            print(f"Callback order: {results}")

        asyncio.run(main())
        ```

---

**Exercise 2.**
Write an async function that uses `loop.run_in_executor()` to run a blocking function (`time.sleep(1)` that returns a value) in a thread pool without blocking the event loop. While the blocking call is running, concurrently run an async countdown from 5 to 1 (printing each number with `await asyncio.sleep(0.2)`). Print the executor result and confirm both ran concurrently.

??? success "Solution to Exercise 2"
        ```python
        import asyncio
        import time

        def blocking_work():
            time.sleep(1)
            return "blocking result"

        async def countdown():
            for i in range(5, 0, -1):
                print(f"  Countdown: {i}")
                await asyncio.sleep(0.2)

        async def main():
            loop = asyncio.get_running_loop()

            executor_task = loop.run_in_executor(None, blocking_work)
            countdown_task = asyncio.create_task(countdown())

            result = await executor_task
            await countdown_task

            print(f"Executor returned: {result}")

        asyncio.run(main())
        ```

---

**Exercise 3.**
Measure the performance difference between sequential and concurrent execution of 10 simulated I/O tasks (each `await asyncio.sleep(0.2)`). Print the sequential time, concurrent time, and the speedup factor.

??? success "Solution to Exercise 3"
        ```python
        import asyncio
        import time

        async def io_task(task_id):
            await asyncio.sleep(0.2)
            return task_id

        async def main():
            # Sequential
            start = time.perf_counter()
            for i in range(10):
                await io_task(i)
            seq_time = time.perf_counter() - start

            # Concurrent
            start = time.perf_counter()
            await asyncio.gather(*[io_task(i) for i in range(10)])
            con_time = time.perf_counter() - start

            print(f"Sequential: {seq_time:.2f}s")
            print(f"Concurrent: {con_time:.2f}s")
            print(f"Speedup: {seq_time / con_time:.1f}x")

        asyncio.run(main())
        ```
