
# Method Chaining

**Method chaining** is a programming pattern where multiple methods are called sequentially on an object, with each method returning an object that supports the next method call.

```python
name.strip().lower().title()
```

---

## How It Works

Method chaining works because each method returns an object, and that object has the next method available.

Step-by-step:

```python
name = "  aLiCe  "

result = name.strip()   # "aLiCe"
result = result.lower() # "alice"
result = result.title() # "Alice"
```

Chained version:

```python
result = name.strip().lower().title()
```

---

## Key Principle

Method chaining works when **each method returns a compatible object for the next method call**. Think of chaining as a flow of types:

```
string -> string -> string -> string   (works)
string -> list -> (no .lower())        (breaks)
```

---

## Not "Returning self"

Method chaining does **not** require methods to return `self`. In many cases (like strings), methods return a **new object**. This is especially true for immutable types:

```python
s = "hello"
t = s.upper()

print(s)  # "hello"
print(t)  # "HELLO"
```

The original string is unchanged. `upper()` returns a new string, and chaining works because the new string also supports string methods.

---

## Immutable vs Mutable Behavior

### Immutable objects (e.g., str)

Methods return **new objects**. Chaining is safe and predictable:

```python
"abc".upper().replace("A", "X")
```

### Mutable objects (e.g., list)

Some methods do **not** return useful values:

```python
nums = [3, 1, 2]
nums.sort()  # returns None

nums.sort().append(4)  # AttributeError: 'NoneType' has no attribute 'append'
```

Many in-place methods return `None` by convention to prevent accidental chaining.

---

## When Chaining Breaks

Chaining fails when the returned object does not support the next method:

```python
name.strip().split().lower()
```

- `strip()` returns a string
- `split()` returns a list
- `list` has no `.lower()` --- `AttributeError`

The key question at each step: **can the next method be called on what was just returned?**

---

## Method Chaining vs Piping

### Method chaining (Python style)

```python
obj.method1().method2()
```

### Piping (functional style)

```python
f3(f2(f1(x)))
```

Python typically uses method chaining. Functional-style composition with nested calls is less common because it reads inside-out.

---

## Designing for Chaining

When writing [instance methods](instance_methods.md), the return value determines whether chaining is possible and what style of chaining you get:

- **Return `self`** (mutable style) --- mutates the object in place and returns it. The chain operates on a single object.
- **Return a new object** (immutable style) --- leaves the original untouched and returns a fresh instance. Each step in the chain produces a new object.

```python
# Mutable style: returns self
class Builder:
    def step1(self):
        print("step1")
        return self

    def step2(self):
        print("step2")
        return self

b = Builder()
b.step1().step2()
```

```python
# Immutable style: returns new object
class Text:
    def __init__(self, value):
        self.value = value

    def upper(self):
        return Text(self.value.upper())

    def add_prefix(self, prefix):
        return Text(prefix + self.value)

result = Text("hello").upper().add_prefix(">> ")
print(result.value)  # >> HELLO
```

The mutable pattern is called a **fluent interface** and is common in configuration builders, query builders, and testing frameworks. The immutable pattern mirrors how built-in string methods work.

---

## Best Practices

- Ensure methods return compatible objects before chaining
- Be aware of return types at each step (`str`, `list`, `None`)
- Avoid chaining methods that return `None`
- Use chaining for readability, not complexity

---

## Exercises

**Exercise 1.**
Predict the output and explain what type each intermediate step produces:

```python
result = "  Hello, World!  ".strip().lower().split(", ")
print(result)
print(type(result))
```

Can you chain `.upper()` after `.split()`? Why or why not?

??? success "Solution to Exercise 1"
    Output:

    ```text
    ['hello', 'world!']
    <class 'list'>
    ```

    Step by step: `strip()` returns `"Hello, World!"` (str), `lower()` returns `"hello, world!"` (str), `split(", ")` returns `["hello", "world!"]` (list).

    You cannot chain `.upper()` after `.split()` because `split()` returns a `list`, and lists do not have an `.upper()` method. This would raise `AttributeError`. To uppercase each element, you would need a comprehension: `[s.upper() for s in result]`.

---

**Exercise 2.**
A student writes:

```python
numbers = [3, 1, 4, 1, 5]
result = numbers.sort().append(6)
print(result)
```

They expect `[1, 1, 3, 4, 5, 6]`. What actually happens? Explain why, and rewrite the code so it works correctly.

??? success "Solution to Exercise 2"
    The code raises `AttributeError: 'NoneType' object has no attribute 'append'`.

    `list.sort()` sorts the list **in place** and returns `None` (by Python convention for mutating methods). So `numbers.sort()` evaluates to `None`, and `None.append(6)` fails.

    Fixed version:

    ```python
    numbers = [3, 1, 4, 1, 5]
    numbers.sort()
    numbers.append(6)
    print(numbers)  # [1, 1, 3, 4, 5, 6]
    ```

    Alternatively, using non-mutating operations:

    ```python
    result = sorted([3, 1, 4, 1, 5]) + [6]
    ```

---

**Exercise 3.**
Write a class `TextProcessor` with methods `strip_text()`, `lowercase()`, and `add_prefix(prefix)` that support method chaining. Each method should return `self` after modifying an internal `text` attribute. Demonstrate chaining all three methods.

??? success "Solution to Exercise 3"
    ```python
    class TextProcessor:
        def __init__(self, text):
            self.text = text

        def strip_text(self):
            self.text = self.text.strip()
            return self

        def lowercase(self):
            self.text = self.text.lower()
            return self

        def add_prefix(self, prefix):
            self.text = prefix + self.text
            return self

    result = TextProcessor("  HELLO  ").strip_text().lowercase().add_prefix(">> ")
    print(result.text)  # >> hello
    ```

    Each method modifies `self.text` and returns `self`, enabling the next method call on the same object. This is the fluent interface pattern. Note that this mutates the object in place --- an immutable alternative would return new `TextProcessor` instances instead.

---

**Exercise 4.**
Rewrite the `TextProcessor` from Exercise 3 using the **immutable style** --- each method should return a new `TextProcessor` instead of modifying `self`. Create an original instance, chain methods, and show that the original is unchanged while the result holds the transformed text.

??? success "Solution to Exercise 4"
    ```python
    class TextProcessor:
        def __init__(self, text):
            self.text = text

        def strip_text(self):
            return TextProcessor(self.text.strip())

        def lowercase(self):
            return TextProcessor(self.text.lower())

        def add_prefix(self, prefix):
            return TextProcessor(prefix + self.text)

        def __repr__(self):
            return f"TextProcessor({self.text!r})"

    original = TextProcessor("  HELLO  ")
    result = original.strip_text().lowercase().add_prefix(">> ")

    print(original)  # TextProcessor('  HELLO  ') — unchanged
    print(result)     # TextProcessor('>> hello')
    ```

    The immutable style mirrors how built-in `str` methods work: each call returns a new object, leaving the original intact. This is safer for shared references but creates more objects. The mutable style (Exercise 3) is more memory-efficient but can surprise callers who hold a reference to the original.
