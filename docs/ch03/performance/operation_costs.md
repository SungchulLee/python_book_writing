# Python Operation Costs

Different Python operations have different performance costs. Understanding which operations are expensive helps optimize code effectively.

!!! tip "Mental Model"
    Not all Python operations are created equal. Membership testing in a list is O(n) but in a set is O(1). String concatenation in a loop is O(n^2) but `''.join()` is O(n). Function calls, attribute lookups, and global variable access all have measurable overhead. Knowing these relative costs lets you spot bottlenecks before reaching for a profiler.

---

## Collection Operations

### List vs Set Membership

```python
import timeit

setup_list = "lst = list(range(100000))"
list_check = timeit.timeit("99999 in lst", setup=setup_list, number=1000)

setup_set = "s = set(range(100000))"
set_check = timeit.timeit("99999 in s", setup=setup_set, number=1000)

print(f"List membership: {list_check:.4f}s")
print(f"Set membership: {set_check:.6f}s")
print(f"Set is {list_check/set_check:.0f}x faster")
```

Output:
```
List membership: 0.0234s
Set membership: 0.000045s
Set is 520x faster
```

## String Operations

### String Concatenation

```python
import timeit

code1 = """
result = ""
for i in range(1000):
    result += str(i)
"""

code2 = """
parts = [str(i) for i in range(1000)]
result = "".join(parts)
"""

concat_time = timeit.timeit(code1, number=100)
join_time = timeit.timeit(code2, number=100)

print(f"Concatenation: {concat_time:.4f}s")
print(f"Join: {join_time:.6f}s")
```

Output:
```
Concatenation: 0.0456s
Join: 0.0123s
```

## Loop Costs

### List Comprehension vs Loop

```python
import timeit

code1 = """
result = []
for i in range(1000):
    result.append(i * 2)
"""

code2 = '[i * 2 for i in range(1000)]'

loop_time = timeit.timeit(code1, number=10000)
comp_time = timeit.timeit(code2, number=10000)

print(f"Loop with append: {loop_time:.4f}s")
print(f"List comprehension: {comp_time:.4f}s")
```

Output:
```
Loop with append: 0.0987s
List comprehension: 0.0654s
```

### Four Ways to Transform a List

Python offers four common patterns for applying a function to every element. Each has different performance characteristics because of how much work stays in the interpreter versus compiled C code:

```python
import time

words = ['hello', 'world', 'python'] * 10_000

# 1. Explicit for loop with append
tic = time.time()
result = []
for word in words:
    result.append(word.upper())
loop_time = time.time() - tic

# 2. map() — pushes the loop into C
tic = time.time()
result = list(map(str.upper, words))
map_time = time.time() - tic

# 3. List comprehension
tic = time.time()
result = [w.upper() for w in words]
comp_time = time.time() - tic

# 4. Generator expression (lazy, no intermediate list)
tic = time.time()
result = list(s.upper() for s in words)
gen_time = time.time() - tic

print(f"for loop:       {loop_time:.4f}s")
print(f"map():          {map_time:.4f}s")
print(f"comprehension:  {comp_time:.4f}s")
print(f"generator:      {gen_time:.4f}s")
```

`map()` is typically fastest because the entire iteration happens in C with no per-element bytecode overhead. List comprehensions are faster than explicit loops because the append is handled internally. Generator expressions avoid allocating the full list but add per-element suspension overhead.

---

## Attribute Lookup Overhead

### Avoiding Dots in Inner Loops

Every dot (`.`) in Python triggers an attribute lookup. In tight loops over large data, caching the method reference outside the loop can produce measurable speedups:

```python
import timeit

# With dots: word.upper() resolves the method on every iteration
code_with_dot = """
oldlist = ['some', 'string', 'that', 'is', 'big'] * 50000
newlist = []
for word in oldlist:
    newlist.append(word.upper())
"""

# Without dots: pre-bind both upper and append
code_without_dot = """
oldlist = ['some', 'string', 'that', 'is', 'big'] * 50000
upper = str.upper
newlist = []
append = newlist.append
for word in oldlist:
    append(upper(word))
"""

t_dot = timeit.timeit(stmt=code_with_dot, number=10)
t_nodot = timeit.timeit(stmt=code_without_dot, number=10)

print(f"With dots:    {t_dot:.4f}s")
print(f"Without dots: {t_nodot:.4f}s")
print(f"Speedup:      {t_dot / t_nodot:.2f}x")
```

The speedup comes from eliminating two dictionary lookups per iteration: one for `newlist.append` and one for `word.upper`. For small loops the difference is negligible, but for millions of iterations it adds up. This technique is most useful in performance-critical inner loops where every microsecond matters.

