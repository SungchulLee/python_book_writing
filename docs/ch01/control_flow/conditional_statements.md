
# Conditional Statements

Conditional statements allow a program to **execute code only when certain conditions are satisfied**. At a deeper level, they define how a program makes decisions: "Given the current state, which path should the program take?"

The primary conditional structure in Python is the `if` statement.

!!! tip "Mental Model"
    Conditional statements are forks in the road. The program evaluates a condition, and the result determines which branch of code executes. Every `if` creates exactly two paths---one for `True`, one for `False`---and `elif` chains let you test multiple conditions in sequence until one matches.

---

### if–else Statement

```python
temperature = 15

if temperature > 20:
    print("Warm")
else:
    print("Cool")
```

The `else` block executes when the condition is `False`.

---

### Multiple Conditions (if–elif–else)

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
```

Python evaluates conditions **top to bottom**, executing the first match.

!!! warning "if vs elif vs multiple if"
    Using separate `if` statements is **not** the same as using `elif`. Separate `if` blocks are checked independently---every condition is evaluated regardless of prior matches. An `elif` chain is **mutually exclusive**: once one branch matches, all remaining branches are skipped.

    ```python
    # Independent checks — both can execute
    if x > 0:
        print("positive")
    if x < 10:
        print("less than 10")

    # Mutually exclusive — only the first match executes
    if x > 0:
        print("positive")
    elif x < 10:
        print("less than 10")
    ```

    Use `elif` when the conditions are mutually exclusive. Use separate `if` statements when multiple conditions may apply simultaneously.

---

### Logical Operators

Python allows combining conditions using logical operators.

| Operator | Meaning                             |
| -------- | ----------------------------------- |
| `and`    | both conditions must be true        |
| `or`     | at least one condition must be true |
| `not`    | reverses a condition                |

Example:

```python
user_age = 22
has_license = True

if user_age >= 18 and has_license:
    print("You can drive")
```

---

### Truthy and Falsy Values

Python treats some values as `False` automatically.

Falsy values include:

```
0
None
False
""
[]
{}
```

Everything else is considered **truthy**. This enables idiomatic Python: `if items:` is preferred over `if len(items) > 0:`, reflecting Python's philosophy of concise, readable expressions over explicit checks.

Example:

```python
name = ""

if name:
    print("Hello")
else:
    print("Name missing")
```

---

### Nested Conditionals

Conditional blocks can appear inside other conditional blocks.

```python
user_age = 20
has_license = True

if user_age >= 18:
    if has_license:
        print("You can drive")
```

However, excessive nesting can make programs harder to read. Prefer early returns or guard clauses to keep the main logic at a shallow indentation level.

```python
# Deeply nested (hard to follow)
if user_age >= 18:
    if has_license:
        if not suspended:
            print("You can drive")

# Flattened with guard clauses (clearer)
if user_age < 18:
    print("Too young")
elif not has_license:
    print("No license")
elif suspended:
    print("License suspended")
else:
    print("You can drive")
```

````

Ternary expressions offer a compact form of `if/else` for inline decisions. Pattern matching extends conditional logic further, allowing decisions based on the structure of data rather than simple conditions.

---

# loops.md

```md
## Loops

Loops allow programs to **repeat a block of code multiple times**.

Python provides two primary looping constructs:

- `for` loops
- `while` loops

```mermaid
flowchart TD
    A[Start Loop] --> B[Check Condition]
    B -->|True| C[Execute Block]
    C --> B
    B -->|False| D[Exit Loop]
````

---

### for Loop

The `for` loop iterates over an iterable object.

```python
for item in iterable:
    statement
```

Example:

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)
```

Output:

```
apple
banana
cherry
```

---

### range()

The `range()` function generates sequences of numbers.

```python
for i in range(5):
    print(i)
```

Output:

```
0
1
2
3
4
```

Other forms:

