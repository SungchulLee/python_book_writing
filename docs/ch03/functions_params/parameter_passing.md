# Parameter Passing

This page builds on [Call-by-Object-Reference](call_by_object_reference.md) with practical guidance on how arguments flow from caller to function.

!!! tip "Mental Model"
    Calling a function is like filling out a form. Positional arguments fill fields left to right, keyword arguments fill fields by name, and defaults pre-fill any field you skip. Once you switch to keyword mode, you cannot go back to positional -- this rule keeps call sites unambiguous.

## Positional and Keyword Arguments

A function can receive arguments by position, by name, or by a mix of both.

```python
def describe(name, age):
    print(name, age)

describe("Alice", 25)              # positional
describe(name="Alice", age=25)     # keyword
describe("Alice", age=25)          # mixed: positional then keyword
describe(age=25, name="Alice")     # keyword order doesn't matter
```

Positional arguments are matched left to right. Once you use a keyword argument, every argument after it must also be a keyword.

```python
# SyntaxError: positional argument follows keyword argument
describe(name="Alice", 25)
```

### Unpacking Arguments

The `*` and `**` operators unpack sequences and mappings into positional and keyword arguments.

```python
args = ("Alice", 25)
describe(*args)                         # same as describe("Alice", 25)

kwargs = {"age": 25, "name": "Alice"}
describe(**kwargs)                      # same as describe(age=25, name="Alice")
```

## Passing Immutable Objects

When you pass an immutable object (int, str, tuple), the function cannot modify the original. Any operation that appears to change the value creates a new object and rebinds the local name.

```python
def try_modify(text: str) -> str:
    text = text.upper()  # Creates a new string, rebinds the local variable
    return text

original = "hello"
result = try_modify(original)

print(original)  # hello
print(result)    # HELLO
```

`text.upper()` creates a new string object. The assignment `text = ...` rebinds the local name `text` inside the function — it does not touch the caller's `original`.

The same pattern holds for integers, floats, and tuples — every "modification" is actually a creation of a new object followed by a rebinding.

```python
def increment(n: int) -> int:
    n = n + 1  # New int object; the caller's variable is untouched
    return n

x = 5
y = increment(x)
print(x)  # 5  — unchanged
print(y)  # 6
```

## Passing Mutable Objects

When you pass a mutable object (list, dict, set), the function can modify the original.

```python
def add_item(collection: list, item: int) -> None:
    collection.append(item)  # Mutates the same object

my_list = [1, 2, 3]
add_item(my_list, 4)

print(my_list)  # [1, 2, 3, 4]
```

`collection` and `my_list` point to the same list object. `append()` mutates that object in place.

## Rebinding vs Mutating

The critical distinction is between **rebinding** a name and **mutating** an object.

```
# Initial state
my_list ──────► [1, 2, 3]

# After passing to function
my_list ──────► [1, 2, 3] ◄────── lst (parameter)

# After lst.append(4)  — MUTATION: same object, caller sees the change
my_list ──────► [1, 2, 3, 4] ◄────── lst

# After lst = [100, 200]  — REBINDING: lst points to a new object
my_list ──────► [1, 2, 3, 4]
lst     ──────► [100, 200]
```

Rebinding a parameter never affects the caller. Mutating a mutable object always does.

```python
def rebind(lst: list) -> None:
    lst = [100, 200, 300]  # Only rebinds the local name
    print("inside:", lst)

def mutate(lst: list) -> None:
    lst[0] = 100           # Modifies the same object
    print("inside:", lst)

my_list = [1, 2, 3]

rebind(my_list)
print("after rebind:", my_list)   # [1, 2, 3]  — unchanged

mutate(my_list)
print("after mutate:", my_list)   # [100, 2, 3]  — changed
```

Output

```text
inside: [100, 200, 300]
after rebind: [1, 2, 3]
inside: [100, 2, 3]
after mutate: [100, 2, 3]
```

## Containers with Mixed Mutability

A tuple is immutable, but if it contains a mutable element, that inner element can still be mutated.

```python
record = ("Alice", [90, 85, 92])

record[1].append(88)       # Mutates the list inside the tuple
print(record)              # ('Alice', [90, 85, 92, 88])

record[0] = "Bob"          # TypeError: 'tuple' object does not support item assignment
```

The tuple itself cannot gain or lose elements, nor can its slots be reassigned. But the list at `record[1]` is a separate mutable object — the tuple merely holds a reference to it.

```python
def add_score(student: tuple, score: int) -> None:
    student[1].append(score)  # Mutates the list inside the tuple

record = ("Alice", [90, 85])
add_score(record, 95)
print(record)  # ('Alice', [90, 85, 95])
```

The identity of the inner list never changes:

```python
record = ("Alice", [])
original_id = id(record[1])

for i in range(1000):
    record[1].append(i)

print(id(record[1]) == original_id)  # True — same list object throughout
```

