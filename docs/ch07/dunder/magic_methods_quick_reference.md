# Python Magic Methods Quick Reference

## Most Commonly Used Magic Methods

### Initialization & Representation
| Method | Purpose | Example |
|--------|---------|---------|
| `__init__(self, ...)` | Constructor | `obj = MyClass(args)` |
| `__repr__(self)` | Developer-friendly string | `repr(obj)` |
| `__str__(self)` | User-friendly string | `str(obj)`, `print(obj)` |

### Comparison Operators
| Method | Operator | Example |
|--------|----------|---------|
| `__eq__(self, other)` | `==` | `a == b` |
| `__ne__(self, other)` | `!=` | `a != b` |
| `__lt__(self, other)` | `<` | `a < b` |
| `__le__(self, other)` | `<=` | `a <= b` |
| `__gt__(self, other)` | `>` | `a > b` |
| `__ge__(self, other)` | `>=` | `a >= b` |

### Arithmetic Operators
| Method | Operator | Example |
|--------|----------|---------|
| `__add__(self, other)` | `+` | `a + b` |
| `__sub__(self, other)` | `-` | `a - b` |
| `__mul__(self, other)` | `*` | `a * b` |
| `__truediv__(self, other)` | `/` | `a / b` |
| `__floordiv__(self, other)` | `//` | `a // b` |
| `__mod__(self, other)` | `%` | `a % b` |
| `__pow__(self, other)` | `**` | `a ** b` |

### Reverse Arithmetic (for `other + self`)
| Method | Operator | Example |
|--------|----------|---------|
| `__radd__(self, other)` | `+` | `5 + obj` |
| `__rsub__(self, other)` | `-` | `5 - obj` |
| `__rmul__(self, other)` | `*` | `5 * obj` |

### In-place Operations
| Method | Operator | Example |
|--------|----------|---------|
| `__iadd__(self, other)` | `+=` | `a += b` |
| `__isub__(self, other)` | `-=` | `a -= b` |
| `__imul__(self, other)` | `*=` | `a *= b` |

### Unary Operators
| Method | Operator | Example |
|--------|----------|---------|
| `__neg__(self)` | `-` | `-obj` |
| `__pos__(self)` | `+` | `+obj` |
| `__abs__(self)` | `abs()` | `abs(obj)` |
| `__invert__(self)` | `~` | `~obj` |

### Container Methods
| Method | Purpose | Example |
|--------|---------|---------|
| `__len__(self)` | Length | `len(obj)` |
| `__getitem__(self, key)` | Get item | `obj[key]` |
| `__setitem__(self, key, val)` | Set item | `obj[key] = val` |
| `__delitem__(self, key)` | Delete item | `del obj[key]` |
| `__contains__(self, item)` | Membership | `item in obj` |
| `__iter__(self)` | Iteration | `for x in obj` |
| `__next__(self)` | Next item | `next(obj)` |
| `__reversed__(self)` | Reverse | `reversed(obj)` |

### Type Conversion
| Method | Purpose | Example |
|--------|---------|---------|
| `__int__(self)` | Convert to int | `int(obj)` |
| `__float__(self)` | Convert to float | `float(obj)` |
| `__bool__(self)` | Convert to bool | `bool(obj)`, `if obj:` |
| `__str__(self)` | Convert to string | `str(obj)` |
| `__bytes__(self)` | Convert to bytes | `bytes(obj)` |

### Special Methods
| Method | Purpose | Example |
|--------|---------|---------|
| `__call__(self, ...)` | Make callable | `obj(args)` |
| `__hash__(self)` | Hash value | `hash(obj)`, `set([obj])` |
| `__format__(self, spec)` | String format | `f"{obj:spec}"` |

### Context Managers
| Method | Purpose | Example |
|--------|---------|---------|
| `__enter__(self)` | Enter context | `with obj:` |
| `__exit__(self, ...)` | Exit context | (automatic) |

### Attribute Access
| Method | Purpose | When Called |
|--------|---------|-------------|
| `__getattr__(self, name)` | Get missing attr | `obj.name` (if not found) |
| `__setattr__(self, name, val)` | Set any attr | `obj.name = val` |
| `__delattr__(self, name)` | Delete attr | `del obj.name` |
| `__getattribute__(self, name)` | Get any attr | `obj.name` (always) |

## Quick Tips

### When implementing `__eq__`, also implement `__hash__`
```python
def __eq__(self, other):
    return self.value == other.value

def __hash__(self):
    return hash(self.value)
```

### Return `NotImplemented` for unsupported types
```python
def __add__(self, other):
    if not isinstance(other, MyClass):
        return NotImplemented
    return MyClass(self.value + other.value)
```

### Use `object.__setattr__()` to avoid recursion
```python
def __setattr__(self, name, value):
    # Validate here
    object.__setattr__(self, name, value)
```

### Context manager pattern
```python
def __enter__(self):
    # Setup code
    return self  # or resource

def __exit__(self, exc_type, exc_val, exc_tb):
    # Cleanup code
    return False  # False = propagate exceptions
```

## Protocol Checklist

Before implementing dunder methods, use this table to identify which methods your class needs:

