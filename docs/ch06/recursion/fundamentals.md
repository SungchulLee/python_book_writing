# Recursion and Stack

## Introduction

**Recursion** is a programming technique where a function calls itself to solve a problem by breaking it down into smaller, similar subproblems. While recursion can provide elegant solutions to certain problems, it requires careful management to avoid stack overflow errors.

This chapter covers recursive functions, how they work, the call stack during recursion, common recursive patterns, optimization techniques, and how to prevent and handle stack overflow errors.

!!! tip "Mental Model"
    Recursion is a function solving a problem by asking itself to solve a smaller version of the same problem. Every recursive function needs two things: a base case that stops the descent, and a recursive case that shrinks the problem. Each call pushes a frame onto the call stack, and the answers bubble back up as frames pop off.

## What is Recursion?

A recursive function has two key components:

1. **Base case**: The condition that stops the recursion
2. **Recursive case**: The function calling itself with modified arguments

```python
def countdown(n):
    # Base case
    if n <= 0:
        print("Blast off!")
        return
    
    # Recursive case
    print(n)
    countdown(n - 1)

countdown(5)
# Output:
# 5
# 4
# 3
# 2
# 1
# Blast off!
```

### 1. How Recursion Works

Each recursive call creates a new stack frame:

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

result = factorial(4)
# Call stack
# factorial(4) -> 4 *
# > 4 * 3 *
# > 4 * 3 * 2 *
# > 4 * 3 * 2 * 1 *
# > 4 * 3 * 2 * 1 * 1 (base case: factorial(0) = 1)
# Result: 24
```

### 2. Recursion vs Iteration

Many recursive problems can be solved iteratively:

```python
# Recursive factorial
def factorial_recursive(n):
    if n == 0:
        return 1
    return n * factorial_recursive(n - 1)

# Iterative factorial
def factorial_iterative(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

print(factorial_recursive(5))  # 120
print(factorial_iterative(5))  # 120
```

**When to use recursion**:

- Problem has recursive structure (tree traversal, divide-and-conquer)
- Code clarity matters more than performance
- Problem is naturally expressed recursively

**When to use iteration**:

- Simple loops suffice
- Performance is critical
- Avoiding stack overflow is important

## Classic Recursive Patterns

### 1. Factorial

```python
def factorial(n):
    """Calculate n! recursively."""
    # Base case
    if n == 0 or n == 1:
        return 1
    # Recursive case
    return n * factorial(n - 1)

print(factorial(5))  # 120
print(factorial(0))  # 1
```

### 2. Fibonacci

```python
def fibonacci(n):
    """Return the nth Fibonacci number."""
    # Base cases
    if n == 0:
        return 0
    if n == 1:
        return 1
    # Recursive case
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(6))  # 8
# Sequence: 0, 1, 1,
```

**Warning**: Naive Fibonacci is extremely inefficient due to repeated calculations!

### 1. Sum of List

```python
def sum_list(numbers):
    """Sum all numbers in a list recursively."""
    # Base case
    if not numbers:
        return 0
    # Recursive case
    return numbers[0] + sum_list(numbers[1:])

print(sum_list([1, 2, 3, 4, 5]))  # 15
```

### 2. Reverse String

```python
def reverse_string(s):
    """Reverse a string recursively."""
    # Base case
    if len(s) <= 1:
        return s
    # Recursive case
    return s[-1] + reverse_string(s[:-1])

print(reverse_string("hello"))  # olleh
```

### 3. Power Function

```python
def power(base, exp):
    """Calculate base^exp recursively."""
    # Base case
    if exp == 0:
        return 1
    # Recursive case
    return base * power(base, exp - 1)

print(power(2, 5))  # 32
```

## The Call Stack in Recursion

### 1. Stack Frame

Each recursive call adds a frame to the call stack:

```python
def factorial(n):
    print(f"Called with n={n}")
    if n == 0:
        print("Base case reached")
        return 1
    result = n * factorial(n - 1)
    print(f"Returning {result} for n={n}")
    return result

