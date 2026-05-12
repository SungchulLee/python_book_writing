
# Side Effects and State Changes

A side effect is any observable change that a function makes beyond returning a value. Understanding side effects---where they occur, why they make code harder to reason about, and when they are genuinely necessary---is essential for writing maintainable Python programs.

## The Mental Model

Imagine calling a function is like asking someone a question. A pure function simply gives you an answer. A function with side effects gives you an answer *and also* rearranges the furniture while you are not looking. The answer might be correct, but now the room looks different, and anyone who walks in next will be surprised.

Side effects create invisible connections between different parts of a program. When function A modifies a global variable that function B reads, those two functions are coupled even though neither calls the other directly. This hidden coupling is the root cause of many subtle bugs.

## Categories of Side Effects

### Modifying Mutable Arguments

When a function receives a mutable object (a list, dictionary, or set) and changes it, the caller's data changes too. This is because Python passes references, not copies.

```python
def add_greeting(messages, name):
    messages.append(f"Hello, {name}!")

my_messages = ["Welcome"]
add_greeting(my_messages, "Alice")
print(my_messages)  # ['Welcome', 'Hello, Alice!'] --- modified by the function
```

The caller might not expect `my_messages` to change. This side effect is especially dangerous when the same list is shared across multiple parts of a program.

A pure alternative returns a new list:

```python
def add_greeting(messages, name):
    return messages + [f"Hello, {name}!"]

my_messages = ["Welcome"]
result = add_greeting(my_messages, "Alice")
print(my_messages)  # ['Welcome'] --- unchanged
print(result)       # ['Welcome', 'Hello, Alice!']
```

### Modifying Global Variables

Functions that read or write global variables create dependencies that are invisible from the function's signature.

```python
counter = 0

def increment():
    global counter
    counter += 1

increment()
increment()
print(counter)  # 2
```

The function `increment` has no parameters and returns nothing. Its entire purpose is a side effect. Anyone reading a call to `increment()` must know about the global `counter` to understand what happens. If multiple functions modify `counter`, tracking its value requires reading the entire program.

A pure alternative makes the state explicit:

```python
def increment(counter):
    return counter + 1

counter = 0
counter = increment(counter)
counter = increment(counter)
print(counter)  # 2
```

Now the data flow is visible: `counter` goes in, a new value comes out.

### I/O Operations

Any interaction with the outside world---printing to the screen, reading from a file, sending a network request, writing to a database---is a side effect.

```python
def save_report(filename, data):
    with open(filename, "w") as f:
        f.write(data)
```

This function creates or overwrites a file on disk. Calling it twice with the same arguments does not just return the same result; it writes to the filesystem twice. The function's behavior depends on (and changes) the external world.

```python
def get_user_input():
    return input("Enter your name: ")
```

This function is impure in two ways: it performs I/O (printing a prompt and reading from the keyboard), and its return value depends on what the user types---not on any argument.

### Raising Exceptions as Side Effects

Raising an exception is a form of side effect because it alters the normal flow of the program in a way that is not captured by the return value.

```python
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

The function's return type suggests it produces a number, but it can also raise an exception. Callers must handle this possibility or risk a crash. This is a necessary side effect in many cases, but it should be documented.

## Why Side Effects Make Code Harder to Reason About

Consider this debugging scenario:

```python
def process_order(order, inventory):
    validate_order(order)
    apply_discount(order)
    update_inventory(order, inventory)
    send_confirmation(order)
    return order
```

When something goes wrong, you cannot look at `process_order` in isolation. Each helper function might modify `order`, `inventory`, or external systems. To understand the state at any point, you must trace through every preceding function call and know what each one mutates.

Compare this with a version that minimizes side effects:

```python
def process_order(order, inventory):
    validated = validate_order(order)
    discounted = apply_discount(validated)
    new_inventory = update_inventory(discounted, inventory)
    send_confirmation(discounted)  # I/O is unavoidable here
    return discounted, new_inventory
```

Now `order` and `inventory` are never mutated. Each step produces a new value, making the data flow explicit. Only `send_confirmation` has a side effect, and it is isolated at the end.

## When Side Effects Are Necessary

Side effects are not inherently bad---they are unavoidable for any program that interacts with the real world. A program that performs no I/O, modifies no files, and displays nothing is useless.

The goal is not to eliminate side effects entirely but to **control and isolate** them.

**Legitimate uses of side effects:**

- **I/O**: reading input, displaying output, writing files, making network requests. These are the program's interface to the outside world.
- **Logging**: recording what the program does for debugging and monitoring.
- **Caching**: storing computed results to avoid redundant work (e.g., `functools.lru_cache` maintains an internal dictionary).
- **Database operations**: persisting and retrieving data.

The key principle is that these side effects should be **deliberate, documented, and concentrated** in specific parts of the code rather than scattered throughout.

## Minimizing Unintended Side Effects

Several practical techniques help reduce accidental side effects.

**Return new values instead of mutating arguments.**

```python
# Instead of this (mutates the input):
def sort_names(names):
    names.sort()

