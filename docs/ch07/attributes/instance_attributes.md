# Instance Attributes

Instance attributes are variables that belong to individual object instances, storing unique state for each object. While [class attributes](class_attributes.md) are shared across all instances, instance attributes give each object its own independent data. For how Python resolves which attribute you get, see [Attribute Lookup](attribute_lookup.md).

---

## What are Instances

### 1. Definition

Attributes specific to each object instance.

```python
class Student:
    def __init__(self, name, major):
        self.name = name    # instance attribute
        self.major = major  # instance attribute

a = Student("Lee", "Math")
b = Student("Kim", "Physics")
```

### 2. Independent State

```python
print(a.name)  # "Lee"
print(b.name)  # "Kim"
# Each instance has its own values
```

### 3. Created in `__init__`

Best practice: define in constructor.

---

## Creating Attributes

### 1. In Constructor (Recommended)

```python
class Student:
    def __init__(self, name, major, courses):
        self.name = name
        self.major = major
        self.courses = courses

a = Student("Lee", "Math", ["Calculus", "Algebra"])
```

### 2. Dynamic Creation (Use with Caution)

Dynamic attribute creation is powerful and used extensively in frameworks (ORMs, serializers, configuration libraries), but it can make code harder to understand and debug when used casually.

```python
class Student:
    pass

a = Student()
a.name = "Lee"      # Created dynamically
a.major = "Math"    # Works, but bypasses __init__
```

### 3. In Methods (Sometimes)

```python
class Counter:
    def __init__(self):
        self.count = 0
    
    def start(self):
        self.start_time = time.time()  # Created in method
```

---

## Accessing Attributes

### 1. Direct Access

```python
student = Student("Lee", "Math", [])
print(student.name)   # Read
student.name = "Kim"  # Write
```

### 2. Via Methods

```python
class Student:
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
```

### 3. Using `getattr`/`setattr`

```python
name = getattr(student, 'name')
setattr(student, 'name', 'Park')
```

---

## Mutable Attributes

### 1. List Attributes

```python
class Student:
    def __init__(self, name, courses):
        self.courses = courses  # mutable list

student = Student("Lee", ["Math"])
student.courses.append("Physics")
print(student.courses)  # ["Math", "Physics"]
```

### 2. Careful with Defaults

```python
# WRONG - mutable default
class Student:
    def __init__(self, name, courses=[]):
        self.courses = courses

# CORRECT - create new list
class Student:
    def __init__(self, name, courses=None):
        self.courses = courses if courses else []
```

### 3. Dictionary Attributes

```python
class Student:
    def __init__(self, name):
        self.name = name
        self.grades = {}  # mutable dict
    
    def add_grade(self, subject, grade):
        self.grades[subject] = grade
```

---

## Attribute Patterns

### 1. Simple Data

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

### 2. Computed Once

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.area = width * height  # computed once
```

### 3. Lazy Initialization

```python
class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self._data = None  # lazy load
    
    @property
    def data(self):
        if self._data is None:
            self._data = load_file(self.filename)
        return self._data
```

---

## Special Attributes

### 1. `__dict__`

Every instance stores its attributes in a `__dict__` dictionary. This is the same dictionary that the [attribute lookup](attribute_lookup.md) mechanism consults at step 2 (after data descriptors).

```python
class Student:
    def __init__(self, name, major):
        self.name = name
        self.major = major

a = Student("Lee", "Math")
print(a.__dict__)
# {'name': 'Lee', 'major': 'Math'}
```

### 2. Modifying `__dict__`

```python
a.__dict__['age'] = 20  # Adds age attribute
print(a.age)  # 20
```

### 3. `vars()` Function

```python
print(vars(a))
# Same as a.__dict__
```

---

## Attribute Methods

### 1. Adding Attributes

```python
class Student:
    def __init__(self, name, major, courses):
        self.name = name
        self.major = major
        self.courses = courses
    
    def add_course(self, course):
        if course not in self.courses:
            self.courses.append(course)
```

### 2. Removing Attributes

```python
def drop_course(self, course):
    if course in self.courses:
        self.courses.remove(course)
```

### 3. Querying Attributes

```python
def has_course(self, course):
    return course in self.courses
```

---

## Instance vs Class

### 1. Instance Attributes

```python
class Student:
    def __init__(self, name):
        self.name = name  # instance

