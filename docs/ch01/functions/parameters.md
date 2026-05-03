
# Parameters

Parameters define the boundary between a function and its environment, controlling how external data enters local execution. They specify how values are bound to names within a function's local scope.

Functions become much more useful when they can accept **inputs**.
Inputs allow the same function to work with different values each time it is called.

!!! tip "Mental Model"
    Parameters are the input slots of a function. When you define `def greet(name)`, you are declaring that `greet` expects one piece of data to work with. When you call `greet("Alice")`, the argument `"Alice"` is bound to the local name `name` inside the function's scope. Parameters make functions general; arguments make them specific.

## The Problem

Consider this function from the previous page:

```python
def greet():
    print("=" * 30)
    print("  Welcome, Alice")
    print("=" * 30)

greet()
greet()
```

Output

```text
==============================
  Welcome, Alice
==============================
==============================
  Welcome, Alice
==============================
```

This function always welcomes **Alice**.
What if we want to welcome different people?

## The Solution

We can add a **parameter** so the function accepts a value.

```python
def greet(name):
    print("=" * 30)
    print("  Welcome,", name)
    print("=" * 30)

greet("Alice")
greet("Bob")
```

Output

```text
==============================
  Welcome, Alice
==============================
==============================
  Welcome, Bob
==============================
```

The function now accepts a value that can change each time it is called.
When we call `greet("Alice")`, Python assigns `"Alice"` to the parameter `name` inside the function body.

```text
greet("Alice")
       │
       └──► name = "Alice"
```

## Parameters and Arguments

A **parameter** is a variable listed in the function definition.

An **argument** is the value supplied when the function is called.

```python
def greet(name):
    print("Welcome,", name)

greet("Alice")
```

Here:

- `name` is the **parameter**
- `"Alice"` is the **argument**

## Multiple Parameters

Functions can accept more than one parameter.

```python
def describe(name, age):
    print(name, "is", age, "years old")

describe("Alice", 25)
describe("Bob", 30)
```

Output

```text
Alice is 25 years old
Bob is 30 years old
```

Each parameter receives its own value when the function is called.
The order of the arguments must match the order of the parameters.

## Default Parameters

Parameters can have **default values**.

```python
def greet(name="guest"):
    print("Welcome,", name)

greet()
greet("Alice")
```

Output

```text
Welcome, guest
Welcome, Alice
```

When no argument is provided, the parameter uses its default value.
When an argument is provided, it overrides the default.


## Key Ideas

Parameters let a function accept different inputs each time it is called.
The parameter name appears in the `def` line; the argument value appears in the call.
When a function has multiple parameters, arguments are matched to parameters by position.

Next: [Return Values](return_values.md).


## Exercises

**Exercise 1.**
A dangerous pitfall in Python is using a mutable default argument:

```python
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item("a"))
print(add_item("b"))
print(add_item("c"))
```

Predict the output. Why does the list accumulate across calls? What is Python doing with the default value, and when is it created? What is the standard fix?

??? success "Solution to Exercise 1"
    Output:

    ```text
    ['a']
    ['a', 'b']
    ['a', 'b', 'c']
    ```

    The default value `[]` is created **once** when the `def` statement executes (at function definition time), not each time the function is called. All calls that use the default share the **same list object**. Each `append` modifies this shared object, so the list accumulates items across calls.

    The standard fix uses `None` as a sentinel:

    ```python
    def add_item(item, items=None):
        if items is None:
            items = []  # New list created on each call
        items.append(item)
        return items
    ```

    Now a fresh list is created on every call that does not provide an explicit argument.

---

**Exercise 2.**
Python passes arguments by "assignment" -- the parameter name is bound to the same object as the argument. Predict the output:

```python
def modify(x, lst):
    x = x + 1
    lst.append(4)

a = 10
b = [1, 2, 3]
modify(a, b)
print(a)
print(b)
```

Why does `a` remain unchanged but `b` is modified? What is the difference between rebinding a name and mutating an object?

??? success "Solution to Exercise 2"
    Output:

    ```text
    10
    [1, 2, 3, 4]
    ```

    Inside `modify`, `x` is a local name bound to the same `int` object as `a` (value `10`). `x = x + 1` creates a **new** `int` object `11` and rebinds the local name `x` to it. The caller's `a` still refers to the original `10`. This is **rebinding** -- changing which object a name refers to.

    `lst` is a local name bound to the same `list` object as `b`. `lst.append(4)` **mutates** that list object in place. Since `b` still refers to the same object, the change is visible. This is **mutation** -- modifying the object itself.

    The critical distinction: rebinding a local name (`x = ...`) never affects the caller. Mutating a shared object (`lst.append(...)`) is visible to everyone holding a reference to that object.

---

**Exercise 3.**
Explain the difference between a **parameter** and an **argument**. In the following code, identify which are parameters and which are arguments:

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice", greeting="Hi")
```

??? success "Solution to Exercise 3"
    **Parameters** are the names declared in the function definition. They are placeholders that receive values when the function is called. In this example, `name` and `greeting` are parameters.

    **Arguments** are the actual values passed when the function is called. In `greet("Alice", greeting="Hi")`, `"Alice"` and `"Hi"` are arguments. `"Alice"` is a **positional argument** (matched to `name` by position). `greeting="Hi"` is a **keyword argument** (matched to `greeting` by name).

    `"Hello"` in the definition is the **default value** for the parameter `greeting` -- it is used when no argument is provided for that parameter.