factorial(4)
```

**Output**:
```
Called with n=4
Called with n=3
Called with n=2
Called with n=1
Called with n=0
Base case reached
Returning 1 for n=1
Returning 2 for n=2
Returning 6 for n=3
Returning 24 for n=4
```

**Stack visualization**:
```
Step 1: factorial(4) calls factorial(3)
Stack: [factorial(4)]

Step 2: factorial(3) calls factorial(2)
Stack: [factorial(4), factorial(3)]

Step 3: factorial(2) calls factorial(1)
Stack: [factorial(4), factorial(3), factorial(2)]

Step 4: factorial(1) calls factorial(0)
Stack: [factorial(4), factorial(3), factorial(2), factorial(1)]

Step 5: factorial(0) returns 1 (base case)
Stack: [factorial(4), factorial(3), factorial(2), factorial(1)]

Step 6: factorial(1) returns 1
Stack: [factorial(4), factorial(3), factorial(2)]

Step 7: factorial(2) returns 2
Stack: [factorial(4), factorial(3)]

Step 8: factorial(3) returns 6
Stack: [factorial(4)]

Step 9: factorial(4) returns 24
Stack: []
```

## Stack Overflow

### 1. What is Stack Overflow

**Stack overflow** occurs when the call stack grows too large and exceeds the system's memory limit.

### 2. Causes of Stack Overflow

1. **No base case**:
```python
def infinite_recursion(n):
    # No base case!
    return infinite_recursion(n - 1)

# infinite_recursion(1
```

2. **Base case never reached**:
```python
def buggy_countdown(n):
    if n == 0:  # Base case
        return
    print(n)
    buggy_countdown(n + 1)  # Goes wrong direction!

# buggy_countdown(5) #
```

3. **Too many recursive calls**:
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# fibonacci(1000)  # RecursionError!
```

### 3. Python's Recursion Limit

Python has a default recursion limit (usually 1000):

```python
import sys

# Check current limit
print(sys.getrecursionlimit())  # 1000 (default)

# Increase limit (use with caution)
sys.setrecursionlimit(5000)

# Test limit
def test_depth(n):
    if n == 0:
        return
    test_depth(n - 1)

try:
    test_depth(2000)
    print("Success!")
except RecursionError:
    print("RecursionError: maximum recursion depth exceeded")
```

**Warning**: Increasing the recursion limit doesn't add memory—it just allows deeper recursion before hitting the actual memory limit!

### 4. Detecting Stack Overflow

```python
def safe_recursion(n):
    try:
        if n == 0:
            return 0
        return n + safe_recursion(n - 1)
    except RecursionError:
        print("Recursion limit exceeded!")
        return -1

result = safe_recursion(5000)
```

## Avoiding Stack Overflow

### 1. Use Iteration

Convert recursion to loops:

```python
# Recursive (can overflow)
def sum_recursive(n):
    if n == 0:
        return 0
    return n + sum_recursive(n - 1)

# Iterative (safe)
def sum_iterative(n):
    total = 0
    for i in range(n + 1):
        total += i
    return total

print(sum_iterative(10000))  # No problem!
```

### 2. Tail Recursion

A function is **tail recursive** if the recursive call is the last operation:

```python
# Not tail recursive
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)  # Operation after recursion

# Tail recursive
def factorial_tail(n, accumulator=1):
    if n == 0:
        return accumulator
    return factorial_tail(n - 1, n * accumulator)  # No operation after

print(factorial_tail(5))  # 120
```

**Note**: Python doesn't optimize tail recursion (unlike some languages), so this doesn't prevent stack overflow by itself.

### 3. Memoization

Cache results to avoid repeated calculations:

```python
# Naive Fibonacci
def fib_naive(n):
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

# Memoized Fibonacci
def fib_memo(n, cache=None):
    if cache is None:
        cache = {}
    
    if n in cache:
        return cache[n]
    
    if n <= 1:
        return n
    
    cache[n] = fib_memo(n - 1, cache) + fib_memo(n - 2, cache)
    return cache[n]

# Using decorator
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_cached(n):
    if n <= 1:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)

print(fib_cached(100))  # Fast!
```