## Function Call Overhead

### Builtin vs User Functions

```python
import timeit

builtin_sum = timeit.timeit("sum(range(1000))", number=10000)

code = """
def my_sum(values):
    total = 0
    for v in values:
        total += v
    return total
my_sum(range(1000))
"""
user_sum = timeit.timeit(code, number=10000)

print(f"Builtin sum: {builtin_sum:.4f}s")
print(f"User function: {user_sum:.4f}s")
```

Output:
```
Builtin sum: 0.0123s
User function: 0.0456s
```

---

## Runnable Example: `reducing_operations.py`

```python
"""
TUTORIAL: Reducing Unnecessary Operations for Performance

Why this matters:
  When writing loops that need to find something or check a condition, how you
  structure the code dramatically impacts performance. The key insight is that
  EARLY TERMINATION (returning immediately when we find what we need) is much
  faster than continuing to process data after finding our target.

  This tutorial shows three critical patterns:
  1. Early return (best): Stop immediately when condition is met
  2. Unnecessary continuation (worst): Keep looping even after finding answer
  3. Using builtins (good): Leverage optimized functions like any()

Core lesson:
  Don't continue work after you have your answer. The CPU time spent on
  unnecessary operations adds up fast, especially in loops.
"""

import timeit


# ============ Example 1: The FAST way - Early Return ============
# This is the optimal pattern. As soon as we find a match, we return True
# immediately. If needle is near the beginning, we save scanning the rest.

def search_fast(haystack, needle):
    """Return True if needle is in haystack, STOP as soon as found."""
    for item in haystack:
        if item == needle:
            return True  # <-- Exit immediately when found
    return False


# ============ Example 2: The SLOW way - No Early Return ============
# This function continues looping EVEN AFTER finding the match. It sets
# return_value to True but keeps iterating through the entire list.
# This wastes CPU cycles on comparisons we don't need.

def search_slow(haystack, needle):
    """Same functionality, but doesn't return early. Much slower!"""
    return_value = False
    for item in haystack:
        if item == needle:
            return_value = True
        # <-- Keeps looping here instead of exiting
    return return_value


# ============ Example 3: Using any() with generator ============
# The any() builtin is optimized in C and also uses short-circuit evaluation.
# This generator expression doesn't create a full list in memory - it generates
# comparisons on-demand, and any() stops as soon as one True is found.

def search_builtin_gen(haystack, needle):
    """Use any() with a generator - efficient and Pythonic."""
    return any((item == needle for item in haystack))


# ============ Example 4: Using any() with list comprehension ============
# WARNING: This creates the entire list of comparisons BEFORE any() starts.
# So this must evaluate the entire list even if the match is near the beginning.
# Don't use this pattern for early termination tasks!

def search_builtin_list(haystack, needle):
    """Using any() with list comprehension - creates full list first."""
    return any([item == needle for item in haystack])


if __name__ == "__main__":
    print("=" * 70)
    print("TUTORIAL: Reducing Unnecessary Operations")
    print("=" * 70)

    # Setup test data
    haystack = list(range(1000))  # 0, 1, 2, ..., 999
    iterations = 10000

    # -------- TEST 1: Needle near the beginning --------
    print("\n" + "=" * 70)
    print("Test 1: Needle CLOSE TO START (position 5)")
    print("=" * 70)

    needle = 5

    t_fast = timeit.timeit(
        stmt="search_fast(haystack, needle)",
        setup="from __main__ import haystack, needle, search_fast",
        number=iterations
    )
    print(f"search_fast:        {t_fast/iterations:.5e} seconds per call")

    t_slow = timeit.timeit(
        stmt="search_slow(haystack, needle)",
        setup="from __main__ import haystack, needle, search_slow",
        number=iterations
    )
    print(f"search_slow:        {t_slow/iterations:.5e} seconds per call")

    t_gen = timeit.timeit(
        stmt="search_builtin_gen(haystack, needle)",
        setup="from __main__ import haystack, needle, search_builtin_gen",
        number=iterations
    )
    print(f"any() + generator:  {t_gen/iterations:.5e} seconds per call")

    t_list = timeit.timeit(
        stmt="search_builtin_list(haystack, needle)",
        setup="from __main__ import haystack, needle, search_builtin_list",
        number=iterations
    )
    print(f"any() + list comp:  {t_list/iterations:.5e} seconds per call")

    slowdown = t_slow / t_fast
    print(f"\nSLOW version is {slowdown:.1f}x slower than FAST!")
    print("WHY: search_slow must scan 995 more items after finding the match.")

    # -------- TEST 2: Needle near the end --------
    print("\n" + "=" * 70)
    print("Test 2: Needle CLOSE TO END (position 990)")
    print("=" * 70)

    needle = len(haystack) - 10

    t_fast = timeit.timeit(
        stmt="search_fast(haystack, needle)",
        setup="from __main__ import haystack, needle, search_fast",
        number=iterations
    )
    print(f"search_fast:        {t_fast/iterations:.5e} seconds per call")

    t_slow = timeit.timeit(
        stmt="search_slow(haystack, needle)",
        setup="from __main__ import haystack, needle, search_slow",
        number=iterations
    )
    print(f"search_slow:        {t_slow/iterations:.5e} seconds per call")

    t_gen = timeit.timeit(
        stmt="search_builtin_gen(haystack, needle)",
        setup="from __main__ import haystack, needle, search_builtin_gen",
        number=iterations
    )
    print(f"any() + generator:  {t_gen/iterations:.5e} seconds per call")

    slowdown = t_slow / t_fast
    print(f"\nSLOW version is {slowdown:.1f}x slower than FAST!")
    print("WHY: Both must scan almost the entire list, so difference is smaller.")
    print("But FAST is still faster because it stops immediately upon finding.")

    # -------- KEY INSIGHTS --------
    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print("""
1. EARLY RETURN beats everything:
   - Return as soon as you find your answer
   - Don't set a variable and keep looping

2. any() with GENERATOR is nearly as good:
   - Generators use lazy evaluation (compute on-demand)
   - any() short-circuits (stops when first True found)
   - More Pythonic than manual loops

3. any() with LIST COMPREHENSION is slower:
   - List comprehension creates the ENTIRE list first
   - No short-circuit benefit since list exists fully
   - Never use this pattern for early-termination logic

4. The impact depends on DATA POSITION:
   - Near the start: HUGE difference (10x+ slowdown)
   - Near the end: Smaller difference but still present
   - Worst case: Missing item requires checking everything

5. CPU TIME MATTERS:
   - In tight loops, unnecessary iterations add up
   - 10,000 iterations × extra work = measurable delay
   - In real code with millions of iterations: seconds wasted
    """)
```


