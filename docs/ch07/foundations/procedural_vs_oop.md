# Procedural vs OOP

Understanding the fundamental differences between procedural and object-oriented programming paradigms.

!!! tip "Mental Model"
    Procedural code is a recipe: step-by-step instructions that transform data passed through function parameters. OOP is a workshop: each object is a workbench with its own tools (methods) and materials (attributes), and objects collaborate by sending messages to each other. The shift from procedural to OOP is the shift from "do this to that data" to "ask this object to handle its own data."

!!! tip "Core Insight"
    Procedural programming separates data and behavior — functions receive data, transform it, and return results. OOP *binds* data and behavior together, so state changes are controlled by the object itself.

---

## Programming Paradigms

Python code can be organized around functions that transform data (procedural) or around objects that own their data and expose operations on it (OOP). The comparison below makes the trade-offs concrete.

### 1. Procedural Focus

Organized around **procedures or functions** that operate on data passed as arguments.

```python
def calculate_area(width, height):
    return width * height

def calculate_perimeter(width, height):
    return 2 * (width + height)

width = 5
height = 3
area = calculate_area(width, height)
```

### 2. OOP Focus

Organized around **objects** that encapsulate data and behavior in a single unit.

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

rect = Rectangle(5, 3)
area = rect.area()
```

### 3. Key Shift

The core change is from function-centric to object-centric design. In procedural code, functions and data live separately — you pass data into functions. In OOP, each object owns its data and exposes methods to operate on it.

---

## Comparison Table

$$
\begin{array}{lcc}
\textbf{Feature} & \textbf{Procedural} & \textbf{OOP} \\
\hline
\text{Primary Abstraction} & \text{Function} & \text{Class/Object} \\
\text{Data Encapsulation} & \text{No} & \text{Yes} \\
\text{Modularity} & \text{Function-centric} & \text{Class-centric} \\
\text{Code Reuse} & \text{Limited} & \text{Inheritance} \\
\text{State Management} & \text{External} & \text{Internal} \\
\end{array}
$$

---

## State Management

The most visible difference between the two paradigms is where state lives. In procedural code, state is stored in variables that must be passed to every function that needs them. In OOP, each object carries its own state internally.

### 1. Procedural State

State lives outside functions and must be threaded through every call.

```python
# State is external to functions
speed = 200
color = "red"

def speed_up(speed):
    return speed + 10

def print_car(speed, color):
    print(f"Speed: {speed}, Color: {color}")

speed = speed_up(speed)
print_car(speed, color)
```

### 2. OOP State

State lives inside the object and methods access it through `self`.

```python
# State is internal to objects
class Car:
    def __init__(self, speed, color):
        self.speed = speed
        self.color = color
    
    def speed_up(self):
        self.speed += 10
    
    def print_all(self):
        print(f"Speed: {self.speed}, Color: {self.color}")

ford = Car(200, "red")
ford.speed_up()
ford.print_all()
```

### 3. State Cohesion

OOP keeps related data and operations together. When state grows — adding `fuel`, `mileage`, `engine_type` — the procedural version requires updating every function signature, while the OOP version simply adds attributes and methods to the class.

---

## Code Organization

As a codebase grows, the way related functions and data are grouped determines how easy it is to navigate, test, and extend. Procedural code relies on naming conventions and file organization, while OOP uses classes as natural organizational boundaries.

### 1. Procedural Organization

```python
# Functions scattered — only naming ties them together
def create_student(name, major):
    return {"name": name, "major": major}

def add_course(student, course):
    if "courses" not in student:
        student["courses"] = []
    student["courses"].append(course)

def drop_course(student, course):
    if "courses" in student:
        student["courses"].remove(course)
```

### 2. OOP Organization

```python
# Everything bundled in class
class Student:
    def __init__(self, name, major):
        self.name = name
        self.major = major
        self.courses = []
    
    def add_course(self, course):
        self.courses.append(course)
    
    def drop_course(self, course):
        self.courses.remove(course)
