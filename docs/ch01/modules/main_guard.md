
# __name__ == "__main__"

Python modules can be executed in two different ways:

1. run directly as a script
2. imported as a module

The variable `__name__` helps distinguish these cases.

```mermaid
flowchart TD
    A[Python file]
    A --> B{run directly?}
    B -->|yes| C[__name__ = "__main__"]
    B -->|no| D[__name__ = module name]
````

!!! tip "Mental Model"
    Every Python file wears a name tag. When you run it directly, the tag reads `"__main__"`; when it is imported, the tag reads the module's actual name. The `if __name__ == "__main__"` guard uses this tag to separate code that should only run when the file is executed as a script from code that should be available when imported.

---

## 1. The **name** Variable

Every Python module has a special variable called `__name__`.

When a file is run directly:

```python
print(__name__)
```

Output:

```text
__main__
```

When the file is imported, `__name__` becomes the module name.

---

## 2. The Main Guard Pattern

The most common pattern is:

```python
if __name__ == "__main__":
    main()
```

Example:

```python
def main():
    print("Running program")

if __name__ == "__main__":
    main()
```

---

## 3. Why This Is Useful

The main guard prevents code from running during import.

Example:

```python
# tools.py

print("module loaded")
```

If imported, the print statement runs immediately.

The main guard avoids this problem.

---

## 4. Typical Program Structure

```python
def main():
    print("program logic")

if __name__ == "__main__":
    main()
```

This pattern separates:

* reusable code
* script execution

---

## 5. Example

File `math_tools.py`

```python
def square(x):
    return x * x

def main():
    print(square(5))

if __name__ == "__main__":
    main()
```

Running the file:

```text
25
```

Importing it:

```python
import math_tools
```

No output occurs.

---


## 6. Summary

Key ideas:

* `__name__` identifies how a module is executed
* `__name__ == "__main__"` is true when a file runs directly
* the main guard prevents unintended execution during import
* this pattern is common in Python programs

The main guard makes modules reusable while still allowing standalone execution.


## Exercises

**Exercise 1.**
A programmer creates `utils.py`:

```python
# utils.py
def helper():
    return 42

print("utils loaded")
result = helper()
print(f"result = {result}")
```

Predict what happens when another file runs `import utils`. Why is the output problematic? Rewrite `utils.py` using the main guard to fix it.

??? success "Solution to Exercise 1"
    When `import utils` runs, Python executes the entire file. Output:

    ```text
    utils loaded
    result = 42
    ```

    This is problematic because the `print` statements and the `helper()` call execute every time someone imports the module. The importer just wants access to `helper()`, not to run it.

    Fixed with the main guard:

    ```python
    # utils.py
    def helper():
        return 42

    if __name__ == "__main__":
        print("utils loaded")
        result = helper()
        print(f"result = {result}")
    ```

    Now `import utils` only defines `helper()` without printing anything. Running `python utils.py` directly still produces the output.

---

**Exercise 2.**
Explain the value of `__name__` in each scenario:

```python
# File: mymodule.py
print(f"__name__ = {__name__}")
```

What does `__name__` contain when: (a) you run `python mymodule.py` directly, (b) another file runs `import mymodule`, (c) another file runs `from mymodule import *`? Why does Python set `__name__` differently in each case?

??? success "Solution to Exercise 2"
    - **(a)** `python mymodule.py` directly: `__name__` = `"__main__"`. Python sets it to `"__main__"` for the file being executed as the entry point.
    - **(b)** `import mymodule`: `__name__` = `"mymodule"`. Python sets it to the module's name (derived from the filename without `.py`).
    - **(c)** `from mymodule import *`: `__name__` = `"mymodule"`. Same as regular import -- `from ... import` still executes the module file, and `__name__` is the module name.

    Python sets `__name__` differently to let code distinguish between "I am the main program" and "I am being used as a library." This is the mechanism that makes the main guard work: `if __name__ == "__main__"` is `True` only in case (a).

---

**Exercise 3.**
Some programs define a `main()` function, while others put code directly in the `if __name__` block:

```python
# Style A
if __name__ == "__main__":
    data = load_data()
    result = process(data)
    print(result)

# Style B
def main():
    data = load_data()
    result = process(data)
    print(result)

if __name__ == "__main__":
    main()
```

Both work. Why is Style B preferred? What practical advantage does having a `main()` function provide for testing and reuse?

??? success "Solution to Exercise 3"
    Style B is preferred for several reasons:

    1. **Testability**: other code can import and call `main()` directly for testing, without running the module as a script:
        ```python
        from mymodule import main
        main()  # Test the program's main logic
        ```

    2. **Local variables**: variables inside `main()` are local to the function. In Style A, `data`, `result`, etc. are global variables that could accidentally interfere with other module-level code.

    3. **Reusability**: `main()` can be called with arguments in more advanced patterns:
        ```python
        def main(args=None):
            ...
        ```

    4. **Profiling and debugging**: tools can target `main()` specifically, e.g., `cProfile.run("main()")`.

    Style A is acceptable for very short scripts, but Style B scales better as programs grow.
