# Functions

Functions are the primary mechanism for structuring programs. They abstract over execution by grouping behavior into reusable units that accept inputs, produce outputs, and isolate execution within their own local scope.

Functions abstract over both control flow and exceptions: control flow defines how execution proceeds, exceptions define how execution fails, and functions encapsulate both into reusable units.

You can think of a function as a **black box**:

- it optionally receives **inputs** (called parameters)
- it performs some operation on those inputs
- it optionally produces an **output** returned with the `return` keyword

```text
         ┌─────────────┐
inputs ──►│   function  ├──► output
         └─────────────┘
```

For now our examples use no inputs and no output.
We will add those in [Parameters](parameters.md) and [Return Values](return_values.md).

!!! tip "Mental Model"
    A function is a named, reusable block of code with its own private workspace. Defining a function does nothing by itself---it just saves the recipe. Calling the function runs the recipe, creates a fresh local scope for its variables, and optionally returns a result to the caller.

## Why Functions

Consider the following code:

```python
print("=" * 30)
print("  Welcome, Alice")
print("=" * 30)

print("=" * 30)
print("  Welcome, Alice")
print("=" * 30)

print("=" * 30)
print("  Welcome, Alice")
print("=" * 30)
```

The same three-line block is repeated several times.

Instead of repeating the same statements, we can place them inside a function and call that function whenever we need it.

```python
def greet():
    print("=" * 30)
    print("  Welcome, Alice")
    print("=" * 30)

greet()
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
==============================
  Welcome, Alice
==============================
```

## Defining a Function

In Python, functions are defined using the `def` keyword.

An important point before we look at the syntax: **defining a function does not execute it**.
Python reads the `def` block and stores the function for later use, but the body does not run until the function is called.

```python
def display_score():
    print("Score: 100")
```

This defines a function named `display_score`.

!!! warning "Defining is not executing"

    Writing `def display_score(): ...` only tells Python that a function named `display_score` exists.
    No code inside the function body runs at this point.
    The function runs only when it is **called**.

## Calling a Function

To run a function, we **call** it using parentheses.

```python
display_score()
```

Output

```text
Score: 100
```

Parentheses tell Python that the function should be executed.
Without them, `display_score` just refers to the function object.

```python
print(display_score())
print(display_score)
```

Output

```text
Score: 100
None
<function display_score at 0x7f3a1c2b4d30>
```

`display_score()` calls the function, which prints `Score: 100` and returns `None` (since there is no `return` statement).
`display_score` without parentheses prints the function object itself, showing its name and memory address.
The address shown will differ on your machine and between runs.

## Execution Flow

Statements above a `def` run first; the function body runs only at the call site.
When a function is called, execution temporarily moves into the function body and then returns to where the call occurred.

```python
def greet():
    print("Inside greet()")
    print("Hello")

print("Start program")
greet()
print("End program")
```

Output

```text
Start program
Inside greet()
Hello
End program
```

We will explore how Python tracks these jumps in [Runtime Model (Call Stack)](call_stack.md).


## Key Ideas

The `def` keyword creates a function, and parentheses after the name call it.
Remember that defining a function only registers it --- no code runs until the function is called.

Next: [Parameters](parameters.md).


## Exercises

**Exercise 1.**
When Python encounters a `def` statement, it does NOT execute the function body. Explain what `def` actually does at runtime. What object does it create, and what name does it bind? Predict the output:

```python
def broken():
    return 1 / 0

print("Function defined")
print(type(broken))
```

Why does this code NOT raise a `ZeroDivisionError`?

??? success "Solution to Exercise 1"
    `def` is an **executable statement** that creates a **function object** and binds it to the name `broken` in the current scope. The function body is compiled into bytecode and stored inside the function object, but it is NOT executed.

    Output:

    ```text
    Function defined
    <class 'function'>
    ```

    No `ZeroDivisionError` occurs because `1 / 0` is inside the function body, which only executes when the function is **called**. `def` merely registers the function -- it says "when someone calls `broken()`, execute this body." Since `broken()` is never called, the division by zero never happens.

---

**Exercise 2.**
In Python, functions are "first-class objects." This means they can be assigned to variables, passed as arguments, and stored in data structures. Predict the output:

```python
def greet():
    return "hello"

f = greet
print(f())
print(type(f))
```

What is the difference between `greet` (no parentheses) and `greet()` (with parentheses)?

??? success "Solution to Exercise 2"
    Output:

    ```text
    hello
    <class 'function'>
    ```

    `greet` (no parentheses) is a reference to the **function object** itself. It can be assigned to another variable: `f = greet` makes `f` refer to the same function object.

    `greet()` (with parentheses) **calls** the function and evaluates to its return value (`"hello"`).

    This distinction is fundamental: the function name is just a variable that happens to refer to a function object. The parentheses are the "call operator." `f()` calls the same function because `f` and `greet` refer to the same object.

---

**Exercise 3.**
A student writes:

```python
def add(a, b):
    a + b

result = add(3, 4)
print(result)
```

They expect `7` but get `None`. Explain why. What is the difference between *computing* a value and *returning* it?

??? success "Solution to Exercise 3"
    Output is `None`.

    The function computes `a + b` (which evaluates to `7`) but does not **return** it. Without a `return` statement, the function implicitly returns `None`. The computed value `7` is discarded.

    Computing a value (evaluating an expression) and returning it (sending it back to the caller) are separate actions. `a + b` computes `7` but the result exists only temporarily. `return a + b` both computes `7` AND sends it back to the caller as the function's result.

    The fix: `return a + b`.
