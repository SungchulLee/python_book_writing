
# Pure Functions

A pure function is a function whose output depends only on its inputs and that causes no observable changes outside itself. This is the simplest kind of function to understand, test, and reuse---and recognizing purity is a foundational skill for writing predictable Python code.

## The Mental Model

Think of a pure function as a reliable machine: you feed it the same raw materials, and it always produces the same product. It never reaches out to flip a switch, rearrange the warehouse, or write a note on the wall. Everything it does is fully captured by the relationship between its inputs and its output.

Two rules define purity:

1. **Deterministic**: given the same arguments, the function always returns the same result.
2. **No side effects**: the function does not modify any state outside its own local scope---no changing global variables, no mutating arguments, no printing, no writing to files.

If a function violates either rule, it is impure.

## Pure Functions in Practice

Many of Python's built-in functions are pure.

```python
# abs() is pure: same input, same output, no side effects
print(abs(-7))   # 7
print(abs(-7))   # 7 again---always

# len() is pure
print(len([1, 2, 3]))  # 3

# sorted() is pure: it returns a new list, leaving the original unchanged
original = [3, 1, 2]
result = sorted(original)
print(result)     # [1, 2, 3]
print(original)   # [3, 1, 2] --- untouched
```

Writing your own pure functions follows the same principle: take inputs, compute, return a result.

```python
def square(n):
    return n * n

def add(a, b):
    return a + b

def initials(first_name, last_name):
    return first_name[0].upper() + last_name[0].upper()
```

Each of these functions depends only on its parameters and produces its result entirely through `return`. No external state is read or written.

## Impure Functions

A function is impure when it either depends on something beyond its arguments or changes something outside its own scope.

```python
# print() is impure: it performs I/O (writes to the screen)
print("hello")

# list.append() is impure: it mutates the list in place
numbers = [1, 2, 3]
numbers.append(4)  # modifies `numbers` rather than returning a new list

# random.randint() is impure: same arguments, different results
import random
print(random.randint(1, 10))  # could be any number
print(random.randint(1, 10))  # likely a different number
```

A subtler case is a function that reads from external state:

```python
tax_rate = 0.08

def calculate_tax(price):
    return price * tax_rate  # depends on the global variable `tax_rate`
```

Even though `calculate_tax` does not modify anything, its result depends on a value that could change elsewhere in the program. A truly pure version would accept the rate as a parameter:

```python
def calculate_tax(price, rate):
    return price * rate
```

## Why Purity Matters

Pure functions provide concrete practical benefits.

**Testability.** A pure function can be tested by calling it with known inputs and checking the output. No setup of global state is needed, and no cleanup is required afterward.

```python
def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32

# Easy to test: just assert input-output pairs
assert celsius_to_fahrenheit(0) == 32.0
assert celsius_to_fahrenheit(100) == 212.0
```

**Reasoning.** When reading code, you can understand a pure function in isolation. You do not need to trace how global variables change or what other functions have run before it.

**Caching.** Because pure functions always return the same result for the same arguments, their results can be cached safely. Python provides `functools.lru_cache` for exactly this purpose.

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(50))  # 12586269025 --- computed efficiently via caching
```

Caching an impure function would be dangerous: you would get stale or incorrect results when the external state changes.

**Composability.** Pure functions combine naturally. Because each one is self-contained, you can chain them without worrying about hidden interactions.

```python
def normalize(text):
    return text.strip().lower()

def word_count(text):
    return len(text.split())

# Compose freely: no hidden state to manage
count = word_count(normalize("  Hello World  "))
print(count)  # 2
```

## Recognizing Purity

A quick checklist for determining whether a function is pure:

- Does it use only its parameters (and local variables) to compute the result? If it reads a global or an attribute of a mutable object passed in from outside, it may not be pure.
- Does it return a value without modifying its arguments? If it calls `.append()`, `.update()`, or similar mutating methods on its inputs, it is impure.
- Does it avoid I/O? If it calls `print()`, `open()`, or interacts with a database or network, it is impure.
- Does it always produce the same output for the same input? If it uses `random`, `datetime.now()`, or reads from a file, it is impure.

---

## Exercises

**Exercise 1.**
Classify each function as pure or impure. For each impure function, identify which rule of purity it violates.

```python
import random

def multiply(a, b):
    return a * b

def greet(name):
    print(f"Hello, {name}!")
    return f"Hello, {name}!"

def roll_dice():
    return random.randint(1, 6)

def first_element(items):
    return items[0]

total = 0

def add_to_total(n):
    global total
    total += n
    return total
```

??? success "Solution to Exercise 1"

    - `multiply(a, b)`: **Pure.** It depends only on its arguments and returns a result without side effects.

    - `greet(name)`: **Impure.** It violates the "no side effects" rule by calling `print()`, which performs I/O. Even though it also returns a value, the `print` call makes it impure.

    - `roll_dice()`: **Impure.** It violates the "deterministic" rule. Calling it twice with no arguments can produce different results because it depends on the random number generator's internal state.

    - `first_element(items)`: **Pure.** It reads from its argument without modifying it and returns a deterministic result. (Note: it will raise an `IndexError` on an empty list, but that is an error condition, not a side effect.)

    - `add_to_total(n)`: **Impure.** It violates both rules. It modifies the global variable `total` (side effect), and its return value depends on the current value of `total` (not deterministic based on arguments alone).

---

**Exercise 2.**
The following function is impure because it mutates its argument. Rewrite it as a pure function that returns a new list instead of modifying the original.

```python
def remove_negatives(numbers):
    i = 0
    while i < len(numbers):
        if numbers[i] < 0:
            numbers.pop(i)
        else:
            i += 1
```

Verify that your rewritten function leaves the original list unchanged.

??? success "Solution to Exercise 2"
    A pure version returns a new list and does not touch the original:

    ```python
    def remove_negatives(numbers):
        return [n for n in numbers if n >= 0]
    ```

    Verification:

    ```python
    original = [3, -1, 4, -5, 2]
    result = remove_negatives(original)

    print(result)    # [3, 4, 2]
    print(original)  # [3, -1, 4, -5, 2] --- unchanged
    ```

    The list comprehension creates a brand-new list, so `original` is never modified. The function is now pure: it depends only on its input and produces its output solely through `return`.

---

**Exercise 3.**
The `fibonacci` function below is pure but slow for large inputs. Explain why caching is safe for this function. Then add `@lru_cache` and compare the performance for `fibonacci(35)`.

```python
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

Would it be safe to cache a function that reads `datetime.now()` inside its body? Why or why not?

??? success "Solution to Exercise 3"
    Caching is safe for `fibonacci` because it is pure: for any given `n`, it always returns the same result, and it has no side effects. This means a cached result is guaranteed to be correct whenever the same `n` is requested again.

    Adding the cache:

    ```python
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)
    ```

    Without caching, `fibonacci(35)` makes roughly 18 million recursive calls (exponential growth). With caching, each value from `fibonacci(0)` through `fibonacci(35)` is computed exactly once---36 calls total. The speedup is dramatic: from several seconds to effectively instant.

    It would **not** be safe to cache a function that reads `datetime.now()`. Such a function is impure (its output depends on external state---the system clock). Caching it would freeze the first result and return that stale timestamp on every subsequent call, which is almost certainly not the intended behavior.

Next: [Side Effects and State Changes](side_effects.md).
