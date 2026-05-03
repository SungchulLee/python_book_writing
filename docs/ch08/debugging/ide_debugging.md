# IDE Debugging Overview

Overview of debugging capabilities in popular Python IDEs.

!!! tip "Mental Model"
    IDE debuggers wrap pdb's power in a visual interface — you click in the gutter to set breakpoints, hover over variables to see values, and step through code with toolbar buttons instead of typing commands. The underlying mechanics are the same as pdb, but the graphical layer makes it easier to navigate complex call stacks and watch many variables at once.

## IDE Debugging Features

Most IDEs provide visual debuggers.

```python
# IDE debugging typically provides:
# - Breakpoints (click on line number)
# - Variable inspection in watch window
# - Call stack visualization
# - Step through code visually
# - Conditional breakpoints
# - Debug console for expressions

def factorial(n):
    if n <= 1:
        return 1
    # Set breakpoint on next line in IDE
    return n * factorial(n - 1)

result = factorial(5)
print(f"5! = {result}")
```

```
5! = 120
```

## Remote Debugging

Debug applications running on remote servers.

```python
# Python debuggers support remote debugging
# Example: debugpy for VS Code

# In application (server-side):
import debugpy

debugpy.listen(('0.0.0.0', 5678))
debugpy.wait_for_client()

def remote_function():
    x = 10
    return x * 2

result = remote_function()
print(result)

# In IDE, connect to localhost:5678 to debug
```

```
Waiting for debugger to attach...
```

---

## Exercises

**Exercise 1.**
Write a recursive function `fibonacci(n)` that returns the nth Fibonacci number. Identify where you would place a conditional breakpoint (in an IDE) to pause only when `n == 5`. Write the function and include a comment indicating the breakpoint line and condition.

??? success "Solution to Exercise 1"

    ```python
    def fibonacci(n):
        if n <= 0:
            return 0
        if n == 1:
            return 1
        # IDE breakpoint here with condition: n == 5
        return fibonacci(n - 1) + fibonacci(n - 2)

    # Test
    for i in range(8):
        print(f"fib({i}) = {fibonacci(i)}")
    # fib(0) = 0, fib(1) = 1, fib(2) = 1, ...
    ```

---

**Exercise 2.**
Write a function `process_records` that takes a list of dictionaries (each with `"name"` and `"score"` keys) and returns the names of records with scores above 90. Include a comment showing where you would set a breakpoint with a hit count condition (break only after the 3rd iteration) in an IDE debugger.

??? success "Solution to Exercise 2"

    ```python
    def process_records(records):
        high_scorers = []
        for i, record in enumerate(records):
            # IDE breakpoint here with hit count = 3
            # to pause on the 3rd record
            if record["score"] > 90:
                high_scorers.append(record["name"])
        return high_scorers

    # Test
    data = [
        {"name": "Alice", "score": 95},
        {"name": "Bob", "score": 80},
        {"name": "Carol", "score": 92},
        {"name": "Dave", "score": 88},
    ]
    print(process_records(data))  # ['Alice', 'Carol']
    ```

---

**Exercise 3.**
Write a function `search_matrix` that takes a 2D list and a target value, and returns the `(row, col)` position of the target or `None`. Include comments describing how you would use the IDE watch window to monitor `row`, `col`, and `matrix[row][col]` while stepping through the nested loop.

??? success "Solution to Exercise 3"

    ```python
    def search_matrix(matrix, target):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                # IDE watch window: monitor row, col, matrix[row][col]
                # Step through with F10 (Step Over) to see values change
                if matrix[row][col] == target:
                    return (row, col)
        return None

    # Test
    grid = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    print(search_matrix(grid, 5))   # (1, 1)
    print(search_matrix(grid, 10))  # None
    ```
