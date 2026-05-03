
# Ternary Expressions

A ternary expression is a compact form of `if/else`, used when the decision fits within a single expression. Unlike `if/else`, which controls **execution** (which statements run), a ternary controls **evaluation** (which value is produced).

Ternary expressions are not about saving lines of code---they are about keeping simple decisions inline with expressions.

Syntax:

````

value_if_true if condition else value_if_false

````

!!! tip "Mental Model"
    A ternary expression is an inline fork: it evaluates a condition and produces one of two values on the spot. Read `A if C else B` as "give me A when C is true, otherwise B." Use it when the choice is simple enough to fit naturally inside an assignment or function argument.

---

## Example

```python
age = 20

status = "adult" if age >= 18 else "minor"

print(status)
````

Output:

```
adult
```

---

## Numeric Example

```python
x = 10
y = 20

maximum = x if x > y else y
```

---

## List Comprehension Example

```python
numbers = [1,2,3,4]

labels = ["even" if n % 2 == 0 else "odd" for n in numbers]
```

### When to Use Ternary Expressions

Use when:

- the condition is simple
- both outcomes are expressions (not complex logic)
- readability improves over a full `if/else` block

Avoid when:

- nesting is required
- the logic becomes harder to scan than a plain `if/else`

Ternary expressions are best used for **simple, two-way choices**.

---

### Design Insight

Python's ternary syntax places the result value first:

```python
value_if_true if condition else value_if_false
```

This reads like English: "use this value *if* the condition holds, *else* that value." Compared to C's `condition ? a : b`, Python's order makes the **chosen values more visible**, which matters when scanning complex expressions.

---

### Tradeoff: Conciseness vs Clarity

Ternary expressions compress code---but compression is not always improvement. Use them when they remove boilerplate and keep logic local. Avoid them when they obscure control flow or require mental parsing.

---

### Limitations

A ternary expression is an **expression**, not a statement. It must evaluate to a value and cannot contain standard assignments (`=`). However, Python 3.8+ assignment expressions (`:=`) can be used:

```python
result = (x := 5) if condition else (x := 10)
```

The key is not the syntax, but recognizing when an expression-level decision is clearer than a statement-level one.

---

## Exercises

**Exercise 1.**
Python's ternary syntax is `value_if_true if condition else value_if_false`, which differs from C's `condition ? value_if_true : value_if_false`. Predict the output:

```python
x = 5
print("positive" if x > 0 else "non-positive")
print(x if x > 0 else -x)
print("even" if x % 2 == 0 else "odd")
```

Why did Python choose this syntax order (value first, condition second) rather than C's order? What readability advantage does it provide?

??? success "Solution to Exercise 1"
    Output:

    ```text
    positive
    5
    odd
    ```

    Python's syntax puts the "happy path" value first: `value_if_true if condition else value_if_false`. This reads like English: "give me positive if x is greater than zero, else non-positive." The common/expected value appears first, making code more readable when scanning.

    C's syntax `condition ? a : b` puts the condition first, which is natural for conditional logic but makes the values harder to spot. Python's order optimizes for readability of the result, which is what matters most when a ternary is used inside a larger expression like `f"The number is {'even' if n % 2 == 0 else 'odd'}"`.

---

**Exercise 2.**
Ternary expressions can be nested, but this quickly becomes unreadable. Predict the output:

```python
x = 0
result = "positive" if x > 0 else "zero" if x == 0 else "negative"
print(result)
```

How does Python parse the nesting? Rewrite this using an explicit `if/elif/else` block. Why do most style guides discourage nested ternaries?

??? success "Solution to Exercise 2"
    Output: `zero`.

    Python parses nested ternaries right-to-left: `"positive" if x > 0 else ("zero" if x == 0 else "negative")`. Since `x = 0`, the first condition `x > 0` is `False`, so Python evaluates the else part. In the nested ternary, `x == 0` is `True`, so `"zero"` is returned.

    Rewritten as `if/elif/else`:

    ```python
    if x > 0:
        result = "positive"
    elif x == 0:
        result = "zero"
    else:
        result = "negative"
    ```

    Most style guides discourage nested ternaries because they are hard to read and easy to misparse. The explicit `if/elif/else` is clearer and barely longer. Ternaries are best for simple two-way choices.

---

**Exercise 3.**
A ternary expression is an **expression**, not a statement. Explain why this distinction matters:

```python
# This works:
y = 10 if True else 20

# This does NOT work as intended:
# 10 if True else print("hello")
```

Can a ternary expression contain assignments? Why or why not? Give an example where using a ternary expression inside a function call is clean and useful.

??? success "Solution to Exercise 3"
    A ternary is an **expression** -- it produces a value. A statement (like `if/else`) performs an action but does not produce a value. This means ternaries can be used anywhere a value is expected: in assignments, function arguments, list comprehensions, and f-strings.

    A ternary expression **cannot** contain assignments (in the traditional sense):

    ```python
    # SyntaxError:
    # x = 5 if True else y = 10
    ```

    However, Python 3.8+ has the walrus operator `:=`, which is an assignment expression:

    ```python
    result = (x := 5) if True else (x := 10)
    ```

    A clean and useful example inside a function call:

    ```python
    print(f"Status: {'active' if user.is_active else 'inactive'}")
    ```

    This is concise, readable, and avoids a temporary variable. The ternary fits naturally inside the f-string because it is an expression.
