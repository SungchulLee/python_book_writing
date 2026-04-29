# Instance Methods

Instance methods are functions defined inside a class that operate on instance-specific data via `self`. They are the most common method type --- for alternatives that operate on the class or neither, see [Class Methods](class_methods.md) and [Static Methods](static_methods.md).

---

## What are Instance Methods

### 1. Functions in Class

```python
class Student:
    def __init__(self, name, courses):
        self.name = name
        self.courses = courses
    
    def add_course(self, course):  # Instance method
        self.courses.append(course)
```

### 2. Receive `self`

First parameter is always `self`.

### 3. Operate on Instance

Methods modify or access instance attributes.

---

## The `self` Parameter

### 1. Reference to Instance

```python
class Student:
    def greet(self):
        print(f"Hello, I'm {self.name}")

a = Student("Lee")
a.greet()  # self = a
```

### 2. Automatic Passing

```python
# These are equivalent:
a.greet()
Student.greet(a)
```

### 3. Access Instance Data

```python
def get_info(self):
    return f"{self.name}, {self.major}"
```

---

## Defining Methods

### 1. Basic Method

```python
class Student:
    def __init__(self, name, courses):
        self.name = name
        self.courses = courses
    
    def add_course(self, course):
        if course not in self.courses:
            self.courses.append(course)
```

### 2. Multiple Parameters

```python
def enroll(self, course, semester):
    enrollment = {
        'course': course,
        'semester': semester
    }
    self.enrollments.append(enrollment)
```

### 3. Return Values

```python
def has_course(self, course):
    return course in self.courses
```

---

## Method Examples

### 1. Getter Method

```python
class Student:
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
```

### 2. Setter Method

```python
def set_name(self, name):
    if name:
        self.name = name
```

### 3. Action Method

```python
def drop_course(self, course):
    if course in self.courses:
        self.courses.remove(course)
```

---

## Calling Methods

### 1. Via Instance

```python
student = Student("Lee", ["Math"])
student.add_course("Physics")
```

### 2. Via Class

```python
Student.add_course(student, "Physics")
# Equivalent but not idiomatic
```

### 3. Chaining Methods

Instance methods can support [method chaining](method_chaining.md) by returning `self` (mutable style) or a new object of the same type (immutable style).

```python
class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
        return self  # Return self for chaining
    
    def reset(self):
        self.count = 0
        return self

c = Counter().increment().increment().reset()
```

---

## `self` Mechanics

### 1. Must Use `self`

```python
# WRONG
def add_course(self, course):
    courses.append(course)  # NameError!

# CORRECT
def add_course(self, course):
    self.courses.append(course)
```

### 2. Access Attributes

```python
def print_info(self):
    print(f"Name: {self.name}")
    print(f"Major: {self.major}")
```

### 3. Call Other Methods

```python
def enroll_and_notify(self, course):
    self.add_course(course)
    self.send_notification()
```

---

## Instance vs Class Variables

### 1. Accessing Instance Variable

```python
class Student:
    def __init__(self, name):
        self.name = name  # instance variable
    
    def greet(self):
        return f"Hello, {self.name}"
```

### 2. Accessing Class Variable

```python
class Student:
    university = 'Yonsei'  # class variable
    
    def get_university(self):
        return Student.university  # or self.university
```

### 3. Modifying Class Variable

```python
def change_university(self, new_name):
    self.university = new_name  # WRONG - creates instance attr
    
@classmethod
def change_university(cls, new_name):
    cls.university = new_name  # CORRECT
```

---

## Method vs Function

### 1. Function Attribute

```python
def f():
    return 1

print(f)      # <function f>
print(f())    # 1
```

### 2. Method Attribute

```python
import numpy as np
x = np.array([1, 2, 3])

print(x.sum)    # <built-in method sum>
print(x.sum())  # 6
```

### 3. Bound Methods

```python
class Student:
    def greet(self):
        return "Hello"

a = Student()
print(Student.greet)  # <function greet>
print(a.greet)        # <bound method greet>
```

This binding happens because functions are **descriptors** --- they implement a `__get__` method. When you access a function through an instance (`a.greet`), Python's descriptor protocol automatically wraps it into a bound method that fixes `self` to the instance. This same mechanism underlies [`@classmethod`](class_methods.md) (binds to the class) and [`@staticmethod`](static_methods.md) (disables binding entirely).

| Type | Receives | Bound to | Use case |
|---|---|---|---|
| Instance method | `self` | instance | Object behavior and state |
| Class method | `cls` | class | Shared config, alt constructors |
| Static method | nothing | nothing | Utility, no state needed |

---

## Common Patterns

### 1. Validation

```python
def set_age(self, age):
    if 0 <= age <= 120:
        self.age = age
    else:
        raise ValueError("Invalid age")
```

### 2. Computation

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
```

### 3. State Change

```python
class Car:
    def __init__(self, speed):
        self.speed = speed
    
    def accelerate(self, amount):
        self.speed += amount
