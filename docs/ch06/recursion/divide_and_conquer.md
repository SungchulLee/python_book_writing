# Divide and Conquer

Divide and Conquer is a recursive algorithm pattern that solves problems by breaking them into smaller subproblems, solving each independently, then combining results.

!!! tip "Mental Model"
    Divide and conquer splits a big problem into independent smaller copies of itself, solves each recursively, and merges the answers. The key insight is that the subproblems don't overlap -- each piece is solved exactly once. This independence is what separates divide-and-conquer from dynamic programming.

---

## The Divide and Conquer Pattern

1. **Divide**: Break problem into smaller subproblems
2. **Conquer**: Solve subproblems recursively (or directly if small)
3. **Combine**: Merge solutions to subproblems

## Merge Sort Example

```python
def merge_sort(arr):
    '''Sort array using divide and conquer'''
    if len(arr) <= 1:
        return arr
    
    # Divide
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    # Conquer
    left_sorted = merge_sort(left)
    right_sorted = merge_sort(right)
    
    # Combine
    return merge(left_sorted, right_sorted)

def merge(left, right):
    '''Merge two sorted arrays'''
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

arr = [38, 27, 43, 3, 9, 82, 10]
print(merge_sort(arr))  # [3, 9, 10, 27, 38, 43, 82]
```

## Binary Search (Divide and Conquer)

```python
def binary_search(arr, target, low=0, high=None):
    '''Search for target in sorted array'''
    if high is None:
        high = len(arr) - 1
    
    if low > high:
        return -1  # Not found
    
    mid = (low + high) // 2
    
    if arr[mid] == target:
        return mid  # Found
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, high)  # Search right half
    else:
        return binary_search(arr, target, low, mid - 1)   # Search left half

arr = [1, 3, 5, 7, 9, 11, 13, 15]
print(binary_search(arr, 7))   # 3
print(binary_search(arr, 6))   # -1
```

## Quick Sort Example

```python
def quick_sort(arr):
    '''Sort array using divide and conquer with pivot'''
    if len(arr) <= 1:
        return arr
    
    # Divide using pivot
    pivot = arr[0]
    left = [x for x in arr[1:] if x < pivot]
    right = [x for x in arr[1:] if x >= pivot]
    
    # Conquer (recursive)
    left_sorted = quick_sort(left)
    right_sorted = quick_sort(right)
    
    # Combine
    return left_sorted + [pivot] + right_sorted

arr = [38, 27, 43, 3, 9, 82, 10]
print(quick_sort(arr))  # [3, 9, 10, 27, 38, 43, 82]
```

## Time Complexity Analysis

- **Merge Sort**: O(n log n) - always
- **Quick Sort**: O(n log n) average, O(n²) worst case
- **Binary Search**: O(log n)

Divide and Conquer is powerful for problems naturally decomposable into similar subproblems.

---

## Runnable Example: `sorting_algorithms_example.py`

