

# Code Structure and Readability

Expressions compute values. Structure determines **which expressions run, and in what order**. Structure controls execution in the same way expressions control computation. Readable code is easier to maintain and less likely to contain errors. Python enforces readability through **indentation rules and simple syntax**.

This chapter explains:

* indentation and blocks
* comments
* the `pass` statement

!!! tip "Mental Model"
    In Python, what you see is what runs. Indentation is not decoration---it is the structure of your program. If two lines are at the same indentation level, they belong to the same block. Visual alignment and logical grouping are the same thing.

---

## 1. Indentation and Blocks

Unlike many languages, Python uses **indentation to define code blocks**.

!!! info "Why does Python use indentation instead of braces?"
    In brace-based languages (C, Java, JavaScript), indentation is optional --- code can be correctly braced but misleadingly indented. This creates a class of bugs where code *looks* right but *behaves* wrong. Python eliminates this by making the visual structure the actual structure. The tradeoff: whitespace errors become syntax errors, which some programmers find restrictive.

Example:

```python
if temperature > 30:
    print("Hot")
    print("Stay hydrated")
```

The colon `:` introduces a block, and all lines in the block must have the same indentation.

### Standard indentation

PEP 8 recommends **4 spaces per indentation level**.

### Block structure

```mermaid
flowchart TD
    A[if statement]
    A --> B[indented block]
    B --> C[statement 1]
    B --> D[statement 2]
```

Mixing tabs and spaces can cause errors such as:

```
IndentationError
```

or

```
TabError
```

---

## 2. Nested Blocks

Blocks can be nested.

Example:

```python
for i in range(3):
    for j in range(3):
        if i == j:
            print(i, j)
```

Each nested level increases indentation.

---

## 3. Guard Clauses

Guard clauses help avoid deep nesting.

Example:

```python
def process(data):
    if data is None:
        return None

    if not validate(data):
        return None

    return transform(data)
```

This improves readability.

---

## 4. Comments

Comments are annotations ignored by the interpreter.

Example:

```python
# This is a comment
x = 5
```

The most important rule:

**comment why, not what**.

Example:

```python
x = 5  # server requires minimum timeout
```

Bad example:

```python
x = x + 1  # increment x by 1
```

Comments that repeat obvious code are not useful. 

---

## 5. Docstrings

Docstrings document functions, classes, and modules.

Example:

```python
def calculate_area(length, width):
    """Calculate rectangle area."""
    return length * width
```

Docstrings are accessible at runtime:

```python
print(calculate_area.__doc__)
```

---

## 6. Comment Markers

Common markers include:

```
TODO
FIXME
HACK
NOTE
```

Example:

```python
# TODO: optimize algorithm
# FIXME: handle empty list
```

---

## 7. The `pass` Statement

Python requires every block to contain at least one statement.

The `pass` statement acts as a **placeholder**.

Example:

```python
def future_feature():
    pass
```

Example class:

```python
class DatabaseConnection:
    pass
```

`pass` performs **no operation** but satisfies the syntax requirement. 

---

## 8. pass vs Ellipsis

Python also provides the **ellipsis literal**:

```python
...
```

Example:

```python
def parse():
    ...
```

Both serve as placeholders.

---

## 9. pass Does Not Exit a Function

Example:

```python
def demo():
    pass
    print("Still runs")

demo()
```

Output:

```
Still runs
```

Unlike `return`, `pass` does not stop execution.

---


## 10. Summary

Key ideas:

* indentation defines program structure
* blocks follow a colon `:`
* comments explain **intent**
* docstrings document functions and modules
* `pass` creates intentionally empty blocks

These conventions help Python code remain **clear and readable**.

!!! tip "One thing to remember"
    Structure controls which expressions run and when. Indentation is not decoration---it is the mechanism Python uses to determine program flow.


## Exercises

**Exercise 1.**
Python uses indentation to define blocks, whereas most other languages use braces `{}`. A programmer writes:

```python
if True:
    x = 1
    if True:
        y = 2
    z = 3
```

Which variables are set inside the inner `if` block, and which belong to the outer `if` block? Then explain what happens if you accidentally mix tabs and spaces for indentation. Why did Python's designers choose significant whitespace over braces?

??? success "Solution to Exercise 1"
    `y = 2` is inside the inner `if` block (indented 8 spaces). `x = 1` and `z = 3` are inside the outer `if` block (indented 4 spaces). `z = 3` is NOT inside the inner block -- it "de-dents" back to the outer block level.

    If you mix tabs and spaces, Python 3 raises a `TabError`. Python 3 does not allow mixing tabs and spaces for indentation (Python 2 was more permissive, which caused subtle bugs where code appeared aligned but was actually in different blocks).

    Python chose significant whitespace because it enforces the visual structure that programmers already use for readability. In brace-based languages, indentation is optional, so code can be correctly indented for the compiler but misleading to the human reader. Python eliminates this class of bugs by making the visual structure the actual structure.