# Do this (returns a new sorted list):
def sort_names(names):
    return sorted(names)
```

**Copy mutable arguments if mutation is needed internally.**

```python
def remove_duplicates(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result  # original `items` is untouched
```

**Avoid global variables.** Pass values as arguments and return results instead.

```python
# Instead of this:
config = {}

def load_config():
    global config
    config = {"debug": True}

# Do this:
def load_config():
    return {"debug": True}

config = load_config()
```

---

## Exercises

**Exercise 1.**
The following function has a subtle side effect. Identify it, explain why it could cause problems, and rewrite the function to be pure.

```python
def extend_with_defaults(user_settings, defaults):
    for key, value in defaults.items():
        if key not in user_settings:
            user_settings[key] = value
    return user_settings
```

What happens if two different parts of the program call this function with the same `user_settings` dictionary?

??? success "Solution to Exercise 1"
    The side effect is that the function modifies the `user_settings` dictionary in place. Even though it also returns the dictionary, the original object passed by the caller is mutated.

    If two different parts of the program share the same `user_settings` dictionary and call this function with different `defaults`, they will interfere with each other. The first call adds keys that the second caller did not expect, and vice versa.

    A pure version creates a new dictionary:

    ```python
    def extend_with_defaults(user_settings, defaults):
        result = dict(defaults)      # start with defaults
        result.update(user_settings) # user settings override defaults
        return result
    ```

    Or equivalently using dictionary unpacking:

    ```python
    def extend_with_defaults(user_settings, defaults):
        return {**defaults, **user_settings}
    ```

    Now `user_settings` is never modified, and each caller gets an independent result.

---

**Exercise 2.**
Classify each of the following operations as "side effect" or "no side effect." For each side effect, name the category (mutation, global state, I/O, or exception).

```python
# (a)
result = [x ** 2 for x in range(10)]

# (b)
print("Processing complete")

# (c)
my_list = [3, 1, 2]
my_list.sort()

# (d)
import json
data = json.dumps({"key": "value"})

# (e)
with open("log.txt", "a") as f:
    f.write("entry\n")

# (f)
scores = {"alice": 90}
scores["bob"] = 85
```

??? success "Solution to Exercise 2"

    - **(a) No side effect.** The list comprehension creates a new list and assigns it to a local variable. No existing data is changed.

    - **(b) Side effect: I/O.** `print()` writes to standard output, which is an interaction with the outside world.

    - **(c) Side effect: mutation.** `my_list.sort()` modifies the list in place rather than returning a new sorted list.

    - **(d) No side effect.** `json.dumps()` takes a dictionary and returns a new string. It does not modify the input or perform I/O.

    - **(e) Side effect: I/O.** Writing to a file changes the state of the filesystem.

    - **(f) Side effect: mutation.** Adding a key to `scores` modifies the existing dictionary. Whether this is a *problem* depends on context---if `scores` is shared with other code, the mutation could cause surprises. If it is purely local, the mutation is contained.

---

**Exercise 3.**
Refactor the following code so that the computation is pure and the side effects are isolated. The program should produce the same output.

```python
results = []

def process_numbers(numbers):
    for n in numbers:
        if n > 0:
            results.append(n ** 2)
    print(f"Processed {len(results)} numbers")

process_numbers([3, -1, 4, -5, 2])
print(results)
```

??? success "Solution to Exercise 3"
    Separate the pure computation from the side effects:

    ```python
    # Pure function: no globals, no mutation, no I/O
    def square_positives(numbers):
        return [n ** 2 for n in numbers if n > 0]

    # Side effects isolated here, at the top level
    results = square_positives([3, -1, 4, -5, 2])
    print(f"Processed {len(results)} numbers")
    print(results)
    ```

    Output (same as the original):

    ```text
    Processed 3 numbers
    [9, 16, 4]
    ```

    The pure function `square_positives` does not touch any global variable, does not mutate its input, and does not perform I/O. All side effects (assigning to a module-level variable and printing) happen in the top-level code, where they are easy to see and control.

Next: [Designing Predictable Functions](design_guidelines.md).