```

---

## Helper Methods

### 1. Private Methods

```python
class Student:
    def process(self):
        self._validate()
        self._compute()
    
    def _validate(self):  # "private" by convention
        if not self.name:
            raise ValueError("Name required")
    
    def _compute(self):
        pass
```

### 2. Public Interface

```python
def enroll(self, course):
    self._validate_prerequisites(course)
    self._add_to_schedule(course)
    self._update_credits()
```

### 3. Internal Logic

Keep complex logic in separate methods.

---

## Method Signatures

### 1. No Parameters

```python
def reset(self):
    self.count = 0
```

### 2. With Parameters

```python
def add(self, item, priority=0):
    self.items.append((item, priority))
```

### 3. Variable Arguments

```python
def add_multiple(self, *courses):
    for course in courses:
        self.add_course(course)
```

---

## Key Takeaways

- Instance methods operate on instance data.
- First parameter is always `self`.
- Access instance attributes via `self`.
- Call methods via instance: `obj.method()`.
- Use `_method` for internal helpers.

---

## Exercises

**Exercise 1.**
Create a `Stack` class with instance methods `push(item)`, `pop()`, `peek()` (returns top without removing), and `is_empty()`. All methods operate on `self._items` (a list). Demonstrate the full lifecycle: push several items, peek, pop, check empty.

??? success "Solution to Exercise 1"

        class Stack:
            def __init__(self):
                self._items = []

            def push(self, item):
                self._items.append(item)

            def pop(self):
                if self.is_empty():
                    raise IndexError("pop from empty stack")
                return self._items.pop()

            def peek(self):
                if self.is_empty():
                    raise IndexError("peek at empty stack")
                return self._items[-1]

            def is_empty(self):
                return len(self._items) == 0

        s = Stack()
        s.push("a")
        s.push("b")
        s.push("c")
        print(s.peek())      # c
        print(s.pop())       # c
        print(s.pop())       # b
        print(s.is_empty())  # False

---

**Exercise 2.**
Write a `StringProcessor` class with `self.text`. Add instance methods `to_upper()`, `to_lower()`, `reverse()`, and `word_count()`. Each method should return a new `StringProcessor` so methods can be chained: `StringProcessor("Hello World").to_upper().reverse()`.

??? success "Solution to Exercise 2"

        class StringProcessor:
            def __init__(self, text):
                self.text = text

            def to_upper(self):
                return StringProcessor(self.text.upper())

            def to_lower(self):
                return StringProcessor(self.text.lower())

            def reverse(self):
                return StringProcessor(self.text[::-1])

            def word_count(self):
                return len(self.text.split())

            def __repr__(self):
                return f"StringProcessor({self.text!r})"

        result = StringProcessor("Hello World").to_upper().reverse()
        print(result)  # StringProcessor('DLROW OLLEH')
        print(StringProcessor("one two three").word_count())  # 3

---

**Exercise 3.**
Build a `Rectangle` class with `width` and `height`. Add instance methods `area()`, `perimeter()`, `is_square()`, and `scale(factor)` (returns a new Rectangle). Show that `scale` returns a new object while the original is unchanged. Also show the difference between calling via instance (`r.area()`) and via class (`Rectangle.area(r)`).

??? success "Solution to Exercise 3"

        class Rectangle:
            def __init__(self, width, height):
                self.width = width
                self.height = height

            def area(self):
                return self.width * self.height

            def perimeter(self):
                return 2 * (self.width + self.height)

            def is_square(self):
                return self.width == self.height

            def scale(self, factor):
                return Rectangle(self.width * factor, self.height * factor)

            def __repr__(self):
                return f"Rectangle({self.width}, {self.height})"

        r = Rectangle(4, 6)
        r2 = r.scale(2)
        print(r)    # Rectangle(4, 6) — unchanged
        print(r2)   # Rectangle(8, 12)

        # Two ways to call
        print(r.area())              # 24
        print(Rectangle.area(r))     # 24 — explicit self

---

**Exercise 4.**
Examine the following code and predict what each `print` outputs. Explain why `Student.greet` and `s.greet` have different types, and what the descriptor protocol has to do with it.

```python
class Student:
    def greet(self):
        return f"Hi, I'm {self.name}"

s = Student()
s.name = "Alice"

print(type(Student.greet))
print(type(s.greet))
print(Student.greet(s))
print(s.greet())

f = s.greet
print(f())
```

??? success "Solution to Exercise 4"

        class Student:
            def greet(self):
                return f"Hi, I'm {self.name}"

        s = Student()
        s.name = "Alice"

        print(type(Student.greet))  # <class 'function'>
        print(type(s.greet))        # <class 'method'>
        print(Student.greet(s))     # Hi, I'm Alice
        print(s.greet())            # Hi, I'm Alice

        f = s.greet
        print(f())  # Hi, I'm Alice — f is a bound method, self is captured

        # Student.greet is a plain function (accessed on the class).
        # s.greet is a bound method (accessed on an instance).
        # The difference exists because functions are descriptors:
        # function.__get__(s, Student) returns a bound method with self=s.
        # That is why s.greet() works without passing self explicitly.