---

**Exercise 2.**
A programmer writes `pass` and `return` in similar contexts:

```python
def version_a():
    pass
    print("after pass")

def version_b():
    return
    print("after return")
```

Predict the output of calling each function. Why does `pass` exist as a keyword if it does nothing? Give two realistic situations where `pass` is the correct choice.

??? success "Solution to Exercise 2"
    `version_a()` prints `"after pass"` and returns `None`. `version_b()` prints nothing and returns `None`.

    `pass` is a no-op -- it does nothing and execution continues to the next line. `return` exits the function immediately, so `print("after return")` is unreachable dead code.

    `pass` exists because Python's syntax requires at least one statement in every block. Without `pass`, you could not write:

    1. **Placeholder functions during development**: `def process_data(): pass` -- you plan to implement it later but need the function to exist now so other code can reference it.
    2. **Empty exception handlers**: `except KeyboardInterrupt: pass` -- you intentionally want to ignore an exception.

    The ellipsis `...` can also serve as a placeholder and is increasingly preferred in type stubs and abstract methods.

---

**Exercise 3.**
The Python style guide (PEP 8) says "comment why, not what." Evaluate each comment below and explain which are useful and which are not:

```python
x = x + 1                  # increment x
x = x + 1                  # compensate for border pixel
results = []               # create empty list
results = []               # accumulator for valid responses
if not user.is_active:     # check if user is not active
    send_reminder(user)    # inactive users get a weekly reminder
```

Why does commenting "what" become harmful as code evolves?

??? success "Solution to Exercise 3"
    - `# increment x` -- **not useful**. It restates the code. Anyone who reads `x = x + 1` already knows it increments `x`.
    - `# compensate for border pixel` -- **useful**. It explains *why* the increment is needed -- a domain-specific reason that is not obvious from the code alone.
    - `# create empty list` -- **not useful**. `results = []` is self-evident.
    - `# accumulator for valid responses` -- **useful**. It explains the *purpose* of the list, which helps readers understand the algorithm.
    - `# check if user is not active` -- **not useful**. It restates the condition.
    - `# inactive users get a weekly reminder` -- **useful**. It explains the business rule behind the code.

---

**Exercise 4.**
A student's code runs but produces wrong results. Find and fix the bug:

```python
temperature = 100
if temperature > 50:
    status = "hot"
    if temperature > 80:
        status = "very hot"
    recommendation = "stay inside"
print(status)
print(recommendation)
```

The student expects `recommendation` to always print, but sometimes gets a `NameError`. Under what condition does this fail, and how should the indentation be fixed?

??? success "Solution to Exercise 4"
    If `temperature` is 50 or less, the outer `if` block never executes, so neither `status` nor `recommendation` is ever defined. The `print` calls then raise `NameError: name 'status' is not defined`.

    Even when `temperature > 50`, the line `recommendation = "stay inside"` is inside the inner `if temperature > 80` block (indented 8 spaces). So if `temperature` is 60, `status` is `"hot"` but `recommendation` is never set.

    Fixed version:

    ```python
    temperature = 100
    if temperature > 50:
        status = "hot"
        if temperature > 80:
            status = "very hot"
        recommendation = "stay inside"  # now inside outer if, not inner
    else:
        status = "mild"
        recommendation = "enjoy outside"
    print(status)
    print(recommendation)
    ```

    This is a classic indentation bug: the visual structure appeared correct, but the indentation placed `recommendation` in the wrong block. In Python, indentation IS the structure.

---

**Exercise 5.**
Rewrite this deeply nested function using guard clauses (early returns) to eliminate nesting:

```python
def process(user):
    if user is not None:
        if user.is_active:
            if user.has_permission("edit"):
                return do_edit(user)
            else:
                return "no permission"
        else:
            return "inactive"
    else:
        return "no user"
```

??? success "Solution to Exercise 5"
    ```python
    def process(user):
        if user is None:
            return "no user"
        if not user.is_active:
            return "inactive"
        if not user.has_permission("edit"):
            return "no permission"
        return do_edit(user)
    ```

    Guard clauses handle error conditions first and return early, keeping the main logic at the shallowest indentation level. This is the same code with the same behavior, but much easier to read because each condition is handled independently rather than nested inside the previous one.

    "What" comments become harmful as code evolves because the code changes but comments often do not get updated. A stale comment that says "increment x" when the line now says `x = x + 2` is worse than no comment -- it actively misleads. "Why" comments are more durable because the reason for doing something changes less frequently than the specific implementation.
