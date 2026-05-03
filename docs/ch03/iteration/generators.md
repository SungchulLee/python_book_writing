# Generators and `yield`

Generators provide a concise way to create iterators using the `yield` keyword. They are central to Python's lazy evaluation model.

!!! tip "Mental Model"
    A generator function is a function that can pause. Each `yield` freezes the function's state and hands a value to the caller; the next `next()` call thaws it and resumes right where it left off. This pause-and-resume mechanism produces values one at a time, keeping memory usage constant regardless of how many values are generated.

---

## Generator Functions

A function becomes a generator if it uses `yield`:

```python
def count_up(n):
    i = 0
    while i < n:
        yield i
        i += 1
```

Calling it returns a generator object (not the result):

```python
g = count_up(3)
print(type(g))  # <class 'generator'>
```

---

## Execution Model

Generator execution **pauses** at each `yield` and **resumes** on `next()`:

```python
def my_gen():
    print("Start")
    yield 1
    print("Middle")
    yield 2
    print("End")

g = my_gen()
print(next(g))  # Start → 1
print(next(g))  # Middle → 2
print(next(g))  # End → StopIteration
```

State (local variables, position) is preserved between yields.

---

## `yield` vs `return`

| Feature | `yield` | `return` |
|---------|---------|----------|
| Pauses execution | ✅ | ❌ (ends function) |
| Preserves state | ✅ | ❌ |
| Can be called multiple times | ✅ | ❌ |
| Creates generator | ✅ | ❌ |

```python
def with_yield():
    yield 1
    yield 2

def with_return():
    return 1
    return 2  # Never reached
```

---

## Generator Expressions

Similar to list comprehensions, but lazy:

```python
# List comprehension (eager)
squares_list = [x*x for x in range(10)]

# Generator expression (lazy)
squares_gen = (x*x for x in range(10))
```

Use parentheses `()` instead of brackets `[]`.

```python
g = (x**2 for x in range(5))
print(next(g))  # 0
print(next(g))  # 1
```

---

## Memory Efficiency

Generators compute values on demand, using minimal memory:

```python
import sys

# List stores all values
lst = [x for x in range(1000000)]
print(sys.getsizeof(lst))  # ~8 MB

# Generator stores only state
gen = (x for x in range(1000000))
print(sys.getsizeof(gen))  # ~200 bytes
```

---

## Memory Comparison

| Type | Memory | Stores All Values? |
|------|--------|-------------------|
| List comprehension | High | ✅ Yes |
| Generator expression | Very low | ❌ No |
| Generator function | Very low | ❌ No |
| Custom iterator | Low | ❌ No |

---

## Generator vs Iterator Class

**Generator** (concise):

```python
def squares(n):
    for i in range(n):
        yield i ** 2
```

**Iterator class** (verbose):

```python
class Squares:
    def __init__(self, n):
        self.n = n
        self.i = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        result = self.i ** 2
        self.i += 1
        return result
```

Both produce the same values, but generators require less code.

---

## When to Use Generators

- Processing large files line by line
- Infinite sequences
- Data pipelines
- When you don't need all values at once

```python
def read_large_file(path):
    with open(path) as f:
        for line in f:
            yield line.strip()
```

---

## Key Takeaways

- `yield` creates generators (pauses and resumes)
- Generators are lazy and memory-efficient
- Generator expressions use `()` syntax
- Essential for scalable data processing
- Generators are single-use (exhausted after iteration)

---

## Runnable Example: `generator_with_yield.py`

