# Is-a vs Has-a

## Relationship Types

### 1. Fundamental Concepts

In object-oriented design, relationships between classes fall into two primary categories:

- **Is-a**: Inheritance relationship (subclass/superclass)
- **Has-a**: Composition/Aggregation relationship (container/component)

Understanding these relationships is the foundation for every design decision in this chapter. The pages on [Composition](composition_pattern.md), [Aggregation](aggregation_pattern.md), [Composition vs Inheritance](composition_vs_inheritance.md), and [Design Guidelines](design_guidelines.md) all build on the concepts introduced here.

!!! tip "Quick Rule"
    **Default to composition.** Use inheritance only when there is a true type relationship. Use aggregation when objects must be shared or outlive their container.

### 2. Identifying Relationships

Ask these questions:

- **Is-a**: "Is the subclass a specialized type of the superclass?"
- **Has-a**: "Does the class contain or use instances of another class?"

The answer guides your design choice.

### 3. Language Test

Use natural language to test relationships:

- Dog **is a** Animal ✅ (inheritance)
- Car **has a** Engine ✅ (composition)
- Student **has a** Course ✅ (aggregation)

## Is-a Relationship

### 1. Inheritance Model

The **is-a** relationship represents a hierarchical connection where the subclass is a specialized version of the superclass:

```python
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"
```

### 2. Key Characteristics

- Subclass **inherits** all attributes and methods
- Subclass can **override** inherited behavior
- Represents **generalization/specialization**
- Creates a **tight coupling** between classes

### 3. When to Use

Use inheritance when:

```python
# Clear specialization hierarchy
class Vehicle:
    pass

class Car(Vehicle):      # Car is-a Vehicle ✅
    pass

class Truck(Vehicle):    # Truck is-a Vehicle ✅
    pass

# Polymorphic behavior needed
def process_vehicle(vehicle: Vehicle):
    vehicle.start()  # Works for any Vehicle subclass
```

## Has-a Relationship

### 1. Composition Model

The **has-a** relationship represents containment where one class holds references to instances of other classes:

```python
class Engine:
    def start(self):
        return "Engine started"

class Car:
    def __init__(self):
        self.engine = Engine()  # Car has-a Engine
    
    def start(self):
        return self.engine.start()
```

### 2. Key Characteristics

- Container class **contains** component objects
- Component lifetime **depends** on container (composition)
- Component lifetime **independent** of container (aggregation)
- Creates **loose coupling** between classes

### 3. When to Use

Use composition/aggregation when:

```python
# Building from components
class Computer:
    def __init__(self):
        self.cpu = CPU()
        self.ram = RAM()
        self.storage = Storage()

# Flexible assembly
class Team:
    def __init__(self, players):
        self.players = players  # Team has-a Players
```

## Comparison

### 1. Coupling Differences

| Aspect | Is-a (Inheritance) | Has-a (Composition) |
|--------|-------------------|---------------------|
| Coupling | Tight | Loose |
| Flexibility | Less | More |
| Reusability | Limited | High |
| Change impact | High | Low |

### 2. Code Examples

**Is-a (Inheritance):**
```python
class Shape:
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
```

**Has-a (Composition):**
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Circle:
    def __init__(self, center, radius):
        self.center = center  # Has-a Point
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
```

### 3. When Each Fails

**Inheritance fails when:**
```python
# ❌ BAD: Square is-a Rectangle (violates LSP)
class Rectangle:
    def set_width(self, w):
        self.width = w
    def set_height(self, h):
        self.height = h

class Square(Rectangle):
    # Must keep width == height, but set_width/set_height
    # allow them to differ → invariant violated.
    # Code expecting a Rectangle (where width and height
    # can change independently) breaks with a Square.
    pass
```

This is the classic **Liskov Substitution** trap: mathematically a square *is* a rectangle, but in code `Square` cannot honor `Rectangle`'s contract that width and height are independently settable.

**Composition works:**
```python
# ✅ GOOD: Square has-a Shape interface
class Square:
    def __init__(self, side):
        self.side = side
    
    def area(self):
        return self.side ** 2
```

## Unified Mental Model

All OOP relationships can be understood through four dimensions:

| Dimension | Inheritance (is-a) | Composition (has-a, strong) | Aggregation (has-a, weak) |
|---|---|---|---|
| Ownership | Implicit (type system) | Container owns parts | No ownership |
| Lifetime | Tied to type | Parts die with container | Independent |
| Coupling | Tight | Moderate | Loose |
| Flexibility | Low (compile-time) | Medium | High (runtime) |

When choosing, think about **ownership** (who creates/destroys?), **lifetime** (do parts outlive the container?), **coupling** (how much does one class know about another?), and **flexibility** (can behavior change at runtime?).

!!! note "Python Reality"
    In Python, the composition vs aggregation distinction is **conceptual, not enforced**. There is no language-level mechanism that ties an object's lifetime to its container or prevents sharing. The difference is purely **design intent** — whether the container creates its parts internally (composition) or receives pre-existing objects from outside (aggregation). Python's garbage collector handles lifetime automatically based on reference counts, regardless of which pattern you intended.

## Design Guidelines

### 1. Favor Composition

Modern OOP design favors **composition over inheritance**:

```python
# Instead of deep inheritance
class Animal:
    pass

