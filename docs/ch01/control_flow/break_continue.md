
# break and continue

Loop control statements modify the execution flow **inside** loops. Loops define an *iteration space*; `break` and `continue` define how execution navigates that space. While `if` decides *which* code runs and loops decide *how many times* code runs, `break` and `continue` provide fine-grained control *within* each iteration.

!!! tip "Mental Model"
    `break` is an emergency exit---it stops the entire loop immediately. `continue` is a skip button---it jumps to the next iteration without finishing the current one. Both give you fine-grained control over a loop's behavior beyond what the loop condition alone provides.

---

## break

Use `break` when the goal has been achieved and further iteration is unnecessary.

`break` exits the loop immediately.

```python
numbers = [1,5,8,3]

for num in numbers:
    if num == 8:
        break
    print(num)
````

Output:

```
1
5
```

Execution stops when `8` is found.

---

## continue

Use `continue` when the current iteration should be skipped but the loop should keep going.

`continue` skips the rest of the current iteration.

```python
for i in range(10):

    if i % 2 == 0:
        continue

    print(i)
```

Output:

```
1
3
5
7
9
```

Even numbers are skipped.

---

## break vs continue

| Statement | Effect                  |
| --------- | ----------------------- |
| break     | exits the loop entirely |
| continue  | skips to next iteration |

!!! tip "Tradeoff"
    Overusing `continue` can make loop bodies harder to follow. When the skip condition is simple, restructuring the `if` condition is often clearer than using `continue`.

---

## Nested Loops

`break` affects only the **innermost loop**.

```python
for i in range(3):
    for j in range(3):
        if j == 1:
            break
        print(i,j)
```

The key is not the syntax, but choosing the right construct for the structure of the problem.

---



---

## Notebook Examples

```python
for i in range(5):
    print(i)

print()
print(i)
```

```python
for _ in range(5):
    print(_)

print()
print(_)
```

```python
for i in range(5):
    if i == 2:
        break
    print(i)

print()
print(i)
```

```python
for i in range(5):
    if i == 2:
        continue
    print(i) # skip when i is 2, continue the for loop (not break the for loop)

print()
print(i)
```

---

## Exercises

**Exercise 1.**
`break` only exits the innermost loop. Predict the output:

```python
for i in range(3):
    for j in range(3):
        if j == 1:
            break
        print(i, j)
    print(f"outer: {i}")
```

How many times does the `print(f"outer: {i}")` line execute? Why does `break` not stop the outer loop? How would you break out of both loops?

??? success "Solution to Exercise 1"
    Output:

    ```text
    0 0
    outer: 0
    1 0
    outer: 1
    2 0
    outer: 2
    ```

    `print(f"outer: {i}")` executes 3 times -- once for each iteration of the outer loop. `break` only exits the inner `for j` loop. The outer `for i` loop continues normally.

    To break out of both loops, you have several options:

    1. Use a flag variable and check it in the outer loop.
    2. Extract the nested loops into a function and use `return`.
    3. Raise an exception (not recommended for flow control).

    Option 2 is the most Pythonic:

    ```python
    def search():
        for i in range(3):
            for j in range(3):
                if j == 1:
                    return i, j
    ```

---

**Exercise 2.**
`continue` skips the rest of the current iteration, not the entire loop. Predict the output:

```python
for i in range(5):
    if i == 2:
        continue
    print(i)
else:
    print("done")
```

Does `continue` prevent the `else` clause from executing? Explain the interaction between `continue`, `break`, and loop `else`.

??? success "Solution to Exercise 2"
    Output:

    ```text
    0
    1
    3
    4
    done
    ```

    `continue` does NOT prevent the `else` clause from executing. The `else` clause runs only when the loop completes without hitting `break`. Since `continue` skips the rest of the current iteration but does NOT exit the loop, the loop still completes "normally."

    The rules:
    - `break`: exits the loop AND skips the `else` clause.
    - `continue`: skips the rest of the current iteration, loop continues normally, `else` still runs.
    - Normal completion (no `break`): `else` runs.

---

**Exercise 3.**
A programmer uses `break` inside a `while True` loop to search for a value:

```python
items = [3, 7, 2, 9, 5]
target = 9
found = False

for item in items:
    if item == target:
        found = True
        break

if found:
    print(f"Found {target}")
```

Rewrite this using the `for...else` pattern to eliminate the `found` flag variable. Why is the `for...else` pattern considered more Pythonic for search operations?

??? success "Solution to Exercise 3"
    Rewritten with `for...else`:

    ```python
    items = [3, 7, 2, 9, 5]
    target = 9

    for item in items:
        if item == target:
            print(f"Found {target}")
            break
    else:
        print(f"{target} not found")
    ```

    The `for...else` pattern eliminates the `found` flag variable. The `else` block runs only if the loop completes without `break` -- meaning the target was not found. If `break` executes (target found), the `else` block is skipped.

    This is more Pythonic because it expresses the intent directly: "search for the item; if not found, do this." The flag-variable approach requires the programmer to mentally track state across multiple lines. The `for...else` pattern makes the search logic self-contained.
