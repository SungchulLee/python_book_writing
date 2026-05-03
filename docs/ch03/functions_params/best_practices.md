# Parameter Best Practices

This page consolidates the decision rules from the 2.13 section into practical guidance.

!!! tip "Mental Model"
    Good parameter design makes call sites readable without checking the signature. Use positional parameters for the one or two main inputs, keyword-only (`*`) for optional flags, and `*args`/`**kwargs` only when the interface is genuinely variable. Default to `None` instead of mutable defaults, and use `/` to lock down implementation-detail parameter names.

## Use Keyword-Only Parameters for Optional Configuration

When a function has optional boolean flags or configuration values, force callers to name them. Positional boolean arguments are unreadable at the call site:

```python
# What do True and False mean here?
process_file("data.txt", True, False)

# Keyword-only makes intent unambiguous
def process_file(path: str, *, verbose: bool = False, overwrite: bool = False) -> None:
    ...

process_file("data.txt", verbose=True)
```

Use `*` to introduce keyword-only parameters whenever a caller would have to look up the function signature to understand what a positional argument means. The built-in `print()` is a familiar example — `sep` and `end` are keyword-only so callers never have to remember their position:

```python
print(1, 2, 3, sep="-")   # 1-2-3
print("done", end="!\n")  # done!
```

## Use *args and **kwargs Only When the Interface Is Genuinely Variable

`*args` and `**kwargs` are appropriate for forwarding patterns and variadic APIs. A timing wrapper is a classic example — it forwards all arguments transparently:

```python
import time

def timed(func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    print(f"{func.__name__} took {elapsed:.4f}s")
    return result

timed(sorted, [3, 1, 4, 1, 5], reverse=True)  # sorted took 0.0000s
```

Avoid them when the parameters are actually known — they hide the interface from callers, type checkers, and documentation tools. If your function always takes a name and an age, declare `name: str, age: int` explicitly.

## Never Use Mutable Objects as Default Values

Default values are evaluated once at definition time, not at each call. A mutable default accumulates state across calls:

```python
# Bad — the list is shared across all calls
def append_to(item, target=[]):
    target.append(item)
    return target

# Good — a fresh list is created on each call
def append_to(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target
```

The rule applies to all mutable defaults: lists, dicts, sets, and custom objects. Always default to `None` and create the mutable object inside the function body. See [Default Parameter Gotcha](default_parameter_gotcha.md) for the full explanation.

## Signal Mutation Intent with -> None

A function that modifies its argument in place and returns nothing should be annotated `-> None`. This tells callers — and static analysis tools — that the function works by side effect:

```python
def sort_in_place(items: list[int]) -> None:
    """Sort the list in place. The original is modified."""
    items.sort()

def sorted_copy(items: list[int]) -> list[int]:
    """Return a new sorted list. The original is unchanged."""
    return sorted(items)
```

When you see `-> None` on a function that takes a mutable argument, expect the argument to be modified. When you see a return value, expect the original to be untouched.

## Protect Mutable Arguments When You Don't Intend to Mutate

If a function should not modify its input, use non-mutating alternatives:

```python
# Accidentally destroys original order
def stats(numbers: list[int]) -> tuple[int, int]:
    numbers.sort()
    return numbers[0], numbers[-1]

# Correct — sorted() returns a new list
def stats(numbers: list[int]) -> tuple[int, int]:
    s = sorted(numbers)
    return s[0], s[-1]
```

Prefer `sorted()` over `.sort()`, `+` over `.append()` when you want a new object, and `.copy()` when you need an explicit shallow copy. For nested structures use `copy.deepcopy` — covered in the data structures chapter.

## Consider a Dataclass When kwargs Gets Large

If a function takes more than four or five keyword arguments, the signature is a sign that the arguments belong together as a structured object:

```python
# Hard to call correctly, hard to extend
def create_server(host, port, timeout=30, retries=3, ssl=False, cert=None):
    ...

# Better — group related config into a dataclass
from dataclasses import dataclass

@dataclass
class ServerConfig:
    host: str
    port: int
    timeout: int = 30
    retries: int = 3
    ssl: bool = False
    cert: str | None = None

def create_server(config: ServerConfig) -> None:
    ...
```

This pattern makes defaults visible, enables validation, and keeps the function signature stable as requirements grow. Dataclasses are covered in the classes chapter.

## Key Ideas

- Make boolean flags and optional settings keyword-only to prevent ambiguous positional calls.
- Use `*args`/`**kwargs` for forwarding patterns; prefer explicit parameters when the interface is fixed.
- Always default mutable parameters to `None` and create the object inside the function body.
- Don't mutate arguments unless mutation is the function's purpose. Signal intent with `-> None` vs a return type.
- When keyword arguments proliferate, extract them into a dataclass or configuration object.

---

## Exercises


**Exercise 1.**
Rewrite the following function to follow best practices: use keyword-only arguments for configuration parameters and provide sensible defaults.

```python
def send_email(to, subject, body, cc, bcc, html, priority):
    pass
```

??? success "Solution to Exercise 1"

        ```python
        def send_email(to, subject, body, *, cc=None, bcc=None,
                       html=False, priority="normal"):
            print(f"To: {to}, Subject: {subject}")
            print(f"CC: {cc}, BCC: {bcc}, HTML: {html}, Priority: {priority}")

        send_email("alice@example.com", "Hello", "Body text")
        send_email("bob@example.com", "Urgent", "Body", priority="high", html=True)
        ```

    The `*` separator forces configuration parameters to be keyword-only, making calls self-documenting.

---

**Exercise 2.**
Write a function `create_user(name, *, email=None, role="viewer", active=True)` that returns a dictionary. The `*` forces `email`, `role`, and `active` to be keyword-only. Demonstrate calling it correctly and incorrectly.

??? success "Solution to Exercise 2"

        ```python
        def create_user(name, *, email=None, role="viewer", active=True):
            return {"name": name, "email": email, "role": role, "active": active}

        # Correct usage
        user = create_user("Alice", email="alice@example.com", role="admin")
        print(user)

        # Incorrect usage
        try:
            create_user("Bob", "bob@example.com")  # Positional not allowed
        except TypeError as e:
            print(f"Error: {e}")
        ```

    Keyword-only arguments prevent positional mistakes and make the call site explicit.

---

**Exercise 3.**
Explain why using `*args` and `**kwargs` together can make APIs harder to understand. Write an example where explicit parameters are better than `**kwargs`.

??? success "Solution to Exercise 3"

        ```python
        # Hard to understand: what kwargs are valid?
        def configure(**kwargs):
            host = kwargs.get("host", "localhost")
            port = kwargs.get("port", 8080)
            debug = kwargs.get("debug", False)
            # Typos like "debugg=True" silently ignored!

        # Better: explicit parameters with defaults
        def configure(host="localhost", port=8080, debug=False):
            pass  # IDE can autocomplete, typos caught immediately

        # configure(debugg=True)  # TypeError: unexpected keyword argument
        ```

    Explicit parameters provide documentation, IDE support, and error checking for typos. Use `**kwargs` only when the set of valid keys is truly dynamic.
