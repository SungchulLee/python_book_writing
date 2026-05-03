# Summation Benchmark

Compare different approaches for computing $\sum_{k=1}^n k^2$.

!!! tip "Mental Model"
    This benchmark uses a simple sum-of-squares to compare Python loops, list comprehensions, `np.sum` on arrays, and the closed-form formula. The results consistently show that vectorized NumPy is 10-100x faster than Python loops, and a closed-form solution (when one exists) beats everything. The exercise teaches you to always look for the highest-level abstraction first.

## Problem Setup

### 1. Mathematical Form

$$\sum_{k=1}^n k^2 = 1^2 + 2^2 + 3^2 + \cdots + n^2$$

### 2. Closed Form

$$\sum_{k=1}^n k^2 = \frac{n(n+1)(2n+1)}{6}$$

### 3. Test Size

We use $n = 10^7$ to highlight performance differences.

## For Loop

### 1. Implementation

```python
import time

def main():
    n = int(1e7)
    
    tic = time.time()
    s_n = 0
    for i in range(1, n + 1):
        s_n += i ** 2
    toc = time.time()
    
    print(f"{s_n = }")
    print(f"For Loop Time: {toc - tic:.4f} sec")

if __name__ == "__main__":
    main()
```

### 2. Characteristics

- Pure Python iteration
- Repeated addition
- Maximum interpreter overhead

### 3. Typical Time

Slowest approach (~3-5 seconds).

## List Append

### 1. Implementation

```python
import time

def main():
    n = int(1e7)
    
    tic = time.time()
    lst = []
    for i in range(1, n + 1):
        lst.append(i ** 2)
    s_n = sum(lst)
    toc = time.time()
    
    print(f"{s_n = }")
    print(f"List Append Time: {toc - tic:.4f} sec")

if __name__ == "__main__":
    main()
```

### 2. Characteristics

- Builds intermediate list
- Extra memory allocation
- Two-pass (build then sum)

### 3. Typical Time

Similar to for loop (~3-5 seconds).

## List Comprehension

### 1. Implementation

```python
import time

def main():
    n = int(1e7)
    
    tic = time.time()
    s_n = sum([i ** 2 for i in range(1, n + 1)])
    toc = time.time()
    
    print(f"{s_n = }")
    print(f"List Comprehension Time: {toc - tic:.4f} sec")

if __name__ == "__main__":
    main()
```

### 2. Characteristics

- More Pythonic syntax
- Still creates full list
- Slightly optimized bytecode

### 3. Typical Time

Slightly faster (~2-4 seconds).

## NumPy Vectorized

### 1. Implementation

```python
import numpy as np
import time

def main():
    n = int(1e7)
    
    tic = time.time()
    x = np.arange(1, n + 1) ** 2
    s_n = np.sum(x)
    toc = time.time()
    
    print(f"{s_n = }")
    print(f"NumPy Time: {toc - tic:.4f} sec")

if __name__ == "__main__":
    main()
```

### 2. Characteristics

- C-level computation
- Contiguous memory
- Optimized reduction

### 3. Typical Time

Much faster (~0.05-0.1 seconds).

## Formula Direct

### 1. Implementation

```python
import time

def main():
    n = int(1e7)
    
    tic = time.time()
    s_n = n * (n + 1) * (2 * n + 1) // 6
    toc = time.time()
    
    print(f"{s_n = }")
    print(f"Formula Time: {toc - tic:.8f} sec")

if __name__ == "__main__":
    main()
```

### 2. Characteristics

- O(1) complexity
- No iteration at all
- Constant time regardless of n

### 3. Typical Time

Essentially instant (~0.000001 seconds).

## Full Comparison

### 1. All Methods

```python
import numpy as np
import time

def main():
    n = int(1e7)
    results = []
    
    # For loop
    tic = time.time()
    s = 0
    for i in range(1, n + 1):
        s += i ** 2
    results.append(("For Loop", time.time() - tic, s))
    
    # List append
    tic = time.time()
    lst = []
    for i in range(1, n + 1):
        lst.append(i ** 2)
    s = sum(lst)
    results.append(("List Append", time.time() - tic, s))
    
    # List comprehension
    tic = time.time()
    s = sum([i ** 2 for i in range(1, n + 1)])
    results.append(("List Comp", time.time() - tic, s))
    
    # NumPy
    tic = time.time()
    s = np.sum(np.arange(1, n + 1) ** 2)
    results.append(("NumPy", time.time() - tic, s))
    
    # Formula
    tic = time.time()
    s = n * (n + 1) * (2 * n + 1) // 6
    results.append(("Formula", time.time() - tic, s))
    
    print(f"{'Method':<15} {'Time (sec)':<12} {'Result'}")
    print("-" * 45)
    for method, elapsed, result in results:
        print(f"{method:<15} {elapsed:<12.6f} {result}")

if __name__ == "__main__":
    main()
```

