# slots and kw_only

The `slots=True` parameter reduces memory usage by preventing `__dict__`. The `kw_only=True` parameter requires keyword-only arguments in `__init__()`.

!!! tip "Mental Model"
    `slots=True` replaces the flexible dictionary inside each instance with a fixed-size struct -- faster and leaner, but you lose the ability to add arbitrary attributes at runtime. `kw_only=True` forces callers to name every argument, eliminating positional mix-ups. Together, they trade flexibility for safety and performance.

---

## Using slots=True

```python
from dataclasses import dataclass

@dataclass(slots=True)
class Point:
    x: float
    y: float

point = Point(1.0, 2.0)
print(point)  # Point(x=1.0, y=2.0)

# Attempt to add arbitrary attributes fails
try:
    point.z = 3.0
except AttributeError as e:
    print(f"Cannot add attribute: {e}")

# Check memory usage
print(f"Point size: {point.__sizeof__()} bytes")
```

## Memory Efficiency with slots

```python
from dataclasses import dataclass
import sys

# Without slots (has __dict__)
@dataclass
class RegularPoint:
    x: float
    y: float

# With slots (no __dict__)
@dataclass(slots=True)
class SlotPoint:
    x: float
    y: float

regular = RegularPoint(1.0, 2.0)
slot = SlotPoint(1.0, 2.0)

print(f"Regular: {sys.getsizeof(regular.__dict__)} bytes for __dict__")
print(f"Slotted: no __dict__, saves memory")
```

## Using kw_only=True

```python
from dataclasses import dataclass

@dataclass(kw_only=True)
class Configuration:
    host: str
    port: int
    timeout: float = 30.0

# Must use keyword arguments
config = Configuration(host="localhost", port=8080)
print(config)  # Configuration(host='localhost', port=8080, timeout=30.0)

# Positional arguments fail
try:
    bad_config = Configuration("localhost", 8080)
except TypeError as e:
    print(f"Error: {e}")
```

## Combining slots and kw_only

```python
from dataclasses import dataclass

@dataclass(slots=True, kw_only=True)
class OptimizedConfig:
    name: str
    debug: bool = False
    workers: int = 4

config = OptimizedConfig(name="production", debug=False)
print(config)  # OptimizedConfig(name='production', debug=False, workers=4)

# Memory efficient and requires keyword arguments
```

## Per-Field kw_only

```python
from dataclasses import dataclass, field

@dataclass
class MixedArgs:
    # Positional argument
    name: str
    
    # Keyword-only arguments
    age: int = field(kw_only=True)
    email: str = field(kw_only=True)

obj = MixedArgs("Alice", age=30, email="alice@example.com")
print(obj)  # MixedArgs(name='Alice', age=30, email='alice@example.com')
```

## Performance with Slots

```python
from dataclasses import dataclass
import timeit

@dataclass
class Regular:
    x: int
    y: int

@dataclass(slots=True)
class Slotted:
    x: int
    y: int

# Attribute access is slightly faster with slots
regular = Regular(1, 2)
slotted = Slotted(1, 2)

time_regular = timeit.timeit(lambda: regular.x, number=1000000)
time_slotted = timeit.timeit(lambda: slotted.x, number=1000000)

print(f"Regular: {time_regular:.4f}s")
print(f"Slotted: {time_slotted:.4f}s")
```

## When to Use

- **slots=True**: Use when you create many instances (100k+) and memory or attribute
  access speed matters. For a handful of instances, the savings are negligible.
- **kw_only=True**: Prevent positional argument confusion, improve code clarity
- **Both**: Performance-critical code with many objects

!!! warning "When NOT to use `slots=True`"
    Slots prevent dynamic attribute assignment, which breaks patterns that rely on it:

    - **No `__dict__`**: Libraries or debugging tools that inspect `instance.__dict__`
      will fail. Monkey-patching attributes in tests also becomes impossible.
    - **Multiple inheritance friction**: If a parent class already defines `__slots__`,
      combining it with a slotted dataclass requires careful coordination to avoid
      duplicate slot definitions.
    - **Harder debugging**: Some debuggers and serializers rely on `__dict__` to
      enumerate attributes. With slots, they may show incomplete information.

    If you only create a handful of instances, the memory savings are negligible and
    the restrictions are not worth it.