```python
"""
Sorting Algorithms: From Simple to Divide-and-Conquer

This tutorial implements four classic sorting algorithms, demonstrating
recursion, divide-and-conquer, and custom comparators.

Algorithms covered:
- Selection Sort: O(n^2) - find minimum, swap to front
- Bubble Sort: O(n^2) - adjacent swaps, optimized with early stop
- Merge Sort: O(n log n) - divide, sort halves, merge (recursive)
- Quick Sort: O(n log n) average - partition around pivot (recursive)

Based on concepts from Python-100-Days example02 and ch05/recursion materials.
"""


# =============================================================================
# Example 1: Selection Sort - O(n^2)
# =============================================================================

def selection_sort(items, *, key=lambda x: x):
    """Sort by repeatedly finding the minimum from the unsorted portion.

    - In each pass, find the smallest element and swap it to its correct position.
    - Not stable (equal elements may change relative order).
    - Always O(n^2) regardless of input.

    >>> selection_sort([35, 97, 12, 68, 55])
    [12, 35, 55, 68, 97]
    """
    result = items[:]  # Don't modify original (no side effects)
    for i in range(len(result) - 1):
        min_idx = i
        for j in range(i + 1, len(result)):
            if key(result[j]) < key(result[min_idx]):
                min_idx = j
        result[i], result[min_idx] = result[min_idx], result[i]
    return result


# =============================================================================
# Example 2: Bubble Sort - O(n^2) with optimization
# =============================================================================

def bubble_sort(items, *, key=lambda x: x):
    """Sort by repeatedly swapping adjacent out-of-order elements.

    Optimization: cocktail shaker variant - alternates left-to-right and
    right-to-left passes, with early termination when no swaps occur.

    - Stable sort (preserves relative order of equal elements).
    - Best case O(n) when already sorted (due to early stop).

    >>> bubble_sort([35, 97, 12, 68, 55])
    [12, 35, 55, 68, 97]
    """
    result = items[:]
    n = len(result)
    for i in range(1, n):
        swapped = False
        # Forward pass: bubble largest to the right
        for j in range(n - i):
            if key(result[j]) > key(result[j + 1]):
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break  # Already sorted - early termination
        swapped = False
        # Backward pass: bubble smallest to the left
        for j in range(n - i - 1, i - 1, -1):
            if key(result[j - 1]) > key(result[j]):
                result[j], result[j - 1] = result[j - 1], result[j]
                swapped = True
        if not swapped:
            break
    return result


# =============================================================================
# Example 3: Merge Sort - O(n log n)
# =============================================================================

def merge_sort(items, *, key=lambda x: x):
    """Sort using divide-and-conquer: split, sort halves, merge.

    - Always O(n log n) - consistent performance.
    - Stable sort.
    - Requires O(n) extra space for merging.

    How it works:
    [35, 97, 12, 68, 55, 73, 81, 40]
     -> [35, 97, 12, 68]  [55, 73, 81, 40]     # split
     -> [35, 97] [12, 68] [55, 73] [81, 40]     # split again
     -> [35] [97] [12] [68] [55] [73] [81] [40] # base case
     -> [35, 97] [12, 68] [55, 73] [40, 81]     # merge pairs
     -> [12, 35, 68, 97] [40, 55, 73, 81]       # merge pairs
     -> [12, 35, 40, 55, 68, 73, 81, 97]        # final merge

    >>> merge_sort([35, 97, 12, 68, 55, 73, 81, 40])
    [12, 35, 40, 55, 68, 73, 81, 97]
    """
    if len(items) < 2:
        return items[:]

    mid = len(items) // 2
    left = merge_sort(items[:mid], key=key)
    right = merge_sort(items[mid:], key=key)
    return _merge(left, right, key=key)


def _merge(left, right, *, key=lambda x: x):
    """Merge two sorted lists into one sorted list."""
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# =============================================================================
# Example 4: Quick Sort - O(n log n) average
# =============================================================================

def quick_sort(items, *, key=lambda x: x):
    """Sort using partition: pick pivot, split into smaller/larger groups.

    - Average O(n log n), worst case O(n^2) (rare with good pivot).
    - In-place partitioning (but this version copies for safety).
    - Not stable.

    How it works:
    [35, 97, 12, 68, 55, 73, 81, 40]  pivot=40
     -> [35, 12] [40] [97, 68, 55, 73, 81]  # partition
     -> recursively sort each half

    >>> quick_sort([35, 97, 12, 68, 55, 73, 81, 40])
    [12, 35, 40, 55, 68, 73, 81, 97]
    """
    result = items[:]
    _quick_sort(result, 0, len(result) - 1, key=key)
    return result


def _quick_sort(items, start, end, *, key):
    """Recursively partition and sort subarrays."""
    if start < end:
        pivot_pos = _partition(items, start, end, key=key)
        _quick_sort(items, start, pivot_pos - 1, key=key)
        _quick_sort(items, pivot_pos + 1, end, key=key)


def _partition(items, start, end, *, key):
    """Lomuto partition scheme: use last element as pivot."""
    pivot = key(items[end])
    i = start - 1
    for j in range(start, end):
        if key(items[j]) <= pivot:
            i += 1
            items[i], items[j] = items[j], items[i]
    items[i + 1], items[end] = items[end], items[i + 1]
    return i + 1


# =============================================================================
# Example 5: Sorting Custom Objects
# =============================================================================

class Person:
    """Simple person class to demonstrate custom sorting."""

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f'{self.name}: {self.age}'


def demo_custom_sorting():
    """Sort custom objects using key functions."""
    people = [
        Person('Alice', 25),
        Person('Bob', 39),
        Person('Charlie', 50),
        Person('Diana', 20),
    ]

    print("=== Sorting Custom Objects ===")
    print(f"Original:    {people}")
    print(f"By age:      {quick_sort(people, key=lambda p: p.age)}")
    print(f"By name:     {merge_sort(people, key=lambda p: p.name)}")
    print()


# =============================================================================
# Example 6: Sorting Strings by Different Criteria
# =============================================================================

def demo_string_sorting():
    """Sort strings alphabetically and by length."""
    fruits = ['apple', 'orange', 'watermelon', 'durian', 'pear']

    print("=== Sorting Strings ===")
    print(f"Original:        {fruits}")
    print(f"Alphabetical:    {merge_sort(fruits)}")
    print(f"By length:       {bubble_sort(fruits, key=len)}")
    print()


# =============================================================================
# Example 7: Performance Comparison
# =============================================================================

def compare_performance():
    """Compare sorting algorithm performance on random data."""
    import random
    import time

    sizes = [100, 1000, 5000]
    algorithms = {
        'Selection': selection_sort,
        'Bubble':    bubble_sort,
        'Merge':     merge_sort,
        'Quick':     quick_sort,
    }

    print("=== Sorting Performance (seconds) ===")
    header = f"{'Size':>6}"
    for name in algorithms:
        header += f" | {name:>10}"
    print(header)
    print("-" * len(header))

    for size in sizes:
        data = [random.randint(0, 10000) for _ in range(size)]
        row = f"{size:>6}"
        for name, func in algorithms.items():
            start = time.perf_counter()
            func(data)
            elapsed = time.perf_counter() - start
            row += f" | {elapsed:>10.4f}"
        print(row)
    print()


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    # Basic sorting demo
    items = [35, 97, 12, 68, 55, 73, 81, 40]
    print("=== Basic Sorting ===")
    print(f"Original:       {items}")
    print(f"Selection sort: {selection_sort(items)}")
    print(f"Bubble sort:    {bubble_sort(items)}")
    print(f"Merge sort:     {merge_sort(items)}")
    print(f"Quick sort:     {quick_sort(items)}")
    print()

    demo_custom_sorting()
    demo_string_sorting()
    compare_performance()
```

