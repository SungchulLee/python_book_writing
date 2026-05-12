

# Assignment vs Mutation

## The Mental Model

Every operation in Python does one of two things to a name-object relationship:

- **Rebinding** changes which object a name refers to.
- **Mutation** changes the object itself, leaving all name bindings intact.

Picture a sticky note (the name) attached to a box (the object). Rebinding
peels the sticky note off one box and sticks it onto a different box. Mutation
opens the box and rearranges its contents. Every other sticky note attached to
that same box will see the changed contents.

Confusing these two operations is the single most common source of bugs
involving shared references in Python.

---

## Rebinding: Changing What a Name Refers To

Any statement that uses `=` to assign a name is a **rebinding** operation.
After rebinding, the name points to a different object:

```python
x = [1, 2, 3]
print(id(x))  # e.g. 140234866203200

x = [4, 5, 6]
print(id(x))  # different id -- x now refers to a new list
```

The original list `[1, 2, 3]` is unaffected. If another name was pointing to
it, that name still sees the original:

```python
x = [1, 2, 3]
y = x          # y and x refer to the same list

x = [4, 5, 6]  # rebind x to a new list
print(y)       # [1, 2, 3] -- y is unaffected
```

Common rebinding operations:

```python
x = value           # simple assignment
x = x + something   # compute new object, rebind
x, y = y, x         # simultaneous rebinding
```

---

## Mutation: Changing the Object Itself

Mutation modifies an object **in place**. The name still refers to the same
object, but the object's contents have changed:

```python
x = [1, 2, 3]
print(id(x))  # e.g. 140234866203200

x.append(4)
print(id(x))  # same id -- same object, modified in place
print(x)      # [1, 2, 3, 4]
```

Because `y` and `x` share the same object, `y` sees the mutation:

```python
x = [1, 2, 3]
y = x

x.append(4)
print(y)  # [1, 2, 3, 4] -- y sees the change
```

Common mutating operations on lists:

```python
x.append(item)       # add one item
x.extend(iterable)   # add multiple items
x.insert(i, item)    # insert at index
x.pop()              # remove and return last item
x.remove(item)       # remove first occurrence
x.sort()             # sort in place
x.reverse()          # reverse in place
x[i] = new_value     # replace element at index
del x[i]             # remove element at index
x.clear()            # remove all elements
```

Common mutating operations on dictionaries:

```python
d[key] = value       # add or update entry
d.update(other)      # merge another dict in place
d.pop(key)           # remove and return value
del d[key]           # remove entry
d.clear()            # remove all entries
```

---

## Side-by-Side Comparison

The following example highlights the difference with identical starting
conditions:

```python
# Setup
a = [1, 2, 3]
b = a

# Rebinding a
a = a + [4]
print(f"a = {a}")        # [1, 2, 3, 4]
print(f"b = {b}")        # [1, 2, 3]
print(f"a is b: {a is b}")  # False
```

```python
# Setup
a = [1, 2, 3]
b = a

# Mutating through a
a.append(4)
print(f"a = {a}")        # [1, 2, 3, 4]
print(f"b = {b}")        # [1, 2, 3, 4]
print(f"a is b: {a is b}")  # True
```

Both produce a list `[1, 2, 3, 4]` accessible through `a`, but only mutation
causes `b` to see the change.

---

## Why This Matters for Shared References

Whenever two or more names refer to the same mutable object, mutation through
one name is visible through all of them. This arises in several common
scenarios.

### Function arguments

```python
def add_item(lst, item):
    lst.append(item)  # mutates the caller's list

shopping = ["milk", "eggs"]
add_item(shopping, "bread")
print(shopping)  # ["milk", "eggs", "bread"]
```

The parameter `lst` and the argument `shopping` refer to the same list object.
The `append` call mutates it, and the change is visible outside the function.

Contrast with rebinding inside a function:

```python
def replace_list(lst):
    lst = [10, 20, 30]  # rebinds the local name lst; does NOT affect caller

data = [1, 2, 3]
replace_list(data)
print(data)  # [1, 2, 3] -- unchanged
```

### Default mutable arguments

```python
def append_to(item, target=[]):
    target.append(item)  # mutates the default list object
    return target

print(append_to(1))  # [1]
print(append_to(2))  # [1, 2] -- the same default list is reused!
```

The default list is created once when the function is defined. Each call
mutates the **same** object. The standard fix is to use `None` as the default:

```python
def append_to(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target
```

### Nested data structures

```python
row = [0, 0, 0]
grid = [row, row, row]  # three references to the same list

grid[0][1] = 5
print(grid)  # [[0, 5, 0], [0, 5, 0], [0, 5, 0]]
```

Mutating through `grid[0]` affects all three rows because they are the same
object. The fix is to create independent lists:

```python
grid = [[0, 0, 0] for _ in range(3)]
grid[0][1] = 5
print(grid)  # [[0, 5, 0], [0, 0, 0], [0, 0, 0]]
```

---

## How to Tell Whether an Operation Mutates

There is no single syntax rule, but reliable guidelines exist:

| Pattern | Usually means | Examples |
| --- | --- | --- |
| `name = ...` | Rebinding | `x = x + 1`, `x = []` |
| `name.method(...)` | Check the docs -- many methods mutate | `x.append(1)`, `x.sort()` |
| `name[index] = ...` | Mutation (item assignment) | `x[0] = 99` |
| `del name[index]` | Mutation (item deletion) | `del x[0]` |

