
# Aliasing

In Python, variables are **names** that refer to objects, not containers that hold values. When two names refer to the **same object**, they are called **aliases**. This distinction is one of the most important mental models in Python: assignment does not copy data -- it creates a new reference to existing data.

Think of it this way: an object is a physical book sitting on a shelf. A variable is a sticky note with a name written on it, attached to the book. If you attach two sticky notes to the same book, you have two aliases. Anything you do to the book through one sticky note is visible through the other, because there is only one book.

!!! tip "Mental Model"
    Two variables are aliases when they point to the same object, not merely to equal values. Mutating through one alias changes what every alias sees, because there is only one underlying object. Recognizing aliasing is the key to predicting when a change in one part of your code unexpectedly appears somewhere else.

---

## 1. Creating Aliases with Assignment

Simple assignment creates an alias, not a copy.

```python
a = [1, 2, 3]
b = a

print(a is b)
print(id(a) == id(b))
```

Output:

```text
True
True
```

Both `a` and `b` refer to the same list object. A mutation through one name is visible through the other:

```python
a = [1, 2, 3]
b = a

b.append(4)
print(a)
print(b)
```

Output:

```text
[1, 2, 3, 4]
[1, 2, 3, 4]
```

There is only one list in memory. Both names see the change because they point to the same object.

This applies to all mutable objects -- lists, dictionaries, sets, and user-defined objects:

```python
d1 = {"name": "Alice", "scores": [90, 85]}
d2 = d1

d2["name"] = "Bob"
print(d1["name"])
```

Output:

```text
Bob
```

---

## 2. When Aliasing Does Not Cause Surprises

Aliasing is only observable with **mutable** objects. Immutable objects (integers, strings, tuples of immutables) cannot be changed in place, so aliasing has no practical effect:

```python
a = 42
b = a

b = b + 1
print(a)
print(b)
```

Output:

```text
42
43
```

The operation `b + 1` creates a **new** integer object and rebinds `b` to it. The original object (`42`) is untouched, and `a` still refers to it. Rebinding is not mutation.

---

## 3. Aliasing in Function Arguments

When you pass a mutable object to a function, the parameter becomes an alias of the argument. This means the function can mutate the caller's object:

```python
def add_element(lst, element):
    lst.append(element)

my_list = [1, 2, 3]
add_element(my_list, 4)
print(my_list)
```

Output:

```text
[1, 2, 3, 4]
```

Inside the function, `lst` is an alias for `my_list`. The `append` call mutates the shared object. This behavior is called **pass-by-object-reference** -- Python does not copy the object, nor does it pass the variable itself. It passes a reference to the same object.

However, **rebinding** the parameter inside the function does not affect the caller:

```python
def try_replace(lst):
    lst = [10, 20, 30]
    print("Inside:", lst)

my_list = [1, 2, 3]
try_replace(my_list)
print("Outside:", my_list)
```

Output:

```text
Inside: [10, 20, 30]
Outside: [1, 2, 3]
```

The assignment `lst = [10, 20, 30]` rebinds the local name `lst` to a new object. It does not affect the object that `my_list` refers to.

---

## 4. Shallow Copy

A **shallow copy** creates a new container object but fills it with references to the same child objects. The top-level structure is independent, but nested objects are still shared.

### Using `copy.copy()`

```python
import copy

original = [1, [2, 3], [4, 5]]
shallow = copy.copy(original)

print(original is shallow)
print(original[1] is shallow[1])
```

Output:

```text
False
True
```

The outer lists are different objects, but the inner lists are shared.

### Using List Slicing

Slicing a list produces a shallow copy:

```python
original = [1, [2, 3], [4, 5]]
shallow = original[:]

print(original is shallow)
print(original[1] is shallow[1])
```

Output:

```text
False
True
```

The same result -- a new outer list, but shared inner lists.

### Other shallow copy methods

```python
# list constructor
shallow = list(original)

# .copy() method
shallow = original.copy()
```

All of these produce shallow copies with the same aliasing behavior for nested objects.

### The danger of shallow copies

Because nested objects are shared, mutating them through one copy affects the other:

```python
import copy

original = [1, [2, 3], [4, 5]]
shallow = copy.copy(original)

shallow[1].append(99)
print(original)
print(shallow)
```

Output:

```text
[1, [2, 3, 99], [4, 5]]
[1, [2, 3, 99], [4, 5]]
```

The inner list `[2, 3]` is the same object in both structures. Appending `99` through `shallow` is visible in `original`.

However, replacing a top-level element does not affect the other copy:

```python
shallow[0] = 999
print(original[0])
print(shallow[0])
```

Output:

```text
1
999
```

---

## 5. Deep Copy

A **deep copy** recursively copies every object in the structure, creating fully independent clones at every level.

```python
import copy

original = [1, [2, 3], [4, 5]]
deep = copy.deepcopy(original)

print(original is deep)
print(original[1] is deep[1])
```

Output:

```text
False
False
```

Now even the nested lists are separate objects. Mutations through one are invisible to the other:

```python
import copy

original = [1, [2, 3], [4, 5]]
deep = copy.deepcopy(original)

deep[1].append(99)
print(original)
print(deep)
```

Output:

```text
[1, [2, 3], [4, 5]]
[1, [2, 3, 99], [4, 5]]
```

The two structures are completely independent.

