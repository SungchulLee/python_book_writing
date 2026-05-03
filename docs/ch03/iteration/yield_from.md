# yield from

The yield from statement delegates to a sub-generator, combining value iteration and exception handling. It's a powerful tool for building complex generator hierarchies and simplifying generator composition.

!!! tip "Mental Model"
    `yield from sub` is shorthand for "step aside and let `sub` yield directly to my caller." Instead of writing a loop that manually forwards each value, `yield from` creates a transparent pipe between the sub-generator and the outer consumer. It also forwards `send()`, `throw()`, and `close()` calls automatically.

---

## Basic yield from

### Delegating to Sub-generator

```python
def simple_generator():
    yield 1
    yield 2
    yield 3

def delegating_generator():
    yield from simple_generator()
    yield 4

for value in delegating_generator():
    print(value)
```

Output:
```
1
2
3
4
```

### vs yield in a Loop

```python
def with_loop(g):
    for value in g:
        yield value

def with_yield_from(g):
    yield from g

g = (i for i in range(3))
print(list(with_loop(g)))

g = (i for i in range(3))
print(list(with_yield_from(g)))
```

Output:
```
[0, 1, 2]
[0, 1, 2]
```

## Nested Generators

### Tree Traversal

```python
def flatten(nested_list):
    for item in nested_list:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

tree = [1, [2, 3, [4, 5]], 6]
result = list(flatten(tree))
print(result)
```

Output:
```
[1, 2, 3, 4, 5, 6]
```

## Exception Handling

### Propagating Exceptions

```python
def sub_gen():
    try:
        yield 1
        yield 2
        yield 3
    except ValueError:
        yield "caught error"

def delegating():
    yield from sub_gen()

gen = delegating()
print(next(gen))
print(next(gen))
```

Output:
```
1
2
```

## Return Values

### Capturing Sub-generator Return

```python
def sub_generator():
    yield 1
    yield 2
    return "done"

def delegating():
    result = yield from sub_generator()
    yield f"Got: {result}"

for value in delegating():
    print(value)
```

Output:
```
1
2
Got: done
```

---

## Runnable Example: `advanced_generators.py`