a = Student("Lee")
b = Student("Kim")
# Each has own name
```

### 2. Different Values

```python
a.name = "Park"
print(a.name)  # "Park"
print(b.name)  # "Kim" - unchanged
```

### 3. Independence

Changes to one instance don't affect others. For how instance attributes interact with [class attributes](class_attributes.md) of the same name (shadowing), see [Attribute Lookup](attribute_lookup.md).

---

## Common Mistakes

### 1. Forgetting `self`

```python
# WRONG
class Student:
    def __init__(self, name):
        name = name  # local variable!

# CORRECT
class Student:
    def __init__(self, name):
        self.name = name
```

### 2. Mutable Defaults

```python
# WRONG
def __init__(self, courses=[]):
    self.courses = courses

# CORRECT
def __init__(self, courses=None):
    self.courses = courses or []
```

### 3. Shadowing Names

```python
class Student:
    def __init__(self, name):
        self.name = name
    
    def process(self, name):  # parameter shadows attribute
        # Use self.name for attribute
        # Use name for parameter
        return f"{self.name} processes {name}"
```

---

## Key Takeaways

- Instance attributes store object-specific state.
- Define in `__init__` for clarity.
- Each instance has independent attributes.
- Access via `self` inside methods.
- Avoid mutable default arguments.

---

## Runnable Example: `basic_attributes_tutorial.py`

```python
"""
01: Basic Attributes in Python

Attributes are variables that belong to a class or object.
They store the state/data of an object.
"""

# ============================================================================
# Example 1: Creating a class with attributes
class Dog:
    def __init__(self, name, age, breed):
        # Instance attributes - unique to each Dog object
        self.name = name
        self.age = age
        self.breed = breed

# Creating objects (instances) of the Dog class

if __name__ == "__main__":
    dog1 = Dog("Buddy", 3, "Golden Retriever")
    dog2 = Dog("Max", 5, "German Shepherd")

    # Accessing attributes
    print(f"{dog1.name} is a {dog1.age}-year-old {dog1.breed}")
    print(f"{dog2.name} is a {dog2.age}-year-old {dog2.breed}")

    # Modifying attributes
    dog1.age = 4
    print(f"\n{dog1.name} just had a birthday! Now {dog1.age} years old")


    # ============================================================================
    # Example 2: Adding attributes after object creation
    class Person:
        def __init__(self, name):
            self.name = name

    person = Person("Alice")
    print(f"\nPerson name: {person.name}")

    # You can add new attributes dynamically (though not recommended)
    person.age = 30
    person.city = "New York"
    print(f"{person.name} is {person.age} years old and lives in {person.city}")


    # ============================================================================
    # Example 3: Default attribute values
    class BankAccount:
        def __init__(self, owner, balance=0):
            self.owner = owner
            self.balance = balance  # Default value is 0
            self.account_number = self._generate_account_number()

        def _generate_account_number(self):
            import random
            return random.randint(10000000, 99999999)

    account1 = BankAccount("John Doe", 1000)
    account2 = BankAccount("Jane Smith")  # Uses default balance of 0

    print(f"\n{account1.owner}'s account #{account1.account_number}: ${account1.balance}")
    print(f"{account2.owner}'s account #{account2.account_number}: ${account2.balance}")


    # ============================================================================
    # Example 4: Multiple types of attributes
    class Student:
        def __init__(self, name, student_id):
            self.name = name              # String
            self.student_id = student_id  # Integer
            self.grades = []              # List (mutable)
            self.enrolled = True          # Boolean
            self.gpa = 0.0                # Float

    student = Student("Emma Wilson", 12345)
    student.grades = [95, 88, 92, 90]
    print(f"\n{student.name} (ID: {student.student_id})")
    print(f"Grades: {student.grades}")
    print(f"Enrolled: {student.enrolled}")


    # Key Takeaways:
    # 1. Attributes are defined in __init__ method using self.attribute_name
    # 2. Each object has its own copy of instance attributes
    # 3. Attributes can be any data type (string, int, list, etc.)
    # 4. You can access and modify attributes using dot notation
    # 5. Default values can be provided in __init__ parameters
