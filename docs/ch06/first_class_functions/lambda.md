# Lambda Expressions

!!! tip "Mental Model"
    A lambda is a throwaway function you define inline -- one expression, no name, no ceremony. Use it when a full `def` would be overkill, like passing a quick sorting key or a simple callback. If your lambda needs more than one line or a descriptive name, switch to `def`.

## What Is a Lambda Expression

A **lambda expression** creates a small, anonymous function in a single line. It uses the `lambda` keyword instead of `def`:

```python
lambda parameters: expression
```

The expression is evaluated and returned automatically — no `return` statement needed.

**Lambda vs `def`** — these two definitions are equivalent:

```python
def add(x, y):
    return x + y

add_lambda = lambda x, y: x + y

print(add(3, 5))        # 8
print(add_lambda(3, 5)) # 8
```

The key difference is readability and intent. A `def` gives the function a name that appears in tracebacks and documentation; a lambda is anonymous and disposable.

## Creating Lambda Functions

**No parameters:**

```python
greet = lambda: "Hello, World!"
print(greet())  # Hello, World!
```

**Single parameter:**

```python
square = lambda x: x ** 2
print(square(5))  # 25

is_even = lambda n: n % 2 == 0
print(is_even(4))  # True
```

**Multiple parameters:**

```python
add = lambda x, y: x + y
print(add(3, 5))  # 8

max_of_two = lambda a, b: a if a > b else b
print(max_of_two(7, 12))  # 12
```

**Default parameters:**

```python
power = lambda x, n=2: x ** n
print(power(5))     # 25 (default n=2)
print(power(5, 3))  # 125
```

## What Lambda Cannot Do

Lambda is deliberately limited — that is what keeps it simple:

- **No statements**: only a single expression, no `if`/`for` blocks, no assignments
- **No type hints**: type annotations cannot be added to a lambda — if you need annotations, use `def`
- **No docstring**: if the function needs explanation, it deserves a name
- **Harder to debug**: tracebacks show `<lambda>` instead of a function name

When any of these matter, use `def`.

## With sorted()

Sorting with a custom key is the most common real use of lambda:

```python
# Sort strings by length
words = ["python", "is", "awesome", "programming", "fun"]
sorted_by_length = sorted(words, key=lambda w: len(w))
print(sorted_by_length)  # ['is', 'fun', 'python', 'awesome', 'programming']
```

```python
# Sort tuples by second element (grade)
students = [
    ("Alice", 85),
    ("Bob", 92),
    ("Charlie", 78),
    ("Diana", 95),
]
sorted_by_grade = sorted(students, key=lambda s: s[1])
print(sorted_by_grade)
# [('Charlie', 78), ('Alice', 85), ('Bob', 92), ('Diana', 95)]
```

```python
# Sort dictionaries by a specific field
products = [
    {"name": "Laptop", "price": 999},
    {"name": "Mouse", "price": 25},
    {"name": "Keyboard", "price": 75},
    {"name": "Monitor", "price": 300},
]
sorted_by_price = sorted(products, key=lambda p: p["price"])
print(sorted_by_price)
# [{'name': 'Mouse', ...}, {'name': 'Keyboard', ...}, ...]
```

```python
# Sort by absolute value
numbers = [-5, -2, 1, 3, -4]
sorted_nums = sorted(numbers, key=lambda x: abs(x))
print(sorted_nums)  # [1, -2, 3, -4, -5]
```

## With map()

`map()` applies a function to every item in an iterable:

```python
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]
```

```python
# Convert Celsius to Fahrenheit
celsius = [0, 10, 20, 30, 40]
fahrenheit = list(map(lambda c: (c * 9 / 5) + 32, celsius))
print(fahrenheit)  # [32.0, 50.0, 68.0, 86.0, 104.0]
```

```python
# String manipulation
words = ["hello", "world", "python", "lambda"]
uppercase = list(map(lambda s: s.upper(), words))
print(uppercase)  # ['HELLO', 'WORLD', 'PYTHON', 'LAMBDA']
```

```python
# map() with multiple iterables
a = [1, 2, 3]
b = [4, 5, 6]
sums = list(map(lambda x, y: x + y, a, b))
print(sums)  # [5, 7, 9]
```

## With filter()

`filter()` keeps items for which the function returns `True`:

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6, 8, 10]
```

```python
# Filter strings by length
words = ["cat", "elephant", "dog", "hippopotamus", "bird"]
long_words = list(filter(lambda w: len(w) > 5, words))
print(long_words)  # ['elephant', 'hippopotamus']
```

```python
# Data cleaning — filter valid emails (simple check)
emails = ["user@example.com", "invalid-email", "another@test.com", "bad@", "good@mail.org"]
valid = list(filter(lambda e: "@" in e and "." in e.split("@")[-1], emails))
print(valid)  # ['user@example.com', 'another@test.com', 'good@mail.org']
```

## List Comprehension Alternative

A list comprehension often reads better than `map()` or `filter()` with a lambda:

```python
numbers = [1, 2, 3, 4, 5]

