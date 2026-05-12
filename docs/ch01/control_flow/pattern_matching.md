

# Pattern Matching

Python 3.10 introduced **structural pattern matching** using the `match` statement.

Traditional conditionals ask: "Does this condition evaluate to true?" Pattern matching asks: **"Does this value match this structure?"** This is a shift from boolean logic to structural decomposition.

Pattern matching allows programs to dispatch behavior based on the **structure of data**. While `if/elif` chains test conditions one by one, `match/case` can simultaneously check a value's type, structure, and contents in a single pattern. This makes `match` particularly powerful when working with structured data like tuples, lists, or objects.

!!! tip "Mental Model"
    Pattern matching is like a mail sorter: it examines the shape and contents of a value and routes it to the matching handler. Unlike `if/elif` which tests conditions sequentially, `match/case` decomposes data---it can simultaneously check type, extract fields, and bind variables in one step.

---

## Basic Syntax

```python
match value:

    case pattern:
        action
````

---

## Example

```python
def http_status(code):

    match code:

        case 200:
            return "OK"

        case 404:
            return "Not Found"

        case _:
            return "Unknown"
```

The underscore `_` acts as a wildcard.

---

## Multiple Patterns

```python
match day:

    case "Saturday" | "Sunday":
        print("Weekend")

    case _:
        print("Weekday")
```

---

## Guards

Guards add conditional checks to patterns, combining structural matching with boolean filtering.

```python
match number:

    case int(x) if x > 0:
        print("positive")

    case int(x) if x < 0:
        print("negative")
```

!!! info "Design Insight"
    Pattern matching separates **structure** (the pattern) from **conditions** (the guard). In `case (x, y) if x > 0:`, the pattern `(x, y)` enforces that the value is a 2-tuple and binds components, while the guard `if x > 0` filters on value. This separation improves readability in complex dispatch logic.

---

## Pattern Types

| Type | Syntax | Effect |
| --- | --- | --- |
| Literal | `case 200:` | matches exact value |
| OR | `case 301 \| 302:` | matches either value |
| Capture | `case x:` | matches anything, binds to `x` |
| Wildcard | `case _:` | matches anything, no binding |
| Guard | `case x if x > 0:` | structural match + boolean filter |

!!! warning "Capture vs Comparison"
    A bare name like `case x:` is a **capture pattern** that matches *everything*---it does not compare against a variable named `x`. To match against a variable's value, use a dotted name (`case Status.OK:`) or a guard (`case x if x == expected:`). This is a common source of subtle bugs.

---

### When to Prefer match

Use `match` when:

- you are checking many structured cases
- you want to destructure data (tuples, lists, objects)
- `if/elif` chains become long or repetitive

Avoid when:

- simple boolean conditions suffice
- you have only 2--3 cases with no structural patterns

Pattern matching provides a more expressive alternative to long `if-elif` chains.

!!! tip "Tradeoff: Power vs Familiarity"
    Pattern matching is more expressive than `if/elif`, but less familiar to many readers and easier to misuse (especially capture patterns). Use it when it makes structure **clearer**, not just shorter.

---

### Relationship to Other Constructs

Pattern matching extends conditional logic along a spectrum:

- `if` --- boolean decisions
- ternary --- inline value selection
- `match` --- structured dispatch

It is not a replacement for `if`, but a **specialized tool** that can replace long `if/elif` chains when the logic depends on structure rather than simple conditions.

---



---

## Notebook Examples

```python
flag = 100

match flag:
    case 200:
        print( "OK" )
    case 404:
        print( "Not Found" )
    case _:
        print( "Unknown" )
```

```python
day = "sunday"

match day:
    case "Saturday" | "Sunday" | "saturday" | "sunday" :
        print("Weekend")
    case _:
        print("Weekday")
```

---

## Exercises

**Exercise 1.**
The wildcard `_` in `match` is NOT the same as the variable `_`. Explain the difference:

```python
match command:
    case "quit":
        exit()
    case _:
        print("Unknown")
```

What would happen if you replaced `_` with a named variable like `other`? Would the `case other:` pattern still match everything? Why is `_` special in pattern matching?

??? success "Solution to Exercise 1"
    In `match/case`, `_` is a **wildcard pattern** that matches anything without binding a name. It is always a catch-all.

    If you use `case other:`, it also matches everything -- but it **binds** the matched value to the variable `other`. After the match, `other` holds the value of `command`.

    ```python
    match command:
        case "quit":
            exit()
        case other:
            print(f"Unknown: {other}")  # other is bound to the value
    ```

    `_` is special because it explicitly communicates "I don't need this value" and does not create a binding. It is the conventional wildcard in Python's pattern matching (inspired by similar patterns in other languages like Haskell and Rust).

    Important: any bare name in a `case` pattern (like `case x:`) is a **capture pattern** that matches anything, not a comparison to a variable named `x`. To match against a variable's value, use a dotted name (`case Status.OK:`) or a guard (`case x if x == expected:`).

---

**Exercise 2.**
`match/case` performs **structural matching**, not just value comparison. Predict the output:

```python
point = (3, 4)

match point:
    case (0, 0):
        print("origin")
    case (x, 0):
        print(f"on x-axis at {x}")
    case (0, y):
        print(f"on y-axis at {y}")
    case (x, y):
        print(f"point at ({x}, {y})")
```

What values do `x` and `y` have after the match? How does structural matching differ from a simple equality check?

??? success "Solution to Exercise 2"
    Output: `point at (3, 4)`.

    The match proceeds top to bottom. `(0, 0)` does not match `(3, 4)`. `(x, 0)` does not match because the second element is `4`, not `0`. `(0, y)` does not match because the first element is `3`, not `0`. `(x, y)` matches any 2-tuple, binding `x = 3` and `y = 4`.

    Structural matching differs from equality in that it **destructures** the value. The pattern `(x, 0)` simultaneously checks that the value is a 2-tuple, that the second element is `0`, and captures the first element into `x`. An `if` statement would require separate checks: `if isinstance(point, tuple) and len(point) == 2 and point[1] == 0`.

---

**Exercise 3.**
A programmer converts an `if/elif` chain to `match/case`:

```python
# Original
if status == 200:
    msg = "OK"
elif status == 301 or status == 302:
    msg = "Redirect"
elif 400 <= status < 500:
    msg = "Client Error"
else:
    msg = "Other"
```

Rewrite this using `match/case` with guards (`if` clauses) and the `|` (or) pattern. What advantage does `match/case` provide over `if/elif` for this kind of dispatch?

??? success "Solution to Exercise 3"
    ```python
    match status:
        case 200:
            msg = "OK"
        case 301 | 302:
            msg = "Redirect"
        case code if 400 <= code < 500:
            msg = "Client Error"
        case _:
            msg = "Other"
    ```

    The `|` pattern (`301 | 302`) matches either value, replacing `or` in the `if` chain. The guard `if 400 <= code < 500` handles the range check, with `code` capturing the matched value.

    Advantages of `match/case`:

    1. Each case clearly shows the pattern being matched -- the dispatch structure is visually obvious.
    2. The `|` pattern for alternatives is cleaner than `or` chains.
    3. Guards separate the pattern (what type/structure) from the condition (what values), making complex dispatch easier to read.
