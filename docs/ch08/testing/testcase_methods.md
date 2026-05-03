# unittest.TestCase Methods

Common assertion methods provided by TestCase.

!!! tip "Mental Model"
    `TestCase` assertion methods are specialized comparisons that produce clear failure messages. `assertEqual(a, b)` is not just `assert a == b` — it tells you *what* `a` and `b` actually were when they differed. Choosing the most specific assertion (e.g., `assertIn`, `assertRaises`, `assertAlmostEqual`) gives you the most informative error output when a test fails.

## Equality and Comparison Assertions

Assert equality and inequality.

```python
import unittest

class TestAssertions(unittest.TestCase):
    def test_equal(self):
        self.assertEqual(5, 5)
    
    def test_not_equal(self):
        self.assertNotEqual(5, 3)
    
    def test_greater(self):
        self.assertGreater(10, 5)
    
    def test_less(self):
        self.assertLess(3, 5)
    
    def test_almost_equal(self):
        self.assertAlmostEqual(0.1 + 0.2, 0.3, places=2)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False, verbosity=2)
```

```
test_almost_equal ... ok
test_equal ... ok
test_greater ... ok
test_less ... ok
test_not_equal ... ok
```

## Container and Type Assertions

Assert membership, containment, and types.

```python
import unittest

class TestContainers(unittest.TestCase):
    def test_in(self):
        self.assertIn(2, [1, 2, 3])
    
    def test_not_in(self):
        self.assertNotIn(4, [1, 2, 3])
    
    def test_is_instance(self):
        self.assertIsInstance("hello", str)
    
    def test_is_none(self):
        self.assertIsNone(None)
    
    def test_is_not_none(self):
        self.assertIsNotNone(42)
    
    def test_true(self):
        self.assertTrue(5 > 3)
    
    def test_false(self):
        self.assertFalse(5 < 3)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False, verbosity=2)
```

```
test_false ... ok
test_in ... ok
test_is_instance ... ok
test_is_none ... ok
test_is_not_none ... ok
test_true ... ok
```

---

## Runnable Example: `search_sort_test_example.py`

```python
"""
Unit Testing: Testing Search and Sort Algorithms

Practical unittest example that tests real algorithms (search and sort)
with setUp/tearDown, multiple assertion methods, and edge cases.

Topics covered:
- unittest.TestCase subclassing
- setUp() for test data preparation
- Test method naming (test_ prefix)
- Assertion methods (assertEqual, assertLessEqual, assertRaises)
- Running tests: python -m unittest or pytest

Based on concepts from Python-100-Days test files and ch07/testing materials.
"""

import unittest


# =============================================================================
# Functions Under Test
# =============================================================================

def sequential_search(items: list, target) -> int:
    """Linear search - returns index or -1."""
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1


def binary_search(items: list, target) -> int:
    """Binary search on sorted list - returns index or -1."""
    start, end = 0, len(items) - 1
    while start <= end:
        mid = (start + end) // 2
        if target > items[mid]:
            start = mid + 1
        elif target < items[mid]:
            end = mid - 1
        else:
            return mid
    return -1


def selection_sort(items: list) -> list:
    """Selection sort - returns new sorted list."""
    result = items[:]
    for i in range(len(result) - 1):
        min_idx = i
        for j in range(i + 1, len(result)):
            if result[j] < result[min_idx]:
                min_idx = j
        result[i], result[min_idx] = result[min_idx], result[i]
    return result


def merge(left: list, right: list) -> list:
    """Merge two sorted lists into one sorted list."""
    result = []
    i, j = 0, 0
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


# =============================================================================
# Test Case 1: Search Algorithm Tests
# =============================================================================

class TestSearchAlgorithms(unittest.TestCase):
    """Tests for sequential and binary search."""

    def setUp(self):
        """Prepare test data - runs before EACH test method."""
        self.unsorted = [35, 97, 12, 68, 55, 73, 81, 40]
        self.sorted = [12, 35, 40, 55, 68, 73, 81, 97]

    def test_sequential_search_found(self):
        """Test sequential search finds existing elements."""
        self.assertEqual(0, sequential_search(self.unsorted, 35))
        self.assertEqual(2, sequential_search(self.unsorted, 12))
        self.assertEqual(6, sequential_search(self.unsorted, 81))
        self.assertEqual(7, sequential_search(self.unsorted, 40))

    def test_sequential_search_not_found(self):
        """Test sequential search returns -1 for missing elements."""
        self.assertEqual(-1, sequential_search(self.unsorted, 99))
        self.assertEqual(-1, sequential_search(self.unsorted, 7))

    def test_sequential_search_empty_list(self):
        """Test sequential search on empty list."""
        self.assertEqual(-1, sequential_search([], 42))

    def test_binary_search_found(self):
        """Test binary search finds elements in sorted list."""
        self.assertEqual(1, binary_search(self.sorted, 35))
        self.assertEqual(0, binary_search(self.sorted, 12))
        self.assertEqual(6, binary_search(self.sorted, 81))
        self.assertEqual(2, binary_search(self.sorted, 40))
        self.assertEqual(7, binary_search(self.sorted, 97))

    def test_binary_search_not_found(self):
        """Test binary search returns -1 for missing elements."""
        self.assertEqual(-1, binary_search(self.sorted, 7))
        self.assertEqual(-1, binary_search(self.sorted, 99))

    def test_binary_search_single_element(self):
        """Test binary search with single-element list."""
        self.assertEqual(0, binary_search([42], 42))
        self.assertEqual(-1, binary_search([42], 99))


# =============================================================================
# Test Case 2: Sort Algorithm Tests
# =============================================================================

class TestSortAlgorithms(unittest.TestCase):
    """Tests for sorting algorithms."""

    def setUp(self):
        self.data = [35, 97, 12, 68, 55, 73, 81, 40]
        self.expected = [12, 35, 40, 55, 68, 73, 81, 97]

    def test_selection_sort_correctness(self):
        """Test that selection sort produces correct order."""
        result = selection_sort(self.data)
        self.assertEqual(result, self.expected)

    def test_selection_sort_no_side_effects(self):
        """Test that original list is not modified."""
        original = self.data[:]
        selection_sort(self.data)
        self.assertEqual(self.data, original)

    def test_selection_sort_already_sorted(self):
        """Test sorting an already sorted list."""
        result = selection_sort(self.expected)
        self.assertEqual(result, self.expected)

    def test_selection_sort_reverse_sorted(self):
        """Test sorting a reverse-sorted list."""
        result = selection_sort([5, 4, 3, 2, 1])
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_selection_sort_duplicates(self):
        """Test sorting with duplicate values."""
        result = selection_sort([3, 1, 4, 1, 5, 9, 2, 6, 5])
        for i in range(len(result) - 1):
            self.assertLessEqual(result[i], result[i + 1])

    def test_selection_sort_empty(self):
        """Test sorting empty list."""
        self.assertEqual(selection_sort([]), [])

    def test_selection_sort_single_element(self):
        """Test sorting single-element list."""
        self.assertEqual(selection_sort([42]), [42])


# =============================================================================
# Test Case 3: Merge Function Tests
# =============================================================================

class TestMerge(unittest.TestCase):
    """Tests for the merge helper function."""

    def test_merge_basic(self):
        """Test merging two sorted lists."""
        left = [12, 35, 68, 97]
        right = [40, 55, 73, 81]
        result = merge(left, right)
        for i in range(len(result) - 1):
            self.assertLessEqual(result[i], result[i + 1])

    def test_merge_preserves_length(self):
        """Test that merge output has correct length."""
        left = [1, 3, 5]
        right = [2, 4, 6]
        result = merge(left, right)
        self.assertEqual(len(result), len(left) + len(right))

    def test_merge_empty_left(self):
        """Test merging with empty left list."""
        self.assertEqual(merge([], [1, 2, 3]), [1, 2, 3])

    def test_merge_empty_right(self):
        """Test merging with empty right list."""
        self.assertEqual(merge([1, 2, 3], []), [1, 2, 3])

    def test_merge_both_empty(self):
        """Test merging two empty lists."""
        self.assertEqual(merge([], []), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
```