```python
"""
PYTHON GENERATORS & ITERATORS - ADVANCED LEVEL
==============================================

Topic: Advanced Generator Techniques
------------------------------------

This module covers:
1. Generator methods: send(), throw(), close()
2. Bidirectional communication with generators
3. Generator delegation with yield from
4. Coroutines and asynchronous patterns
5. Generator pipelines and composition
6. Advanced performance optimization

Learning Objectives:
- Master advanced generator methods
- Implement bidirectional generator communication
- Use yield from for generator delegation
- Build complex generator pipelines
- Apply coroutine patterns
- Optimize generator performance

Prerequisites:
- Completion of beginner and intermediate levels
- Strong understanding of generators and yield
- Familiarity with exceptions
- Basic understanding of function composition
"""

import sys
import traceback

# ============================================================================
# SECTION 1: GENERATOR METHODS - send()
# ============================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SECTION 1: BIDIRECTIONAL COMMUNICATION WITH send()")
    print("=" * 70)

    """
    GENERATOR.send(value): Send a value INTO a running generator

    So far, generators have been one-way: they yield values OUT.
    With send(), we can also pass values IN to the generator.

    How it works:
    1. The sent value becomes the result of the yield expression
    2. Generator resumes execution
    3. Continues until next yield
    4. Returns the yielded value

    Key points:
    - Must call next() or send(None) first to start the generator
    - The yield keyword can be used as an expression
    - Enables bidirectional communication
    """

    # Example 1.1: Basic send() usage
    print("\n--- Example 1.1: Introduction to send() ---")


    def echo_generator():
        """
        Simple generator demonstrating send().

        The generator receives values sent to it and
        processes them before yielding results.
        """
        print("  Generator started")

        while True:
            # yield is used as an expression here
            # The value sent via send() becomes the result of this expression
            received = yield
            print(f"  Received: {received}")


    # Using send()
    gen = echo_generator()

    # IMPORTANT: Must prime the generator first!
    next(gen)  # or gen.send(None) - advances to first yield

    # Now we can send values
    gen.send("Hello")
    gen.send("World")
    gen.send(42)


    # Example 1.2: send() with yielded values
    print("\n--- Example 1.2: send() with Return Values ---")


    def accumulator():
        """
        Generator that accumulates sent values.

        Demonstrates both receiving values via send()
        and yielding values back to the caller.
        """
        total = 0
        print("  Accumulator ready")

        while True:
            # Receive value and yield current total
            value = yield total
            if value is None:
                break
            total += value
            print(f"  Added {value}, total now {total}")


    # Using the accumulator
    print("Accumulator example:")
    acc = accumulator()

    # Prime the generator
    print(f"Initial total: {next(acc)}")

    # Send values and get updated totals
    print(f"After sending 10: {acc.send(10)}")
    print(f"After sending 20: {acc.send(20)}")
    print(f"After sending 30: {acc.send(30)}")

    # Stop by sending None
    acc.send(None)


    # Example 1.3: Practical send() example - running average
    print("\n--- Example 1.3: Running Average Calculator ---")


    def running_average():
        """
        Calculate running average of sent values.

        Demonstrates a practical use of send() for
        maintaining state and performing calculations.
        """
        total = 0.0
        count = 0
        average = None

        while True:
            # Yield current average, receive new value
            value = yield average

            if value is None:
                break

            total += value
            count += 1
            average = total / count


    # Using running average
    print("Running average calculator:")
    avg_calc = running_average()
    next(avg_calc)  # Prime the generator

    values = [10, 20, 30, 40, 50]
    for val in values:
        avg = avg_calc.send(val)
        print(f"Sent {val}, running average: {avg:.2f}")


    # Example 1.4: Two-way communication pattern
    print("\n--- Example 1.4: Request-Response Pattern ---")


    def data_processor():
        """
        Generator that processes different types of requests.

        Demonstrates using send() for command-based interaction.
        """
        data_store = []

        while True:
            # Receive command dict: {'action': 'add'/'get'/'sum', 'value': ...}
            command = yield

            if command is None:
                break

            action = command.get('action')

            if action == 'add':
                value = command.get('value')
                data_store.append(value)
                result = f"Added {value}"

            elif action == 'get':
                result = data_store.copy()

            elif action == 'sum':
                result = sum(data_store)

            else:
                result = "Unknown action"

            # Yield result back
            print(f"  {result}")


    # Using the data processor
    print("Data processor example:")
    processor = data_processor()
    next(processor)

    processor.send({'action': 'add', 'value': 10})
    processor.send({'action': 'add', 'value': 20})
    processor.send({'action': 'add', 'value': 30})
    processor.send({'action': 'sum'})


    # ============================================================================
    # SECTION 2: GENERATOR METHODS - throw()
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 2: EXCEPTION HANDLING WITH throw()")
    print("=" * 70)

    """
    GENERATOR.throw(exception): Throw an exception INTO a generator

    The throw() method allows you to inject an exception into a generator
    at the point where it's currently paused (at a yield).

    How it works:
    1. Exception is raised at the yield statement
    2. Generator can catch and handle it with try/except
    3. If caught, generator can continue
    4. If not caught, exception propagates to caller

    Use cases:
    - Signal errors or special conditions
    - Graceful shutdown of generators
    - Implementing timeout or cancel operations
    """

    # Example 2.1: Basic throw() usage
    print("\n--- Example 2.1: Introduction to throw() ---")


    def resilient_generator():
        """
        Generator that handles exceptions.

        Demonstrates catching exceptions thrown into the generator.
        """
        try:
            print("  Starting")
            yield 1

            print("  After first yield")
            yield 2

            print("  After second yield")
            yield 3

        except ValueError as e:
            print(f"  Caught ValueError: {e}")
            yield "Error handled"

        except Exception as e:
            print(f"  Caught Exception: {e}")
            yield "Unknown error"


    # Using throw()
    print("Throwing exception into generator:")
    gen = resilient_generator()

    print(f"First value: {next(gen)}")

    # Throw ValueError into the generator
    try:
        result = gen.throw(ValueError, "Something went wrong")
        print(f"After throw: {result}")
    except StopIteration:
        print("Generator stopped")


    # Example 2.2: Using throw() for cancellation
    print("\n--- Example 2.2: Cancellation Pattern ---")


    class CancelOperation(Exception):
        """Custom exception for cancelling operations."""
        pass


    def long_running_task():
        """
        Generator simulating a long-running task.

        Can be cancelled by throwing CancelOperation.
        """
        try:
            for i in range(10):
                print(f"  Processing step {i}")
                result = yield f"Step {i} complete"

        except CancelOperation:
            print("  Task cancelled, cleaning up...")
            yield "Cancelled"
            return

        print("  Task completed successfully")
        yield "Complete"


    # Simulate cancellation
    print("Running task and cancelling midway:")
    task = long_running_task()

    # Run a few steps
    print(next(task))
    print(next(task))

    # Cancel the operation
    try:
        result = task.throw(CancelOperation)
        print(result)
    except StopIteration:
        pass


    # Example 2.3: Retry mechanism with throw()
    print("\n--- Example 2.3: Retry Mechanism ---")


    class RetryException(Exception):
        """Signal that operation should be retried."""
        pass


    def operation_with_retry():
        """
        Generator that can retry operations.

        Demonstrates using throw() to trigger retries.
        """
        attempt = 0

        while True:
            try:
                attempt += 1
                print(f"  Attempt {attempt}")

                # Yield attempt number
                yield attempt

                # If we get here, operation succeeded
                print("  Operation successful")
                break

            except RetryException:
                print("  Retrying...")
                if attempt >= 3:
                    print("  Max retries reached")
                    raise


    # Using retry mechanism
    print("Testing retry mechanism:")
    operation = operation_with_retry()

    # First attempt
    print(f"Result: {next(operation)}")

    # Trigger retry
    try:
        operation.throw(RetryException)
        print(f"Result: {next(operation)}")
    except StopIteration:
        print("Operation completed")


    # ============================================================================
    # SECTION 3: GENERATOR METHODS - close()
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 3: CLEANUP WITH close()")
    print("=" * 70)

    """
    GENERATOR.close(): Terminate a generator cleanly

    The close() method:
    1. Raises GeneratorExit exception at the current yield
    2. Generator can catch it for cleanup in finally block
    3. Generator must not yield any more values after GeneratorExit
    4. If it does, RuntimeError is raised

    Use cases:
    - Clean up resources (files, connections)
    - Graceful shutdown
    - Breaking out of infinite generators
    """

    # Example 3.1: Basic close() usage
    print("\n--- Example 3.1: Introduction to close() ---")


    def generator_with_cleanup():
        """
        Generator with cleanup code.

        Demonstrates proper resource cleanup with finally block.
        """
        print("  Acquiring resource")
        resource = "database_connection"

        try:
            for i in range(10):
                print(f"  Yielding {i}")
                yield i
        finally:
            print("  Releasing resource")
            # Cleanup code here
            resource = None


    # Using close()
    print("Using generator and closing early:")
    gen = generator_with_cleanup()

    print(next(gen))
    print(next(gen))

    # Close the generator
    gen.close()
    print("Generator closed")

    # Trying to use it after close() raises StopIteration
    try:
        next(gen)
    except StopIteration:
        print("Cannot use generator after close()")


    # Example 3.2: Automatic cleanup with context manager
    print("\n--- Example 3.2: Generator as Context Manager ---")


    class GeneratorContextManager:
        """
        Wrapper to use generator as context manager.

        Ensures close() is called even if exception occurs.
        """

        def __init__(self, generator):
            self.generator = generator

        def __enter__(self):
            return self.generator

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.generator.close()
            return False


    def resource_generator():
        """Generator managing a resource."""
        print("  Setup")
        try:
            for i in range(5):
                yield i
        finally:
            print("  Cleanup")


    # Using as context manager
    print("Using generator with context manager:")
    with GeneratorContextManager(resource_generator()) as gen:
        print(next(gen))
        print(next(gen))
        # Cleanup happens automatically


    # Example 3.3: Breaking infinite generators
    print("\n--- Example 3.3: Closing Infinite Generators ---")


    def infinite_generator():
        """Infinite generator that needs explicit closing."""
        count = 0
        try:
            while True:
                yield count
                count += 1
        finally:
            print(f"  Generator closed after {count} iterations")


    # Must use close() to stop infinite generator
    print("Using infinite generator:")
    gen = infinite_generator()

    for i in range(3):
        print(next(gen))

    gen.close()


    # ============================================================================
    # SECTION 4: YIELD FROM - GENERATOR DELEGATION
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 4: GENERATOR DELEGATION WITH yield from")
    print("=" * 70)

    """
    YIELD FROM: Delegate to a sub-generator

    yield from sub_gen is equivalent to:
        for value in sub_gen:
            yield value

    But yield from does more:
    - Automatically forwards send() calls
    - Automatically forwards throw() calls
    - Returns the sub-generator's return value
    - More efficient than manual forwarding

    Use cases:
    - Composing generators
    - Flattening nested structures
    - Building generator pipelines
    - Simplifying complex iteration
    """

    # Example 4.1: Basic yield from
    print("\n--- Example 4.1: Introduction to yield from ---")


    def sub_generator():
        """Sub-generator that yields some values."""
        print("  Sub-generator starting")
        yield 1
        yield 2
        yield 3
        print("  Sub-generator ending")
        return "Sub done"


    def main_generator_manual():
        """Manual delegation (the old way)."""
        print("Main starting")
        for value in sub_generator():
            yield value
        print("Main ending")


    def main_generator_yield_from():
        """Delegation with yield from (the better way)."""
        print("Main starting")
        result = yield from sub_generator()
        print(f"Sub-generator returned: {result}")
        print("Main ending")


    # Compare both approaches
    print("Manual delegation:")
    for val in main_generator_manual():
        print(val)

    print("\nWith yield from:")
    for val in main_generator_yield_from():
        print(val)


    # Example 4.2: Chaining multiple generators
    print("\n--- Example 4.2: Chaining Generators ---")


    def gen1():
        """First generator."""
        yield 'A'
        yield 'B'


    def gen2():
        """Second generator."""
        yield 'C'
        yield 'D'


    def gen3():
        """Third generator."""
        yield 'E'
        yield 'F'


    def chain_generators():
        """
        Chain multiple generators using yield from.

        Much cleaner than manual loop nesting.
        """
        yield from gen1()
        yield from gen2()
        yield from gen3()


    print("Chained generators:")
    for item in chain_generators():
        print(item, end=' ')
    print()


    # Example 4.3: Flattening nested structures
    print("\n--- Example 4.3: Flattening Nested Lists ---")


    def flatten(nested_list):
        """
        Recursively flatten a nested list structure.

        Demonstrates recursive use of yield from.
        """
        for item in nested_list:
            if isinstance(item, list):
                # Recursively flatten sub-lists
                yield from flatten(item)
            else:
                # Yield individual items
                yield item


    # Test with nested list
    nested = [1, [2, [3, 4], 5], [6, 7], 8]
    print(f"Original: {nested}")
    print(f"Flattened: {list(flatten(nested))}")


    # Example 4.4: yield from forwards send()
    print("\n--- Example 4.4: Forwarding send() with yield from ---")


    def sub_gen_with_send():
        """Sub-generator that receives values via send()."""
        while True:
            received = yield
            if received is None:
                break
            print(f"  Sub received: {received}")


    def delegating_generator():
        """
        Delegate to sub-generator.

        yield from automatically forwards send() calls
        to the sub-generator.
        """
        print("Delegating to sub-generator")
        yield from sub_gen_with_send()
        print("Back from sub-generator")


    # send() is automatically forwarded
    print("Forwarding send() through yield from:")
    gen = delegating_generator()
    next(gen)  # Prime

    gen.send("Hello")
    gen.send("World")
    gen.send(None)


    # Example 4.5: Building data pipelines
    print("\n--- Example 4.5: Data Pipeline with yield from ---")


    def read_data():
        """Simulate data source."""
        data = ['1', '2', '3', 'bad', '4', '5']
        for item in data:
            yield item


    def parse_numbers(data_source):
        """Parse strings to integers."""
        for item in data_source:
            try:
                yield int(item)
            except ValueError:
                pass  # Skip invalid values


    def filter_even(number_source):
        """Filter even numbers."""
        for num in number_source:
            if num % 2 == 0:
                yield num


    def double_values(number_source):
        """Double each number."""
        for num in number_source:
            yield num * 2


    def pipeline():
        """
        Complete processing pipeline using yield from.

        Demonstrates composition of multiple generators.
        """
        data = read_data()
        numbers = parse_numbers(data)
        evens = filter_even(numbers)
        doubled = double_values(evens)
        yield from doubled


    print("Processing pipeline result:")
    print(list(pipeline()))


    # ============================================================================
    # SECTION 5: COROUTINES
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 5: COROUTINES")
    print("=" * 70)

    """
    COROUTINE: Generator used for consuming values rather than producing them

    Characteristics:
    - Primary purpose is to receive values (via send())
    - May not yield meaningful values
    - Often runs in infinite loop
    - Represents a data consumer/processor

    Pattern:
    1. Create coroutine generator
    2. Prime it with next() or .send(None)
    3. Send values to it with .send()
    4. Close when done

    Note: This is the "generator-based coroutine" pattern.
    Modern async/await (Python 3.5+) is the preferred approach
    for concurrent programming, but this pattern is still useful
    for understanding and certain use cases.
    """

    # Example 5.1: Simple coroutine
    print("\n--- Example 5.1: Basic Coroutine ---")


    def coroutine_example():
        """
        Simple coroutine that receives and processes values.

        Demonstrates the coroutine pattern: receiving data
        rather than generating it.
        """
        print("  Coroutine started, waiting for values")

        try:
            while True:
                # Receive value
                value = yield
                print(f"  Processing: {value}")
        except GeneratorExit:
            print("  Coroutine closing")


    # Using a coroutine
    coro = coroutine_example()
    next(coro)  # Prime the coroutine

    coro.send(10)
    coro.send(20)
    coro.send(30)
    coro.close()


    # Example 5.2: Coroutine decorator for auto-priming
    print("\n--- Example 5.2: Auto-Priming Decorator ---")


    def coroutine(func):
        """
        Decorator to automatically prime a coroutine.

        Eliminates the need to call next() before first send().
        """
        def wrapper(*args, **kwargs):
            gen = func(*args, **kwargs)
            next(gen)  # Prime it
            return gen
        return wrapper


    @coroutine
    def averaging_coroutine():
        """
        Coroutine that maintains running average.

        Automatically primed by decorator.
        """
        total = 0.0
        count = 0

        while True:
            value = yield
            total += value
            count += 1
            average = total / count
            print(f"  Average: {average:.2f}")


    # No need to call next() - decorator does it
    avg = averaging_coroutine()
    avg.send(10)
    avg.send(20)
    avg.send(30)


    # Example 5.3: Coroutine pipeline
    print("\n--- Example 5.3: Coroutine Pipeline ---")


    @coroutine
    def printer():
        """Final stage: print values."""
        while True:
            value = yield
            print(f"  OUTPUT: {value}")


    @coroutine
    def multiplier(target, factor):
        """Middle stage: multiply by factor and send to target."""
        while True:
            value = yield
            target.send(value * factor)


    @coroutine
    def filter_positive(target):
        """Filter stage: only pass positive values."""
        while True:
            value = yield
            if value > 0:
                target.send(value)


    # Build the pipeline: filter -> multiply -> print
    print("Coroutine pipeline (filter -> multiply -> print):")
    print_stage = printer()
    multiply_stage = multiplier(print_stage, 2)
    filter_stage = filter_positive(multiply_stage)

    # Send values through the pipeline
    test_values = [1, -5, 3, -2, 7]
    for val in test_values:
        print(f"Sending: {val}")
        filter_stage.send(val)


    # Example 5.4: Broadcast coroutine
    print("\n--- Example 5.4: Broadcasting to Multiple Targets ---")


    @coroutine
    def broadcast(*targets):
        """
        Send received values to multiple target coroutines.

        Useful for splitting data streams.
        """
        while True:
            value = yield
            for target in targets:
                target.send(value)


    @coroutine
    def logger(name):
        """Log received values."""
        while True:
            value = yield
            print(f"  [{name}] Logged: {value}")


    @coroutine
    def accumulator(name):
        """Accumulate received values."""
        total = 0
        while True:
            value = yield
            total += value
            print(f"  [{name}] Total: {total}")


    # Set up broadcast to multiple targets
    print("Broadcasting to multiple coroutines:")
    log = logger("LOGGER")
    acc = accumulator("ACCUMULATOR")
    bcast = broadcast(log, acc)

    bcast.send(10)
    bcast.send(20)
    bcast.send(30)


    # ============================================================================
    # SECTION 6: ADVANCED PATTERNS AND OPTIMIZATION
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 6: ADVANCED PATTERNS")
    print("=" * 70)

    # Example 6.1: Generator state machine
    print("\n--- Example 6.1: State Machine with Generator ---")


    def state_machine():
        """
        Implement a state machine using generator.

        Demonstrates using generators for complex state management.
        """
        state = 'START'

        while True:
            if state == 'START':
                print("  State: START")
                command = yield "Ready"

                if command == 'begin':
                    state = 'PROCESSING'
                elif command == 'quit':
                    break

            elif state == 'PROCESSING':
                print("  State: PROCESSING")
                command = yield "Processing"

                if command == 'finish':
                    state = 'DONE'
                elif command == 'cancel':
                    state = 'START'

            elif state == 'DONE':
                print("  State: DONE")
                command = yield "Complete"

                if command == 'reset':
                    state = 'START'
                elif command == 'quit':
                    break

        print("  State machine stopped")


    # Using state machine
    print("State machine example:")
    sm = state_machine()
    print(next(sm))

    print(sm.send('begin'))
    print(sm.send('finish'))
    print(sm.send('reset'))
    print(sm.send('quit'))


    # Example 6.2: Memoization with generators
    print("\n--- Example 6.2: Memoized Generator ---")


    def memoized_fibonacci():
        """
        Fibonacci generator with memoization.

        Demonstrates optimization technique using cache.
        """
        cache = {0: 0, 1: 1}

        def fib(n):
            if n not in cache:
                cache[n] = fib(n-1) + fib(n-2)
            return cache[n]

        n = 0
        while True:
            yield fib(n)
            n += 1


    # Generate Fibonacci numbers efficiently
    print("Memoized Fibonacci (first 15):")
    fib_gen = memoized_fibonacci()
    for i in range(15):
        print(next(fib_gen), end=' ')
    print()


    # Example 6.3: Generator for tree traversal
    print("\n--- Example 6.3: Tree Traversal Generator ---")


    class TreeNode:
        """Simple tree node class."""

        def __init__(self, value, left=None, right=None):
            self.value = value
            self.left = left
            self.right = right


    def inorder_traversal(node):
        """
        Generator for in-order tree traversal.

        Demonstrates recursive generators for tree structures.
        """
        if node is not None:
            # Traverse left subtree
            yield from inorder_traversal(node.left)

            # Visit node
            yield node.value

            # Traverse right subtree
            yield from inorder_traversal(node.right)


    # Build a small tree
    #       4
    #      / \
    #     2   6
    #    / \ / \
    #   1  3 5  7
    root = TreeNode(4,
                    TreeNode(2, TreeNode(1), TreeNode(3)),
                    TreeNode(6, TreeNode(5), TreeNode(7)))

    print("In-order tree traversal:")
    for value in inorder_traversal(root):
        print(value, end=' ')
    print()


    # ============================================================================
    # SUMMARY AND KEY TAKEAWAYS
    # ============================================================================

    print("\n" + "=" * 70)
    print("SUMMARY: ADVANCED GENERATOR TECHNIQUES")
    print("=" * 70)

    print("""
    KEY CONCEPTS:

    1. GENERATOR.send(value):
       - Send values INTO a generator
       - yield can be used as expression
       - Enables bidirectional communication
       - Must prime generator first with next()

    2. GENERATOR.throw(exception):
       - Inject exceptions into generator
       - Generator can catch and handle
       - Useful for cancellation, errors
       - Can trigger cleanup or retry logic

    3. GENERATOR.close():
       - Terminate generator cleanly
       - Raises GeneratorExit
       - Use finally for cleanup
       - Essential for resource management

    4. YIELD FROM:
       - Delegate to sub-generator
       - Automatically forwards send/throw
       - Returns sub-generator result
       - Cleaner than manual forwarding
       - Essential for composition

    5. COROUTINES:
       - Generators as data consumers
       - Receive values via send()
       - Build processing pipelines
       - Use decorator for auto-priming

    6. ADVANCED PATTERNS:
       - State machines
       - Broadcasting
       - Memoization
       - Tree traversal
       - Pipeline composition

    BEST PRACTICES:

    1. Always prime coroutines before sending
    2. Use finally for cleanup
    3. Use yield from for delegation
    4. Close generators when done
    5. Handle GeneratorExit properly
    6. Don't yield after GeneratorExit
    7. Use decorators for common patterns

    COMMON PATTERNS:

    1. Request-Response:
       while True:
           request = yield response

    2. Pipeline:
       yield from filter(transform(source()))

    3. Broadcast:
       for target in targets:
           target.send(value)

    4. Cleanup:
       try:
           while True:
               yield value
       finally:
           cleanup()

    REMEMBER:
    - send() for bidirectional communication
    - throw() for exception injection
    - close() for cleanup
    - yield from for delegation
    - Coroutines for data processing
    - Always manage resources properly
    """)

    print("\n" + "=" * 70)
    print("END OF ADVANCED TUTORIAL")
    print("Next: See PRACTICAL APPLICATIONS of these techniques!")
    print("=" * 70)
```

