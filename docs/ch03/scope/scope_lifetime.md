# Scope Lifetime

!!! tip "Mental Model"
    A scope is born when its containing block starts executing and dies when it ends. A function's local scope is created on each call and destroyed on return -- unless a closure captures it, keeping the variables alive as long as the closure exists. Global scope lives for the entire program; built-in scope is eternal.

## Local Scope

### 1. Function Call

```python
def function():
    x = 10  # Created at call
    return x
    # Destroyed after return

result = function()
# x no longer exists
```

### 2. Frame Lifetime

```python
def outer():
    x = 10
    
    def inner():
        return x
    
    return inner
    # Frame ends but x kept for closure

f = outer()
print(f())  # x still accessible
```

## Global Scope

### 1. Module Lifetime

```python
# Exists for program lifetime
x = 10

def function():
    print(x)

# x available throughout
```

## Summary

- Local: function call duration
- Enclosing: kept if captured
- Global: program lifetime
- Built-in: always available


---

## Exercises


**Exercise 1.**
Write a function that creates a local variable. After the function returns, attempt to access that variable and show that it no longer exists.

??? success "Solution to Exercise 1"

    ```python
    def create_local():
        secret = 42
        print(f"Inside function: {secret}")
        return secret

    result = create_local()
    # print(secret)  # NameError: name 'secret' is not defined
    print(f"Returned value: {result}")
    ```

    Local variables are created when the function is called and destroyed when it returns. The name `secret` does not exist outside the function.

---

**Exercise 2.**
Demonstrate that a closure keeps enclosing variables alive even after the outer function returns. Create an outer function that returns an inner function, and show the inner function can still use the outer variable.

??? success "Solution to Exercise 2"

    ```python
    def outer():
        message = "I survive!"

        def inner():
            return message

        return inner

    closure = outer()
    # outer() has returned, but message is kept alive
    print(closure())  # I survive!
    ```

    The inner function holds a reference to `message` through a closure. Python keeps the enclosing variable alive as long as the closure exists.

---

**Exercise 3.**
Create a global variable, modify it inside a function using the `global` keyword, and show that the change persists after the function call. Then explain the lifetime difference between global and local variables.

??? success "Solution to Exercise 3"

    ```python
    count = 0

    def increment():
        global count
        count += 1

    increment()
    increment()
    print(count)  # 2
    ```

    Global variables live for the entire duration of the program. Local variables are created when a function is called and destroyed when it returns. Closures extend the lifetime of enclosing variables beyond the outer function's return.
