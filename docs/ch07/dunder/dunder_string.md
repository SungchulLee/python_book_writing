# String Representation

These dunder methods control how objects are converted to strings.

!!! tip "Mental Model"
    `__repr__` is for developers (unambiguous, ideally copy-pasteable to recreate the object), `__str__` is for end users (clean, readable). When in doubt, implement `__repr__` first -- Python falls back to it whenever `__str__` is missing, so one good `__repr__` covers both debugging and basic display.

## __repr__: Developer Representation

`__repr__` provides an unambiguous, developer-friendly representation.

### Basic __repr__

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

p = Point(3, 4)
print(repr(p))  # Point(3, 4)
print(p)        # Point(3, 4) (uses __repr__ as fallback)
print([p])      # [Point(3, 4)]
```

### Guidelines for __repr__

```python
class User:
    def __init__(self, name, email, role='user'):
        self.name = name
        self.email = email
        self.role = role
    
    def __repr__(self):
        # Goal: Valid Python expression that recreates the object
        return f"User({self.name!r}, {self.email!r}, role={self.role!r})"

u = User("Alice", "alice@example.com", "admin")
print(repr(u))  # User('Alice', 'alice@example.com', role='admin')

# Can often recreate the object
u2 = eval(repr(u))
print(u2.name)  # Alice
```

### When Exact Repr Isn't Possible

```python
class DatabaseConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._connection = self._connect()  # Internal state
    
    def _connect(self):
        return f"<connection to {self.host}:{self.port}>"
    
    def __repr__(self):
        # Use angle brackets for non-reconstructible objects
        return f"<DatabaseConnection host={self.host!r} port={self.port}>"

conn = DatabaseConnection("localhost", 5432)
print(conn)  # <DatabaseConnection host='localhost' port=5432>
```

## __str__: User-Friendly Representation

`__str__` provides a readable, user-friendly string.

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius
    
    def __repr__(self):
        return f"Temperature({self.celsius})"
    
    def __str__(self):
        return f"{self.celsius}°C"

t = Temperature(25)
print(repr(t))  # Temperature(25)
print(str(t))   # 25°C
print(t)        # 25°C (print uses __str__)
print([t])      # [Temperature(25)] (list uses __repr__)
```

### __str__ vs __repr__ Priority

```python
# print() and str() use __str__ first, fall back to __repr__
# repr() always uses __repr__
# Containers (list, dict) always use __repr__ for elements

class Example:
    def __repr__(self):
        return "repr"
    
    def __str__(self):
        return "str"

e = Example()
print(str(e))    # str
print(repr(e))   # repr
print(e)         # str
print([e])       # [repr]
print(f"{e}")    # str
print(f"{e!r}")  # repr
```

### Always Implement __repr__

```python
# If only one: implement __repr__
# __str__ will fall back to __repr__ automatically

class MinimalClass:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"MinimalClass({self.value!r})"

m = MinimalClass("test")
print(str(m))   # MinimalClass('test')
print(repr(m))  # MinimalClass('test')
```

!!! tip "The One Rule"

    If you implement only one string method, make it `__repr__`. Python falls back to `__repr__` when `__str__` is not defined, so `print()` and `str()` will still produce useful output. The reverse is not true — if you only define `__str__`, the interactive console and containers will show the default unhelpful `<MyClass object at 0x...>` representation. Always start with `__repr__`; add `__str__` only when you need a separate user-facing format.

## __format__: Custom Formatting

`__format__` enables custom format specifications.

### Basic __format__

```python
class Money:
    def __init__(self, amount, currency='USD'):
        self.amount = amount
        self.currency = currency
    
    def __format__(self, spec):
        if spec == '':
            return f"{self.amount:.2f} {self.currency}"
        elif spec == 'short':
            return f"${self.amount:.2f}"
        elif spec == 'full':
            return f"{self.amount:.2f} {self.currency} (US Dollars)"
        else:
            # Pass spec to float formatting
            return f"{self.amount:{spec}} {self.currency}"

m = Money(1234.567)
print(f"{m}")         # 1234.57 USD
print(f"{m:short}")   # \$1234.57
print(f"{m:full}")    # 1234.57 USD (US Dollars)
print(f"{m:,.2f}")    # 1,234.57 USD
print(format(m, 'short'))  # \$1234.57
```

### Complex Format Specifications

```python
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __format__(self, spec):
        # Parse spec: [precision][format_type]
        # format_type: 'c' for cartesian, 'p' for polar-like
        
        if not spec:
            return f"({self.x}, {self.y}, {self.z})"
        
        # Extract precision and type
        precision = ''
        fmt_type = 'c'
        
        for char in spec:
            if char.isdigit() or char == '.':
                precision += char
            else:
                fmt_type = char
        
        if fmt_type == 'c':  # Cartesian
            if precision:
                return f"({self.x:{precision}f}, {self.y:{precision}f}, {self.z:{precision}f})"
            return f"({self.x}, {self.y}, {self.z})"
        elif fmt_type == 'n':  # Named
            if precision:
                return f"x={self.x:{precision}f}, y={self.y:{precision}f}, z={self.z:{precision}f}"
            return f"x={self.x}, y={self.y}, z={self.z}"
        else:
            raise ValueError(f"Unknown format type: {fmt_type}")

v = Vector(1.234, 5.678, 9.012)
print(f"{v}")        # (1.234, 5.678, 9.012)
print(f"{v:.2c}")    # (1.23, 5.68, 9.01)
print(f"{v:.1n}")    # x=1.2, y=5.7, z=9.0
```

