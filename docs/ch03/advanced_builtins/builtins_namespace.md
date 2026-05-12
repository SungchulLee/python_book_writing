# The `builtins`

Python’s built-in functions, exceptions, and types live in the **`builtins` namespace**. Understanding this namespace clarifies what is always available without imports.

!!! tip "Mental Model"
    Think of `builtins` as Python’s always-open toolbox -- every name you use without an import (`len`, `print`, `int`, `ValueError`) lives there. When you accidentally shadow one of these names with your own variable, you are placing a sticky note over a tool in the toolbox; removing the note (`del`) reveals the original tool underneath.

---

## What is `builtins`?

`builtins` is a module automatically loaded by Python that contains:

- core functions (`len`, `print`, `range`, …),
- built-in types (`int`, `list`, `dict`, …),
- built-in exceptions (`ValueError`, `TypeError`, …).

You normally use these names without qualification.

---

## Inspecting

```python
import builtins
dir(builtins)
```

This shows all names that are globally available.

---

## Shadowing builtins

You can accidentally override built-ins:

```python
list = [1, 2, 3]   # BAD
```

After this, `list()` no longer refers to the type.

Avoid shadowing built-in names.

---

## Why this matters

Understanding `builtins` helps with:

- debugging name conflicts,
- reading unfamiliar code,
- metaprogramming and introspection.

---

## Key takeaways

- Built-ins live in the `builtins` module.
- They are always available without imports.
- Avoid shadowing built-in names.

---

## Exercises


**Exercise 1.**
Write a function `count_builtins_by_type()` that returns a dictionary with three keys: `"functions"`, `"exceptions"`, and `"other"`. Iterate over all names in the `builtins` module, look up each attribute with `getattr`, and classify each as an exception class (subclass of `BaseException`), a callable (function or type), or other. Return the counts for each category.

??? success "Solution to Exercise 1"

        ```python
        import builtins

        def count_builtins_by_type():
            counts = {"functions": 0, "exceptions": 0, "other": 0}
            for name in dir(builtins):
                obj = getattr(builtins, name)
                if isinstance(obj, type) and issubclass(obj, BaseException):
                    counts["exceptions"] += 1
                elif callable(obj):
                    counts["functions"] += 1
                else:
                    counts["other"] += 1
            return counts

        print(count_builtins_by_type())
        ```

    The function checks for exception classes first using `issubclass(obj, BaseException)`, then classifies remaining callables as functions. Everything else (constants like `True`, `None`) goes into "other".

---

**Exercise 2.**
Without running the code, predict the output of the following snippet. Then verify your prediction.

```python
list = [1, 2, 3]
try:
    result = list("hello")
except TypeError as e:
    print(f"Error: {e}")

del list
result = list("hello")
print(result)
```

??? success "Solution to Exercise 2"

    The output is:

        ```
        Error: 'list' object is not callable
        ['h', 'e', 'l', 'l', 'o']
        ```

    Assigning `list = [1, 2, 3]` shadows the built-in `list` class. Calling `list("hello")` tries to call the list *object*, which raises `TypeError`. After `del list`, the local name is removed and the built-in `list` becomes accessible again.

---

**Exercise 3.**
Write a function `safe_builtin(name)` that takes a string and returns the corresponding built-in object if it exists, or `None` otherwise. Use the `builtins` module and `getattr` with a default value. Test it with `"len"`, `"print"`, and `"foobar"`.

??? success "Solution to Exercise 3"

        ```python
        import builtins

        def safe_builtin(name):
            return getattr(builtins, name, None)

        print(safe_builtin("len"))      # <built-in function len>
        print(safe_builtin("print"))    # <built-in function print>
        print(safe_builtin("foobar"))   # None
        ```

    Using `getattr` with a default of `None` avoids raising `AttributeError` when the name does not exist in the `builtins` module.
