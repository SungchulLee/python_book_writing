# Immutable vs Mutable

!!! tip "Mental Model"
    Immutable objects are like printed pages -- once created, their content cannot change, so any "modification" produces a brand-new page. Mutable objects are like whiteboards -- you can erase and rewrite freely, and everyone looking at the same whiteboard sees the update instantly.

## Immutable Objects

### 1. Cannot Change

```python
x = 42
s = "hello"
t = (1, 2, 3)

# Cannot modify
# s[0] = "H"        # TypeError
```

### 2. Create New

```python
x = 42
x = x + 1           # New object

s = "hello"
s = s + " world"    # New string
```

## Mutable Objects

### 1. Can Change

```python
lst = [1, 2, 3]
d = {'a': 1}
s = {1, 2, 3}

# Can modify
lst[0] = 100
d['b'] = 2
s.add(4)
```

### 2. Same Object

```python
lst = [1, 2, 3]
original_id = id(lst)

lst.append(4)
print(id(lst) == original_id)  # True
```

### 3. Reference Sharing

When two names point to the same mutable object:

```python
a = [1, 2, 3]
b = a
a.append(4)
print(b)  # [1, 2, 3, 4]
```

```
Before:
a ─┬──► [1, 2, 3]
   │
b ─┘

After a.append(4):
a ─┬──► [1, 2, 3, 4]
   │
b ─┘
```

### 4. Immutable Rebinding

```python
a = 10
b = a
b += 1
print(a)  # 10 (unchanged)
```

```
Before:
a ─┬──► 10
   │
b ─┘

After b += 1:
a ───► 10

b ───► 11  (new object)
```

## Type Classification

### 1. Immutable

- int, float, str
- tuple, frozenset
- bytes, bool, None

### 2. Mutable

- list, dict, set
- bytearray
- User classes

## Hashability

### 1. Immutable Hashable

```python
d = {42: "int", "key": "str"}
s = {1, "two", (3, 4)}
```

### 2. Mutable Unhashable

```python
# Cannot use as dict key
# d[[1, 2]] = "bad"  # TypeError
```

### 3. Shallow Immutability

Tuples containing mutable objects are **not hashable**:

```python
t = (1, [2, 3])      # Tuple with list inside
hash(t)              # TypeError: unhashable type: 'list'
```

The tuple is immutable (can't reassign `t[1]`), but the list inside can change.


## Operations That Create New Objects

Even with mutable types, some operations create new objects:

```python
lst = [1, 2, 3]
print(id(lst))

# In-place (same object)
lst.append(4)
lst.sort()
print(id(lst))       # Same id

# Creates new object
lst = lst + [5]
print(id(lst))       # Different id!

lst = sorted(lst)
print(id(lst))       # Different id!

lst = [x for x in lst]
print(id(lst))       # Different id!
```

| Operation | Same Object? |
|-----------|--------------|
| `lst.append(x)` | ✅ Yes |
| `lst.sort()` | ✅ Yes |
| `lst += [x]` | ✅ Yes |
| `lst = lst + [x]` | ❌ No |
| `lst = sorted(lst)` | ❌ No |
| `lst = [x for x in lst]` | ❌ No |

## Default Arguments

### 1. Dangerous

```python
def bad(item, lst=[]):
    lst.append(item)
    return lst

print(bad(1))       # [1]
print(bad(2))       # [1, 2]  # Bug!
```

### 2. Safe

```python
def good(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```


## Summary

| Aspect | Immutable | Mutable |
|--------|-----------|---------|
| Change | No | Yes |
| Operations | New object | In-place |
| Hashable | Yes | No |
| Default arg | Safe | Danger |


## Exercises

**Exercise 1.**
Predict the output and explain each result:

```python
a = (1, [2, 3])
a[1].append(4)
print(a)

try:
    a[1] = [2, 3, 4]
except TypeError as e:
    print(e)
```

How can a "immutable" tuple be modified? Is this a contradiction? What exactly is immutable about a tuple?

??? success "Solution to Exercise 1"
    Output:

    ```text
    (1, [2, 3, 4])
    'tuple' object does not support item assignment
    ```

    This is NOT a contradiction. A tuple's immutability means its **structure** (the references it holds) cannot change -- you cannot make `a[0]` or `a[1]` point to different objects. But the objects those references point to may themselves be mutable.

    `a[1]` is a reference to a list object. `a[1].append(4)` mutates that list object -- it does not change the tuple's reference. The tuple still holds a reference to the same list; the list just has different contents.

    `a[1] = [2, 3, 4]` tries to change the tuple's reference at index 1 to point to a different object -- this IS a structural change to the tuple, which is forbidden.

    The key insight: immutability of a container constrains the **container's structure**, not the **contents of the objects it references**.

---

**Exercise 2.**
Consider augmented assignment with different types:

```python
a = [1, 2]
b = a
a += [3]
print(b)  # What?

x = (1, 2)
y = x
x += (3,)
print(y)  # What?
```

Predict the output. Why does `+=` behave differently for lists and tuples? What happens internally in each case?

??? success "Solution to Exercise 2"
    Output:

    ```text
    [1, 2, 3]
    (1, 2)
    ```

    For **lists** (mutable): `a += [3]` calls `a.__iadd__([3])`, which mutates the list in place and returns the same object. Since `b` is an alias for the same list, `b` sees the change.

    For **tuples** (immutable): `x += (3,)` calls `x.__iadd__((3,))`, but tuples cannot be mutated. Instead, `__iadd__` creates a **new tuple** `(1, 2, 3)` and rebinds `x` to it. `y` still refers to the original `(1, 2)`.

    The `+=` operator has **dual behavior**: for mutable types, it mutates in place (same object); for immutable types, it creates a new object and rebinds. This is why `+=` can be confusing -- its behavior depends on the type of the left operand.

---

**Exercise 3.**
Explain why mutable default arguments are dangerous using Python's object model. Trace what happens internally in this code:

```python
def append_to(item, lst=[]):
    lst.append(item)
    return lst

result1 = append_to(1)
result2 = append_to(2)
print(result1)
print(result2)
print(result1 is result2)
```

At what point in time is the default list created? How many list objects exist?

??? success "Solution to Exercise 3"
    Output:

    ```text
    [1, 2]
    [1, 2]
    True
    ```

    The default list `[]` is created **once**, when the `def` statement executes (at function definition time). This single list object is stored as part of the function object (in `append_to.__defaults__`).

    Every call that uses the default shares the **same list object**:

    1. `append_to(1)`: `lst` is the default list `[]`. `lst.append(1)` mutates it to `[1]`. Returns `[1]`.
    2. `append_to(2)`: `lst` is the same default list (now `[1]`). `lst.append(2)` mutates it to `[1, 2]`. Returns `[1, 2]`.

    Only **one** list object exists. `result1` and `result2` are both references to it (`result1 is result2` is `True`). That is why `result1` also shows `[1, 2]` -- it was mutated by the second call.

    The fix uses `None` as a sentinel and creates a new list on each call:

    ```python
    def append_to(item, lst=None):
        if lst is None:
            lst = []
        lst.append(item)
        return lst
    ```
