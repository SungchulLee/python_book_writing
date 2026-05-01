# Arithmetic Operators

Arithmetic dunder methods enable mathematical operations on custom objects through operator overloading. Before implementing them, ask: **does this operation make semantic sense for the class?** `Vector + Vector` is natural; `User + User` is not. If the meaning of `+` is not immediately obvious without reading the source, use a named method instead.

## Basic Arithmetic Operations

### Addition: `__add__`

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)  # Vector(4, 6)
```

### All Basic Operations

Every arithmetic method should type-check its operand and return `NotImplemented` for unsupported types. This allows Python to try the reflected operation on the other operand instead of crashing.

```python
class Number:
    def __init__(self, value):
        self.value = value
    
    def __add__(self, other):       # self + other
        if not isinstance(other, Number):
            return NotImplemented
        return Number(self.value + other.value)
    
    def __sub__(self, other):       # self - other
        if not isinstance(other, Number):
            return NotImplemented
        return Number(self.value - other.value)
    
    def __mul__(self, other):       # self * other
        if not isinstance(other, Number):
            return NotImplemented
        return Number(self.value * other.value)
    
    def __truediv__(self, other):   # self / other
        if not isinstance(other, Number):
            return NotImplemented
        return Number(self.value / other.value)
    
    def __floordiv__(self, other):  # self // other
        if not isinstance(other, Number):
            return NotImplemented
        return Number(self.value // other.value)
    
    def __mod__(self, other):       # self % other
        if not isinstance(other, Number):
            return NotImplemented
        return Number(self.value % other.value)
    
    def __pow__(self, other):       # self ** other
        if not isinstance(other, Number):
            return NotImplemented
        return Number(self.value ** other.value)
    
    def __repr__(self):
        return f"Number({self.value})"
```

### Operator Summary Table

| Method | Operator | Example |
|--------|----------|---------|
| `__add__` | `+` | `a + b` |
| `__sub__` | `-` | `a - b` |
| `__mul__` | `*` | `a * b` |
| `__truediv__` | `/` | `a / b` |
| `__floordiv__` | `//` | `a // b` |
| `__mod__` | `%` | `a % b` |
| `__pow__` | `**` | `a ** b` |
| `__matmul__` | `@` | `a @ b` |

## Unary Operators

```python
class Number:
    def __init__(self, value):
        self.value = value
    
    def __neg__(self):      # -self
        return Number(-self.value)
    
    def __pos__(self):      # +self
        return Number(+self.value)
    
    def __abs__(self):      # abs(self)
        return Number(abs(self.value))
    
    def __invert__(self):   # ~self (bitwise NOT)
        return Number(~self.value)
    
    def __repr__(self):
        return f"Number({self.value})"

n = Number(-5)
print(-n)      # Number(5)
print(abs(n))  # Number(5)
```

## Reflected (Right) Operations

When the left operand doesn't support the operation, Python tries the right operand's reflected method.

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __mul__(self, scalar):
        """Vector * scalar"""
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        return NotImplemented
    
    def __rmul__(self, scalar):
        """scalar * Vector (when scalar.__mul__ fails)"""
        return self.__mul__(scalar)
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v = Vector(1, 2)
print(v * 3)    # Vector(3, 6)  - uses __mul__
print(3 * v)    # Vector(3, 6)  - uses __rmul__
```

### How Reflected Operations Work

```
3 * v
  ↓
int.__mul__(3, v) → NotImplemented
  ↓
Vector.__rmul__(v, 3) → Vector(3, 6)
```

!!! note "Subclass Priority"

    If the right operand's type is a **subclass** of the left operand's type, Python tries the right operand's reflected method **first**, before the left operand's forward method. This ensures that subclasses can override the behavior of their parent's operators. For example, if `B` is a subclass of `A`, then `a + b` tries `B.__radd__(b, a)` before `A.__add__(a, b)`. Without this rule, a subclass could never customize how it interacts with its parent type.

### All Reflected Methods

| Regular | Reflected | When Used |
|---------|-----------|-----------|
| `__add__` | `__radd__` | `other + self` |
| `__sub__` | `__rsub__` | `other - self` |
| `__mul__` | `__rmul__` | `other * self` |
| `__truediv__` | `__rtruediv__` | `other / self` |
| `__floordiv__` | `__rfloordiv__` | `other // self` |
| `__mod__` | `__rmod__` | `other % self` |
| `__pow__` | `__rpow__` | `other ** self` |
| `__matmul__` | `__rmatmul__` | `other @ self` |

## In-Place Operations

In-place operations modify the object and return `self`.

```python
class Counter:
    def __init__(self, value=0):
        self.value = value
    
    def __iadd__(self, other):
        """self += other"""
        self.value += other
        return self  # Must return self!
    
    def __isub__(self, other):
        """self -= other"""
        self.value -= other
        return self
    
    def __imul__(self, other):
        """self *= other"""
        self.value *= other
        return self
    
    def __repr__(self):
        return f"Counter({self.value})"

c = Counter(10)
print(id(c))    # 140234567890
c += 5
print(c)        # Counter(15)
print(id(c))    # 140234567890 (same object!)
```

### Mutable vs Immutable In-Place

Whether `+=` modifies the object in place or creates a new one is a **deliberate design decision**, not an implementation detail. Choose one style and be consistent:

- **Mutable** (`__iadd__` returns `self`): efficient, but shared references see the change.
- **Immutable** (no `__iadd__`, falls back to `__add__` + rebind): safer, but allocates a new object.

```python
# Mutable: modify in place
class MutableVector:
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self  # Same object

# Immutable: return new object
class ImmutableVector:
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def __add__(self, other):
        return ImmutableVector(self.x + other.x, self.y + other.y)
    
    # No __iadd__ - += will use __add__ and rebind
```

### All In-Place Methods

| Method | Operator | Effect |
|--------|----------|--------|
| `__iadd__` | `+=` | Add in place |
| `__isub__` | `-=` | Subtract in place |
| `__imul__` | `*=` | Multiply in place |
| `__itruediv__` | `/=` | Divide in place |
| `__ifloordiv__` | `//=` | Floor divide in place |
| `__imod__` | `%=` | Modulo in place |
| `__ipow__` | `**=` | Power in place |
| `__imatmul__` | `@=` | Matrix multiply in place |

## Bitwise Operations

```python
class Flags:
    def __init__(self, value=0):
        self.value = value
    
    def __and__(self, other):       # self & other
        return Flags(self.value & other.value)
    
    def __or__(self, other):        # self | other
        return Flags(self.value | other.value)
    
    def __xor__(self, other):       # self ^ other
        return Flags(self.value ^ other.value)
    
    def __invert__(self):           # ~self
        return Flags(~self.value)
    
    def __lshift__(self, n):        # self << n
        return Flags(self.value << n)
    
    def __rshift__(self, n):        # self >> n
        return Flags(self.value >> n)
    
    def __repr__(self):
        return f"Flags(0b{self.value:08b})"

READ = Flags(0b001)
WRITE = Flags(0b010)
EXECUTE = Flags(0b100)

permissions = READ | WRITE
print(permissions)           # Flags(0b00000011)
print(permissions & READ)    # Flags(0b00000001)
```

### Bitwise Method Summary

| Method | Operator | Reflected | In-Place |
|--------|----------|-----------|----------|
| `__and__` | `&` | `__rand__` | `__iand__` |
| `__or__` | `\|` | `__ror__` | `__ior__` |
| `__xor__` | `^` | `__rxor__` | `__ixor__` |
| `__lshift__` | `<<` | `__rlshift__` | `__ilshift__` |
| `__rshift__` | `>>` | `__rrshift__` | `__irshift__` |

## Matrix Multiplication (@)

Python 3.5+ added the `@` operator for matrix multiplication.

```python
class Matrix:
    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0
    
    def __matmul__(self, other):
        """Matrix multiplication: self @ other"""
        if self.cols != other.rows:
            raise ValueError("Incompatible dimensions")
        
        result = [[0] * other.cols for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(other.cols):
                for k in range(self.cols):
                    result[i][j] += self.data[i][k] * other.data[k][j]
        return Matrix(result)
    
    def __repr__(self):
        return f"Matrix({self.data})"

A = Matrix([[1, 2], [3, 4]])
B = Matrix([[5, 6], [7, 8]])
C = A @ B
print(C)  # Matrix([[19, 22], [43, 50]])
```

## Practical Example: Money Class

```python
from functools import total_ordering

@total_ordering
class Money:
    def __init__(self, amount, currency='USD'):
        self.amount = round(amount, 2)
        self.currency = currency
    
    def _check_currency(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError(f"Cannot mix {self.currency} and {other.currency}")
        return True
    
    def __add__(self, other):
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)
    
    def __sub__(self, other):
        self._check_currency(other)
        return Money(self.amount - other.amount, self.currency)
    
    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Money(self.amount * scalar, self.currency)
        return NotImplemented
    
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Money(self.amount / scalar, self.currency)
        return NotImplemented
    
    def __neg__(self):
        return Money(-self.amount, self.currency)
    
    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency
    
    def __lt__(self, other):
        self._check_currency(other)
        return self.amount < other.amount
    
    def __repr__(self):
        return f"Money({self.amount}, '{self.currency}')"
    
    def __str__(self):
        return f"${self.amount:.2f} {self.currency}"

# Usage
price = Money(19.99)
tax = Money(1.60)
total = price + tax
print(total)        # \$21.59 USD
print(total * 2)    # \$43.18 USD
print(2 * total)    # \$43.18 USD (uses __rmul__)
```

## Returning NotImplemented

Always return `NotImplemented` (not raise `NotImplementedError`) when an operation doesn't make sense:

```python
class Vector:
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        # DON'T: raise TypeError("unsupported operand type")
        # DO: return NotImplemented
        return NotImplemented
```

This allows Python to try the reflected operation on the other operand.

## divmod and Power with Modulo

```python
class Number:
    def __init__(self, value):
        self.value = value
    
    def __divmod__(self, other):
        """divmod(self, other) → (quotient, remainder)"""
        q = self.value // other.value
        r = self.value % other.value
        return (Number(q), Number(r))
    
    def __pow__(self, exp, mod=None):
        """pow(self, exp[, mod])"""
        if mod is None:
            return Number(self.value ** exp.value)
        return Number(pow(self.value, exp.value, mod.value))
    
    def __repr__(self):
        return f"Number({self.value})"

a = Number(17)
b = Number(5)
q, r = divmod(a, b)
print(q, r)  # Number(3) Number(2)

# Modular exponentiation
print(pow(Number(2), Number(10), Number(100)))  # Number(24)
```

## Key Takeaways

- Arithmetic dunders enable natural mathematical syntax
- Always return `NotImplemented` for unsupported types
- Implement `__rmul__` etc. for commutative operations with scalars
- In-place methods (`__iadd__` etc.) must return `self`
- Use `@total_ordering` to reduce comparison boilerplate
- Type check with `isinstance()` before operations
- Bitwise operators work similarly with `&`, `|`, `^`, `~`, `<<`, `>>`

---

## Runnable Example: `arithmetic_operators_tutorial.py`

```python
"""
Example 3: Arithmetic Operators
Demonstrates: __add__, __sub__, __mul__, __truediv__, __pow__, etc.
"""


class Vector:
    """A 2D vector class with arithmetic operations."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __str__(self):
        return f"<{self.x}, {self.y}>"
    
    def __add__(self, other):
        """Add two vectors or add a scalar to both components."""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        elif isinstance(other, (int, float)):
            return Vector(self.x + other, self.y + other)
        return NotImplemented
    
    def __radd__(self, other):
        """Right-side addition (when left operand doesn't support +)."""
        return self.__add__(other)
    
    def __sub__(self, other):
        """Subtract two vectors or subtract a scalar."""
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        elif isinstance(other, (int, float)):
            return Vector(self.x - other, self.y - other)
        return NotImplemented
    
    def __mul__(self, other):
        """Multiply vector by scalar."""
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        return NotImplemented
    
    def __rmul__(self, other):
        """Right-side multiplication (allows scalar * vector)."""
        return self.__mul__(other)
    
    def __truediv__(self, other):
        """Divide vector by scalar."""
        if isinstance(other, (int, float)):
            if other == 0:
                raise ValueError("Cannot divide by zero")
            return Vector(self.x / other, self.y / other)
        return NotImplemented
    
    def __neg__(self):
        """Negate the vector."""
        return Vector(-self.x, -self.y)
    
    def __abs__(self):
        """Return the magnitude of the vector."""
        return (self.x ** 2 + self.y ** 2) ** 0.5


class Money:
    """A money class with currency support."""
    
    def __init__(self, amount, currency="USD"):
        self.amount = amount
        self.currency = currency
    
    def __repr__(self):
        return f"Money({self.amount}, '{self.currency}')"
    
    def __str__(self):
        return f"{self.currency} ${self.amount:.2f}"
    
    def __add__(self, other):
        """Add two money amounts (must be same currency)."""
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise ValueError(f"Cannot add {self.currency} and {other.currency}")
            return Money(self.amount + other.amount, self.currency)
        elif isinstance(other, (int, float)):
            return Money(self.amount + other, self.currency)
        return NotImplemented
    
    def __sub__(self, other):
        """Subtract two money amounts."""
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise ValueError(f"Cannot subtract {other.currency} from {self.currency}")
            return Money(self.amount - other.amount, self.currency)
        elif isinstance(other, (int, float)):
            return Money(self.amount - other, self.currency)
        return NotImplemented
    
    def __mul__(self, other):
        """Multiply money by a number."""
        if isinstance(other, (int, float)):
            return Money(self.amount * other, self.currency)
        return NotImplemented
    
    def __rmul__(self, other):
        """Right-side multiplication."""
        return self.__mul__(other)
    
    def __truediv__(self, other):
        """Divide money by a number."""
        if isinstance(other, (int, float)):
            if other == 0:
                raise ValueError("Cannot divide by zero")
            return Money(self.amount / other, self.currency)
        return NotImplemented


# Examples
if __name__ == "__main__":

    # ============================================================================
    print("=== Vector Arithmetic Examples ===")
    v1 = Vector(3, 4)
    v2 = Vector(1, 2)
    
    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    
    print(f"\nv1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"v1 * 3 = {v1 * 3}")
    print(f"2 * v1 = {2 * v1}")  # Uses __rmul__
    print(f"v1 / 2 = {v1 / 2}")
    print(f"-v1 = {-v1}")
    print(f"abs(v1) = {abs(v1)}")
    
    print("\n=== Vector with Scalar ===")
    v3 = v1 + 5  # Add 5 to both components
    print(f"v1 + 5 = {v3}")
    
    print("\n\n=== Money Arithmetic Examples ===")
    price1 = Money(25.50)
    price2 = Money(10.25)
    
    print(f"price1 = {price1}")
    print(f"price2 = {price2}")
    
    print(f"\nTotal: {price1 + price2}")
    print(f"Difference: {price1 - price2}")
    print(f"Double price1: {price1 * 2}")
    print(f"Split price1 3 ways: {price1 / 3}")
    
    print("\n=== Currency Mismatch Example ===")
    usd = Money(100, "USD")
    eur = Money(85, "EUR")
    print(f"usd = {usd}")
    print(f"eur = {eur}")
    
    try:
        result = usd + eur
    except ValueError as e:
        print(f"Error: {e}")
    
    print("\n=== Tax Calculation Example ===")
    subtotal = Money(50.00)
    tax_rate = 0.08
    tax = subtotal * tax_rate
    total = subtotal + tax
    
    print(f"Subtotal: {subtotal}")
    print(f"Tax (8%): {tax}")
    print(f"Total: {total}")
```


---

## Runnable Example: `vector_arithmetic_operators.py`

```python
"""
TUTORIAL: Vector Arithmetic with Operator Overloading

This tutorial teaches you how to implement dunder methods that let custom
objects work with Python's arithmetic operators (+, *, abs()). We'll build a
Vector class and overload operators so that mathematical operations on vectors
feel natural and intuitive.

Key Learning Goals:
  - Understand how Python's operators are just method calls
  - Learn to implement __add__, __mul__, __abs__, __bool__
  - See why operator overloading makes code more readable
  - Understand how these operators combine with __repr__ for clarity
"""

import math

if __name__ == "__main__":

    print("=" * 70)
    print("TUTORIAL: Vector Arithmetic with Operator Overloading")
    print("=" * 70)

    # ============ EXAMPLE 1: Basic Vector Class ============
    print("\n# Example 1: Creating a Basic Vector Class")
    print("=" * 70)

    class Vector:
        """
        A simple 2D vector supporting arithmetic operations.

        This class demonstrates how operator overloading makes mathematical
        objects intuitive. Instead of v1.add(v2), you can write v1 + v2.
        """

        def __init__(self, x=0, y=0):
            """Initialize a vector with x and y components."""
            self.x = x
            self.y = y

        def __repr__(self):
            """
            Return a developer-friendly string representation.

            This is crucial for debugging. When you print a vector or inspect
            it in the interactive interpreter, you see exactly what you need.
            The !r format specifier ensures the values are clearly shown as numbers.
            """
            return f'Vector({self.x!r}, {self.y!r})'

        def __str__(self):
            """Human-readable string representation (optional)."""
            return f'({self.x}, {self.y})'


    v1 = Vector(2, 3)
    v2 = Vector(4, 5)

    print(f"Created v1 = {v1}")
    print(f"Created v2 = {v2}")
    print(f"v1.x = {v1.x}, v1.y = {v1.y}")
    print("""
    WHY: The __repr__ method is your first step. It makes vectors readable
    in the Python interpreter, which is essential when learning and debugging.
    """)

    # ============ EXAMPLE 2: The __abs__ Method ============
    print("\n# Example 2: Magnitude with abs() - __abs__")
    print("=" * 70)

    class Vector:
        """Vector with magnitude calculation."""

        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

        def __repr__(self):
            return f'Vector({self.x!r}, {self.y!r})'

        def __abs__(self):
            """
            Return the magnitude (length) of the vector.

            The magnitude of a 2D vector (x, y) is sqrt(x^2 + y^2).
            Python's abs() function calls __abs__, so you can write:
              abs(v)  instead of  v.magnitude()

            This uses the Pythagorean theorem via math.hypot, which is
            numerically stable and handles edge cases.
            """
            return math.hypot(self.x, self.y)


    v1 = Vector(3, 4)

    print(f"Vector: {v1}")
    print(f"abs(v1) = {abs(v1)}")
    print(f"Explanation: sqrt(3^2 + 4^2) = sqrt(9 + 16) = sqrt(25) = 5")
    print()

    v2 = Vector(5, 12)
    print(f"Vector: {v2}")
    print(f"abs(v2) = {abs(v2)}")
    print(f"Explanation: sqrt(5^2 + 12^2) = sqrt(25 + 144) = sqrt(169) = 13")
    print("""
    WHY: Using abs() for magnitude is more readable than v.magnitude().
    It's shorter and feels natural because we use abs() for magnitudes
    in mathematics.
    """)

    # ============ EXAMPLE 3: The __bool__ Method ============
    print("\n# Example 3: Truthiness with __bool__")
    print("=" * 70)

    class Vector:
        """Vector with magnitude and boolean evaluation."""

        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

        def __repr__(self):
            return f'Vector({self.x!r}, {self.y!r})'

        def __abs__(self):
            return math.hypot(self.x, self.y)

        def __bool__(self):
            """
            Return False if the vector has zero magnitude, True otherwise.

            In Python, objects are "truthy" or "falsy". By implementing __bool__,
            we define when a vector should be considered "empty" or "zero".

            We use abs(self) because a vector is zero only if its magnitude is 0.
            For any non-zero vector, the magnitude is positive.
            """
            return bool(abs(self))


    zero_vector = Vector(0, 0)
    unit_vector = Vector(1, 0)
    normal_vector = Vector(3, 4)

    print(f"Zero vector: {zero_vector}")
    print(f"  abs(zero_vector) = {abs(zero_vector)}")
    print(f"  bool(zero_vector) = {bool(zero_vector)}")
    print()

    print(f"Unit vector: {unit_vector}")
    print(f"  abs(unit_vector) = {abs(unit_vector)}")
    print(f"  bool(unit_vector) = {bool(unit_vector)}")
    print()

    print(f"Normal vector: {normal_vector}")
    print(f"  abs(normal_vector) = {abs(normal_vector)}")
    print(f"  bool(normal_vector) = {bool(normal_vector)}")
    print()

    print("Using vectors in if statements:")
    if zero_vector:
        print("  Zero vector is truthy")
    else:
        print("  Zero vector is falsy")

    if normal_vector:
        print("  Normal vector is truthy")
    else:
        print("  Normal vector is falsy")

    print("""
    WHY: __bool__ lets us treat vectors intuitively in boolean context.
    A zero vector "doesn't exist" in a sense, so it's falsy. This makes
    code like 'if vector:' feel natural.
    """)

    # ============ EXAMPLE 4: The __add__ Method ============
    print("\n# Example 4: Addition with __add__")
    print("=" * 70)

    class Vector:
        """Vector with arithmetic operations."""

        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

        def __repr__(self):
            return f'Vector({self.x!r}, {self.y!r})'

        def __abs__(self):
            return math.hypot(self.x, self.y)

        def __bool__(self):
            return bool(abs(self))

        def __add__(self, other):
            """
            Add two vectors component-wise.

            Vector addition in mathematics:
              (x1, y1) + (x2, y2) = (x1+x2, y1+y2)

            By implementing __add__, you can write:
              v1 + v2  instead of  v1.add(v2)

            When you write v1 + v2, Python actually calls v1.__add__(v2).
            This is how ALL operators work in Python - they're just method calls!
            """
            x = self.x + other.x
            y = self.y + other.y
            return Vector(x, y)


    v1 = Vector(2, 3)
    v2 = Vector(4, 5)

    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print()

    v3 = v1 + v2
    print(f"v1 + v2 = {v3}")
    print(f"Explanation: Vector(2+4, 3+5) = Vector(6, 8)")
    print()

    v4 = Vector(10, 20)
    v5 = Vector(1, 2)
    result = v4 + v5
    print(f"Vector(10, 20) + Vector(1, 2) = {result}")
    print("""
    WHY: The __add__ method makes vector math readable. The syntax matches
    mathematical notation exactly, so code is easier to understand and verify.

    Behind the scenes:
      v1 + v2
      ↓ (Python translates + to __add__)
      v1.__add__(v2)
      ↓ (method executes and returns a new Vector)
      Vector(6, 8)
    """)

    # ============ EXAMPLE 5: The __mul__ Method ============
    print("\n# Example 5: Scalar Multiplication with __mul__")
    print("=" * 70)

    class Vector:
        """Vector with full arithmetic support."""

        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

        def __repr__(self):
            return f'Vector({self.x!r}, {self.y!r})'

        def __abs__(self):
            return math.hypot(self.x, self.y)

        def __bool__(self):
            return bool(abs(self))

        def __add__(self, other):
            x = self.x + other.x
            y = self.y + other.y
            return Vector(x, y)

        def __mul__(self, scalar):
            """
            Multiply a vector by a scalar (number).

            Scalar multiplication in mathematics:
              c * (x, y) = (c*x, c*y)

            This scales the vector by stretching or shrinking it, but maintains
            its direction. A scalar of 2 doubles the vector, 0.5 halves it,
            -1 reverses its direction.
            """
            return Vector(self.x * scalar, self.y * scalar)


    v1 = Vector(2, 3)

    print(f"v1 = {v1}")
    print(f"abs(v1) = {abs(v1)}")
    print()

    v2 = v1 * 2
    print(f"v1 * 2 = {v2}")
    print(f"Explanation: Vector(2*2, 3*2) = Vector(4, 6)")
    print(f"abs(v1 * 2) = {abs(v2)} (twice the magnitude)")
    print()

    v3 = v1 * 0.5
    print(f"v1 * 0.5 = {v3}")
    print(f"Explanation: Vector(2*0.5, 3*0.5) = Vector(1.0, 1.5)")
    print(f"abs(v1 * 0.5) = {abs(v3)} (half the magnitude)")
    print()

    v4 = v1 * -1
    print(f"v1 * -1 = {v4}")
    print(f"Explanation: Vector(2*-1, 3*-1) = Vector(-2, -3)")
    print(f"Reverses direction, same magnitude: abs(v1 * -1) = {abs(v4)}")
    print("""
    WHY: Scalar multiplication is fundamental in vector math. By overloading
    __mul__, we make scaling vectors as simple as multiplication: v * 2.

    This is more intuitive and mathematically concise than v.scale(2).
    """)

    # ============ EXAMPLE 6: Combining Operations ============
    print("\n# Example 6: Combining Multiple Operations")
    print("=" * 70)

    # Using all our Vector methods together
    v1 = Vector(3, 4)
    v2 = Vector(1, 2)

    print(f"v1 = {v1}, magnitude = {abs(v1)}")
    print(f"v2 = {v2}, magnitude = {abs(v2)}")
    print()

    # Complex expression combining operators
    result = (v1 + v2) * 2
    print(f"(v1 + v2) * 2")
    print(f"  = ({v1} + {v2}) * 2")
    print(f"  = Vector(4, 6) * 2")
    print(f"  = {result}")
    print(f"  magnitude = {abs(result)}")
    print()

    # Using boolean context
    v_zero = Vector(0, 0)
    if v_zero:
        print("Zero vector is truthy")
    else:
        print("Zero vector is falsy (correct!)")

    if v1:
        print(f"v1 is truthy (magnitude: {abs(v1)})")

    print("""
    WHY: When operators are overloaded properly, you can compose them in
    expressions that read almost like mathematical notation. This is far
    superior to:
      Vector.multiply(Vector.add(v1, v2), 2)

    which is what you'd write without operator overloading.
    """)

    # ============ EXAMPLE 7: Understanding __mul__ Semantics ============
    print("\n# Example 7: Why __mul__ Takes a Scalar")
    print("=" * 70)

    v = Vector(2, 3)

    print(f"v = {v}")
    print()

    print("Scalar multiplication (what we support):")
    print(f"  v * 3 = {v * 3}")
    print(f"  Result: components scaled by 3")
    print()

    print("""
    NOTE: We don't support vector * vector multiplication (dot product).
    That would require a different design:
      - __mul__ could call it "cross product" (confusing)
      - Better: use a separate method v1.dot(v2) for clarity

    The rule: Use __mul__ only for operations that feel like multiplication.
    Don't force every operation into operator syntax.
    """)

    # ============ EXAMPLE 8: The Complete Vector Class ============
    print("\n# Example 8: Complete Vector Class Summary")
    print("=" * 70)

    print("""
    class Vector:
        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

        def __repr__(self):
            # For debugging and inspection
            return f'Vector({self.x!r}, {self.y!r})'

        def __abs__(self):
            # For abs(v) - returns magnitude
            return math.hypot(self.x, self.y)

        def __bool__(self):
            # For if v: - zero vector is falsy
            return bool(abs(self))

        def __add__(self, other):
            # For v1 + v2 - component-wise addition
            return Vector(self.x + other.x, self.y + other.y)

        def __mul__(self, scalar):
            # For v * n - scalar multiplication
            return Vector(self.x * scalar, self.y * scalar)

    With just 5 methods (6 lines of code each), we've built a powerful,
    intuitive vector class that feels like a first-class Python object.
    """)

    # ============ EXAMPLE 9: Real-World Usage ============
    print("\n# Example 9: Real-World Vector Math")
    print("=" * 70)

    # Simulate a particle with velocity
    position = Vector(0, 0)
    velocity = Vector(1, 2)
    acceleration = Vector(0.1, 0)

    print("Simulating object movement:")
    print(f"Initial position: {position}")
    print(f"Velocity: {velocity}")
    print(f"Acceleration: {acceleration}")
    print()

    # Simulate physics: position += velocity; velocity += acceleration
    for step in range(3):
        position = position + velocity
        velocity = velocity + acceleration
        print(f"Step {step+1}: pos={position}, vel={velocity}, speed={abs(velocity):.2f}")

    print("""
    WHY: With operator overloading, physics simulation code reads naturally.
    The physics equations map directly to Python code:
      position = position + velocity
      velocity = velocity + acceleration

    Without overloading, it would be:
      position = position.add(velocity)
      velocity = velocity.add(acceleration)

    Much more verbose and harder to read!
    """)

    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)
    print("""
    1. OPERATORS ARE METHOD CALLS: When you write v1 + v2, Python calls
       v1.__add__(v2). All operators (+, -, *, /) are just methods!

    2. READABLE MATH: Overloading operators makes mathematical code match
       mathematical notation. This reduces cognitive load and prevents bugs.

    3. MATCH THE SEMANTICS: Only overload operators where they make sense.
       For vectors, + is addition, * is scalar multiplication. Clear and
       intuitive.

    4. IMMUTABILITY: Our operations (+ and *) return new vectors rather
       than modifying existing ones. This is the Pythonic style for operators.

    5. COMPOSE OPERATIONS: With proper operator overloading, you can compose
       complex expressions that read naturally: (v1 + v2) * 2 - v3

    6. __repr__ IS IMPORTANT: Always implement __repr__ with any dunder
       methods. It makes debugging vastly easier.
    """)
```


---

## Runnable Example: `operator_overloading_vector.py`

```python
"""
TUTORIAL: Comprehensive Vector Class - Production-Ready Operator Overloading

This tutorial builds a professional-grade 2D vector class implementing a
comprehensive set of dunder methods. We'll cover operator overloading, type
checking, immutability, hashing, formatting, binary serialization, and more.

This is what a real, production-quality implementation looks like, not a toy example.

Key Learning Goals:
  - Implement multiple operators safely with type checking
  - Use properties for read-only attributes
  - Support binary serialization with __bytes__
  - Implement __hash__ and __eq__ for use in sets and dicts
  - Use __format__ for flexible string formatting
  - Understand __iter__ and unpacking
"""

from array import array
import math

if __name__ == "__main__":

    print("=" * 70)
    print("TUTORIAL: Comprehensive Vector2d - Production-Quality Implementation")
    print("=" * 70)

    # ============ EXAMPLE 1: Basic Class Structure ============
    print("\n# Example 1: Private Attributes and Properties")
    print("=" * 70)

    class Vector2d:
        """
        A 2D vector with comprehensive operator support.

        Key design decisions:
        - Use private attributes (__x, __y) to prevent accidental modification
        - Use properties to expose them as read-only (can read, not write)
        - Ensure immutability (vectors don't change after creation)
        - Support rich comparisons and hashing
        """

        typecode = 'd'  # for array.array and binary serialization

        def __init__(self, x, y):
            """Initialize with x and y coordinates, converted to float."""
            # Private attributes (name mangling with __) prevent direct modification
            self.__x = float(x)
            self.__y = float(y)

        @property
        def x(self):
            """Read-only x coordinate. You can read but not set."""
            return self.__x

        @property
        def y(self):
            """Read-only y coordinate. You can read but not set."""
            return self.__y


    # Create and use a vector
    v = Vector2d(3, 4)

    print(f"Created: {v.__class__.__name__}")
    print(f"v.x = {v.x}")
    print(f"v.y = {v.y}")
    print(f"Type of v.x: {type(v.x)}")  # Always float, even if you passed int
    print()

    print("Attempting to modify v.x (read-only property):")
    try:
        v.x = 10
    except AttributeError as e:
        print(f"  Error: {e}")

    print("""
    WHY: Properties let us expose attributes while preventing modification.
    This is important for vectors because changing them would violate the
    principle of immutability. A vector (3, 4) should always be (3, 4).
    """)

    # ============ EXAMPLE 2: String Representations ============
    print("\n# Example 2: __repr__ and __str__")
    print("=" * 70)

    class Vector2d:
        """Vector with string representations."""

        typecode = 'd'

        def __init__(self, x, y):
            self.__x = float(x)
            self.__y = float(y)

        @property
        def x(self):
            return self.__x

        @property
        def y(self):
            return self.__y

        def __repr__(self):
            """
            Developer-friendly representation.

            This uses the class name dynamically (type(self).__name__), so if you
            subclass Vector2d, it will show the subclass name. The !r format
            ensures values are precisely represented.

            We unpack self with *self, which requires __iter__ to work.
            This is shown in the next example.
            """
            class_name = type(self).__name__
            return f'{class_name}({self.__x!r}, {self.__y!r})'

        def __str__(self):
            """
            Human-readable representation: show as a coordinate pair.

            Simpler than __repr__, easier to read but less precise.
            Used by print() when __repr__ isn't needed.
            """
            return str(tuple(self))  # Uses __iter__ via tuple()


    v = Vector2d(3, 4)

    print(f"repr(v) = {repr(v)}")
    print(f"str(v) = {str(v)}")
    print(f"print(v) output: {v}")
    print()

    print(f"Type information in repr: {type(v).__name__}")
    print("""
    WHY: __repr__ should be unambiguous (you could copy it to recreate the
    object), while __str__ is just for readability. In REPL:
      >>> v
      Vector2d(3.0, 4.0)  <- calls __repr__

    With print():
      >>> print(v)
      (3.0, 4.0)  <- calls __str__
    """)

    # ============ EXAMPLE 3: Iteration and Unpacking ============
    print("\n# Example 3: __iter__ - Unpacking and Iteration")
    print("=" * 70)

    class Vector2d:
        """Vector supporting unpacking."""

        typecode = 'd'

        def __init__(self, x, y):
            self.__x = float(x)
            self.__y = float(y)

        @property
        def x(self):
            return self.__x

        @property
        def y(self):
            return self.__y

        def __iter__(self):
            """
            Yield x and y in sequence, enabling unpacking.

            This generator yields coordinates one at a time. With __iter__,
            you can:
              x, y = vector
              for coord in vector:
              tuple(vector)
              list(vector)

            All work because Python knows how to iterate.
            """
            return (i for i in (self.__x, self.__y))

        def __repr__(self):
            class_name = type(self).__name__
            return f'{class_name}({self.__x!r}, {self.__y!r})'

        def __str__(self):
            return str(tuple(self))


    v = Vector2d(3, 4)

    print(f"Vector: {v}")
    print()

    # Unpacking
    x, y = v
    print(f"Unpacking: x={x}, y={y}")

    # Iteration
    print("Iterating:")
    for i, coord in enumerate(v):
        print(f"  [{i}] = {coord}")

    # Conversion
    print(f"tuple(v) = {tuple(v)}")
    print(f"list(v) = {list(v)}")

    print("""
    WHY: __iter__ makes your custom objects work with Python's standard
    iteration patterns. Users don't need to know about Vector2d internals.
    They can unpack, iterate, and convert just like built-in sequences.
    """)

    # ============ EXAMPLE 4: Equality and Hashing ============
    print("\n# Example 4: __eq__ and __hash__ - Comparison and Hashing")
    print("=" * 70)

    class Vector2d:
        """Vector supporting equality and hashing."""

        typecode = 'd'

        def __init__(self, x, y):
            self.__x = float(x)
            self.__y = float(y)

        @property
        def x(self):
            return self.__x

        @property
        def y(self):
            return self.__y

        def __iter__(self):
            return (i for i in (self.__x, self.__y))

        def __repr__(self):
            class_name = type(self).__name__
            return f'{class_name}({self.__x!r}, {self.__y!r})'

        def __eq__(self, other):
            """
            Two vectors are equal if their coordinates are equal.

            We convert both to tuples for comparison. This works because
            __iter__ yields coordinates in a well-defined order.

            Important: If you define __eq__, Python sets __hash__ to None
            unless you explicitly define __hash__ too. This prevents bugs
            where equal objects would have different hashes.
            """
            return tuple(self) == tuple(other)

        def __hash__(self):
            """
            Hash based on the XOR of coordinate hashes.

            This is a common pattern: combine hashes of components using XOR.
            The hash must be stable (same vector = same hash always) and
            consistent with equality (equal vectors = equal hashes).

            Important: Vectors MUST be immutable to be hashable. If a vector
            changes, its hash would become wrong, breaking dict/set lookups.
            """
            return hash(self.__x) ^ hash(self.__y)


    # Test equality
    v1 = Vector2d(3, 4)
    v2 = Vector2d(3, 4)
    v3 = Vector2d(4, 5)

    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"v3 = {v3}")
    print()

    print(f"v1 == v2: {v1 == v2} (same coordinates)")
    print(f"v1 == v3: {v1 == v3} (different coordinates)")
    print(f"v1 is v2: {v1 is v2} (different objects!)")
    print()

    # Test hashing
    print("Hashing vectors:")
    print(f"hash(v1) = {hash(v1)}")
    print(f"hash(v2) = {hash(v2)}")
    print(f"hash(v3) = {hash(v3)}")
    print()

    # Use in a set (requires __hash__ and __eq__)
    vectors = {v1, v2, v3}
    print(f"Set of {v1}, {v2}, {v3}: {vectors}")
    print(f"Length: {len(vectors)} (v1 and v2 are equal, so one is dropped)")
    print()

    # Use as dict keys
    vector_data = {v1: "origin area", v3: "far away"}
    print(f"Using vectors as dict keys: {vector_data}")

    print("""
    WHY: __hash__ lets vectors work in sets and as dict keys. Combined
    with __eq__, it enables reliable comparison and storage. This is
    essential for data structures that rely on equality and hashing.

    Important: Only define __hash__ for immutable objects. If a vector's
    coordinates changed, code like dict[v] would break because v's hash
    would be wrong.
    """)

    # ============ EXAMPLE 5: Magnitude and Boolean ============
    print("\n# Example 5: __abs__ and __bool__")
    print("=" * 70)

    class Vector2d:
        """Vector with magnitude and truthiness."""

        typecode = 'd'

        def __init__(self, x, y):
            self.__x = float(x)
            self.__y = float(y)

        @property
        def x(self):
            return self.__x

        @property
        def y(self):
            return self.__y

        def __abs__(self):
            """Return magnitude using Pythagorean theorem."""
            return math.hypot(self.__x, self.__y)

        def __bool__(self):
            """Zero vector is falsy, any other vector is truthy."""
            return bool(abs(self))

        def __repr__(self):
            class_name = type(self).__name__
            return f'{class_name}({self.__x!r}, {self.__y!r})'


    v_zero = Vector2d(0, 0)
    v_unit = Vector2d(1, 0)
    v_normal = Vector2d(3, 4)

    print(f"v_zero = {v_zero}, abs = {abs(v_zero)}, bool = {bool(v_zero)}")
    print(f"v_unit = {v_unit}, abs = {abs(v_unit)}, bool = {bool(v_unit)}")
    print(f"v_normal = {v_normal}, abs = {abs(v_normal)}, bool = {bool(v_normal)}")
    print()

    print("In if statements:")
    if v_zero:
        print("  v_zero is truthy")
    else:
        print("  v_zero is falsy")

    if v_normal:
        print(f"  v_normal is truthy (magnitude: {abs(v_normal)})")

    print("""
    WHY: Magnitude and truthiness are core vector properties.
    abs() gives you the length, while bool() lets you treat zero
    vectors specially in conditional logic.
    """)

    # ============ EXAMPLE 6: Binary Serialization ============
    print("\n# Example 6: __bytes__ and frombytes() - Binary Format")
    print("=" * 70)

    class Vector2d:
        """Vector supporting binary serialization."""

        typecode = 'd'  # typecode tells array.array how to store numbers

        def __init__(self, x, y):
            self.__x = float(x)
            self.__y = float(y)

        @property
        def x(self):
            return self.__x

        @property
        def y(self):
            return self.__y

        def __bytes__(self):
            """
            Serialize to bytes: typecode + binary data.

            First byte is the typecode (identifies the format).
            Remaining bytes are raw binary representations.

            This is compact and fast for saving to disk or network.
            """
            return (bytes([ord(self.typecode)]) +
                    bytes(array(self.typecode, self)))

        @classmethod
        def frombytes(cls, octets):
            """
            Deserialize from bytes created by __bytes__.

            Read typecode from first byte, then interpret remaining bytes
            using that typecode. Return a new Vector2d instance.
            """
            typecode = chr(octets[0])
            memv = memoryview(octets[1:]).cast(typecode)
            return cls(*memv)

        def __iter__(self):
            return (i for i in (self.__x, self.__y))

        def __repr__(self):
            class_name = type(self).__name__
            return f'{class_name}({self.__x!r}, {self.__y!r})'


    v1 = Vector2d(3, 4)

    print(f"Original vector: {v1}")
    print()

    # Serialize to bytes
    data = bytes(v1)
    print(f"Serialized to bytes: {data!r}")
    print(f"Byte length: {len(data)}")
    print()

    # Deserialize from bytes
    v2 = Vector2d.frombytes(data)
    print(f"Deserialized vector: {v2}")
    print(f"v1 == v2: {v1 == v2}")
    print()

    print(f"Typecode '{Vector2d.typecode}' is: float64 (8 bytes per number)")
    print(f"Total bytes: 1 (typecode) + 8 (x) + 8 (y) = 17 bytes")
    print("""
    WHY: Binary serialization is fast and compact. Useful for:
      - Saving vectors to files
      - Sending over network
      - Storing in databases
      - Speed-critical applications

    The typecode makes deserialization unambiguous - the byte stream
    completely describes itself.
    """)

    # ============ EXAMPLE 7: Custom Formatting ============
    print("\n# Example 7: __format__ - Flexible String Formatting")
    print("=" * 70)

    class Vector2d:
        """Vector supporting custom formatting."""

        typecode = 'd'

        def __init__(self, x, y):
            self.__x = float(x)
            self.__y = float(y)

        @property
        def x(self):
            return self.__x

        @property
        def y(self):
            return self.__y

        def angle(self):
            """Return angle in radians from positive x-axis."""
            return math.atan2(self.__y, self.__x)

        def __iter__(self):
            return (i for i in (self.__x, self.__y))

        def __abs__(self):
            return math.hypot(self.__x, self.__y)

        def __format__(self, fmt_spec=''):
            """
            Custom formatting supporting Cartesian and polar coordinates.

            fmt_spec examples:
              'p'       -> polar format: <magnitude, angle>
              '.2f'     -> 2 decimal places (Cartesian)
              '.3ep'    -> 3 decimals, scientific, polar
              '.5fp'    -> 5 decimals, polar

            This is flexible formatting that respects both format spec
            and coordinate system preference.
            """
            if fmt_spec.endswith('p'):
                # Polar format: remove 'p', convert to polar
                fmt_spec = fmt_spec[:-1]
                coords = (abs(self), self.angle())
                outer_fmt = '<{}, {}>'
            else:
                # Cartesian format (default)
                coords = self
                outer_fmt = '({}, {})'

            # Format each coordinate with the format spec
            components = (format(c, fmt_spec) for c in coords)
            return outer_fmt.format(*components)

        def __repr__(self):
            class_name = type(self).__name__
            return f'{class_name}({self.__x!r}, {self.__y!r})'


    v = Vector2d(1, 1)

    print(f"Vector: {v}")
    print(f"Magnitude: {abs(v):.6f}, Angle: {v.angle():.6f} radians")
    print()

    print("Cartesian formatting (default):")
    print(f"  format(v, '') = {format(v)}")
    print(f"  format(v, '.2f') = {format(v, '.2f')}")
    print(f"  format(v, '.3e') = {format(v, '.3e')}")
    print()

    print("Polar formatting (endswith 'p'):")
    print(f"  format(v, 'p') = {format(v, 'p')}")
    print(f"  format(v, '.2fp') = {format(v, '.2fp')}")
    print()

    v2 = Vector2d(3, 4)
    print(f"v2 = {v2}")
    print(f"  Cartesian: {format(v2, '.2f')}")
    print(f"  Polar: {format(v2, '.2fp')}")

    print("""
    WHY: __format__ provides flexible, user-friendly output. Users can
    choose between representations (Cartesian vs polar) with simple syntax:
      f"{v:.2f}"    # Cartesian: (3.00, 4.00)
      f"{v:.2fp}"   # Polar: <5.00, 0.93>

    This is much better than having two separate methods.
    """)

    # ============ EXAMPLE 8: Arithmetic Operators ============
    print("\n# Example 8: __add__ and Type Checking")
    print("=" * 70)

    class Vector2d:
        """Vector with safe arithmetic operations."""

        typecode = 'd'

        def __init__(self, x, y):
            self.__x = float(x)
            self.__y = float(y)

        @property
        def x(self):
            return self.__x

        @property
        def y(self):
            return self.__y

        def __iter__(self):
            return (i for i in (self.__x, self.__y))

        def __add__(self, other):
            """
            Add two vectors (or raise a clear error if 'other' isn't compatible).

            Type checking prevents cryptic errors. Without it, you might add
            a Vector and a tuple by accident, leading to confusing results.
            With explicit checking, errors are immediate and clear.
            """
            if isinstance(other, Vector2d):
                return Vector2d(*tuple(self) + tuple(other))
            return NotImplemented  # Let Python try other.__radd__(self)

        def __repr__(self):
            class_name = type(self).__name__
            return f'{class_name}({self.__x!r}, {self.__y!r})'


    v1 = Vector2d(2, 3)
    v2 = Vector2d(4, 5)

    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"v1 + v2 = {v1 + v2}")
    print()

    print("Type checking prevents bugs:")
    try:
        result = v1 + (1, 2)
    except TypeError as e:
        print(f"  v1 + (1, 2) raises TypeError: {e}")

    print("""
    WHY: Type checking in operators prevents silent bugs. If you try to add
    incompatible types, you get a clear error immediately rather than getting
    garbage data later. The NotImplemented return allows Python to try the
    reverse operation (other.__radd__(v1)).
    """)

    # ============ EXAMPLE 9: Complete Professional Implementation ============
    print("\n# Example 9: The Complete Vector2d Class")
    print("=" * 70)

    print("""
    Key design principles in a production Vector2d:

    1. IMMUTABILITY: Private attributes (__x, __y) and read-only properties
       ensure vectors can't be modified. Essential for hashing!

    2. TYPE SAFETY: __float__ conversion on inputs, type checking in operators

    3. RICH COMPARISON: __eq__ for equality, __hash__ for use in collections

    4. ITERATION: __iter__ for unpacking (x, y = v), conversion to tuple/list

    5. NUMERIC PROTOCOL: __abs__ for magnitude, __bool__ for truthiness

    6. SERIALIZATION: __bytes__ and frombytes() for persistence

    7. FORMATTING: __format__ for flexible output (Cartesian vs polar)

    8. OPERATORS: __add__ with type checking, NotImplemented for compatibility

    9. REPRESENTATION: __repr__ for debugging, __str__ for readability

    10. METADATA: __match_args__ for pattern matching, typecode for flexibility

    All these features work together to make Vector2d feel like a native
    Python type, not a bolt-on class. Users don't have to learn special
    methods - they use standard Python idioms.
    """)

    # ============ EXAMPLE 10: Practical Usage ============
    print("\n# Example 10: Real-World Vector Operations")
    print("=" * 70)

    class Vector2d:
        """Complete Vector2d for real use."""

        __match_args__ = ('x', 'y')  # enables pattern matching
        typecode = 'd'

        def __init__(self, x, y):
            self.__x = float(x)
            self.__y = float(y)

        @property
        def x(self):
            return self.__x

        @property
        def y(self):
            return self.__y

        def __iter__(self):
            return (i for i in (self.__x, self.__y))

        def __repr__(self):
            class_name = type(self).__name__
            return f'{class_name}({self.__x!r}, {self.__y!r})'

        def __str__(self):
            return str(tuple(self))

        def __bytes__(self):
            return (bytes([ord(self.typecode)]) +
                    bytes(array(self.typecode, self)))

        def __eq__(self, other):
            return tuple(self) == tuple(other)

        def __hash__(self):
            return hash(self.__x) ^ hash(self.__y)

        def __abs__(self):
            return math.hypot(self.__x, self.__y)

        def __bool__(self):
            return bool(abs(self))

        def angle(self):
            return math.atan2(self.__y, self.__x)

        def __format__(self, fmt_spec=''):
            if fmt_spec.endswith('p'):
                fmt_spec = fmt_spec[:-1]
                coords = (abs(self), self.angle())
                outer_fmt = '<{}, {}>'
            else:
                coords = self
                outer_fmt = '({}, {})'
            components = (format(c, fmt_spec) for c in coords)
            return outer_fmt.format(*components)

        def __add__(self, other):
            if isinstance(other, Vector2d):
                return Vector2d(*tuple(self) + tuple(other))
            return NotImplemented

        @classmethod
        def frombytes(cls, octets):
            typecode = chr(octets[0])
            memv = memoryview(octets[1:]).cast(typecode)
            return cls(*memv)


    # Practical scenario: navigation system
    print("Navigation system with vectors:")
    print()

    # Starting position and direction
    position = Vector2d(0, 0)
    direction = Vector2d(1, 1)  # NE direction

    print(f"Starting at: {position}")
    print(f"Moving in direction: {direction}")
    print(f"Direction magnitude: {abs(direction):.2f}")
    print()

    # Move in direction
    distance = 10
    movement = Vector2d(direction.x * distance / abs(direction),
                        direction.y * distance / abs(direction))
    position = Vector2d(position.x + movement.x, position.y + movement.y)

    print(f"After moving 10 units: {position}")
    print(f"Distance from origin: {abs(position):.2f}")
    print()

    # Store in a collection
    waypoints = {
        Vector2d(0, 0): "start",
        Vector2d(10, 10): "checkpoint",
        Vector2d(20, 20): "end"
    }

    print("Navigation waypoints:")
    for point, name in waypoints.items():
        print(f"  {point} ({format(point, '.1fp')}) -> {name}")

    print("""
    This demonstrates real usage: vectors work seamlessly in collections,
    arithmetic, formatting, and comparisons. Users don't think about dunder
    methods - they just use vectors naturally.
    """)

    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)
    print("""
    1. IMMUTABILITY: Use private attributes and properties to prevent
       modification. This is essential for hashing and predictability.

    2. DUNDER METHODS ENABLE PROTOCOLS: Each dunder method (like __eq__)
       enables a specific Python protocol (hashability, comparability).

    3. TYPE SAFETY: Check types in operators, use NotImplemented to allow
       Python to try the other operand's methods.

    4. CONSISTENCY: If you define __eq__, define __hash__. If you implement
       __iter__, you get unpacking for free. Dunder methods work together.

    5. DOCUMENTATION: Each method needs clear docs explaining why and when
       to use it. These are important design decisions.

    6. COMPLETENESS: A professional class doesn't just have __add__ - it has
       __repr__, __str__, __eq__, __hash__, __iter__, and more working
       together smoothly.

    7. PROTOCOLS OVER INHERITANCE: You don't inherit from list or need a
       special base class. You just implement the right dunder methods.

    8. PYTHONIC DESIGN: Make your objects work with standard Python features:
       collections, iteration, formatting, arithmetic. Users should never
       feel like they're using a special library type.
    """)
```

---

## Exercises

**Exercise 1.**
Create a `Fraction` class with `numerator` and `denominator`. Implement `__add__`, `__sub__`, `__mul__`, and `__repr__`. Use the formula for fraction arithmetic (e.g., `a/b + c/d = (a*d + b*c) / (b*d)`). Simplify results using `math.gcd`. Show that `Fraction(1, 2) + Fraction(1, 3)` produces `Fraction(5, 6)`.

??? success "Solution to Exercise 1"

        from math import gcd

        class Fraction:
            def __init__(self, num, den):
                if den == 0:
                    raise ValueError("Denominator cannot be zero")
                g = gcd(abs(num), abs(den))
                self.num = num // g
                self.den = den // g

            def __add__(self, other):
                return Fraction(self.num * other.den + other.num * self.den,
                                self.den * other.den)

            def __sub__(self, other):
                return Fraction(self.num * other.den - other.num * self.den,
                                self.den * other.den)

            def __mul__(self, other):
                return Fraction(self.num * other.num, self.den * other.den)

            def __repr__(self):
                return f"Fraction({self.num}, {self.den})"

        print(Fraction(1, 2) + Fraction(1, 3))  # Fraction(5, 6)
        print(Fraction(3, 4) - Fraction(1, 4))  # Fraction(1, 2)
        print(Fraction(2, 3) * Fraction(3, 4))  # Fraction(1, 2)

---

**Exercise 2.**
Write a `Money` class with `amount` and `currency`. Implement `__add__` that only allows adding money of the same currency (raise `ValueError` otherwise). Implement `__mul__` for scalar multiplication (e.g., `Money(10, "USD") * 3`), and `__rmul__` so `3 * Money(10, "USD")` also works. Include `__repr__`.

??? success "Solution to Exercise 2"

        class Money:
            def __init__(self, amount, currency):
                self.amount = amount
                self.currency = currency

            def __add__(self, other):
                if self.currency != other.currency:
                    raise ValueError(f"Cannot add {self.currency} and {other.currency}")
                return Money(self.amount + other.amount, self.currency)

            def __mul__(self, scalar):
                return Money(self.amount * scalar, self.currency)

            def __rmul__(self, scalar):
                return self.__mul__(scalar)

            def __repr__(self):
                return f"Money({self.amount}, '{self.currency}')"

        a = Money(10, "USD") + Money(20, "USD")
        print(a)  # Money(30, 'USD')

        b = Money(10, "USD") * 3
        print(b)  # Money(30, 'USD')

        c = 3 * Money(10, "USD")
        print(c)  # Money(30, 'USD')

---

**Exercise 3.**
Build a `Matrix2x2` class representing a 2x2 matrix. Implement `__add__` (element-wise addition), `__mul__` (matrix multiplication), and `__repr__`. Show that matrix multiplication is not commutative: `A * B` may differ from `B * A`.

??? success "Solution to Exercise 3"

        class Matrix2x2:
            def __init__(self, a, b, c, d):
                self.data = [[a, b], [c, d]]

            def __add__(self, other):
                return Matrix2x2(
                    self.data[0][0] + other.data[0][0],
                    self.data[0][1] + other.data[0][1],
                    self.data[1][0] + other.data[1][0],
                    self.data[1][1] + other.data[1][1],
                )

            def __mul__(self, other):
                a, b = self.data
                c, d = other.data
                return Matrix2x2(
                    a[0]*c[0][0] + a[1]*c[1][0], a[0]*c[0][1] + a[1]*c[1][1],
                    b[0]*c[0][0] + b[1]*c[1][0], b[0]*c[0][1] + b[1]*c[1][1],
                )

            def __repr__(self):
                return f"Matrix2x2({self.data[0]}, {self.data[1]})"

        A = Matrix2x2(1, 2, 3, 4)
        B = Matrix2x2(5, 6, 7, 8)
        print(A * B)  # Matrix2x2([19, 22], [43, 50])
        print(B * A)  # Matrix2x2([23, 34], [31, 46]) — different!