class Mammal(Animal):
    pass

class Dog(Mammal):
    pass

# Use composition
class Animal:
    def __init__(self, behavior):
        self.behavior = behavior  # Has-a Behavior
    
    def act(self):
        self.behavior.perform()
```

### 2. Mix Both Approaches

Combine inheritance and composition:

```python
class Drawable:
    """Interface through inheritance"""
    def draw(self):
        pass

class Circle(Drawable):
    def __init__(self, center, radius):
        self.center = center      # Has-a Point
        self.radius = radius
    
    def draw(self):
        # Implementation
        pass
```

### 3. Decision Tree

```
Need to model relationship?
    ↓
Is it specialization? → Use Inheritance (is-a)
    ↓
Is it containment? → Use Composition (has-a)
    ↓
Strong ownership? → Composition
    ↓
Weak ownership? → Aggregation
```

## Common Patterns

### 1. Interface Inheritance

Use inheritance for **interfaces**, composition for **implementation**:

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount):
        pass

class CreditCardProcessor(PaymentProcessor):
    def __init__(self, gateway):
        self.gateway = gateway  # Has-a Gateway
    
    def process(self, amount):
        return self.gateway.charge(amount)
```

### 2. Strategy Pattern

Combine both:

```python
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data):
        pass

class QuickSort(SortStrategy):
    def sort(self, data):
        # Quick sort implementation
        pass

class DataProcessor:
    def __init__(self, strategy):
        self.strategy = strategy  # Has-a Strategy
    
    def process(self, data):
        return self.strategy.sort(data)
```

### 3. Decorator Pattern

Composition for extending behavior:

```python
class Coffee:
    def cost(self):
        return 5

class MilkDecorator:
    def __init__(self, coffee):
        self.coffee = coffee  # Has-a Coffee
    
    def cost(self):
        return self.coffee.cost() + 2

coffee = MilkDecorator(Coffee())
print(coffee.cost())  # 7
```

## Real-World Examples

### 1. UI Components

```python
# Inheritance for type hierarchy
class Widget:
    pass

class Button(Widget):
    pass

class TextField(Widget):
    pass

# Composition for assembly
class Form:
    def __init__(self):
        self.buttons = []      # Has-a Buttons
        self.textfields = []   # Has-a TextFields
```

### 2. Game Entities

```python
# Inheritance for base entity
class GameObject:
    pass

class Character(GameObject):
    def __init__(self):
        self.position = Vector2D()  # Has-a Position
        self.health = HealthBar()   # Has-a HealthBar
        self.inventory = []         # Has-a Items
```

### 3. Business Systems

```python
# Inheritance for business entities
class Person:
    pass

class Employee(Person):
    def __init__(self, department):
        self.department = department  # Has-a Department

class Customer(Person):
    def __init__(self, orders):
        self.orders = orders  # Has-a Orders
```

## Testing Validity

### 1. Liskov Substitution

Test inheritance with LSP:

```python
def process_animal(animal: Animal):
    animal.speak()

# Should work for any subclass
process_animal(Dog())
process_animal(Cat())
```

### 2. Composition Validity

Test composition by swapping components:

```python
class Car:
    def __init__(self, engine):
        self.engine = engine

# Should work with any Engine
car1 = Car(ElectricEngine())
car2 = Car(GasEngine())
```

### 3. Relationship Questions

Ask yourself:

- Can I say "B is-a A" naturally? → Inheritance
- Can I say "B has-a A" naturally? → Composition
- Does B exist without A? → Aggregation
- Is B meaningless without A? → Composition

---

## Exercises

**Exercise 1.**
For each of the following pairs, decide whether the relationship is "is-a" (inheritance) or "has-a" (composition/aggregation), and explain why: (a) `Dog` and `Animal`, (b) `Car` and `Engine`, (c) `Manager` and `Employee`, (d) `Library` and `Book`.

??? success "Solution to Exercise 1"

        # (a) Dog is-a Animal — inheritance
        #     A dog IS a kind of animal. Natural type hierarchy.

        # (b) Car has-a Engine — composition
        #     A car is NOT an engine. It contains an engine as a part.

        # (c) Manager is-a Employee — inheritance
        #     A manager IS a specialized type of employee.

        # (d) Library has-a Book — aggregation
        #     A library contains books, but books exist independently.
        #     Books can be moved between libraries.

---

