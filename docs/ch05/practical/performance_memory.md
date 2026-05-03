# Performance and Memory

Techniques for writing efficient Python code with optimal memory usage.

!!! tip "Mental Model"
    Performance and memory are two sides of the same coin. Using more memory (caching, pre-computation) often buys speed; using less memory (generators, lazy evaluation) sometimes costs speed. The art is profiling both dimensions and finding the sweet spot for your specific workload.

## Measuring Performance

### Using `timeit`

```python
import timeit

# Time a simple statement
time = timeit.timeit('sum(range(100))', number=10000)
print(f"Time: {time:.4f}s")

# Time a function
def my_function():
    return [x**2 for x in range(1000)]

time = timeit.timeit(my_function, number=1000)
print(f"Time: {time:.4f}s")

# Compare approaches
list_time = timeit.timeit('[x**2 for x in range(1000)]', number=1000)
gen_time = timeit.timeit('list(x**2 for x in range(1000))', number=1000)
print(f"List comp: {list_time:.4f}s, Generator: {gen_time:.4f}s")
```

### Using `cProfile`

```python
import cProfile

def slow_function():
    result = []
    for i in range(10000):
        result.append(i ** 2)
    return result

# Profile the function
cProfile.run('slow_function()')
```

---

## Performance Optimizations

### Use Comprehensions

Comprehensions are faster than equivalent loops:

```python
# Fast: list comprehension
squares = [x**2 for x in range(1000)]

# Slower: explicit loop
squares = []
for x in range(1000):
    squares.append(x**2)
```

### Local Variable Caching

Accessing local variables is faster than global lookups:

```python
# Slower: global lookup each iteration
def slow():
    for i in range(10000):
        len([1, 2, 3])  # Looks up len() each time

# Faster: cache the function locally
def fast():
    _len = len  # Local reference
    for i in range(10000):
        _len([1, 2, 3])
```

### Use Built-in Functions

Built-in functions are implemented in C and optimized:

```python
# Fast: built-in sum
total = sum(numbers)

# Slower: manual loop
total = 0
for n in numbers:
    total += n

# Fast: built-in map
result = list(map(str, numbers))

# Slower: list comprehension for simple transforms
result = [str(n) for n in numbers]
```

### String Joining

```python
# Fast: join method
result = ''.join(strings)

# Slow: concatenation in loop
result = ''
for s in strings:
    result += s  # Creates new string each time
```

### Use `collections` Module

```python
from collections import Counter, defaultdict, deque

# Fast counting
counts = Counter(words)

# Fast grouping
groups = defaultdict(list)
for item in items:
    groups[item.category].append(item)

# Fast append/pop from both ends
queue = deque()
queue.append(item)      # O(1)
queue.appendleft(item)  # O(1)
```

---

## Memory Efficiency

### Generators for Lazy Evaluation

Generators produce values on-demand, avoiding memory allocation for entire sequences:

```python
# Memory efficient: generator expression
gen = (x**2 for x in range(10000000))

# Memory expensive: list comprehension
lst = [x**2 for x in range(10000000)]  # All in memory at once

# Generator function
def squares(n):
    for x in range(n):
        yield x**2

# Process without loading all into memory
for square in squares(10000000):
    process(square)
```

### `__slots__` for Classes

Reduce memory overhead when creating many instances:

```python
# Without __slots__: ~152 bytes per instance
class PointRegular:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# With __slots__: ~56 bytes per instance
class PointSlots:
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Significant savings with many instances
points = [PointSlots(i, i) for i in range(1000000)]
```

### Use `array` for Homogeneous Data

```python
import array

# Regular list: ~8MB for 1M integers
lst = list(range(1000000))

# Array: ~4MB for 1M integers
arr = array.array('i', range(1000000))
```

### Avoid Unnecessary Copies

```python
# Creates copy (uses memory)
subset = large_list[100:200]

# Use iterator (no copy)
import itertools
subset = itertools.islice(large_list, 100, 200)

# Process in chunks
def chunked(iterable, size):
    it = iter(iterable)
    while chunk := list(itertools.islice(it, size)):
        yield chunk

for chunk in chunked(large_data, 1000):
    process(chunk)
```

### Delete Large Objects

