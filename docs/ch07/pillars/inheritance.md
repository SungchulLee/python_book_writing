# Inheritance Basics

Inheritance allows a class to reuse and extend the behavior of another, creating an **is-a** relationship with tight coupling. `super()` enables cooperative method calls across the hierarchy. Inheritance works alongside [encapsulation](encapsulation.md) (protecting state), [abstraction](abstraction.md) (defining interfaces), and [polymorphism](polymorphism.md) (enabling flexible dispatch).

!!! tip "Mental Model"
    Inheritance is a parent-child contract: the child gets everything the parent has (attributes, methods) for free, and can override or extend any part. The trade-off is tight coupling -- changes to the parent ripple into every child. Use inheritance for genuine "is-a" taxonomies (Dog is an Animal), not just to reuse code.

---

## Basic Inheritance

```python
class Animal:
    def speak(self):
        print("sound")

class Dog(Animal):
    def speak(self):
        print("bark")
```

---

## Calling Parent Methods

```python
class LoggedDog(Dog):
    def speak(self):
        super().speak()
        print("logged")
```

`super()` respects the MRO.

---

## Why Use `super()`

### 1. Multiple Inheritance

Enables cooperative inheritance patterns.

### 2. Avoids Hardcoding

No need to hardcode parent class names.

### 3. Extensible Design

Makes refactoring easier and designs more flexible.

---

## Best Practices

### 1. Use `super()` Always

In cooperative hierarchies, always use `super()` instead of hardcoding parent class names (e.g., `Parent.__init__(self, ...)`). Hardcoded calls break the MRO chain in multiple inheritance.

### 2. Keep Shallow

Prefer shallow inheritance hierarchies. Deep chains become impossible to reason about and amplify the fragile base class problem.

### 3. Prefer Composition

Use composition when you need to reuse behavior without establishing an is-a relationship. Composition gives controlled flexibility; inheritance gives tight coupling.

```python
# Composition: Bird HAS-A fly behavior
class Bird:
    def __init__(self, fly_behavior):
        self.fly_behavior = fly_behavior

# Inheritance: Penguin IS-A Bird — but can it fly?
class Penguin(Bird):
    pass  # Violates expectations if Bird.fly() exists
```

---

## Dangers of Inheritance

### 1. Tight Coupling

Subclasses depend on the parent's internal design. If the parent renames a method, changes its signature, or reorders internal calls, every subclass can silently break --- even if the subclass code itself was not touched.

```python
# Parent changes _validate() to _check() → Child breaks
class Parent:
    def save(self):
        self._check()  # was _validate()

class Child(Parent):
    def _validate(self):  # dead code now — never called
        ...
```

### 2. Fragile Base Class Problem

Adding or changing a method in a base class may break subclasses that assumed the old behavior. This is particularly dangerous when the base class is in a library you don't control --- an upgrade can break your subclass without warning.

### 3. Liskov Substitution Violations

If a subclass cannot be used everywhere the parent is expected (e.g., a `Penguin` that cannot `fly()`), the hierarchy is incorrectly modeled. Code that calls `bird.fly()` will fail at runtime for penguins, defeating the purpose of polymorphism.

### When NOT to Use Inheritance

- When the relationship is "has-a" rather than "is-a"
- When you only need one or two methods from the parent
- When the base class is likely to change frequently
- When deep hierarchies make behavior hard to trace

---

## How Inheritance Connects to the Other Pillars

Inheritance does not work in isolation:

- [Encapsulation](encapsulation.md) **protects** parent internals so subclasses don't depend on implementation details.
- [Abstraction](abstraction.md) **defines** the interface that subclasses must honor (via ABC or convention).
- [Polymorphism](polymorphism.md) **uses** the shared interface so callers don't care which subclass they hold.

When inheritance is well-designed, these four pillars reinforce each other. When it is misused (tight coupling, broken Liskov Substitution), the other pillars break down too.

!!! note "Inheritance Is Not the Goal"

    Inheritance is a **mechanism**, not an objective. Its primary purpose is to enable [polymorphism](polymorphism.md): by sharing a common interface through a base class, different subclasses become interchangeable in client code. If inheritance does not produce polymorphic substitutability, it is likely the wrong tool — consider composition instead.

---

## Key Takeaways

- Inheritance extends behavior but introduces tight coupling.
- `super()` follows the MRO --- never hardcode parent names.
- Prefer composition over inheritance when the is-a relationship is not strict.
- Watch for fragile base class and Liskov Substitution violations.

---

## Runnable Example: `inheritance_examples.py`

