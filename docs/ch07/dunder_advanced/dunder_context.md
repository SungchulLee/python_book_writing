# Context Managers

Resource management is a recurring challenge in programming: files must be closed, locks must be released, and database connections must be returned to the pool — even when an exception interrupts normal flow. Python's `with` statement and the context manager protocol guarantee that cleanup code runs no matter what. Any object that implements `__enter__` and `__exit__` can be used with `with`.

## With Statement Support

### 1. The __enter__ Method

The `__enter__` method is called when execution enters the `with` block. It performs any setup work (opening a file, acquiring a lock) and returns the resource that will be bound to the variable after the `as` keyword. If no resource needs to be returned, it typically returns `self`.

### 2. The __exit__ Method

The `__exit__` method is called when execution leaves the `with` block, whether normally or because of an exception. It receives three arguments — `exc_type`, `exc_val`, and `exc_tb` — that describe the exception, or are all `None` if the block completed successfully. After performing cleanup, `__exit__` can suppress the exception by returning `True`, or let it propagate by returning `False` (or `None`).

### 3. Usage

The following class wraps a filename and ensures the underlying file handle is always closed, even if an error occurs inside the `with` block.

```python
class ManagedFile:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, "r")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        return False  # Do not suppress exceptions

with ManagedFile("example.txt") as f:
    contents = f.read()
# f is guaranteed to be closed here
```

When the `with` block begins, `__enter__` opens the file and returns the file handle. When the block ends — normally or via exception — `__exit__` closes the file.

## `with` vs `try/finally`

Context managers replace the `try/finally` pattern. Both guarantee cleanup, but `with` is shorter and harder to get wrong:

```python
# try/finally — correct but verbose
f = open("data.txt")
try:
    data = f.read()
finally:
    f.close()

# with — same guarantee, less code
with open("data.txt") as f:
    data = f.read()
```

As resource management grows more complex (nested resources, exception handling, conditional cleanup), `try/finally` becomes error-prone while `with` stays clean. Context managers also serve as a design pattern analogous to RAII (Resource Acquisition Is Initialization) in C++. See also [Callable Objects](dunder_callable.md), [Containers](dunder_containers.md), and [Iteration](dunder_iterables.md) for the other core protocols.

## Summary

- Context managers guarantee resource cleanup by pairing setup (`__enter__`) with teardown (`__exit__`).
- The `__exit__` method always runs, even when an exception occurs inside the `with` block.
- Prefer `with` over `try/finally` --- it is shorter, safer, and composable.
- Implement `__enter__` and `__exit__` on any class to make its instances usable with the `with` statement.

---

## Runnable Example: `context_manager_protocol.py`

