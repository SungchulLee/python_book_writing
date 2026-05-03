# Compile vs Runtime Errors

Programming errors fall into three main categories based on when they occur: compile-time errors (caught before execution), runtime errors (caught during execution), and logical errors (never caught by Python).

!!! tip "Mental Model"
    Python catches errors at two stages. Syntax errors are caught when the source code is parsed into bytecode -- before any line runs. Runtime errors (like `NameError` or `TypeError`) only surface when the faulty line actually executes. Logical errors are the sneakiest: the code runs without complaint but produces wrong results.

## Compile-Time Errors

Compile errors occur during the compilation or parsing phase before the program runs. In Python, these are primarily **syntax errors**.

```python
# SyntaxError: Missing colon
if True
    print("Hello")

# SyntaxError: Invalid syntax
x = 5 +

# SyntaxError: Unmatched parenthesis
print("Hello"
```

Python catches these errors when it parses the code, before any execution begins.


## Syntax Error Examples

```python
# Missing colon after if
if x > 5
    print(x)

# IndentationError (a type of SyntaxError)
def foo():
print("Hello")

# Invalid assignment
5 = x

# Unclosed string
message = "Hello
```


## Compile Errors Prevent Execution

With a syntax error, no code runs at all.

```python
print("This never prints")

if True  # SyntaxError here
    print("Hello")

print("This also never prints")
```

None of the `print` statements execute because Python fails to parse the file.


## Compile Errors Cannot Be Caught

Syntax errors cannot be caught with `try/except` in the same file.

```python
# This doesn't work
try:
    if True  # SyntaxError
        pass
except SyntaxError:
    print("Caught")  # Never reached
```

The entire file fails to parse, so `try/except` never executes.


## Runtime Errors

Runtime errors occur during program execution when the code encounters a situation it cannot handle.

```python
# ZeroDivisionError
result = 10 / 0

# TypeError
result = "5" + 5

# IndexError
lst = [1, 2, 3]
print(lst[10])

# KeyError
d = {"a": 1}
print(d["b"])

# FileNotFoundError
f = open("nonexistent.txt")
```


## Common Runtime Error Types

| Error | Cause |
|-------|-------|
| `ZeroDivisionError` | Division by zero |
| `TypeError` | Wrong type for operation |
| `ValueError` | Right type, wrong value |
| `IndexError` | List index out of range |
| `KeyError` | Dictionary key not found |
| `AttributeError` | Object has no attribute |
| `NameError` | Name not defined |
| `FileNotFoundError` | File does not exist |


## Runtime Errors Allow Partial Execution

With runtime errors, code runs until the error occurs.

```python
print("This prints")  # Executes

x = 10 / 0  # RuntimeError here

print("This never prints")  # Never reached
```

Output:
```
This prints
ZeroDivisionError: division by zero
```


## Handling Runtime Errors

Runtime errors can be caught and handled with `try/except`.

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
    result = 0

print(f"Result: {result}")
```

Output:
```
Cannot divide by zero
Result: 0
```


## Forward Referencing Errors

Forward referencing errors occur when code attempts to use a variable, function, or class before it has been defined. These are runtime errors (`NameError`) caused by Python's sequential execution model.


### Variable Forward Reference

Using a variable before assignment raises `NameError`.

```python
print(x)  # NameError: name 'x' is not defined
x = 10
```

**Fix**: Define variables before use.

```python
x = 10
print(x)  # 10
```


### Function Forward Reference

Calling a function before its definition raises `NameError`.

```python
result = add(5, 3)  # NameError: name 'add' is not defined

def add(a, b):
    return a + b
```

**Fix**: Define functions before calling them.

```python
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # 8
```


### Why Forward Referencing Errors Occur

Python processes code sequentially:

1. The interpreter reads code line by line
2. Names are added to the namespace when assigned
3. Referencing a name requires it to already exist

```python
# At this point, 'x' is not in the namespace
print(x)  # NameError

# Now 'x' is added to the namespace
x = 10
```


### Functions Can Reference Each Other

Function bodies are not executed until called, so mutual references work.

```python
def is_even(n):
    if n == 0:
        return True
    return is_odd(n - 1)  # is_odd not defined yet, but OK