```python
"""
Example 01: Basic Inheritance

This example demonstrates the fundamental concept of inheritance,
where a child class inherits attributes and methods from a parent class.
"""

# Parent Class (also called Base Class or Superclass)

# =============================================================================
# Definitions
# =============================================================================

class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def eat(self):
        return f"{self.name} is eating."
    
    def sleep(self):
        return f"{self.name} is sleeping."
    
    def info(self):
        return f"{self.name} is a {self.species}."


# Child Class (also called Derived Class or Subclass)
class Dog(Animal):
    def __init__(self, name, breed):
        # Call parent constructor
        super().__init__(name, "Dog")
        self.breed = breed
    
    # Dog-specific method
    def bark(self):
        return f"{self.name} says Woof!"


class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name, "Cat")
        self.color = color
    
    # Cat-specific method
    def meow(self):
        return f"{self.name} says Meow!"


# Testing the classes

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("BASIC INHERITANCE DEMO")
    print("=" * 50)
    
    # Create a Dog object
    dog = Dog("Buddy", "Golden Retriever")
    print(f"\nDog Name: {dog.name}")
    print(f"Breed: {dog.breed}")
    print(dog.info())  # Inherited method
    print(dog.eat())   # Inherited method
    print(dog.bark())  # Dog-specific method
    
    # Create a Cat object
    cat = Cat("Whiskers", "Orange")
    print(f"\nCat Name: {cat.name}")
    print(f"Color: {cat.color}")
    print(cat.info())  # Inherited method
    print(cat.sleep()) # Inherited method
    print(cat.meow())  # Cat-specific method
    
    # Check inheritance
    print("\n" + "=" * 50)
    print("INHERITANCE VERIFICATION")
    print("=" * 50)
    print(f"Is dog an Animal? {isinstance(dog, Animal)}")
    print(f"Is dog a Dog? {isinstance(dog, Dog)}")
    print(f"Is cat an Animal? {isinstance(cat, Animal)}")
    print(f"Is dog a Cat? {isinstance(dog, Cat)}")

"""
KEY TAKEAWAYS:
1. Child classes inherit all attributes and methods from parent class
2. Use super() to call parent class constructor
3. Child classes can have their own unique methods
4. isinstance() checks if an object is an instance of a class
5. A child class object is also an instance of its parent class
"""
```


---

## Runnable Example: `method_overriding_examples.py`

```python
"""
Example 02: Method Overriding

Method overriding allows a child class to provide a specific implementation
of a method that is already defined in its parent class.
"""

# =============================================================================
# Definitions
# =============================================================================

class Shape:
    def __init__(self, name):
        self.name = name
    
    def area(self):
        return 0  # Default implementation
    
    def perimeter(self):
        return 0  # Default implementation
    
    def describe(self):
        return f"This is a {self.name}"


class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height
    
    # Override area method
    def area(self):
        return self.width * self.height
    
    # Override perimeter method
    def perimeter(self):
        return 2 * (self.width + self.height)
    
    # Override describe method
    def describe(self):
        # Call parent's describe and add more info
        parent_desc = super().describe()
        return f"{parent_desc} with width {self.width} and height {self.height}"


class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius
    
    # Override area method
    def area(self):
        return 3.14159 * self.radius ** 2
    
    # Override perimeter method (circumference)
    def perimeter(self):
        return 2 * 3.14159 * self.radius
    
    # Override describe method
    def describe(self):
        return f"{super().describe()} with radius {self.radius}"


class Triangle(Shape):
    def __init__(self, base, height, side1, side2, side3):
        super().__init__("Triangle")
        self.base = base
        self.height = height
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3
    
    # Override area method
    def area(self):
        return 0.5 * self.base * self.height
    
    # Override perimeter method
    def perimeter(self):
        return self.side1 + self.side2 + self.side3


# Testing method overriding

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("METHOD OVERRIDING DEMO")
    print("=" * 60)
    
    # Create different shapes
    shapes = [
        Rectangle(5, 3),
        Circle(4),
        Triangle(6, 4, 5, 5, 6)
    ]
    
    # Process each shape
    for shape in shapes:
        print(f"\n{shape.describe()}")
        print(f"  Area: {shape.area():.2f}")
        print(f"  Perimeter: {shape.perimeter():.2f}")
    
    # Demonstrate that the same method name gives different results
    print("\n" + "=" * 60)
    print("SAME METHOD, DIFFERENT BEHAVIOR")
    print("=" * 60)
    
    rect = Rectangle(4, 5)
    circ = Circle(3)
    
    print(f"\nrect.area() = {rect.area()}")
    print(f"circ.area() = {circ.area():.2f}")
    print("\nSame method name 'area()', but different calculations!")

"""
KEY TAKEAWAYS:
1. Child classes can override parent methods to provide specific behavior
2. Use super() to call the parent's version of the method if needed
3. Method overriding is the foundation of polymorphism
4. The overridden method must have the same name as the parent's method
5. You can completely replace or extend the parent's functionality
"""
```


