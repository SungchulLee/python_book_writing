# Benchmarking Methodology

Proper benchmarking requires careful methodology to get accurate, reproducible results. Learn best practices for performance testing.

!!! tip "Mental Model"
    Benchmarking is the scientific method applied to code performance. A single timing run is an anecdote, not data. Use `timeit` for micro-benchmarks with many repetitions, collect statistics across runs, and control for noise -- just as you would control variables in an experiment. Measure, don't guess.

---

## Using timeit Module

The `timeit` module is the standard way to benchmark small code snippets:

```python
import timeit

# Method 1: Direct timing
time1 = timeit.timeit('sum(range(100))', number=1000000)
print(f"Time: {time1:.4f} seconds")

# Method 2: Using a function
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

time2 = timeit.timeit(lambda: fibonacci(20), number=100)
print(f"Average: {time2/100:.6f} seconds")
```

## Statistical Benchmarking

```python
import timeit
import statistics

def benchmark(func, number=100, repeat=5):
    times = timeit.repeat(
        lambda: func(),
        number=number,
        repeat=repeat
    )
    return {
        'min': min(times),
        'max': max(times),
        'mean': statistics.mean(times),
        'stdev': statistics.stdev(times) if len(times) > 1 else 0
    }

def test_function():
    return sum(i ** 2 for i in range(1000))

stats = benchmark(test_function)
print(f"Mean: {stats['mean']:.4f}s ± {stats['stdev']:.4f}s")
```

## Comparing Implementations

```python
import timeit

# Compare two approaches
list_comp = 'result = [x**2 for x in range(1000)]'
map_func = 'result = list(map(lambda x: x**2, range(1000)))'
generator = 'result = (x**2 for x in range(1000))'

time_list = timeit.timeit(list_comp, number=100000)
time_map = timeit.timeit(map_func, number=100000)
time_gen = timeit.timeit(generator, number=100000)

print(f"List comprehension: {time_list:.4f}s")
print(f"Map function: {time_map:.4f}s")
print(f"Generator: {time_gen:.4f}s")
```

## Best Practices

- Run benchmarks multiple times (10-100+)
- Disable background processes
- Use realistic data sizes
- Warm up code before benchmarking (JIT compilation)
- Profile on production-like hardware
- Compare against baselines, not absolute times
- Report mean, min, max, and standard deviation

---


## Runnable Example: `timeit_tutorial.py`