### 4. Increase Stack Size

```python
import sys
import threading

# Increase thread stack size
threading.stack_size(67108864)  # 64 MB

def deep_recursion(n):
    if n == 0:
        return 0
    return deep_recursion(n - 1) + 1

# Run in thread with larger stack
thread = threading.Thread(target=lambda: print(deep_recursion(50000)))
thread.start()
thread.join()
```

### 5. Convert to Dynamic Programming

```python
# Recursive Fibonacci
def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)

# Dynamic programming
def fib_dp(n):
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]

print(fib_dp(1000))  # Fast and safe!
```

## Advanced Recursive Patterns

### 1. Multiple Recursive Calls

```python
def fibonacci(n):
    """Two recursive calls per function."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Tree-like recursion
```

### 1. Mutual Recursion

Functions calling each other:

```python
def is_even(n):
    """Check if n is even using mutual recursion."""
    if n == 0:
        return True
    return is_odd(n - 1)

def is_odd(n):
    """Check if n is odd using mutual recursion."""
    if n == 0:
        return False
    return is_even(n - 1)

print(is_even(4))  # True
print(is_odd(5))   # True
```

### 2. Tree Recursion

Recursing through tree structures:

```python
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def tree_sum(node):
    """Sum all values in binary tree."""
    if node is None:
        return 0
    return node.value + tree_sum(node.left) + tree_sum(node.right)

#       1
#      / \
#     2   3
#    / \
#   4   5

root = TreeNode(1,
    TreeNode(2, TreeNode(4), TreeNode(5)),
    TreeNode(3)
)

print(tree_sum(root))  # 15
```

### 3. Backtracking

Try different paths and backtrack if they don't work:

```python
def find_path(maze, x, y, path=[]):
    """Find path through maze using backtracking."""
    # Check bounds and if position is valid
    if x < 0 or y < 0 or x >= len(maze) or y >= len(maze[0]):
        return False
    if maze[x][y] == 1:  # Wall
        return False
    if (x, y) in path:  # Already visited
        return False
    
    # Add current position to path
    path.append((x, y))
    
    # Check if reached goal
    if maze[x][y] == 9:
        return True
    
    # Try all four directions
    if (find_path(maze, x + 1, y, path) or
        find_path(maze, x - 1, y, path) or
        find_path(maze, x, y + 1, path) or
        find_path(maze, x, y - 1, path)):
        return True
    
    # Backtrack
    path.pop()
    return False

maze = [
    [0, 0, 1, 0],
    [0, 0, 0, 0],
    [1, 0, 1, 0],
    [0, 0, 0, 9]
]

path = []
if find_path(maze, 0, 0, path):
    print("Path found:", path)
```

### 4. Divide and Conquer

```python
def merge_sort(arr):
    """Sort array using divide and conquer."""
    # Base case
    if len(arr) <= 1:
        return arr
    
    # Divide
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Conquer (merge)
    return merge(left, right)

def merge(left, right):
    """Merge two sorted arrays."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

print(merge_sort([38, 27, 43, 3, 9, 82, 10]))
# [3, 9, 10, 27, 38, 43, 82]
```

## Recursion Best Practices

### 1. Always Have a Base Case

```python
# Wrong - no base case
def infinite(n):
    return infinite(n - 1)  # Never stops!

# Correct - clear base case
def countdown(n):
    if n <= 0:  # Base case
        return
    print(n)
    countdown(n - 1)
```

### 2. Ensure Progress Toward Base Case

```python
# Wrong - not progressing
def bad_factorial(n):
    if n == 0:
        return 1
    return n * bad_factorial(n)  # n doesn't change!

# Correct - making progress
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)  # n decreases
```

### 3. Use Meaningful Names

```python
# Poor
def f(n):
    if n == 0:
        return 0
    return n + f(n - 1)

# Better
def sum_to_n(n):
    if n == 0:
        return 0
    return n + sum_to_n(n - 1)
```