```

### 3. Logical Grouping

Classes provide natural organization boundaries. With the class, discovering what operations exist on a student is as simple as inspecting `Student` — no need to search the entire module for functions that accept a `student` dictionary.

---

## When to Use Each

Neither paradigm is universally better. The right choice depends on the problem's complexity and how the code will evolve.

### 1. Use Procedural

- Simple scripts and utilities
- Mathematical computations
- Data transformations
- Quick prototypes

### 2. Use OOP

- Complex systems with multiple interacting entities
- Domains where objects have identity and lifecycle
- Projects requiring inheritance and polymorphism
- Long-term codebases that need extensible design

### 3. Hybrid Approach

Modern Python often mixes both paradigms. A data pipeline might use classes for configuration and connection pooling while keeping transformation logic as pure functions.

---

## Code Reuse

Both paradigms support reuse, but through different mechanisms. Procedural code reuses by calling shared functions. OOP adds inheritance and composition, which allow extending behavior without modifying existing code.

### 1. Procedural Reuse

```python
# Limited to function calls
def process_data(data):
    return sorted(data)

result1 = process_data(data1)
result2 = process_data(data2)
```

### 2. OOP Reuse

```python
# Inheritance and composition
class BaseProcessor:
    def process(self, data):
        return sorted(data)

class CustomProcessor(BaseProcessor):
    def process(self, data):
        data = super().process(data)
        return [x * 2 for x in data]
