# Class Attributes

Class attributes are shared across all instances of a class, storing data that belongs to the class itself. Unlike [instance attributes](instance_attributes.md) which hold per-object state, class attributes exist once on the class and are found via the [attribute lookup chain](attribute_lookup.md) when not shadowed by an instance attribute.

!!! tip "Mental Model"
    A class attribute is a sign posted on the classroom wall -- every student (instance) can read it, but if a student writes the same name on their own notebook (instance attribute), the notebook wins for that student. Reading is shared; writing is local. This read/write asymmetry is the single most common source of class-attribute confusion.

!!! tip "Core Rule"

    **Reading** an attribute via an instance may find a class attribute (through the [lookup chain](attribute_lookup.md)). **Writing** an attribute via an instance **always** creates an instance attribute, shadowing the class attribute. This asymmetry between reads and writes is the source of most class-attribute bugs.

---

## What are Class Attributes

### 1. Shared Variables

```python
class Student:
    university = 'Yonsei'  # class attribute
    
    def __init__(self, name):
        self.name = name  # instance attribute

a = Student("Lee")
b = Student("Kim")
print(a.university)  # 'Yonsei'
print(b.university)  # 'Yonsei' - same value
```

### 2. Belong to Class

```python
print(Student.university)  # Access via class
```

### 3. Single Copy

Only one copy shared by all instances.

---

## Defining Class Attributes

### 1. At Class Level

```python
class Student:
    university = 'Yonsei'     # class attribute
    num_students = 0          # class attribute
    students_list = []        # class attribute
    mandatory = ['Chapel']    # class attribute
```

### 2. Not in `__init__`

```python
class Student:
    university = 'Yonsei'  # class level
    
    def __init__(self, name):
        self.name = name  # instance level
```

### 3. Outside Methods

Defined directly in class body.

---

## Correct Usage

### 1. Modify via Class

```python
class Student:
    num_students = 0
    
    def __init__(self, name):
        self.name = name
        Student.num_students += 1  # Correct!

a = Student("Lee")
b = Student("Kim")
print(Student.num_students)  # 2
```

### 2. Shared Lists

```python
class Student:
    students_list = []
    
    def __init__(self, name):
        self.name = name
        Student.students_list.append(self)
```

### 3. Constants

```python
class Math:
    PI = 3.14159
    E = 2.71828
```

---

## Wrong Usage

### 1. Modifying via `self`

```python
# WRONG
class Student:
    num_students = 0
    
    def __init__(self, name):
        self.num_students += 1  # Creates instance attribute!

a = Student("Lee")
b = Student("Kim")
print(Student.num_students)  # Still 0!
```

### 2. Creates Instance Attribute

`self.num_students += 1` is equivalent to `self.num_students = self.num_students + 1`. The read on the right-hand side finds the class attribute (via [lookup](attribute_lookup.md)), but the write on the left-hand side creates a new entry in the instance's `__dict__`, shadowing the class attribute.

```python
a = Student("Lee")
print(a.__dict__)  # {'name': 'Lee', 'num_students': 1}
print(Student.__dict__)  # num_students still 0
```

!!! note "Connection to Attribute Lookup"

    This is a direct consequence of the [attribute lookup model](attribute_lookup.md): reading `self.num_students` (right-hand side) walks up to the class to find the value, but assigning `self.num_students = ...` (left-hand side) always writes to the instance `__dict__`. The lookup chain governs reads; writes always target the instance. Understanding this asymmetry prevents the most common class-attribute mistake.

### 3. Shadowing

Instance attribute shadows class attribute. See [Attribute Lookup](attribute_lookup.md) for the full resolution order.

---

## Class Attribute Use Cases

### 1. Counters

```python
class Student:
    count = 0
    
    def __init__(self, name):
        self.name = name
        Student.count += 1
```

### 2. Shared Configuration

```python
class Logger:
    enable_debug = False  # Shared flag
    
    def log(self, msg):
        if Logger.enable_debug:
            print(msg)
```

### 3. Default Values

```python
class Connection:
    default_timeout = 30
    
    def __init__(self, timeout=None):
        self.timeout = timeout or Connection.default_timeout
```

