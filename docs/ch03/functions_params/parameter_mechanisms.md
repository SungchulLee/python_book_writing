# Parameter Mechanisms

All four of these calls produce the same output, but each uses a different passing mechanism:

```python
def describe(name: str, age: int) -> None:
    print(name, age)

describe("Alice", 25)                          # positional
describe(age=25, name="Alice")                  # keyword
describe(*("Alice", 25))                        # unpacking tuple
describe(**{"age": 25, "name": "Alice"})        # unpacking dict
```

This page covers every mechanism Python offers for getting arguments into a function.

!!! tip "Mental Model"
    A function signature is a contract with five zones, always in this order: positional-only (before `/`), positional-or-keyword, `*args`, keyword-only (after `*`), and `**kwargs`. The caller side mirrors this: bare values fill positional slots left to right, `name=value` fills by name, `*iterable` unpacks into positional, and `**dict` unpacks into keyword arguments.

## Parameter Categories

Python has five categories of parameters:

1. **Positional-or-keyword** - Can be passed either way
2. **Positional-only** - Must be passed by position (before `/`)
3. **Keyword-only** - Must be passed by name (after `*`)
4. **`*args`** - Captures extra positional arguments
5. **`**kwargs`** - Captures extra keyword arguments


## Basic Positional and Keyword Arguments

By default, parameters can be passed positionally or by keyword.

```python
def greet(name: str, greeting: str) -> str:
    return f"{greeting}, {name}!"

# All equivalent
greet("Alice", "Hello")                   # Positional
greet(name="Alice", greeting="Hello")     # Keyword
greet("Alice", greeting="Hello")          # Mixed
```

A positional argument followed by a keyword argument is fine, but the reverse is a `SyntaxError`:

```python
greet("Alice", greeting="Hello")          # OK
greet(name="Alice", "Hello")              # SyntaxError
```


## Default Values

Parameters can have default values, making them optional.

```python
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

greet("Alice")           # "Hello, Alice!"
greet("Alice", "Hi")     # "Hi, Alice!"
```

**Rule**: Parameters with defaults must come after parameters without defaults.

```python
# Valid
def func(a: int, b: int, c: int = 10, d: int = 20) -> None:
    pass

# Invalid - SyntaxError
def func(a: int, b: int = 10, c: int) -> None:  # Non-default after default
    pass
```


## *args: Variable Positional Arguments

`*args` captures any extra positional arguments as a tuple.

```python
def sum_all(*numbers: int) -> int:
    return sum(numbers)

sum_all(1, 2)            # 3
sum_all(1, 2, 3, 4, 5)  # 15
sum_all()                # 0
```

Inside the function, `args` is an ordinary tuple:

```python
def show_args(*args: int) -> None:
    print(type(args))   # <class 'tuple'>
    print(args)

show_args(1, 2, 3)  # (1, 2, 3)
```


## **kwargs: Variable Keyword Arguments

`**kwargs` captures any extra keyword arguments as a dictionary.

```python
def print_info(**kwargs: str) -> None:
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age="30", city="NYC")
```

Output:
```
name: Alice
age: 30
city: NYC
```


## Combining *args and **kwargs

A function can accept any combination of positional and keyword arguments with `*args` and `**kwargs` together. This is useful when forwarding arguments to another function:

```python
def log_and_call(func, *args, **kwargs):
    print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
    return func(*args, **kwargs)

def add(a: int, b: int) -> int:
    return a + b

log_and_call(add, 1, 2)       # Calling add with args=(1, 2), kwargs={}
log_and_call(add, a=1, b=2)   # Calling add with args=(), kwargs={'a': 1, 'b': 2}
```


## Unpacking Arguments

Use `*` and `**` when calling functions to unpack iterables and dictionaries.

```python
def add(a: int, b: int, c: int) -> int:
    return a + b + c

# Unpack list/tuple
numbers = [1, 2, 3]
add(*numbers)  # 6

# Unpack dictionary
params = {"a": 1, "b": 2, "c": 3}
add(**params)  # 6

# Combined
add(*[1, 2], **{"c": 3})  # 6
```


## Positional-Only Parameters (/)

Parameters before `/` must be passed positionally. Positional-only parameters are rare in everyday code but appear in many built-in functions like `len()`. This syntax requires Python 3.8 or later.

```python
def divide(x: float, y: float, /) -> float:
    return x / y

divide(10, 2)      # OK: 5.0
divide(x=10, y=2)  # TypeError: positional-only argument
```

```python
# Built-in example: len() is positional-only
len([1, 2, 3])     # OK
len(obj=[1, 2, 3]) # TypeError
```


## Keyword-Only Parameters (*)

Parameters after `*` must be passed by keyword. This forces callers to be explicit, which prevents confusing positional calls.

