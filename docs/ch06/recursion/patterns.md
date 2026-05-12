# Recursion Patterns

!!! tip "Mental Model"
    Recursive problems come in recognizable shapes. Direct recursion calls itself; indirect recursion bounces between functions; linear recursion makes one recursive call per step; tree recursion branches into multiple calls. Recognizing the pattern tells you the time complexity and whether optimizations like memoization or tail-call conversion apply.

## Types of Recursion

### 1. Direct Recursion

A function calls itself directly.

```
f → f → f → base case
```

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)  # Direct call to itself

print(factorial(5))  # 120
```

### 2. Indirect Recursion

Functions call each other in a cycle.

```
f → g → f → g → base case
```

```python
n = 1

def print_odd():
    global n
    if n <= 10:
        print(n + 1, end=" ")
        n += 1
        print_even()

def print_even():
    global n
    if n <= 10:
        print(n - 1, end=" ")
        n += 1
        print_odd()

print_odd()  # 2 1 4 3 6 5 8 7 10 9
```


## Tail vs Non-Tail Recursion

### 1. Tail Recursion

The recursive call is the **last operation** — nothing happens after it returns.

```python
def countdown(n):
    if n == 0:
        return
    print(n, end=" ")
    return countdown(n - 1)  # Last operation

countdown(3)  # 3 2 1
```

### 2. Non-Tail Recursion

Operations occur **after** the recursive call returns.

```python
def countdown_reverse(n):
    if n == 0:
        return
    countdown_reverse(n - 1)  # Not the last operation
    print(n, end=" ")         # This happens after

countdown_reverse(3)  # 1 2 3
```

### 3. Why It Matters

Tail recursion can theoretically be optimized to use constant stack space (tail call optimization). However, **Python does not implement TCO**, so both forms use O(n) stack space.

```python
# Tail recursive factorial
def factorial_tail(n, acc=1):
    if n <= 1:
        return acc
    return factorial_tail(n - 1, n * acc)

# Still causes stack overflow for large n in Python
```


## Fibonacci: A Case Study

The Fibonacci sequence demonstrates different recursion strategies.

$$F(n) = F(n-1) + F(n-2), \quad F(0)=0, \quad F(1)=1$$

### 1. Naïve Recursion — O(2^n)

```python
def fib_naive(n):
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)
```

**Problem**: Exponential time due to repeated calculations.

```
fib(5)
├── fib(4)
│   ├── fib(3)
│   │   ├── fib(2)
│   │   └── fib(1)
│   └── fib(2)
└── fib(3)
    ├── fib(2)
    └── fib(1)
```

Time complexity: $T(n) \in \Theta(\phi^n)$ where $\phi = \frac{1+\sqrt{5}}{2} \approx 1.618$

### 2. Memoization (Top-Down) — O(n)

Cache results to avoid redundant calculations.

```python
memo = {0: 0, 1: 1}

def fib_memo(n):
    if n in memo:
        return memo[n]
    memo[n] = fib_memo(n - 1) + fib_memo(n - 2)
    return memo[n]

print(fib_memo(50))  # 12586269025
```

Or using `@lru_cache`:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_cached(n):
    if n < 2:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)
```

- Time: O(n)
- Space: O(n) for cache + O(n) for call stack

### 3. Tabulation (Bottom-Up) — O(n) time, O(1) space

Build solution iteratively from base cases.

```python
def fib_iterative(n):
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

print(fib_iterative(50))  # 12586269025
```

- Time: O(n)
- Space: O(1)
- No recursion stack

### 4. Binet's Formula — O(1)

Closed-form solution using the golden ratio.

$$F(n) = \frac{\phi^n - (-\phi)^{-n}}{\sqrt{5}}, \quad \phi = \frac{1+\sqrt{5}}{2}$$

```python
import math

def fib_binet(n):
    phi = (1 + math.sqrt(5)) / 2
    return round((phi**n - (-phi)**(-n)) / math.sqrt(5))

print(fib_binet(50))  # 12586269025
```

**Caveat**: Floating-point errors make this inaccurate for large n.


## Complexity Comparison

| Method | Time | Space | Stack Depth | Best For |
|--------|------|-------|-------------|----------|
| Naïve Recursion | O(2^n) | O(n) | Deep | Education only |
| Memoization | O(n) | O(n) | Moderate | When recursion preferred |
| Tabulation | O(n) | O(1) | None | Production use |
| Binet's Formula | O(1) | O(1) | None | Approximation only |


## Classic Recursive Problems

### 1. Sum to N

```python
def sum_to_n(n):
    if n == 0:
        return 0
    return n + sum_to_n(n - 1)

print(sum_to_n(10))  # 55
```

### 2. Triangular Numbers

$$T_n = T_{n-1} + n, \quad T_1 = 1$$