```

### 3. Extensibility

OOP provides more mechanisms for extension. `CustomProcessor` reuses `BaseProcessor.process` via `super()` and adds new behavior on top — without touching the base class.

---

## How Python Makes OOP Work

!!! note "Under the Hood"
    OOP in Python is built on attribute access and method binding — not a separate execution model. When you write:

    ```python
    ford.speed_up()
    ```

    Python does:

    1. Look up `speed_up` in `ford.__dict__` (instance namespace)
    2. If not found, look up in `type(ford).__dict__` (class namespace)
    3. If it's a function, bind it: `Car.speed_up.__get__(ford, Car)` → bound method
    4. Call the bound method, which passes `ford` as `self`

    This means OOP is not a special mode — it is built on the same attribute lookup and descriptor protocol that powers everything else in Python. Understanding this connection makes the transition from procedural to OOP feel natural rather than magical.

## Key Takeaways

- Procedural programming organizes code around functions that operate on external data.
- OOP organizes code around objects that encapsulate data and behavior.
- OOP provides better encapsulation, cohesion, and reuse mechanisms.
- Choose the paradigm based on problem complexity and expected growth.
- Modern Python often blends both paradigms in the same project.
- OOP in Python is built on attribute lookup and method binding — not a separate paradigm engine.

---

## Exercises

**Exercise 1.**
Write a procedural solution for managing a to-do list (using functions and a list of dicts). Then rewrite it using OOP with `Task` and `TodoList` classes. Compare the two approaches in terms of code organization and extensibility.

??? success "Solution to Exercise 1"

        # Procedural
        def create_task(title):
            return {"title": title, "done": False}

        def complete_task(tasks, title):
            for t in tasks:
                if t["title"] == title:
                    t["done"] = True

        tasks = [create_task("Buy milk"), create_task("Write code")]
        complete_task(tasks, "Buy milk")
        print(tasks)

        # OOP
        class Task:
            def __init__(self, title):
                self.title = title
                self.done = False

            def complete(self):
                self.done = True

        class TodoList:
            def __init__(self):
                self.tasks = []

            def add(self, title):
                self.tasks.append(Task(title))

            def complete(self, title):
                for t in self.tasks:
                    if t.title == title:
                        t.complete()

        todo = TodoList()
        todo.add("Buy milk")
        todo.add("Write code")
        todo.complete("Buy milk")

---

**Exercise 2.**
Implement a simple calculator both ways: procedurally (functions `add`, `subtract`, `multiply`, `divide` plus a `history` list) and with OOP (a `Calculator` class with methods and a history attribute). Show how the OOP version encapsulates state more cleanly.

??? success "Solution to Exercise 2"

        # Procedural
        history = []
        def add(a, b):
            result = a + b
            history.append(f"{a} + {b} = {result}")
            return result

        print(add(2, 3))  # 5

        # OOP
        class Calculator:
            def __init__(self):
                self.history = []

            def add(self, a, b):
                result = a + b
                self.history.append(f"{a} + {b} = {result}")
                return result

            def subtract(self, a, b):
                result = a - b
                self.history.append(f"{a} - {b} = {result}")
                return result

        calc = Calculator()
        print(calc.add(2, 3))       # 5
        print(calc.subtract(10, 4)) # 6
        print(calc.history)  # Encapsulated — each Calculator has its own

---

**Exercise 3.**
Model a library checkout system. Procedurally: use dictionaries and functions. OOP: use `Book` and `Library` classes. The system should support `checkout(title)`, `return_book(title)`, and `available()`. Show that the OOP version handles multiple libraries naturally while the procedural version requires passing state explicitly.

??? success "Solution to Exercise 3"

        # Procedural
        def create_library(name):
            return {"name": name, "books": []}

        def add_book(library, title, author):
            library["books"].append({"title": title, "author": author, "checked_out": False})

        def checkout(library, title):
            for b in library["books"]:
                if b["title"] == title and not b["checked_out"]:
                    b["checked_out"] = True
                    return True
            return False

        def return_book(library, title):
            for b in library["books"]:
                if b["title"] == title and b["checked_out"]:
                    b["checked_out"] = False
                    return True
            return False

        def available(library):
            return [b["title"] for b in library["books"] if not b["checked_out"]]

        lib = create_library("City Library")
        add_book(lib, "Python 101", "Author A")
        add_book(lib, "Data Science", "Author B")
        checkout(lib, "Python 101")
        print(available(lib))  # ['Data Science']

        # OOP
        class Book:
            def __init__(self, title, author):
                self.title = title
                self.author = author
                self.checked_out = False

        class Library:
            def __init__(self, name):
                self.name = name
                self.books = []

            def add_book(self, title, author):
                self.books.append(Book(title, author))

            def checkout(self, title):
                for b in self.books:
                    if b.title == title and not b.checked_out:
                        b.checked_out = True
                        return True
                return False

            def return_book(self, title):
                for b in self.books:
                    if b.title == title and b.checked_out:
                        b.checked_out = False
                        return True
                return False

            def available(self):
                return [b.title for b in self.books if not b.checked_out]

        lib = Library("City Library")
        lib.add_book("Python 101", "Author A")
        lib.add_book("Data Science", "Author B")
        lib.checkout("Python 101")
        print(lib.available())  # ['Data Science']

---

**Exercise 4.**
Explain in your own words why the procedural `speed_up(speed)` function in the State Management section must return the new value, while the OOP `Car.speed_up()` method does not. What does this reveal about how each paradigm handles state?

??? success "Solution to Exercise 4"

        # The procedural function receives speed as a parameter — a local copy.
        # To propagate the change, it must return the new value so the caller
        # can rebind the variable:
        #
        #   speed = speed_up(speed)
        #
        # The OOP method accesses self.speed — the object's own attribute.
        # Mutating self.speed changes the object in place, so no return is needed:
        #
        #   ford.speed_up()
        #
        # This reveals the core difference: procedural code treats data as
        # values flowing through functions, while OOP treats data as state
        # owned by objects. OOP's internal state eliminates the need to
        # thread variables through every function call.

---

**Exercise 5.**
A colleague argues that OOP is always better than procedural code. Write a short script where the procedural approach is clearly simpler and more readable than an OOP equivalent. Explain your reasoning.

??? success "Solution to Exercise 5"

        import math

        # Procedural — clean and direct
        def distance(x1, y1, x2, y2):
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        def midpoint(x1, y1, x2, y2):
            return ((x1 + x2) / 2, (y1 + y2) / 2)

        print(distance(0, 0, 3, 4))   # 5.0
        print(midpoint(0, 0, 3, 4))   # (1.5, 2.0)

        # OOP — unnecessary ceremony for a stateless computation
        class GeometryCalculator:
            def distance(self, x1, y1, x2, y2):
                return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            def midpoint(self, x1, y1, x2, y2):
                return ((x1 + x2) / 2, (y1 + y2) / 2)

        calc = GeometryCalculator()
        print(calc.distance(0, 0, 3, 4))   # 5.0
        print(calc.midpoint(0, 0, 3, 4))   # (1.5, 2.0)

        # The class adds no value here: there is no state to encapsulate,
        # no behavior to inherit, and no identity to track. The procedural
        # version is shorter, clearer, and avoids creating an object that
        # serves only as a namespace. OOP shines when objects have state
        # and lifecycle — for pure computations, functions are the right tool.
