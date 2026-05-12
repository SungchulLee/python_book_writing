# Tree Recursion

Tree recursion occurs when a function calls itself multiple times per invocation, creating a tree-like call pattern. This is common in problems with overlapping subproblems.

!!! tip "Mental Model"
    Tree recursion branches at every call -- each invocation spawns two or more recursive calls, forming a tree of computation. Without memoization, the same subproblems are recomputed many times, leading to exponential time. Recognizing tree recursion is the first step toward applying memoization or converting to bottom-up dynamic programming.

---

## Fibonacci: Classic Tree Recursion

```python
def fibonacci(n):
    '''Fibonacci sequence using naive recursion'''
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Example calls
print(fibonacci(5))   # Output: 5
print(fibonacci(6))   # Output: 8
```

The call tree for `fibonacci(5)`:
```
                fibonacci(5)
              /            \
        fibonacci(4)      fibonacci(3)
        /      \          /      \
    fib(3)  fib(2)    fib(2)  fib(1)
    /  \    / \      / \
fib(2) fib(1) fib(1) fib(0) ...
```

Notice `fibonacci(3)` and `fibonacci(2)` are computed multiple times!

## Counting Recursive Calls

```python
def fibonacci_counted(n, call_count=None):
    '''Fibonacci with call counter'''
    if call_count is None:
        call_count = {'count': 0}
    
    call_count['count'] += 1
    
    if n <= 1:
        return n
    return fibonacci_counted(n - 1, call_count) + fibonacci_counted(n - 2, call_count)

# Count calls for different inputs
for n in [5, 10, 15, 20]:
    call_count = {'count': 0}
    fibonacci_counted(n, call_count)
    print(f"fib({n:2d}): {call_count['count']:6d} calls")
```

Output:
```
fib( 5):     15 calls
fib(10):    177 calls
fib(15):   1973 calls
fib(20):  21891 calls
```

## Binary Search Tree Traversal

```python
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def traverse_tree(node, result=None):
    '''In-order tree traversal'''
    if result is None:
        result = []
    
    if node is None:
        return result
    
    traverse_tree(node.left, result)
    result.append(node.value)
    traverse_tree(node.right, result)
    
    return result

# Build and traverse
root = TreeNode(4)
root.left = TreeNode(2)
root.right = TreeNode(6)
root.left.left = TreeNode(1)
root.left.right = TreeNode(3)

print(traverse_tree(root))  # [1, 2, 3, 4, 6]
```

## Performance Comparison

The exponential nature of tree recursion means small input size changes cause huge performance differences. Use memoization (chapter on memoization) to fix this.

---

## Exercises

**Exercise 1.**
Write a tree-recursive function `count_partitions(n, max_part)` that counts the number of ways to partition the integer `n` using parts up to `max_part`. For example, `count_partitions(6, 4)` returns `9`. Identify the two recursive branches (use the largest part vs. exclude it).

??? success "Solution to Exercise 1"

        def count_partitions(n, max_part):
            if n == 0:
                return 1
            if n < 0 or max_part == 0:
                return 0
            # Use max_part + don't use max_part
            return (count_partitions(n - max_part, max_part)

                    + count_partitions(n, max_part - 1))

        print(count_partitions(6, 4))   # 9
        print(count_partitions(5, 5))   # 7
        print(count_partitions(10, 5))  # 30

---

**Exercise 2.**
Add a call counter to the naive recursive `fibonacci(n)` function. Compute `fibonacci(25)` and print the total number of function calls. Then add `@lru_cache` and repeat, printing the new call count to demonstrate the dramatic difference.

??? success "Solution to Exercise 2"

        from functools import lru_cache

        # Without memoization
        naive_calls = 0

        def fib_naive(n):
            global naive_calls
            naive_calls += 1
            if n < 2:
                return n
            return fib_naive(n - 1) + fib_naive(n - 2)

        fib_naive(25)
        print(f"Naive calls for fib(25): {naive_calls}")  # 242785

        # With memoization
        memo_calls = 0

        @lru_cache(maxsize=None)
        def fib_cached(n):
            global memo_calls
            memo_calls += 1
            if n < 2:
                return n
            return fib_cached(n - 1) + fib_cached(n - 2)

        fib_cached(25)
        print(f"Cached calls for fib(25): {memo_calls}")  # 26

---

**Exercise 3.**
Write a tree-recursive function `paths_in_grid(rows, cols)` that counts the number of unique paths from the top-left to the bottom-right of a `rows x cols` grid, where you can only move right or down. Draw the call tree for `paths_in_grid(3, 3)` in a comment and verify the result is `6`.

??? success "Solution to Exercise 3"

        def paths_in_grid(rows, cols):
            # Base cases
            if rows == 1 or cols == 1:
                return 1
            # Move down + move right
            return paths_in_grid(rows - 1, cols) + paths_in_grid(rows, cols - 1)

        print(paths_in_grid(3, 3))  # 6
        print(paths_in_grid(4, 4))  # 20

        # Call tree for paths_in_grid(3, 3):
        #                 (3,3)
        #                /     \
        #           (2,3)       (3,2)
        #           /   \       /   \
        #       (1,3) (2,2)  (2,2) (3,1)
        #              / \    / \
        #          (1,2)(2,1)(1,2)(2,1)