```python
"""
PYTHON CODE PROFILING & OPTIMIZATION - BEGINNER LEVEL
======================================================
Module 3: Timeit Module - Precise Micro-Benchmarking

LEARNING OBJECTIVES:
- Master the timeit module for accurate performance measurement
- Understand repeat vs number parameters
- Learn to compare code snippets reliably
- Avoid common micro-benchmarking pitfalls
- Use timeit from command line and in code

THEORY:
-------
The timeit module provides a simple way to time small code snippets.
It automatically:
- Runs code multiple times to get reliable measurements
- Disables garbage collection during timing
- Provides statement setup capability
- Returns minimum time (most reliable for micro-benchmarks)

Author: Python Course Development Team
Date: 2024
"""

import timeit
import random


# ============================================================================
# SECTION 1: BASIC TIMEIT USAGE
# ============================================================================

def basic_timeit_example():
    """
    Basic usage of timeit module
    
    timeit.timeit():
        stmt: Statement to time
        number: How many times to execute stmt (default: 1,000,000)
        
    Returns: Total time for all executions
    """
    print("=" * 70)
    print("BASIC TIMEIT USAGE")
    print("=" * 70)
    
    # Example 1: Time a simple statement
    time_taken = timeit.timeit('x = 2 + 2', number=1000000)
    print(f"'x = 2 + 2' (1M times): {time_taken:.6f} seconds")
    print(f"  Per operation: {time_taken/1000000*1e9:.2f} nanoseconds\n")
    
    # Example 2: Time a string operation
    time_taken = timeit.timeit('"hello" + " " + "world"', number=1000000)
    print(f"String concatenation (1M times): {time_taken:.6f} seconds")
    print(f"  Per operation: {time_taken/1000000*1e9:.2f} nanoseconds\n")
    
    # Example 3: Time list operations
    time_taken = timeit.timeit('[i for i in range(100)]', number=10000)
    print(f"List comprehension [i for i in range(100)] (10K times): {time_taken:.6f} seconds")
    print(f"  Per operation: {time_taken/10000*1e6:.2f} microseconds\n")


# ============================================================================
# SECTION 2: USING SETUP PARAMETER
# ============================================================================

def demonstrate_setup_parameter():
    """
    Using setup parameter for initialization
    
    Setup code runs once before timing begins.
    Use it to:
    - Import modules
    - Create test data
    - Initialize variables
    """
    print("=" * 70)
    print("USING SETUP PARAMETER")
    print("=" * 70)
    
    # Example 1: Testing list search with setup
    setup = '''
import random
data = [random.randint(0, 1000) for _ in range(1000)]
target = random.choice(data)
'''
    
    stmt = 'target in data'
    
    time_taken = timeit.timeit(stmt, setup=setup, number=10000)
    print(f"List membership test:")
    print(f"  Time for 10,000 searches: {time_taken:.6f} seconds")
    print(f"  Per search: {time_taken/10000*1e6:.2f} microseconds\n")
    
    # Example 2: Testing dictionary search with setup
    setup_dict = '''
import random
data = {i: i*2 for i in range(1000)}
target = random.randint(0, 999)
'''
    
    stmt_dict = 'target in data'
    
    time_taken_dict = timeit.timeit(stmt_dict, setup=setup_dict, number=10000)
    print(f"Dictionary membership test:")
    print(f"  Time for 10,000 searches: {time_taken_dict:.6f} seconds")
    print(f"  Per search: {time_taken_dict/10000*1e6:.2f} microseconds")
    
    # Comparison
    print(f"\nDictionary is {time_taken/time_taken_dict:.1f}x faster than list!\n")


# ============================================================================
# SECTION 3: REPEAT PARAMETER
# ============================================================================

def demonstrate_repeat():
    """
    Using repeat to get multiple measurements
    
    timeit.repeat():
        Returns a list of times from multiple runs
        repeat: Number of times to repeat the entire timing
        number: Number of executions per repeat
    
    Best practice: Report the minimum time
    Why? Minimum represents the machine's best performance
    (least affected by background processes)
    """
    print("=" * 70)
    print("USING REPEAT FOR MULTIPLE MEASUREMENTS")
    print("=" * 70)
    
    stmt = '[i**2 for i in range(100)]'
    
    # Run 5 repetitions, each with 10,000 executions
    times = timeit.repeat(stmt, repeat=5, number=10000)
    
    print(f"Statement: {stmt}")
    print(f"Repetitions: 5, Executions per repeat: 10,000\n")
    
    for i, t in enumerate(times, 1):
        print(f"Repeat {i}: {t:.6f} seconds ({t/10000*1e6:.2f} μs per operation)")
    
    print(f"\nBest time:  {min(times):.6f} seconds")
    print(f"Worst time: {max(times):.6f} seconds")
    print(f"Average:    {sum(times)/len(times):.6f} seconds")
    
    print("\nRecommendation: Report minimum time for micro-benchmarks")
    print("It represents the machine's best performance.\n")


# ============================================================================
# SECTION 4: COMPARING IMPLEMENTATIONS
# ============================================================================

def compare_string_concatenation():
    """
    Compare different methods of string concatenation
    
    Demonstrates how to use timeit to compare alternatives
    """
    print("=" * 70)
    print("COMPARING STRING CONCATENATION METHODS")
    print("=" * 70)
    
    n = 1000
    
    # Method 1: + operator
    setup = f'strings = [str(i) for i in range({n})]'
    stmt1 = '''
result = ""
for s in strings:
    result = result + s
'''
    
    # Method 2: join()
    stmt2 = 'result = "".join(strings)'
    
    # Method 3: += operator
    stmt3 = '''
result = ""
for s in strings:
    result += s
'''
    
    # Time each method
    time1 = min(timeit.repeat(stmt1, setup=setup, repeat=3, number=100))
    time2 = min(timeit.repeat(stmt2, setup=setup, repeat=3, number=100))
    time3 = min(timeit.repeat(stmt3, setup=setup, repeat=3, number=100))
    
    print(f"Concatenating {n} strings:\n")
    print(f"Method 1 (+ operator):   {time1:.6f} seconds")
    print(f"Method 2 (join):         {time2:.6f} seconds")
    print(f"Method 3 (+= operator):  {time3:.6f} seconds")
    
    # Find best method
    best_time = min(time1, time2, time3)
    
    print(f"\nSpeedup factors (relative to best):")
    print(f"  + operator:  {time1/best_time:.2f}x")
    print(f"  join():      {time2/best_time:.2f}x")
    print(f"  += operator: {time3/best_time:.2f}x")
    
    print("\nWinner: join() is fastest for concatenating many strings!\n")


def compare_list_creation():
    """
    Compare different methods of creating lists
    """
    print("=" * 70)
    print("COMPARING LIST CREATION METHODS")
    print("=" * 70)
    
    n = 1000
    
    # Method 1: append in loop
    stmt1 = f'''
result = []
for i in range({n}):
    result.append(i**2)
'''
    
    # Method 2: list comprehension
    stmt2 = f'result = [i**2 for i in range({n})]'
    
    # Method 3: map with lambda
    stmt3 = f'result = list(map(lambda x: x**2, range({n})))'
    
    # Time each method
    time1 = min(timeit.repeat(stmt1, repeat=5, number=1000))
    time2 = min(timeit.repeat(stmt2, repeat=5, number=1000))
    time3 = min(timeit.repeat(stmt3, repeat=5, number=1000))
    
    print(f"Creating list of {n} squared numbers:\n")
    print(f"Method 1 (append loop):       {time1:.6f} seconds")
    print(f"Method 2 (list comprehension): {time2:.6f} seconds")
    print(f"Method 3 (map with lambda):    {time3:.6f} seconds")
    
    # Find best method
    best_time = min(time1, time2, time3)
    
    print(f"\nSpeedup factors (relative to best):")
    print(f"  append loop:       {time1/best_time:.2f}x")
    print(f"  list comprehension: {time2/best_time:.2f}x")
    print(f"  map with lambda:    {time3/best_time:.2f}x")
    
    print("\nWinner: List comprehension is fastest!\n")


# ============================================================================
# SECTION 5: TIMING FUNCTIONS
# ============================================================================

def demonstrate_timing_functions():
    """
    Time custom functions using timeit
    
    Shows how to test your own functions
    """
    print("=" * 70)
    print("TIMING CUSTOM FUNCTIONS")
    print("=" * 70)
    
    # Define functions to test
    def factorial_recursive(n):
        """Recursive factorial"""
        if n <= 1:
            return 1
        return n * factorial_recursive(n - 1)
    
    def factorial_iterative(n):
        """Iterative factorial"""
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    # Make functions available to timeit
    # Method 1: Using globals parameter
    time_recursive = min(timeit.repeat(
        'factorial_recursive(20)',
        globals={'factorial_recursive': factorial_recursive},
        repeat=5,
        number=10000
    ))
    
    time_iterative = min(timeit.repeat(
        'factorial_iterative(20)',
        globals={'factorial_iterative': factorial_iterative},
        repeat=5,
        number=10000
    ))
    
    print("Calculating factorial(20):\n")
    print(f"Recursive: {time_recursive:.6f} seconds")
    print(f"Iterative: {time_iterative:.6f} seconds")
    print(f"\nIterative is {time_recursive/time_iterative:.2f}x faster\n")


# ============================================================================
# SECTION 6: COMMAND-LINE USAGE
# ============================================================================

def demonstrate_cli_usage():
    """
    Demonstrate command-line usage of timeit
    
    Shows how to use timeit from terminal
    """
    print("=" * 70)
    print("COMMAND-LINE USAGE")
    print("=" * 70)
    
    examples = '''
The timeit module can be run from command line:

Basic usage:
    python -m timeit "2 + 2"

With setup code:
    python -m timeit -s "import math" "math.sqrt(2)"

Specify number of executions:
    python -m timeit -n 100000 "[x**2 for x in range(100)]"

Specify repeats:
    python -m timeit -r 5 "'-'.join(str(n) for n in range(100))"

Multiple statements:
    python -m timeit -s "x = range(1000)" "sum(x)"

Compare two approaches:
    python -m timeit "'hello' + 'world'"
    python -m timeit "''.join(['hello', 'world'])"

Options:
    -n N, --number=N    Execute statement N times
    -r N, --repeat=N    Repeat timer N times (default: 5)
    -s S, --setup=S     Setup statement to run before timing
    -p, --process       Use time.process_time() instead of time.perf_counter()
    -u, --unit=U        Time unit (nsec, usec, msec, or sec)
    -v, --verbose       Print raw timing results
    -h, --help          Show help message

Example output:
    $ python -m timeit "'hello' + 'world'"
    5000000 loops, best of 5: 58.3 nsec per loop
'''
    
    print(examples)


# ============================================================================
# SECTION 7: TIMEIT BEST PRACTICES
# ============================================================================

def timeit_best_practices():
    """
    Best practices and common pitfalls
    """
    print("=" * 70)
    print("TIMEIT BEST PRACTICES")
    print("=" * 70)
    
    practices = '''
DO:
✓ Report minimum time (most reliable for micro-benchmarks)
✓ Use enough repetitions (at least 3-5)
✓ Use appropriate number of executions
✓ Include setup code that runs once
✓ Test with realistic data sizes
✓ Compare implementations on same machine
✓ Use globals parameter for custom functions
✓ Verify results are correct before timing

DON'T:
✗ Don't time one-time operations (like imports) in the main statement
✗ Don't include print statements in timed code
✗ Don't time operations with side effects
✗ Don't forget to warm up (timeit handles this automatically)
✗ Don't compare absolute times across different machines
✗ Don't time overly simplistic operations (results may not scale)

COMMON PITFALLS:

1. Timing with side effects:
   BAD:  timeit.timeit('list.append(1)', setup='list = []')
   GOOD: timeit.timeit('x = 1')

2. Including initialization in timed code:
   BAD:  timeit.timeit('data = [1,2,3]; sum(data)')
   GOOD: timeit.timeit('sum(data)', setup='data = [1,2,3]')

3. Using print in timed code:
   BAD:  timeit.timeit('print(2+2)')
   GOOD: timeit.timeit('result = 2+2')

4. Not enough context:
   BAD:  "0.5 seconds"
   GOOD: "0.5 seconds for 1M iterations (500 ns per op)"

5. Comparing apples to oranges:
   Make sure compared implementations solve the same problem!

WHEN TO USE TIMEIT:
- Micro-benchmarks (small code snippets)
- Comparing alternative implementations
- Testing optimization ideas
- Quick performance checks

WHEN NOT TO USE TIMEIT:
- Profiling complete programs (use cProfile)
- Finding bottlenecks in large codebases (use profilers)
- Timing with I/O operations (use time module instead)
- Measuring real-world application performance
'''
    
    print(practices)


# ============================================================================
# SECTION 8: PRACTICAL EXAMPLES
# ============================================================================

def practical_examples():
    """
    Practical examples of using timeit
    """
    print("=" * 70)
    print("PRACTICAL EXAMPLES")
    print("=" * 70)
    
    # Example 1: Which is faster - 'in' or try/except for dict?
    print("\n1. Dictionary key check: 'in' vs try/except")
    
    setup = '''
data = {i: i*2 for i in range(1000)}
key = 500
'''
    
    stmt_in = 'result = key in data'
    stmt_try = '''
try:
    result = data[key]
except KeyError:
    result = None
'''
    
    time_in = min(timeit.repeat(stmt_in, setup=setup, repeat=5, number=100000))
    time_try = min(timeit.repeat(stmt_try, setup=setup, repeat=5, number=100000))
    
    print(f"  'in' operator:  {time_in:.6f} seconds")
    print(f"  try/except:     {time_try:.6f} seconds")
    print(f"  Winner: {'in' if time_in < time_try else 'try/except'} ({min(time_in, time_try)/max(time_in, time_try):.2f}x faster)")
    
    # Example 2: List vs tuple creation
    print("\n2. List vs Tuple creation")
    
    time_list = min(timeit.repeat('[1,2,3,4,5]', repeat=5, number=1000000))
    time_tuple = min(timeit.repeat('(1,2,3,4,5)', repeat=5, number=1000000))
    
    print(f"  List:   {time_list:.6f} seconds")
    print(f"  Tuple:  {time_tuple:.6f} seconds")
    print(f"  Winner: Tuple ({time_list/time_tuple:.2f}x faster)")
    
    # Example 3: String formatting methods
    print("\n3. String formatting methods")
    
    setup = 'name = "Alice"; age = 30'
    
    stmt_concat = 'result = "Name: " + name + ", Age: " + str(age)'
    stmt_format = 'result = "Name: {}, Age: {}".format(name, age)'
    stmt_fstring = 'result = f"Name: {name}, Age: {age}"'
    
    time_concat = min(timeit.repeat(stmt_concat, setup=setup, repeat=5, number=100000))
    time_format = min(timeit.repeat(stmt_format, setup=setup, repeat=5, number=100000))
    time_fstring = min(timeit.repeat(stmt_fstring, setup=setup, repeat=5, number=100000))
    
    print(f"  Concatenation: {time_concat:.6f} seconds")
    print(f"  .format():     {time_format:.6f} seconds")
    print(f"  f-string:      {time_fstring:.6f} seconds")
    
    best = min(time_concat, time_format, time_fstring)
    winner = ['Concatenation', '.format()', 'f-string'][
        [time_concat, time_format, time_fstring].index(best)
    ]
    print(f"  Winner: {winner}\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main function to run all demonstrations
    """
    print("\n" + "=" * 70)
    print("TIMEIT MODULE - COMPREHENSIVE TUTORIAL")
    print("=" * 70 + "\n")
    
    # Run all demonstrations
    basic_timeit_example()
    demonstrate_setup_parameter()
    demonstrate_repeat()
    compare_string_concatenation()
    compare_list_creation()
    demonstrate_timing_functions()
    demonstrate_cli_usage()
    timeit_best_practices()
    practical_examples()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    Key Takeaways:
    1. timeit is perfect for micro-benchmarking small code snippets
    2. Use setup parameter for initialization code
    3. Use repeat to get multiple measurements
    4. Report minimum time for most reliable results
    5. Always verify correctness before timing
    6. Compare implementations with same data and conditions
    
    Remember:
    - timeit.timeit() for single measurement
    - timeit.repeat() for multiple measurements
    - Use globals parameter for custom functions
    - Command-line usage: python -m timeit "statement"
    
    Next Steps:
    - Practice comparing your own implementations
    - Use timeit to validate optimization ideas
    - Learn cProfile for larger codebases
    """)


if __name__ == "__main__":
    main()
```


