# Magic Methods Practice Exercises

!!! tip "Mental Model"
    These exercises ask you to make custom objects behave like built-in types. The key insight: every Python operator and built-in function has a corresponding dunder method. By implementing the right hooks, your objects become indistinguishable from native types at the call site -- they support `+`, `len()`, `for`, `with`, and `[]` just like lists and dicts.

## Exercise 1: Temperature Class
Create a `Temperature` class that:
- Stores temperature in Celsius
- Implements `__init__`, `__repr__`, and `__str__`
- Implements comparison operators (`__eq__`, `__lt__`, `__gt__`, etc.)
- Implements arithmetic operators to add/subtract temperatures
- Has a custom `__format__` method that supports 'C', 'F', and 'K' format specs

Example usage:
```python
t1 = Temperature(25)
t2 = Temperature(30)
print(t1)  # "25.0°C"
print(f"{t1:F}")  # "77.0°F"
print(t1 < t2)  # True
print(t1 + 5)  # Temperature(30)
```

---

## Exercise 2: Shopping Cart
Create a `ShoppingCart` class that:
- Implements `__len__` to return the number of items
- Implements `__getitem__` to access items by index
- Implements `__setitem__` to update items
- Implements `__delitem__` to remove items
- Implements `__contains__` to check if an item is in the cart
- Implements `__iter__` to iterate over items
- Has an `add_item(item, quantity, price)` method
- Has a `total()` method that returns the total cost

---

## Exercise 3: Fraction Class
Create a `Fraction` class that:
- Stores numerator and denominator
- Implements all arithmetic operators (`__add__`, `__sub__`, `__mul__`, `__truediv__`)
- Automatically simplifies fractions (greatest common divisor)
- Implements comparison operators
- Implements `__str__` to display as "numerator/denominator"
- Implements `__float__` to convert to decimal
- Handles division by zero appropriately

Example usage:
```python
f1 = Fraction(1, 2)
f2 = Fraction(1, 3)
print(f1 + f2)  # 5/6
print(f1 * f2)  # 1/6
print(float(f1))  # 0.5
```

---

## Exercise 4: Range-like Class
Create a `CustomRange` class that mimics Python's built-in `range()`:
- Implements `__init__` with start, stop, and step parameters
- Implements `__len__` to return the number of elements
- Implements `__getitem__` to access elements by index
- Implements `__contains__` to check if a value is in the range
- Implements `__iter__` to make it iterable
- Implements `__reversed__` for reverse iteration

---

## Exercise 5: Callable Validator
Create a `Validator` class that:
- Takes validation rules in `__init__` (e.g., min, max, type)
- Implements `__call__` to validate a value
- Returns True if valid, False otherwise
- Can be used as a decorator for functions

Example usage:
```python
age_validator = Validator(min=0, max=150, type=int)
print(age_validator(25))  # True
print(age_validator(-5))  # False
```

---

## Exercise 6: File Logger Context Manager
Create a `FileLogger` context manager that:
- Opens a log file when entering the context
- Implements `__enter__` and `__exit__`
- Provides a `log(message)` method
- Automatically adds timestamps to log entries
- Safely closes the file even if exceptions occur
- Optionally formats exceptions in the log

Example usage:
```python
with FileLogger('app.log') as logger:
    logger.log('Application started')
    # do some work
    logger.log('Processing complete')
```

---

## Exercise 7: Coordinate System
Create a `Coordinate` class that:
- Represents a point in 2D space
- Implements arithmetic operators for vector operations
- Implements `__abs__` to return distance from origin
- Implements `__eq__` and `__hash__` so coordinates can be used in sets
- Implements `__neg__` to reflect across origin
- Has a `distance_to(other)` method

---

## Exercise 8: Counter Dictionary
Create a `CounterDict` class that:
- Automatically initializes missing keys to 0
- Implements `__missing__` for default values
- Implements `__getitem__` and `__setitem__`
- Implements arithmetic operators to combine counters
- Has a `most_common(n)` method

Example usage:
```python
counter = CounterDict()
counter['a'] = 5
counter['b'] = 3
print(counter['c'])  # 0 (not KeyError)
```

---

## Exercise 9: Smart String
Create a `SmartString` class that:
- Wraps a regular string
- Implements `__len__`, `__getitem__`, and `__iter__`
- Implements `__add__` for concatenation
- Implements `__mul__` for repetition
- Implements `__contains__` for substring checking
- Implements comparison operators (case-insensitive)
- Implements `__int__` and `__float__` for conversion (if possible)