---

## Logger Example

### 1. Wrong: Instance Flag

```python
# WRONG - each instance has own flag
class Logger:
    enable_debug = False
    
    def print(self, msg):
        if self.enable_debug:
            print(msg)
    
    def set_debug(self):
        self.enable_debug = True  # Instance attribute!

a = Logger()
b = Logger()
a.set_debug()
a.print("hello")  # Prints
b.print("hello")  # Doesn't print
```

### 2. Correct: Class Method

```python
# CORRECT - modify class attribute
class Logger:
    enable_debug = False
    
    def print(self, msg):
        if Logger.enable_debug:
            print(msg)
    
    @classmethod
    def set_debug(cls):
        cls.enable_debug = True  # Class attribute!

a = Logger()
b = Logger()
Logger.set_debug()
a.print("hello")  # Prints
b.print("hello")  # Prints
```

### 3. Affects All Instances

Class method modifies shared state.

---

## Class `__dict__`

### 1. Read-Only Mapping

`Student.__dict__` is a **mappingproxy** --- a read-only view of the class namespace. You can read from it like a dictionary, but you cannot modify it with dict-style operations. Changes must go through normal attribute assignment.

```python
class Student:
    university = 'Yonsei'
    num_students = 0

print(Student.__dict__)
# mappingproxy({'university': 'Yonsei', 'num_students': 0, ...})

Student.__dict__['university'] = "Harvard"  # ❌ TypeError
Student.university = "Harvard"               # ✅ Works
print(Student.__dict__['university'])        # "Harvard"
```

This is different from instance `__dict__`, which is a regular writable dictionary:

| Object | Type | Writable via `__dict__` |
|---|---|---|
| `a.__dict__` (instance) | `dict` | Yes |
| `Student.__dict__` (class) | `mappingproxy` | No — use attribute assignment instead |

Python protects the class `__dict__` because it interacts with descriptors, method binding, MRO, and metaclasses.

### 2. Access Attributes

```python
print(Student.__dict__['university'])  # 'Yonsei'
```

### 3. `vars()` on Class

```python
print(vars(Student))
# Same as Student.__dict__
```

---

## Special Class Attributes

### 1. `__doc__`

```python
class Car:
    """This is a Car class."""
    pass

print(Car.__doc__)
# "This is a Car class."
```

### 2. `__name__`

```python
print(Car.__name__)  # 'Car'
```

### 3. `__module__`

```python
print(Car.__module__)  # '__main__'
```

---

## Instance vs Class

### 1. Instance `__dict__`

```python
a = Student("Lee", "Math")
print(a.__dict__)
# {'name': 'Lee', 'major': 'Math'}
```

### 2. Class `__dict__`

```python
print(Student.__dict__)
# {'university': 'Yonsei', 'num_students': 0, ...}
```

### 3. Separate Namespaces

Instance and class have different dictionaries. When you access an attribute on an instance, Python searches the instance dictionary first, then the class dictionary, then parent classes. See [Attribute Lookup](attribute_lookup.md) for the complete resolution model including descriptors.

---

## Best Practices

### 1. Use Class Name

```python
# Good
Student.num_students += 1

# Avoid
self.num_students += 1
```

### 2. Use `@classmethod`

```python
@classmethod
def increment_count(cls):
    cls.num_students += 1
```

### 3. Document Purpose

```python
class Config:
    """Global configuration settings."""
    DEBUG = False  # Class attribute for all instances
```

---

## Key Takeaways

- Class attributes are shared across instances.
- Modify via class name, not `self`.
- Using `self` creates instance attribute (shadowing).
- Use `@classmethod` for class-level operations.
- Class `__dict__` is read-only mapping.
- The read/write asymmetry (reads walk the lookup chain; writes target the instance) is the root cause of accidental shadowing.

---

## Runnable Example: `instance_vs_class_tutorial.py`