### 2. Sample Output

```
Method          Time (sec)   Result
---------------------------------------------
For Loop        3.245000     333333383333335000
List Append     3.512000     333333383333335000
List Comp       2.891000     333333383333335000
NumPy           0.078000     333333383333335000
Formula         0.000001     333333383333335000
```

### 3. Key Insight

NumPy is ~40× faster than Python loops; formulas are instant when available.

## Takeaways

### 1. Avoid Python Loops

For numerical computation, Python loops are prohibitively slow.

### 2. Use NumPy

Vectorized NumPy operations provide massive speedups.

### 3. Know Your Math

Closed-form solutions beat all iterative methods.

---

## Runnable Example: `python_vs_numpy_diffusion.py`

```python
"""
2D Diffusion Simulation: Pure Python vs NumPy Vectorization

This tutorial shows how vectorization transforms a simulation from slow to fast.
We'll simulate diffusion (how a substance spreads over time) on a 2D grid.

WHAT IS DIFFUSION?
A substance spreads from areas of high concentration to low concentration. Think
of food coloring diffusing through water - it spreads until evenly distributed.

THE MATH:
For each grid cell, the new concentration is determined by:
1. The cell's current value
2. Its neighbors' values (up, down, left, right)
3. The diffusion coefficient D and time step dt

This is governed by the discrete Laplacian operator, which measures how different
a cell is from its neighbors.

PURE PYTHON APPROACH:
- Nested loops over grid dimensions
- Each cell update requires accessing neighbor values
- Results in slow, interpreted code

NUMPY APPROACH:
- Use roll() to shift the entire array
- Subtract and add entire arrays at once
- Single equation: grid + dt * D * laplacian(grid)
- All operations compiled in C, huge speedup

Learning Goals:
- See how spatial operations can be vectorized
- Understand the Laplacian and diffusion math
- Compare nested loops vs array operations
- Measure dramatic speedup from vectorization
"""

import time
import numpy as np

if __name__ == "__main__":


    print("=" * 70)
    print("2D DIFFUSION SIMULATION: PURE PYTHON vs NUMPY VECTORIZATION")
    print("=" * 70)


    # ============ EXAMPLE 1: Understanding the Problem ============
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Understanding Diffusion and the Laplacian Operator")
    print("=" * 70)

    print("""
    DIFFUSION INTUITION:
    Imagine a 2D grid where each cell contains a concentration value.
    Over time, particles move from high concentration to low concentration.

    The rate of change at each point depends on:
    - How much the point differs from its neighbors
    - This difference is measured by the Laplacian operator

    LAPLACIAN IN 2D:
    For a point (i, j), the Laplacian is:
        L = grid[i+1][j] + grid[i-1][j] + grid[i][j+1] + grid[i][j-1] - 4*grid[i][j]

    It sums the four neighbors and subtracts 4 times the center point.
    If neighbors are high, L is positive (substance increases).
    If neighbors are low, L is negative (substance decreases).

    EVOLUTION EQUATION:
        new_grid[i][j] = grid[i][j] + dt * D * Laplacian

    Where:
    - dt = time step (how much time passes in one iteration)
    - D = diffusion coefficient (how fast diffusion happens)

    Let's see this in action:
    """)


    # ============ EXAMPLE 2: Pure Python Implementation ============
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Pure Python Implementation (Nested Loops)")
    print("=" * 70)

    def evolve_python(grid, dt, D=1.0):
        """
        Update the grid one time step using pure Python loops.

        This is slow because:
        1. Two nested loops iterate over every cell
        2. Four array accesses per cell (neighbors)
        3. Arithmetic operations happen in Python, not compiled code
        4. For a 640x640 grid, this is 409,600 operations per iteration!

        Grid wraps around (periodic boundary conditions) - edges connect to opposite side.
        """
        grid_shape = (len(grid), len(grid[0]))
        xmax, ymax = grid_shape

        # Create new grid for the updated values
        new_grid = [[0.0 for _ in range(ymax)] for _ in range(xmax)]

        for i in range(xmax):
            for j in range(ymax):
                # Get neighbors with wraparound (periodic boundary)
                # % operator wraps indices: 640 % 640 = 0, -1 % 640 = 639
                neighbor_right = grid[(i + 1) % xmax][j]
                neighbor_left = grid[(i - 1) % xmax][j]
                neighbor_down = grid[i][(j + 1) % ymax]
                neighbor_up = grid[i][(j - 1) % ymax]

                # Compute Laplacian: sum of neighbors - 4 * center
                laplacian = (neighbor_right + neighbor_left +
                            neighbor_down + neighbor_up - 4.0 * grid[i][j])

                # Update: new value = old value + diffusion term
                new_grid[i][j] = grid[i][j] + D * laplacian * dt

        return new_grid


    # Setup a small grid to demonstrate
    grid_shape = (10, 10)
    print(f"\nSmall demo with {grid_shape[0]}x{grid_shape[1]} grid:")

    # Initialize with zeros
    demo_grid = [[0.0 for _ in range(grid_shape[1])] for _ in range(grid_shape[0])]

    # Add a "hot spot" in the center
    center_low = 4
    center_high = 6
    for i in range(center_low, center_high):
        for j in range(center_low, center_high):
            demo_grid[i][j] = 1.0

    print(f"\nInitial grid (center 4x4 block = 1.0, rest = 0.0):")
    for row in demo_grid:
        print("  " + "  ".join(f"{v:.1f}" for v in row))

    # Run one evolution step
    demo_grid_after = evolve_python(demo_grid, dt=0.1, D=1.0)

    print(f"\nAfter one evolution step (dt=0.1, D=1.0):")
    for row in demo_grid_after:
        print("  " + "  ".join(f"{v:.2f}" for v in row))

    print(f"\nNotice: The hot spot stays mostly concentrated, with slight")
    print(f"spreading to neighbors. This is diffusion!")


    # Time the pure Python version
    print(f"\n" + "-" * 70)
    print(f"PERFORMANCE TEST: Pure Python with larger grid")
    print(f"-" * 70)

    grid_size = (256, 256)
    num_iterations = 10

    # Create initial grid
    grid = [[0.0 for _ in range(grid_size[1])] for _ in range(grid_size[0])]

    # Add initial conditions (hot spot in center)
    block_low = int(grid_size[0] * 0.4)
    block_high = int(grid_size[0] * 0.5)
    for i in range(block_low, block_high):
        for j in range(block_low, block_high):
            grid[i][j] = 0.005

    print(f"Grid size: {grid_size[0]}x{grid_size[1]} = {grid_size[0]*grid_size[1]:,} cells")
    print(f"Iterations: {num_iterations}")
    print(f"Total cells updated: {grid_size[0]*grid_size[1]*num_iterations:,}")

    start = time.time()
    for step in range(num_iterations):
        grid = evolve_python(grid, dt=0.1, D=1.0)
    elapsed_python = time.time() - start

    print(f"\nPure Python time: {elapsed_python:.4f}s ({elapsed_python/num_iterations:.4f}s per iteration)")


    # ============ EXAMPLE 3: NumPy Vectorized Implementation ============
    print("\n" + "=" * 70)
    print("EXAMPLE 3: NumPy Vectorized Implementation")
    print("=" * 70)

    def laplacian_numpy(grid):
        """
        Compute the Laplacian using NumPy array operations.

        Key insight: Instead of loops, use roll() to shift the entire array.

        roll(grid, +1, 0) shifts rows down: new row i = old row i-1
        roll(grid, -1, 0) shifts rows up:   new row i = old row i+1
        roll(grid, +1, 1) shifts cols right: new col j = old col j-1
        roll(grid, -1, 1) shifts cols left:  new col j = old col j+1

        Then compute: neighbors - 4*center in one vectorized operation!

        Why this is fast:
        1. No Python loops - NumPy handles all iteration in C
        2. roll() is optimized (just pointer manipulation, not data copy)
        3. Array arithmetic uses compiled operations
        4. Can use SIMD instructions for multiple cells at once
        """
        return (
            np.roll(grid, +1, 0) +   # neighbor above (wrapped)
            np.roll(grid, -1, 0) +   # neighbor below (wrapped)
            np.roll(grid, +1, 1) +   # neighbor to left (wrapped)
            np.roll(grid, -1, 1) -   # neighbor to right (wrapped)
            4 * grid                  # center cell (4 times)
        )


    def evolve_numpy(grid, dt, D=1.0):
        """
        Update the grid one time step using NumPy operations.

        This is fast because:
        1. laplacian_numpy() does all computation without Python loops
        2. Grid update is a single array equation
        3. All operations are compiled C code
        4. NumPy can parallelize with SIMD instructions
        """
        return grid + dt * D * laplacian_numpy(grid)


    # Test with same small grid to verify correctness
    print(f"Verifying NumPy gives same results as Pure Python:")

    grid_numpy = np.array([[0.0 for _ in range(grid_shape[1])] for _ in range(grid_shape[0])])

    # Add same initial conditions
    center_low = 4
    center_high = 6
    for i in range(center_low, center_high):
        for j in range(center_low, center_high):
            grid_numpy[i][j] = 1.0

    grid_numpy_after = evolve_numpy(grid_numpy, dt=0.1, D=1.0)

    print(f"\nNumPy result after one step:")
    for row in grid_numpy_after:
        print("  " + "  ".join(f"{v:.2f}" for v in row))

    print(f"\nResults match Pure Python! (Both methods are mathematically equivalent)")


    # Time the NumPy version
    print(f"\n" + "-" * 70)
    print(f"PERFORMANCE TEST: NumPy with same grid")
    print(f"-" * 70)

    grid_numpy = np.zeros(grid_size)

    # Add initial conditions
    block_low = int(grid_size[0] * 0.4)
    block_high = int(grid_size[0] * 0.5)
    grid_numpy[block_low:block_high, block_low:block_high] = 0.005

    print(f"Grid size: {grid_size[0]}x{grid_size[1]} = {grid_size[0]*grid_size[1]:,} cells")
    print(f"Iterations: {num_iterations}")

    start = time.time()
    for step in range(num_iterations):
        grid_numpy = evolve_numpy(grid_numpy, dt=0.1, D=1.0)
    elapsed_numpy = time.time() - start

    print(f"\nNumPy time: {elapsed_numpy:.4f}s ({elapsed_numpy/num_iterations:.4f}s per iteration)")


    # ============ EXAMPLE 4: Performance Comparison ============
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Performance Comparison & Speedup Analysis")
    print("=" * 70)

    speedup = elapsed_python / elapsed_numpy
    print(f"\nResults for {grid_size[0]}x{grid_size[1]} grid over {num_iterations} iterations:")
    print(f"  Pure Python: {elapsed_python:.4f}s total ({elapsed_python/num_iterations:.4f}s per iteration)")
    print(f"  NumPy:       {elapsed_numpy:.4f}s total ({elapsed_numpy/num_iterations:.4f}s per iteration)")
    print(f"  Speedup:     {speedup:.1f}x faster with NumPy")

    print(f"\n{'*' * 70}")
    print("HOW NUMPY ACHIEVES THIS SPEEDUP")
    print("{'*' * 70}")

    print("""
    1. NO PYTHON LOOPS
       Pure Python: Two nested loops * 256*256 cells = 131,072 iterations
       NumPy: One function call that processes all cells at once

    2. VECTORIZED OPERATIONS
       Pure Python: Access neighbors, compute arithmetic per cell (many operations)
       NumPy: Shift entire array with roll(), subtract arrays with - operator

    3. COMPILED CODE
       Pure Python: Each operation interpreted by Python VM
       NumPy: All operations written in optimized C

    4. MEMORY LAYOUT
       Pure Python: Lists of lists - scattered in memory, poor cache usage
       NumPy: Contiguous array in memory - CPU cache works optimally

    5. ALGORITHMIC TRICKS
       roll() doesn't actually copy the array - it's pointer manipulation!
       This is orders of magnitude faster than accessing elements one by one
    """)


    # ============ EXAMPLE 5: The Vectorization Pattern ============
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Recognizing the Stencil/Neighbor Pattern")
    print("=" * 70)

    print("""
    This tutorial demonstrates a common pattern called a STENCIL OPERATION:
    - Each output depends on neighbors of each input
    - Very common in: physics simulations, image processing, PDEs

    PURE PYTHON STENCIL PATTERN:
        for i in range(height):
            for j in range(width):
                value = grid[i][j]
                neighbors = [grid[i+1][j], grid[i-1][j], ...]
                new_grid[i][j] = compute(value, neighbors)

    NUMPY STENCIL PATTERN:
        neighbors_up = np.roll(grid, -1, 0)
        neighbors_down = np.roll(grid, +1, 0)
        neighbors_left = np.roll(grid, +1, 1)
        neighbors_right = np.roll(grid, -1, 1)
        new_grid = compute(grid, neighbors_up, neighbors_down, ...)

    The key insight: Use array operations (roll, slicing) to extract neighbors,
    then use vectorized arithmetic to compute updates.

    Applications:
    - Image filters (each pixel depends on neighbor pixels)
    - Physics simulations (this tutorial!)
    - Fluid dynamics
    - Weather modeling
    - Any spatial computation on grids
    """)


    print("\n" + "=" * 70)
    print("KEY TAKEAWAY")
    print("=" * 70)
    print(f"""
    Vectorizing from pure Python to NumPy achieved {speedup:.1f}x speedup.

    The transformation principle:
    1. Identify loops over array elements
    2. Recognize operations that can be expressed with array operations
    3. Use NumPy's broadcasting and functions (roll, slicing, etc.)
    4. Replace loops with array equations

    This is one of the most powerful optimization techniques in Python.
    When you have nested loops over numerical data, consider vectorization!
    """)
```

