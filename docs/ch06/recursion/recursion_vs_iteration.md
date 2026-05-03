# Recursion vs Iteration

Both recursion and iteration solve repetitive problems, but they differ in clarity, efficiency, and use cases. Understanding trade-offs helps you choose correctly.

!!! tip "Mental Model"
    Recursion uses the call stack as implicit state; iteration uses explicit variables. Recursion is often clearer for problems with natural self-similar structure (trees, nested data), while iteration is more memory-efficient and avoids Python's recursion limit. When in doubt, write it recursively for clarity, then convert to iteration if performance demands it.

---

## Sum Calculation: Both Approaches

```python
# Recursive: Natural for mathematical definitions
def sum_recursive(numbers):
    if not numbers:
        return 0
    return numbers[0] + sum_recursive(numbers[1:])

# Iterative: More memory-efficient
def sum_iterative(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

numbers = [1, 2, 3, 4, 5]
print(sum_recursive(numbers))   # 15
print(sum_iterative(numbers))   # 15
```

## Factorial Comparison

```python
# Recursive: Elegant, matches mathematical notation
def factorial_recursive(n):
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)

# Iterative: More predictable performance
def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

print(factorial_recursive(5))   # 120
print(factorial_iterative(5))   # 120
```

## Tree Traversal: Recursion's Strength

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

# Recursive: Simple and clear
def count_nodes_recursive(node):
    count = 1
    for child in node.children:
        count += count_nodes_recursive(child)
    return count

# Iterative: Requires stack data structure
def count_nodes_iterative(root):
    count = 0
    stack = [root]
    while stack:
        node = stack.pop()
        count += 1
        stack.extend(node.children)
    return count
```

## Performance and Memory

```python
import sys

# Check stack depth limit
print(f"Recursion limit: {sys.getrecursionlimit()}")

# Iterative uses constant stack space
# Recursive uses O(n) stack space

# For large n, iteration is safer
def large_sum_iterative(n):
    return sum(range(n))

def large_sum_recursive(n):
    if n <= 0:
        return 0
    return n + large_sum_recursive(n - 1)
```

## When to Use Each

**Use Recursion for:**
- Tree/graph traversal
- Divide-and-conquer algorithms
- Mathematical problem definitions
- When code clarity is priority

**Use Iteration for:**
- Simple loops (for, while)
- Processing sequences
- When memory/stack is limited
- Performance-critical code

---

## Exercises

**Exercise 1.**
Write both recursive and iterative versions of a function `count_digits(n)` that returns the number of digits in a positive integer. Compare both on the input `123456789`.

??? success "Solution to Exercise 1"

        # Recursive
        def count_digits_recursive(n):
            if n < 10:
                return 1
            return 1 + count_digits_recursive(n // 10)

        # Iterative
        def count_digits_iterative(n):
            count = 0
            while n > 0:
                count += 1
                n //= 10
            return count

        print(count_digits_recursive(123456789))  # 9
        print(count_digits_iterative(123456789))  # 9

---

**Exercise 2.**
Implement both recursive and iterative versions of `fibonacci(n)`. Time both for `n = 30` and `n = 35` and compare performance. Explain why the recursive version is dramatically slower.

??? success "Solution to Exercise 2"

        import time

        # Recursive (exponential time)
        def fib_recursive(n):
            if n < 2:
                return n
            return fib_recursive(n - 1) + fib_recursive(n - 2)

        # Iterative (linear time)
        def fib_iterative(n):
            if n < 2:
                return n
            a, b = 0, 1
            for _ in range(n - 1):
                a, b = b, a + b
            return b

        for n in [30, 35]:
            start = time.time()
            r = fib_recursive(n)
            t_rec = time.time() - start

            start = time.time()
            i = fib_iterative(n)
            t_iter = time.time() - start

            print(f"n={n}: recursive={t_rec:.3f}s, iterative={t_iter:.6f}s")
        # Recursive is exponential O(2^n); iterative is O(n).

---

**Exercise 3.**
Write a recursive `tree_depth(node)` function that returns the maximum depth of a binary tree (where each node has `.left` and `.right` attributes). Then write an iterative version using a stack. Build a sample tree and verify both return the same result.

??? success "Solution to Exercise 3"

        class TreeNode:
            def __init__(self, val, left=None, right=None):
                self.val = val
                self.left = left
                self.right = right

        # Recursive
        def tree_depth_recursive(node):
            if node is None:
                return 0
            return 1 + max(tree_depth_recursive(node.left),
                           tree_depth_recursive(node.right))

        # Iterative (using stack with depth tracking)
        def tree_depth_iterative(root):
            if root is None:
                return 0
            max_depth = 0
            stack = [(root, 1)]
            while stack:
                node, depth = stack.pop()
                max_depth = max(max_depth, depth)
                if node.left:
                    stack.append((node.left, depth + 1))
                if node.right:
                    stack.append((node.right, depth + 1))
            return max_depth

        root = TreeNode(1,
            TreeNode(2, TreeNode(4), TreeNode(5)),
            TreeNode(3, None, TreeNode(6, TreeNode(7), None)),
        )

        print(tree_depth_recursive(root))  # 4
        print(tree_depth_iterative(root))  # 4