```python
def process_large_data():
    data = load_huge_file()  # 1GB
    result = compute(data)
    
    del data  # Free memory immediately
    gc.collect()  # Optional: force garbage collection
    
    return result
```

---

## Profiling Memory

```python
import sys
import tracemalloc

# Check object size
x = [1, 2, 3]
print(sys.getsizeof(x))  # Bytes

# Track memory allocations
tracemalloc.start()

# ... your code ...
data = [x**2 for x in range(100000)]

current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024 / 1024:.2f} MB")
print(f"Peak: {peak / 1024 / 1024:.2f} MB")

tracemalloc.stop()
```

---

## Summary

### Performance Tips

| Technique | Benefit |
|-----------|---------|
| List comprehensions | Faster than loops |
| Local variable caching | Faster lookups |
| Built-in functions | C-optimized |
| `''.join()` | O(n) vs O(n²) |
| `collections` module | Optimized data structures |

### Memory Tips

| Technique | Benefit |
|-----------|---------|
| Generators | Lazy evaluation |
| `__slots__` | Smaller instances |
| `array.array` | Compact numeric storage |
| Iterators | Avoid copies |
| `del` + `gc.collect()` | Free memory early |

### Key Principles

1. **Measure before optimizing** - Use `timeit` and `cProfile`
2. **Prefer built-ins** - They're implemented in C
3. **Use appropriate data structures** - `deque`, `Counter`, etc.
4. **Think about memory** - Generators for large data
5. **Cache expensive operations** - Local variables, `lru_cache`

---


## Runnable Example: `time_complexity.py`

