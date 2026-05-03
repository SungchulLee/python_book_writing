

# `str`: Immutability

Python strings are **immutable**: once created, their contents cannot be changed.

This means operations on strings **never modify the original object**.
Instead, they **create new strings**.

!!! tip "Mental Model"
    A Python string is a sealed tube of characters -- you can read any position, but you cannot change one in place. Every "modification" (`replace`, `upper`, concatenation) builds a brand-new string. This immutability is why strings are hashable and safe as dict keys, but it also means repeated concatenation in a loop creates many throwaway objects -- use `''.join()` instead.

---

## Attempting to Modify a String

Trying to change a character in a string raises an error.

```python
a = "Hello Pi"

print(a[1])  # e

a[1] = "E"
# TypeError: 'str' object does not support item assignment
```

Strings do not support **item assignment**, so individual characters cannot be modified.

---

## String Methods Return New Objects

String methods return **new strings** rather than modifying the original.

```python
def main():
    s = "the brand has had its ups and downs."

    upper = s.upper()

    print(s)      # original string
    print(upper)  # new string

if __name__ == "__main__":
    main()
```

Output:

```
the brand has had its ups and downs.
THE BRAND HAS HAD ITS UPS AND DOWNS.
```

The original string remains unchanged.

---

## New Object Creation

Operations on strings produce **new objects**.

```python
a = "hello"
b = a.upper()

print(id(a))
print(id(b))
```

The object IDs differ, showing that a **new string object was created**.

---

## Variable Rebinding

Variables can be reassigned to reference new objects.

```python
a = "hello"
b = a

a = a.upper()

print(a)  # HELLO
print(b)  # hello
```

The original string still exists. The variable `a` simply points to a new object.

---

## Slicing Creates New Strings

Slicing also produces new string objects.

```python
a = "PI"

b = a[::-1]

print(a)  # PI
print(b)  # IP
```

The original string is unchanged.

---

## Why Strings Are Immutable

Immutability provides several advantages.

### Memory Efficiency

Python can reuse identical string objects.

```python
a = "hello"
b = "hello"

print(a is b)  # often True
```

This optimization is called **string interning**. Small strings may be interned by Python, but interning behavior is implementation dependent.

---

### Hashability

Immutable objects can be used as dictionary keys.

```python
d = {"hello": 1}
```

Mutable objects cannot reliably serve as keys.

---

### Thread Safety

Immutable objects can be shared safely between threads. Because the object cannot change, multiple threads can safely read the same string without synchronization.

---

### Predictability

Functions cannot accidentally modify the caller's string.

```python
def process(s):
    return s.upper()

original = "hello"
result = process(original)

print(original)  # still "hello"
```

This eliminates unintended side effects.

---

## Key Takeaways

* Python strings are **immutable**.
* Characters cannot be modified after creation.
* String methods **return new objects**.
* Variables may be reassigned, but the original object is unchanged.
* Immutability enables **memory optimizations, hashing, and safer code**.



---

## Exercises


**Exercise 1.**
Show that calling `.upper()` on a string returns a new object by comparing the `id()` of the original and the result. Verify that the original string is unchanged.

??? success "Solution to Exercise 1"

    ```python
    original = "hello"
    upper = original.upper()

    print(f"original: {original}, id: {id(original)}")
    print(f"upper:    {upper}, id: {id(upper)}")
    print(f"Same object: {original is upper}")  # False
    ```

    `.upper()` creates a new string object. The original remains unchanged because strings are immutable.

---

**Exercise 2.**
Write code that attempts to change the second character of a string using index assignment. Catch the resulting error and then show the correct way to create a modified string using slicing.

??? success "Solution to Exercise 2"

    ```python
    s = "hello"
    try:
        s[1] = "E"
    except TypeError as e:
        print(f"Error: {e}")

    # Correct approach using slicing
    s_new = s[0] + "E" + s[2:]
    print(s_new)  # hEllo
    print(s)      # hello (unchanged)
    ```

    Strings do not support item assignment. To create a modified version, build a new string from slices of the original.

---

**Exercise 3.**
Demonstrate string interning by creating two variables with the same short string literal and checking if they are the same object using `is`. Then show a case where interning does not apply.

??? success "Solution to Exercise 3"

    ```python
    a = "hello"
    b = "hello"
    print(a is b)  # True (interned)

    # Interning may not apply for dynamically created strings
    c = "".join(["h", "e", "l", "l", "o"])
    print(a == c)  # True (same value)
    print(a is c)  # May be False (different object)
    ```

    Python interns small string literals as an optimization. However, dynamically constructed strings may not be interned, so `is` may return `False` even when values are equal.