### 4. Consider Alternatives

```python
# Recursion overkill
def sum_recursive(numbers):
    if not numbers:
        return 0
    return numbers[0] + sum_recursive(numbers[1:])

# Better - use built-in
total = sum(numbers)
```

### 5. Add Safeguards

```python
def safe_factorial(n, max_depth=100):
    """Factorial with depth limit."""
    if max_depth <= 0:
        raise RecursionError("Maximum recursion depth reached")
    if n == 0:
        return 1
    return n * safe_factorial(n - 1, max_depth - 1)
```

### 6. Document Recursive Functions

```python
def fibonacci(n):
    """
    Calculate the nth Fibonacci number recursively.
    
    Args:
        n (int): Position in Fibonacci sequence (n >= 0)
    
    Returns:
        int: The nth Fibonacci number
    
    Raises:
        ValueError: If n is negative
    
    Note:
        This implementation is inefficient for large n.
        Consider using memoization or iteration.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

## Debugging Recursive Functions

### 1. Add Print Statements

```python
def factorial(n, depth=0):
    indent = "  " * depth
    print(f"{indent}factorial({n}) called")
    
    if n == 0:
        print(f"{indent}Base case: returning 1")
        return 1
    
    result = n * factorial(n - 1, depth + 1)
    print(f"{indent}factorial({n}) returning {result}")
    return result

factorial(4)
```

### 2. Visualize the Call Stack

```python
def visualize_recursion(func):
    """Decorator to visualize recursive calls."""
    def wrapper(n, depth=0):
        print("  " * depth + f"-> {func.__name__}({n})")
        result = func(n)
        print("  " * depth + f"<- {result}")
        return result
    return wrapper

@visualize_recursion
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### 3. Set Breakpoints

```python
def debug_factorial(n):
    if n == 2:  # Set breakpoint condition
        import pdb; pdb.set_trace()
    
    if n == 0:
        return 1
    return n * debug_factorial(n - 1)
```

## Quick Reference

### 1. Recursive Function Template
```python
def recursive_function(parameters):
    # Base case(s)
    if base_condition:
        return base_value
    
    # Recursive case
    # 1. Modify parameters
    # 2. Make recursive call
    # 3. Combine results
    return combine(recursive_function(modified_parameters))
```

### 2. Common Patterns
```python
# Linear recursion
def linear(n):
    if n == 0:
        return base
    return combine(n, linear(n - 1))

# Tree recursion
def tree(n):
    if n == 0:
        return base
    return combine(tree(n-1), tree(n-2))

# Tail recursion
def tail(n, acc=initial):
    if n == 0:
        return acc
    return tail(n - 1, update(acc, n))
```

### 3. Avoiding Stack Overflow
```python
# Use iteration
for i in range(n):
    ...

# Use memoization
from functools import lru_cache
@lru_cache(maxsize=None)
def func(n):
    ...

# Check depth
if depth > MAX_DEPTH:
    raise RecursionError()

# Increase limit
import sys
sys.setrecursionlimit(new_limit)
```

## Summary

- **Recursion**: Function calling itself with simpler inputs
- **Base case**: Stopping condition (essential!)
- **Recursive case**: Function calling itself
- **Call stack**: Tracks all active function calls
- **Stack overflow**: Occurs when call stack grows too large
- **Python recursion limit**: Default 1000 calls
- **Avoidance strategies**: Iteration, memoization, tail recursion, dynamic programming
- **Best practices**: Clear base case, progress toward base case, add safeguards
- **When to use**: Tree structures, divide-and-conquer, naturally recursive problems
- **When not to use**: Simple loops, performance-critical code, deep recursion

Recursion is a powerful technique but requires careful implementation. Understanding the call stack and potential for stack overflow is crucial for writing correct, efficient recursive functions.

---

## Runnable Example: `recursion_examples.py`