```

---

## Exercises

**Exercise 1.**
Create a `Person` class whose `__init__` accepts `name`, `age`, and an optional `hobbies` list (defaulting to `None`). If `hobbies` is `None`, assign an empty list. Add an `add_hobby(hobby)` method. Create two instances and show that adding a hobby to one does not affect the other. Then create a buggy version where the default is `hobbies=[]` and show the mutable default argument problem.

??? success "Solution to Exercise 1"

        # Correct version
        class Person:
            def __init__(self, name, age, hobbies=None):
                self.name = name
                self.age = age
                self.hobbies = hobbies if hobbies is not None else []

            def add_hobby(self, hobby):
                self.hobbies.append(hobby)

        p1 = Person("Alice", 30)
        p2 = Person("Bob", 25)
        p1.add_hobby("chess")
        print(p1.hobbies)  # ['chess']
        print(p2.hobbies)  # [] - independent

        # Buggy version with mutable default
        class PersonBuggy:
            def __init__(self, name, age, hobbies=[]):
                self.name = name
                self.age = age
                self.hobbies = hobbies

            def add_hobby(self, hobby):
                self.hobbies.append(hobby)

        b1 = PersonBuggy("Alice", 30)
        b2 = PersonBuggy("Bob", 25)
        b1.add_hobby("chess")
        print(b1.hobbies)  # ['chess']
        print(b2.hobbies)  # ['chess'] - shared default list!

---

**Exercise 2.**
Write a `Temperature` class with an instance attribute `_celsius` set in `__init__`. Add a method `to_fahrenheit()` that computes the conversion. Create an instance, print the Fahrenheit value, then modify `_celsius` directly and print again. Finally, add a new attribute `_label` outside of `__init__` (e.g., `t._label = "Room"`) and show it appears in `__dict__`.

??? success "Solution to Exercise 2"

        class Temperature:
            def __init__(self, celsius):
                self._celsius = celsius

            def to_fahrenheit(self):
                return self._celsius * 9 / 5 + 32

        t = Temperature(25)
        print(t.to_fahrenheit())  # 77.0

        t._celsius = 100
        print(t.to_fahrenheit())  # 212.0

        # Add attribute outside __init__
        t._label = "Room"
        print(t.__dict__)
        # {'_celsius': 100, '_label': 'Room'}

---

**Exercise 3.**
Design a `Student` class with instance attributes `name`, `grades` (a list), and `enrolled` (a boolean, default `True`). Add methods `add_grade(grade)`, `average()`, and `drop()` (sets enrolled to `False`). Create two students, add different grades, drop one, and print both students' states. Use `vars()` to inspect each instance's `__dict__`.

??? success "Solution to Exercise 3"

        class Student:
            def __init__(self, name, grades=None, enrolled=True):
                self.name = name
                self.grades = grades if grades is not None else []
                self.enrolled = enrolled

            def add_grade(self, grade):
                self.grades.append(grade)

            def average(self):
                if not self.grades:
                    return 0.0
                return sum(self.grades) / len(self.grades)

            def drop(self):
                self.enrolled = False

        s1 = Student("Alice")
        s2 = Student("Bob")

        s1.add_grade(90)
        s1.add_grade(85)
        s2.add_grade(70)
        s2.add_grade(75)
        s2.add_grade(80)

        s1.drop()

        print(f"{s1.name}: avg={s1.average()}, enrolled={s1.enrolled}")
        # Alice: avg=87.5, enrolled=False
        print(f"{s2.name}: avg={s2.average()}, enrolled={s2.enrolled}")
        # Bob: avg=75.0, enrolled=True

        print(vars(s1))
        # {'name': 'Alice', 'grades': [90, 85], 'enrolled': False}
        print(vars(s2))
        # {'name': 'Bob', 'grades': [70, 75, 80], 'enrolled': True}

---

**Exercise 4.**
Debug the following class. Predict what `print(a.x, b.x)` outputs and explain why. Then fix the code so that each instance tracks its own count independently.

```python
class Broken:
    x = 0
    def __init__(self):
        self.x += 1

a = Broken()
b = Broken()
print(a.x, b.x)
print(Broken.x)
```

??? success "Solution to Exercise 4"

        class Broken:
            x = 0
            def __init__(self):
                self.x += 1

        a = Broken()
        b = Broken()
        print(a.x, b.x)   # 1 1
        print(Broken.x)    # 0

        # Explanation:
        # self.x += 1 is self.x = self.x + 1
        # On the right side, self.x finds class attribute x = 0 (via lookup)
        # On the left side, self.x = ... creates an INSTANCE attribute
        # So each instance gets its own x = 1, and Broken.x stays 0
        #
        # This is the shadowing trap described in Attribute Lookup.

        # Fixed version - use a proper instance attribute
        class Fixed:
            def __init__(self):
                self.x = 0  # explicit instance attribute
                self.x += 1

        a = Fixed()
        b = Fixed()
        print(a.x, b.x)  # 1 1 - each has own independent counter
