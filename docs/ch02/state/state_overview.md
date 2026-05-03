# State and Program Execution

## What is State?

At any point during a program's execution, there exists a collection of names and the objects they refer to. This collection is the program's **state**.

State is not a single variable or a single value. It is the complete snapshot of all name-to-object bindings that exist at a given moment. When you read a line of code and ask "what would `x` be right now?"---you are reasoning about state.

!!! tip "Mental Model"
    A program's state is the complete set of name-to-object bindings at a given moment. Every assignment changes the state by creating or updating a binding, and every expression reads from the state as it exists right now. Tracing how state evolves line by line is the most reliable way to predict what code will do.

---

## State as Snapshot

Consider the following program:

```python
x = 10
y = x + 5
x = 20
```

The state changes at each line:

| After line | State |
|-----------|-------|
| `x = 10` | `x` -> `10` |
| `y = x + 5` | `x` -> `10`, `y` -> `15` |
| `x = 20` | `x` -> `20`, `y` -> `15` |

Notice that reassigning `x` does not affect `y`. The value of `y` was computed from the object that `x` referred to *at the time of the assignment*, not from the name `x` itself. There is no ongoing link between `y` and `x`.

This is a direct consequence of the name-binding model: `y = x + 5` evaluates `x + 5` to produce the object `15`, then binds `y` to that object. Once bound, `y` has no memory of how it was computed.

---

## Assignments Change State

Every assignment statement changes the program's state by creating or updating a name binding.

```python
count = 0          # state: {count: 0}
count = count + 1  # state: {count: 1}
count = count + 1  # state: {count: 2}
```

The right-hand side is evaluated first using the *current* state. Then the result is bound to the left-hand name, producing a *new* state. Program execution is, at its core, a sequence of state transitions driven by assignments and expressions.

This perspective clarifies what a program does: it transforms state step by step until it reaches a result.

---

## Function Calls Create Local State

When a function is called, Python creates a **new namespace** for that call. The function's parameters and local variables live in this namespace, separate from the caller's state.

```python
def double(n):
    result = n * 2
    return result

x = 5
y = double(x)
```

During the call `double(x)`, the following local state exists inside the function:

| Name | Object |
|------|--------|
| `n` | `5` |
| `result` | `10` |

This local state is created when the function is called and destroyed when it returns. The caller's state (`x`, `y`) and the function's state (`n`, `result`) are separate namespaces.

The returned value `10` flows back to the caller and is bound to `y`, updating the caller's state. This is the primary mechanism by which data moves between functions: arguments flow in through parameter binding, and results flow out through return values.

---

## Advanced Note: Scope Affects Evaluation

In Python, assignment has an important interaction with **variable scope** that can be surprising at first.

Consider:

```python
n = 10

def f():
    n = n + 1
    return n
```

This results in an error:

```
UnboundLocalError: local variable 'n' referenced before assignment
```

Why?

Before the function runs, Python determines that `n` is a **local variable** because it appears on the left-hand side of an assignment (`n = ...`) inside the function.

This decision is made **before execution**, not dynamically at runtime.

As a result, when evaluating the right-hand side:

```python
n + 1
```

Python looks for the **local** `n`, not the global one. But since the local `n` has not been assigned a value yet, evaluation fails.

A useful mental model is:

> **scope → evaluate RHS → bind to LHS**

- First, Python determines where each name lives (local/global/nonlocal)
- Then it evaluates the right-hand side using that scope
- Finally, it binds the result to the left-hand name

---

## The Big Picture

Understanding state gives you a mental framework for reasoning about any program:

1. **Read the code line by line.** At each assignment, update the state snapshot.
2. **Evaluate expressions using the current state.** Names resolve to whatever objects they are currently bound to.
3. **Function calls create temporary local states.** These are isolated from the caller but connected through arguments and return values.

This model---state as a sequence of snapshots, transformed by assignments and function calls---is the foundation for everything else in this chapter.

---

## Exercises

**Exercise 1.**
Trace the state after each line. What are the values of `a`, `b`, and `c` at the end?

```python
a = 5
b = a
a = a + 3
c = a + b
```

Does changing `a` on line 3 affect `b`? Why or why not?

??? success "Solution to Exercise 1"
    | After line | State |
    |---|---|
    | `a = 5` | `a` -> `5` |
    | `b = a` | `a` -> `5`, `b` -> `5` |
    | `a = a + 3` | `a` -> `8`, `b` -> `5` |
    | `c = a + b` | `a` -> `8`, `b` -> `5`, `c` -> `13` |

    Changing `a` on line 3 does NOT affect `b`. When `b = a` executed, `b` was bound to the object `5`. Rebinding `a` to `8` only changes what `a` refers to --- `b` still refers to the original `5`. There is no ongoing link between `b` and `a`.

---

**Exercise 2.**
Predict whether this function modifies the caller's state:

```python
def increment(n):
    n = n + 1
    return n

x = 10
y = increment(x)
print(x)
print(y)
```

??? success "Solution to Exercise 2"
    Output:

    ```text
    10
    11
    ```

    `x` is unchanged. Inside `increment`, the parameter `n` is a local name initially bound to the same object as `x` (the integer `10`). The line `n = n + 1` rebinds the local `n` to a new object `11`. Since integers are immutable, there is no way to modify the original object. The caller's `x` still refers to `10`. The new value `11` flows back to the caller only through the return value, which is bound to `y`.

---

**Exercise 3.**
Explain why this code raises `UnboundLocalError`:

```python
count = 0

def increment():
    count = count + 1
    return count

increment()
```

How would you fix it? Give two different solutions.

??? success "Solution to Exercise 3"
    Python sees `count = ...` inside the function and marks `count` as a **local variable** at compile time. When the function executes, it tries to evaluate `count + 1` using the local `count`, which has not been assigned yet. This raises `UnboundLocalError`.

    **Fix 1 --- use `global`** (generally discouraged):

    ```python
    count = 0

    def increment():
        global count
        count = count + 1
        return count
    ```

    **Fix 2 --- pass and return** (preferred):

    ```python
    count = 0

    def increment(n):
        return n + 1

    count = increment(count)
    ```

    Fix 2 is preferred because it avoids modifying global state. The function takes a value in and returns a new value out, making data flow explicit.
