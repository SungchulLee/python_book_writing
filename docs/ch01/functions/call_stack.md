# Runtime Model (Call Stack)

The call stack defines how function execution is organized at runtime. Each function call creates a new frame, allowing functions to isolate execution while still composing into larger programs.

When functions call other functions, Python must remember where execution should return after each function finishes. This is handled by the **call stack**.

!!! tip "Mental Model"
    The call stack is a stack of sticky notes. Each time a function is called, Python writes down "where to return" on a new note and pushes it on top. When the function finishes, Python pops the top note and resumes at the recorded location. This is how Python keeps track of deeply nested function calls.

## Nested Function Calls

Functions can call other functions.

```python
def g():
    print("inside g")

def f():
    print("inside f")
    g()
    print("back in f")

f()
```

Output

```text
inside f
inside g
back in f
```

Execution order:

1. `f()` starts running
2. `f()` calls `g()`
3. `g()` runs and finishes
4. execution returns to `f()`
5. `f()` continues and finishes

## How the Call Stack Works

The call stack keeps track of which functions are currently running.

The program itself runs inside a **main frame** at the bottom of the call stack.

The stack follows a **last-in, first-out (LIFO)** rule:
the most recent function call is always on top of the stack.
The function at the top of the stack is the one currently running.

Program start:

```text
+--------+
|  main  |
+--------+
```

When `main` calls `f()`:

```text
+--------+
|   f    |
|  main  |
+--------+
```

When `f()` calls `g()`:

```text
+--------+
|   g    |
|   f    |
|  main  |
+--------+
```

`g()` is now running. `f()` is paused and waiting for `g()` to finish.

When `g()` returns:

```text
+--------+
|   f    |
|  main  |
+--------+
```

Execution returns to `f()`.

When `f()` returns:

```text
+--------+
|  main  |
+--------+
```

When the program ends:

```text
(empty)
```

## Stack Frames

Each function call creates a **stack frame** that stores information needed while the function runs.

A stack frame stores:

- local variables
- the current execution position
- where to return after the function completes

Each function call creates its own separate stack frame.
This means that local variables in one function are completely isolated from local variables in another, even if they share the same name.

```python
def f():
    x = 10
    g()
    print("f sees x =", x)

def g():
    x = 99
    print("g sees x =", x)

f()
```

Output

```text
g sees x = 99
f sees x = 10
```

Both `f` and `g` use a variable named `x`, but each function has its own stack frame with its own `x`.
When `g` sets `x = 99`, it does not affect the `x` inside `f`.

## Tracebacks and the Call Stack

When an error occurs, Python prints a **traceback**.

A traceback lists the sequence of calls from the program entry point to the location where the error occurred.

```python
def g():
    x = 1 / 0

def f():
    g()

f()
```

Output

```text
Traceback (most recent call last):
  File "example.py", line 7, in <module>
    f()
  File "example.py", line 5, in f
    g()
  File "example.py", line 2, in g
    x = 1 / 0
ZeroDivisionError: division by zero
```

This traceback shows the call stack at the moment of the error.

!!! tip

    Reading a traceback is essentially reading the call stack from the point where the error occurred.

## Key Ideas

Python tracks function calls using the call stack, which follows a last-in, first-out rule.
Each function call creates a stack frame that holds its own local variables, execution position, and return address.
Because each call gets its own frame, local variables are fully isolated between functions.
Tracebacks are snapshots of the call stack at the moment an error occurs — learning to read them is one of the most practical debugging skills in Python.

Understanding the call stack becomes especially important when learning **recursion**.

---

## Putting It Together

Functions provide a complete abstraction over program execution:

- parameters define inputs
- return values define outputs
- control flow defines the success path
- exceptions define the failure path
- the call stack defines how execution is organized

Functions allow programs to scale by separating concerns: each function handles a small part of execution, while the call stack composes them into larger behavior. Understanding functions means understanding how programs are structured, executed, and controlled.

---



---

## Notebook Examples