---

## Exercises

**Exercise 1.** Write a `TestCase` that tests a `clamp(value, lo, hi)` function using `assertEqual`, `assertGreaterEqual`, and `assertLessEqual`. The function should return `lo` if `value < lo`, `hi` if `value > hi`, and `value` otherwise.

??? success "Solution to Exercise 1"
    ```python
    import unittest

    def clamp(value, lo, hi):
        if value < lo:
            return lo
        if value > hi:
            return hi
        return value

    class TestClamp(unittest.TestCase):
        def test_within_range(self):
            self.assertEqual(clamp(5, 0, 10), 5)

        def test_below_range(self):
            result = clamp(-5, 0, 10)
            self.assertEqual(result, 0)
            self.assertGreaterEqual(result, 0)

        def test_above_range(self):
            result = clamp(15, 0, 10)
            self.assertEqual(result, 10)
            self.assertLessEqual(result, 10)

    if __name__ == "__main__":
        unittest.main()
    ```

---

**Exercise 2.** Use `assertAlmostEqual` to test that `math.sin(math.pi)` is approximately zero. Why would `assertEqual` fail here?

??? success "Solution to Exercise 2"
    ```python
    import unittest
    import math

    class TestSin(unittest.TestCase):
        def test_sin_pi(self):
            self.assertAlmostEqual(math.sin(math.pi), 0, places=10)

    if __name__ == "__main__":
        unittest.main()
    ```

    `assertEqual` would fail because `math.sin(math.pi)` returns a tiny floating-point number like `1.2246e-16` due to floating-point precision, not exactly `0`. `assertAlmostEqual` checks within a tolerance.

---

**Exercise 3.** Write tests for a `Stack` class using `assertRaises` for popping from an empty stack, `assertIn` for checking membership after push, and `assertIsNone` for checking the return value of push.

??? success "Solution to Exercise 3"
    ```python
    import unittest

    class Stack:
        def __init__(self):
            self._items = []
        def push(self, item):
            self._items.append(item)
        def pop(self):
            if not self._items:
                raise IndexError("Pop from empty stack")
            return self._items.pop()
        def __contains__(self, item):
            return item in self._items

    class TestStack(unittest.TestCase):
        def test_pop_empty(self):
            s = Stack()
            with self.assertRaises(IndexError):
                s.pop()

        def test_push_contains(self):
            s = Stack()
            s.push(42)
            self.assertIn(42, s)

        def test_push_returns_none(self):
            s = Stack()
            result = s.push(1)
            self.assertIsNone(result)

    if __name__ == "__main__":
        unittest.main()
    ```

---

**Exercise 4.** Use `assertCountEqual` to verify that a function `unique_chars(s)` returns the correct set of characters regardless of order.

??? success "Solution to Exercise 4"
    ```python
    import unittest

    def unique_chars(s):
        return list(set(s))

    class TestUniqueChars(unittest.TestCase):
        def test_unique(self):
            result = unique_chars("banana")
            self.assertCountEqual(result, ["b", "a", "n"])

        def test_empty(self):
            self.assertCountEqual(unique_chars(""), [])

    if __name__ == "__main__":
        unittest.main()
    ```
