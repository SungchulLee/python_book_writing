# functools.partial

`partial` freezes some arguments of a function, creating a new callable with fewer parameters. It's the standard way to do **partial function application** in Python.

!!! tip "Mental Model"
    `partial` is like setting default values from the outside: you take a general function, lock in one or more arguments, and get back a simpler, specialized version. Unlike `lambda`, the resulting `partial` object preserves the original function's identity and is easier to inspect and pickle.

```python
from functools import partial
```

---

## Basic Usage

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

# Freeze keyword argument
square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))   # 25
print(cube(5))     # 125

# Freeze positional argument
double = partial(pow, 2)  # pow(2, x)
print(double(8))   # 256 (2^8)
print(double(10))  # 1024 (2^10)
```

---

## How partial Works

`partial(func, *args, **kwargs)` returns a new callable that:

1. Prepends `args` to the positional arguments
2. Merges `kwargs` with keyword arguments (call-time kwargs override)

```python
from functools import partial

def greet(greeting, name, punctuation="!"):
    return f"{greeting}, {name}{punctuation}"

# Freeze 'greeting' positionally
hello = partial(greet, "Hello")
print(hello("Alice"))           # Hello, Alice!
print(hello("Bob", punctuation="."))  # Hello, Bob.

# Freeze keyword argument
casual = partial(greet, punctuation="~")
print(casual("Hey", "Alice"))   # Hey, Alice~
```

### Inspecting partial Objects

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)

print(square.func)      # <function power at 0x...>
print(square.args)      # ()
print(square.keywords)  # {'exponent': 2}

double = partial(pow, 2)
print(double.func)      # <built-in function pow>
print(double.args)      # (2,)
print(double.keywords)  # {}
```

---

## partial vs lambda

```python
from functools import partial

# These produce the same result:
f1 = partial(pow, 2)
f2 = lambda x: pow(2, x)

print(f1(10))  # 1024
print(f2(10))  # 1024
```

### Why Prefer partial

| Feature | `partial` | `lambda` |
|---------|----------|----------|
| Readability | Clear intent | Can be cryptic |
| Introspection | `.func`, `.args`, `.keywords` | Opaque |
| Pickling | Picklable | Not picklable |
| Performance | Slightly faster | Slight overhead |
| Late binding | No — arguments frozen at creation | Yes — evaluated at call time |

```python
from functools import partial

# Late binding gotcha with lambda
funcs = [lambda x: x + i for i in range(3)]
print([f(0) for f in funcs])  # [2, 2, 2] — all use i=2!

# partial avoids this
funcs = [partial(lambda x, i: x + i, i=i) for i in range(3)]
print([f(0) for f in funcs])  # [0, 1, 2] — correct!
```

### When lambda Is Better

```python
# Complex transformations that aren't simple argument freezing
transform = lambda x: x.strip().lower().replace(" ", "_")

# Conditional logic
process = lambda x: x * 2 if x > 0 else 0

# These can't be expressed cleanly with partial
```

---

## Practical Examples

### Customizing Built-in Functions

```python
from functools import partial

# Custom print
debug_print = partial(print, "[DEBUG]", end="\n\n")
debug_print("Starting process")
# [DEBUG] Starting process

error_print = partial(print, "[ERROR]", flush=True)
error_print("Something failed")
# [ERROR] Something failed

# Custom int parsing
parse_binary = partial(int, base=2)
parse_hex = partial(int, base=16)

print(parse_binary("1010"))  # 10
print(parse_hex("FF"))       # 255
```

### Sorting with Fixed Keys

```python
from functools import partial
from operator import itemgetter

# Sort list of dicts by specific key
sort_by_name = partial(sorted, key=itemgetter('name'))
sort_by_age = partial(sorted, key=itemgetter('age'))

users = [
    {'name': 'Charlie', 'age': 30},
    {'name': 'Alice', 'age': 25},
    {'name': 'Bob', 'age': 35},
]

print(sort_by_name(users))
# [{'name': 'Alice', ...}, {'name': 'Bob', ...}, {'name': 'Charlie', ...}]

print(sort_by_age(users))
# [{'name': 'Alice', ...}, {'name': 'Charlie', ...}, {'name': 'Bob', ...}]
```

