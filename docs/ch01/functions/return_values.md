
# Return Values

Return values define how results leave a function, completing the function's interface. The `return` statement not only produces a value but also immediately terminates the function's execution---making it a form of control flow as well as output.

!!! tip "Mental Model"
    `return` does two things at once: it sends a value back to the caller and immediately exits the function. If a function has no `return` statement, it implicitly returns `None`. This means every function call in Python is an expression that produces a value---you just need to decide whether to capture it.

## The Problem

In Python, every function returns a value.
If no `return` statement is present, Python automatically returns `None`.

Consider this function:

```python
def add(a, b):
    print(a + b)

result = add(3, 4)

print("Result:", result)
```

Output

```text
7
Result: None
```

The function printed the value `7`, but it did not return anything.
Because there is no `return` statement, `result` receives `None`.

## The Solution

The `return` statement sends a value back to the caller.

```python
def add(a, b):
    return a + b

result = add(3, 4)

print("Result:", result)
```

Output

```text
Result: 7
```

Now `result` holds the value `7` and can be used later in the program.

## Printing vs Returning

`print` displays a value on the screen.
`return` sends a value back to the caller.

The key difference is that a returned value can be **reused** — stored in a variable, passed to another function, or used in an expression.

```python
def add(a, b):
    return a + b

print(add(2, 5) * 2)
```

Output

```text
14
```

Because `add(2, 5)` returns `7`, the expression `add(2, 5) * 2` evaluates to `14`.
If `add` had used `print` instead of `return`, this would not be possible.

## Key Ideas

The `return` statement lets a function produce a value that the caller can store, print, or use in further computation.
Without `return`, a function always returns `None`.
The distinction between printing and returning is one of the most important concepts for beginners to internalize — `print` is for humans to read, `return` is for the program to use.

---

## Exercises

**Exercise 1.**
A beginner writes a function that prints instead of returning:

```python
def add(a, b):
    print(a + b)

result = add(3, 4)
total = result * 2
```

What happens when this code runs? What is the value of `result`? Why does the last line fail? Explain the fundamental difference between `print` and `return`.

??? success "Solution to Exercise 1"
    Running the code:

    1. `add(3, 4)` prints `7` to the screen and returns `None` (no `return` statement).
    2. `result` is assigned `None`.
    3. `result * 2` is `None * 2`, which raises `TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'`.

    The fundamental difference: `print` sends text to the screen for humans to read. `return` sends a value back to the calling code for the program to use. `print` does not create a value that can be stored or computed with. `return` does.

    The fix: `return a + b` instead of `print(a + b)`.

---

**Exercise 2.**
A function can return multiple values using a tuple. Predict the output:

```python
def divide(a, b):
    return a // b, a % b

result = divide(17, 5)
print(result)
print(type(result))

q, r = divide(17, 5)
print(q, r)
```

What type does `divide` actually return? Why does `q, r = divide(17, 5)` work? What Python feature makes this possible?

??? success "Solution to Exercise 2"
    Output:

    ```text
    (3, 2)
    <class 'tuple'>
    3 2
    ```

    `divide` actually returns a **single tuple** `(3, 2)`. The syntax `return a // b, a % b` is equivalent to `return (a // b, a % b)` -- the comma creates a tuple.

    `q, r = divide(17, 5)` works because of **tuple unpacking**: the tuple `(3, 2)` is unpacked into `q = 3` and `r = 2`. This is the same unpacking mechanism as `a, b = 1, 2`.

    Python does not truly have "multiple return values" -- it returns a single tuple, and the caller unpacks it. This is a common idiom that looks like multiple returns.

---

**Exercise 3.**
Explain what happens when `return` is reached inside a loop:

```python
def find_first_even(numbers):
    for n in numbers:
        if n % 2 == 0:
            return n
    return None

print(find_first_even([1, 3, 4, 6, 8]))
print(find_first_even([1, 3, 5]))
```

Predict both outputs. Why does `return` exit the entire function (not just the loop)? What would happen if the second `return None` were omitted?

??? success "Solution to Exercise 3"
    Output:

    ```text
    4
    None
    ```

    `find_first_even([1, 3, 4, 6, 8])` returns `4` -- the first even number. When `return n` executes, it exits the **entire function** immediately, including the loop. The remaining elements `6` and `8` are never examined.

    `find_first_even([1, 3, 5])` returns `None` -- no even numbers were found, so the loop completes without hitting `return n`, and execution falls through to `return None`.

    `return` always exits the entire function because a function can have only one return point per execution path. This is different from `break` (which exits only the loop) and `continue` (which skips to the next iteration).

    If the second `return None` were omitted, the function would still return `None` implicitly -- Python automatically returns `None` when a function ends without an explicit `return`. However, the explicit `return None` makes the intent clear: "returning None is a deliberate design choice, not a mistake."

Next: [Type Hints](type_hints.md).
