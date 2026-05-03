# First-Class Functions

In Python, functions are **first-class objects**. This means functions can be treated like any other value — assigned to variables, passed as arguments, returned from other functions, and stored in data structures.

!!! tip "Mental Model"
    A function in Python is just an object that happens to be callable. You can assign it to a variable, toss it into a list, or hand it to another function the same way you would an integer or a string. Once you stop thinking of functions as special and start thinking of them as values, patterns like callbacks, decorators, and higher-order functions become natural.


## Functions Are Objects

Every function in Python is an instance of the `function` type. The name `f` without parentheses refers to the function object itself; `f()` *calls* it:

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

print(type(greet))               # <class 'function'>
print(isinstance(greet, object)) # True

print(greet)          # <function greet at 0x...>
print(greet("Alice")) # Hello, Alice!
```

Like integers and strings, a function has a type, an identity (`id`), and attributes:

```python
print(greet.__name__)   # 'greet'
print(greet.__doc__)    # None (no docstring here)
```


## Assigning Functions to Variables

A function name is just a variable that references a function object. You can bind another name to the same object:

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

say_hello = greet  # No parentheses — assigns the object, not the result

print(say_hello("Alice"))  # Hello, Alice!
print(say_hello is greet)  # True — same object
```


## Passing Functions as Arguments

Functions that accept other functions as arguments are called **higher-order functions**:

```python
def apply(func, value: int) -> int:  # func is any callable
    return func(value)

def square(x: int) -> int:
    return x ** 2

result = apply(square, 5)  # 25
```

### Applying Multiple Times

```python
def apply_twice(func, value: int) -> int:  # func is any callable
    return func(func(value))

def add_ten(x: int) -> int:
    return x + 10

result = apply_twice(add_ten, 5)
print(result)  # 25 (5 + 10 + 10)
```

### Built-in Higher-Order Functions

Python's `sorted`, `map`, and `filter` all accept a function argument:

```python
numbers = [3, 1, 4, 1, 5]

def negate(x: int) -> int:
    return -x

sorted(numbers, key=negate)  # [5, 4, 3, 1, 1]

list(map(str, numbers))      # ['3', '1', '4', '1', '5']

def greater_than_two(x: int) -> bool:
    return x > 2

list(filter(greater_than_two, numbers))  # [3, 4, 5]
```

Writing a named function for every small operation gets verbose. Python provides `lambda` for short, anonymous functions — covered in its own page. For now, notice that `key=negate` is the same idea as writing `key=lambda x: -x`.


## Returning Functions

A function can create and return another function. The inner function remembers the value of `n` even after `make_multiplier` has finished — this mechanism is called a **closure**, covered in detail in a later chapter:

```python
def make_multiplier(n: int):
    def multiply(x: int) -> int:
        return x * n
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15
```


## Storing Functions in Data Structures

Functions can be stored in lists, dictionaries, or any container.

### Lists

```python
def increment(x: int) -> int:
    return x + 1

def double(x: int) -> int:
    return x * 2

def square(x: int) -> int:
    return x ** 2

operations = [increment, double, square]

for op in operations:
    print(op(5))  # 6, 10, 25
```

### Dispatch Table

A dictionary that maps names to handler functions replaces long `if/elif` chains:

```python
def handle_get(request: dict) -> str:
    return "GET response"

def handle_post(request: dict) -> str:
    return "POST response"

def handle_delete(request: dict) -> str:
    return "DELETE response"

handlers = {
    "GET": handle_get,
    "POST": handle_post,
    "DELETE": handle_delete,
}

def dispatch(method: str, request: dict) -> str:
    handler = handlers.get(method)
    if handler:
        return handler(request)
    return "Unknown method"

print(dispatch("GET", {}))    # GET response
print(dispatch("POST", {}))   # POST response
print(dispatch("PATCH", {}))  # Unknown method
```

Because functions are values, the dictionary stores the function objects directly — no special syntax required.

First-class functions also enable closures, decorators, and callable objects, each of which builds on the ideas introduced here and is covered in its own chapter.

---

## Exercises

**Exercise 1.**
Write a function `apply_operations(value, operations)` that takes a number and a list of single-argument functions. It should apply each function in order, passing the result of each to the next. For example, `apply_operations(5, [double, add_one, str])` where `double` returns `x * 2` and `add_one` returns `x + 1` should return `"11"`.

??? success "Solution to Exercise 1"

        def double(x):
            return x * 2

        def add_one(x):
            return x + 1

        def apply_operations(value, operations):
            for op in operations:
                value = op(value)
            return value

        result = apply_operations(5, [double, add_one, str])
        print(result)       # "11"
        print(type(result)) # <class 'str'>

---

**Exercise 2.**
Create a dispatch table (dictionary) that maps command strings like `"greet"`, `"farewell"`, and `"shout"` to functions. Each function should accept a `name` argument and return a formatted string. Write a `run_command(command, name)` function that looks up and calls the correct function, raising `KeyError` for unknown commands.

??? success "Solution to Exercise 2"

        def greet(name):
            return f"Hello, {name}!"

        def farewell(name):
            return f"Goodbye, {name}!"

        def shout(name):
            return f"HEY, {name.upper()}!"

        commands = {
            "greet": greet,
            "farewell": farewell,
            "shout": shout,
        }

        def run_command(command, name):
            return commands[command](name)

        print(run_command("greet", "Alice"))     # Hello, Alice!
        print(run_command("shout", "Bob"))        # HEY, BOB!

---

**Exercise 3.**
Write a function `sort_by(data, key_func)` that sorts a list of dictionaries by a key extracted with `key_func`. Demonstrate by sorting a list of `{"name": ..., "age": ...}` dictionaries first by name (alphabetically) and then by age (numerically), passing different functions each time.

??? success "Solution to Exercise 3"

        def sort_by(data, key_func):
            return sorted(data, key=key_func)

        people = [
            {"name": "Charlie", "age": 30},
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 35},
        ]

        by_name = sort_by(people, lambda p: p["name"])
        print(by_name)
        # [{'name': 'Alice', ...}, {'name': 'Bob', ...}, {'name': 'Charlie', ...}]

        by_age = sort_by(people, lambda p: p["age"])
        print(by_age)
        # [{'name': 'Alice', 'age': 25}, {'name': 'Charlie', 'age': 30}, ...]
