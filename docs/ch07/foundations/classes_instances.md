# Classes and Instances

Understanding the building blocks of OOP: classes define structure, instances carry data.

!!! tip "Mental Model"
    A class is a cookie cutter; an instance is a cookie. The cutter defines the shape (attributes and methods), but each cookie carries its own filling (instance data). Many cookies can come from the same cutter, yet each one is independent -- changing the frosting on one does not affect the others.

!!! tip "Core Insight"
    A class couples state and behavior — the data and the operations on it live together, so each object controls its own state.

---

## Defining a Class

### 1. Basic Structure

A class groups data and behavior into a single definition.

```python
class Dog:
    # Class attribute
    species = "Canis familiaris"
    
    def __init__(self, name):
        # Instance attribute
        self.name = name
    
    def bark(self):
        return f"{self.name} says woof!"
```

### 2. Components

A class definition includes:

- **Class attributes**: data shared across all instances
- **`__init__`**: initializer that sets up instance state
- **Methods**: functions that operate on instance data via `self`

### 3. What a Class Defines

A class specifies how objects store data (attributes) and what they can do (methods). Class attributes exist on the class itself, but instance-specific data does not exist until an object is created.

---

## Creating Instances

### 1. Instantiation

Calling a class creates a new instance. Each call produces a distinct object.

```python
dog1 = Dog("Rex")
dog2 = Dog("Max")

print(dog1.name)   # Rex
print(dog2.name)   # Max
```

### 2. Independence

Each instance carries its own state. Modifying one does not affect others.

```python
print(dog1.bark())  # Rex says woof!
print(dog2.bark())  # Max says woof!

# Different objects
print(dog1 is dog2)  # False
```

### 3. Self Reference

Inside a method, `self` refers to the instance the method was called on. This is how methods access and modify instance-specific data.

---

## Class vs Instance Attributes

### 1. Class Attributes

Defined in the class body, shared by all instances.

```python
class MyClass:
    class_var = "shared"
    
    def __init__(self):
        self.instance_var = "unique"
```

### 2. Instance Attributes

Defined in `__init__` via `self`, unique to each object.

```python
obj1 = MyClass()
obj2 = MyClass()

print(obj1.class_var)      # shared
print(obj1.instance_var)   # unique
```

### 3. Lookup Order and Shadowing

When you write `obj.attr`, Python follows a lookup chain:

!!! note "Attribute Lookup Mechanism"
    ```text
    obj.attr →
        1. obj.__dict__          (instance namespace)
        2. type(obj).__dict__    (class namespace)
        3. base classes          (via MRO)
        4. descriptors           (methods, properties)
    ```
    This is why methods are found on the class (step 2), instance attributes override class attributes (step 1 wins), and `self` is automatically passed — because `type(obj).__dict__['method'].__get__(obj, type(obj))` creates a **bound method** that injects `obj` as the first argument.

Python searches the instance namespace first, then the class namespace. Assigning to an instance attribute with the same name as a class attribute creates a shadow — the class attribute remains unchanged for other instances.

```python
obj1.class_var = "new"      # Creates instance attribute — shadows class_var
print(obj1.class_var)       # "new" (instance)
print(obj2.class_var)       # "shared" (class — unchanged)
print(MyClass.class_var)    # "shared" (class — unchanged)
```

---

## Encapsulation

### 1. Public Attributes

By default, all attributes are public and can be accessed directly.

```python
class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
        self.odometer = 0

    def drive(self, miles):
        self.odometer += miles
        return f"Drove {miles} miles. Total: {self.odometer}"

car = Car("Toyota", "Camry", 2020)
print(car.drive(100))  # Drove 100 miles. Total: 100
```

### 2. Name Mangling with `__var`

Double underscores trigger name mangling — Python rewrites `self.__var` to `self._ClassName__var`. This is designed to avoid accidental name collisions in inheritance, not to enforce true access restriction.

```python
class Base:
    def __init__(self):
        self.__value = 10

class Child(Base):
    def __init__(self):
        super().__init__()
        self.__value = 20

c = Child()
print(c._Base__value)   # 10 — Base's version preserved
print(c._Child__value)  # 20 — no collision
```

### 3. Access Conventions

Python has no true private variables — it uses conventions and name rewriting.

| Name | Meaning | Enforcement |
|---|---|---|
| `self.var` | Public API | None |
| `self._var` | Internal use (convention) | None — a warning to users |
| `self.__var` | Avoid name collisions | Name mangling |

Single underscore warns users ("please don't touch"); double underscore protects against accidental override in subclasses.

---

## Key Takeaways

- A class defines how objects store data (attributes) and what they can do (methods).
- Class attributes are shared; instance attributes are unique to each object.
- `self` refers to the current instance inside methods.
- Python searches instance namespace before class namespace — assignments create shadows.
- Encapsulation protects internal state via private attributes and methods.

---

## Exercises

**Exercise 1.**
Create a `Dog` class with instance attributes `name`, `breed`, and `age`. Add methods `bark()` (returns a string), `birthday()` (increments age), and `__str__`. Create two dogs and show they are independent instances with separate state.