# map + lambda
squares = list(map(lambda x: x ** 2, numbers))

# list comprehension — same result, easier to read
squares = [x ** 2 for x in numbers]
```

```python
# filter + lambda
evens = list(filter(lambda x: x % 2 == 0, numbers))

# list comprehension
evens = [x for x in numbers if x % 2 == 0]
```

Use lambda when passing a key function (e.g. `sorted(..., key=lambda ...)`) — there is no comprehension equivalent for that. Use comprehensions when you are transforming or filtering a sequence and want clear, readable code.

## Practical Examples

**Data cleaning with `map()`:**

```python
data = ["  hello  ", "  WORLD  ", "  Python  "]
cleaned = list(map(lambda s: s.strip().lower(), data))
print(cleaned)  # ['hello', 'world', 'python']
```

**Extract fields from records:**

```python
users = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "London"},
    {"name": "Charlie", "age": 35, "city": "Paris"},
]

# Get active users sorted by age
names = list(map(lambda u: u["name"], users))
print(names)  # ['Alice', 'Bob', 'Charlie']

by_age = sorted(users, key=lambda u: u["age"])
print([u["name"] for u in by_age])  # ['Bob', 'Alice', 'Charlie']
```

**Calculate discounted prices:**

```python
prices = [100, 250, 50, 399, 75]
discount = 0.20
discounted = list(map(lambda p: p * (1 - discount), prices))
print(discounted)  # [80.0, 200.0, 40.0, 319.2, 60.0]
```

**Dictionary of operations:**

```python
ops = {
    "add": lambda x, y: x + y,
    "sub": lambda x, y: x - y,
    "mul": lambda x, y: x * y,
}

print(ops["add"](10, 5))  # 15
print(ops["mul"](10, 5))  # 50
```

## Key Ideas

Lambda is a convenience, not a necessity — anything a lambda can do, `def` can do too. Reach for lambda when you need a short throwaway function as an argument (especially for `sorted`, `map`, or `filter`) and the logic fits in a single expression. If the function is complex, reused, or needs documentation, write a `def`.

PEP 8 discourages assigning a lambda to a variable (`square = lambda x: x ** 2`); if you need a name, use `def`. The one place lambda shines is inline, right where it is consumed.

For more on returning functions from functions — a pattern closely related to lambda — see [Function Factories](function_factories.md).

---

## Exercises

**Exercise 1.**
Given a list of strings `["banana", "apple", "cherry", "date"]`, use `sorted()` with a lambda to sort them by their last character. Print the sorted result.

??? success "Solution to Exercise 1"

        fruits = ["banana", "apple", "cherry", "date"]
        sorted_fruits = sorted(fruits, key=lambda s: s[-1])
        print(sorted_fruits)  # ['banana', 'apple', 'date', 'cherry']

---

**Exercise 2.**
Use `map()` with a lambda to convert a list of Celsius temperatures `[0, 20, 37, 100]` to Fahrenheit (formula: `F = C * 9/5 + 32`). Then use `filter()` with a lambda to keep only temperatures above 80 F. Print both results.

??? success "Solution to Exercise 2"

        celsius = [0, 20, 37, 100]

        fahrenheit = list(map(lambda c: c * 9 / 5 + 32, celsius))
        print(fahrenheit)  # [32.0, 68.0, 98.6, 212.0]

        hot = list(filter(lambda f: f > 80, fahrenheit))
        print(hot)  # [98.6, 212.0]

---

**Exercise 3.**
Write a function `make_adder` that takes a number `n` and returns a lambda that adds `n` to its argument. Create `add5` and `add10` using `make_adder`, and verify they work correctly. Then rewrite `make_adder` using `def` instead of `lambda` for the inner function and explain why PEP 8 recommends the `def` version.

??? success "Solution to Exercise 3"

        # Lambda version
        make_adder = lambda n: lambda x: x + n

        add5 = make_adder(5)
        add10 = make_adder(10)

        print(add5(3))    # 8
        print(add10(3))   # 13

        # PEP 8 preferred version using def
        def make_adder_def(n):
            def adder(x):
                return x + n
            return adder

        add5 = make_adder_def(5)
        print(add5(3))    # 8
        # PEP 8 discourages assigning a lambda to a name;
        # if you need a name, use def.