### Callback Registration

```python
from functools import partial

def handle_event(event_type, data, timestamp=None):
    print(f"[{event_type}] {data} at {timestamp}")

# Register specialized handlers
on_click = partial(handle_event, "CLICK")
on_hover = partial(handle_event, "HOVER")
on_submit = partial(handle_event, "SUBMIT")

on_click("Button A", timestamp="12:00")
# [CLICK] Button A at 12:00
```

### Configuring API Clients

```python
from functools import partial
import json

def api_request(method, url, headers=None, timeout=30):
    """Simulated API request."""
    return f"{method} {url} (timeout={timeout})"

# Create pre-configured request functions
auth_headers = {"Authorization": "Bearer TOKEN"}
api_get = partial(api_request, "GET", headers=auth_headers)
api_post = partial(api_request, "POST", headers=auth_headers)
fast_get = partial(api_get, timeout=5)

print(api_get("/users"))
# GET /users (timeout=30)

print(fast_get("/health"))
# GET /health (timeout=5)
```

### Mathematical Functions

```python
from functools import partial
import math

# Logarithms with fixed base
log2 = partial(math.log, base=2)    # Actually: math.log(x, base=2)
log10 = partial(math.log, base=10)

# Note: math.log signature is log(x, base=e)
# So we need keyword argument for base
log2 = partial(math.log, 2)  # This is log(2, x) — wrong!

# Better approach for positional-only built-ins:
log2 = lambda x: math.log(x, 2)    # Use lambda here
log10 = lambda x: math.log(x, 10)

# Rounding with fixed precision
round2 = partial(round, ndigits=2)
round4 = partial(round, ndigits=4)

print(round2(3.14159))  # 3.14
print(round4(3.14159))  # 3.1416
```

---

## partialmethod — For Class Methods

`partialmethod` works like `partial` but is designed for use inside class definitions:

```python
from functools import partialmethod

class Connection:
    def __init__(self):
        self._connected = False

    def set_state(self, state):
        self._connected = state
        print(f"Connected: {self._connected}")

    connect = partialmethod(set_state, True)
    disconnect = partialmethod(set_state, False)

conn = Connection()
conn.connect()     # Connected: True
conn.disconnect()  # Connected: False
```

### Why Not Use Regular partial

```python
class Broken:
    def set_state(self, state):
        self._state = state

    # This doesn't work — partial doesn't know about 'self'
    # connect = partial(set_state, True)  # TypeError!

    # partialmethod handles the descriptor protocol correctly
    connect = partialmethod(set_state, True)  # Works!
```

---

## Chaining partial

```python
from functools import partial

def request(method, url, headers=None, timeout=30, retries=1):
    return f"{method} {url} (timeout={timeout}, retries={retries})"

# Build up configuration in layers
authenticated = partial(request, headers={"Auth": "token"})
fast_auth = partial(authenticated, timeout=5)
resilient_fast_auth = partial(fast_auth, retries=3)

print(resilient_fast_auth("GET", "/api/data"))
# GET /api/data (timeout=5, retries=3)
```

**Note**: Later keyword arguments override earlier ones:

```python
from functools import partial

def func(a=1, b=2, c=3):
    return (a, b, c)

p1 = partial(func, a=10, b=20)
p2 = partial(p1, b=99)  # Overrides b=20

print(p2())  # (10, 99, 3)
```

---

## Use with map, filter, sorted