```python
"""
TUTORIAL: Context Managers - The __enter__ and __exit__ Protocol

This tutorial teaches you how to implement the context manager protocol by
defining __enter__ and __exit__ methods. Context managers enable the 'with'
statement, which is Python's way of managing resource setup and cleanup
safely and reliably.

Real-world uses: file handling, database connections, locks, temporary
redirects, transaction management, and anything that needs setup/teardown.

Key Learning Goals:
  - Understand when and why context managers matter
  - Implement __enter__ and __exit__ properly
  - Handle exceptions in __exit__
  - See how the 'with' statement works under the hood
"""

import sys

if __name__ == "__main__":

    print("=" * 70)
    print("TUTORIAL: Context Managers - __enter__ and __exit__")
    print("=" * 70)

    # ============ EXAMPLE 1: The Problem Context Managers Solve ============
    print("\n# Example 1: Resource Cleanup Without Context Managers")
    print("=" * 70)

    print("""
    Imagine you have a resource that needs setup and teardown:

    WRONG WAY (without context manager):
        resource = acquire_resource()
        resource.do_work()
        resource.cleanup()  # Oops! What if do_work() raises an exception?
        # cleanup() never runs!

    SAFER WAY (manual try/finally):
        resource = acquire_resource()
        try:
            resource.do_work()
        finally:
            resource.cleanup()  # Always runs, even if exception occurs

    PYTHONIC WAY (context manager):
        with acquire_resource() as resource:
            resource.do_work()  # cleanup() automatically happens after

    The 'with' statement guarantees cleanup happens, even on exceptions.
    It's cleaner, safer, and more readable than try/finally.
    """)

    # ============ EXAMPLE 2: The Context Manager Protocol ============
    print("\n# Example 2: Understanding __enter__ and __exit__")
    print("=" * 70)

    print("""
    A context manager is any object with two dunder methods:

        class ContextManager:
            def __enter__(self):
                # Called when entering the with block
                # Setup goes here
                # Return a value (or None) to assign to 'as variable'
                return something

            def __exit__(self, exc_type, exc_value, traceback):
                # Called when exiting the with block (always!)
                # Cleanup goes here
                # If it returns True, the exception is suppressed
                # If it returns False or None, exception propagates
                return False  # Don't suppress exceptions

    When you write:
        with obj:
            # ... code ...

    Python does this:
        mgr = obj
        exit = type(mgr).__exit__
        value = type(mgr).__enter__(mgr)
        try:
            # ... code ...
        except:
            exc_info = sys.exc_info()
            if not exit(mgr, *exc_info):
                raise  # Exception propagates
        else:
            exit(mgr, None, None, None)  # Normal exit
    """)

    # ============ EXAMPLE 3: A Simple Example - Stdout Redirection ============
    print("\n# Example 3: The LookingGlass Context Manager")
    print("=" * 70)

    class LookingGlass:
        """
        A context manager that reverses stdout output (mirror effect).

        This is a playful example but demonstrates the protocol perfectly.
        While active, all print output is reversed - it appears backwards.
        """

        def __enter__(self):
            """
            Called when entering the with block.

            Tasks:
            1. Save the original sys.stdout.write method
            2. Replace it with our reverse_write method
            3. Return a value to be assigned to 'as variable'

            This is the setup phase.
            """
            # Save the original so we can restore it later
            self.original_write = sys.stdout.write

            # Replace with our custom function
            sys.stdout.write = self.reverse_write

            # Return a value for the 'as' variable
            return 'JABBERWOCKY'

        def reverse_write(self, text):
            """
            Our custom stdout.write that reverses text.

            This will be called by print() internally, so output appears
            backwards. We call the original write with reversed text.
            """
            self.original_write(text[::-1])

        def __exit__(self, exc_type, exc_value, traceback):
            """
            Called when exiting the with block (always!).

            Parameters:
                exc_type: Exception class if an exception occurred (None otherwise)
                exc_value: Exception instance if one occurred (None otherwise)
                traceback: Exception traceback if one occurred (None otherwise)

            Tasks:
            1. Restore the original stdout.write
            2. Optionally handle exceptions (return True to suppress)

            Return value:
                True: suppress the exception (don't re-raise)
                False/None: let exception propagate normally
            """
            # Always restore the original write method
            sys.stdout.write = self.original_write

            # Handle ZeroDivisionError specially
            if exc_type is ZeroDivisionError:
                print('Please DO NOT divide by zero!')
                return True  # Suppress this specific exception

            # All other exceptions propagate normally (implicit return None)


    # Demonstrate the context manager
    print("Before entering context manager:")
    print("This text is printed normally")
    print()

    print("Entering context manager with LookingGlass():")

    with LookingGlass() as what:
        print('Alice, Kitty and Snowdrop')
        print(f"The variable 'what' is: {what}")

    print()
    print("After exiting context manager:")
    print("Output is back to normal")

    print("""
    WHY: The context manager handles all the complexity for you.
    You don't have to remember try/finally or manual cleanup.
    The 'with' statement makes it impossible to forget.
    """)

    # ============ EXAMPLE 4: Understanding the Execution Order ============
    print("\n# Example 4: Step-by-Step Execution")
    print("=" * 70)

    class Tracer:
        """Context manager that logs when things happen."""

        def __enter__(self):
            print("  1. __enter__ called (setup phase)")
            return "Inside the with block"

        def __exit__(self, exc_type, exc_value, traceback):
            print("  3. __exit__ called (cleanup phase)")
            if exc_type is not None:
                print(f"     Exception occurred: {exc_type.__name__}")
            return False  # Don't suppress exceptions


    print("Normal execution:")
    with Tracer() as var:
        print(f"  2. Inside with block, var = {var}")

    print()
    print("Execution with exception:")
    try:
        with Tracer() as var:
            print(f"  2. Inside with block")
            x = 1 / 0  # Raise exception
    except ZeroDivisionError:
        print("  4. Exception propagated and caught by outer try/except")

    print("""
    KEY INSIGHT: __exit__ is ALWAYS called, whether the block completes
    normally or an exception occurs. This guarantee is what makes context
    managers so powerful for cleanup.
    """)

    # ============ EXAMPLE 5: Handling Exceptions ============
    print("\n# Example 5: Exception Handling in __exit__")
    print("=" * 70)

    class ErrorHandler:
        """
        Context manager that can suppress certain exceptions.

        Shows how returning True from __exit__ suppresses exceptions.
        """

        def __init__(self, exception_type):
            self.exception_type = exception_type

        def __enter__(self):
            print(f"  __enter__: Will suppress {self.exception_type.__name__}")
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            if exc_type is None:
                print("  __exit__: Normal exit (no exception)")
                return False
            elif exc_type is self.exception_type:
                print(f"  __exit__: Caught {exc_type.__name__} - suppressing it")
                return True  # Suppress this exception
            else:
                print(f"  __exit__: Caught {exc_type.__name__} - NOT suppressing")
                return False  # Don't suppress


    print("Suppressing ValueError:")
    with ErrorHandler(ValueError):
        print("  Inside block, raising ValueError")
        raise ValueError("This will be suppressed")
    print("  Block exited - exception was suppressed!")
    print()

    print("NOT suppressing TypeError:")
    try:
        with ErrorHandler(ValueError):
            print("  Inside block, raising TypeError")
            raise TypeError("This will NOT be suppressed")
    except TypeError:
        print("  Block exited - exception propagated and caught!")

    print("""
    WHY: Some context managers (like pytest fixtures) suppress expected
    exceptions. Returning True says "I handled this, don't propagate."
    Returning False or None says "I didn't handle this, propagate it."

    Most context managers return None or False - they don't suppress.
    """)

    # ============ EXAMPLE 6: Real-World Example - File Handling ============
    print("\n# Example 6: File Handling (Real-World Context Manager)")
    print("=" * 70)

    class ManagedFile:
        """
        A context manager for file operations.

        This demonstrates why context managers matter in real code:
        files need to be opened and closed reliably.
        """

        def __init__(self, name, mode):
            self.name = name
            self.mode = mode
            self.file = None

        def __enter__(self):
            print(f"  __enter__: Opening file '{self.name}'")
            self.file = open(self.name, self.mode)
            return self.file

        def __exit__(self, exc_type, exc_value, traceback):
            if self.file:
                print(f"  __exit__: Closing file '{self.name}'")
                self.file.close()
            if exc_type is not None:
                print(f"  __exit__: Exception occurred: {exc_type.__name__}")
            return False


    # Demonstrate file handling
    print("Writing to a file:")
    with ManagedFile('/tmp/test.txt', 'w') as f:
        f.write("Hello, World!\n")
        f.write("This is a test file.\n")

    print()
    print("Reading from the file:")
    with ManagedFile('/tmp/test.txt', 'r') as f:
        for line in f:
            print(f"  Read: {line.rstrip()}")

    print()
    print("File closed automatically after each with block!")

    print("""
    WHY: Built-in file objects already implement the context manager protocol,
    so you can use:
        with open('file.txt') as f:
            # ...

    This is so common that it's the Pythonic way to open files. Files are
    automatically closed when exiting the with block, even if an exception
    occurs.
    """)

    # ============ EXAMPLE 7: Multiple Resources ============
    print("\n# Example 7: Managing Multiple Resources")
    print("=" * 70)

    class Resource:
        """Simulates a resource that needs cleanup."""

        def __init__(self, name):
            self.name = name

        def __enter__(self):
            print(f"  Acquired {self.name}")
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            print(f"  Released {self.name}")
            return False

        def use(self):
            print(f"  Using {self.name}")


    print("Managing multiple resources with nested with statements:")
    with Resource("Resource A") as a:
        with Resource("Resource B") as b:
            with Resource("Resource C") as c:
                a.use()
                b.use()
                c.use()

    print()
    print("More readable: use comma syntax (Python 3.10+):")
    print("""
        with Resource("A") as a, \\
             Resource("B") as b, \\
             Resource("C") as c:
            a.use()
            b.use()
            c.use()

    Resources are acquired and released in the correct order (LIFO - Last In,
    First Out). C is released first, then B, then A.
    """)

    # ============ EXAMPLE 8: The Complete Pattern ============
    print("\n# Example 8: Context Manager Checklist")
    print("=" * 70)

    print("""
    When implementing a context manager, follow this pattern:

    class MyContextManager:
        def __init__(self, ...):
            # Store initialization parameters
            self.resource = None

        def __enter__(self):
            # 1. Acquire resource
            self.resource = acquire_resource()
            # 2. Perform any setup
            self.resource.setup()
            # 3. Return a value for 'as variable' (or self)
            return self.resource

        def __exit__(self, exc_type, exc_value, traceback):
            # 1. Always clean up resources
            if self.resource:
                self.resource.cleanup()

            # 2. Optional: handle specific exceptions
            if exc_type is SomeException:
                # Handle it
                return True  # Suppress

            # 3. Return False/None to propagate exceptions
            return False

    USAGE:
        with MyContextManager(...) as resource:
            resource.do_something()
        # Cleanup guaranteed to happen here

    KEY RULES:
        - __enter__ runs when entering the with block
        - __exit__ ALWAYS runs when exiting (normal or exception)
        - __exit__ receives exception info (or None, None, None if normal)
        - Return True to suppress exception, False/None to propagate
        - Use __exit__ for cleanup, not for normal work
    """)

    # ============ EXAMPLE 9: Common Pattern - Lock Management ============
    print("\n# Example 9: Lock Management (Concurrency Pattern)")
    print("=" * 70)

    class SimpleLock:
        """Context manager for thread synchronization."""

        def __init__(self, name):
            self.name = name
            self.acquired = False

        def __enter__(self):
            print(f"  Acquiring lock: {self.name}")
            self.acquired = True
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            if self.acquired:
                print(f"  Releasing lock: {self.name}")
                self.acquired = False


    print("Lock acquisition and release:")
    with SimpleLock("data_lock"):
        print("  Critical section protected by lock")
        print("  Can safely access shared data")
    print("  Lock automatically released")

    print("""
    WHY: Context managers are essential for thread-safe code. Locks are
    acquired on __enter__ and released on __exit__, even if exceptions occur.
    This prevents deadlocks and data corruption.

    This pattern is used in threading.Lock, threading.RLock, and many
    concurrency libraries.
    """)

    # ============ EXAMPLE 10: Summary ============
    print("\n# Example 10: When to Use Context Managers")
    print("=" * 70)

    print("""
    USE CONTEXT MANAGERS FOR:
        1. File operations (open, read, write, close)
        2. Database transactions (begin, commit, rollback)
        3. Network connections (connect, disconnect)
        4. Thread locks (acquire, release)
        5. Temporary state changes (redirect stdout, change directory)
        6. Resource pooling (acquire from pool, return to pool)
        7. Timing operations (start timer, stop and report)
        8. Error suppression (catch specific exceptions)

    PATTERN CHECKLIST:
        ✓ __enter__ acquires resources and returns them
        ✓ __exit__ releases resources (cleanup)
        ✓ __exit__ always runs, even on exceptions
        ✓ Suppressing exceptions is optional (usually don't)
        ✓ Use 'with' statement (never call __enter__/__exit__ directly)
        ✓ Can stack multiple with statements for multiple resources

    BENEFITS:
        ✓ Guaranteed cleanup (no forgotten cleanup calls)
        ✓ Clean, readable code
        ✓ Exception-safe
        ✓ Clear intent (anyone sees 'with' knows resource is managed)
        ✓ Pythonic (idiomatic Python style)

    NEXT: If you find context managers verbose, learn about @contextmanager
    decorator in the next tutorial - it simplifies many common cases!
    """)

    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)
    print("""
    1. CONTEXT MANAGERS ARE FOR RESOURCE MANAGEMENT: Use them whenever
       something needs setup and cleanup (files, locks, transactions, etc).

    2. __enter__ AND __exit__ ARE THE PROTOCOL: Implement these two methods
       and any object becomes a context manager usable with 'with'.

    3. __exit__ IS GUARANTEED TO RUN: This is what makes context managers
       so powerful - cleanup is guaranteed even if exceptions occur.

    4. RETURN VALUE MATTERS: Return True to suppress exceptions, False/None
       to propagate them. Most context managers propagate.

    5. WITH STATEMENT IS CLEANER: 'with' is more readable and safer than
       manual try/finally. Always prefer 'with' when possible.

    6. USE THE PROTOCOL EVERYWHERE APPLICABLE: Any resource that needs
       cleanup should be managed through a context manager. It's a sign
       of professional Python code.

    7. YOU'RE PROBABLY ALREADY USING THEM: File objects, database
       connections, and many libraries use context managers. Now you can
       build your own!
    """)
```