```python
"""
Python Recursion - Examples
See recursion in action with these demonstrations!
"""

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    print("="*60)
    print("EXAMPLE 1: Simple Countdown")
    print("="*60)

    def countdown(n):
        if n <= 0:
            print("Blastoff!")
        else:
            print(n)
            countdown(n - 1)

    countdown(5)
    print()

    print("="*60)
    print("EXAMPLE 2: Factorial")
    print("="*60)

    def factorial(n):
        """Calculate n! recursively"""
        if n <= 1:
            return 1
        return n * factorial(n - 1)

    print(f"5! = {factorial(5)}")
    print(f"7! = {factorial(7)}")
    print()

    print("="*60)
    print("EXAMPLE 3: Fibonacci Sequence")
    print("="*60)

    def fibonacci(n):
        """Return nth Fibonacci number"""
        if n == 0:
            return 0
        if n == 1:
            return 1
        return fibonacci(n - 1) + fibonacci(n - 2)

    print("First 10 Fibonacci numbers:")
    for i in range(10):
        print(f"F({i}) = {fibonacci(i)}")
    print()

    print("="*60)
    print("EXAMPLE 4: Sum of Numbers")
    print("="*60)

    def sum_numbers(n):
        """Sum numbers from 1 to n"""
        if n == 0:
            return 0
        return n + sum_numbers(n - 1)

    print(f"Sum 1 to 10: {sum_numbers(10)}")
    print(f"Sum 1 to 100: {sum_numbers(100)}")
    print()

    print("="*60)
    print("EXAMPLE 5: Power Function")
    print("="*60)

    def power(base, exp):
        """Calculate base^exp recursively"""
        if exp == 0:
            return 1
        return base * power(base, exp - 1)

    print(f"2^5 = {power(2, 5)}")
    print(f"3^4 = {power(3, 4)}")
    print()

    print("="*60)
    print("EXAMPLE 6: Reverse a String")
    print("="*60)

    def reverse_string(s):
        """Reverse string recursively"""
        if len(s) <= 1:
            return s
        return s[-1] + reverse_string(s[:-1])

    print(f"'hello' reversed: {reverse_string('hello')}")
    print(f"'Python' reversed: {reverse_string('Python')}")
    print()

    print("="*60)
    print("EXAMPLE 7: Sum of List")
    print("="*60)

    def sum_list(numbers):
        """Sum all numbers in list"""
        if len(numbers) == 0:
            return 0
        return numbers[0] + sum_list(numbers[1:])

    print(f"Sum of [1,2,3,4,5]: {sum_list([1,2,3,4,5])}")
    print(f"Sum of [10,20,30]: {sum_list([10,20,30])}")
    print()

    print("="*60)
    print("EXAMPLE 8: Count Occurrences")
    print("="*60)

    def count_occurrences(lst, target):
        """Count how many times target appears in list"""
        if len(lst) == 0:
            return 0
        count = 1 if lst[0] == target else 0
        return count + count_occurrences(lst[1:], target)

    numbers = [1, 2, 3, 2, 4, 2, 5]
    print(f"List: {numbers}")
    print(f"Count of 2: {count_occurrences(numbers, 2)}")
    print()

    print("="*60)
    print("EXAMPLE 9: Greatest Common Divisor (GCD)")
    print("="*60)

    def gcd(a, b):
        """Calculate GCD using Euclidean algorithm"""
        if b == 0:
            return a
        return gcd(b, a % b)

    print(f"GCD(48, 18) = {gcd(48, 18)}")
    print(f"GCD(100, 35) = {gcd(100, 35)}")
    print()

    print("="*60)
    print("EXAMPLE 10: Binary Search")
    print("="*60)

    def binary_search(arr, target, left, right):
        """Search for target in sorted array"""
        if left > right:
            return -1

        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            return binary_search(arr, target, left, mid - 1)
        else:
            return binary_search(arr, target, mid + 1, right)

    sorted_array = [1, 3, 5, 7, 9, 11, 13, 15]
    print(f"Array: {sorted_array}")
    print(f"Search for 7: index {binary_search(sorted_array, 7, 0, len(sorted_array)-1)}")
    print(f"Search for 13: index {binary_search(sorted_array, 13, 0, len(sorted_array)-1)}")
    print(f"Search for 6: index {binary_search(sorted_array, 6, 0, len(sorted_array)-1)}")
    print()

    print("="*60)
    print("EXAMPLE 11: Palindrome Checker")
    print("="*60)

    def is_palindrome(s):
        """Check if string is palindrome"""
        # Remove spaces and convert to lowercase
        s = s.lower().replace(" ", "")

        # Base cases
        if len(s) <= 1:
            return True

        # Check first and last character
        if s[0] != s[-1]:
            return False

        # Recurse on middle part
        return is_palindrome(s[1:-1])

    print(f"'racecar' is palindrome: {is_palindrome('racecar')}")
    print(f"'hello' is palindrome: {is_palindrome('hello')}")
    print(f"'A man a plan a canal Panama' is palindrome: {is_palindrome('A man a plan a canal Panama')}")
    print()

    print("="*60)
    print("EXAMPLE 12: Flatten Nested List")
    print("="*60)

    def flatten(nested_list):
        """Flatten a nested list"""
        result = []
        for item in nested_list:
            if isinstance(item, list):
                result.extend(flatten(item))
            else:
                result.append(item)
        return result

    nested = [1, [2, 3], [4, [5, 6]], 7]
    print(f"Nested: {nested}")
    print(f"Flattened: {flatten(nested)}")
    print()

    print("="*60)
    print("EXAMPLE 13: Print All Permutations")
    print("="*60)

    def permutations(s):
        """Generate all permutations of string"""
        if len(s) <= 1:
            return [s]

        result = []
        for i, char in enumerate(s):
            rest = s[:i] + s[i+1:]
            for perm in permutations(rest):
                result.append(char + perm)
        return result

    print(f"Permutations of 'ABC': {permutations('ABC')}")
    print()

    print("="*60)
    print("EXAMPLE 14: Tower of Hanoi")
    print("="*60)

    def tower_of_hanoi(n, source, destination, auxiliary):
        """Solve Tower of Hanoi puzzle"""
        if n == 1:
            print(f"Move disk 1 from {source} to {destination}")
            return

        tower_of_hanoi(n-1, source, auxiliary, destination)
        print(f"Move disk {n} from {source} to {destination}")
        tower_of_hanoi(n-1, auxiliary, destination, source)

    print("Tower of Hanoi with 3 disks:")
    tower_of_hanoi(3, 'A', 'C', 'B')
    print()

    print("="*60)
    print("EXAMPLE 15: Fibonacci with Memoization")
    print("="*60)

    def fibonacci_memo(n, memo=None):
        """Optimized Fibonacci with memoization"""
        if memo is None:
            memo = {}

        if n in memo:
            return memo[n]

        if n <= 1:
            return n

        memo[n] = fibonacci_memo(n-1, memo) + fibonacci_memo(n-2, memo)
        return memo[n]

    print("Computing Fibonacci(30) with memoization:")
    print(f"F(30) = {fibonacci_memo(30)}")
    print(f"F(40) = {fibonacci_memo(40)}")
    print("(Much faster than regular recursion!)")
    print()

    print("="*60)
    print("EXAMPLE 16: Count Digits")
    print("="*60)

    def count_digits(n):
        """Count number of digits"""
        if n < 10:
            return 1
        return 1 + count_digits(n // 10)

    print(f"Digits in 12345: {count_digits(12345)}")
    print(f"Digits in 987654321: {count_digits(987654321)}")
    print()

    print("="*60)
    print("EXAMPLE 17: Digital Root")
    print("="*60)

    def digital_root(n):
        """Find digital root (sum digits until single digit)"""
        if n < 10:
            return n

        digit_sum = 0
        while n > 0:
            digit_sum += n % 10
            n //= 10

        return digital_root(digit_sum)

    print(f"Digital root of 38: {digital_root(38)}")  # 3+8=11, 1+1=2
    print(f"Digital root of 1234: {digital_root(1234)}")  # 1+2+3+4=10, 1+0=1
    print()

    print("="*60)
    print("EXAMPLE 18: List Maximum")
    print("="*60)

    def find_max(lst):
        """Find maximum in list recursively"""
        if len(lst) == 1:
            return lst[0]

        max_of_rest = find_max(lst[1:])
        return lst[0] if lst[0] > max_of_rest else max_of_rest

    numbers = [3, 7, 2, 9, 1, 5, 8]
    print(f"List: {numbers}")
    print(f"Maximum: {find_max(numbers)}")
    print()

    print("="*60)
    print("EXAMPLE 19: String to Integer")
    print("="*60)

    def string_to_int(s):
        """Convert string to integer recursively"""
        if len(s) == 1:
            return int(s)
        return int(s[0]) * (10 ** (len(s)-1)) + string_to_int(s[1:])

    print(f"'1234' to int: {string_to_int('1234')}")
    print(f"'987' to int: {string_to_int('987')}")
    print()

    print("="*60)
    print("EXAMPLE 20: Recursive vs Iterative Comparison")
    print("="*60)

    def sum_recursive(n):
        """Sum 1 to n recursively"""
        if n == 0:
            return 0
        return n + sum_recursive(n - 1)

    def sum_iterative(n):
        """Sum 1 to n iteratively"""
        total = 0
        for i in range(1, n + 1):
            total += i
        return total

    n = 10
    print(f"Sum 1 to {n}:")
    print(f"  Recursive: {sum_recursive(n)}")
    print(f"  Iterative: {sum_iterative(n)}")
    print(f"  Both give same result!")
    print()

    print("="*60)
    print("All examples completed!")
    print("="*60)
    print("\nKey Insights:")
    print("• Recursion breaks problems into smaller pieces")
    print("• Always need a base case to stop")
    print("• Recursive case moves toward base case")
    print("• Many problems have both recursive and iterative solutions")
    print("• Memoization can dramatically improve performance")
    print("• Choose recursion when it makes code clearer")
```

