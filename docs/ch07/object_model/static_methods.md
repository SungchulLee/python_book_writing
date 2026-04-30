# Static Methods

Static methods are utility functions that belong to a class namespace but don't access instance or class data. Unlike [instance methods](instance_methods.md) (bound to `self`) and [class methods](class_methods.md) (bound to `cls`), static methods receive no implicit first argument --- they are essentially plain functions that happen to live on a class.

!!! tip "Importance Hierarchy"
    ```text
    1. Instance methods → core OOP behavior (used everywhere)
    2. Class methods    → advanced patterns (alt constructors, shared config)
    3. Static methods   → organizational convenience (least important)
    ```
    Static methods are the **least essential** of the three. If you are unsure
    whether something should be a static method or a module-level function, the
    module-level function is usually the simpler choice.

---

## What are Static Methods

### 1. Decorated with `@staticmethod`

```python
class MathTools:
    @staticmethod
    def add(a, b):
        return a + b
```

### 2. No `self` or `cls`

Don't receive implicit first parameter.

### 3. Namespace Functions

Logically grouped with class but independent.

---

## Defining Static Methods

### 1. Basic Syntax

```python
class MyClass:
    @staticmethod
    def utility_function(param):
        return param * 2
```

### 2. Call via Class

```python
result = MyClass.utility_function(5)
```

### 3. Call via Instance

```python
obj = MyClass()
result = obj.utility_function(5)
```

---

## Static vs Instance

### 1. Instance Method

```python
class Student:
    def greet(self):
        return f"Hello, {self.name}"

a = Student()
print(Student.greet)  # <function>
print(a.greet)        # <bound method>
```

### 2. Static Method

```python
class Student:
    @staticmethod
    def is_workday(day):
        # implementation
        pass

print(Student.is_workday)  # <function>
print(a.is_workday)        # <function> (not bound!)
```

### 3. Not Bound

Static methods are never bound to instances. Under the hood, `@staticmethod` is a descriptor that *disables* the normal binding mechanism --- it returns the raw function regardless of whether you access it via the class or an instance. Compare this with regular functions (which become bound methods on instances) and `@classmethod` (which binds to the class). See [Instance Methods](instance_methods.md) for details on method binding.

---

## Use Cases

### 1. Utility Functions

```python
class StringUtils:
    @staticmethod
    def is_palindrome(s):
        return s == s[::-1]
    
    @staticmethod
    def capitalize_words(s):
        return ' '.join(word.capitalize() for word in s.split())
```

### 2. Validation

```python
class Validator:
    @staticmethod
    def is_valid_email(email):
        return '@' in email and '.' in email
    
    @staticmethod
    def is_valid_phone(phone):
        return len(phone) == 10 and phone.isdigit()
```

### 3. Formatting

```python
class Formatter:
    @staticmethod
    def format_currency(amount):
        return f"${amount:,.2f}"
    
    @staticmethod
    def format_date(date):
        return date.strftime("%Y-%m-%d")
```

---

## Workday Example

### 1. Date Validation

```python
from datetime import datetime

class Student:
    def __init__(self, name):
        self.name = name
    
    @staticmethod
    def is_workday(day):
        day_obj = datetime.strptime(day, '%Y-%m-%d')
        # Saturday = 5, Sunday = 6
        return day_obj.weekday() not in [5, 6]
```

### 2. Usage

```python
student = Student("Lee")
for day in range(10, 20):
    date = f"2024-04-{day}"
    if student.is_workday(date):
        print(f"{date} is a workday")
```

### 3. No Instance Access

Static method doesn't use `self.name`.

---

## When to Use Static

### 1. Pure Utility

```python
class Math:
    @staticmethod
    def factorial(n):
        if n <= 1:
            return 1
        return n * Math.factorial(n - 1)
```

### 2. No Class/Instance Data

Function doesn't need access to `self` or `cls`.

### 3. Logical Grouping

```python
class DateUtils:
    @staticmethod
    def is_leap_year(year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
    @staticmethod
    def days_in_month(month, year):
        # implementation
        pass
```

