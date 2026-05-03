# sys Runtime Information

Access runtime information like memory usage, loaded modules, and recursion limits.

!!! tip "Mental Model"
    `sys` runtime functions are the interpreter's dashboard gauges. `sys.getsizeof()` shows an object's memory footprint, `sys.getrecursionlimit()` reveals how deep the call stack can go, and `sys.modules` lists everything that has been imported. Use these tools to diagnose memory bloat, stack overflows, or unexpected import side effects.

## Memory and Resource Information

Check memory and system resources.

```python
import sys
import gc

# Garbage collection
gc.collect()
print(f"GC stats: {gc.get_stats()}")

# Reference count
x = [1, 2, 3]
print(f"Reference count: {sys.getrefcount(x)}")

# Recursion limit
print(f"Recursion limit: {sys.getrecursionlimit()}")

# Stack info
import traceback
print(f"Call stack depth: {len(traceback.extract_stack())}")
```

```
GC stats: [{'collections': 123}]
Reference count: 2
Recursion limit: 1000
Call stack depth: 5
```

## Modules and Paths

Check loaded modules and search paths.

```python
import sys

# Module path
print(f"Python path: {sys.path[:3]}")

# Loaded modules
core_modules = [m for m in sys.modules if not '.' in m]
print(f"Core modules loaded: {len(core_modules)}")

# Module info
if 'json' in sys.modules:
    print("json module is loaded")

# Standard modules
import json
print(f"json module path: {json.__file__}")
```

```
Python path: ['', '/usr/lib/python3.12', '/usr/lib/python3.12/lib-dynload']
Core modules loaded: 25
json module is loaded
json module path: /usr/lib/python3.12/json/__init__.py
```

---

## Exercises

**Exercise 1.**
Write a function `loaded_modules_count` that returns a dictionary with two keys: `"total"` (total number of loaded modules in `sys.modules`) and `"builtin"` (number of built-in modules, identifiable by having no `__file__` attribute).

??? success "Solution to Exercise 1"

    ```python
    import sys

    def loaded_modules_count():
        total = len(sys.modules)
        builtin = sum(
            1 for m in sys.modules.values()
            if m is not None and not hasattr(m, "__file__")
        )
        return {"total": total, "builtin": builtin}

    # Test
    counts = loaded_modules_count()
    print(f"Total modules: {counts['total']}")
    print(f"Built-in modules: {counts['builtin']}")
    ```

---

**Exercise 2.**
Write a function `recursion_test` that gets the current recursion limit using `sys.getrecursionlimit()`, temporarily sets it to 50, attempts a recursive function to demonstrate the limit, then restores the original limit.

??? success "Solution to Exercise 2"

    ```python
    import sys

    def recursion_test():
        original = sys.getrecursionlimit()
        print(f"Original limit: {original}")

        sys.setrecursionlimit(50)
        print(f"Temporary limit: {sys.getrecursionlimit()}")

        def recurse(n):
            if n <= 0:
                return 0
            return recurse(n - 1)

        try:
            recurse(100)
        except RecursionError:
            print("RecursionError caught as expected")
        finally:
            sys.setrecursionlimit(original)
            print(f"Restored limit: {sys.getrecursionlimit()}")

    recursion_test()
    ```

---

**Exercise 3.**
Write a function `object_references` that takes an object and returns the reference count using `sys.getrefcount`. Demonstrate by creating a list, assigning it to multiple variables, and showing how the reference count increases.

??? success "Solution to Exercise 3"

    ```python
    import sys

    def object_references():
        a = [1, 2, 3]
        print(f"After creation: {sys.getrefcount(a)}")
        # Note: getrefcount adds 1 temporary reference

        b = a
        print(f"After b = a: {sys.getrefcount(a)}")

        c = a
        print(f"After c = a: {sys.getrefcount(a)}")

        del b
        print(f"After del b: {sys.getrefcount(a)}")

    object_references()
    ```