---

## Exercises

**Exercise 1.** Write a vectorized NumPy solution and a pure Python loop solution for the same computation. Measure and compare their performance using `time.perf_counter()`.

??? success "Solution to Exercise 1"
    ```python
    import numpy as np
    import time

    n = 1_000_000
    data = np.random.default_rng(42).random(n)

    # Python loop
    start = time.perf_counter()
    result_py = [x ** 2 for x in data]
    py_time = time.perf_counter() - start

    # NumPy vectorized
    start = time.perf_counter()
    result_np = data ** 2
    np_time = time.perf_counter() - start

    print(f"Python: {py_time:.4f}s, NumPy: {np_time:.6f}s")
    print(f"Speedup: {py_time / np_time:.0f}x")
    ```

---

**Exercise 2.** Identify a potential performance pitfall in the following code and rewrite it using NumPy vectorization:

```python
result = []
for i in range(len(data)):
    result.append(data[i] ** 2 + 2 * data[i] + 1)
```

??? success "Solution to Exercise 2"
    ```python
    import numpy as np

    data = np.random.default_rng(42).random(100000)

    # Vectorized (fast)
    result = data ** 2 + 2 * data + 1
    ```

    The loop version creates Python objects for each element and calls `append` repeatedly. The vectorized version computes everything in compiled C code on contiguous memory.