```python
"""
PYTHON CODE PROFILING & OPTIMIZATION - BEGINNER LEVEL
======================================================
Module 1: Time Complexity Basics - Understanding Big O Notation

LEARNING OBJECTIVES:
- Understand what time complexity means
- Learn Big O notation and common complexity classes
- Recognize different complexity patterns in code
- Analyze simple algorithms for their time complexity

THEORY:
-------
Time Complexity measures how the runtime of an algorithm grows relative to 
the input size (n). It's expressed using Big O notation, which describes 
the upper bound of growth rate, ignoring constants and lower-order terms.

Common Complexity Classes (from best to worst):
1. O(1)       - Constant time
2. O(log n)   - Logarithmic time
3. O(n)       - Linear time
4. O(n log n) - Linearithmic time
5. O(n²)      - Quadratic time
6. O(n³)      - Cubic time
7. O(2ⁿ)      - Exponential time
8. O(n!)      - Factorial time

Author: Python Course Development Team
Date: 2024
"""

import time
import random


# ============================================================================
# SECTION 1: O(1) - CONSTANT TIME COMPLEXITY
# ============================================================================
# Operations that take the same amount of time regardless of input size

def constant_time_access(my_list, index):
    """
    Access an element by index - O(1) operation
    
    Explanation:
    - Array/list access by index is direct memory lookup
    - Doesn't matter if list has 10 or 10 million items
    - Time taken is constant
    
    Args:
        my_list: A list of elements
        index: Index to access
        
    Returns:
        Element at the specified index
        
    Time Complexity: O(1)
    """
    # Direct index access - constant time
    return my_list[index]


def constant_time_operations():
    """
    Demonstrate various O(1) operations
    
    Common O(1) operations in Python:
    - Accessing list/array element by index
    - Accessing dictionary value by key
    - Append to list
    - Push/pop from stack (list)
    - Basic arithmetic operations
    """
    # Create sample data structures
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    my_dict = {'a': 1, 'b': 2, 'c': 3}
    
    print("=" * 70)
    print("O(1) - CONSTANT TIME OPERATIONS")
    print("=" * 70)
    
    # Operation 1: List access by index - O(1)
    start = time.time()
    element = numbers[5]
    end = time.time()
    print(f"List index access: {element}, Time: {end - start:.10f}s")
    
    # Operation 2: Dictionary access by key - O(1) average case
    start = time.time()
    value = my_dict['b']
    end = time.time()
    print(f"Dict key access: {value}, Time: {end - start:.10f}s")
    
    # Operation 3: List append - O(1) amortized
    start = time.time()
    numbers.append(11)
    end = time.time()
    print(f"List append, Time: {end - start:.10f}s")
    
    # Operation 4: Arithmetic - O(1)
    start = time.time()
    result = 1234567 * 9876543
    end = time.time()
    print(f"Arithmetic: {result}, Time: {end - start:.10f}s")
    
    print("\nKey Point: All these operations take roughly the same time")
    print("regardless of data structure size.\n")


# ============================================================================
# SECTION 2: O(log n) - LOGARITHMIC TIME COMPLEXITY
# ============================================================================
# Operations that cut the problem size in half each iteration

def binary_search(sorted_list, target):
    """
    Binary search on a sorted list - O(log n) operation
    
    Explanation:
    - Each comparison eliminates half of the remaining elements
    - For 1000 elements, needs at most 10 comparisons (2^10 = 1024)
    - For 1,000,000 elements, needs at most 20 comparisons
    - Doubling input size only adds one more comparison
    
    Args:
        sorted_list: A sorted list of comparable elements
        target: Element to search for
        
    Returns:
        Index of target if found, -1 otherwise
        
    Time Complexity: O(log n)
    """
    left = 0  # Left boundary of search space
    right = len(sorted_list) - 1  # Right boundary
    comparisons = 0  # Track number of comparisons
    
    # Continue while search space is valid
    while left <= right:
        comparisons += 1
        # Find middle point (avoid overflow with this formula)
        mid = left + (right - left) // 2
        
        # Check if target is at mid
        if sorted_list[mid] == target:
            print(f"  Found {target} after {comparisons} comparisons")
            return mid
        
        # If target is greater, ignore left half
        elif sorted_list[mid] < target:
            left = mid + 1
        
        # If target is smaller, ignore right half
        else:
            right = mid - 1
    
    # Target not found
    print(f"  Target {target} not found after {comparisons} comparisons")
    return -1


def demonstrate_logarithmic():
    """
    Demonstrate O(log n) complexity with binary search
    
    Shows how logarithmic algorithms scale beautifully:
    - Small increase in comparisons for massive increase in data size
    """
    print("=" * 70)
    print("O(log n) - LOGARITHMIC TIME COMPLEXITY")
    print("=" * 70)
    
    # Test with different sizes
    sizes = [100, 1000, 10000, 100000]
    
    for size in sizes:
        # Create sorted list
        sorted_data = list(range(size))
        target = random.randint(0, size - 1)
        
        print(f"\nSearching in list of size {size:,}:")
        start = time.time()
        result = binary_search(sorted_data, target)
        end = time.time()
        print(f"  Time taken: {end - start:.10f}s")
    
    print("\nKey Point: Time grows logarithmically with input size.")
    print("10x larger input ≈ 3-4 more operations (log₂(10) ≈ 3.32)\n")


# ============================================================================
# SECTION 3: O(n) - LINEAR TIME COMPLEXITY
# ============================================================================
# Operations that must examine each element once

def linear_search(my_list, target):
    """
    Linear search - O(n) operation
    
    Explanation:
    - Must potentially check every element
    - In worst case, target is at end or not present
    - Time grows proportionally with input size
    
    Args:
        my_list: List to search
        target: Element to find
        
    Returns:
        Index of target if found, -1 otherwise
        
    Time Complexity: O(n)
    """
    # Iterate through each element
    for i in range(len(my_list)):
        # Check if current element matches target
        if my_list[i] == target:
            return i
    
    # Target not found after checking all elements
    return -1


def find_maximum(numbers):
    """
    Find maximum value in list - O(n) operation
    
    Explanation:
    - Must examine every element to ensure we found the maximum
    - Cannot skip any elements
    - Doubling input size doubles the time
    
    Args:
        numbers: List of numbers
        
    Returns:
        Maximum value in the list
        
    Time Complexity: O(n)
    """
    # Initialize max with first element
    max_val = numbers[0]
    
    # Compare each element with current max
    for num in numbers[1:]:
        if num > max_val:
            max_val = num
    
    return max_val


def demonstrate_linear():
    """
    Demonstrate O(n) complexity with various algorithms
    """
    print("=" * 70)
    print("O(n) - LINEAR TIME COMPLEXITY")
    print("=" * 70)
    
    # Test with different sizes
    sizes = [1000, 10000, 100000, 1000000]
    
    for size in sizes:
        # Create test data
        data = list(range(size))
        
        print(f"\nProcessing list of size {size:,}:")
        
        # Linear search (worst case - element not present)
        start = time.time()
        result = linear_search(data, -1)  # Search for non-existent element
        end = time.time()
        print(f"  Linear search time: {end - start:.10f}s")
        
        # Find maximum
        start = time.time()
        max_val = find_maximum(data)
        end = time.time()
        print(f"  Find maximum time: {end - start:.10f}s")
    
    print("\nKey Point: Time grows linearly with input size.")
    print("10x larger input ≈ 10x more time\n")


# ============================================================================
# SECTION 4: O(n²) - QUADRATIC TIME COMPLEXITY
# ============================================================================
# Nested loops that examine all pairs of elements

def bubble_sort(arr):
    """
    Bubble sort algorithm - O(n²) operation
    
    Explanation:
    - Two nested loops, each running n times
    - Outer loop: n iterations
    - Inner loop: n iterations for each outer iteration
    - Total operations: n × n = n²
    
    Args:
        arr: List to sort
        
    Returns:
        Sorted list
        
    Time Complexity: O(n²)
    """
    # Create a copy to avoid modifying original
    arr = arr.copy()
    n = len(arr)
    
    # Outer loop: n passes through the array
    for i in range(n):
        # Inner loop: compare adjacent elements
        # After each pass, largest element "bubbles" to the end
        for j in range(0, n - i - 1):
            # Swap if elements are in wrong order
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    
    return arr


def find_duplicates_naive(numbers):
    """
    Find all duplicate pairs - O(n²) operation
    
    Explanation:
    - Compare each element with every other element
    - For n elements, we make n × (n-1) / 2 comparisons
    - This is still O(n²) as we ignore constants
    
    Args:
        numbers: List of numbers
        
    Returns:
        List of duplicate pairs
        
    Time Complexity: O(n²)
    """
    duplicates = []
    n = len(numbers)
    
    # Outer loop: select first element of pair
    for i in range(n):
        # Inner loop: compare with remaining elements
        for j in range(i + 1, n):
            # Check if elements are equal
            if numbers[i] == numbers[j]:
                duplicates.append((numbers[i], i, j))
    
    return duplicates


def demonstrate_quadratic():
    """
    Demonstrate O(n²) complexity
    
    Warning: Quadratic algorithms become very slow for large inputs!
    """
    print("=" * 70)
    print("O(n²) - QUADRATIC TIME COMPLEXITY")
    print("=" * 70)
    
    # Test with smaller sizes (quadratic is slow!)
    sizes = [100, 500, 1000, 2000]
    
    for size in sizes:
        # Create test data
        data = [random.randint(0, size) for _ in range(size)]
        
        print(f"\nProcessing list of size {size:,}:")
        
        # Bubble sort
        start = time.time()
        sorted_data = bubble_sort(data)
        end = time.time()
        print(f"  Bubble sort time: {end - start:.6f}s")
    
    print("\nKey Point: Time grows quadratically with input size.")
    print("10x larger input ≈ 100x more time (10² = 100)")
    print("WARNING: Avoid O(n²) algorithms for large datasets!\n")


# ============================================================================
# SECTION 5: O(n log n) - LINEARITHMIC TIME COMPLEXITY
# ============================================================================
# Efficient sorting algorithms like merge sort, quick sort

def merge_sort(arr):
    """
    Merge sort algorithm - O(n log n) operation
    
    Explanation:
    - Divide and conquer algorithm
    - Divides array into halves recursively: O(log n) divisions
    - Merges sorted halves: O(n) operations per level
    - Total: O(n) × O(log n) = O(n log n)
    
    Args:
        arr: List to sort
        
    Returns:
        Sorted list
        
    Time Complexity: O(n log n)
    """
    # Base case: arrays of length 0 or 1 are already sorted
    if len(arr) <= 1:
        return arr
    
    # Divide: split array into two halves
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    # Conquer: recursively sort both halves
    left_sorted = merge_sort(left_half)
    right_sorted = merge_sort(right_half)
    
    # Combine: merge the sorted halves
    return merge(left_sorted, right_sorted)


def merge(left, right):
    """
    Merge two sorted arrays - O(n) operation
    
    Helper function for merge sort
    
    Args:
        left: First sorted array
        right: Second sorted array
        
    Returns:
        Merged sorted array
    """
    result = []
    i = j = 0
    
    # Merge elements from both arrays in sorted order
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Append remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


def demonstrate_linearithmic():
    """
    Demonstrate O(n log n) complexity
    
    Shows that O(n log n) is much better than O(n²) for large inputs
    """
    print("=" * 70)
    print("O(n log n) - LINEARITHMIC TIME COMPLEXITY")
    print("=" * 70)
    
    # Test with various sizes
    sizes = [100, 1000, 10000, 100000]
    
    for size in sizes:
        # Create test data
        data = [random.randint(0, size) for _ in range(size)]
        
        print(f"\nSorting list of size {size:,}:")
        
        # Merge sort - O(n log n)
        start = time.time()
        sorted_data = merge_sort(data)
        end = time.time()
        print(f"  Merge sort time: {end - start:.6f}s")
        
        # Compare with Python's built-in sort (also O(n log n) - Timsort)
        data_copy = data.copy()
        start = time.time()
        data_copy.sort()
        end = time.time()
        print(f"  Python sort time: {end - start:.6f}s")
    
    print("\nKey Point: O(n log n) is optimal for comparison-based sorting.")
    print("Much faster than O(n²) for large inputs!")
    print("10x larger input ≈ 33x more time (10 × log₂(10) ≈ 33.2)\n")


# ============================================================================
# SECTION 6: COMPARING COMPLEXITY CLASSES
# ============================================================================

def compare_all_complexities():
    """
    Compare different complexity classes side by side
    
    Demonstrates how different algorithms scale with input size
    """
    print("=" * 70)
    print("COMPLEXITY CLASS COMPARISON")
    print("=" * 70)
    print("\nHow many operations for different input sizes?\n")
    print(f"{'n':<12} {'O(1)':<12} {'O(log n)':<12} {'O(n)':<12} {'O(n log n)':<15} {'O(n²)':<12}")
    print("-" * 85)
    
    import math
    
    # Different input sizes
    sizes = [10, 100, 1000, 10000, 100000]
    
    for n in sizes:
        o_1 = 1
        o_log_n = math.log2(n)
        o_n = n
        o_n_log_n = n * math.log2(n)
        o_n2 = n * n
        
        print(f"{n:<12} {o_1:<12} {o_log_n:<12.2f} {o_n:<12} {o_n_log_n:<15.0f} {o_n2:<12}")
    
    print("\nKey Insights:")
    print("1. O(1) is always best - constant time regardless of input")
    print("2. O(log n) scales beautifully - very slow growth")
    print("3. O(n) grows linearly - acceptable for most applications")
    print("4. O(n log n) is optimal for sorting - reasonable growth")
    print("5. O(n²) grows very fast - avoid for large inputs!")
    print()


# ============================================================================
# SECTION 7: SPACE COMPLEXITY
# ============================================================================
# Space complexity measures memory usage relative to input size

def space_o1_example(n):
    """
    Algorithm with O(1) space complexity
    
    Uses constant extra space regardless of input size
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    # Only uses a fixed number of variables
    total = 0  # One integer variable
    count = 0  # Another integer variable
    
    # Process n items but don't store them
    for i in range(n):
        total += i
        count += 1
    
    return total / count if count > 0 else 0


def space_on_example(n):
    """
    Algorithm with O(n) space complexity
    
    Creates data structure proportional to input size
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    # Creates a list of size n
    result = []
    
    # Store all values
    for i in range(n):
        result.append(i * 2)
    
    return result


def demonstrate_space_complexity():
    """
    Demonstrate space complexity concepts
    """
    print("=" * 70)
    print("SPACE COMPLEXITY")
    print("=" * 70)
    
    import sys
    
    n = 1000
    
    print(f"\nFor n = {n}:")
    
    # O(1) space
    result1 = space_o1_example(n)
    print(f"O(1) space: stores only a few variables")
    print(f"  Result: {result1}")
    
    # O(n) space
    result2 = space_on_example(n)
    print(f"\nO(n) space: stores {len(result2)} elements")
    print(f"  Memory used: ~{sys.getsizeof(result2)} bytes")
    
    print("\nKey Point: Space complexity is equally important!")
    print("Memory-efficient algorithms are crucial for large datasets.\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main function to run all demonstrations
    
    Runs through all complexity classes with examples and timing
    """
    print("\n" + "=" * 70)
    print("TIME COMPLEXITY BASICS - COMPREHENSIVE TUTORIAL")
    print("=" * 70 + "\n")
    
    # Run all demonstrations
    constant_time_operations()
    demonstrate_logarithmic()
    demonstrate_linear()
    demonstrate_quadratic()
    demonstrate_linearithmic()
    compare_all_complexities()
    demonstrate_space_complexity()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    Best to Worst Complexity Classes:
    1. O(1)       - Constant      - Excellent
    2. O(log n)   - Logarithmic   - Excellent
    3. O(n)       - Linear        - Good
    4. O(n log n) - Linearithmic  - Acceptable
    5. O(n²)      - Quadratic     - Poor for large n
    6. O(2ⁿ)      - Exponential   - Impractical for large n
    
    Remember:
    - Always analyze both time AND space complexity
    - Constants matter in practice (Big O ignores them)
    - Choose the right algorithm for your data size
    - Profile real code to verify theoretical analysis
    """)


if __name__ == "__main__":
    main()
```


