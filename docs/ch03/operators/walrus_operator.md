# Walrus Operator (:=)

The walrus operator (assignment expression) assigns a value and returns it in a single expression. Introduced in Python 3.8 (PEP 572), it enables more concise code in loops, conditions, and comprehensions.

!!! tip "Mental Model"
    `:=` is "assign and use in one shot." Instead of computing a value on one line and testing it on the next, `if (n := len(data)) > 10` does both at once. It shines in `while` loops and `if` conditions where you need to capture and test a result simultaneously. Use it sparingly -- readability drops fast if overused.

---

## Basic Usage

### Assignment in Condition

```python
if (n := len("hello")) > 3:
    print(f"String length {n} is greater than 3")
```

Output:
```
String length 5 is greater than 3
```

### Assignment in while Loop

```python
data = iter([1, 2, 3, None, 4])

while (value := next(data, None)) is not None:
    print(f"Value: {value}")
```

Output:
```
Value: 1
Value: 2
Value: 3
```

## List Comprehension Usage

### Filtering with Walrus

```python
numbers = range(10)
squared = [y for x in numbers if (y := x**2) > 20]
print(squared)
```

Output:
```
[25, 36, 49, 64, 81]
```

### Reusing Computation

```python
import re

text = "Hello123World"
pattern = re.compile(r'\d+')

if (match := pattern.search(text)):
    print(f"Found: {match.group()}")
```

Output:
```
Found: 123
```

## Practical Examples

### While Loop with Input

```python
import io

user_input = iter(["valid", "another", "quit"])

while (command := next(user_input)) != "quit":
    print(f"Processing: {command}")
```

Output:
```
Processing: valid
Processing: another
```

### Dictionary Comprehension

```python
data = ["apple", "pie", "a", "banana"]
lengths = {word: length for word in data if (length := len(word)) > 2}
print(lengths)
```

Output:
```
{'apple': 5, 'banana': 6}
```

## Advantages

### Cleaner Code

```python
def some_expensive_computation():
    return [1, 2, 3]

def process(x):
    pass

if (data := some_expensive_computation()):
    process(data)
```

Output:
```
```


---

## Exercises


**Exercise 1.**
Rewrite the following code to use the walrus operator so that `len(data)` is computed only once:

```python
data = [1, 2, 3, 4, 5]
if len(data) > 3:
    print(f"Long list with {len(data)} elements")
```

??? success "Solution to Exercise 1"

    ```python
    data = [1, 2, 3, 4, 5]
    if (n := len(data)) > 3:
        print(f"Long list with {n} elements")
    ```

    The walrus operator assigns `len(data)` to `n` and evaluates it in the condition simultaneously, avoiding a redundant call.

---

**Exercise 2.**
Use the walrus operator in a list comprehension to collect the squares of numbers from 1 to 10, but only include squares greater than 50.

??? success "Solution to Exercise 2"

    ```python
    result = [sq for x in range(1, 11) if (sq := x**2) > 50]
    print(result)  # [64, 81, 100]
    ```

    The walrus operator computes `x**2` once per iteration, assigns it to `sq`, uses it in the filter condition, and includes it in the output list.

---

**Exercise 3.**
Write a `while` loop that uses the walrus operator to read items from an iterator until `None` is encountered. Use `iter([10, 20, 30, None, 40])` as the data source.

??? success "Solution to Exercise 3"

    ```python
    data = iter([10, 20, 30, None, 40])

    while (value := next(data, None)) is not None:
        print(f"Processing: {value}")
    # Processing: 10
    # Processing: 20
    # Processing: 30
    ```

    The loop stops when `next()` returns `None`. The value `40` is never reached because `None` appears first and terminates the loop.
