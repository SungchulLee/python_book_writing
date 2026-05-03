# Common pdb Commands

Master the most useful pdb commands for effective debugging.

!!! tip "Mental Model"
    pdb commands fall into three categories: *navigation* (step, next, continue — controlling where execution goes), *inspection* (print, display, where — seeing program state), and *control* (break, condition, clear — managing breakpoints). Learning a handful from each category is enough to debug most issues efficiently.

## Navigation Commands

Commands for stepping through code.

```python
# Common pdb navigation:
# l - list current code section
# n (next) - execute next line
# s (step) - step into function
# c (continue) - resume execution
# u (up) - go up one frame
# d (down) - go down one frame
# j lineno (jump) - jump to line

def example():
    x = 1  # Breakpoint here, then n to next
    y = 2  # n again
    z = x + y  # s into any function calls
    return z

# In pdb session:
# (Pdb) l
# (Pdb) n
# (Pdb) s
# (Pdb) c
```

```
Commands accepted and executed in pdb
```

## Inspection Commands

Commands for examining variables and state.

```python
# Inspection commands in pdb:
# p expression - print value
# pp object - pretty print object
# whatis variable - show type
# h - help
# h command - help on specific command

def inspect_example(data):
    result = sum(data)
    count = len(data)
    # Breakpoint and inspect
    import pdb; pdb.set_trace()
    
    # In pdb:
    # (Pdb) p result
    # (Pdb) pp data
    # (Pdb) whatis count
    
    return result

print("Inspection commands available")
```

```
Inspection commands available
```

---

## Exercises

**Exercise 1.**
Write a function `accumulate_with_debug` that takes a list of numbers and returns a list of cumulative sums. Add a `pdb.set_trace()` call inside the loop. Then describe (in a comment) the sequence of pdb commands you would use to: list the code (`l`), print the running total (`p total`), step to the next iteration (`n`), and continue to the end (`c`).

??? success "Solution to Exercise 1"

    ```python
    import pdb

    def accumulate_with_debug(numbers):
        result = []
        total = 0
        for num in numbers:
            total += num
            # pdb.set_trace()  # Uncomment to debug
            # In pdb: l (list code), p total, p num, p result
            # Then: n (next), or c (continue to end)
            result.append(total)
        return result

    # Test
    print(accumulate_with_debug([1, 2, 3, 4, 5]))
    # [1, 3, 6, 10, 15]
    ```

---

**Exercise 2.**
Write a function `nested_lookup` that takes a nested dictionary and a list of keys representing a path (e.g., `["a", "b", "c"]` for `d["a"]["b"]["c"]`). Use `pdb.set_trace()` to debug the traversal. Add comments showing how you would use `p current`, `pp keys`, and `whatis current` to inspect state at each level.

??? success "Solution to Exercise 2"

    ```python
    import pdb

    def nested_lookup(data, keys):
        current = data
        for key in keys:
            # pdb.set_trace()  # Uncomment to debug
            # In pdb: p current, pp keys, whatis current
            # Use 'n' to step through each key
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current

    # Test
    nested = {"a": {"b": {"c": 42}}}
    print(nested_lookup(nested, ["a", "b", "c"]))  # 42
    print(nested_lookup(nested, ["a", "x"]))         # None
    ```

---

**Exercise 3.**
Write a function `buggy_sort` that attempts to implement a simple sorting algorithm but has a deliberate off-by-one bug. Add a `breakpoint()` call and describe in comments the pdb commands (`p`, `l`, `n`, `w` for call stack) you would use to identify the bug. Then fix the bug.

??? success "Solution to Exercise 3"

    ```python
    def buggy_sort(numbers):
        nums = numbers.copy()
        n = len(nums)
        # Bug was: range(n) instead of range(n - 1)
        for i in range(n - 1):
            for j in range(n - 1 - i):
                # breakpoint()  # Uncomment to debug
                # In pdb: p i, p j, p nums, l, w (call stack)
                if nums[j] > nums[j + 1]:
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]
        return nums

    # Test
    print(buggy_sort([5, 3, 8, 1, 2]))  # [1, 2, 3, 5, 8]
    print(buggy_sort([1]))               # [1]
    ```
