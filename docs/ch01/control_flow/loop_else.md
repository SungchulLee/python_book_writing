
# Loop Else

Python loops support an optional `else` clause. This feature builds directly on `break`---it is `break` that determines whether the `else` block runs.

The `else` block runs **only if the loop completes normally** (without hitting `break`).

If a `break` statement occurs, the `else` block is skipped. A useful way to read `for...else` is: "for each item, do this; if no `break` occurred, then do that."

!!! tip "Mental Model"
    Read `for...else` as "search...not found." The `else` block fires only when the loop ends naturally without `break`. This makes it a clean pattern for search-and-report: loop through items looking for a match, and if no `break` occurs, the `else` block handles the "not found" case.

## Example

```python
numbers = [1,3,5,7]

for num in numbers:

    if num == 4:
        print("Found")
        break

else:
    print("4 not found")
```

Output:

```
4 not found
```

## Practical Pattern: Searching

The `for...else` construct is designed to express: "Search for something; if not found, handle the fallback."

```python
def find_number(nums,target):

    for num in nums:

        if num == target:
            return True

    else:
        return False
```

This pattern cleanly expresses **search logic**.

---

## Comparison: for...else vs Flag Variable

The flag-based approach uses extra state to track whether the loop succeeded:

```python
found = False

for num in nums:
    if num == target:
        found = True
        break

if not found:
    print("not found")
```

The `for...else` approach keeps the logic local:

```python
for num in nums:
    if num == target:
        break
else:
    print("not found")
```

| Approach      | Characteristics                   |
| ------------- | --------------------------------- |
| Flag variable | explicit state, more verbose      |
| `for...else`  | no extra state, logic stays local |

`for...else` is preferable when the loop's purpose is **search** and the fallback depends on "not found."

---

## Interaction with continue

`continue` does **not** affect the `else` clause. Only `break` determines whether `else` runs.

```python
for i in range(5):
    if i == 2:
        continue
    print(i)
else:
    print("done")
```

Output:

```
0
1
3
4
done
```

---

## Design Insight

Python's `for...else` eliminates the need for external state tracking. Instead of managing a flag variable and checking it after the loop, you express the logic directly: "If the loop didn't terminate early, do this." This keeps logic localized and intent explicit.

---

## When Not to Use for...else

Avoid `for...else` when:

- You can use `return` directly inside a function
- The loop is not conceptually a search
- It reduces readability for your audience

```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True  # clearer than for...else here
```

In functions, `return` often makes `else` unnecessary.

---

!!! warning "Common Misconception"
    The name `else` does **not** mean "if the loop condition is false" (by analogy with `if/else`). It actually means "if no `break` occurred." A clearer mental reading is `nobreak` or `if_no_break`.

---



---

## Notebook Examples

```python
for i in range(10):
    if i == 7:
        break
    print(i)
```

```python
for i in range(10):
    if i == 7:
        break
    print(i)
else:
    print("wow")
```

```python
for i in range(10):
    if i == 77:
        break
    print(i)
else: # no break
    print("wow")
```

---

## Exercises

**Exercise 1.**
The `else` clause on a loop runs when the loop completes "normally" (without `break`). Predict the output:

```python
for i in range(5):
    if i == 10:
        break
else:
    print("no break")

for i in range(5):
    if i == 3:
        break
else:
    print("no break")
```

Why does the name `else` confuse many programmers? What would be a more intuitive name for this feature?

??? success "Solution to Exercise 1"
    Output:

    ```text
    no break
    ```

    Only the first `"no break"` prints. In the first loop, `i` never equals `10`, so `break` never executes, and the `else` clause runs. In the second loop, `i == 3` triggers `break`, so the `else` clause is **skipped**.

    The name `else` confuses programmers because they read it as "else if the loop condition is false" (by analogy with `if/else`). A more intuitive name would be `nobreak` or `then` -- "do this if the loop completed without breaking." Raymond Hettinger (Python core developer) has suggested thinking of it as "if no break."

---

**Exercise 2.**
`while` loops also support `else`. Predict the output:

```python
n = 5
while n > 0:
    n -= 1
else:
    print(f"ended with n={n}")

n = 5
while n > 0:
    n -= 1
    if n == 2:
        break
else:
    print(f"ended with n={n}")
```

Explain when the `else` clause executes in each case. Is it possible for the `else` block to run if the `while` condition was never `True`?

??? success "Solution to Exercise 2"
    Output:

    ```text
    ended with n=0
    ```

    Only the first `else` clause runs. The first `while` loop runs until `n` reaches `0`, at which point `n > 0` is `False` and the loop exits normally. The `else` clause executes.

    The second `while` loop hits `break` when `n == 2`, so the `else` clause is skipped.

    Yes, the `else` block runs even if the `while` condition was never `True`:

    ```python
    while False:
        pass
    else:
        print("runs!")  # This prints!
    ```

    The `else` clause runs whenever `break` was NOT hit. If the loop body never executes (because the condition was initially false), `break` was certainly not hit, so `else` runs.

---

**Exercise 3.**
The classic use case for loop `else` is primality testing:

```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    else:
        return True
```

Explain how this works. Then explain: could you write this function without `for...else`? What is the equivalent code without using `else`? Is the `else` version actually clearer?

??? success "Solution to Exercise 3"
    The function works as follows: it loops through potential divisors from 2 to sqrt(n). If any divisor is found (`n % i == 0`), it returns `False` immediately via `break`-like behavior (actually `return`, which also exits the loop). If no divisor is found, the loop completes normally, and the `else` clause returns `True`.

    Without `for...else`:

    ```python
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    ```

    This is actually **simpler and more readable**. When the function returns inside the loop, the `else` clause is unnecessary -- `return True` at the end naturally means "we checked all divisors and found none." The `for...else` pattern is most useful when you need to distinguish "break happened" from "loop completed" and you are **not** inside a function that can use `return`. In practice, many Pythonistas find `for...else` confusing and prefer explicit alternatives.