### Datetime-Style Formatting

```python
class Person:
    def __init__(self, first, last, birth_year):
        self.first = first
        self.last = last
        self.birth_year = birth_year
    
    def __format__(self, spec):
        # %f = first, %l = last, %F = full, %y = year
        result = spec
        result = result.replace('%f', self.first)
        result = result.replace('%l', self.last)
        result = result.replace('%F', f"{self.first} {self.last}")
        result = result.replace('%y', str(self.birth_year))
        
        # If no spec, return full name
        if result == spec and not spec:
            return f"{self.first} {self.last}"
        
        return result

p = Person("Ada", "Lovelace", 1815)
print(f"{p}")              # Ada Lovelace
print(f"{p:%l, %f}")       # Lovelace, Ada
print(f"{p:%F (%y)}")      # Ada Lovelace (1815)
print(f"{p:Dr. %l}")       # Dr. Lovelace
```

## __bytes__: Bytes Representation

`__bytes__` returns a bytes representation of the object.

```python
class Message:
    def __init__(self, text, encoding='utf-8'):
        self.text = text
        self.encoding = encoding
    
    def __bytes__(self):
        return self.text.encode(self.encoding)
    
    def __str__(self):
        return self.text

msg = Message("Hello, 世界!")
print(str(msg))    # Hello, 世界!
print(bytes(msg))  # b'Hello, \xe4\xb8\x96\xe7\x95\x8c!'
```

### Binary Data Classes

```python
class Pixel:
    def __init__(self, r, g, b, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
    
    def __bytes__(self):
        return bytes([self.r, self.g, self.b, self.a])
    
    def __repr__(self):
        return f"Pixel({self.r}, {self.g}, {self.b}, {self.a})"
    
    @classmethod
    def from_bytes(cls, data):
        return cls(*data[:4])

red = Pixel(255, 0, 0)
print(bytes(red))          # b'\xff\x00\x00\xff'
print(list(bytes(red)))    # [255, 0, 0, 255]

# Round-trip
red2 = Pixel.from_bytes(bytes(red))
print(red2)  # Pixel(255, 0, 0, 255)
```

## __bool__: Truth Value

`__bool__` defines when an object is considered truthy.

```python
class Container:
    def __init__(self, items=None):
        self.items = items or []
    
    def __bool__(self):
        return len(self.items) > 0
    
    def __len__(self):
        return len(self.items)

empty = Container()
full = Container([1, 2, 3])

print(bool(empty))  # False
print(bool(full))   # True

if full:
    print("Container has items")  # Prints this
```

### __bool__ vs __len__ Fallback

```python
# If __bool__ not defined, Python uses __len__ != 0
# If neither defined, object is always truthy

class OnlyLen:
    def __init__(self, size):
        self.size = size
    
    def __len__(self):
        return self.size

print(bool(OnlyLen(0)))   # False (len is 0)
print(bool(OnlyLen(5)))   # True (len is not 0)
```

## Practical Example: Complete Class

```python
class Duration:
    """Represents a time duration."""
    
    def __init__(self, seconds):
        self.total_seconds = int(seconds)
    
    @property
    def hours(self):
        return self.total_seconds // 3600
    
    @property
    def minutes(self):
        return (self.total_seconds % 3600) // 60
    
    @property
    def seconds(self):
        return self.total_seconds % 60
    
    def __repr__(self):
        return f"Duration({self.total_seconds})"
    
    def __str__(self):
        if self.hours:
            return f"{self.hours}h {self.minutes}m {self.seconds}s"
        elif self.minutes:
            return f"{self.minutes}m {self.seconds}s"
        else:
            return f"{self.seconds}s"
    
    def __format__(self, spec):
        if spec == '':
            return str(self)
        elif spec == 'hms':
            return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"
        elif spec == 'ms':
            total_min = self.hours * 60 + self.minutes
            return f"{total_min:02d}:{self.seconds:02d}"
        elif spec == 's':
            return str(self.total_seconds)
        elif spec == 'verbose':
            parts = []
            if self.hours:
                parts.append(f"{self.hours} hour{'s' if self.hours != 1 else ''}")
            if self.minutes:
                parts.append(f"{self.minutes} minute{'s' if self.minutes != 1 else ''}")
            if self.seconds or not parts:
                parts.append(f"{self.seconds} second{'s' if self.seconds != 1 else ''}")
            return ', '.join(parts)
        else:
            raise ValueError(f"Unknown format spec: {spec}")
    
    def __bool__(self):
        return self.total_seconds > 0
    
    def __bytes__(self):
        # 4-byte big-endian representation
        return self.total_seconds.to_bytes(4, 'big')

# Usage
d = Duration(3725)  # 1h 2m 5s

print(repr(d))        # Duration(3725)
print(str(d))         # 1h 2m 5s
print(f"{d}")         # 1h 2m 5s
print(f"{d:hms}")     # 01:02:05
print(f"{d:ms}")      # 62:05
print(f"{d:s}")       # 3725
print(f"{d:verbose}") # 1 hour, 2 minutes, 5 seconds
print(bool(d))        # True
print(bytes(d))       # b'\x00\x00\x0e\x8d'

# Falsy duration
zero = Duration(0)
print(bool(zero))     # False
if not zero:
    print("No duration")  # Prints this
```