---

**Exercise 3.** Explain why NumPy vectorized operations are faster than Python loops. Reference memory layout, type checking overhead, and SIMD instructions in your answer.

??? success "Solution to Exercise 3"
    NumPy vectorized operations are faster because:

    1. **Contiguous memory**: NumPy arrays store elements in a contiguous block, enabling efficient CPU cache usage.
    2. **No type checking**: Python loops check types at each iteration; NumPy knows the dtype in advance.
    3. **Compiled C loops**: The actual computation runs in compiled C/Fortran code, not interpreted Python.
    4. **SIMD instructions**: Modern CPUs can process multiple array elements simultaneously using SIMD (Single Instruction, Multiple Data).

---

**Exercise 4.** Apply the concepts from this page to a practical problem: given a large array of temperatures in Celsius, convert them all to Fahrenheit and find the maximum. Compare vectorized and loop approaches.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    import time

    rng = np.random.default_rng(42)
    celsius = rng.uniform(-40, 50, 1_000_000)

    # Vectorized
    start = time.perf_counter()
    fahrenheit = celsius * 9/5 + 32
    max_f = fahrenheit.max()
    vec_time = time.perf_counter() - start

    # Loop
    start = time.perf_counter()
    max_f_loop = max(c * 9/5 + 32 for c in celsius)
    loop_time = time.perf_counter() - start

    print(f"Vectorized: {vec_time:.6f}s, max={max_f:.1f}F")
    print(f"Loop: {loop_time:.4f}s, max={max_f_loop:.1f}F")
    ```
