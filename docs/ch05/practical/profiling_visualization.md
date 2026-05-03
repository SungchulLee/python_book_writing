# Profiling Visualization (snakeviz)

Visualizing profiling data makes it easier to understand performance characteristics. `snakeviz` provides interactive flame graphs for cProfile output.

!!! tip "Mental Model"
    Raw profiling output is a wall of numbers. Visualization tools like `snakeviz` turn that data into interactive flame graphs where wide bars mean slow functions and nested bars show call hierarchy. Your eyes can spot the dominant bar in a flame graph far faster than scanning a sorted text table.

---

## Installation and Basic Usage

```bash
pip install snakeviz
```

Generate a profile and visualize:
```bash
python -m cProfile -o profile.prof your_script.py
snakeviz profile.prof
```

## Creating Profiler Output

```python
# example_code.py
import cProfile

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def process_data():
    results = []
    for i in range(25, 30):
        results.append(fibonacci(i))
    return results

if __name__ == "__main__":
    cProfile.run('process_data()', filename='profile.prof')
```

View the visualization:
```bash
snakeviz profile.prof
```

## Interpreting Flame Graphs

The visualization shows:
- **Box width**: Time spent in that function
- **Box height**: Call stack depth
- **Colors**: Different functions (random assignment)
- **Hover**: Shows function name and timing details
- **Click**: Zoom into that portion of the call tree

## Command-line Options

```bash
# Open on specific port
snakeviz --port 8080 profile.prof

# Open in specific browser
snakeviz --browser firefox profile.prof

# Don't open browser automatically
snakeviz --nostrip profile.prof
```

## Programmatic Profiling with Visualization

```python
import cProfile
import pstats
from io import StringIO

def slow_function():
    total = 0
    for i in range(100000):
        total += sum(range(i))
    return total

# Profile the function
profiler = cProfile.Profile()
profiler.enable()
slow_function()
profiler.disable()

# Save for visualization
profiler.dump_stats('results.prof')

# Also print text summary
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(5)
```

## Practical Workflow

1. Profile with cProfile
2. Save to .prof file
3. Visualize with snakeviz
4. Identify hot spots (wide boxes)
5. Focus optimization on hot spots
6. Profile again to verify improvements

---

## Exercises

**Exercise 1.**
Write a script that profiles a recursive Fibonacci function (n=25) using `cProfile`, saves the result to a `.prof` file, then loads it with `pstats.Stats` and prints the top 5 functions by cumulative time. Print the exact command a user would run to visualize this file with `snakeviz`.

??? success "Solution to Exercise 1"
        ```python
        import cProfile
        import pstats

        def fibonacci(n):
            if n <= 1:
                return n
            return fibonacci(n - 1) + fibonacci(n - 2)

        profiler = cProfile.Profile()
        profiler.enable()
        fibonacci(25)
        profiler.disable()

        profiler.dump_stats("fib_profile.prof")

        stats = pstats.Stats("fib_profile.prof")
        stats.strip_dirs()
        stats.sort_stats('cumulative')
        stats.print_stats(5)

        print("\nTo visualize, run:")
        print("  snakeviz fib_profile.prof")
        ```

---

**Exercise 2.**
Create a function `profile_to_file(func, filename, *args)` that wraps any callable with `cProfile.Profile`, runs it with the given arguments, saves the profile to the given filename, and also prints a text summary of the top 10 functions sorted by total time. Test it with a function that does 100 sorts of 10,000-element lists.

??? success "Solution to Exercise 2"
        ```python
        import cProfile
        import pstats
        import random

        def profile_to_file(func, filename, *args):
            profiler = cProfile.Profile()
            profiler.enable()
            result = func(*args)
            profiler.disable()
            profiler.dump_stats(filename)
            stats = pstats.Stats(profiler)
            stats.strip_dirs()
            stats.sort_stats('tottime')
            stats.print_stats(10)
            return result

        def sort_many():
            for _ in range(100):
                data = [random.random() for _ in range(10_000)]
                data.sort()

        profile_to_file(sort_many, "sort_profile.prof")
        ```

---

**Exercise 3.**
Write a script that profiles two implementations of the same task (finding prime numbers up to 100,000 using trial division vs sieve of Eratosthenes), saves each to separate `.prof` files, loads both with `pstats.Stats`, and prints a side-by-side comparison of total calls and total time.

??? success "Solution to Exercise 3"
        ```python
        import cProfile
        import pstats

        def primes_trial(limit):
            primes = []
            for n in range(2, limit):
                is_prime = True
                for p in primes:
                    if p * p > n:
                        break
                    if n % p == 0:
                        is_prime = False
                        break
                if is_prime:
                    primes.append(n)
            return primes

        def primes_sieve(limit):
            sieve = [True] * limit
            sieve[0] = sieve[1] = False
            for i in range(2, int(limit ** 0.5) + 1):
                if sieve[i]:
                    for j in range(i * i, limit, i):
                        sieve[j] = False
            return [i for i, v in enumerate(sieve) if v]

        limit = 100_000

        p1 = cProfile.Profile()
        p1.enable()
        primes_trial(limit)
        p1.disable()
        p1.dump_stats("trial.prof")

        p2 = cProfile.Profile()
        p2.enable()
        primes_sieve(limit)
        p2.disable()
        p2.dump_stats("sieve.prof")

        s1 = pstats.Stats(p1)
        s2 = pstats.Stats(p2)

        print(f"{'':>20} {'Trial':>12} {'Sieve':>12}")
        print(f"{'Total calls':>20} {s1.total_calls:>12,} "
              f"{s2.total_calls:>12,}")
        print(f"{'Total time':>20} {s1.total_tt:>12.4f}s "
              f"{s2.total_tt:>12.4f}s")
        ```