```python
"""
03: Instance vs Class Attributes and Methods

Understanding the difference between instance-level and class-level members.
"""

# ============================================================================
# Example 1: Instance vs Class Attributes
class Dog:
    # Class attribute - shared by ALL dogs
    species = "Canis familiaris"
    total_dogs = 0
    
    def __init__(self, name, age):
        # Instance attributes - unique to each dog
        self.name = name
        self.age = age
        Dog.total_dogs += 1  # Increment class attribute

if __name__ == "__main__":

    dog1 = Dog("Buddy", 3)
    dog2 = Dog("Max", 5)

    print("Instance attributes (different for each object):")
    print(f"{dog1.name} is {dog1.age} years old")
    print(f"{dog2.name} is {dog2.age} years old")

    print("\nClass attribute (same for all objects):")
    print(f"{dog1.name} is a {dog1.species}")
    print(f"{dog2.name} is a {dog2.species}")
    print(f"Total dogs created: {Dog.total_dogs}")


    # ============================================================================
    # Example 2: Class Methods
    class Employee:
        # Class attributes
        company_name = "TechCorp"
        employee_count = 0
        raise_percentage = 1.05

        def __init__(self, name, salary):
            self.name = name
            self.salary = salary
            Employee.employee_count += 1

        # Instance method (works with instance data)
        def apply_raise(self):
            self.salary = int(self.salary * Employee.raise_percentage)
            return f"{self.name}'s new salary: ${self.salary}"

        # Class method (works with class data)
        @classmethod
        def set_raise_percentage(cls, percentage):
            cls.raise_percentage = percentage

        @classmethod
        def get_employee_count(cls):
            return f"Total employees: {cls.employee_count}"

        @classmethod
        def from_string(cls, emp_string):
            # Alternative constructor
            name, salary = emp_string.split('-')
            return cls(name, int(salary))

    emp1 = Employee("Alice", 50000)
    emp2 = Employee("Bob", 60000)

    print(f"\n{Employee.get_employee_count()}")
    print(f"{emp1.apply_raise()}")

    # Using class method to change class attribute
    Employee.set_raise_percentage(1.10)
    print(f"{emp2.apply_raise()}")

    # Using alternative constructor (class method)
    emp3 = Employee.from_string("Charlie-55000")
    print(f"\nCreated employee: {emp3.name} with salary ${emp3.salary}")


    # ============================================================================
    # Example 3: Static Methods
    class MathOperations:
        """A collection of mathematical operations"""

        # Static method - doesn't use instance or class data
        @staticmethod
        def add(x, y):
            return x + y

        @staticmethod
        def multiply(x, y):
            return x * y

        @staticmethod
        def is_even(number):
            return number % 2 == 0

        @staticmethod
        def is_prime(number):
            if number < 2:
                return False
            for i in range(2, int(number ** 0.5) + 1):
                if number % i == 0:
                    return False
            return True

    # Static methods can be called without creating an instance
    print(f"\n10 + 5 = {MathOperations.add(10, 5)}")
    print(f"10 × 5 = {MathOperations.multiply(10, 5)}")
    print(f"Is 10 even? {MathOperations.is_even(10)}")
    print(f"Is 17 prime? {MathOperations.is_prime(17)}")


    # ============================================================================
    # Example 4: When to use what
    class Pizza:
        # Class attribute - shared information
        menu_prices = {"small": 8.99, "medium": 12.99, "large": 16.99}
        total_orders = 0

        def __init__(self, size, toppings):
            # Instance attributes - specific to this order
            self.size = size
            self.toppings = toppings
            self.price = self._calculate_price()
            Pizza.total_orders += 1

        # Instance method - uses instance data
        def _calculate_price(self):
            base_price = Pizza.menu_prices[self.size]
            topping_cost = len(self.toppings) * 1.50
            return base_price + topping_cost

        def get_description(self):
            toppings_str = ", ".join(self.toppings)
            return f"{self.size.capitalize()} pizza with {toppings_str} - ${self.price:.2f}"

        # Class method - works with class data
        @classmethod
        def update_price(cls, size, new_price):
            cls.menu_prices[size] = new_price

        @classmethod
        def get_total_orders(cls):
            return cls.total_orders

        # Static method - utility function, doesn't need instance or class
        @staticmethod
        def is_valid_size(size):
            return size in ["small", "medium", "large"]

    order1 = Pizza("large", ["pepperoni", "mushrooms"])
    order2 = Pizza("medium", ["cheese"])

    print(f"\n{order1.get_description()}")
    print(f"{order2.get_description()}")
    print(f"Total orders: {Pizza.get_total_orders()}")

    # Using static method
    print(f"\nIs 'extra-large' a valid size? {Pizza.is_valid_size('extra-large')}")
    print(f"Is 'medium' a valid size? {Pizza.is_valid_size('medium')}")


    # ============================================================================
    # Example 5: Comparison table
    print("\n" + "="*70)
    print("COMPARISON: Instance vs Class vs Static")
    print("="*70)

    class Example:
        class_var = "I am a class variable"

        def __init__(self, value):
            self.instance_var = value

        def instance_method(self):
            # Can access both instance and class variables
            return f"Instance: {self.instance_var}, Class: {Example.class_var}"

        @classmethod
        def class_method(cls):
            # Can only access class variables (no self)
            return f"Class method accessing: {cls.class_var}"

        @staticmethod
        def static_method():
            # Cannot access instance or class variables directly
            return "Static method - independent function"

    obj = Example("my value")
    print("\nInstance Method:", obj.instance_method())
    print("Class Method:", Example.class_method())
    print("Static Method:", Example.static_method())


    # Key Takeaways:
    # 1. INSTANCE ATTRIBUTES: Unique to each object, defined with self
    # 2. CLASS ATTRIBUTES: Shared by all objects, defined at class level
    # 3. INSTANCE METHODS: Use 'self', access instance data
    # 4. CLASS METHODS: Use '@classmethod' and 'cls', access class data
    # 5. STATIC METHODS: Use '@staticmethod', don't access instance or class data
    # 6. Access class attributes with ClassName.attribute or self.attribute
    # 7. Class methods often used as alternative constructors
    # 8. Static methods are utility functions related to the class
```