## f-string Conversion Flags

```python
class Example:
    def __repr__(self):
        return "Example()"
    
    def __str__(self):
        return "An Example"

e = Example()

# Default (uses __str__)
print(f"{e}")      # An Example

# !r forces __repr__
print(f"{e!r}")    # Example()

# !s forces __str__ (explicit)
print(f"{e!s}")    # An Example

# !a forces ascii() - escapes non-ASCII
class Unicode:
    def __repr__(self):
        return "Unicode('café')"

u = Unicode()
print(f"{u!a}")    # Unicode('caf\xe9')
```

## Key Takeaways

- Always implement `__repr__` - it's the foundation
- `__repr__` should be unambiguous and developer-friendly
- `__str__` is for end-user display; falls back to `__repr__`
- `__format__` enables custom format specifications in f-strings
- `__bytes__` is for binary/serialization representations
- `__bool__` controls truthiness; falls back to `__len__`
- Use `!r`, `!s`, `!a` in f-strings to control conversion
- Quote strings in repr with `!r`: `f"Cls({self.name!r})"`

---

## Exercises

**Exercise 1.**
Create a `Date` class with `year`, `month`, `day`. Implement `__repr__` to return `Date(2024, 3, 15)` and `__str__` to return `2024-03-15`. Also implement `__format__` to support `"{:long}"` (returns `"March 15, 2024"`) and `"{:short}"` (returns `"03/15/24"`). Default format uses `__str__`.

??? success "Solution to Exercise 1"

        class Date:
            MONTHS = ["", "January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]

            def __init__(self, year, month, day):
                self.year = year
                self.month = month
                self.day = day

            def __repr__(self):
                return f"Date({self.year}, {self.month}, {self.day})"

            def __str__(self):
                return f"{self.year}-{self.month:02d}-{self.day:02d}"

            def __format__(self, spec):
                if spec == "long":
                    return f"{self.MONTHS[self.month]} {self.day}, {self.year}"
                elif spec == "short":
                    return f"{self.month:02d}/{self.day:02d}/{self.year % 100:02d}"
                return str(self)

        d = Date(2024, 3, 15)
        print(repr(d))      # Date(2024, 3, 15)
        print(str(d))       # 2024-03-15
        print(f"{d:long}")  # March 15, 2024
        print(f"{d:short}") # 03/15/24

---

**Exercise 2.**
Write a `LogLevel` class with a `level` attribute (string like "INFO", "WARNING", "ERROR"). Implement `__repr__`, `__str__`, and `__bool__` (where "ERROR" is truthy for "has errors" checks). Show the difference between `print()`, `repr()`, and boolean context.

??? success "Solution to Exercise 2"

        class LogLevel:
            def __init__(self, level):
                self.level = level.upper()

            def __repr__(self):
                return f"LogLevel('{self.level}')"

            def __str__(self):
                return self.level

            def __bool__(self):
                return self.level == "ERROR"

        info = LogLevel("INFO")
        error = LogLevel("ERROR")

        print(info)         # INFO
        print(repr(error))  # LogLevel('ERROR')
        if error:
            print("Has errors!")  # prints
        if not info:
            print("No errors")   # prints

---

**Exercise 3.**
Create a `RichText` class with `text` and `style` attributes. Implement `__str__` (returns plain text), `__repr__` (returns `RichText('text', style='bold')`), and `__format__` (when spec is `"html"`, returns `"<b>text</b>"` for bold style). Demonstrate all three outputs.

??? success "Solution to Exercise 3"

        class RichText:
            def __init__(self, text, style="plain"):
                self.text = text
                self.style = style

            def __str__(self):
                return self.text

            def __repr__(self):
                return f"RichText({self.text!r}, style={self.style!r})"

            def __format__(self, spec):
                if spec == "html":
                    if self.style == "bold":
                        return f"<b>{self.text}</b>"
                    elif self.style == "italic":
                        return f"<i>{self.text}</i>"
                    return self.text
                return str(self)

        rt = RichText("Hello", style="bold")
        print(str(rt))       # Hello
        print(repr(rt))      # RichText('Hello', style='bold')
        print(f"{rt:html}")  # <b>Hello</b>
