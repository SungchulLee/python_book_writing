# and/or Return Values

The and and or operators don't return boolean values—they return one of their operands. This behavior is powerful for default value patterns and conditional value selection, but differs from other languages' boolean operators.

!!! tip "Mental Model"
    `and` walks left to right looking for the first falsy value and returns it; if everything is truthy, it returns the last value. `or` does the opposite -- it returns the first truthy value, or the last value if all are falsy. Neither operator ever converts its result to `True`/`False`; they always return an original operand.

---

## and Return Values

### Returns First Falsy or Last Value

```python
print(5 and 10)
print(0 and 10)
print(False and 20)
```

Output:
```
10
0
False
```

### Understanding the Pattern

```python
# Returns first falsy operand
print([] and "value")
print("" and "value")

# Returns last operand if all truthy
print("a" and "b" and "c")
```

Output:
```
[]

c
```

## or Return Values

### Returns First Truthy or Last Value

```python
print(5 or 10)
print(0 or 10)
print(False or None or "default")
```

Output:
```
5
10
default
```

### Default Value Pattern

```python
config = {"port": None}
port = config["port"] or 8000
print(f"Port: {port}")

config["port"] = 5000
port = config["port"] or 8000
print(f"Port: {port}")
```

Output:
```
Port: 8000
Port: 5000
```

## Practical Applications

### Chained Defaults

```python
user_preference = None
system_setting = None
fallback = "light"

theme = user_preference or system_setting or fallback
print(f"Theme: {theme}")
```

Output:
```
Theme: light
```

### Value Selection

```python
scores = [85, 92, 78, 88]
passing_scores = [s for s in scores if s >= 80]

best = passing_scores and max(passing_scores) or 0
print(f"Best passing score: {best}")
```

Output:
```
Best passing score: 92
```

### Configuration Resolution

```python
def get_config(env_var, config_dict, default):
    return env_var or config_dict.get("setting") or default

result1 = get_config(None, {}, "fallback")
result2 = get_config("custom", {}, "fallback")

print(f"Result 1: {result1}")
print(f"Result 2: {result2}")
```

Output:
```
Result 1: fallback
Result 2: custom
```

## Edge Cases

### Empty Collections Are Falsy

```python
items = []
result = items or ["default"]
print(result)

items = [1, 2, 3]
result = items or ["default"]
print(result)
```

Output:
```
['default']
[1, 2, 3]
```

---

## Exercises


**Exercise 1.**
Without running the code, predict the value of each expression. Then verify.

```python
a = 0 or "" or [] or "hello" or 42
b = 1 and "yes" and [] and "no"
c = None or 0 or False or "found"
```

??? success "Solution to Exercise 1"

        ```python
        a = 0 or "" or [] or "hello" or 42
        print(a)  # "hello"

        b = 1 and "yes" and [] and "no"
        print(b)  # []

        c = None or 0 or False or "found"
        print(c)  # "found"
        ```

    `or` returns the first truthy operand (or the last if all are falsy). `and` returns the first falsy operand (or the last if all are truthy). In `b`, the empty list `[]` is falsy, so `and` stops and returns it.

---

**Exercise 2.**
Write a function `first_truthy(*args)` that returns the first truthy value from its arguments, or `None` if all are falsy. Use `or` chaining or a loop with short-circuit logic.

??? success "Solution to Exercise 2"

        ```python
        def first_truthy(*args):
            for arg in args:
                if arg:
                    return arg
            return None

        print(first_truthy(0, "", [], "hello", 42))  # "hello"
        print(first_truthy(0, "", [], None))          # None
        ```

    The loop returns the first truthy value immediately. If none are found, `None` is returned. This is equivalent to chaining `or` but works with any number of arguments.

---

**Exercise 3.**
Explain why `x = a or b` is not the same as `x = a if a else b` in all cases. Provide a concrete example where they produce different results, or explain why they are always equivalent.

??? success "Solution to Exercise 3"

    They are always equivalent for the purpose of choosing between `a` and `b`. Both expressions evaluate `a` for truthiness: if truthy, `a` is the result; otherwise `b` is the result.

        ```python
        a = 0
        b = 42

        x1 = a or b
        x2 = a if a else b

        print(x1)  # 42
        print(x2)  # 42
        print(x1 == x2)  # True
        ```

    The expressions `a or b` and `a if a else b` always produce the same result because `or` returns the first truthy value or the last value, which is exactly the behavior of the conditional expression.