---



---

## Notebook Examples

```python
class Student:

    university = 'Yonsei' # class attribute
    num_students = 0 # class attribute
    students_list = [] # class attribute
    mandatory = ['Chapel'] # class attribute

    def __init__(self, name):
        self.name = name  # instance attribute
        Student.num_students += 1
        Student.students_list.append(name)

a = Student("Kim")
print(a.name)
print(a.university)
print(a.num_students)
print(a.students_list)
print(a.mandatory, end="\n\n")

b = Student("Lee")
print(b.name)
print(b.university)
print(b.num_students)
print(b.students_list)
print(b.mandatory)
```

```python
class Student:

    university = 'Yonsei' # class attribute
    num_students = 0 # class attribute
    students_list = [] # class attribute
    mandatory = ['Chapel'] # class attribute

    def __init__(self, name):
        self.name = name  # instance attribute
        self.increase_num_student()
        self.append_student_name(name)

    @classmethod # <--- decorator
    def increase_num_student(cls):
        cls.num_students += 1

    @classmethod # <--- decorator
    def append_student_name(cls, name):
        cls.students_list.append(name)


a = Student("Kim")
print(a.name)
print(a.university)
print(a.num_students)
print(a.students_list)
print(a.mandatory, end="\n\n")

b = Student("Lee")
print(b.name)
print(b.university)
print(b.num_students)
print(b.students_list)
print(b.mandatory, end="\n\n")

print(a.__dict__)
print(b.__dict__)
print(Student.__dict__)
```

---

## Exercises

**Exercise 1.**
Create a `BankAccount` class with a class attribute `interest_rate = 0.02` and an instance attribute `balance`. Write a method `apply_interest()` that adds `balance * interest_rate` to the balance. Create two accounts and show that changing `BankAccount.interest_rate` affects the interest calculation for both accounts, while changing `instance.interest_rate` on one account only affects that account.