---

## Runnable Example: `super_function_examples.py`

```python
"""
Example 03: Using super() Function

The super() function is used to call methods from the parent class.
This is especially useful when you want to extend (not replace) parent functionality.
"""

# =============================================================================
# Definitions
# =============================================================================

class Employee:
    def __init__(self, name, employee_id, salary):
        self.name = name
        self.employee_id = employee_id
        self.salary = salary
        print(f"Employee.__init__ called for {name}")
    
    def get_details(self):
        return f"ID: {self.employee_id}, Name: {self.name}, Salary: ${self.salary}"
    
    def calculate_bonus(self):
        return self.salary * 0.05  # 5% base bonus


class Manager(Employee):
    def __init__(self, name, employee_id, salary, department):
        # Call parent constructor using super()
        super().__init__(name, employee_id, salary)
        self.department = department
        self.team_size = 0
        print(f"Manager.__init__ called for {name}")
    
    def get_details(self):
        # Extend parent's method
        parent_details = super().get_details()
        return f"{parent_details}, Department: {self.department}, Team Size: {self.team_size}"
    
    def calculate_bonus(self):
        # Extend parent's calculation
        base_bonus = super().calculate_bonus()
        management_bonus = self.salary * 0.10  # Additional 10% for managers
        return base_bonus + management_bonus


class Developer(Employee):
    def __init__(self, name, employee_id, salary, programming_languages):
        super().__init__(name, employee_id, salary)
        self.programming_languages = programming_languages
        self.projects_completed = 0
        print(f"Developer.__init__ called for {name}")
    
    def get_details(self):
        parent_details = super().get_details()
        langs = ", ".join(self.programming_languages)
        return f"{parent_details}, Languages: {langs}, Projects: {self.projects_completed}"
    
    def calculate_bonus(self):
        base_bonus = super().calculate_bonus()
        # Bonus per project completed
        project_bonus = self.projects_completed * 500
        return base_bonus + project_bonus


class TechLead(Manager, Developer):
    """
    A TechLead is both a Manager and a Developer.

    ⚠️ WARNING: This example uses Manager.__init__() directly, which
    bypasses cooperative MRO — Developer.__init__() is never called.
    This is shown as an anti-pattern. See the corrected version below
    using super() with **kwargs for proper cooperative initialization.
    """
    def __init__(self, name, employee_id, salary, department, programming_languages):
        # ❌ Hardcoded parent call — breaks cooperative MRO!
        # Developer.__init__() is skipped entirely.
        Manager.__init__(self, name, employee_id, salary, department)
        self.programming_languages = programming_languages
        self.projects_completed = 0
        print(f"TechLead.__init__ called for {name}")
    
    def get_details(self):
        # Get base employee details
        base_details = Employee.get_details(self)
        langs = ", ".join(self.programming_languages)
        return f"{base_details}, Department: {self.department}, Languages: {langs}"
    
    def calculate_bonus(self):
        # Combines bonuses from both Manager and Developer roles
        base_bonus = Employee.calculate_bonus(self)
        management_bonus = self.salary * 0.10
        project_bonus = self.projects_completed * 500
        return base_bonus + management_bonus + project_bonus


# Testing super() usage

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SUPER() FUNCTION DEMO")
    print("=" * 70)
    
    print("\n1. Creating a Manager:")
    print("-" * 70)
    manager = Manager("Alice Johnson", "M001", 80000, "Engineering")
    manager.team_size = 5
    print(manager.get_details())
    print(f"Bonus: ${manager.calculate_bonus():.2f}")
    
    print("\n2. Creating a Developer:")
    print("-" * 70)
    dev = Developer("Bob Smith", "D001", 75000, ["Python", "JavaScript", "Go"])
    dev.projects_completed = 8
    print(dev.get_details())
    print(f"Bonus: ${dev.calculate_bonus():.2f}")
    
    print("\n3. Creating a TechLead (Multiple Inheritance):")
    print("-" * 70)
    tech_lead = TechLead("Carol Williams", "TL001", 95000, "Backend", ["Python", "Java"])
    tech_lead.team_size = 3
    tech_lead.projects_completed = 5
    print(tech_lead.get_details())
    print(f"Bonus: ${tech_lead.calculate_bonus():.2f}")
    
    print("\n" + "=" * 70)
    print("METHOD RESOLUTION ORDER (MRO)")
    print("=" * 70)
    print(f"TechLead MRO: {[cls.__name__ for cls in TechLead.__mro__]}")

"""
KEY TAKEAWAYS:
1. super() calls the parent class methods
2. Use super() to extend (not replace) parent functionality
3. super() is essential in __init__ to properly initialize parent classes
4. With multiple inheritance, super() follows the Method Resolution Order (MRO)
5. super() makes your code more maintainable and flexible
6. You can call parent methods explicitly, but super() is usually better

COMMON PATTERNS:
- super().__init__(...) - Initialize parent in child __init__
- super().method() - Call parent's method before/after child's logic
- parent_result = super().method() - Get parent's result and extend it
"""
```