## Exercises

**Exercise 1.**
Use `timeit.repeat` with `repeat=7` and `number=10000` to benchmark three ways of checking membership in a collection of 10,000 elements: (a) a list, (b) a set, (c) a dictionary. Report the minimum time for each and compute the speedup of set and dict over list.

??? success "Solution to Exercise 1"
        ```python
        import timeit

        setup = """
data_list = list(range(10_000))
data_set = set(range(10_000))
data_dict = {i: None for i in range(10_000)}
target = 9_999
"""

        t_list = min(timeit.repeat(
            'target in data_list', setup=setup, repeat=7, number=10000))
        t_set = min(timeit.repeat(
            'target in data_set', setup=setup, repeat=7, number=10000))
        t_dict = min(timeit.repeat(
            'target in data_dict', setup=setup, repeat=7, number=10000))

        print(f"List: {t_list:.4f}s")
        print(f"Set:  {t_set:.4f}s  ({t_list/t_set:.0f}x faster)")
        print(f"Dict: {t_dict:.4f}s  ({t_list/t_dict:.0f}x faster)")
        ```

---

**Exercise 2.**
Write a `benchmark_report(func, name, number=1000, repeat=5)` function that uses `timeit.repeat` and the `statistics` module to print a formatted report including the function name, min, max, mean, and standard deviation of the timings. Test it on two sorting approaches: `sorted(data)` vs `data.sort()` on a list of 10,000 random integers.

