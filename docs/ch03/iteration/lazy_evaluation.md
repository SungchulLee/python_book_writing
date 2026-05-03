# Lazy Evaluation Patterns

Lazy evaluation defers computation until values are actually needed. Generators and iterators enable lazy evaluation, reducing memory usage and enabling infinite sequences.

!!! tip "Mental Model"
    Lazy evaluation is "pay as you go" -- no value is computed until something asks for it. A generator sitting idle consumes no CPU; it only does work when you call `next()`. This means you can define an infinite sequence and safely consume just the first ten items, because the rest are never computed.

---

## Generator Laziness

### Computation on Demand

```python
def lazy_range(n):
    print("Starting generator")
    for i in range(n):
        print(f"Computing {i}")
        yield i

gen = lazy_range(3)
print("Generator created (nothing computed)")
print(next(gen))
print(next(gen))
```

Output:
```
Generator created (nothing computed)
Starting generator
Computing 0
0
Computing 1
1
```

### Memory Efficiency

```python
# List - all values in memory
nums_list = [x**2 for x in range(1000000)]
print(f"List uses memory for 1M items")

# Generator - one value at a time
nums_gen = (x**2 for x in range(1000000))
print(f"Generator created (lazy)")
print(next(nums_gen))
```

Output:
```
List uses memory for 1M items
Generator created (lazy)
0
```

## Infinite Sequences

### Creating Infinite Generators

```python
def infinite_counter(start=0):
    current = start
    while True:
        yield current
        current += 1

counter = infinite_counter()
for _ in range(5):
    print(next(counter))
```

Output:
```
0
1
2
3
4
```

### Fibonacci Sequence

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
print([next(fib) for _ in range(8)])
```

Output:
```
[0, 1, 1, 2, 3, 5, 8, 13]
```

## Chaining Operations

### Lazy Composition

```python
def multiply(iterable, factor):
    for value in iterable:
        yield value * factor

def add_offset(iterable, offset):
    for value in iterable:
        yield value + offset

pipeline = add_offset(multiply(range(5), 2), 10)
print(list(pipeline))
```

Output:
```
[10, 12, 14, 16, 18]
```

### Filtering Lazily

```python
def lazy_filter(iterable, predicate):
    for value in iterable:
        if predicate(value):
            yield value

nums = range(10)
evens = lazy_filter(nums, lambda x: x % 2 == 0)
print(list(evens))
```

Output:
```
[0, 2, 4, 6, 8]
```

---

## Runnable Example: `generator_performance_fibonacci.py`

```python
"""
TUTORIAL: Generator vs List - Memory and Performance with Fibonacci

Why this matters:
  When generating sequences of values, you face a choice:
  - List: Store ALL values in memory at once (O(n) memory)
  - Generator: Compute values on-demand (O(1) memory)

  For small sequences, this doesn't matter. But for large sequences or
  streams that never end, generators are essential. They also tend to be faster
  because they don't allocate huge blocks of memory.

Core lesson:
  Use generators for sequences you iterate over once. Use lists when you need
  to access items multiple times or by index. Generators are memory-efficient
  and often faster for streaming data.
"""

import timeit


# ============ Example 1: List-based Fibonacci ============
# This generates N Fibonacci numbers and returns them all in a list.
# Allocates O(n) memory and O(n) initialization time.
# Good when you need to iterate multiple times or access by index.

def fibonacci_list(num_items):
    """Generate first N Fibonacci numbers. Returns a list."""
    numbers = []
    a, b = 0, 1
    while len(numbers) < num_items:
        numbers.append(a)
        a, b = b, a + b
    return numbers


# ============ Example 2: Generator-based Fibonacci ============
# This uses yield to generate Fibonacci numbers one at a time.
# Allocates O(1) memory (just two state variables).
# Fast and efficient for iterating once through the sequence.

def fibonacci_gen(num_items):
    """Generate first N Fibonacci numbers. Yields one at a time."""
    a, b = 0, 1
    while num_items:
        yield a
        a, b = b, a + b
        num_items -= 1


# ============ Example 3: Helper for testing ============

def test_fibonacci(func, N):
    """Consume a fibonacci sequence (list or generator)."""
    for i in func(N):
        pass  # Just iterate, don't store values


