# Time vs Space

Efficient programs balance **time complexity** and **space complexity**. Understanding this trade-off is essential for writing performant Python code.

!!! tip "Mental Model"
    Most optimizations trade memory for speed or speed for memory. Caching (memoization) spends memory to avoid recomputation. Generators spend CPU to avoid storing all values at once. There is rarely a free lunch -- the art is choosing which resource matters more for your specific workload.

---

## Time complexity

Time complexity measures how execution time grows with input size.

Common classes:
- O(1): constant time
- O(log n): logarithmic
- O(n): linear
- O(n log n), O(n²): increasingly expensive

In Python, constant factors also matter.

---

## Space complexity

Space complexity measures memory usage:
- stack usage (call frames),
- heap usage (objects, containers),
- temporary allocations.

Faster algorithms often use more memory.

---

## Trade-offs in

Examples:
- caching results speeds up computation but uses memory,
- precomputing arrays avoids recomputation,
- vectorization trades memory for speed.

```python
# trade memory for
cache = {}
```

---

## Financial computing

In quantitative finance:
- latency matters in trading,
- memory matters in simulations,
- robustness matters more than micro-optimizations.

Choose trade-offs intentionally.

---

## Key takeaways

- Faster code often uses more memory.
- Python performance depends on algorithm choice.
- Optimize only after correctness.


---

## Exercises


**Exercise 1.**
Implement a Fibonacci function in two ways: (a) naive recursion (O(2^n) time, O(n) space) and (b) memoized version using a dictionary (O(n) time, O(n) space). Compare their execution times for `n = 30`.

??? success "Solution to Exercise 1"

    ```python
    import time

    def fib_naive(n):
        if n <= 1:
            return n
        return fib_naive(n - 1) + fib_naive(n - 2)

    def fib_memo(n, memo={}):
        if n in memo:
            return memo[n]
        if n <= 1:
            return n
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
        return memo[n]

    start = time.perf_counter()
    fib_naive(30)
    naive_time = time.perf_counter() - start

    start = time.perf_counter()
    fib_memo(30)
    memo_time = time.perf_counter() - start

    print(f"Naive:    {naive_time:.4f}s")
    print(f"Memoized: {memo_time:.6f}s")
    ```

    Memoization trades O(n) memory for eliminating redundant computation, reducing time from exponential to linear.

---

**Exercise 2.**
Demonstrate the time-space tradeoff by implementing a function that checks for duplicate elements in a list. Write one version that uses O(1) extra space (nested loops, O(n^2) time) and one that uses O(n) extra space (set, O(n) time). Compare for a list of 5,000 elements.

??? success "Solution to Exercise 2"

    ```python
    import time

    def has_dupes_quadratic(lst):
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                if lst[i] == lst[j]:
                    return True
        return False

    def has_dupes_linear(lst):
        seen = set()
        for item in lst:
            if item in seen:
                return True
            seen.add(item)
        return False

    data = list(range(5000))  # no duplicates (worst case)

    start = time.perf_counter()
    has_dupes_quadratic(data)
    quad_time = time.perf_counter() - start

    start = time.perf_counter()
    has_dupes_linear(data)
    lin_time = time.perf_counter() - start

    print(f"O(n^2): {quad_time:.4f}s")
    print(f"O(n):   {lin_time:.6f}s")
    ```

    The set-based approach uses extra memory proportional to the input size but provides O(1) lookups, making the overall check O(n).

---

**Exercise 3.**
Explain why `functools.lru_cache` is an example of the time-space tradeoff. Write a decorated function that computes factorials and show that repeated calls with the same argument are instant after the first call.

??? success "Solution to Exercise 3"

    ```python
    import functools
    import time

    @functools.lru_cache(maxsize=None)
    def factorial(n):
        if n <= 1:
            return 1
        return n * factorial(n - 1)

    # First call: computes and caches
    start = time.perf_counter()
    factorial(500)
    first_time = time.perf_counter() - start

    # Second call: returns cached result
    start = time.perf_counter()
    factorial(500)
    second_time = time.perf_counter() - start

    print(f"First call:  {first_time:.6f}s")
    print(f"Second call: {second_time:.6f}s")
    print(f"Cache info:  {factorial.cache_info()}")
    ```

    `lru_cache` stores previously computed results in memory (space cost) so that identical calls return instantly (time saving). This is the classic time-space tradeoff.