```python
def triangular(n):
    if n == 1:
        return 1
    return triangular(n - 1) + n

for i in range(1, 7):
    print(f"T_{i} = {triangular(i)}")
# T_1 = 1, T_2 = 3, T_3 = 6, T_4 = 10, T_5 = 15, T_6 = 21
```

### 3. Tower of Hanoi

$$a_n = 2a_{n-1} + 1, \quad a_1 = 1$$

Minimum moves to solve n-disk puzzle.

```python
def hanoi_moves(n):
    if n == 1:
        return 1
    return 2 * hanoi_moves(n - 1) + 1

for i in range(1, 8):
    print(f"n={i}: {hanoi_moves(i)} moves")
# n=1: 1, n=2: 3, n=3: 7, n=4: 15, n=5: 31, n=6: 63, n=7: 127
```


## Advantages and Disadvantages

### Advantages

1. **Elegant code** — Natural expression for recursive problems
2. **Divide-and-conquer** — Breaks complex problems into subproblems
3. **Tree structures** — Natural fit for trees and graphs

### Disadvantages

1. **Stack overhead** — Each call adds a frame
2. **Performance** — Function call overhead vs iteration
3. **Stack overflow** — Deep recursion hits Python's limit
4. **Debugging** — Harder to trace execution flow


## When to Use Recursion

**Use recursion when:**

- Problem has recursive structure (trees, graphs)
- Divide-and-conquer is natural
- Code clarity matters more than performance
- Depth is bounded and manageable

**Use iteration when:**

- Simple loops suffice
- Performance is critical
- Deep recursion is possible
- Stack overflow is a concern


## Summary

- **Direct recursion**: Function calls itself
- **Indirect recursion**: Functions call each other cyclically
- **Tail recursion**: Recursive call is last operation (no TCO in Python)
- **Memoization**: Top-down DP, caches results
- **Tabulation**: Bottom-up DP, iterative
- **Trade-off**: Recursion for clarity, iteration for performance

---

## Runnable Example: `greedy_algorithm_example.py`

```python
"""
Greedy Algorithm: The Knapsack Problem

A greedy algorithm makes the locally optimal choice at each step,
hoping to find a global optimum. It doesn't always find the best
solution, but it finds a satisfactory one quickly.

Topics covered:
- Greedy strategy: best value-to-weight ratio first
- OOP with @property for computed attributes
- sorted() with custom key functions

Based on concepts from Python-100-Days example04 and ch05/recursion materials.
"""


# =============================================================================
# Example 1: Item Class with Computed Property
# =============================================================================

class Item:
    """An item with name, value, and weight.

    The value_per_weight property computes the efficiency ratio,
    which the greedy algorithm uses to prioritize items.
    """

    def __init__(self, name: str, value: float, weight: float):
        self.name = name
        self.value = value
        self.weight = weight

    @property
    def value_per_weight(self) -> float:
        """Value-to-weight ratio (higher = more efficient)."""
        return self.value / self.weight

    def __repr__(self):
        return (f"Item('{self.name}', value={self.value}, "
                f"weight={self.weight}, ratio={self.value_per_weight:.2f})")


# =============================================================================
# Example 2: Greedy Knapsack (0/1 variant)
# =============================================================================

def greedy_knapsack(items: list[Item], capacity: float) -> tuple[list[Item], float]:
    """Select items using greedy strategy: best value/weight ratio first.

    This is the 0/1 knapsack variant - items cannot be split.
    The greedy approach doesn't guarantee the optimal solution for 0/1
    knapsack, but it's fast: O(n log n) for sorting + O(n) for selection.

    Args:
        items: Available items to choose from.
        capacity: Maximum weight the knapsack can hold.

    Returns:
        Tuple of (selected items, total value).

    >>> items = [Item('A', 60, 10), Item('B', 100, 20), Item('C', 120, 30)]
    >>> selected, value = greedy_knapsack(items, 50)
    >>> value
    220.0
    """
    # Sort by value-to-weight ratio (highest first)
    sorted_items = sorted(items, key=lambda x: x.value_per_weight, reverse=True)

    selected = []
    total_weight = 0.0
    total_value = 0.0

    for item in sorted_items:
        if total_weight + item.weight <= capacity:
            selected.append(item)
            total_weight += item.weight
            total_value += item.value

    return selected, total_value


# =============================================================================
# Example 3: Fractional Knapsack (items can be split)
# =============================================================================

def fractional_knapsack(items: list[Item], capacity: float) -> float:
    """Fractional knapsack: items can be partially taken.

    The greedy approach IS optimal for fractional knapsack.
    Take items by best ratio; if an item doesn't fully fit,
    take the fraction that fits.

    >>> items = [Item('A', 60, 10), Item('B', 100, 20), Item('C', 120, 30)]
    >>> fractional_knapsack(items, 50)
    240.0
    """
    sorted_items = sorted(items, key=lambda x: x.value_per_weight, reverse=True)

    total_value = 0.0
    remaining = capacity

    for item in sorted_items:
        if remaining <= 0:
            break
        if item.weight <= remaining:
            total_value += item.value
            remaining -= item.weight
        else:
            # Take partial item
            fraction = remaining / item.weight
            total_value += item.value * fraction
            remaining = 0

    return total_value


# =============================================================================
# Example 4: Practical Demo
# =============================================================================

def demo():
    """Demonstrate greedy knapsack with sample items."""
    items = [
        Item('Gold Bar',    500, 25),
        Item('Diamond',     300,  5),
        Item('Painting',    200, 15),
        Item('Laptop',      150,  3),
        Item('Sculpture',   100, 20),
        Item('Book Set',     50, 10),
    ]
    capacity = 40

    print("=== Available Items ===")
    print(f"{'Name':<12} {'Value':>6} {'Weight':>6} {'Ratio':>8}")
    print("-" * 35)
    for item in items:
        print(f"{item.name:<12} {item.value:>6.0f} {item.weight:>6.0f} "
              f"{item.value_per_weight:>8.2f}")
    print(f"\nKnapsack capacity: {capacity}")

    # 0/1 Knapsack (greedy)
    selected, value = greedy_knapsack(items, capacity)
    print(f"\n--- 0/1 Knapsack (Greedy) ---")
    total_weight = sum(item.weight for item in selected)
    for item in selected:
        print(f"  Selected: {item.name} (value={item.value}, weight={item.weight})")
    print(f"  Total value:  {value:.0f}")
    print(f"  Total weight: {total_weight:.0f}/{capacity}")

    # Fractional Knapsack (greedy - optimal)
    frac_value = fractional_knapsack(items, capacity)
    print(f"\n--- Fractional Knapsack (Greedy, Optimal) ---")
    print(f"  Total value: {frac_value:.0f}")

    print("\nNote: Greedy is optimal for fractional knapsack but NOT")
    print("guaranteed optimal for 0/1 knapsack. Dynamic programming")
    print("is needed for optimal 0/1 solutions.")


if __name__ == '__main__':
    demo()
```