```python
"""
Generator Functions with yield - A Simpler Way to Create Iterators
This tutorial demonstrates how to use generator functions with yield
to create iterators with much less code than the iterator protocol.
Run this file to see generators in action!
"""

import re
import reprlib

if __name__ == "__main__":

    print("=" * 70)
    print("GENERATOR FUNCTIONS WITH YIELD - EXAMPLES")
    print("=" * 70)

    # ============================================================================
    # EXAMPLE 1: The Problem - Iterator Protocol is Verbose
    # ============================================================================
    print("\n1. THE PROBLEM - ITERATOR PROTOCOL IS VERBOSE")
    print("-" * 70)

    print("\nFrom the previous tutorial, we needed TWO classes:")
    print("- Sentence class with __iter__()")
    print("- SentenceIterator class with __iter__() and __next__()")
    print("\nThis is a lot of boilerplate code for something conceptually simple!")
    print("\nWhat if we could write iteration logic like a simple function?")

    # ============================================================================
    # EXAMPLE 2: Introduction to Generators and yield
    # ============================================================================
    print("\n2. INTRODUCTION TO GENERATORS AND YIELD")
    print("-" * 70)

    print("\nA generator function is a regular function that uses 'yield'")
    print("instead of 'return'.\n")

    print("When you call a generator function:")
    print("1. It returns a GENERATOR OBJECT (an iterator)")
    print("2. It doesn't execute the function body immediately")
    print("3. Each call to next() executes until the next yield")
    print("4. The function suspends at yield, remembering its state")
    print("5. The next call to next() resumes from where it stopped\n")

    print("This is MUCH simpler than implementing __iter__ and __next__!")

    # ============================================================================
    # EXAMPLE 3: Simple Generator Example
    # ============================================================================
    print("\n3. SIMPLE GENERATOR EXAMPLE")
    print("-" * 70)

    def simple_generator():
        """A simple generator to demonstrate yield."""
        print("  [Generator] Starting")
        yield 1
        print("  [Generator] After yield 1")
        yield 2
        print("  [Generator] After yield 2")
        yield 3
        print("  [Generator] After yield 3 (done)")

    print("\nDefined simple_generator():\n")

    gen = simple_generator()
    print(f"Called: gen = simple_generator()")
    print(f"Result: {gen}")
    print(f"Type: {type(gen)}\n")

    print("Notice: The function body hasn't executed yet!")
    print("The generator just sits there, waiting.\n")

    print("Now let's iterate:\n")
    for value in gen:
        print(f"Got: {value}")

    print("\nWHY THIS MATTERS:")
    print("- yield pauses execution and returns a value")
    print("- Execution resumes where it left off")
    print("- State is automatically saved!")

    # ============================================================================
    # EXAMPLE 4: The Sentence Class with yield
    # ============================================================================
    print("\n4. THE SENTENCE CLASS - SIMPLIFIED WITH YIELD")
    print("-" * 70)

    RE_WORD = re.compile(r'\w+')

    class Sentence:
        """
        A sequence of words extracted from a string.

        This version uses a generator function (with yield) instead of
        creating a separate iterator class. Much simpler!
        """

        def __init__(self, text):
            """Initialize with a text string."""
            self.text = text
            self.words = RE_WORD.findall(text)

        def __repr__(self):
            """Nice representation of the sentence."""
            return 'Sentence(%s)' % reprlib.repr(self.text)

        def __iter__(self):
            """
            Make Sentence iterable using a generator function.

            This is SO much simpler than creating a separate iterator class!
            Instead of managing state in __next__, we just yield each word.
            Python handles all the iteration logic for us.
            """
            for word in self.words:
                yield word

    print("\nDefined Sentence class with:")
    print("- __init__(text): Extract words from text")
    print("- __repr__(): Nice representation")
    print("- __iter__(): Generator function that yields words")
    print("\nCompare this to the previous version with SentenceIterator!")
    print("Much simpler, much clearer!\n")

    # ============================================================================
    # EXAMPLE 5: Using the Generator-Based Sentence
    # ============================================================================
    print("\n5. USING THE GENERATOR-BASED SENTENCE")
    print("-" * 70)

    text = 'To be, or not to be, that is the question'
    s = Sentence(text)

    print(f"\nCreated: s = Sentence('{text}')\n")

    print("Iterating with for loop:")
    print("-" * 40)

    for i, word in enumerate(s, 1):
        print(f"  Word {i}: {word}")

    print("\nWHY THIS WORKS:")
    print("- __iter__() returns a generator object")
    print("- for loop calls next() on the generator")
    print("- Each yield returns a word to the for loop")
    print("- When the loop in __iter__ ends, StopIteration is raised automatically")

    # ============================================================================
    # EXAMPLE 6: Generators are Lazy
    # ============================================================================
    print("\n6. GENERATORS ARE LAZY - MEMORY EFFICIENT")
    print("-" * 70)

    def count_up_to(n):
        """Generate numbers from 1 to n."""
        print(f"  [Generator] count_up_to({n}) starting")
        for i in range(1, n + 1):
            print(f"  [Generator] About to yield {i}")
            yield i
            print(f"  [Generator] Resumed after yield {i}")
        print(f"  [Generator] Finished")

    print("\nDefined count_up_to(n)\n")

    print("Creating: gen = count_up_to(3)")
    gen = count_up_to(3)
    print(f"Type: {type(gen)}\n")

    print("Notice: count_up_to(3) printed NOTHING!")
    print("The generator function body hasn't run yet.\n")

    print("Now iterating:\n")
    result = next(gen)
    print(f"First next() returned: {result}\n")

    result = next(gen)
    print(f"Second next() returned: {result}\n")

    result = next(gen)
    print(f"Third next() returned: {result}\n")

    print("This is LAZY EVALUATION:")
    print("- Values are computed only when requested")
    print("- Memory-efficient for large sequences")
    print("- Can even be infinite (with a while True loop)")

    # ============================================================================
    # EXAMPLE 7: Generator Expressions
    # ============================================================================
    print("\n7. GENERATOR EXPRESSIONS")
    print("-" * 70)

    print("\nYou can also create generators with expressions (like list comprehensions):")
    print("\nSyntax: (expression for item in iterable if condition)\n")

    squares = (x * x for x in range(10) if x % 2 == 0)
    print(f"Created: squares = (x*x for x in range(10) if x % 2 == 0)")
    print(f"Type: {type(squares)}\n")

    print("Note: Parentheses instead of square brackets!")
    print("This creates a generator, not a list.\n")

    print("Values:")
    for sq in squares:
        print(f"  {sq}")

    # Compare with list comprehension
    print("\nCompare with list comprehension:")
    squares_list = [x * x for x in range(10) if x % 2 == 0]
    print(f"List: {squares_list}")
    print(f"Type: {type(squares_list)}\n")

    print("Generator expression: Lazy, memory-efficient")
    print("List comprehension: Eager, all values in memory")

    # ============================================================================
    # EXAMPLE 8: Practical Example - Reading Large Files
    # ============================================================================
    print("\n8. PRACTICAL EXAMPLE - READING LINES EFFICIENTLY")
    print("-" * 70)

    def read_lines(filename):
        """
        Read a file line by line using a generator.

        This is more memory-efficient than reading the entire file
        with readlines() because it yields one line at a time.
        """
        with open(filename, 'r') as f:
            for line in f:
                yield line.rstrip('\n')  # Remove newline

    print("\nDefined read_lines(filename)")
    print("This reads a file line-by-line using a generator.\n")

    print("Why generators are perfect for this:")
    print("- You don't load the entire file into memory")
    print("- Works with files of any size")
    print("- Can process each line immediately")
    print("- Yields one line at a time on demand")

    # ============================================================================
    # EXAMPLE 9: Using iter() to Manually Control Generators
    # ============================================================================
    print("\n9. MANUALLY ITERATING WITH iter() AND next()")
    print("-" * 70)

    def countdown(n):
        """Count down from n to 1."""
        while n > 0:
            yield n
            n -= 1

    gen = countdown(5)
    print(f"Created: gen = countdown(5)\n")

    print("Using next() manually:")
    print(f"  next(gen) = {next(gen)}")
    print(f"  next(gen) = {next(gen)}")
    print(f"  next(gen) = {next(gen)}")

    print("\nContinue with for loop:")
    for val in gen:
        print(f"  {val}")

    print("\nYou can mix manual next() calls with for loops!")

    # ============================================================================
    # EXAMPLE 10: Comparing Approaches
    # ============================================================================
    print("\n10. COMPARING ITERATOR PROTOCOLS VS GENERATORS")
    print("-" * 70)

    print("""
    ITERATOR PROTOCOL (Previous Tutorial):
      - Must create a separate iterator class
      - Need to implement __iter__() and __next__()
      - Manual state management with instance variables
      - More boilerplate code
      + More control over iteration

    GENERATORS (This Tutorial):
      - Use 'yield' in a regular function
      - Python handles __iter__() and __next__() automatically
      - State is saved automatically between yields
      - Much less code, cleaner and more readable
      + Simpler, more Pythonic

    GENERATOR EXPRESSIONS:
      - Like list comprehensions but with parentheses
      - Even shorter syntax for simple cases
      + Most concise for simple iterations

    RECOMMENDATION:
    Use generators (yield) for most cases!
    The iterator protocol is great when you need more control.
    """)

    # ============================================================================
    # EXAMPLE 11: Key Insight - yield is Syntactic Sugar
    # ============================================================================
    print("\n" + "=" * 70)
    print("KEY INSIGHT - yield IS SYNTACTIC SUGAR")
    print("=" * 70)

    print("""
    When you write:

        def __iter__(self):
            for word in self.words:
                yield word

    Python automatically creates the iterator machinery for you!

    Equivalently, without yield:

        def __iter__(self):
            return SentenceIterator(self.words)

        class SentenceIterator:
            def __init__(self, words):
                self.words = words
                self.index = 0
            def __iter__(self):
                return self
            def __next__(self):
                try:
                    word = self.words[self.index]
                except IndexError:
                    raise StopIteration
                self.index += 1
                return word

    The generator version does exactly the same thing,
    but with a fraction of the code!

    GENERATORS ARE THE PYTHONIC WAY TO CREATE ITERATORS!
    """)
```


