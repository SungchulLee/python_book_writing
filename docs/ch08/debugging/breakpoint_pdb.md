# breakpoint() and pdb Basics

Use breakpoint() to start the debugger and understand pdb for interactive debugging.

!!! tip "Mental Model"
    Calling `breakpoint()` is like pressing pause on a running program. Execution freezes at that line and drops you into an interactive shell where you can inspect variables, step through code one line at a time, and test expressions live. It is the fastest way to see what your code is actually doing versus what you think it is doing.

## breakpoint() Function

Add breakpoints to pause execution for inspection.

```python
def calculate(x, y):
    result = x + y
    breakpoint()  # Debugger will start here
    return result * 2

# When executed, this will start pdb debugger
# You can inspect variables and step through code
print("Debugger example")
```

```
Debugger example
> /path/to/script.py(3)calculate()
-> breakpoint()
```

## pdb Basics

Understand pdb debugger and basic commands.

```python
import pdb

def debug_function(items):
    total = 0
    for i, item in enumerate(items):
        # Start debugger at specific point
        if item > 5:
            pdb.set_trace()
        total += item
    return total

# Debugger commands:
# l - list code
# n - next line
# s - step into function
# c - continue
# p variable - print variable
# pp dict - pretty print

result = debug_function([1, 2, 3, 6, 7])
print(f"Result: {result}")
```

```
Result: 19
```

---

## Exercises

**Exercise 1.**
Write a function `find_first_negative` that takes a list of numbers and returns the index of the first negative number. Insert a `breakpoint()` call just before the return statement so you can inspect the variables when debugging. Remove the breakpoint after testing. For example, `find_first_negative([3, 7, -2, 5])` should return `2`.

??? success "Solution to Exercise 1"

    ```python
    def find_first_negative(numbers):
        for i, num in enumerate(numbers):
            if num < 0:
                # breakpoint()  # Uncomment to debug
                return i
        return -1

    # Test
    print(find_first_negative([3, 7, -2, 5]))  # 2
    print(find_first_negative([1, 2, 3]))       # -1
    ```

---

**Exercise 2.**
Write a function `debug_dict_merge` that takes two dictionaries and merges them. If there are duplicate keys, the function should keep the higher value. Add a conditional `pdb.set_trace()` that only triggers when a duplicate key is found. For example, `debug_dict_merge({"a": 1, "b": 5}, {"b": 3, "c": 4})` should return `{"a": 1, "b": 5, "c": 4}`.

??? success "Solution to Exercise 2"

    ```python
    import pdb

    def debug_dict_merge(d1, d2):
        result = d1.copy()
        for key, value in d2.items():
            if key in result:
                # pdb.set_trace()  # Uncomment to debug duplicates
                result[key] = max(result[key], value)
            else:
                result[key] = value
        return result

    # Test
    merged = debug_dict_merge({"a": 1, "b": 5}, {"b": 3, "c": 4})
    print(merged)  # {'a': 1, 'b': 5, 'c': 4}
    ```

---

**Exercise 3.**
Write a function `trace_recursive_sum` that recursively sums a list of numbers. Use `breakpoint()` with a condition to only pause when the list has exactly 2 elements remaining. This demonstrates conditional breakpoint placement for debugging recursion.

??? success "Solution to Exercise 3"

    ```python
    def trace_recursive_sum(numbers):
        if len(numbers) == 0:
            return 0
        if len(numbers) == 1:
            return numbers[0]
        # if len(numbers) == 2:
        #     breakpoint()  # Uncomment to debug
        mid = len(numbers) // 2
        left = trace_recursive_sum(numbers[:mid])
        right = trace_recursive_sum(numbers[mid:])
        return left + right

    # Test
    print(trace_recursive_sum([1, 2, 3, 4, 5]))  # 15
    print(trace_recursive_sum([10]))               # 10
    ```