A useful heuristic: **methods that return `None` usually mutate in place**.
Methods that return a new object usually do not.

```python
data = [3, 1, 2]

result = data.sort()
print(result)  # None -- sort() mutated data in place
print(data)    # [1, 2, 3]

data = [3, 1, 2]
result = sorted(data)
print(result)  # [1, 2, 3] -- sorted() returns a new list
print(data)    # [3, 1, 2] -- original unchanged
```

!!! note "Immutable objects cannot be mutated"
    Strings, integers, floats, tuples, and frozensets are immutable. Any
    operation that appears to modify them actually creates a new object and
    rebinds the name. For example, `s = s.upper()` creates a new string; the
    original string is not changed.

---

## The Rebinding Test

When you are unsure whether an operation rebinds or mutates, check the object
identity before and after:

```python
x = [1, 2, 3]
before = id(x)

x.append(4)       # mutation
print(id(x) == before)  # True -- same object

x = x + [5]       # rebinding
print(id(x) == before)  # False -- different object
```

If `id()` stays the same, the object was mutated. If it changes, the name was
rebound to a new object.

---

## Summary

| Operation | What changes | Effect on shared references |
| --- | --- | --- |
| Rebinding (`x = new_value`) | The name-object binding | Other names that referred to the old object are unaffected |
| Mutation (`x.append(item)`) | The object's internal state | All names that refer to the same object see the change |

The rule is simple: **rebinding is private to the name; mutation is shared
across all references to the object.**

---

## Exercises

**Exercise 1.**
A student writes the following function and is surprised by the output.
Explain what happens and fix the function so that it returns a new list without
modifying the original.

```python
def double_values(numbers):
    for i in range(len(numbers)):
        numbers[i] = numbers[i] * 2
    return numbers

original = [1, 2, 3]
doubled = double_values(original)
print(doubled)    # [2, 4, 6]
print(original)   # [2, 4, 6] -- the student expected [1, 2, 3]
```

??? success "Solution to Exercise 1"
    The function mutates the list passed in. The item assignment
    `numbers[i] = numbers[i] * 2` changes the object in place. Since
    `numbers` and `original` refer to the same list, the caller's list is
    modified.

    **Fix -- create a new list instead of mutating:**

    ```python
    def double_values(numbers):
        return [n * 2 for n in numbers]

    original = [1, 2, 3]
    doubled = double_values(original)
    print(doubled)    # [2, 4, 6]
    print(original)   # [1, 2, 3] -- unchanged
    ```

    The list comprehension builds a brand-new list. The parameter `numbers`
    is never mutated, so the original list is preserved. This is the preferred
    approach when a function should produce a result without side effects.

---

**Exercise 2.**
For each of the following operations, state whether it is a rebinding or a
mutation. Justify each answer.

```python
a = [1, 2, 3]

# Operation 1
a.reverse()

# Operation 2
a = list(reversed(a))

# Operation 3
a += [4]

# Operation 4
a = a + [5]

# Operation 5
a[0] = 99
```

??? success "Solution to Exercise 2"

    1. **`a.reverse()`** -- **Mutation.** The `reverse()` method reverses the
       list in place and returns `None`. The object `a` refers to is modified;
       `id(a)` stays the same.

    2. **`a = list(reversed(a))`** -- **Rebinding.** `reversed(a)` returns an
       iterator, and `list(...)` creates a new list. The `=` then rebinds `a`
       to this new list. The original list is not modified.

    3. **`a += [4]`** -- **Both mutation and rebinding.** For lists, `+=` calls
       `__iadd__`, which extends the list in place (mutation) and then rebinds
       `a` to the same object. The `id` does not change, so the dominant effect
       is mutation. Any other name sharing the object will see `[4]` appended.

    4. **`a = a + [5]`** -- **Rebinding.** The `+` operator creates a new list
       by concatenation. The `=` rebinds `a` to the new list. The original list
       is not modified.

    5. **`a[0] = 99`** -- **Mutation.** Item assignment modifies the list
       object in place. The `id` stays the same, and all shared references see
       the change.

---

**Exercise 3.**
Explain why the following code produces unexpected output. Draw a diagram of
which names point to which objects after each line. Then rewrite the code so
that each row of the grid is an independent list.

```python
row = [0] * 4
grid = [row] * 3
grid[0][0] = 1
print(grid)
# Expected: [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
# Actual:   [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]]
```

??? success "Solution to Exercise 3"
    **What happens:**

    - `row = [0] * 4` creates a single list object `[0, 0, 0, 0]`.
    - `grid = [row] * 3` creates a list containing **three references to the
      same list object**. It does not create three independent lists.
    - `grid[0][0] = 1` is a mutation (item assignment). It modifies the one
      shared list object, changing its first element to `1`.
    - Since `grid[0]`, `grid[1]`, and `grid[2]` all refer to the same object,
      printing `grid` shows the change in every row.

    **Name-object diagram after `grid[0][0] = 1`:**

    ```text
    grid ──> [ ref, ref, ref ]
                │     │     │
                └─────┼─────┘
                      ▼
               [1, 0, 0, 0]   (one list object shared by all three slots)
    ```

    **Fix -- use a list comprehension to create independent lists:**

    ```python
    grid = [[0] * 4 for _ in range(3)]
    grid[0][0] = 1
    print(grid)
    # [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    ```

    The comprehension calls `[0] * 4` three separate times, creating three
    distinct list objects. Mutating one does not affect the others.
