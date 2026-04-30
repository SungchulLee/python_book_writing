# Design Guidelines

Choosing between composition and inheritance is one of the most consequential design decisions in object-oriented programming. The widely cited guideline "favor composition over inheritance" exists because composition generally provides greater flexibility, simpler testing, and fewer surprises as a codebase grows. This page summarizes when each approach is appropriate and why.

## Prefer Composition

### 1. Over Inheritance

Using multiple inheritance to combine unrelated capabilities creates rigid class hierarchies that are difficult to modify. Composition lets you attach capabilities dynamically, keeping each component independent and interchangeable.

```python
# Fragile: combining unrelated capabilities via inheritance
class FlyingDog(Dog, Flying):
    pass

# Flexible: attaching capabilities via composition
class Dog:
    def __init__(self):
        self.abilities = []

    def add_ability(self, ability):
        self.abilities.append(ability)
```

With the composition approach, you can add or remove abilities at runtime without changing the class hierarchy. The inheritance approach, by contrast, locks the set of capabilities into the class definition.

## When to Use

### 1. Composition

Choose composition when the relationship between objects is best described as "has-a." The following criteria point toward composition.

- **Has-a relationship**: the object contains or uses another object as a part (e.g., a `Car` has an `Engine`).
- **Flexible behavior**: the set of capabilities may change at runtime or vary across instances.
- **Multiple components**: the object is built from several independent parts that can be developed and tested separately.

### 2. Inheritance

Choose inheritance when there is a genuine "is-a" relationship and the subclass truly represents a specialized version of the parent.

- **Is-a relationship**: the subclass is a natural specialization of the parent (e.g., a `SavingsAccount` is a `BankAccount`).
- **Shared interface**: all subclasses need to expose the same set of methods so that client code can treat them interchangeably.
- **Natural hierarchy**: the domain has a clear, shallow hierarchy that is unlikely to change frequently.

## Ambiguous Cases

Real design decisions are often not clear-cut. Some cases genuinely support either approach:

- **`Manager` and `Employee`**: a manager *is-a* employee, but a manager also *has-a* set of responsibilities that could be composed. If roles change at runtime, composition may be better.
- **`Stack` and `list`**: a stack *is-a* restricted list, but inheriting from `list` exposes methods (`insert`, `sort`) that violate the stack contract. Composition (wrapping a list) is safer.

When the choice is ambiguous, ask: **will this hierarchy need to change?** If yes, lean toward composition. If the hierarchy is small and stable, inheritance is fine. See [Is-a vs Has-a](isa_vs_hasa.md) and [Composition vs Inheritance](composition_vs_inheritance.md) for deeper comparisons.

## Summary

- Favor composition when you need flexibility, runtime configurability, or when combining unrelated behaviors.
- Use inheritance sparingly and only for genuine is-a relationships with shallow, stable hierarchies.
- **When the choice is ambiguous**, ask whether the hierarchy will need to change --- if yes, lean toward composition.
- Think about the relationship first --- if "has-a" describes it more accurately than "is-a," composition is almost always the better choice.

---

## Exercises

**Exercise 1.**
Given a scenario where you need to model `Logger` functionality for different output targets (console, file, network), explain whether inheritance or composition is more appropriate. Implement your chosen approach with a `Logger` class and interchangeable `Output` objects.

??? success "Solution to Exercise 1"

        # Composition is more appropriate: Logger "has-a" Output target
        class ConsoleOutput:
            def write(self, message):
                print(f"[CONSOLE] {message}")

        class FileOutput:
            def __init__(self, filename):
                self.filename = filename

            def write(self, message):
                print(f"[FILE:{self.filename}] {message}")

        class NetworkOutput:
            def __init__(self, url):
                self.url = url

            def write(self, message):
                print(f"[NETWORK:{self.url}] {message}")

        class Logger:
            def __init__(self, output):
                self._output = output

            def log(self, message):
                self._output.write(message)

            def set_output(self, output):
                self._output = output

        logger = Logger(ConsoleOutput())
        logger.log("Application started")
        logger.set_output(FileOutput("app.log"))
        logger.log("Switched to file output")

---

**Exercise 2.**
You have a `Vehicle` class with `start()` and `stop()` methods. You want to add `GPS`, `AirConditioning`, and `MusicPlayer` features. Implement this using composition, creating separate feature classes. Show how a `Vehicle` can have any combination of features without creating subclasses for each combination.

??? success "Solution to Exercise 2"

        class GPS:
            def status(self):
                return "GPS: Active"

        class AirConditioning:
            def __init__(self, temp=22):
                self.temp = temp

            def status(self):
                return f"AC: {self.temp}C"

        class MusicPlayer:
            def status(self):
                return "Music: Playing"

        class Vehicle:
            def __init__(self, name, features=None):
                self.name = name
                self.features = features or []

            def start(self):
                print(f"{self.name} started")

            def stop(self):
                print(f"{self.name} stopped")

            def show_features(self):
                for f in self.features:
                    print(f"  {f.status()}")

        basic = Vehicle("Sedan", [GPS()])
        luxury = Vehicle("Luxury", [GPS(), AirConditioning(18), MusicPlayer()])

        basic.start()
        basic.show_features()   # GPS: Active

        luxury.start()
        luxury.show_features()  # GPS, AC, Music — no subclasses needed

---

**Exercise 3.**
Identify a case where inheritance IS the right choice: model a `Shape` hierarchy with `Circle`, `Rectangle`, and `Triangle`. Each shape must implement `area()` and `perimeter()`. Justify why inheritance is appropriate here (is-a relationship, shared interface, stable hierarchy) and implement it.

??? success "Solution to Exercise 3"

        import math

        # Inheritance IS appropriate: Circle is-a Shape, stable hierarchy
        class Shape:
            def area(self):
                raise NotImplementedError

            def perimeter(self):
                raise NotImplementedError

            def describe(self):
                return f"{self.__class__.__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"

        class Circle(Shape):
            def __init__(self, radius):
                self.radius = radius

            def area(self):
                return math.pi * self.radius ** 2

            def perimeter(self):
                return 2 * math.pi * self.radius

        class Rectangle(Shape):
            def __init__(self, width, height):
                self.width = width
                self.height = height

            def area(self):
                return self.width * self.height

            def perimeter(self):
                return 2 * (self.width + self.height)

        class Triangle(Shape):
            def __init__(self, a, b, c):
                self.a, self.b, self.c = a, b, c

            def area(self):
                s = (self.a + self.b + self.c) / 2
                return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

            def perimeter(self):
                return self.a + self.b + self.c

        shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)]
        for s in shapes:
            print(s.describe())
