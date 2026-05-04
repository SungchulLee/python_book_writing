# Class Methods

Class methods receive the class itself as the first argument, enabling operations on class-level data and alternative constructors. Unlike [instance methods](instance_methods.md) that bind to an object via `self`, class methods bind to the class via `cls`. For utilities that need neither, see [Static Methods](static_methods.md).

!!! tip "Mental Model"
    An instance method works on one object (`self`); a class method works on the class itself (`cls`). The most common use is alternative constructors -- `dict.fromkeys()`, `datetime.now()` -- that create instances through a different entry point than `__init__`. Because `cls` is passed automatically, class methods also work correctly with inheritance: a subclass calling an inherited class method receives its own class, not the parent.

---

## What are Class Methods

### 1. Decorated with `@classmethod`

```python
class Student:
    count = 0
    
    @classmethod
    def increment_count(cls):
        cls.count += 1
```

### 2. Receive `cls`

First parameter is the class, not instance.

### 3. Operate on Class

Modify or access class-level attributes.

---

## Defining Class Methods

### 1. Basic Syntax

```python
class MyClass:
    class_var = 0
    
    @classmethod
    def class_method(cls):
        cls.class_var += 1
```

### 2. Call via Class

```python
MyClass.class_method()
print(MyClass.class_var)  # 1
```

### 3. Call via Instance

```python
obj = MyClass()
obj.class_method()  # Works but not idiomatic
```

---

## Class Method Use Cases

### 1. Modify Class Attributes

```python
class Student:
    university = 'Yonsei'
    
    @classmethod
    def change_university(cls, new_name):
        cls.university = new_name

Student.change_university('YonHei')
```

### 2. Track All Instances

```python
class Student:
    students_list = []
    mandatory = ['Chapel']
    
    @classmethod
    def add_mandatory(cls, course):
        if course not in cls.mandatory:
            cls.mandatory.append(course)
            for student in cls.students_list:
                student.subject.append(course)
```

### 3. Global Configuration

```python
class Logger:
    enable_debug = False
    
    @classmethod
    def set_debug(cls):
        cls.enable_debug = True
```

---

## Alternative Constructors

### 1. Factory Pattern

```python
from datetime import date

class Person:
    def __init__(self, name, birth_year):
        self.name = name
        self.birth_year = birth_year
    
    @classmethod
    def from_age(cls, name, age):
        current_year = date.today().year
        return cls(name, current_year - age)

p = Person.from_age("Alice", 30)
```

### 2. Parse Data

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    @classmethod
    def from_string(cls, point_str):
        x, y = map(float, point_str.split(','))
        return cls(x, y)

p = Point.from_string("3.5,2.1")
```

### 3. Multiple Formats

```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    @classmethod
    def from_string(cls, date_str):
        y, m, d = map(int, date_str.split('-'))
        return cls(y, m, d)
    
    @classmethod
    def today(cls):
        import datetime
        today = datetime.date.today()
        return cls(today.year, today.month, today.day)
```

---

## Student Example

### 1. Class Setup

```python
class Student:
    students_list = []
    mandatory = ['Chapel']
    
    def __init__(self, name, major, courses):
        self.name = name
        self.major = major
        self.courses = courses
        Student.students_list.append(self)
```

### 2. Add Mandatory Course

```python
@classmethod
def add_mandatory(cls, course):
    if course not in cls.mandatory:
        cls.mandatory.append(course)
        for student in cls.students_list:
            student.courses.append(course)
```

### 3. Drop Mandatory Course

```python
@classmethod
def drop_mandatory(cls, course):
    if course in cls.mandatory:
        cls.mandatory.remove(course)
        for student in cls.students_list:
            if course in student.courses:
                student.courses.remove(course)
```

---

## `cls` vs `self`

### 1. `cls` Parameter

```python
@classmethod
def class_method(cls):
    # cls refers to the class
    cls.class_var = 10