---

## Static vs Class Method

### 1. Static Method

```python
class Config:
    @staticmethod
    def validate_port(port):
        return 1 <= port <= 65535
```

No access to class or instance.

### 2. Class Method

```python
class Config:
    default_port = 8080
    
    @classmethod
    def set_default_port(cls, port):
        cls.default_port = port
```

Has access to class via `cls`.

### 3. Choose Appropriately

Use static if no class access needed.

---

## Comparison Example

### 1. Three Method Types

```python
class Demo:
    class_var = 10
    
    def instance_method(self):
        return f"Instance: {self.class_var}"
    
    @classmethod
    def class_method(cls):
        return f"Class: {cls.class_var}"
    
    @staticmethod
    def static_method(value):
        return f"Static: {value}"
```

### 2. Calling Methods

```python
obj = Demo()

obj.instance_method()           # Needs instance
Demo.class_method()             # Works on class
Demo.static_method(42)          # Independent
```

### 3. Different Purposes

Each serves distinct needs.

---

## Real-World Examples

### 1. Conversion Utilities

```python
class Temperature:
    @staticmethod
    def celsius_to_fahrenheit(c):
        return c * 9/5 + 32
    
    @staticmethod
    def fahrenheit_to_celsius(f):
        return (f - 32) * 5/9
```

### 2. String Processing

```python
class TextProcessor:
    @staticmethod
    def remove_punctuation(text):
        import string
        return text.translate(str.maketrans('', '', string.punctuation))
    
    @staticmethod
    def word_count(text):
        return len(text.split())
```

### 3. Data Validation

```python
class InputValidator:
    @staticmethod
    def is_positive(num):
        return num > 0
    
    @staticmethod
    def is_in_range(num, low, high):
        return low <= num <= high
```

---

## Design Considerations

Static methods are primarily **organizational**, not conceptual. They don't leverage the class system (no `self`, no `cls`, no inheritance binding). In many cases a plain module-level function is simpler and equally correct.

### 1. Alternative: Module Function

```python
# Could be a module-level function
def is_workday(day):
    # implementation
    pass

# vs class static method
class DateUtils:
    @staticmethod
    def is_workday(day):
        # implementation
        pass
```

### 2. Prefer Static Method When

- Function is conceptually part of the class's domain
- You want to group related utilities under a namespace
- Subclasses may need to override the behavior

### 3. Prefer Module Function When

- The function is a truly independent utility
- It has no conceptual link to a specific class
- You want it easily importable without referencing a class

---

## Inheritance

### 1. Can Override

```python
class Parent:
    @staticmethod
    def method():
        return "Parent"

class Child(Parent):
    @staticmethod
    def method():
        return "Child"

print(Child.method())  # "Child"
```

### 2. Still Not Bound

```python
c = Child()
print(c.method)  # <function> (not bound method)
```

### 3. Override Without Dynamic Binding

Static methods can be overridden by name in subclasses, but they do not participate in dynamic binding the way instance or class methods do. The method called depends purely on attribute lookup (which class the name is found on), not on the instance's runtime type. If you need polymorphic dispatch, use an instance method or class method instead.

---

## When NOT to Use Static Methods

- The function is reusable across modules → use a module-level function
- The function may later need `self` or `cls` → start with an instance or class method
- You need polymorphic behavior → static methods do not support dynamic dispatch naturally

---

## Key Takeaways

- Static methods don't receive `self` or `cls`.
- Use `@staticmethod` decorator.
- For utility functions grouped with class.
- Not bound to instances.
- Use when no class/instance access needed.

---

## Exercises

**Exercise 1.**
Create a `MathUtils` class with static methods `is_prime(n)`, `factorial(n)`, and `fibonacci(n)`. Show that these can be called without creating an instance: `MathUtils.is_prime(17)`. Discuss why static methods are appropriate here.