---

## Exercises


**Exercise 1.**
Compare building a string from 10,000 integers using `+=` concatenation versus `"".join()`. Time both approaches and explain why one is faster.

??? success "Solution to Exercise 1"

    ```python
    import timeit

    code_concat = '''
    result = ""
    for i in range(10000):
        result += str(i)
    '''

    code_join = '''
    result = "".join(str(i) for i in range(10000))
    '''

    t_concat = timeit.timeit(code_concat, number=100)
    t_join = timeit.timeit(code_join, number=100)

    print(f"+= concat: {t_concat:.4f}s")
    print(f"join():    {t_join:.4f}s")
    ```

    String concatenation with `+=` creates a new string object each iteration because strings are immutable. `"".join()` allocates the final string once after computing the total length.

---

**Exercise 2.**
Show the performance difference between appending to a list with `append()` in a loop versus using a list comprehension. Use `timeit` with 100,000 elements.

??? success "Solution to Exercise 2"

    ```python
    import timeit

    code_loop = '''
    result = []
    for i in range(100000):
        result.append(i * 2)
    '''

    code_comp = '[i * 2 for i in range(100000)]'

    t_loop = timeit.timeit(code_loop, number=100)
    t_comp = timeit.timeit(code_comp, number=100)

    print(f"Loop + append: {t_loop:.4f}s")
    print(f"Comprehension: {t_comp:.4f}s")
    ```

    List comprehensions are faster because the append operation is handled internally in C bytecode, avoiding the overhead of the `append` method lookup and call on every iteration.

---

**Exercise 3.**
Demonstrate the attribute lookup optimization by caching `list.append` in a local variable before a loop. Compare the timed results for 1,000,000 iterations with and without caching.

??? success "Solution to Exercise 3"

    ```python
    import timeit

    code_with_dot = '''
    result = []
    for i in range(1000000):
        result.append(i)
    '''

    code_cached = '''
    result = []
    append = result.append
    for i in range(1000000):
        append(i)
    '''

    t_dot = timeit.timeit(code_with_dot, number=10)
    t_cached = timeit.timeit(code_cached, number=10)

    print(f"With dot:    {t_dot:.4f}s")
    print(f"Cached:      {t_cached:.4f}s")
    print(f"Speedup:     {t_dot / t_cached:.2f}x")
    ```

    Caching `result.append` avoids an attribute dictionary lookup on every iteration. For millions of iterations, eliminating one dictionary lookup per cycle produces a measurable speedup.