```

### 2. `self` Parameter

```python
def instance_method(self):
    # self refers to the instance
    self.instance_var = 10
```

### 3. Different Scopes

Class methods operate on class, instance methods on instances. See [Instance Methods](instance_methods.md) for a comparison table of all three method types.

---

## Inheritance Behavior

### 1. Inherited Methods

```python
class Parent:
    count = 0
    
    @classmethod
    def increment(cls):
        cls.count += 1

class Child(Parent):
    pass

Child.increment()
print(Child.count)  # 1
print(Parent.count) # 0
```

### 2. `cls` is Dynamic

`cls` refers to the calling class, not the class where the method was defined. Under the hood, `@classmethod` is a descriptor whose `__get__` method returns a callable
bound to the class rather than the instance:

```text
classmethod.__get__(None, Child) → function bound to Child
```

This is why `Child.increment()` sets `cls` to `Child`, not `Parent` — the
descriptor binds to whatever class triggered the attribute lookup.

### 3. Polymorphic Behavior

```python
class Shape:
    @classmethod
    def create_default(cls):
        return cls()  # Creates instance of calling class

class Circle(Shape):
    pass

c = Circle.create_default()  # Creates Circle
```

---

## When to Use

### 1. Modify Class State

```python
@classmethod
def reset_counter(cls):
    cls.counter = 0
```

### 2. Alternative Constructors

```python
@classmethod
def from_json(cls, json_str):
    data = json.loads(json_str)
    return cls(**data)
```

### 3. Affect All Instances

```python
@classmethod
def enable_feature_for_all(cls):
    cls.feature_enabled = True
```

---

## Common Patterns

### 1. Configuration

```python
class Config:
    debug_mode = False
    
    @classmethod
    def enable_debug(cls):
        cls.debug_mode = True
    
    @classmethod
    def disable_debug(cls):
        cls.debug_mode = False
```

### 2. Registry

```python
class Plugin:
    _plugins = []
    
    @classmethod
    def register(cls, plugin):
        cls._plugins.append(plugin)
    
    @classmethod
    def get_plugins(cls):
        return cls._plugins[:]
```

### 3. Singleton Pattern

```python
class Singleton:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
```

---

## Class vs Static

### 1. Class Method

```python
@classmethod
def class_method(cls, param):
    # Has access to cls
    cls.class_var = param
```

### 2. Static Method

```python
@staticmethod
def static_method(param):
    # No access to cls or self
    return param * 2
```

### 3. Choose Based on Need

Use class method when you need access to the class (e.g., modifying class state, alternative constructors). Use [static method](static_methods.md) when the function needs no access to class or instance.

---

## Key Takeaways

- Class methods receive `cls` as first parameter.
- Use `@classmethod` decorator.
- Modify class-level attributes.
- Create alternative constructors.
- Affect all instances of the class.

---



---

## Notebook Examples

```python
class Student:

    university = 'Yonsei'
    num_students = 0
    students_list = []
    mandatory = ['Chapel']

    def __init__(self, name):
        if self.is_valid_name(name):
            self.name = self.format_name(name)
            self.increase_num_student()
            self.append_student_name(name)

    @classmethod
    def increase_num_student(cls):
        cls.num_students += 1

    @classmethod
    def append_student_name(cls, name):
        cls.students_list.append(name)

    @staticmethod
    def is_valid_name(name):
        """Check if name is a non-empty string"""
        return isinstance(name, str) and len(name) > 0

    @staticmethod
    def format_name(name):
        """Capitalize the name nicely"""
        return name.strip().title()

    @staticmethod
    def school_motto():
        """Return a fixed message (no class/instance needed)"""
        return "Truth and Freedom"


