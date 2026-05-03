# timeit Module

The timeit module measures execution time of code snippets, useful for benchmarking and performance comparison. It handles timing overhead and runs code multiple times for accurate results.

!!! tip "Mental Model"
    `timeit` is a stopwatch for code. It disables garbage collection, runs your snippet many times, and reports the total. By running many iterations it averages out noise from OS scheduling and caching. Always compare two approaches with `timeit` side by side rather than relying on intuition about which is faster.

---

## Basic Timing

### Simple Benchmarking

```python
import timeit

result = timeit.timeit("sum(range(100))", number=100000)
print(f"Execution time: {result:.4f}s")
```

Output:
```
Execution time: 0.1234s
```

### Timer Class

```python
import timeit

timer = timeit.Timer("x = 1 + 1")
result = timer.timeit(number=1000000)
print(f"1000000 iterations: {result:.4f}s")
```

Output:
```
1000000 iterations: 0.0234s
```

## Setup Code

### Initializing Before Timing

```python
import timeit

setup = "lst = list(range(1000))"
time1 = timeit.timeit("5 in lst", setup=setup, number=100000)
print(f"Membership test: {time1:.4f}s")
```

Output:
```
Membership test: 0.0456s
```

## Comparing Code Snippets

### Which is Faster?

```python
import timeit

concat_time = timeit.timeit(
    'x = "a" + "b" + "c"',
    number=1000000
)

format_time = timeit.timeit(
    'x = f"{"a"}{"b"}{"c"}"',
    number=1000000
)

print(f"Concatenation: {concat_time:.4f}s")
print(f"F-string: {format_time:.4f}s")
```

Output:
```
Concatenation: 0.0234s
F-string: 0.0198s
```

## Repeat and Compare

### Multiple Runs

```python
import timeit

times = timeit.repeat(
    "sum(range(100))",
    number=10000,
    repeat=5
)

print(f"Times: {[f'{t:.4f}' for t in times]}")
print(f"Best: {min(times):.4f}s")
print(f"Worst: {max(times):.4f}s")
```

Output:
```
Times: ['0.1234', '0.1201', '0.1198', '0.1205', '0.1211']
Best: 0.1198s
Worst: 0.1234s
```

## Real-World Example

### Benchmarking List Operations

```python
import timeit

operations = {
    'append': 'lst.append(100)',
    'insert_0': 'lst.insert(0, 100)',
    'extend': 'lst.extend([100, 101])'
}

setup = "lst = list(range(100))"

for name, code in operations.items():
    time = timeit.timeit(code, setup=setup, number=10000)
    print(f"{name}: {time:.4f}s")
```

Output:
```
append: 0.0012s
insert_0: 0.0456s
extend: 0.0045s
```


---

## Exercises


**Exercise 1.**
Use `timeit.timeit()` to compare the speed of creating a list using `list(range(1000))` versus `[*range(1000)]`. Run each 10,000 times and report which is faster.

??? success "Solution to Exercise 1"

    ```python
    import timeit

    t_list = timeit.timeit("list(range(1000))", number=10000)
    t_unpack = timeit.timeit("[*range(1000)]", number=10000)

    print(f"list():    {t_list:.4f}s")
    print(f"[*...]:    {t_unpack:.4f}s")
    ```

    Both create a list from a range, but unpacking (`[*range()]`) can be slightly faster because it avoids the overhead of calling the `list()` constructor function.

---

**Exercise 2.**
Use `timeit.repeat()` to measure `sum(range(1000))` with 5 repeats of 10,000 executions each. Print the best, worst, and average times.

??? success "Solution to Exercise 2"

    ```python
    import timeit

    times = timeit.repeat("sum(range(1000))", number=10000, repeat=5)

    print(f"Best:    {min(times):.4f}s")
    print(f"Worst:   {max(times):.4f}s")
    print(f"Average: {sum(times)/len(times):.4f}s")
    ```

    `timeit.repeat()` runs the full measurement multiple times. The best time is the most reliable because higher times include OS scheduling overhead.

---

**Exercise 3.**
Write a benchmark that compares three ways to check if a number is even: `n % 2 == 0`, `n & 1 == 0`, and `not n % 2`. Use `timeit` to determine which is fastest.

??? success "Solution to Exercise 3"

    ```python
    import timeit

    setup = "n = 42"

    t_mod = timeit.timeit("n % 2 == 0", setup=setup, number=1000000)
    t_bit = timeit.timeit("n & 1 == 0", setup=setup, number=1000000)
    t_not = timeit.timeit("not n % 2", setup=setup, number=1000000)

    print(f"n % 2 == 0: {t_mod:.4f}s")
    print(f"n & 1 == 0: {t_bit:.4f}s")
    print(f"not n % 2:  {t_not:.4f}s")
    ```

    All three approaches are very fast for single checks. The bitwise approach (`n & 1`) may be marginally faster since it avoids a comparison, but the difference is negligible in practice.
