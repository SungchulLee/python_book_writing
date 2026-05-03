# sys.setrecursionlimit()

Python limits recursion depth to prevent stack overflow. The default is typically 1000. Understanding and adjusting this limit is important for deep recursion.

!!! tip "Mental Model"
    Python's recursion limit is a safety guardrail, not a performance knob. Each recursive call consumes real stack memory, and exceeding the OS stack size crashes the interpreter. Raising the limit lets deeper recursion succeed, but the real fix for deep problems is usually converting to iteration or using `sys.setrecursionlimit` together with `threading.stack_size`.

---

## The Default Limit

```python
import sys

# Check current limit
print(f"Default recursion limit: {sys.getrecursionlimit()}")
# Output: Default recursion limit: 1000

# Each recursive call uses stack space
def count_depth(n):
    if n == 0:
        return n
    return count_depth(n - 1)

try:
    result = count_depth(1000)
    print("Reached depth 1000")
except RecursionError:
    print("RecursionError: maximum recursion depth exceeded")
```

## Increasing the Limit

```python
import sys

# Increase the limit
sys.setrecursionlimit(5000)
print(f"New recursion limit: {sys.getrecursionlimit()}")

# Now deeper recursion works
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# This now works (would fail with default limit)
result = factorial(2000)
print(f"factorial(2000) computed successfully")
```

## When to Increase

```python
import sys

def process_deep_tree(node, depth=0):
    '''Process deeply nested tree structure'''
    if node is None:
        return
    
    # Process node
    if depth % 100 == 0:
        print(f"Depth: {depth}")
    
    process_deep_tree(node.left, depth + 1)
    process_deep_tree(node.right, depth + 1)

# For deep structures, increase limit temporarily
old_limit = sys.getrecursionlimit()
sys.setrecursionlimit(10000)
try:
    process_deep_tree(root)
finally:
    sys.setrecursionlimit(old_limit)  # Restore original
```

## Caveats

```python
import sys

# Set too high: risk actual stack overflow (hard crash)
sys.setrecursionlimit(1000000)  # Dangerous!

# Better practice: increase moderately for specific task
sys.setrecursionlimit(5000)

# Watch for:
# - Memory consumption increases with limit
# - Stack overflows might not give clean errors
# - Prefer iteration for deep recursion
```

## Best Practices

```python
import sys

def safe_deep_recursion(data):
    '''Safely handle potentially deep recursion'''
    old_limit = sys.getrecursionlimit()
    
    # Increase limit for this operation only
    sys.setrecursionlimit(10000)
    
    try:
        return process_recursively(data)
    finally:
        # Always restore original limit
        sys.setrecursionlimit(old_limit)
```

## Alternative: Use Iteration

For very deep recursion, prefer iteration:

```python
# Recursive: limited by sys.getrecursionlimit()
def sum_recursive(numbers):
    if not numbers:
        return 0
    return numbers[0] + sum_recursive(numbers[1:])

# Iterative: no limit
def sum_iterative(numbers):
    return sum(numbers)
```

---

## Exercises

**Exercise 1.**
Write a script that checks the current recursion limit with `sys.getrecursionlimit()`, then writes a recursive function `depth_test(n)` that recurses `n` times. Call it with increasing values until you hit `RecursionError`. Print the exact depth at which the error occurs.

??? success "Solution to Exercise 1"

        import sys

        def depth_test(n):
            if n == 0:
                return 0
            return depth_test(n - 1)

        limit = sys.getrecursionlimit()
        print(f"Recursion limit: {limit}")

        low, high = 1, limit + 100
        max_depth = 0
        while low <= high:
            mid = (low + high) // 2
            try:
                depth_test(mid)
                max_depth = mid
                low = mid + 1
            except RecursionError:
                high = mid - 1

        print(f"Max depth before RecursionError: {max_depth}")

---

**Exercise 2.**
Write a `safe_recursion(limit)` context manager that temporarily increases the recursion limit to `limit`, then restores the original value. Use it to safely call a deeply recursive function with depth 3000 without permanently changing the system limit.

??? success "Solution to Exercise 2"

        import sys

        class safe_recursion:
            def __init__(self, limit):
                self.limit = limit

            def __enter__(self):
                self.old_limit = sys.getrecursionlimit()
                sys.setrecursionlimit(self.limit)
                return self

            def __exit__(self, *args):
                sys.setrecursionlimit(self.old_limit)

        def deep_function(n):
            if n == 0:
                return 0
            return deep_function(n - 1)

        with safe_recursion(5000):
            result = deep_function(3000)
            print(f"Reached depth 3000, result = {result}")

        print(f"Limit restored: {sys.getrecursionlimit()}")

---

**Exercise 3.**
Convert the recursive function `def sum_to(n): return 0 if n <= 0 else n + sum_to(n - 1)` into an iterative version. Then demonstrate that the recursive version fails for `n = 5000` (with the default limit) while the iterative version succeeds.

??? success "Solution to Exercise 3"

        import sys

        # Recursive version
        def sum_to_recursive(n):
            if n <= 0:
                return 0
            return n + sum_to_recursive(n - 1)

        # Iterative version
        def sum_to_iterative(n):
            total = 0
            for i in range(1, n + 1):
                total += i
            return total

        # Iterative works for large n
        print(sum_to_iterative(5000))  # 12502500

        # Recursive fails for large n
        try:
            sum_to_recursive(5000)
        except RecursionError:
            print("RecursionError: recursive version failed at n=5000")