**Exercise 2.**
Model a `University` system. A `University` has-a list of `Department` objects (composition---departments don't exist without the university). Each `Department` has-a list of `Professor` objects (aggregation---professors exist independently). Implement both relationships and demonstrate the lifecycle differences.

??? success "Solution to Exercise 2"

        class Professor:
            def __init__(self, name):
                self.name = name

            def __repr__(self):
                return f"Prof({self.name})"

        class Department:
            def __init__(self, name, professors):
                self.name = name
                self.professors = professors  # Aggregation

        class University:
            def __init__(self, name, dept_names):
                # Composition: departments created here
                self.name = name
                self._departments = [Department(n, []) for n in dept_names]

            def get_department(self, name):
                for d in self._departments:
                    if d.name == name:
                        return d
                return None

        prof_a = Professor("Dr. Smith")
        prof_b = Professor("Dr. Jones")

        uni = University("MIT", ["CS", "Math"])
        cs = uni.get_department("CS")
        cs.professors.append(prof_a)
        cs.professors.append(prof_b)

        del uni  # Departments destroyed (composition)
        print(prof_a)  # Prof(Dr. Smith) — still exists (aggregation)

---

**Exercise 3.**
Create an `Employee` class with `name` and `role`. Then create `Company` that owns a list of employees (composition) and `Project` that references employees (aggregation). Show that when a `Company` is deleted, its employees are gone (if no other references exist), but employees assigned to a `Project` from an external source survive the project's deletion.

??? success "Solution to Exercise 3"

        class Employee:
            def __init__(self, name, role):
                self.name = name
                self.role = role

            def __repr__(self):
                return f"Employee('{self.name}')"

        class Company:
            def __init__(self, name):
                self.name = name
                self._employees = []  # Composition: owns employees

            def hire(self, name, role):
                emp = Employee(name, role)
                self._employees.append(emp)
                return emp

        class Project:
            def __init__(self, name, members):
                self.name = name
                self.members = members  # Aggregation: references

        company = Company("Acme")
        alice = company.hire("Alice", "Developer")
        bob = company.hire("Bob", "Designer")

        # External reference to alice for the project
        project = Project("Website", [alice])

        del project
        print(alice)  # Employee('Alice') — survives project deletion

---

**Exercise 4.**
The classic Square/Rectangle problem illustrates when "is-a" thinking goes wrong. Implement a `Rectangle` with `set_width` and `set_height` methods, and a `Square` that inherits from it. Show a function that expects a `Rectangle` (sets width and height independently) but breaks when given a `Square`. Explain the Liskov Substitution Principle violation.

??? success "Solution to Exercise 4"

        class Rectangle:
            def __init__(self, w, h):
                self._w = w
                self._h = h

            def set_width(self, w):
                self._w = w

            def set_height(self, h):
                self._h = h

            def area(self):
                return self._w * self._h

        class Square(Rectangle):
            def __init__(self, side):
                super().__init__(side, side)

            def set_width(self, w):
                self._w = w
                self._h = w  # Must keep square invariant

            def set_height(self, h):
                self._w = h
                self._h = h

        def double_width(rect: Rectangle):
            """Assumes width and height are independent."""
            old_height = rect._h
            rect.set_width(rect._w * 2)
            assert rect._h == old_height, "Height should not change!"
            return rect.area()

        r = Rectangle(4, 5)
        print(double_width(r))  # 40 — works fine

        s = Square(4)
        try:
            double_width(s)  # AssertionError: Height should not change!
        except AssertionError as e:
            print(f"LSP violation: {e}")

    **LSP violation:** `Rectangle`'s contract says width and height can change independently. `Square` breaks this contract — setting the width also changes the height. Any code that depends on independent dimensions breaks when a `Square` is substituted for a `Rectangle`. Mathematically a square *is* a rectangle, but in code the `Square` class cannot satisfy the `Rectangle` interface contract.

    **Fix:** don't inherit `Square` from `Rectangle`. Either make both independent classes implementing a `Shape` interface, or use a single `Rectangle` class with a factory method `Rectangle.square(side)`.

---

**Exercise 5.**
For each scenario below, decide whether to use inheritance, composition, or aggregation. Justify your choice using the four dimensions from the Unified Mental Model table (ownership, lifetime, coupling, flexibility).

1. A `Browser` that uses a `RenderingEngine`
2. A `Student` enrolled in multiple `Course`s
3. A `CheckingAccount` in a banking system that is a kind of `BankAccount`

??? success "Solution to Exercise 5"

    **1. Browser / RenderingEngine → Composition**

    - *Ownership:* The browser creates and owns its rendering engine.
    - *Lifetime:* The engine lives and dies with the browser.
    - *Coupling:* Moderate — the browser delegates rendering to the engine.
    - *Flexibility:* The engine could be swapped (e.g., switching from one rendering backend to another).

    A browser *has-a* rendering engine; it *is not* a rendering engine.

    **2. Student / Courses → Aggregation**

    - *Ownership:* Neither owns the other. A course exists before students enroll.
    - *Lifetime:* Students and courses have independent lifetimes.
    - *Coupling:* Loose — a student holds references to courses.
    - *Flexibility:* High — students can enroll/unenroll at runtime, and courses can be shared across students.

    A student *has* courses, but does not *own* them.

    **3. CheckingAccount / BankAccount → Inheritance**

    - *Ownership:* Type system relationship — no part/container involved.
    - *Lifetime:* The subclass *is* the superclass (same object).
    - *Coupling:* Tight, but appropriate — all bank accounts share a core interface.
    - *Flexibility:* Low, but the hierarchy is stable (account types don't change often).

    A checking account *is-a* bank account. The hierarchy is shallow and stable, and polymorphism is needed (e.g., processing a list of mixed account types).