---

## Exercises


**Exercise 1.**
Write a generator `flatten(nested)` that uses `yield from` to flatten a list of lists. For example, `list(flatten([[1,2],[3,4],[5]]))` should return `[1,2,3,4,5]`.

??? success "Solution to Exercise 1"

        ```python
        def flatten(nested):
            for sublist in nested:
                yield from sublist

        print(list(flatten([[1, 2], [3, 4], [5]])))
        # [1, 2, 3, 4, 5]
        ```

    `yield from sublist` delegates iteration to the sublist, yielding each element directly.

---

**Exercise 2.**
Write two generators: `evens(n)` yields even numbers up to `n`, and `odds(n)` yields odd numbers up to `n`. Then write a generator `all_numbers(n)` that uses `yield from` to combine both.

??? success "Solution to Exercise 2"

        ```python
        def evens(n):
            for i in range(0, n + 1, 2):
                yield i

        def odds(n):
            for i in range(1, n + 1, 2):
                yield i

        def all_numbers(n):
            yield from evens(n)
            yield from odds(n)

        print(list(all_numbers(6)))
        # [0, 2, 4, 6, 1, 3, 5]
        ```

    `yield from` delegates to each sub-generator in sequence.

---

**Exercise 3.**
Explain the difference between `yield from iterable` and looping with `for item in iterable: yield item`. Are they always equivalent?

??? success "Solution to Exercise 3"

    For simple iteration, they are equivalent:

        ```python
        # These produce identical output
        def gen1(iterable):
            yield from iterable

        def gen2(iterable):
            for item in iterable:
                yield item
        ```

    However, `yield from` also handles `.send()`, `.throw()`, and `.close()` by forwarding them to the sub-generator. The `for` loop version does not propagate these methods. For coroutine-style generators, `yield from` is essential.