## Exercises

**Exercise 1.**
Write a benchmark comparing four ways to sum a list of 1,000,000 integers: (a) a `for` loop with `+=`, (b) the built-in `sum()`, (c) `functools.reduce` with `operator.add`, and (d) a generator expression inside `sum()`. Use `timeit` to measure each and print a ranked table from fastest to slowest.

??? success "Solution to Exercise 1"
        ```python
        import timeit
        import functools
        import operator

        data = list(range(1_000_000))

        def sum_loop():
            total = 0
            for x in data:
                total += x
            return total

        def sum_builtin():
            return sum(data)

        def sum_reduce():
            return functools.reduce(operator.add, data)

        def sum_genexpr():
            return sum(x for x in data)

        methods = [
            ("for loop", sum_loop),
            ("sum()", sum_builtin),
            ("reduce", sum_reduce),
            ("sum(gen)", sum_genexpr),
        ]

        results = []
        for name, func in methods:
            t = min(timeit.repeat(func, repeat=3, number=10))
            results.append((name, t))

        results.sort(key=lambda x: x[1])
        print(f"{'Method':<12} {'Time (s)':>10}")
        print("-" * 24)
        for name, t in results:
            print(f"{name:<12} {t:>10.4f}")
        ```

---

**Exercise 2.**
Create a class `Point` with and without `__slots__`, each having `x` and `y` attributes. Create 500,000 instances of each, measure total memory using `tracemalloc`, and print the memory used and savings percentage from using `__slots__`.