!!! tip "Why `kw_only` prevents real bugs"
    Positional arguments become dangerous when a dataclass has many fields of the
    same type. Consider:

    ```python
    @dataclass
    class Transfer:
        sender: str
        receiver: str
        amount: float

    # Bug: sender and receiver are swapped, but no error raised
    t = Transfer("bob@bank.com", "alice@bank.com", 500.0)
    ```

    With `kw_only=True`, the call site must name every argument, making the swap
    immediately visible:

    ```python
    @dataclass(kw_only=True)
    class Transfer:
        sender: str
        receiver: str
        amount: float

    t = Transfer(sender="alice@bank.com", receiver="bob@bank.com", amount=500.0)
    ```

---

## Exercises

**Exercise 1.**
Create a dataclass `Point3D` with `slots=True` and fields `x`, `y`, `z` (all floats). Show that accessing attributes works normally but adding a new attribute (e.g., `p.w = 1.0`) raises `AttributeError`. Compare memory usage by creating 10,000 instances with and without slots using `sys.getsizeof`.

??? success "Solution to Exercise 1"

        from dataclasses import dataclass
        import sys

        @dataclass(slots=True)
        class Point3DSlots:
            x: float
            y: float
            z: float

        @dataclass
        class Point3DNoSlots:
            x: float
            y: float
            z: float

        p = Point3DSlots(1.0, 2.0, 3.0)
        print(p.x, p.y, p.z)  # 1.0 2.0 3.0

        try:
            p.w = 4.0  # Cannot add dynamic attributes
        except AttributeError as e:
            print(f"Error: {e}")

        # Memory comparison
        with_slots = [Point3DSlots(1.0, 2.0, 3.0) for _ in range(10000)]
        without_slots = [Point3DNoSlots(1.0, 2.0, 3.0) for _ in range(10000)]
        print(f"With slots: {sys.getsizeof(with_slots[0])} bytes per instance")
        print(f"Without slots: {sys.getsizeof(without_slots[0])} bytes per instance")

---

**Exercise 2.**
Define a dataclass `UserRecord` with `kw_only=True` and fields `name` (str), `age` (int), and `email` (str). Show that you MUST use keyword arguments to create an instance (`UserRecord(name="Alice", age=30, email="a@b.com")`). Demonstrate that positional arguments raise a `TypeError`.

??? success "Solution to Exercise 2"

        from dataclasses import dataclass

        @dataclass(kw_only=True)
        class UserRecord:
            name: str
            age: int
            email: str

        # Must use keyword arguments
        user = UserRecord(name="Alice", age=30, email="alice@example.com")
        print(user)

        try:
            bad = UserRecord("Alice", 30, "alice@example.com")
        except TypeError as e:
            print(f"Error: {e}")
            # TypeError: UserRecord.__init__() takes 1 positional argument but 4 were given

---

**Exercise 3.**
Create a dataclass `SensorReading` with `slots=True` and `kw_only=True`, containing fields `sensor_id` (str), `value` (float), `unit` (str, default `"celsius"`), and `timestamp` (str, default computed via `field(default_factory=...)`). Create multiple readings and show that both slot restrictions (no dynamic attributes) and keyword-only construction are enforced simultaneously.

??? success "Solution to Exercise 3"

        from dataclasses import dataclass, field
        from datetime import datetime

        @dataclass(slots=True, kw_only=True)
        class SensorReading:
            sensor_id: str
            value: float
            unit: str = "celsius"
            timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

        r1 = SensorReading(sensor_id="T-001", value=23.5)
        r2 = SensorReading(sensor_id="T-002", value=98.6, unit="fahrenheit")
        print(r1)
        print(r2)

        # No dynamic attributes (slots)
        try:
            r1.location = "Lab A"
        except AttributeError as e:
            print(f"Slots error: {e}")

        # Must use keywords (kw_only)
        try:
            bad = SensorReading("T-003", 50.0)
        except TypeError as e:
            print(f"kw_only error: {e}")