def is_odd(n):
    if n == 0:
        return False
    return is_even(n - 1)

print(is_even(4))  # True
```

This works because `is_odd` is only looked up when `is_even` is actually called, by which time both functions exist.


### Default Parameter Pitfall

A common forward referencing error occurs when using `self` in default parameter values.

```python
class BlackScholes:
    def __init__(self, T):
        self.T = T
    
    # ERROR: self doesn't exist when default is evaluated
    def run_MC(self, num_steps=int(self.T * 12 * 21)):
        pass
```

This fails because default parameter values are evaluated at function definition time, not at call time. At definition time, `self` doesn't exist yet.

**Fix**: Use `None` as default and set the value inside the method.

```python
class BlackScholes:
    def __init__(self, T):
        self.T = T
    
    def run_MC(self, num_steps=None):
        if num_steps is None:
            num_steps = int(self.T * 12 * 21)
        # ... method body
```


## Logical Errors

A third category exists: **logical errors**. The code runs without exceptions but produces incorrect results.

```python
# Logical error: wrong formula
def average(a, b):
    return a + b  # Should be (a + b) / 2

result = average(10, 20)
print(result)  # 30, but should be 15
```

Logical errors are the hardest to find because Python cannot detect them.


## Key Differences Summary

| Feature | Compile Error | Runtime Error | Logical Error |
|---------|---------------|---------------|---------------|
| When detected | Before execution | During execution | Never (by Python) |
| Program runs? | No | Partially (until error) | Yes, completely |
| Type in Python | `SyntaxError` | Various exception types | None |
| Can be caught? | No | Yes, with `try/except` | No |
| Detection method | Parser | Interpreter | Testing/review |


## Best Practices

1. **Define variables before use**
   ```python
   x = 10
   print(x)
   ```

2. **Define functions before calling**
   ```python
   def greet():
       print("Hello")
   
   greet()
   ```

3. **Use `None` for instance-dependent defaults**
   ```python
   def method(self, value=None):
       if value is None:
           value = self.default_value
   ```

4. **Organize code with definitions first**
   ```python
   # Constants
   MAX_SIZE = 100
   
   # Functions
   def process():
       pass
   
   # Main execution
   if __name__ == "__main__":
       process()
   ```

---

## Exercises


**Exercise 1.**
Classify each of the following errors as compile-time (syntax) or runtime. Verify by writing code that triggers each.

- Missing colon after `if`
- Dividing by zero
- Using an undefined variable
- Invalid indentation

??? success "Solution to Exercise 1"

        ```python
        # Compile-time (SyntaxError):
        # if True      # Missing colon -> SyntaxError
        # def f():
        #  x = 1       # Invalid indentation -> IndentationError

        # Runtime errors:
        try:
            result = 1 / 0
        except ZeroDivisionError as e:
            print(f"Runtime: {e}")

        try:
            print(undefined_variable)
        except NameError as e:
            print(f"Runtime: {e}")
        ```

    Syntax errors are caught during parsing, before any code executes. Runtime errors occur during execution.

---

**Exercise 2.**
Write a function that contains a syntax error and show that importing the module fails immediately. Then fix the error and show that the function works.

??? success "Solution to Exercise 2"

        ```python
        # File with syntax error (cannot be imported):
        # def broken(:     # SyntaxError: invalid syntax

        # Fixed version:
        def fixed():
            return "It works!"

        print(fixed())  # It works!
        ```

    Python compiles the entire module before executing any code. A syntax error anywhere in the file prevents the entire module from loading.

---

**Exercise 3.**
Write code that passes syntax checking but raises a `TypeError` at runtime. Explain why Python cannot catch this error at compile time.

??? success "Solution to Exercise 3"

        ```python
        def add(a, b):
            return a + b

        # This is valid syntax but fails at runtime
        try:
            result = add("hello", 42)
        except TypeError as e:
            print(f"Runtime error: {e}")
            # unsupported operand type(s) for +: 'str' and 'int'
        ```

    Python is dynamically typed, so the types of `a` and `b` are not known until runtime. The syntax `a + b` is valid for many type combinations, so Python cannot determine at compile time that this particular call will fail.