??? success "Solution to Exercise 2"
        ```python
        import tracemalloc

        class PointRegular:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        class PointSlots:
            __slots__ = ('x', 'y')
            def __init__(self, x, y):
                self.x = x
                self.y = y

        n = 500_000

        tracemalloc.start()
        regular = [PointRegular(i, i) for i in range(n)]
        _, peak_regular = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tracemalloc.start()
        slotted = [PointSlots(i, i) for i in range(n)]
        _, peak_slotted = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        savings = (1 - peak_slotted / peak_regular) * 100
        print(f"Regular: {peak_regular / 1024 / 1024:.1f} MB")
        print(f"Slotted: {peak_slotted / 1024 / 1024:.1f} MB")
        print(f"Savings: {savings:.1f}%")
        ```

---

**Exercise 3.**
Write a generator-based version and a list-based version of a function that yields/returns the first n Fibonacci numbers. For n = 1,000,000, use `tracemalloc` to compare peak memory of iterating through all values (consuming but not storing them) for both versions.

??? success "Solution to Exercise 3"
        ```python
        import tracemalloc

        def fib_generator(n):
            a, b = 0, 1
            for _ in range(n):
                yield a
                a, b = b, a + b

        def fib_list(n):
            result = []
            a, b = 0, 1
            for _ in range(n):
                result.append(a)
                a, b = b, a + b
            return result

        n = 1_000_000

        # Generator version
        tracemalloc.start()
        total = 0
        for x in fib_generator(n):
            total += x
        _, peak_gen = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # List version
        tracemalloc.start()
        total = 0
        for x in fib_list(n):
            total += x
        _, peak_list = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"Generator peak: {peak_gen / 1024 / 1024:.1f} MB")
        print(f"List peak:      {peak_list / 1024 / 1024:.1f} MB")
        ```

---