### When to use each

| Situation | Use |
| --------- | --- |
| No nested mutables | Shallow copy is sufficient |
| Nested mutable objects | Deep copy for full independence |
| Read-only access | Aliasing (no copy needed) |
| Large data structures | Consider whether a copy is truly necessary |

---

## 6. Summary

Key ideas:

- Assignment creates aliases, not copies. Both names refer to the same object.
- Aliasing is only observable through mutation of mutable objects. Immutable objects are unaffected in practice.
- Function arguments are aliases of the caller's objects. Mutation inside the function is visible outside; rebinding is not.
- Shallow copies (`copy.copy`, slicing, `.copy()`) create a new container but share nested objects.
- Deep copies (`copy.deepcopy`) recursively duplicate the entire structure.
- Choose the right level of copying based on whether nested objects are mutable and whether independence is required.


## Exercises

**Exercise 1.**
Predict the output of the following code. Trace through each line, noting when `a` and `b` refer to the same object and when they do not.

```python
a = [1, 2, 3]
b = a
b.append(4)
print("Step 1:", a, b)

b = [1, 2, 3, 4, 5]
print("Step 2:", a, b)

a.append(6)
print("Step 3:", a, b)
```

??? success "Solution to Exercise 1"
    ```text
    Step 1: [1, 2, 3, 4] [1, 2, 3, 4]
    Step 2: [1, 2, 3, 4] [1, 2, 3, 4, 5]
    Step 3: [1, 2, 3, 4, 6] [1, 2, 3, 4, 5]
    ```

    **Step 1**: `b = a` makes `b` an alias of `a`. They refer to the same list. `b.append(4)` mutates that shared list. Both names see `[1, 2, 3, 4]`.

    **Step 2**: `b = [1, 2, 3, 4, 5]` **rebinds** `b` to a brand-new list. This does not affect `a`. Now `a` still points to the original list `[1, 2, 3, 4]`, and `b` points to a new list `[1, 2, 3, 4, 5]`. They are no longer aliases.

    **Step 3**: `a.append(6)` mutates the list `a` refers to. Since `b` now refers to a different object, `b` is unaffected.

    The critical insight is the difference between **mutation** (`b.append(4)`, which changes the shared object) and **rebinding** (`b = [...]`, which makes `b` point to a new object).

---

**Exercise 2.**
A function receives a list and is supposed to return a sorted version without modifying the original. Identify the bug in the following code, explain why it fails, and provide a corrected version.

```python
def sorted_copy(data):
    result = data
    result.sort()
    return result

numbers = [3, 1, 4, 1, 5]
ordered = sorted_copy(numbers)
print("Original:", numbers)
print("Sorted:", ordered)
```

??? success "Solution to Exercise 2"
    The bug is on the line `result = data`. This creates an alias, not a copy. When `result.sort()` is called, it sorts the list in place -- but `result` and `data` (and `numbers` in the caller) all refer to the same list. The original is destroyed.

    Output of the buggy code:

    ```text
    Original: [1, 1, 3, 4, 5]
    Sorted: [1, 1, 3, 4, 5]
    ```

    Both print the sorted version because there is only one list.

    Corrected version using a shallow copy:

    ```python
    def sorted_copy(data):
        result = data[:]   # or data.copy() or list(data)
        result.sort()
        return result

    numbers = [3, 1, 4, 1, 5]
    ordered = sorted_copy(numbers)
    print("Original:", numbers)   # [3, 1, 4, 1, 5]
    print("Sorted:", ordered)     # [1, 1, 3, 4, 5]
    ```

    Alternatively, use the built-in `sorted()` function, which always returns a new list:

    ```python
    def sorted_copy(data):
        return sorted(data)
    ```

    A shallow copy is sufficient here because the list contains integers (immutable), so there are no nested mutable objects to worry about.

---

**Exercise 3.**
Consider the following nested structure. Predict the output and explain the difference between shallow and deep copy behavior.

```python
import copy

matrix = [[1, 2], [3, 4]]
shallow = copy.copy(matrix)
deep = copy.deepcopy(matrix)

matrix[0][0] = 99

print("Original:", matrix)
print("Shallow:", shallow)
print("Deep:", deep)
```

??? success "Solution to Exercise 3"
    ```text
    Original: [[99, 2], [3, 4]]
    Shallow: [[99, 2], [3, 4]]
    Deep: [[1, 2], [3, 4]]
    ```

    `matrix[0][0] = 99` modifies the inner list `[1, 2]` -- specifically, it replaces the first element of that inner list object.

    **Shallow copy**: `copy.copy(matrix)` created a new outer list, but the inner lists `[1, 2]` and `[3, 4]` are shared between `matrix` and `shallow`. Since `matrix[0]` and `shallow[0]` refer to the same inner list object, the change to `matrix[0][0]` is visible through `shallow[0][0]`.

    **Deep copy**: `copy.deepcopy(matrix)` recursively copied every object. The inner lists in `deep` are independent copies. The change to `matrix[0][0]` has no effect on `deep`.

    To verify the sharing:

    ```python
    print(matrix[0] is shallow[0])  # True -- shared inner list
    print(matrix[0] is deep[0])     # False -- independent copy
    ```

    This demonstrates why deep copy is necessary when working with nested mutable structures where modifications to the original must not propagate to the copy.
