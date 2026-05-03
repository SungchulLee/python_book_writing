# __post_init__ Method

The `__post_init__()` method is called after the generated `__init__()` completes, allowing you to perform additional initialization or validation.

!!! tip "Mental Model"
    The generated `__init__` handles the mechanical work of assigning arguments to fields. `__post_init__` is your callback -- the moment right after the scaffolding is up, where you can validate invariants, compute derived fields, or transform raw inputs into their final form. It separates "what the user passes in" from "what the object actually stores."

---

## Basic __post_init__ Usage

```python
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Event:
    name: str
    date: str
    duration_minutes: int
    
    def __post_init__(self):
        # Convert string to datetime
        self.date = datetime.strptime(self.date, "%Y-%m-%d")
        # Calculate end time
        self.end_time = self.date + timedelta(minutes=self.duration_minutes)

event = Event("Meeting", "2024-02-15", 60)
print(f"{event.name} on {event.date.date()} until {event.end_time.time()}")
```

## Validation in __post_init__

```python
from dataclasses import dataclass

@dataclass
class Age:
    years: int
    
    def __post_init__(self):
        if self.years < 0 or self.years > 150:
            raise ValueError(f"Invalid age: {self.years}")

try:
    invalid = Age(-5)
except ValueError as e:
    print(f"Error: {e}")

valid = Age(25)
print(f"Valid age: {valid.years}")
```

## Derived Fields

```python
from dataclasses import dataclass, field

@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)
    perimeter: float = field(init=False)
    
    def __post_init__(self):
        # Calculate derived fields
        self.area = self.width * self.height
        self.perimeter = 2 * (self.width + self.height)

rect = Rectangle(5, 10)
print(f"Area: {rect.area}, Perimeter: {rect.perimeter}")  # 50, 30
```

## Complex Initialization Logic

```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class FileConfig:
    path: str
    mode: str = "r"
    encoding: str = "utf-8"
    _file = None
    
    def __post_init__(self):
        # Validate path exists for read mode
        if self.mode == "r" and not Path(self.path).exists():
            raise FileNotFoundError(f"{self.path} not found")
        
        # Store as Path object
        self.path = Path(self.path)
        
        print(f"Initialized config for {self.path}")

try:
    config = FileConfig("/nonexistent/file.txt")
except FileNotFoundError as e:
    print(f"Error: {e}")
```

## __post_init__ with Field Modifications

```python
from dataclasses import dataclass, field

@dataclass
class Container:
    items: list = field(default_factory=list)
    
    def __post_init__(self):
        # Ensure items is always a list
        if not isinstance(self.items, list):
            self.items = list(self.items)
        
        # Sort items
        self.items.sort()

container = Container((3, 1, 2))
print(container.items)  # [1, 2, 3]
```

## Performance and Side-Effect Considerations

- `__post_init__()` runs on **every** instantiation, including copies via
  `dataclasses.replace()`. Heavy logic (file I/O, network calls, expensive
  computation) directly impacts object creation throughput.
- Keep it lightweight for frequently created objects. If you need to create
  thousands of instances in a loop, move expensive work to an explicit method
  the caller invokes after construction.
- Avoid **side effects** (writing files, sending requests, modifying global state)
  in `__post_init__`. Code that creates a dataclass does not expect I/O to happen
  as a side effect, and it makes testing harder.
- Use `__post_init__` for: validation, derived fields, and type conversions.
- **When NOT to use `__post_init__`**: if your initialization logic requires
  conditional field assignment, complex branching, or multiple construction paths,
  write a custom `__init__` instead (set `@dataclass(init=False)`) — forcing
  complex logic into `__post_init__` produces fragile, hard-to-read code.

---

## Exercises

**Exercise 1.**
Create a `Rectangle` dataclass with `width` and `height` fields. In `__post_init__`, validate that both are positive numbers (raise `ValueError` if not). Also add a derived field `area` using `field(init=False)` that is computed in `__post_init__`. Show that the validation works and the area is automatically calculated.

??? success "Solution to Exercise 1"

        from dataclasses import dataclass, field

        @dataclass
        class Rectangle:
            width: float
            height: float
            area: float = field(init=False)

            def __post_init__(self):
                if self.width <= 0 or self.height <= 0:
                    raise ValueError("Width and height must be positive")
                self.area = self.width * self.height

        r = Rectangle(5.0, 3.0)
        print(r)  # Rectangle(width=5.0, height=3.0, area=15.0)

        try:
            bad = Rectangle(-1, 5)
        except ValueError as e:
            print(f"Error: {e}")
            # Error: Width and height must be positive

---

**Exercise 2.**
Define an `Email` dataclass with a `address` field. In `__post_init__`, normalize the address to lowercase and validate that it contains `@`. If invalid, raise `ValueError`. Create valid and invalid instances to demonstrate both behaviors.

??? success "Solution to Exercise 2"

        from dataclasses import dataclass

        @dataclass
        class Email:
            address: str

            def __post_init__(self):
                self.address = self.address.lower().strip()
                if "@" not in self.address:
                    raise ValueError(f"Invalid email: {self.address}")

        e = Email("  Alice@Example.COM  ")
        print(e)  # Email(address='alice@example.com')

        try:
            bad = Email("not-an-email")
        except ValueError as e:
            print(f"Error: {e}")
            # Error: Invalid email: not-an-email

---

**Exercise 3.**
Build a `TimePeriod` dataclass with `start_date` (str in "YYYY-MM-DD" format) and `end_date` (str). In `__post_init__`, convert both strings to `datetime.date` objects (store as new attributes `_start` and `_end`), validate that `start_date` is before `end_date`, and compute a `duration_days` field (`field(init=False)`). Show the conversion and validation in action.

??? success "Solution to Exercise 3"

        from dataclasses import dataclass, field
        from datetime import date

        @dataclass
        class TimePeriod:
            start_date: str
            end_date: str
            duration_days: int = field(init=False)

            def __post_init__(self):
                self._start = date.fromisoformat(self.start_date)
                self._end = date.fromisoformat(self.end_date)
                if self._start >= self._end:
                    raise ValueError("start_date must be before end_date")
                self.duration_days = (self._end - self._start).days

        tp = TimePeriod("2024-01-01", "2024-03-15")
        print(tp)  # TimePeriod(start_date='2024-01-01', end_date='2024-03-15', duration_days=74)
        print(f"Duration: {tp.duration_days} days")

        try:
            bad = TimePeriod("2024-12-31", "2024-01-01")
        except ValueError as e:
            print(f"Error: {e}")
            # Error: start_date must be before end_date