---

## Runnable Example: `intermediate_generators.py`

```python
"""
PYTHON GENERATORS & ITERATORS - INTERMEDIATE LEVEL
==================================================

Topic: Generator Functions and Expressions
-------------------------------------------

This module covers:
1. What are generators?
2. Generator functions and the yield keyword
3. Generator expressions
4. Lazy evaluation and memory efficiency
5. Generator state and execution flow
6. Practical use cases and patterns

Learning Objectives:
- Understand how generators simplify iterator creation
- Master the yield keyword and its behavior
- Write generator functions and expressions
- Apply lazy evaluation for memory efficiency
- Understand generator state management

Prerequisites:
- Completion of beginner iteration basics
- Understanding of iterators and the iteration protocol
- Basic Python functions and comprehensions
"""

import sys
import time

# ============================================================================
# SECTION 1: INTRODUCTION TO GENERATORS
# ============================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SECTION 1: WHAT ARE GENERATORS?")
    print("=" * 70)

    """
    GENERATOR: A simple way to create iterators

    Instead of creating a class with __iter__() and __next__() methods,
    we can use a generator function with the 'yield' keyword.

    Key advantages:
    - Much simpler syntax than iterator classes
    - Automatically implements iterator protocol
    - State is preserved automatically between yields
    - Memory efficient - values generated on-demand
    - More readable and maintainable code

    A generator is a special type of iterator that is created using:
    1. Generator functions (functions with yield)
    2. Generator expressions (like list comprehensions but with parentheses)
    """

    # Example 1.1: Simple generator function
    print("\n--- Example 1.1: First Generator Function ---")


    def simple_generator():
        """
        A basic generator function that yields three values.

        The 'yield' keyword makes this function a generator.
        Instead of returning once, it can yield multiple values.
        """
        print("  Yielding first value")
        yield 1
        print("  Yielding second value")
        yield 2
        print("  Yielding third value")
        yield 3
        print("  Generator complete")


    # When we call a generator function, it returns a generator object
    print("Calling simple_generator():")
    gen = simple_generator()
    print(f"Type: {type(gen)}")
    print(f"Is it an iterator? {hasattr(gen, '__next__')}")

    # Now iterate over it
    print("\nIterating over generator:")
    for value in gen:
        print(f"Received: {value}")


    # Example 1.2: Comparing class-based iterator with generator
    print("\n--- Example 1.2: Iterator vs Generator Comparison ---")


    # Old way: Class-based iterator
    class CounterIterator:
        """Traditional iterator class - requires more boilerplate code."""

        def __init__(self, start, end):
            self.current = start
            self.end = end

        def __iter__(self):
            return self

        def __next__(self):
            if self.current > self.end:
                raise StopIteration
            value = self.current
            self.current += 1
            return value


    # New way: Generator function
    def counter_generator(start, end):
        """
        Generator version - much simpler!

        No need to:
        - Create a class
        - Implement __iter__ and __next__
        - Manually raise StopIteration
        - Track state in instance variables
        """
        current = start
        while current <= end:
            yield current
            current += 1


    # Both produce the same result
    print("Class-based iterator:")
    for num in CounterIterator(1, 5):
        print(num, end=' ')
    print()

    print("\nGenerator function:")
    for num in counter_generator(1, 5):
        print(num, end=' ')
    print()


    # ============================================================================
    # SECTION 2: THE YIELD KEYWORD
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 2: UNDERSTANDING YIELD")
    print("=" * 70)

    """
    YIELD: The magic keyword that creates generators

    Key differences between 'return' and 'yield':

    RETURN:
    - Terminates function execution
    - Returns a single value
    - Function state is lost
    - Can only be called once

    YIELD:
    - Suspends function execution
    - Can yield multiple values
    - Function state is preserved
    - Can resume where it left off
    """

    # Example 2.1: How yield preserves state
    print("\n--- Example 2.1: Yield Preserves State ---")


    def demonstrate_state():
        """
        This generator demonstrates how state is preserved.

        Notice how local variables maintain their values
        between yield statements.
        """
        print("  Generator started")
        local_var = 0

        print(f"  Before first yield, local_var = {local_var}")
        yield local_var

        local_var += 10
        print(f"  Before second yield, local_var = {local_var}")
        yield local_var

        local_var += 10
        print(f"  Before third yield, local_var = {local_var}")
        yield local_var

        print("  Generator finished")


    gen = demonstrate_state()
    print("Calling next() three times:")
    print(f"First next(): {next(gen)}")
    print(f"Second next(): {next(gen)}")
    print(f"Third next(): {next(gen)}")


    # Example 2.2: Generator execution flow
    print("\n--- Example 2.2: Execution Flow ---")


    def execution_flow():
        """
        Demonstrates the execution flow of a generator.

        The function executes until it hits a yield, then pauses.
        It resumes from that exact point on the next next() call.
        """
        print("  Starting generator")

        for i in range(3):
            print(f"  About to yield {i}")
            yield i
            print(f"  Resumed after yielding {i}")

        print("  Generator ending")


    print("Creating and iterating generator:")
    for val in execution_flow():
        print(f"Main: received {val}")


    # Example 2.3: Multiple yields in different contexts
    print("\n--- Example 2.3: Yields in Different Contexts ---")


    def flexible_generator(n):
        """
        Generator with yields in different control structures.

        Yields can appear anywhere in the function:
        - In loops
        - In conditionals
        - Multiple times in sequence
        """
        # Yield in a sequence
        yield "Start"

        # Yields in a loop
        for i in range(n):
            if i % 2 == 0:
                yield f"Even: {i}"
            else:
                yield f"Odd: {i}"

        # Another yield after the loop
        yield "End"


    print("Generator with yields in different contexts:")
    for item in flexible_generator(4):
        print(item)


    # Example 2.4: Generator with conditional yielding
    print("\n--- Example 2.4: Conditional Yielding ---")


    def even_numbers(start, end):
        """
        Generator that yields only even numbers in range.

        Demonstrates that not every iteration needs to yield.
        """
        for num in range(start, end + 1):
            if num % 2 == 0:
                yield num


    print("Even numbers from 1 to 10:")
    for num in even_numbers(1, 10):
        print(num, end=' ')
    print()


    # ============================================================================
    # SECTION 3: GENERATOR EXPRESSIONS
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 3: GENERATOR EXPRESSIONS")
    print("=" * 70)

    """
    GENERATOR EXPRESSION: Compact syntax for creating generators

    Similar to list comprehensions but with parentheses instead of brackets.

    Syntax:
        (expression for item in iterable if condition)

    Key differences from list comprehensions:
    - Uses parentheses () instead of brackets []
    - Creates a generator (lazy) instead of a list (eager)
    - Memory efficient for large sequences
    - Can only be iterated once
    """

    # Example 3.1: List comprehension vs generator expression
    print("\n--- Example 3.1: List vs Generator Expression ---")

    # List comprehension - creates entire list in memory
    list_comp = [x ** 2 for x in range(5)]
    print(f"List comprehension: {list_comp}")
    print(f"Type: {type(list_comp)}")
    print(f"Size in memory: {sys.getsizeof(list_comp)} bytes")

    # Generator expression - creates generator object
    gen_exp = (x ** 2 for x in range(5))
    print(f"\nGenerator expression: {gen_exp}")
    print(f"Type: {type(gen_exp)}")
    print(f"Size in memory: {sys.getsizeof(gen_exp)} bytes")

    # Generator produces values on-demand
    print("\nIterating over generator:")
    for value in gen_exp:
        print(value, end=' ')
    print()


    # Example 3.2: Memory efficiency demonstration
    print("\n--- Example 3.2: Memory Efficiency ---")


    def compare_memory():
        """
        Compare memory usage of list comprehension vs generator expression.

        For large sequences, generators use constant memory
        while lists use memory proportional to sequence size.
        """
        n = 1000000

        # List comprehension - stores all values
        list_result = [x for x in range(n)]
        list_size = sys.getsizeof(list_result)

        # Generator expression - stores only the generator object
        gen_result = (x for x in range(n))
        gen_size = sys.getsizeof(gen_result)

        print(f"List of {n:,} items: {list_size:,} bytes")
        print(f"Generator for {n:,} items: {gen_size:,} bytes")
        print(f"Memory savings: {list_size / gen_size:.0f}x")


    compare_memory()


    # Example 3.3: Common generator expression patterns
    print("\n--- Example 3.3: Generator Expression Patterns ---")

    # Pattern 1: Filtering
    print("Even numbers from 0-9:")
    evens = (x for x in range(10) if x % 2 == 0)
    print(list(evens))  # Convert to list for display

    # Pattern 2: Transformation
    print("\nSquares of numbers:")
    squares = (x ** 2 for x in range(5))
    print(list(squares))

    # Pattern 3: Chaining operations
    print("\nSquares of even numbers:")
    result = (x ** 2 for x in range(10) if x % 2 == 0)
    print(list(result))

    # Pattern 4: Using with functions
    print("\nSum using generator expression:")
    total = sum(x ** 2 for x in range(10))
    print(total)

    # Pattern 5: Nested generator expressions
    print("\nFlattening a matrix:")
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = (num for row in matrix for num in row)
    print(list(flattened))


    # Example 3.4: When to use generator expressions
    print("\n--- Example 3.4: Generator Expression Use Cases ---")

    """
    Use generator expressions when:
    1. Working with large datasets
    2. Processing streaming data
    3. Only need to iterate once
    4. Want lazy evaluation
    5. Memory efficiency is important

    Use list comprehensions when:
    1. Need to iterate multiple times
    2. Need to access by index
    3. Need to know length
    4. Data set is small
    5. Need to modify the collection
    """

    # Good use: Large file processing (simulated)
    print("Processing large dataset efficiently:")
    large_dataset = range(1000000)
    # Generator expression doesn't create list in memory
    processed = (x * 2 for x in large_dataset if x % 2 == 0)
    # Only compute first 5 values
    print(f"First 5 values: {[next(processed) for _ in range(5)]}")


    # ============================================================================
    # SECTION 4: LAZY EVALUATION
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 4: LAZY EVALUATION")
    print("=" * 70)

    """
    LAZY EVALUATION: Computing values only when needed

    Benefits:
    1. Memory efficiency - don't store unnecessary data
    2. Performance - don't compute unused values
    3. Infinite sequences - can represent infinite series
    4. On-demand processing - compute as you consume
    """

    # Example 4.1: Lazy vs eager evaluation
    print("\n--- Example 4.1: Lazy vs Eager Evaluation ---")


    def expensive_operation(x):
        """
        Simulates an expensive computation.
        """
        print(f"  Computing expensive_operation({x})")
        time.sleep(0.1)  # Simulate delay
        return x ** 2


    # Eager evaluation - all computed immediately
    print("Eager evaluation (list comprehension):")
    start = time.time()
    eager = [expensive_operation(x) for x in range(5)]
    eager_time = time.time() - start
    print(f"List created in {eager_time:.2f}s")
    print(f"Using first 2: {eager[:2]}")

    # Lazy evaluation - computed on-demand
    print("\nLazy evaluation (generator expression):")
    start = time.time()
    lazy = (expensive_operation(x) for x in range(5))
    lazy_time = time.time() - start
    print(f"Generator created in {lazy_time:.4f}s (instant!)")
    print("Using first 2:")
    result = [next(lazy) for _ in range(2)]
    print(result)


    # Example 4.2: Infinite sequences
    print("\n--- Example 4.2: Infinite Sequences ---")


    def infinite_counter(start=0):
        """
        Generator for infinite sequence.

        This would be impossible with a list (infinite memory),
        but trivial with a generator.
        """
        count = start
        while True:  # Infinite loop!
            yield count
            count += 1


    def fibonacci():
        """
        Infinite Fibonacci sequence generator.

        Demonstrates lazy evaluation - we can have an infinite
        sequence but only compute what we need.
        """
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b


    # Use infinite generators with limits
    print("First 10 counting numbers:")
    counter = infinite_counter()
    for i, num in enumerate(counter):
        if i >= 10:
            break
        print(num, end=' ')
    print()

    print("\nFirst 10 Fibonacci numbers:")
    fib = fibonacci()
    for i, num in enumerate(fib):
        if i >= 10:
            break
        print(num, end=' ')
    print()


    # Example 4.3: Pipeline processing
    print("\n--- Example 4.3: Generator Pipelines ---")


    def read_data():
        """Simulate reading data from source."""
        data = ['1', '2', 'invalid', '3', '4', 'bad', '5']
        for item in data:
            print(f"  Reading: {item}")
            yield item


    def parse_data(data_gen):
        """Parse and filter data."""
        for item in data_gen:
            try:
                num = int(item)
                print(f"  Parsed: {num}")
                yield num
            except ValueError:
                print(f"  Skipping invalid: {item}")
                continue


    def transform_data(num_gen):
        """Transform the data."""
        for num in num_gen:
            result = num * 2
            print(f"  Transformed: {result}")
            yield result


    # Create processing pipeline
    print("Processing pipeline (lazy evaluation):")
    pipeline = transform_data(parse_data(read_data()))

    # Only processes when we consume
    print("\nConsuming first 3 items:")
    for i, value in enumerate(pipeline):
        if i >= 3:
            break
        print(f"Final: {value}\n")


    # ============================================================================
    # SECTION 5: PRACTICAL GENERATOR PATTERNS
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 5: PRACTICAL PATTERNS")
    print("=" * 70)

    # Example 5.1: Reading files efficiently
    print("\n--- Example 5.1: File Processing Pattern ---")


    def read_large_file(filename):
        """
        Generator for reading large files line by line.

        Memory efficient - doesn't load entire file into memory.
        Only one line in memory at a time.
        """
        with open(filename, 'r') as file:
            for line in file:
                yield line.strip()


    def process_log_file(filename):
        """
        Process log file and yield only error lines.

        Demonstrates filtering with generators.
        """
        for line in read_large_file(filename):
            if 'ERROR' in line:
                yield line


    print("File processing pattern defined (see code)")


    # Example 5.2: Batching data
    print("\n--- Example 5.2: Batching Pattern ---")


    def batch_data(iterable, batch_size):
        """
        Group data into batches.

        Useful for processing large datasets in chunks,
        e.g., batch API requests, database inserts.

        Args:
            iterable: Any iterable to batch
            batch_size: Number of items per batch

        Yields:
            Lists of batch_size items
        """
        batch = []
        for item in iterable:
            batch.append(item)
            if len(batch) == batch_size:
                yield batch
                batch = []

        # Don't forget remaining items
        if batch:
            yield batch


    # Example usage
    print("Batching numbers 1-10 into groups of 3:")
    for batch in batch_data(range(1, 11), 3):
        print(batch)


    # Example 5.3: Window/sliding view
    print("\n--- Example 5.3: Sliding Window Pattern ---")


    def sliding_window(iterable, window_size):
        """
        Create a sliding window over an iterable.

        Useful for:
        - Moving averages
        - Pattern matching
        - Sequence analysis

        Args:
            iterable: Sequence to window over
            window_size: Size of window

        Yields:
            Tuples of window_size elements
        """
        iterator = iter(iterable)

        # Initialize window
        window = []
        for _ in range(window_size):
            try:
                window.append(next(iterator))
            except StopIteration:
                return

        yield tuple(window)

        # Slide the window
        for item in iterator:
            window.pop(0)
            window.append(item)
            yield tuple(window)


    # Example usage
    print("Sliding window of size 3 over [1,2,3,4,5]:")
    for window in sliding_window([1, 2, 3, 4, 5], 3):
        print(window)


    # Example 5.4: Chaining generators
    print("\n--- Example 5.4: Chaining Generators ---")


    def first_n(gen, n):
        """Take first n items from generator."""
        for i, item in enumerate(gen):
            if i >= n:
                break
            yield item


    def filter_even(gen):
        """Filter even numbers from generator."""
        for item in gen:
            if item % 2 == 0:
                yield item


    def square(gen):
        """Square each number from generator."""
        for item in gen:
            yield item ** 2


    # Chain multiple generators
    print("Chaining: numbers -> filter even -> square -> first 5")
    numbers = range(20)
    result = first_n(square(filter_even(numbers)), 5)
    print(list(result))


    # Example 5.5: Generator with cleanup
    print("\n--- Example 5.5: Generator with Cleanup ---")


    def resource_generator():
        """
        Generator that manages resources properly.

        Demonstrates using try/finally for cleanup.
        """
        print("  Acquiring resource")
        resource = "resource_handle"

        try:
            for i in range(3):
                print(f"  Yielding {i}")
                yield i
        finally:
            print("  Releasing resource")
            # Cleanup code here


    # Normal iteration - cleanup happens
    print("Normal iteration:")
    for val in resource_generator():
        print(f"Got: {val}")

    # Early termination - cleanup still happens
    print("\nEarly termination with break:")
    for val in resource_generator():
        print(f"Got: {val}")
        if val == 1:
            break


    # ============================================================================
    # SECTION 6: PERFORMANCE CONSIDERATIONS
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 6: PERFORMANCE CONSIDERATIONS")
    print("=" * 70)

    # Example 6.1: When generators are faster
    print("\n--- Example 6.1: Performance Comparison ---")


    def performance_comparison():
        """
        Compare performance of different approaches.
        """
        n = 100000

        # Method 1: List comprehension
        start = time.time()
        result1 = sum([x ** 2 for x in range(n)])
        time1 = time.time() - start

        # Method 2: Generator expression
        start = time.time()
        result2 = sum(x ** 2 for x in range(n))
        time2 = time.time() - start

        # Method 3: Generator function
        def squares(n):
            for i in range(n):
                yield i ** 2

        start = time.time()
        result3 = sum(squares(n))
        time3 = time.time() - start

        print(f"List comprehension: {time1:.4f}s")
        print(f"Generator expression: {time2:.4f}s")
        print(f"Generator function: {time3:.4f}s")
        print(f"\nAll produce same result: {result1 == result2 == result3}")


    performance_comparison()


    # ============================================================================
    # SUMMARY AND KEY TAKEAWAYS
    # ============================================================================

    print("\n" + "=" * 70)
    print("SUMMARY: GENERATORS")
    print("=" * 70)

    print("""
    KEY CONCEPTS:

    1. GENERATOR FUNCTIONS:
       - Functions that use 'yield' keyword
       - Automatically create iterators
       - State preserved between yields
       - Much simpler than iterator classes

    2. GENERATOR EXPRESSIONS:
       - Syntax: (expression for item in iterable if condition)
       - Like list comprehensions but lazy
       - Memory efficient for large sequences
       - Can only iterate once

    3. YIELD KEYWORD:
       - Suspends function execution
       - Returns a value to caller
       - Resumes from same point on next call
       - Can yield multiple times

    4. LAZY EVALUATION:
       - Values computed on-demand
       - Memory efficient
       - Enables infinite sequences
       - Better performance for large datasets

    5. PRACTICAL PATTERNS:
       - File processing (line-by-line)
       - Data batching
       - Sliding windows
       - Generator pipelines
       - Resource management

    6. WHEN TO USE GENERATORS:
       - Large datasets
       - Streaming data
       - One-time iteration
       - Memory constraints
       - Complex iteration logic
       - Infinite sequences

    7. WHEN NOT TO USE:
       - Need random access
       - Multiple iterations
       - Need to know length
       - Small datasets where lists are fine

    REMEMBER:
    - Generators are iterators created easily
    - Use generators for memory efficiency
    - Generator expressions for simple cases
    - Generator functions for complex logic
    - Always use lazy evaluation when possible
    """)

    print("\n" + "=" * 70)
    print("END OF INTERMEDIATE TUTORIAL")
    print("Next: Learn about ADVANCED generator techniques!")
    print("=" * 70)
```