---

## Exercises

**Exercise 1.** Create a base class `Shape` with a method `describe()` that returns `"I am a shape"`. Then create subclasses `Square` and `Triangle` that override `describe()` to return their specific descriptions. Verify that `isinstance(Square(...), Shape)` returns `True`.

??? success "Solution to Exercise 1"
    ```python
    class Shape:
        def describe(self):
            return "I am a shape"

    class Square(Shape):
        def __init__(self, side):
            self.side = side

        def describe(self):
            return f"I am a square with side {self.side}"

    class Triangle(Shape):
        def __init__(self, base, height):
            self.base = base
            self.height = height

        def describe(self):
            return f"I am a triangle with base {self.base} and height {self.height}"

    sq = Square(5)
    tr = Triangle(3, 4)

    print(sq.describe())                  # I am a square with side 5
    print(tr.describe())                  # I am a triangle with base 3 and height 4
    print(isinstance(sq, Shape))          # True
    print(isinstance(tr, Shape))          # True
    ```

---

**Exercise 2.** Predict the output of the following code and explain the role of `super()`.

```python
class A:
    def greet(self):
        return "Hello from A"

class B(A):
    def greet(self):
        parent = super().greet()
        return f"{parent} and B"

class C(B):
    def greet(self):
        parent = super().greet()
        return f"{parent} and C"

print(C().greet())
```

??? success "Solution to Exercise 2"
    The output is:

    ```
    Hello from A and B and C
    ```

    When `C().greet()` is called, `C.greet` calls `super().greet()`, which resolves to `B.greet` via the MRO (`C -> B -> A`). Inside `B.greet`, `super().greet()` resolves to `A.greet`, which returns `"Hello from A"`. Then `B.greet` appends `" and B"`, and finally `C.greet` appends `" and C"`. The chain builds the full string through cooperative `super()` calls.

---

**Exercise 3.** Write a class `Employee` with attributes `name` and `salary`, and a method `annual_pay()` that returns 12 times the salary. Then write a subclass `Manager` that adds a `bonus` attribute and overrides `annual_pay()` to include the bonus. Use `super()` to call the parent method.

??? success "Solution to Exercise 3"
    ```python
    class Employee:
        def __init__(self, name, salary):
            self.name = name
            self.salary = salary

        def annual_pay(self):
            return 12 * self.salary

    class Manager(Employee):
        def __init__(self, name, salary, bonus):
            super().__init__(name, salary)
            self.bonus = bonus

        def annual_pay(self):
            return super().annual_pay() + self.bonus

    emp = Employee("Alice", 5000)
    mgr = Manager("Bob", 7000, 10000)

    print(emp.annual_pay())  # 60000
    print(mgr.annual_pay())  # 94000
    ```

---

**Exercise 4.** Given the following classes, determine the Method Resolution Order (MRO) of `D` without running the code. Then verify by printing `D.__mro__`.

```python
class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass
```

??? success "Solution to Exercise 4"
    The MRO of `D` is: `D -> B -> C -> A -> object`.

    Python uses C3 linearization. Since `D` inherits from `B` then `C`, and both `B` and `C` inherit from `A`, the order is determined by preserving the local precedence order (`B` before `C`) and ensuring that `A` appears after both its children.

    ```python
    class A:
        pass

    class B(A):
        pass

    class C(A):
        pass

    class D(B, C):
        pass

    print([cls.__name__ for cls in D.__mro__])
    # ['D', 'B', 'C', 'A', 'object']
    ```

---

**Exercise 5.** Explain why the following code raises an error. Fix it so that the `Student` class properly initializes both `name` (from `Person`) and `student_id`.

```python
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, student_id):
        self.student_id = student_id

s = Student("S001")
print(s.name)  # AttributeError
```

??? success "Solution to Exercise 5"
    The error occurs because `Student.__init__` never calls `Person.__init__`, so `self.name` is never set. The fix is to accept `name` as a parameter and pass it to `super().__init__`:

    ```python
    class Person:
        def __init__(self, name):
            self.name = name

    class Student(Person):
        def __init__(self, name, student_id):
            super().__init__(name)
            self.student_id = student_id

    s = Student("Alice", "S001")
    print(s.name)        # Alice
    print(s.student_id)  # S001
    ```