---

## Exercises

**Exercise 1.**
Write both a naive recursive and a memoized version of a function `tribonacci(n)` that computes the n-th Tribonacci number (defined as `T(n) = T(n-1) + T(n-2) + T(n-3)`, with `T(0)=0, T(1)=0, T(2)=1`). Compare the number of calls for `n=20` using a call counter.

??? success "Solution to Exercise 1"

        # Naive version
        naive_calls = 0

        def tribonacci_naive(n):
            global naive_calls
            naive_calls += 1
            if n == 0 or n == 1:
                return 0
            if n == 2:
                return 1
            return tribonacci_naive(n-1) + tribonacci_naive(n-2) + tribonacci_naive(n-3)

        # Memoized version
        memo_calls = 0

        def tribonacci_memo(n, cache=None):
            global memo_calls
            memo_calls += 1
            if cache is None:
                cache = {}
            if n in cache:
                return cache[n]
            if n == 0 or n == 1:
                return 0
            if n == 2:
                return 1
            cache[n] = (tribonacci_memo(n-1, cache)

                        + tribonacci_memo(n-2, cache)
                        + tribonacci_memo(n-3, cache))
            return cache[n]

        print(tribonacci_naive(20), f"({naive_calls} calls)")
        print(tribonacci_memo(20), f"({memo_calls} calls)")

---

**Exercise 2.**
Implement the Tower of Hanoi solution as a recursive function `hanoi(n, source, target, auxiliary)` that prints each move (e.g., `"Move disk 1 from A to C"`). Verify the number of moves for `n=4` equals `2^4 - 1 = 15`.

??? success "Solution to Exercise 2"

        move_count = 0

        def hanoi(n, source="A", target="C", auxiliary="B"):
            global move_count
            if n == 1:
                move_count += 1
                print(f"Move disk 1 from {source} to {target}")
                return
            hanoi(n - 1, source, auxiliary, target)
            move_count += 1
            print(f"Move disk {n} from {source} to {target}")
            hanoi(n - 1, auxiliary, target, source)

        hanoi(4)
        print(f"Total moves: {move_count}")  # 15

---

**Exercise 3.**
Write an indirect recursion example: function `is_even(n)` calls `is_odd(n - 1)`, and `is_odd(n)` calls `is_even(n - 1)`. The base case for both is `n == 0` (`is_even(0)` returns `True`, `is_odd(0)` returns `False`). Test with several inputs and verify correctness.

??? success "Solution to Exercise 3"

        def is_even(n):
            if n == 0:
                return True
            return is_odd(n - 1)

        def is_odd(n):
            if n == 0:
                return False
            return is_even(n - 1)

        for i in range(6):
            print(f"{i}: even={is_even(i)}, odd={is_odd(i)}")
        # 0: even=True,  odd=False
        # 1: even=False, odd=True
        # 2: even=True,  odd=False
        # ...