## Defensive Copying

When a function should not modify its input, work on a copy instead.

```python
def calculate_stats(numbers: list) -> tuple:
    sorted_nums = sorted(numbers)  # Creates a new list; original untouched
    return sorted_nums[0], sorted_nums[-1]

data = [3, 1, 4, 1, 5]
low, high = calculate_stats(data)

print(data)        # [3, 1, 4, 1, 5]  — original order preserved
print(low, high)   # 1 5
```

For nested structures (lists of lists, dicts containing lists), a shallow copy is not enough — use `copy.deepcopy` from the standard library. That pattern is covered in the data structures chapter.

## Type Hints Signal Intent

Return type annotations communicate whether a function mutates its argument or produces a new value.

```python
def sort_in_place(items: list) -> None:
    """Mutates the caller's list."""
    items.sort()

def sorted_copy(items: list) -> list:
    """Returns a new sorted list; original unchanged."""
    return sorted(items)
```

`-> None` signals that the function works by side effect — it modifies the argument in place. A return type like `-> list` signals that the caller gets a new object back and the input is left alone.

## Common Mistakes

### Mistake 1: Expecting a function to modify an immutable argument

```python
def increment(n: int) -> None:
    n += 1  # Rebinds local n; caller's variable is unaffected

x = 5
increment(x)
print(x)  # 5  — unchanged

# Fix: return the new value and reassign
def increment(n: int) -> int:
    return n + 1

x = increment(x)
print(x)  # 6
```

### Mistake 2: Accidentally mutating a mutable argument

```python
def calculate_stats(numbers: list) -> tuple:
    numbers.sort()  # Modifies the caller's list!
    return numbers[0], numbers[-1]

data = [3, 1, 4, 1, 5]
low, high = calculate_stats(data)
print(data)  # [1, 1, 3, 4, 5]  — original order destroyed

# Fix: use sorted() which returns a new list
def calculate_stats(numbers: list) -> tuple:
    s = sorted(numbers)
    return s[0], s[-1]
```

## Key Ideas

- Immutable arguments cannot be changed by a function — any assignment inside the function rebinds a local name and leaves the caller's variable untouched.
- Mutable arguments can be changed if the function mutates the object rather than rebinding the name.
- A tuple holding a mutable element (such as a list) allows mutation of that inner element even though the tuple itself is immutable.
- Use `-> None` to signal in-place mutation and a return type to signal a new object is produced.
- When in doubt, use `sorted()`, `.copy()`, or similar non-mutating alternatives to protect the caller's data.

Next: [Default Parameter Gotcha](default_parameter_gotcha.md).

---

## Exercises


**Exercise 1.**
Write a function `swap(a, b)` that attempts to swap two integers. Explain why the swap is not visible to the caller. Then write a version using a list to achieve a visible swap.

??? success "Solution to Exercise 1"

        ```python
        def swap(a, b):
            a, b = b, a  # Only swaps local names

        x, y = 1, 2
        swap(x, y)
        print(x, y)  # 1 2 (unchanged)

        # Visible swap using a list
        def swap_list(pair):
            pair[0], pair[1] = pair[1], pair[0]

        pair = [1, 2]
        swap_list(pair)
        print(pair)  # [2, 1]
        ```

    Integers are immutable. `swap` only rebinds local names. The list version works because it mutates the mutable container.

---

**Exercise 2.**
Write a function `extend_and_return(lst, items)` that extends `lst` with `items` and returns the modified list. Show that the caller's list is also modified. Then write a version that does not modify the original.

??? success "Solution to Exercise 2"

        ```python
        # Modifies original
        def extend_and_return(lst, items):
            lst.extend(items)
            return lst

        a = [1, 2]
        b = extend_and_return(a, [3, 4])
        print(a)  # [1, 2, 3, 4] (modified)

        # Does not modify original
        def extend_copy(lst, items):
            return lst + items

        c = [1, 2]
        d = extend_copy(c, [3, 4])
        print(c)  # [1, 2] (unchanged)
        print(d)  # [1, 2, 3, 4]
        ```

    `lst.extend(items)` mutates the list. `lst + items` creates a new list.

---

**Exercise 3.**
Given `def f(x): x = x + [4]` and `def g(x): x += [4]`, explain why `f` and `g` behave differently when passed a list. Demonstrate with code.

??? success "Solution to Exercise 3"

        ```python
        def f(x):
            x = x + [4]  # Rebinds x to new list

        def g(x):
            x += [4]     # Calls x.__iadd__([4]) -> mutates in place

        a = [1, 2, 3]
        f(a)
        print(a)  # [1, 2, 3] (unchanged)

        b = [1, 2, 3]
        g(b)
        print(b)  # [1, 2, 3, 4] (modified)
        ```

    `x = x + [4]` creates a new list and rebinds the local `x`. `x += [4]` calls `list.__iadd__`, which extends the list in place.