def demo_memory_difference():
    """Show the memory difference between list and generator."""
    print("\n" + "=" * 70)
    print("Example 1: Memory Usage - List vs Generator")
    print("=" * 70)

    import sys

    N = 100

    fib_list = fibonacci_list(N)
    fib_gen = fibonacci_gen(N)

    list_size = sys.getsizeof(fib_list) + sum(sys.getsizeof(x) for x in fib_list)
    gen_size = sys.getsizeof(fib_gen)

    print(f"For first {N} Fibonacci numbers:\n")
    print(f"List object memory:      ~{list_size:,} bytes")
    print(f"Generator object memory: ~{gen_size:,} bytes")
    print()
    print(f"Memory ratio: {list_size / gen_size:.0f}x")
    print()
    print("""
    WHY the difference:
    - List stores all 100 numbers in memory (each is ~30 bytes)
    - Generator stores only 2 variables: a and b (~100 bytes total)
    - Generator doesn't allocate the list container

    For larger sequences:
    - 1,000 items: ~50x more memory for list
    - 1,000,000 items: ~50,000x more memory for list
    - For large N, generator is essential
    """)


def demo_speed_comparison():
    """Compare execution speed of list vs generator."""
    print("\n" + "=" * 70)
    print("Example 2: Speed Comparison - List vs Generator")
    print("=" * 70)

    setup = "from __main__ import test_fibonacci, fibonacci_gen, fibonacci_list, N"
    iterations = 1000

    print(f"Iterating through Fibonacci sequences {iterations} times each:\n")

    # Test different sequence sizes
    test_sizes = [2, 100, 1_000, 10_000]

    for N in test_sizes:
        # Test list version
        t_list = timeit.timeit(
            stmt="test_fibonacci(fibonacci_list, N)",
            setup=setup,
            number=iterations
        )

        # Test generator version
        t_gen = timeit.timeit(
            stmt="test_fibonacci(fibonacci_gen, N)",
            setup=setup,
            number=iterations
        )

        time_list = t_list / iterations
        time_gen = t_gen / iterations

        # Speedup (list divided by gen, so > 1 means gen is faster)
        speedup = time_list / time_gen

        print(f"N = {N:5} items:")
        print(f"  List:      {time_list:.5e}s")
        print(f"  Generator: {time_gen:.5e}s")
        print(f"  Speedup:   {speedup:.2f}x (generator faster)")
        print()


def demo_when_generator_needed():
    """Show scenarios where generators are essential."""
    print("\n" + "=" * 70)
    print("Example 3: When Generators Are Essential")
    print("=" * 70)

    print("""
    SCENARIO 1: Infinite sequences

    # List approach: IMPOSSIBLE
    all_primes = sieve_of_eratosthenes(infinity)  # Can't create infinite list!

    # Generator approach: WORKS
    for prime in infinite_primes():
        if prime > 1000000:
            break  # Stop whenever you want

    You can generate values as needed, forever.


    SCENARIO 2: Large data files

    # List approach: Load entire file into memory (may not fit)
    lines = open('huge_file.txt').readlines()  # 10GB file won't fit!

    # Generator approach: Process line by line
    for line in open('huge_file.txt'):
        process(line)  # Memory stays constant

    File generators are built-in with the file iterator.


    SCENARIO 3: Pipeline processing

    # List approach: Create intermediate lists
    numbers = range(1000000)
    doubled = [x * 2 for x in numbers]
    squared = [x ** 2 for x in doubled]
    filtered = [x for x in squared if x % 2 == 0]

    Creates 4 lists in memory, huge memory cost!

    # Generator approach: Pipeline
    def process():
        for x in range(1000000):
            yield x * 2
    def process2(gen):
        for x in gen:
            yield x ** 2
    def process3(gen):
        for x in gen:
            if x % 2 == 0:
                yield x

    Chain generators, single value in memory at a time!


    SCENARIO 4: Multiple iterations

    # List approach: Works, memory stays constant
    data = [1, 2, 3, 4, 5]
    for item in data: pass  # First iteration
    for item in data: pass  # Second iteration

    # Generator approach: Can't iterate twice!
    gen = (x for x in range(5))
    for item in gen: pass  # First iteration
    for item in gen: pass  # Empty! Generator exhausted!

    Generators are one-time use. Lists can iterate multiple times.
    """)


def demo_practical_example():
    """Show practical usage patterns."""
    print("\n" + "=" * 70)
    print("Example 4: Practical Usage Patterns")
    print("=" * 70)

    N = 20

    print(f"First {N} Fibonacci numbers:\n")

    # Generator: Simple to iterate once
    print("Using generator (iterate once):")
    fib_values = []
    for num in fibonacci_gen(N):
        fib_values.append(num)
    print(fib_values)

    print("\nUsing list (multiple access):")
    fib_list = fibonacci_list(N)

    # Can access by index
    print(f"First 5: {fib_list[:5]}")
    print(f"Last 3: {fib_list[-3:]}")
    print(f"Index 10: {fib_list[10]}")
    print(f"Sum: {sum(fib_list)}")

    print("""
    KEY DIFFERENCE:
    - Generator: Efficient, but can only iterate once
    - List: Uses more memory, but allows multiple iterations and indexing
    """)