```python
def connect(host: str, port: int, *, timeout: int = 30, retries: int = 3) -> None:
    print(f"Connecting to {host}:{port}")
    print(f"timeout={timeout}, retries={retries}")

connect("localhost", 8080)                    # OK
connect("localhost", 8080, timeout=60)        # OK
connect("localhost", 8080, 60)                # TypeError
```

Without keyword-only parameters, boolean flags become unreadable:

```python
# What does True mean? What does False mean?
process_file("data.txt", True, False)

# Keyword-only makes the intent clear
def process_file(path: str, *, verbose: bool = False, overwrite: bool = False) -> None:
    pass

process_file("data.txt", verbose=True, overwrite=False)
```


## Combined Syntax

You can combine `/` and `*` in the same function now that both separators are understood:

```python
def func(pos_only: int, /, standard: int, *, kw_only: int) -> None:
    print(f"{pos_only}, {standard}, {kw_only}")

func(1, 2, kw_only=3)           # OK
func(1, standard=2, kw_only=3)  # OK
func(pos_only=1, standard=2, kw_only=3)  # TypeError
func(1, 2, 3)                   # TypeError
```


## Real-World Examples

### print() signature

```python
# Simplified signature of print()
def print(*values, sep=' ', end='\n', file=None):
    pass

print(1, 2, 3)              # 1 2 3
print(1, 2, 3, sep='-')     # 1-2-3
print(1, 2, 3, end='!\n')   # 1 2 3!
```

### sorted() signature

```python
# sorted(iterable, /, *, key=None, reverse=False)
sorted([3, 1, 2])                    # [1, 2, 3]
sorted([3, 1, 2], reverse=True)      # [3, 2, 1]
sorted(["banana", "Apple"], key=str.lower)  # ['Apple', 'banana']
```

The `key` function transforms each element for comparison only — the original values appear in the output. Here `str.lower` makes the sort case-insensitive, but `'Apple'` keeps its capital A in the result.


## Quick Reference

| Syntax | Meaning |
|--------|---------|
| `def f(a, b)` | Standard parameters |
| `def f(a, b=10)` | Default value |
| `def f(a, /)` | Positional-only (before `/`) |
| `def f(*, a)` | Keyword-only (after `*`) |
| `def f(*args)` | Variable positional (tuple) |
| `def f(**kwargs)` | Variable keyword (dict) |
| `def f(a, /, b, *args, c, **kwargs)` | Full parameter order |
| `f(*list)` | Unpack iterable at call site |
| `f(**dict)` | Unpack dictionary at call site |

---

## Exercises


**Exercise 1.**
Write a function that accepts positional-only parameters, keyword-only parameters, and a mix of both. Use the `/` and `*` separators. Demonstrate valid and invalid ways to call it.

??? success "Solution to Exercise 1"

        ```python
        def example(a, b, /, c, *, d, e=10):
            print(f"a={a}, b={b}, c={c}, d={d}, e={e}")

        example(1, 2, 3, d=4)         # Valid
        example(1, 2, c=3, d=4, e=5)  # Valid

        # example(a=1, b=2, c=3, d=4)  # TypeError: positional-only
        # example(1, 2, 3, 4)           # TypeError: d is keyword-only
        ```

    `a` and `b` are positional-only (before `/`). `d` and `e` are keyword-only (after `*`). `c` can be either.

---

**Exercise 2.**
Write a function `tag(name, /, *children, **attrs)` that builds an HTML-like tag string. For example, `tag("div", "hello", "world", id="main")` should return `'<div id="main">helloworld</div>'`.

??? success "Solution to Exercise 2"

        ```python
        def tag(name, /, *children, **attrs):
            attr_str = " ".join(f'{k}="{v}"' for k, v in attrs.items())
            opening = f"<{name} {attr_str}>" if attrs else f"<{name}>"
            content = "".join(str(c) for c in children)
            return f"{opening}{content}</{name}>"

        print(tag("div", "hello", "world", id="main"))
        # <div id="main">helloworld</div>

        print(tag("br"))
        # <br></br>
        ```

    `name` is positional-only, `*children` collects content, and `**attrs` collects HTML attributes.

---

**Exercise 3.**
Explain the difference between `*args` and `**kwargs`. Write a function `debug_call(func, *args, **kwargs)` that prints the function name, positional arguments, and keyword arguments, then calls the function.

??? success "Solution to Exercise 3"

        ```python
        def debug_call(func, *args, **kwargs):
            print(f"Calling: {func.__name__}")
            print(f"  args: {args}")
            print(f"  kwargs: {kwargs}")
            return func(*args, **kwargs)

        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}!"

        result = debug_call(greet, "Alice", greeting="Hi")
        print(f"  result: {result}")
        ```

    `*args` captures extra positional arguments as a tuple. `**kwargs` captures extra keyword arguments as a dictionary.