```python
def f():
    x = 10
    print(x)

f()
```

```python
x = 10

def f():
    print(x)

f()
```

```python
x = 10

def f():
    x = 7
    print(x)

f()
```

```python
x = 10

def f():
    x = 7
    def g():
        print(x)
    g()

f()
```

```python
x = 10

def f():
    x = 7
    def g():
        x = 5
        print(x)
    g()

f()
```

```python
x = 10

def f():
    #x = 7
    def g():
        #x = 5
        print(x)
    g()

f()
```

```python
#LEGB - local ---> enclosing ---> global ---> built-in

x = 10 # <--- global

def f():
    #x = 7 <--- enclosing
    def g():
        #x = 5 <--- local
        print(x)
    g()

f()
```

```python
print(__name__)
print(__file__)
```

```python
print(__doc__)
```

```python
def add(a, b):
    """Returns a + b."""
    return a + b

print(add.__doc__)  # 'Returns a + b.'
print(help(add))
```

```python
def add(a, b):
    """Returns a + b."""
    return a + b

print(add.__doc__)  # 'Returns a + b.'
help(add)
```

```python
x = 10

def f():
    print(x)

f()
```

```python
x = 10

def f():
    x = x + 1 # UnboundLocalError
    # when "x = ", python think x is a local variable
    print(x)

f()
```

```python
x = 10

def f():
    global x
    x = x + 1 # UnboundLocalError
    # when "x = ", python think x is a local variable
    print(x)

f()
print(x)
```

```python
x = 10

def f():
    def g():
        global x
        x = x + 1 # UnboundLocalError
        # when "x = ", python think x is a local variable
        print(x)
    g()

f()
print(x)
```

```python
x = 10

def f():
    x = 11
    def g():
        nonlocal x
        x = x + 1 # UnboundLocalError
        # when "x = ", python think x is a local variable
        print(x) # <--- 12
    g()
    print(x) # <--- 12

f()
print(x) # <--- 10
```

```python
x = 10

def f():
    #x = 11
    def g():
        nonlocal x
        x = x + 1 # UnboundLocalError
        # when "x = ", python think x is a local variable
        print(x) # <--- 12
    g()
    print(x) # <--- 12

f()
print(x) # <--- 10
```

```python
def f(n: int) -> int:
    """n: int >= 0"""
    # base case
    if n <= 1:
        return n

    # recursive case
    return f(n-1) + f(n-2)

for n in range(10):
    print( f(n) )
```

```python
num_fun_frames = 0

def f(n: int) -> int:
    """n: int >= 0"""
    global num_fun_frames
    num_fun_frames += 1
    #print(num_fun_frames, end="\t")

    # base case
    if n <= 1:
        return n

    # recursive case
    return f(n-1) + f(n-2)


f(100)
print(num_fun_frames)
```

```python
# memoization (top down)

memo = {0 : 0, 1 : 1}

def f(n: int) -> int:
    """n: int >= 0"""
    global memo
    if n not in memo: # n is key of dictionary
        memo[n] = f(n-1) + f(n-2)
    return memo[n]

print( f(0) ) # no memo writing
print( f(1) ) # no memo writing
print( f(2) ) # memo[2]
print( f(100) )
```

```python
# bottom up

def f(n: int) -> int:
    """n: int >= 0"""
    # base case
    if n <= 1:
        return n

    # recursive case
    a_n_minus_2 = 0
    a_n_minus_1 = 1
    for i in range(2, n+1):
        a_n = a_n_minus_1 + a_n_minus_2
        a_n_minus_2, a_n_minus_1 = a_n_minus_1, a_n
    return a_n

print( f(0) ) # no memo writing
print( f(1) ) # no memo writing
print( f(2) ) # memo[2]
print( f(3) )
print( f(4) )
print( f(5) )
print( f(6) )
```

