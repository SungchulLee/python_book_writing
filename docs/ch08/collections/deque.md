# deque

A `deque` (double-ended queue, pronounced "deck") supports O(1) appends and pops from both ends. It's the go-to data structure for queues and sliding windows.

!!! tip "Mental Model"
    Picture a deck of cards you can deal from either end in constant time. A Python list is fast at the right end but slow at the left because it must shift every element. A `deque` uses a doubly-linked block structure, so pushing or popping from either side is always O(1) — making it the natural choice for queues, stacks, and fixed-size sliding windows.

---

## The Problem with Lists

Lists are slow for front operations:

```python
lst = [1, 2, 3, 4, 5]

lst.append(6)       # O(1) ✅
lst.pop()           # O(1) ✅

lst.insert(0, 0)    # O(n) ❌ shifts all elements
lst.pop(0)          # O(n) ❌ shifts all elements
```

---

## deque Solution

```python
from collections import deque

d = deque([1, 2, 3, 4, 5])

# Right operations (like list)
d.append(6)         # O(1)
d.pop()             # O(1)

# Left operations (fast!)
d.appendleft(0)     # O(1)
d.popleft()         # O(1)
```

---

## Performance Comparison

| Operation | list | deque |
|-----------|------|-------|
| `append(x)` | O(1) | O(1) |
| `pop()` | O(1) | O(1) |
| `insert(0, x)` | **O(n)** | O(1) |
| `pop(0)` | **O(n)** | O(1) |
| `x[i]` (random access) | O(1) | **O(n)** |

**Trade-off**: deque has O(n) random access, but O(1) at both ends.

---

## Basic Operations

```python
from collections import deque

d = deque([1, 2, 3])

# Add elements
d.append(4)         # [1, 2, 3, 4]
d.appendleft(0)     # [0, 1, 2, 3, 4]

# Remove elements
d.pop()             # Returns 4, deque is [0, 1, 2, 3]
d.popleft()         # Returns 0, deque is [1, 2, 3]

# Extend
d.extend([4, 5])    # [1, 2, 3, 4, 5]
d.extendleft([0, -1])  # [-1, 0, 1, 2, 3, 4, 5]
# Note: extendleft reverses order!
```

---

## Rotation

Rotate elements in-place:

```python
d = deque([1, 2, 3, 4, 5])

d.rotate(2)         # Rotate right: [4, 5, 1, 2, 3]
d.rotate(-2)        # Rotate left: [1, 2, 3, 4, 5]
```

### Use Case: Round-Robin

```python
tasks = deque(['A', 'B', 'C', 'D'])
for _ in range(8):
    current = tasks[0]
    print(f"Processing: {current}")
    tasks.rotate(-1)  # Move to next
```

---

## Fixed-Size deque (maxlen)

Automatically discards old items when full:

```python
d = deque(maxlen=3)

d.append(1)         # [1]
d.append(2)         # [1, 2]
d.append(3)         # [1, 2, 3]
d.append(4)         # [2, 3, 4] - 1 dropped!
d.append(5)         # [3, 4, 5] - 2 dropped!
```

### Use Case: Recent History

```python
# Keep last 5 actions for undo
history = deque(maxlen=5)

history.append('edit')
history.append('delete')
history.append('paste')
# ... more actions
# Only last 5 are kept
```

### Use Case: Moving Average

```python
from collections import deque

def moving_average(values, window_size):
    window = deque(maxlen=window_size)
    for value in values:
        window.append(value)
        if len(window) == window_size:
            yield sum(window) / window_size

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(list(moving_average(data, 3)))
# [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
```

---

## Queue Implementation

### FIFO Queue (First-In-First-Out)

```python
from collections import deque

queue = deque()

# Enqueue
queue.append('first')
queue.append('second')
queue.append('third')

# Dequeue
queue.popleft()     # 'first'
queue.popleft()     # 'second'
queue.popleft()     # 'third'
```

### Stack (LIFO)

```python
stack = deque()

stack.append('first')
stack.append('second')
stack.append('third')

stack.pop()         # 'third'
stack.pop()         # 'second'
stack.pop()         # 'first'
```

---

## BFS with deque

Breadth-First Search requires a queue:

```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    
    while queue:
        node = queue.popleft()  # O(1)
        if node not in visited:
            visited.add(node)
            print(node)
            queue.extend(graph.get(node, []))
    
    return visited

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [], 'E': [], 'F': []
}

bfs(graph, 'A')  # A, B, C, D, E, F
```

---

## Sliding Window

```python
from collections import deque

def sliding_window_max(nums, k):
    """Find max in each window of size k."""
    result = []
    window = deque()  # Stores indices
    
    for i, num in enumerate(nums):
        # Remove indices outside window
        while window and window[0] <= i - k:
            window.popleft()
        
        # Remove smaller elements (won't be max)
        while window and nums[window[-1]] < num:
            window.pop()
        
        window.append(i)
        
        if i >= k - 1:
            result.append(nums[window[0]])
    
    return result

print(sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))
# [3, 3, 5, 5, 6, 7]
```

---

## Other Methods

```python
d = deque([1, 2, 3, 2, 1])

len(d)              # 5
d.count(2)          # 2
d.index(3)          # 2 (first occurrence)
d.remove(2)         # Remove first 2: [1, 3, 2, 1]
d.reverse()         # In-place: [1, 2, 3, 1]
d.clear()           # Empty deque
```

---

## deque vs list vs queue.Queue

| Feature | `deque` | `list` | `queue.Queue` |
|---------|---------|--------|---------------|
| Thread-safe | ❌ | ❌ | ✅ |
| O(1) both ends | ✅ | ❌ | ✅ |
| Random access | O(n) | O(1) | ❌ |
| maxlen | ✅ | ❌ | ✅ (maxsize) |
| Use case | General | Random access | Threading |

---

## Key Takeaways

- `deque` has O(1) operations at both ends
- Use for queues, stacks, and sliding windows
- `maxlen` auto-discards old items
- `rotate()` for circular operations
- Essential for BFS and efficient queue implementations
- Trade-off: O(n) random access (use list if needed)

---

## Exercises

**Exercise 1.**
Write a function `is_palindrome_deque` that takes a string and uses a `deque` to check if it is a palindrome (ignoring spaces and case). Pop from both ends simultaneously and compare characters. For example, `is_palindrome_deque("race car")` should return `True`.

??? success "Solution to Exercise 1"

    ```python
    from collections import deque

    def is_palindrome_deque(text):
        cleaned = deque(text.lower().replace(" ", ""))
        while len(cleaned) > 1:
            if cleaned.popleft() != cleaned.pop():
                return False
        return True

    # Test
    print(is_palindrome_deque("race car"))   # True
    print(is_palindrome_deque("hello"))      # False
    print(is_palindrome_deque("A man a plan a canal Panama"))  # True
    ```

---

**Exercise 2.**
Write a function `sliding_window_avg` that takes a list of numbers and a window size `k`, and returns a list of the average of each sliding window. Use a `deque` with `maxlen=k`. For example, `sliding_window_avg([1, 3, 5, 7, 9], 3)` should return `[3.0, 5.0, 7.0]`.

??? success "Solution to Exercise 2"

    ```python
    from collections import deque

    def sliding_window_avg(nums, k):
        window = deque(maxlen=k)
        result = []
        for num in nums:
            window.append(num)
            if len(window) == k:
                result.append(sum(window) / k)
        return result

    # Test
    print(sliding_window_avg([1, 3, 5, 7, 9], 3))
    # [3.0, 5.0, 7.0]
    print(sliding_window_avg([10, 20, 30, 40], 2))
    # [15.0, 25.0, 35.0]
    ```

---

**Exercise 3.**
Write a function `interleave_queues` that takes two lists, creates a `deque` from each, and returns a single list produced by alternately popping from the left of each deque until both are empty. For example, `interleave_queues([1, 2, 3], ['a', 'b'])` should return `[1, 'a', 2, 'b', 3]`.

??? success "Solution to Exercise 3"

    ```python
    from collections import deque

    def interleave_queues(list1, list2):
        q1 = deque(list1)
        q2 = deque(list2)
        result = []
        while q1 or q2:
            if q1:
                result.append(q1.popleft())
            if q2:
                result.append(q2.popleft())
        return result

    # Test
    print(interleave_queues([1, 2, 3], ['a', 'b']))
    # [1, 'a', 2, 'b', 3]
    print(interleave_queues([1], [10, 20, 30]))
    # [1, 10, 20, 30]
    ```