??? success "Solution to Exercise 1"

        class BankAccount:
            interest_rate = 0.02

            def __init__(self, balance):
                self.balance = balance

            def apply_interest(self):
                self.balance += self.balance * self.interest_rate

        a1 = BankAccount(1000)
        a2 = BankAccount(2000)

        # Changing class attribute affects both
        BankAccount.interest_rate = 0.05
        a1.apply_interest()
        a2.apply_interest()
        print(a1.balance)  # 1050.0
        print(a2.balance)  # 2100.0

        # Changing on instance only affects that one
        a1.interest_rate = 0.10  # shadows class attribute
        a1.apply_interest()
        a2.apply_interest()
        print(a1.balance)  # 1155.0 (10% of 1050)
        print(a2.balance)  # 2205.0 (still 5% of 2100)

---

**Exercise 2.**
Design a `Registry` class that tracks all created instances using a class attribute `_instances = []`. Each time a new instance is created, append `self` to `_instances`. Add a class method `get_all()` that returns the list. Create several instances and demonstrate that `get_all()` returns them all. Then discuss the potential problem with mutable class attributes (hint: what happens with subclasses?).

??? success "Solution to Exercise 2"

        class Registry:
            _instances = []

            def __init__(self, name):
                self.name = name
                Registry._instances.append(self)

            @classmethod
            def get_all(cls):
                return cls._instances

        r1 = Registry("first")
        r2 = Registry("second")
        r3 = Registry("third")

        for r in Registry.get_all():
            print(r.name)
        # first, second, third

        # Potential problem: subclasses share the same list
        class SubRegistry(Registry):
            pass

        s = SubRegistry("sub")
        print(len(Registry.get_all()))  # 4 - includes SubRegistry!
        # Fix: use cls._instances in __init__ and define _instances per class

---

**Exercise 3.**
Write a `Counter` class with a class attribute `count = 0` that tracks how many instances have been created. Increment `count` in `__init__` using `Counter.count += 1` (not `self.count += 1`). Create a subclass `SpecialCounter` that also increments `Counter.count`. Create instances of both and show the total count. Then explain what would go wrong if you used `self.count += 1` instead.

??? success "Solution to Exercise 3"

        class Counter:
            count = 0

            def __init__(self):
                Counter.count += 1  # Modify class attribute directly

        class SpecialCounter(Counter):
            def __init__(self):
                super().__init__()

        c1 = Counter()
        c2 = Counter()
        s1 = SpecialCounter()

        print(Counter.count)  # 3 - all instances counted

        # What goes wrong with self.count += 1:
        # self.count += 1 is equivalent to self.count = self.count + 1
        # The read (self.count) finds the class attribute
        # The write (self.count = ...) creates an INSTANCE attribute
        # So the class attribute is never incremented after the first call

---

**Exercise 4.**
Create a `Settings` class with a mutable class attribute `options = {"color": "blue", "size": 10}`. In `__init__`, do NOT copy `options`. Create two instances. Mutate `options` through one instance (`self.options["color"] = "red"`) and show that both instances see the change. Now add a line `self.options = {"color": "green"}` to a third instance and inspect its `__dict__`. Explain the difference between mutating a shared mutable class attribute in place versus reassigning it on an instance, using the [attribute lookup model](attribute_lookup.md).

??? success "Solution to Exercise 4"

        class Settings:
            options = {"color": "blue", "size": 10}

            def __init__(self):
                pass

        s1 = Settings()
        s2 = Settings()

        # Mutating in place - modifies the shared class dict
        s1.options["color"] = "red"
        print(s2.options["color"])  # "red" - both see the change
        print("options" in s1.__dict__)  # False - no instance attribute created

        # Reassigning - creates an instance attribute that shadows class attr
        s3 = Settings()
        s3.options = {"color": "green"}
        print(s3.options["color"])  # "green" - instance attribute
        print(s2.options["color"])  # "red" - still sees class attribute
        print("options" in s3.__dict__)  # True - instance attribute exists

        # Key insight:
        # s1.options["color"] = "red" never assigns to s1.options itself,
        # it calls __setitem__ on the dict found via lookup (the class dict).
        # s3.options = {...} assigns to s3.options, creating an instance
        # attribute that shadows the class attribute from that point on.
