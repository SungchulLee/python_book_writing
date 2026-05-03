# Practical Uses

Boolean logic has extensive practical applications in real-world programming scenarios.

!!! tip "Mental Model"
    Booleans are the steering wheel of your program. Every `if`, `while`, and `filter` ultimately reduces to a `True`/`False` decision. Once you recognize that any Python object can act as a boolean (truthy or falsy), you can use boolean logic everywhere -- from controlling loops with flags to compressing conditional chains into single expressions.

---

## Conditional Execution

Using booleans to control program flow.

### 1. Basic Conditional

```python
x = 10
y = 20
if x < y:
    print("x is smaller than y")
```

### 2. Decision Making

Booleans enable branching logic based on conditions.

---

## Boolean Flags

Using boolean variables to control program state.

### 1. Control Loop

```python
active = True
while active:
    command = input("Enter command: ")
    if command == "exit":
        active = False
```

### 2. State Management

Boolean flags track program state and control execution flow.

---

## Data Filtering

Using boolean logic to filter collections.

### 1. Remove Falsy

```python
numbers = [0, 1, 2, 3, 4, 5]
filtered = list(filter(bool, numbers))  # Removes falsy values (0)
print(filtered)  # Output: [1, 2, 3, 4, 5]
```

### 2. Filter Pattern

Boolean functions enable elegant data filtering patterns.

---

## Optimization

Boolean logic in performance-critical code.

### 1. Branch Prediction

Boolean logic allows for branch prediction improvements in modern CPUs.

### 2. Redundant Compute

Short-circuit evaluation reduces redundant computations in performance-critical applications.

### 3. Algorithm Design

Boolean flags optimize algorithm flow and reduce unnecessary operations.

---

## Common Patterns

Frequently used boolean patterns.

### 1. Validation

```python
def is_valid_email(email):
    return '@' in email and '.' in email
```

### 2. Guard Clauses

```python
def process_data(data):
    if not data:
        return None
    # Process data
```

### 3. Toggle State

```python
is_enabled = False
is_enabled = not is_enabled  # Toggle
```

---

## Applications

Boolean logic spans multiple domains.

### 1. AI Systems

Decision-making frameworks in artificial intelligence.

### 2. Data Validation

Protocols for ensuring data integrity and correctness.

### 3. Numerical Computing

Optimization in numerical algorithms and scientific computing.

### 4. Machine Learning

Feature engineering and conditional logic in ML pipelines.

---

## Conclusion

Mastering boolean logic is essential for writing robust, efficient, and scalable code across various computational disciplines. Boolean values enable expressive control structures, efficient filtering, and optimized performance in both high-level and low-level applications.

---

## Exercises


**Exercise 1.**
Write a function `all_positive(numbers)` that returns `True` if every number in the list is positive, without using the built-in `all()`. Use boolean logic and early return.

??? success "Solution to Exercise 1"

        ```python
        def all_positive(numbers):
            for n in numbers:
                if n <= 0:
                    return False
            return True

        print(all_positive([1, 2, 3]))     # True
        print(all_positive([1, -2, 3]))    # False
        print(all_positive([]))            # True
        ```

    The function returns `False` as soon as a non-positive number is found. If the loop completes, all numbers are positive.

---

**Exercise 2.**
Write a one-liner using `sum()` and a generator expression to count how many strings in a list have length greater than 5. For example, `["hi", "hello", "wonderful", "ok", "python"]` should return `2`.

??? success "Solution to Exercise 2"

        ```python
        words = ["hi", "hello", "wonderful", "ok", "python"]
        count = sum(len(s) > 5 for s in words)
        print(count)  # 2
        ```

    `len(s) > 5` produces `True` or `False`, and `sum()` treats `True` as `1` and `False` as `0`, effectively counting matches.

---

**Exercise 3.**
Write a function `classify_value(x)` that returns `"falsy"` if `x` is falsy and `"truthy"` otherwise. Test it with `0`, `""`, `[]`, `None`, `1`, `"hello"`, and `[1, 2]`.

??? success "Solution to Exercise 3"

        ```python
        def classify_value(x):
            return "falsy" if not x else "truthy"

        for val in [0, "", [], None, 1, "hello", [1, 2]]:
            print(f"{str(val):>10} -> {classify_value(val)}")
        ```

    Output:

        ```
                 0 -> falsy
                   -> falsy
                [] -> falsy
              None -> falsy
                 1 -> truthy
             hello -> truthy
            [1, 2] -> truthy
        ```