```python
range(start, stop)
range(start, stop, step)
```

Example:

```python
for i in range(2,10,2):
    print(i)
```

---

### Nested Loops

Loops can be placed inside other loops.

```python
for i in range(3):
    for j in range(3):
        print(i,j)
```

Nested loops are often used in **matrix operations or grid computations**.

---

## while Loop

The `while` loop continues executing while a condition remains true.

```python
count = 0

while count < 5:
    print(count)
    count += 1
```

Output:

```
0
1
2
3
4
```

---

## Infinite Loops

A `while True` loop creates an infinite loop.

```python
while True:
    command = input("> ")

    if command == "quit":
        break
```

This pattern is common in **interactive programs and servers**.

## Exercises

**Exercise 1.**
Python uses `if/elif/else` rather than a `switch` statement (before Python 3.10). A student writes:

```python
if x == 1:
    result = "one"
if x == 2:
    result = "two"
if x == 3:
    result = "three"
```

Explain why this is NOT equivalent to using `elif`. What would happen if `x` is `1` and one of the later `if` blocks accidentally sets `x = 2`? How does `elif` prevent this class of bug?

??? success "Solution to Exercise 1"
    With separate `if` statements, EACH condition is checked independently, in sequence. If `x == 1` is true and the first block sets some variable, the second `if x == 2` is still checked. If something inside the first block changes `x` to `2`, the second block would also execute -- both branches run.

    With `elif`, once a branch matches, all subsequent `elif` and `else` branches are **skipped entirely**. The chain is mutually exclusive by design. `elif` says "only check this if all previous conditions were false."

    ```python
    # Correct: mutually exclusive
    if x == 1:
        result = "one"
    elif x == 2:
        result = "two"
    elif x == 3:
        result = "three"
    ```

    The `elif` chain is also more efficient -- it stops checking conditions after the first match, while separate `if` statements always check every condition.

---

**Exercise 2.**
Predict the output and explain *why* Python treats these values this way in an `if` statement:

```python
for val in [0, 1, "", "hello", [], [0], None, True, False]:
    if val:
        print(f"{val!r:>10} -> truthy")
    else:
        print(f"{val!r:>10} -> falsy")
```

Why does Python allow non-boolean values in `if` conditions? What design philosophy does this reflect?

??? success "Solution to Exercise 2"
    Output:

    ```text
             0 -> falsy
             1 -> truthy
            '' -> falsy
       'hello' -> truthy
            [] -> falsy
           [0] -> truthy
          None -> falsy
          True -> truthy
         False -> falsy
    ```

    Python allows any value in an `if` condition because of **truthiness**: every object has a boolean interpretation. This reflects Python's "duck typing" philosophy -- if an object can be interpreted as true/false, it can be used where a boolean is expected.

    The rule: `0`, `""`, `[]`, `None`, `False` and other "empty" or "zero" values are falsy. Everything else is truthy. This makes code more concise: `if items:` is preferred over `if len(items) > 0:`.

---

**Exercise 3.**
A `while` loop condition is checked BEFORE each iteration, including the first one. What does this imply about a `while False:` loop? Contrast this with `for x in []:` -- are these equivalent? What is the fundamental difference between `while` and `for` in terms of when they terminate?

??? success "Solution to Exercise 3"
    `while False:` never executes its body -- the condition is checked first and is immediately false. The loop body runs zero times.

    `for x in []:` also never executes its body -- there are no elements to iterate over.

    Both result in zero iterations, but the mechanism differs:

    - `while` checks a **condition** before each iteration. It terminates when the condition becomes false (or was never true). The number of iterations is unpredictable -- it depends on how the condition changes.
    - `for` iterates over a **sequence** (or iterable). It terminates when the sequence is exhausted. The number of iterations is determined by the length of the iterable.

    `while` is for open-ended repetition (when you don't know how many times to repeat). `for` is for definite iteration (when you have a collection to process).