---

## Runnable Example: `context_manager_decorator.py`

```python
"""
TUTORIAL: The @contextmanager Decorator - Simpler Context Managers

This tutorial teaches you how to use @contextmanager decorator from the
contextlib module. Instead of writing classes with __enter__ and __exit__
methods, you can write a simple generator function that's much more concise.

This is the Pythonic way to create context managers when you don't need
the full power of a class.

Key Learning Goals:
  - Understand how @contextmanager transforms generators into context managers
  - Write context managers as functions instead of classes
  - Learn when to use decorator vs class approach
  - Master the yield pattern for setup/teardown
"""

import contextlib
import sys

if __name__ == "__main__":

    print("=" * 70)
    print("TUTORIAL: @contextmanager Decorator - Simpler Context Managers")
    print("=" * 70)

    # ============ EXAMPLE 1: Why the Decorator Exists ============
    print("\n# Example 1: Class vs Function Approaches")
    print("=" * 70)

    print("""
    REMINDER: Context managers can be classes:

        class LookingGlass:
            def __enter__(self):
                self.original = sys.stdout.write
                sys.stdout.write = self.reverse_write
                return 'JABBERWOCKY'

            def reverse_write(self, text):
                self.original(text[::-1])

            def __exit__(self, exc_type, exc_value, traceback):
                sys.stdout.write = self.original
                return False

    This is verbose and has a lot of boilerplate. If your context manager
    just does setup (before), then cleanup (after), there's a simpler way.

    WITH @contextmanager:

        @contextlib.contextmanager
        def looking_glass():
            original = sys.stdout.write
            sys.stdout.write = lambda text: original(text[::-1])
            try:
                yield 'JABBERWOCKY'
            finally:
                sys.stdout.write = original

    Much more concise! The decorator handles __enter__ and __exit__ for you.
    """)

    # ============ EXAMPLE 2: Basic @contextmanager Usage ============
    print("\n# Example 2: Your First @contextmanager")
    print("=" * 70)

    @contextlib.contextmanager
    def simple_context():
        """
        A simple context manager using the decorator.

        The pattern:
        1. Do setup before yield
        2. Yield a value to return from __enter__
        3. Do cleanup after yield (in finally block)

        The decorator automatically:
        - Wraps the yield value in a context manager
        - Runs code before yield in __enter__
        - Runs code after yield in __exit__
        - Handles exceptions properly
        """
        print("  Entering context (setup)")
        yield "setup complete"
        print("  Exiting context (cleanup)")


    print("Using the context manager:")
    with simple_context() as value:
        print(f"  Inside with block, value = {value}")

    print()
    print("Notice how clean this is:")
    print("  - No class definition needed")
    print("  - No __enter__ and __exit__ methods")
    print("  - Setup and cleanup are adjacent in the code")
    print("""
    WHY: For simple setup/cleanup patterns, the decorator is more readable.
    The yield statement clearly marks what gets returned and when cleanup happens.
    """)

    # ============ EXAMPLE 3: The LookingGlass with Decorator ============
    print("\n# Example 3: LookingGlass Revisited (Much Simpler)")
    print("=" * 70)

    @contextlib.contextmanager
    def looking_glass():
        """
        Reverse stdout output using the decorator.

        Compare this to the class version in the previous tutorial.
        This is so much simpler!

        HOW IT WORKS:
        1. Save original sys.stdout.write
        2. Yield the magic word to be returned by __enter__
        3. In finally block, restore the original write
        4. Everything between yield and end of function runs in __exit__
        """
        original_write = sys.stdout.write

        def reverse_write(text):
            original_write(text[::-1])

        sys.stdout.write = reverse_write
        try:
            yield 'JABBERWOCKY'  # This value is returned by __enter__
        finally:
            sys.stdout.write = original_write  # Always runs in __exit__


    print("Before context:")
    print("Normal output here")
    print()

    with looking_glass() as word:
        print('Alice, Kitty and Snowdrop')
        print(f"The magic word: {word}")

    print()
    print("After context:")
    print("Back to normal output")

    print("""
    WHY: The try/finally ensures cleanup happens even if an exception occurs
    inside the with block. The decorator handles all the __enter__/__exit__
    machinery for you.
    """)

    # ============ EXAMPLE 4: Yielding None ============
    print("\n# Example 4: Yielding None (No Return Value)")
    print("=" * 70)

    @contextlib.contextmanager
    def timed_operation(operation_name):
        """
        Context manager that measures execution time.

        Sometimes you don't yield a value - you just yield None or nothing.
        The context manager still works; 'as variable' will be None.
        """
        import time
        start_time = time.time()
        print(f"  Starting {operation_name}")
        try:
            yield  # No value returned
        finally:
            elapsed = time.time() - start_time
            print(f"  Finished {operation_name} in {elapsed:.4f} seconds")


    print("Measuring operation time:")
    with timed_operation("file read"):
        # Simulate work
        data = sum(range(1000000))

    print()
    print("Another operation:")
    with timed_operation("file write"):
        # Simulate work
        temp = [x for x in range(100000)]

    print("""
    WHY: Not all context managers need to return a value. Sometimes they just
    manage state or timing. Yielding None (or nothing) is perfectly valid.
    """)

    # ============ EXAMPLE 5: Exception Handling ============
    print("\n# Example 5: Handling Exceptions in Decorated Generators")
    print("=" * 70)

    @contextlib.contextmanager
    def error_handler(exception_type):
        """
        A decorator-based context manager that can suppress exceptions.

        The key insight: exceptions raised in the with block propagate to
        the code after yield. You can catch them with try/except.
        """
        print(f"  Entering (will handle {exception_type.__name__})")
        try:
            yield
        except exception_type as e:
            print(f"  Caught and suppressed: {exception_type.__name__}")
            # Exception is suppressed by not re-raising
        except Exception as e:
            print(f"  Caught but re-raising: {type(e).__name__}")
            raise
        finally:
            print(f"  Always cleaning up")


    print("Suppressing ValueError:")
    with error_handler(ValueError):
        print("  Doing work...")
        raise ValueError("Something went wrong")
    print("  After with block (exception was suppressed)")
    print()

    print("Not suppressing TypeError:")
    try:
        with error_handler(ValueError):
            print("  Doing work...")
            raise TypeError("Wrong type!")
    except TypeError:
        print("  After with block (exception propagated)")

    print("""
    WHY: Decorated generators let you handle exceptions elegantly.
    - Don't re-raise to suppress
    - Re-raise to propagate
    - finally block always runs (cleanup guaranteed)
    """)

    # ============ EXAMPLE 6: Resource Management Pattern ============
    print("\n# Example 6: Database-Like Resource Management")
    print("=" * 70)

    class FakeDatabase:
        """Simulates a database connection."""

        def __init__(self, name):
            self.name = name
            self.is_open = False

        def open(self):
            self.is_open = True
            print(f"    Database '{self.name}' opened")

        def close(self):
            self.is_open = False
            print(f"    Database '{self.name}' closed")

        def query(self, sql):
            if not self.is_open:
                raise RuntimeError("Database is closed")
            return f"Results of: {sql}"


    @contextlib.contextmanager
    def database_session(db_name):
        """
        Context manager for database operations.

        Pattern: open connection, yield it, close on exit.
        This is how many real database libraries work.
        """
        db = FakeDatabase(db_name)
        db.open()
        try:
            yield db
        finally:
            db.close()


    print("Using database context manager:")
    with database_session("mydb") as db:
        print(f"  Database open: {db.is_open}")
        result = db.query("SELECT * FROM users")
        print(f"  Query result: {result}")

    print(f"  After with block: {db.is_open}")

    print()
    print("Exception handling in database context:")
    try:
        with database_session("tempdb") as db:
            print(f"  Database open: {db.is_open}")
            # Simulate error
            raise ValueError("Invalid query")
    except ValueError:
        print("  Exception propagated and caught")
        print(f"  Database closed during exception: {db.is_open}")

    print("""
    WHY: Real libraries (SQLAlchemy, psycopg2, etc.) use this pattern.
    The decorator makes it simple to write context managers that acquire
    and release resources safely.
    """)

    # ============ EXAMPLE 7: Complex Setup and Teardown ============
    print("\n# Example 7: Multi-Step Setup and Cleanup")
    print("=" * 70)

    @contextlib.contextmanager
    def multi_step_context():
        """
        Context manager with multiple setup/teardown steps.

        Even complex operations stay clean with the decorator.
        """
        print("  Step 1: Initialize resources")
        resource1 = "resource_1"

        print("  Step 2: Configure resource")
        resource2 = "resource_2"

        print("  Step 3: Open connections")
        print("  SETUP COMPLETE")

        try:
            yield (resource1, resource2)
        finally:
            print("  Step 1: Close connections")
            print("  Step 2: Save state")
            print("  Step 3: Release resources")
            print("  CLEANUP COMPLETE")


    print("Multi-step context manager:")
    with multi_step_context() as (r1, r2):
        print(f"  Working with {r1} and {r2}")

    print("""
    WHY: Complex initialization and cleanup is still readable with decorators.
    The setup code is grouped at the top, cleanup at the bottom (in finally).
    """)

    # ============ EXAMPLE 8: Nesting and Composition ============
    print("\n# Example 8: Combining Multiple Context Managers")
    print("=" * 70)

    @contextlib.contextmanager
    def lock_context(name):
        """Simulates acquiring and releasing a lock."""
        print(f"  Acquired lock: {name}")
        try:
            yield
        finally:
            print(f"  Released lock: {name}")


    @contextlib.contextmanager
    def transaction_context():
        """Simulates a database transaction."""
        print("  BEGIN TRANSACTION")
        try:
            yield
        finally:
            print("  COMMIT TRANSACTION")


    print("Combining context managers with nesting:")
    with lock_context("data_lock"):
        with transaction_context():
            print("  Executing operations under lock and transaction")

    print()
    print("Cleaner syntax with multiple contexts (Python 3.10+):")
    print("""
        with lock_context("lock"), transaction_context():
            # operations here
    """)

    print("""
    WHY: Context managers compose well. You can nest them when you need
    multiple resources, or use comma syntax for cleaner code.
    """)

    # ============ EXAMPLE 9: When to Use Decorator vs Class ============
    print("\n# Example 9: Decorator vs Class - When to Use Each")
    print("=" * 70)

    print("""
    USE @contextmanager (DECORATOR) WHEN:
        ✓ Simple setup/cleanup pattern
        ✓ Just need to yield a value once
        ✓ Logic is straightforward
        ✓ Less than ~50 lines of code

    EXAMPLE: File cleanup, timing, simple redirects, database transactions

        @contextlib.contextmanager
        def simple():
            setup()
            try:
                yield value
            finally:
                cleanup()


    USE A CLASS WHEN:
        ✓ Need complex initialization
        ✓ Need multiple methods
        ✓ State management is complex
        ✓ Need to support multiple protocols (__enter__, __exit__, and others)
        ✓ Plan to reuse in multiple contexts

    EXAMPLE: Database connection pool, transaction with savepoints, API wrapper

        class ComplexManager:
            def __init__(self, ...):
                # Complex init
            def __enter__(self):
                # Setup
            def __exit__(self, ...):
                # Cleanup
            def helper_method(self):
                # Additional methods

    RULE OF THUMB: Start with @contextmanager. If you find yourself adding
    complexity, convert to a class. The decorator is for simple cases.
    """)

    # ============ EXAMPLE 10: Real-World Example - Temporary Directory ============
    print("\n# Example 10: Real-World Example - Temporary File Management")
    print("=" * 70)

    import tempfile
    import os

    @contextlib.contextmanager
    def temporary_directory():
        """
        Context manager for temporary directory.

        This shows a realistic use case: manage a temporary resource
        that needs cleanup.
        """
        tmpdir = tempfile.mkdtemp()
        print(f"  Created temporary directory: {tmpdir}")
        try:
            yield tmpdir
        finally:
            # Clean up
            if os.path.exists(tmpdir):
                print(f"  Removing temporary directory: {tmpdir}")
                # In real code: shutil.rmtree(tmpdir)
                # Here we just print it


    print("Using temporary directory:")
    with temporary_directory() as tmpdir:
        print(f"  Working in {tmpdir}")
        # Create files, do work, etc.
        print(f"  Directory exists: {os.path.exists(tmpdir)}")

    print(f"  Directory cleaned up after with block")

    print("""
    WHY: Real libraries (tempfile, sqlite3, requests, etc.) use decorated
    context managers extensively. This pattern is idiomatic Python.

    REAL-WORLD USAGE:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create files, do work
        # tmpdir automatically cleaned up

        with requests.Session() as session:
            response = session.get(url)
        # Connection automatically closed

        with open('file.txt') as f:
            data = f.read()
        # File automatically closed
    """)

    # ============ EXAMPLE 11: Summary and Comparison ============
    print("\n# Example 11: Summary - Class vs Decorator")
    print("=" * 70)

    print("""
    CONTEXT MANAGER AS CLASS:

        class ManagedResource:
            def __init__(self, name):
                self.name = name

            def __enter__(self):
                print(f"Opening {self.name}")
                return self

            def __exit__(self, exc_type, exc_value, traceback):
                print(f"Closing {self.name}")
                return False

        with ManagedResource("file") as res:
            # use res

    SAME CONTEXT MANAGER WITH DECORATOR:

        @contextlib.contextmanager
        def managed_resource(name):
            print(f"Opening {name}")
            try:
                yield type('Resource', (), {'name': name})()
            finally:
                print(f"Closing {name}")

        with managed_resource("file") as res:
            # use res

    The decorator is simpler for straightforward cases. The class is better
    for complex logic.
    """)

    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)
    print("""
    1. @contextmanager TURNS GENERATORS INTO CONTEXT MANAGERS: Decorate a
       generator function and it becomes usable with 'with' statements.

    2. THE YIELD PATTERN IS CLEAR: Code before yield = __enter__,
       code after yield = __exit__. Very readable!

    3. try/finally ENSURES CLEANUP: Always use try/finally around yield
       to guarantee cleanup happens, even on exceptions.

    4. DECORATOR SIMPLIFIES COMMON CASE: For simple setup/cleanup patterns,
       the decorator is far less verbose than a class.

    5. EXCEPTION HANDLING WORKS NATURALLY: Exceptions in the with block
       propagate to the code after yield. Catch them with try/except.

    6. YIELD NOTHING FOR SIDE-EFFECT MANAGERS: Not all context managers
       return values. Some just manage state (timing, locks, transactions).

    7. CHOOSE BASED ON COMPLEXITY: Decorator for simple cases, class for
       complex cases. Start with the decorator, convert to class if needed.

    8. STANDARD LIBRARIES USE THIS: Many real libraries use @contextmanager.
       Understanding it helps you read and use library code confidently.

    NEXT: Explore advanced patterns like ExitStack for managing multiple
    contexts dynamically, or write your own context managers for domain
    -specific resources (database transactions, API sessions, etc.).
    """)
```