```python
from functools import partial

# With map
numbers = [1, 2, 3, 4, 5]
multiply_by_3 = partial(lambda x, factor: x * factor, factor=3)
result = list(map(multiply_by_3, numbers))
print(result)  # [3, 6, 9, 12, 15]

# Simpler with operator
from operator import mul
triple = partial(mul, 3)
result = list(map(triple, numbers))
print(result)  # [3, 6, 9, 12, 15]

# With filter
is_greater_than_3 = partial(lambda threshold, x: x > threshold, 3)
result = list(filter(is_greater_than_3, numbers))
print(result)  # [4, 5]

# With sorted
data = ["banana", "apple", "cherry"]
sort_by_length = partial(sorted, key=len)
print(sort_by_length(data))  # ['apple', 'banana', 'cherry']
```

---

## Common Pitfalls

### Positional Argument Order

```python
from functools import partial

def divide(a, b):
    return a / b

# This fixes 'a', not 'b'
half = partial(divide, 2)  # divide(2, x) → 2/x, not x/2!
print(half(10))  # 0.2 (not 5.0!)

# To fix 'b', use keyword argument
half = partial(divide, b=2)  # divide(x, b=2) → x/2
print(half(10))  # 5.0
```

### Keyword Override Silently Replaces

```python
from functools import partial

def func(a, b, c):
    return (a, b, c)

p = partial(func, b=10)
print(p(1, c=3))       # (1, 10, 3)
print(p(1, b=99, c=3)) # (1, 99, 3) — b=10 silently overridden
```

---

## Summary

| Feature | Details |
|---------|---------|
| Import | `from functools import partial` |
| Purpose | Freeze arguments to create specialized functions |
| Attributes | `.func`, `.args`, `.keywords` |
| Class variant | `partialmethod` for methods in class bodies |
| Picklable | Yes (unlike lambda) |

**Key Takeaways**:

- `partial` freezes positional and keyword arguments, creating a simpler callable
- Prefer `partial` over `lambda` for simple argument freezing — it's more readable and inspectable
- Use `partialmethod` inside class definitions where `self` is involved
- Watch positional argument order — `partial(f, x)` always fills the first positional argument
- Later keyword arguments override earlier ones when chaining partial objects
- `partial` objects are picklable, making them suitable for multiprocessing

---

## Exercises

**Exercise 1.**
Write a `power(base, exponent)` function. Use `functools.partial` to create `square`, `cube`, and `fourth_power` functions. Verify each with the input `5`.

??? success "Solution to Exercise 1"

        from functools import partial

        def power(base, exponent):
            return base ** exponent

        square = partial(power, exponent=2)
        cube = partial(power, exponent=3)
        fourth_power = partial(power, exponent=4)

        print(square(5))        # 25
        print(cube(5))          # 125
        print(fourth_power(5))  # 625

---

**Exercise 2.**
Use `partial` to create a family of string formatting functions from a single `format_string(template, value)` function. Create `format_currency` (template `"${:.2f}"`), `format_percent` (template `"{:.1%}"`), and `format_scientific` (template `"{:.2e}"`). Test each.

??? success "Solution to Exercise 2"

        from functools import partial

        def format_string(template, value):
            return template.format(value)

        format_currency = partial(format_string, "${:.2f}")
        format_percent = partial(format_string, "{:.1%}")
        format_scientific = partial(format_string, "{:.2e}")

        print(format_currency(1234.5))     # $1234.50
        print(format_percent(0.856))       # 85.6%
        print(format_scientific(0.00042))  # 4.20e-04

---

**Exercise 3.**
Demonstrate the difference between `partial` and `lambda` for argument binding. Create both `partial_double = partial(mul, 2)` and `lambda_double = lambda x: mul(2, x)`. Print the `func`, `args`, and `keywords` of the partial object and show that the lambda has no such attributes. Verify both produce the same results.

??? success "Solution to Exercise 3"

        from functools import partial
        from operator import mul

        partial_double = partial(mul, 2)
        lambda_double = lambda x: mul(2, x)

        # partial exposes its internals
        print(partial_double.func)       # <built-in function mul>
        print(partial_double.args)       # (2,)
        print(partial_double.keywords)   # {}

        # lambda has no such attributes
        print(hasattr(lambda_double, 'func'))  # False

        # Both produce the same results
        print(partial_double(5))  # 10
        print(lambda_double(5))   # 10