# usage
print(Student.is_valid_name("Kim"))   # True
print(Student.format_name("  lee "))  # Lee
print(Student.school_motto())         # Truth and Freedom
```

---

## Exercises

**Exercise 1.**
Create a `Date` class with `year`, `month`, `day` attributes. Add a class method `from_string(date_str)` that parses a date string in `"YYYY-MM-DD"` format and returns a `Date` instance. Add another class method `today()` that returns today's date. Demonstrate both alternative constructors.

??? success "Solution to Exercise 1"

        from datetime import date

        class Date:
            def __init__(self, year, month, day):
                self.year = year
                self.month = month
                self.day = day

            @classmethod
            def from_string(cls, date_str):
                year, month, day = map(int, date_str.split("-"))
                return cls(year, month, day)

            @classmethod
            def today(cls):
                t = date.today()
                return cls(t.year, t.month, t.day)

            def __repr__(self):
                return f"Date({self.year}, {self.month}, {self.day})"

        d1 = Date.from_string("2024-03-15")
        d2 = Date.today()
        print(d1)  # Date(2024, 3, 15)
        print(d2)  # Date(today's date)

---

**Exercise 2.**
Write an `Employee` class with a class attribute `company_name` and a class method `set_company(name)` that changes it for all instances. Create instances before and after changing the company name and show that the class attribute change affects all instances.

??? success "Solution to Exercise 2"

        class Employee:
            company_name = "Acme Corp"

            def __init__(self, name):
                self.name = name

            @classmethod
            def set_company(cls, name):
                cls.company_name = name

        e1 = Employee("Alice")
        print(e1.company_name)  # Acme Corp

        Employee.set_company("New Corp")
        e2 = Employee("Bob")

        print(e1.company_name)  # New Corp — changed for all
        print(e2.company_name)  # New Corp

---

**Exercise 3.**
Build a `Currency` class with `amount` and `code`. Add class methods `from_usd(amount)`, `from_eur(amount)`, and `from_gbp(amount)` that create instances with the appropriate code. Make the class method use `cls(...)` instead of `Currency(...)` so that subclasses inherit the constructors correctly. Demonstrate with a `Crypto` subclass.

??? success "Solution to Exercise 3"

        class Currency:
            def __init__(self, amount, code):
                self.amount = amount
                self.code = code

            @classmethod
            def from_usd(cls, amount):
                return cls(amount, "USD")

            @classmethod
            def from_eur(cls, amount):
                return cls(amount, "EUR")

            @classmethod
            def from_gbp(cls, amount):
                return cls(amount, "GBP")

            def __repr__(self):
                return f"{self.__class__.__name__}({self.amount}, '{self.code}')"

        class Crypto(Currency):
            pass

        c = Crypto.from_usd(100)
        print(c)            # Crypto(100, 'USD')
        print(type(c))      # <class 'Crypto'> — cls works correctly

---

**Exercise 4.**
Consider the following hierarchy. Predict the output and explain why `cls` is different in each call, even though `increment` is defined only on `Base`.

```python
class Base:
    count = 0

    @classmethod
    def increment(cls):
        cls.count += 1
        return cls.__name__

class Alpha(Base):
    count = 0

class Beta(Base):
    count = 0

print(Alpha.increment())
print(Alpha.increment())
print(Beta.increment())
print(Base.count, Alpha.count, Beta.count)
```

??? success "Solution to Exercise 4"

        class Base:
            count = 0

            @classmethod
            def increment(cls):
                cls.count += 1
                return cls.__name__

        class Alpha(Base):
            count = 0

        class Beta(Base):
            count = 0

        print(Alpha.increment())  # "Alpha"
        print(Alpha.increment())  # "Alpha"
        print(Beta.increment())   # "Beta"
        print(Base.count, Alpha.count, Beta.count)  # 0 2 1

        # cls is dynamic: when called as Alpha.increment(), cls=Alpha,
        # so cls.count += 1 modifies Alpha.count, not Base.count.
        # This works because @classmethod is a descriptor that binds
        # the function to the calling class, not the defining class.