---

## Exercises

**Exercise 1.**
Write a recursive function `reverse_string(s)` that reverses a string without using slicing or built-in `reversed()`. The base case is when the string has 0 or 1 characters. Verify with `"hello"` (expected: `"olleh"`).

??? success "Solution to Exercise 1"

        def reverse_string(s):
            # Base case
            if len(s) <= 1:
                return s
            # Recursive case: last char + reverse of the rest
            return s[-1] + reverse_string(s[:-1])

        print(reverse_string("hello"))    # olleh
        print(reverse_string("abcdef"))   # fedcba
        print(reverse_string("a"))        # a
        print(reverse_string(""))         # (empty)

---

**Exercise 2.**
Write a recursive function `is_palindrome(s)` that returns `True` if a string reads the same forwards and backwards, ignoring case. The base case is when the string has 0 or 1 characters. Test with `"racecar"`, `"Madam"`, and `"hello"`.

??? success "Solution to Exercise 2"

        def is_palindrome(s):
            s = s.lower()
            # Base case
            if len(s) <= 1:
                return True
            # Recursive case
            if s[0] != s[-1]:
                return False
            return is_palindrome(s[1:-1])

        print(is_palindrome("racecar"))  # True
        print(is_palindrome("Madam"))    # True
        print(is_palindrome("hello"))    # False

---

**Exercise 3.**
Write a recursive function `flatten(data)` that takes an arbitrarily nested list structure and returns a flat list. For example, `flatten([1, [2, [3, [4]], 5]])` returns `[1, 2, 3, 4, 5]`. Identify the base case and recursive case clearly.

??? success "Solution to Exercise 3"

        def flatten(data):
            result = []
            for item in data:
                if isinstance(item, list):
                    # Recursive case: flatten the nested list
                    result.extend(flatten(item))
                else:
                    # Base case: non-list element
                    result.append(item)
            return result

        print(flatten([1, [2, [3, [4]], 5]]))     # [1, 2, 3, 4, 5]
        print(flatten([[1, 2], [3, [4, [5]]]]))   # [1, 2, 3, 4, 5]
        print(flatten([]))                         # []