def demo_hybrid_approach():
    """Show how to combine both approaches."""
    print("\n" + "=" * 70)
    print("Example 5: Hybrid Approach - Generator and List")
    print("=" * 70)

    print("""
    BEST OF BOTH WORLDS:

    # Use generator for on-demand computation
    def expensive_computation():
        for i in range(1000000):
            yield do_expensive_work(i)

    # Convert to list only when you need multiple accesses
    results = list(expensive_computation())

    # Or process in batches
    gen = expensive_computation()
    batch = list(itertools.islice(gen, 0, 1000))  # First 1000 items

    This pattern:
    - Uses generator for initial processing (memory efficient)
    - Converts to list only for the portion you need
    - Best of both worlds: lazy evaluation + indexing
    """)


if __name__ == "__main__":
    print("=" * 70)
    print("TUTORIAL: Generators vs Lists - Fibonacci Comparison")
    print("=" * 70)

    demo_memory_difference()
    demo_speed_comparison()
    demo_when_generator_needed()
    demo_practical_example()
    demo_hybrid_approach()

    # -------- KEY INSIGHTS --------
    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print("""
1. GENERATORS use O(1) memory:
   - Only store state variables (current position, temporary values)
   - Don't allocate space for full sequence
   - Perfect for large or infinite sequences

2. LISTS use O(n) memory:
   - Store all values in a container
   - Significant memory for large sequences
   - But allow indexing and multiple iterations

3. GENERATORS are usually FASTER:
   - No memory allocation overhead
   - No container initialization
   - CPU cache friendly (single values)
   - ~2-3x faster for streaming use cases

4. GENERATORS are ONE-TIME USE:
   - Can only iterate once
   - After exhaustion, must create new generator
   - Lists are reusable indefinitely

5. CHOOSE BY USE CASE:
   - Generator: Stream, one-time iteration, huge data
   - List: Multiple accesses, indexing, reasonable size
   - Hybrid: Generate lazily, convert to list if needed

6. REAL-WORLD IMPACT:
   - File reading: Always use generators (file iterator)
   - Network streaming: Always use generators
   - Data pipelines: Chain generators (memory efficient)
   - Local computation: Generator usually better even when list would fit
   - Random access: Must use list or convert generator

7. PYTHON IDIOM:
   - (x for x in iterable): Generator expression
   - [x for x in iterable]: List comprehension
   - Use () by default, [] only when you need list
    """)
```

---

## Exercises


**Exercise 1.**
Write a generator `infinite_squares()` that yields 1, 4, 9, 16, ... (squares of natural numbers) indefinitely. Use `itertools.islice` to get the first 10 squares.

??? success "Solution to Exercise 1"

        ```python
        from itertools import islice

        def infinite_squares():
            n = 1
            while True:
                yield n * n
                n += 1

        print(list(islice(infinite_squares(), 10)))
        # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
        ```

    The generator produces squares indefinitely. `islice` takes only the first 10 without running forever.

---

**Exercise 2.**
Demonstrate lazy evaluation by writing a generator that prints a message each time it yields a value. Show that values are produced one at a time, not all at once.

??? success "Solution to Exercise 2"

        ```python
        def verbose_range(n):
            for i in range(n):
                print(f"  Yielding {i}")
                yield i

        print("Creating generator:")
        gen = verbose_range(5)
        print("No output yet -- lazy!")

        print("Taking first 3:")
        for i, val in enumerate(gen):
            if i >= 3:
                break
            print(f"  Got {val}")
        ```

    Messages appear only when values are consumed, proving that the generator does not execute ahead of time.

---

**Exercise 3.**
Write a function `first_match(predicate, iterable)` that returns the first element for which `predicate` returns `True`, or `None` if no match is found. Use lazy evaluation to avoid processing the entire iterable.

??? success "Solution to Exercise 3"

        ```python
        def first_match(predicate, iterable):
            for item in iterable:
                if predicate(item):
                    return item
            return None

        result = first_match(lambda x: x > 100, range(1_000_000))
        print(result)  # 101
        ```

    The function returns immediately upon finding a match. It does not process the remaining 999,898 elements.