---

## Exercises


**Exercise 1.**
Write a generator function `fibonacci(n)` that yields the first `n` Fibonacci numbers. Test it by printing the first 10.

??? success "Solution to Exercise 1"

        ```python
        def fibonacci(n):
            a, b = 0, 1
            for _ in range(n):
                yield a
                a, b = b, a + b

        print(list(fibonacci(10)))
        # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        ```

    The generator yields one value at a time, keeping only `a` and `b` in memory regardless of `n`.

---

**Exercise 2.**
Write a generator function `chunks(lst, size)` that yields successive chunks of `size` elements from `lst`. For example, `list(chunks([1,2,3,4,5], 2))` should return `[[1,2], [3,4], [5]]`.

??? success "Solution to Exercise 2"

        ```python
        def chunks(lst, size):
            for i in range(0, len(lst), size):
                yield lst[i:i + size]

        print(list(chunks([1, 2, 3, 4, 5], 2)))
        # [[1, 2], [3, 4], [5]]
        ```

    `range(0, len(lst), size)` steps through the list in increments of `size`.

---

**Exercise 3.**
Explain the memory advantage of generators over lists. Write a comparison that shows `sum(range(10_000_000))` uses much less memory than `sum(list(range(10_000_000)))` using `sys.getsizeof`.

??? success "Solution to Exercise 3"

        ```python
        import sys

        r = range(10_000_000)
        l = list(range(10_000_000))

        print(f"range size: {sys.getsizeof(r)} bytes")     # ~48 bytes
        print(f"list size: {sys.getsizeof(l)} bytes")       # ~80,000,000 bytes

        # Both produce the same sum
        print(sum(range(10_000_000)) == sum(list(range(10_000_000))))  # True
        ```

    `range` (like a generator) produces values on demand, using constant memory. The list materializes all 10 million integers in memory.