??? success "Solution to Exercise 1"

        class MathUtils:
            @staticmethod
            def is_prime(n):
                if n < 2:
                    return False
                for i in range(2, int(n**0.5) + 1):
                    if n % i == 0:
                        return False
                return True

            @staticmethod
            def factorial(n):
                result = 1
                for i in range(2, n + 1):
                    result *= i
                return result

            @staticmethod
            def fibonacci(n):
                a, b = 0, 1
                for _ in range(n):
                    a, b = b, a + b
                return a

        print(MathUtils.is_prime(17))    # True
        print(MathUtils.factorial(5))     # 120
        print(MathUtils.fibonacci(10))    # 55
        # Static because: no instance/class state needed

---

**Exercise 2.**
Write a `Validator` class with static methods `is_email(text)` (checks for `@`), `is_phone(text)` (checks digits and length), and `is_url(text)` (checks for `http`). Use the class to validate user input. Show that static methods can also be called on instances, though it adds no benefit.

??? success "Solution to Exercise 2"

        class Validator:
            @staticmethod
            def is_email(text):
                return "@" in text and "." in text.split("@")[-1]

            @staticmethod
            def is_phone(text):
                digits = text.replace("-", "").replace(" ", "")
                return digits.isdigit() and len(digits) >= 10

            @staticmethod
            def is_url(text):
                return text.startswith("http://") or text.startswith("https://")

        print(Validator.is_email("user@example.com"))  # True
        print(Validator.is_phone("555-123-4567"))      # True
        print(Validator.is_url("https://python.org"))  # True

        # Works on instance too (but no benefit)
        v = Validator()
        print(v.is_email("test"))  # False

---

**Exercise 3.**
Build a `Temperature` class with instance attribute `celsius` and static methods `c_to_f(c)` and `f_to_c(f)` for conversion. Add an instance method `to_fahrenheit()` that uses the static method internally. Demonstrate both calling patterns: `Temperature.c_to_f(100)` and `t.to_fahrenheit()`.

??? success "Solution to Exercise 3"

        class Temperature:
            def __init__(self, celsius):
                self.celsius = celsius

            @staticmethod
            def c_to_f(c):
                return c * 9 / 5 + 32

            @staticmethod
            def f_to_c(f):
                return (f - 32) * 5 / 9

            def to_fahrenheit(self):
                return Temperature.c_to_f(self.celsius)

        # Static method call (no instance needed)
        print(Temperature.c_to_f(100))  # 212.0
        print(Temperature.f_to_c(32))   # 0.0

        # Instance method uses static method internally
        t = Temperature(37)
        print(t.to_fahrenheit())  # 98.6

---

**Exercise 4.**
A colleague argues that this static method should be a module-level function instead. Evaluate their claim --- is `@staticmethod` justified here, or would a module function be better? Explain your reasoning.

```python
class FileParser:
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path) as f:
            return self._parse(f.read())

    def _parse(self, raw):
        return [self.clean_line(line) for line in raw.splitlines()]

    @staticmethod
    def clean_line(line):
        return line.strip().lower()
```

??? success "Solution to Exercise 4"

        # The static method IS justified here. Reasons:
        #
        # 1. clean_line is used internally by the instance method _parse,
        #    so it belongs to FileParser's domain.
        #
        # 2. A subclass might override clean_line to change parsing behavior
        #    (e.g., preserve case). If it were a module function, subclasses
        #    could not override it without also overriding _parse.
        #
        # 3. It does not need self or cls, so @staticmethod is correct
        #    (an instance method would misleadingly suggest state dependency).
        #
        # Counter-argument: if clean_line is genuinely reusable outside
        # FileParser, a module-level function would be more accessible.
        # But as a helper tied to the class's parsing logic, @staticmethod
        # is the right call.

        class FileParser:
            def __init__(self, path):
                self.path = path

            def read(self):
                with open(self.path) as f:
                    return self._parse(f.read())

            def _parse(self, raw):
                return [self.clean_line(line) for line in raw.splitlines()]

            @staticmethod
            def clean_line(line):
                return line.strip().lower()

        # Subclass can override without touching _parse:
        class CaseSensitiveParser(FileParser):
            @staticmethod
            def clean_line(line):
                return line.strip()  # preserve case