```python
def fib(n: int) -> int:
    """Return the nth Fibonacci number, n >= 0."""
    if n < 0:
        raise ValueError("n must be >= 0")
    return _fib_pair(n)[0]

def _fib_pair(n: int) -> tuple[int, int]:
    """
    Returns (F(n), F(n+1)).
    """
    if n == 0:
        return (0, 1)

    a, b = _fib_pair(n // 2)   # a = F(k), b = F(k+1)
    c = a * (2 * b - a)        # F(2k)
    d = a * a + b * b          # F(2k+1)

    if n % 2 == 0:
        return (c, d)
    else:
        return (d, c + d)

print(fib(0))
print(fib(1))
print(fib(2))
print(fib(10))
print(fib(100))
print(fib(1000))
```

---

## Exercises

**Exercise 1.**
Each function call creates a new stack frame with its own local variables. Predict the output:

```python
def f(x):
    x = x + 1
    print(f"f: x = {x}")
    return x

x = 10
result = f(x)
print(f"main: x = {x}")
print(f"main: result = {result}")
```

Why does the `x` in `main` remain `10` even though `f` changes `x` to `11`? How does the call stack explain this?

??? success "Solution to Exercise 1"
    Output:

    ```text
    f: x = 11
    main: x = 10
    main: result = 11
    ```

    The `x` in `main` and the `x` in `f` are **different variables in different stack frames**. When `f(x)` is called, a new stack frame is created for `f` with its own local `x`, initialized to the value `10`. The line `x = x + 1` inside `f` modifies `f`'s local `x` to `11`, but this has no effect on `main`'s `x`.

    The call stack explains this: `main`'s frame has `x = 10`, and `f`'s frame has its own `x = 11`. When `f` returns, its frame is destroyed, and execution returns to `main`'s frame where `x` is still `10`. The returned value `11` is stored in `result`.

---

**Exercise 2.**
When a recursive function calls itself, each call adds a new frame to the stack. Predict what happens:

```python
def countdown(n):
    print(n)
    countdown(n - 1)

countdown(5)
```

Why does this eventually crash with `RecursionError`? What is Python's default recursion limit, and why does it exist? How would you fix this function?

??? success "Solution to Exercise 2"
    The function prints `5, 4, 3, 2, 1, 0, -1, -2, ...` and eventually crashes with:

    ```text
    RecursionError: maximum recursion depth exceeded
    ```

    Each call to `countdown(n - 1)` adds a new frame to the call stack. Since there is no base case to stop the recursion, the stack grows indefinitely. Python's default recursion limit is **1000** frames (checked via `sys.getrecursionlimit()`). This limit exists to prevent stack overflow, which would crash the entire Python process.

    Fixed version:

    ```python
    def countdown(n):
        if n < 0:    # base case
            return
        print(n)
        countdown(n - 1)
    ```

    The base case `if n < 0: return` stops the recursion, ensuring the stack eventually unwinds.

---

**Exercise 3.**
A programmer sees this traceback and must identify the bug:

```text
Traceback (most recent call last):
  File "app.py", line 15, in <module>
    result = process(data)
  File "app.py", line 10, in process
    return transform(item)
  File "app.py", line 5, in transform
    return int(value)
ValueError: invalid literal for int() with base 10: 'hello'
```

Read the traceback and answer: which function raised the error? Which function called it? What was the original call that started the chain? Why does Python print the traceback in order from outermost to innermost call?

??? success "Solution to Exercise 3"

    - **Which function raised the error?** `transform` -- the error occurred at line 5, inside `transform`, when `int(value)` was called with the string `'hello'`.
    - **Which function called it?** `process` -- line 10 in `process` called `transform(item)`.
    - **What was the original call?** Line 15 in `<module>` (the main script) called `process(data)`.

    The call chain is: `<module>` -> `process` -> `transform` -> `int()` (error).

    Python prints the traceback from **outermost to innermost** (most recent call last) because the most useful information -- where the error actually occurred -- is at the bottom. This way, you see the immediate cause first when reading from the bottom up, and can trace the full call chain by reading upward.
