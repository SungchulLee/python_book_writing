
# print() and input()

These functions connect the program to its environment---`print()` sends data out, `input()` brings data in. They are the primary mechanism for console interaction.

Unlike most built-ins which transform data and return results, these functions primarily produce **side effects**: `print()` writes to the output stream (and returns `None`), while `input()` reads from the input stream (and returns a string).

| Function | Purpose |
|---|---|
| `print()` | display output |
| `input()` | receive user input |

These functions enable simple **input/output interaction** in programs.

```mermaid
flowchart LR
    A[Program] --> B[input()]
    B --> C[User]
    C --> D[print()]
    D --> A
````

!!! tip "Mental Model"
    `print()` and `input()` are your program's mouth and ears. `print()` converts any Python object into text and sends it to the screen; `input()` pauses the program, waits for the user to type, and always returns a string. Remember that `input()` returns a string even when the user types a number---you must convert it yourself.

---

## print()

`print()` displays information to the console.

### Example

```python
print("Hello Python")
```

Output

```
Hello Python
```

---

## Multiple Values

```python
name = "Alice"
age = 25

print(name, age)
```

Output

```
Alice 25
```

---

## Separator and End

```python
print("A","B","C",sep="-")
```

Output

```
A-B-C
```

Example

```python
print("Hello", end=" ")
print("World")
```

Output

```
Hello World
```

---

## input()

`input()` reads user input from the keyboard.

Example

```python
name = input("Enter your name: ")
print("Hello", name)
```

---

## Important Note

`input()` always returns a **string**, because interactive input is always text from the terminal. Parsing it into other types is the program's responsibility.

Example

```python
age = input("Enter age: ")
print(type(age))
```

Output

```
<class 'str'>
```

Convert values if needed:

```python
age = int(input("Enter age: "))
```

---

## Practical Example

```python
# Simple CLI program
name = input("Enter your name: ")
age = int(input("Enter your age: "))

print(f"{name} will be {age + 1} next year.")
```

---

## Exercises

**Exercise 1.**
`print()` has several keyword arguments. Predict the output:

```python
print("a", "b", "c")
print("a", "b", "c", sep="")
print("a", "b", "c", sep="-", end="!\n")
print("x", end="")
print("y", end="")
print()
```

What are the default values of `sep` and `end`? Why does `print()` with no arguments print an empty line?

??? success "Solution to Exercise 1"
    Output:

    ```text
    a b c
    abc
    a-b-c!
    xy
    ```

    The default values are `sep=" "` (single space) and `end="\n"` (newline). These defaults make `print("a", "b", "c")` produce `"a b c\n"`.

    `print()` with no arguments prints just the `end` value, which defaults to `"\n"` -- so it outputs an empty line. This is the idiomatic way to print a blank line in Python.

---

**Exercise 2.**
`input()` always returns a string, which leads to a common bug:

```python
age = input("Age: ")  # User types: 25
print(age + 10)
```

What error occurs? Why does Python not automatically convert input to numbers? Show the safe pattern for reading integers from `input()` that handles invalid input gracefully.

??? success "Solution to Exercise 2"
    `age + 10` raises `TypeError: can only concatenate str (not "int") to str` because `age` is the string `"25"`, not the integer `25`.

    Python does not automatically convert because the conversion is ambiguous: should `"25" + 10` be `"2510"` (concatenation after converting `10` to string) or `35` (addition after converting `"25"` to int)? Python refuses to guess.

    Safe pattern:

    ```python
    while True:
        try:
            age = int(input("Age: "))
            break
        except ValueError:
            print("Please enter a valid number")
    ```

---

**Exercise 3.**
`print()` returns `None`. Predict the output:

```python
result = print("hello")
print(result)
print(type(result))
```

Why does `print()` return `None` instead of the string it printed? How does this relate to the distinction between functions that perform side effects and functions that compute values?

??? success "Solution to Exercise 3"
    Output:

    ```text
    hello
    None
    <class 'NoneType'>
    ```

    `print("hello")` displays `"hello"` on the screen and returns `None`. The `None` return value is then printed by the second `print()`.

    `print()` returns `None` because its purpose is a **side effect** (displaying text), not computing a value. Functions that primarily cause side effects (printing, writing to files, modifying global state) conventionally return `None` in Python. Functions that compute values (`len()`, `sum()`, `sorted()`) return the computed result. This convention helps programmers distinguish between "do something" functions and "compute something" functions.
