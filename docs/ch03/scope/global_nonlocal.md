
# Global and Nonlocal

By default, assignment inside a function creates a local variable. The `global` and `nonlocal` keywords let a function explicitly modify a variable defined in an outer scope---`global` targets the module-level scope, while `nonlocal` targets the nearest enclosing function scope.

!!! tip "Mental Model"
    Python's default rule is simple: any assignment inside a function creates a local variable. `global` and `nonlocal` are explicit overrides that say "do not create a local -- rebind the name in a specific outer scope instead." `global` always means the module-level scope; `nonlocal` means the nearest enclosing function scope.

## global Keyword

### Modifying a Global Variable

```python
x = 10

def function():
    global x
    x = 20

function()
print(x)  # 20
```

## nonlocal Keyword

### Modifying an Enclosing Variable

```python
def outer():
    x = 10

    def inner():
        nonlocal x
        x = 20

    inner()
    print(x)  # 20
```

## Summary

- `global`: modifies a variable at module level
- `nonlocal`: modifies a variable in the enclosing function scope
- Both allow a function to modify variables defined in an outer scope


---

## Exercises


**Exercise 1.**
Write a function `increment_counter()` that modifies a global variable `counter` each time it is called. Call it three times and print the final value.

??? success "Solution to Exercise 1"

    ```python
    counter = 0

    def increment_counter():
        global counter
        counter += 1

    increment_counter()
    increment_counter()
    increment_counter()
    print(counter)  # 3
    ```

    Without `global`, the assignment `counter += 1` would create a local variable, causing an `UnboundLocalError`.

---

**Exercise 2.**
Write a function `make_accumulator(start)` that returns an inner function. Each call to the inner function should add a given amount to the running total (using `nonlocal`) and return the new total.

??? success "Solution to Exercise 2"

    ```python
    def make_accumulator(start):
        total = start

        def add(amount):
            nonlocal total
            total += amount
            return total

        return add

    acc = make_accumulator(100)
    print(acc(10))   # 110
    print(acc(20))   # 130
    print(acc(5))    # 135
    ```

    `nonlocal total` allows the inner function to modify `total` in the enclosing scope. Each call updates the same variable.

---

**Exercise 3.**
Explain what happens if you try to use `nonlocal` to reference a global variable. Write code that demonstrates the resulting error.

??? success "Solution to Exercise 3"

    ```python
    x = 10

    def func():
        try:
            # nonlocal x  # Uncommenting causes: SyntaxError
            pass
        except:
            pass

    # nonlocal can only refer to variables in an enclosing function scope,
    # not the global (module-level) scope.
    # To modify a global variable, use 'global' instead.
    ```

    `nonlocal` targets the nearest enclosing function scope. It cannot be used at the module level. For module-level variables, use `global` instead.