---

## Exercises

**Exercise 1.**
Implement `merge_sort(arr)` from scratch using the divide-and-conquer pattern. Split the array in half, recursively sort each half, then merge them. Verify by sorting `[38, 27, 43, 3, 9, 82, 10]`.

??? success "Solution to Exercise 1"

        def merge_sort(arr):
            if len(arr) <= 1:
                return arr

            mid = len(arr) // 2
            left = merge_sort(arr[:mid])
            right = merge_sort(arr[mid:])

            # Merge
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
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

---

**Exercise 2.**
Write a recursive `binary_search(arr, target)` function that returns the index of `target` in a sorted array, or `-1` if not found. Use the divide-and-conquer approach by comparing with the middle element and recursing into the appropriate half.

??? success "Solution to Exercise 2"

        def binary_search(arr, target, low=0, high=None):
            if high is None:
                high = len(arr) - 1
            if low > high:
                return -1

            mid = (low + high) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                return binary_search(arr, target, mid + 1, high)
            else:
                return binary_search(arr, target, low, mid - 1)

        data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
        print(binary_search(data, 23))   # 5
        print(binary_search(data, 100))  # -1

---

**Exercise 3.**
Implement a `max_subarray_sum(arr)` function using divide and conquer. Split the array in half, recursively find the max subarray sum in the left half, right half, and the crossing subarray. Return the maximum of the three. Verify with `[-2, 1, -3, 4, -1, 2, 1, -5, 4]` (expected answer: `6`).

??? success "Solution to Exercise 3"

        def max_subarray_sum(arr):
            if len(arr) == 1:
                return arr[0]

            mid = len(arr) // 2
            left_max = max_subarray_sum(arr[:mid])
            right_max = max_subarray_sum(arr[mid:])

            # Max crossing subarray
            left_sum = float("-inf")
            total = 0
            for i in range(mid - 1, -1, -1):
                total += arr[i]
                left_sum = max(left_sum, total)

            right_sum = float("-inf")
            total = 0
            for i in range(mid, len(arr)):
                total += arr[i]
                right_sum = max(right_sum, total)

            cross_max = left_sum + right_sum
            return max(left_max, right_max, cross_max)

        print(max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # 6