---

## Exercise 10: Matrix Operations
Create a `Matrix` class that:
- Stores a 2D grid of numbers
- Implements `__add__` and `__sub__` for matrix addition/subtraction
- Implements `__mul__` for scalar multiplication and matrix multiplication
- Implements `__getitem__` with tuple indexing (row, col)
- Implements `__eq__` for matrix equality
- Has methods for `transpose()`, `determinant()` (for 2x2)

---

## Challenge Exercise: Database-like Table
Create a `Table` class that:
- Stores rows of data with named columns
- Implements `__len__` for number of rows
- Implements `__getitem__` to get rows by index or columns by name
- Implements `__iter__` to iterate over rows
- Implements `__contains__` to check if a value exists in any column
- Has methods: `add_row()`, `filter()`, `sort_by(column)`, `select(columns)`
- Can be used as a context manager to auto-save to file

This is a complex exercise that combines multiple magic methods!

---

## Testing Your Solutions

For each exercise, write test cases that verify:
1. All magic methods work correctly
2. Edge cases are handled (empty inputs, None, zeros, etc.)
3. Type checking works appropriately
4. Error messages are clear and helpful

Good luck!

---

## Exercises

**Exercise 1.**
Create a `Counter` class that supports `+` (add counts), `-` (subtract counts, minimum 0), `==` (compare counts), and `str()` (display as `"Counter(N)"`). Implement `__add__`, `__sub__`, `__eq__`, `__str__`, and `__repr__`. Show all operations.

??? success "Solution to Exercise 1"

        class Counter:
            def __init__(self, count=0):
                self.count = max(0, count)

            def __add__(self, other):
                return Counter(self.count + other.count)

            def __sub__(self, other):
                return Counter(max(0, self.count - other.count))

            def __eq__(self, other):
                return self.count == other.count

            def __str__(self):
                return f"Counter({self.count})"

            def __repr__(self):
                return f"Counter({self.count})"

        a = Counter(5)
        b = Counter(3)
        print(a + b)  # Counter(8)
        print(a - b)  # Counter(2)
        print(b - a)  # Counter(0) — floors at 0
        print(a == Counter(5))  # True

---

**Exercise 2.**
Write a `Percentage` class that stores a value between 0 and 100. Implement `__init__` (validates range), `__repr__`, `__str__` (shows `"45.0%"`), `__add__` (caps at 100), `__sub__` (floors at 0), and `__float__` (returns the decimal, e.g., 0.45). Demonstrate all methods.

??? success "Solution to Exercise 2"

        class Percentage:
            def __init__(self, value):
                if not 0 <= value <= 100:
                    raise ValueError("Value must be between 0 and 100")
                self.value = float(value)

            def __repr__(self):
                return f"Percentage({self.value})"

            def __str__(self):
                return f"{self.value}%"

            def __add__(self, other):
                return Percentage(min(100, self.value + other.value))

            def __sub__(self, other):
                return Percentage(max(0, self.value - other.value))

            def __float__(self):
                return self.value / 100

        p = Percentage(45)
        print(str(p))         # 45.0%
        print(float(p))       # 0.45
        print(p + Percentage(60))  # 100.0% (capped)
        print(p - Percentage(50))  # 0.0% (floored)

---

**Exercise 3.**
Build a `Stack` class using a list internally. Implement `__len__`, `__bool__`, `__contains__`, `__iter__`, and `__repr__`. Add `push(item)` and `pop()` methods. Show that `len(stack)`, `item in stack`, `bool(empty_stack)`, and `for item in stack` all work.

??? success "Solution to Exercise 3"

        class Stack:
            def __init__(self):
                self._items = []

            def push(self, item):
                self._items.append(item)

            def pop(self):
                if not self._items:
                    raise IndexError("pop from empty stack")
                return self._items.pop()

            def __len__(self):
                return len(self._items)

            def __bool__(self):
                return len(self._items) > 0

            def __contains__(self, item):
                return item in self._items

            def __iter__(self):
                return iter(reversed(self._items))

            def __repr__(self):
                return f"Stack({self._items})"

        s = Stack()
        print(bool(s))    # False (empty)

        s.push("a")
        s.push("b")
        s.push("c")
        print(len(s))      # 3
        print("b" in s)    # True
        print(bool(s))     # True

        for item in s:
            print(item, end=" ")  # c b a (LIFO order)