---

## Exercises

**Exercise 1.**
Create a `Timer` context manager that measures elapsed time. `__enter__` records the start time and returns `self`. `__exit__` computes the elapsed time and stores it in `self.elapsed`. Demonstrate with a `with` block that sleeps briefly, then print the elapsed time.

??? success "Solution to Exercise 1"

        import time

        class Timer:
            def __enter__(self):
                self.start = time.time()
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.elapsed = time.time() - self.start
                return False

        with Timer() as t:
            time.sleep(0.1)

        print(f"Elapsed: {t.elapsed:.3f}s")  # ~0.100s

---

**Exercise 2.**
Write an `Indenter` context manager that tracks indentation level. Each nested `with Indenter()` block increases the indent level. Provide a `print(text)` method that prints text with the current indentation. Show nested usage producing indented output.

??? success "Solution to Exercise 2"

        class Indenter:
            _level = 0

            def __enter__(self):
                Indenter._level += 1
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                Indenter._level -= 1
                return False

            def print(self, text):
                print("    " * Indenter._level + text)

        with Indenter() as i1:
            i1.print("Level 1")
            with Indenter() as i2:
                i2.print("Level 2")
                with Indenter() as i3:
                    i3.print("Level 3")
            i1.print("Back to level 1")
        #     Level 1
        #         Level 2
        #             Level 3
        #     Back to level 1

---

**Exercise 3.**
Build a `Transaction` context manager for a simple in-memory database (a dictionary). `__enter__` saves a snapshot of the data. If the block completes without exception, changes are kept. If an exception occurs, `__exit__` rolls back to the snapshot. Demonstrate both successful and rolled-back transactions.

??? success "Solution to Exercise 3"

        class Transaction:
            def __init__(self, database):
                self.database = database

            def __enter__(self):
                self._snapshot = dict(self.database)
                return self.database

            def __exit__(self, exc_type, exc_val, exc_tb):
                if exc_type is not None:
                    self.database.clear()
                    self.database.update(self._snapshot)
                    print("Transaction rolled back")
                    return True  # Suppress exception
                print("Transaction committed")
                return False

        db = {"name": "Alice", "balance": 100}

        # Successful transaction
        with Transaction(db) as data:
            data["balance"] = 200

        print(db)  # {'name': 'Alice', 'balance': 200}

        # Failed transaction
        with Transaction(db) as data:
            data["balance"] = 9999
            raise ValueError("Something went wrong")

        print(db)  # {'name': 'Alice', 'balance': 200} — rolled back