??? success "Solution to Exercise 1"

        class Dog:
            def __init__(self, name, breed, age):
                self.name = name
                self.breed = breed
                self.age = age

            def bark(self):
                return f"{self.name} says: Woof!"

            def birthday(self):
                self.age += 1

            def __str__(self):
                return f"{self.name} ({self.breed}, {self.age} years)"

        d1 = Dog("Buddy", "Lab", 3)
        d2 = Dog("Max", "Poodle", 5)

        print(d1)          # Buddy (Lab, 3 years)
        print(d2.bark())   # Max says: Woof!
        d1.birthday()
        print(d1.age)      # 4
        print(d2.age)      # 5 — independent

---

**Exercise 2.**
Write a `BankAccount` class with `owner` and `balance` attributes. Add `deposit(amount)`, `withdraw(amount)` (raises `ValueError` if insufficient funds), and `__repr__` methods. Create two accounts, perform transactions, and show balances are independent.

??? success "Solution to Exercise 2"

        class BankAccount:
            def __init__(self, owner, balance=0):
                self.owner = owner
                self.balance = balance

            def deposit(self, amount):
                self.balance += amount

            def withdraw(self, amount):
                if amount > self.balance:
                    raise ValueError("Insufficient funds")
                self.balance -= amount

            def __repr__(self):
                return f"BankAccount('{self.owner}', {self.balance})"

        a1 = BankAccount("Alice", 1000)
        a2 = BankAccount("Bob", 500)
        a1.deposit(200)
        a2.withdraw(100)
        print(a1)  # BankAccount('Alice', 1200)
        print(a2)  # BankAccount('Bob', 400)

---

**Exercise 3.**
Build a `Classroom` class that stores a `name` and a list of `students`. Add `enroll(student_name)`, `drop(student_name)`, and `roster()` (returns sorted list) methods. Show that `isinstance()` confirms the type, and two classrooms maintain separate student lists.

??? success "Solution to Exercise 3"

        class Classroom:
            def __init__(self, name):
                self.name = name
                self.students = []

            def enroll(self, student_name):
                if student_name not in self.students:
                    self.students.append(student_name)

            def drop(self, student_name):
                self.students.remove(student_name)

            def roster(self):
                return sorted(self.students)

        c1 = Classroom("Math 101")
        c2 = Classroom("Physics 201")
        c1.enroll("Alice")
        c1.enroll("Bob")
        c2.enroll("Charlie")

        print(c1.roster())   # ['Alice', 'Bob']
        print(c2.roster())   # ['Charlie'] — independent
        print(isinstance(c1, Classroom))  # True

---

**Exercise 4.**
Explain the difference between class attributes and instance attributes. What happens when you assign `obj.x = 5` if `x` is already a class attribute? Write a short example demonstrating attribute shadowing and show that the class attribute is unaffected.

??? success "Solution to Exercise 4"

        class Config:
            debug = False  # Class attribute

        c1 = Config()
        c2 = Config()

        # Before shadowing — both see the class attribute
        print(c1.debug)  # False
        print(c2.debug)  # False

        # Assign to instance — creates a shadow
        c1.debug = True

        print(c1.debug)         # True  (instance attribute)
        print(c2.debug)         # False (class attribute — unchanged)
        print(Config.debug)     # False (class attribute — unchanged)

        # When you assign obj.x = value, Python creates or updates
        # an instance attribute. The class attribute with the same name
        # is not modified — it is merely hidden (shadowed) for that
        # specific instance. Other instances and the class itself
        # continue to see the original class attribute.

---

**Exercise 5.**
Explain how `self` gets passed automatically when you call `dog.bark()`. Using what you know about attribute lookup and method binding, describe the steps Python takes from `dog.bark()` to executing the `bark` function with `dog` as the first argument. Verify your explanation by calling `Dog.bark(dog)` directly and showing it produces the same result.

??? success "Solution to Exercise 5"

        class Dog:
            def __init__(self, name):
                self.name = name

            def bark(self):
                return f"{self.name} says woof!"

        dog = Dog("Rex")

        # Normal call — self is passed automatically
        print(dog.bark())  # Rex says woof!

        # Manual call — equivalent to what Python does internally
        print(Dog.bark(dog))  # Rex says woof!

        # What happens step by step:
        # 1. Python looks up 'bark' in dog.__dict__ — not found
        # 2. Python looks up 'bark' in type(dog).__dict__ (Dog.__dict__) — found
        # 3. Dog.bark is a function, so the descriptor protocol kicks in:
        #      Dog.bark.__get__(dog, Dog) → bound method
        # 4. The bound method wraps the function with dog as the first argument
        # 5. Calling the bound method passes dog as 'self'
        #
        # This is why dog.bark() and Dog.bark(dog) produce the same result.
        # 'self' is not magic — it is the result of method binding through
        # the descriptor protocol.

        # Verify they are the same
        assert dog.bark() == Dog.bark(dog)