| Goal | Required Methods |
|---|---|
| Numeric type | `__add__`, `__mul__`, `__eq__`, `__lt__`, `__repr__`, `__hash__` |
| Sequence (read-only) | `__len__`, `__getitem__` |
| Mutable sequence | `__len__`, `__getitem__`, `__setitem__`, `__delitem__` |
| Hashable object | `__eq__` + `__hash__` (must be immutable) |
| Sortable object | `__eq__` + `__lt__` (use `@total_ordering` for the rest) |
| Context manager | `__enter__`, `__exit__` |
| Callable object | `__call__` |
| Iterable | `__iter__` (or `__getitem__` as fallback) |

## Design Rules

Only implement dunder methods when they match user expectations:

1. **Does the operation make semantic sense?** `Vector + Vector` is natural; `User + User` is not.
2. **Is it consistent?** If `a + b` works, `b + a` should too (when appropriate). Implement `__radd__`.
3. **What about other types?** Always return `NotImplemented` for unsupported types --- never raise `TypeError` directly in the method.
4. **Mutable or immutable?** Decide upfront. If immutable, implement `__hash__`. If mutable, set `__hash__ = None`.
5. **Does `__eq__` exist?** Then `__hash__` must too (or be explicitly `None`).

---

## Common Patterns

### Immutable Class (tuple-like)
Implement: `__init__`, `__repr__`, `__str__`, `__eq__`, `__hash__`, `__getitem__`, `__len__`

### Container Class (list-like)
Implement: `__init__`, `__len__`, `__getitem__`, `__setitem__`, `__delitem__`, `__contains__`, `__iter__`

### Numeric Class
Implement: `__init__`, `__repr__`, `__add__`, `__sub__`, `__mul__`, `__truediv__`, `__neg__`, `__abs__`, `__eq__`, `__lt__`

### Callable Class (function-like)
Implement: `__init__`, `__call__`, `__repr__`

### Context Manager Class
Implement: `__init__`, `__enter__`, `__exit__`

## Remember
- Magic methods should be intuitive - follow the principle of least surprise
- Always document your magic methods
- Test edge cases thoroughly
- Use `super()` when inheriting
- Consider performance implications

---

## Exercises

**Exercise 1.**
Using this reference, create a `TimeSlot` class that implements at least 6 different magic methods from different categories (representation, comparison, arithmetic, container, context manager, truth). List which magic method corresponds to which category.

??? success "Solution to Exercise 1"

        from functools import total_ordering

        @total_ordering
        class TimeSlot:
            """Uses 6+ magic methods from different categories."""

            # Lifecycle
            def __init__(self, start_hour, end_hour):
                self.start = start_hour
                self.end = end_hour

            # Representation
            def __repr__(self):
                return f"TimeSlot({self.start}, {self.end})"

            def __str__(self):
                return f"{self.start}:00-{self.end}:00"

            # Comparison
            def __eq__(self, other):
                return (self.start, self.end) == (other.start, other.end)

            def __lt__(self, other):
                return self.start < other.start

            # Arithmetic
            def __add__(self, hours):
                return TimeSlot(self.start, self.end + hours)

            # Truth
            def __bool__(self):
                return self.end > self.start

            # Container (length = duration)
            def __len__(self):
                return max(0, self.end - self.start)

        ts = TimeSlot(9, 12)
        print(repr(ts))       # Representation: TimeSlot(9, 12)
        print(str(ts))        # Representation: 9:00-12:00
        print(ts == TimeSlot(9, 12))  # Comparison: True
        print(ts + 2)         # Arithmetic: TimeSlot(9, 14)
        print(bool(ts))       # Truth: True
        print(len(ts))        # Container: 3

---

**Exercise 2.**
Write a `Config` class that uses `__getitem__` and `__setitem__` (container methods), `__contains__` (membership), `__len__` (sizing), `__repr__` (representation), and `__bool__` (truth). It should behave like a dictionary. Create and demonstrate all six methods.

??? success "Solution to Exercise 2"

        class Config:
            def __init__(self, **kwargs):
                self._data = dict(kwargs)

            def __getitem__(self, key):
                return self._data[key]

            def __setitem__(self, key, value):
                self._data[key] = value

            def __contains__(self, key):
                return key in self._data

            def __len__(self):
                return len(self._data)

            def __repr__(self):
                return f"Config({self._data})"

            def __bool__(self):
                return len(self._data) > 0

        cfg = Config(host="localhost", port=8080)
        print(cfg["host"])       # localhost
        cfg["debug"] = True
        print("debug" in cfg)    # True
        print(len(cfg))          # 3
        print(repr(cfg))         # Config({...})
        print(bool(cfg))         # True
        print(bool(Config()))    # False

---

**Exercise 3.**
Build a `FileWrapper` class that uses `__init__` (lifecycle), `__enter__`/`__exit__` (context manager), `__len__` (returns file size), `__str__` (returns filename), and `__bool__` (returns whether file has content). Simulate the file operations without actually opening files.

??? success "Solution to Exercise 3"

        class FileWrapper:
            def __init__(self, filename, content=""):
                self.filename = filename
                self.content = content
                self.is_open = False

            def __enter__(self):
                self.is_open = True
                print(f"Opened {self.filename}")
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.is_open = False
                print(f"Closed {self.filename}")
                return False

            def __len__(self):
                return len(self.content)

            def __str__(self):
                return self.filename

            def __bool__(self):
                return len(self.content) > 0

        with FileWrapper("data.txt", "Hello World") as f:
            print(str(f))      # data.txt
            print(len(f))      # 11
            print(bool(f))     # True

        print(bool(FileWrapper("empty.txt")))  # False