??? success "Solution to Exercise 2"
        ```python
        import timeit
        import statistics
        import random

        def benchmark_report(func, name, number=1000, repeat=5):
            times = timeit.repeat(func, number=number, repeat=repeat)
            print(f"{name}:")
            print(f"  Min:   {min(times):.6f}s")
            print(f"  Max:   {max(times):.6f}s")
            print(f"  Mean:  {statistics.mean(times):.6f}s")
            print(f"  Stdev: {statistics.stdev(times):.6f}s")

        data = [random.randint(0, 100_000) for _ in range(10_000)]

        benchmark_report(
            lambda: sorted(data), "sorted(data)")
        benchmark_report(
            lambda: data.copy().sort(), "data.sort() (on copy)")
        ```

---

**Exercise 3.**
Compare the performance of three string formatting methods (f-string, `.format()`, and `%` formatting) for building 10,000 strings of the form `"Name: Alice, Age: 30"`. Use `timeit` to time each approach and print the results in a table showing method name, total time, and per-operation time in microseconds.

??? success "Solution to Exercise 3"
        ```python
        import timeit

        setup = 'name = "Alice"; age = 30'
        n = 10_000

        methods = {
            "f-string":  'f"Name: {name}, Age: {age}"',
            ".format()": '"Name: {}, Age: {}".format(name, age)',
            "% format":  '"Name: %s, Age: %d" % (name, age)',
        }

        print(f"{'Method':<12} {'Total (s)':>10} {'Per op (us)':>12}")
        print("-" * 36)

        for label, stmt in methods.items():
            t = min(timeit.repeat(stmt, setup=setup, repeat=5, number=n))
            per_op = t / n * 1e6
            print(f"{label:<12} {t:>10.4f} {per_op:>12.2f}")
        ```

---
