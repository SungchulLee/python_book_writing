# Getter Setter Deleter

The `@property` decorator with `@prop.setter` and `@prop.deleter` provides the three access hooks for an attribute. Under the hood, each `@property` creates a **descriptor object** that intercepts reads, writes, and deletions --- see [Properties as Descriptors](property_descriptor_connection.md) for the full mechanism. For a deeper treatment of property design, see [Property Decorator](property_decorator.md).

## Property Decorator

### 1. Getter

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius

c = Circle(5)
print(c.radius)  # 5
```

### 2. Setter

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Negative radius")
        self._radius = value

c = Circle(5)
c.radius = 10  # OK
```

### 3. Deleter

```python
    @radius.deleter
    def radius(self):
        del self._radius
```

## Best Practices

- **Start with plain attributes**. Add `@property` only when you need validation, computation, or read-only access.
- **Don't use setters for expensive operations** (I/O, network calls). Users expect `obj.x = val` to be fast.
- **Setter names must match** the property name --- `@radius.setter def radius(self, value)`.
- **Prefer immutability** when possible: omit the setter to make an attribute read-only.

## Summary

- `@property` for getter
- `@prop.setter` for setter
- `@prop.deleter` for deleter
- All three are backed by a single descriptor object on the class

---

## Exercises

**Exercise 1.** Write a `Temperature` class with a `celsius` property that has a getter, setter, and deleter. The setter should reject values below $-273.15$. The deleter should reset the temperature to `0`. Demonstrate all three operations.

??? success "Solution to Exercise 1"
    ```python
    class Temperature:
        def __init__(self, celsius=0):
            self.celsius = celsius

        @property
        def celsius(self):
            return self._celsius

        @celsius.setter
        def celsius(self, value):
            if value < -273.15:
                raise ValueError("Below absolute zero")
            self._celsius = value

        @celsius.deleter
        def celsius(self):
            self._celsius = 0

    t = Temperature(100)
    print(t.celsius)       # 100

    t.celsius = -10
    print(t.celsius)       # -10

    del t.celsius
    print(t.celsius)       # 0

    try:
        t.celsius = -300
    except ValueError as e:
        print(e)           # Below absolute zero
    ```

---

**Exercise 2.** Predict the output:

```python
class Item:
    def __init__(self, price):
        self._price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Negative price")
        self._price = value

    @price.deleter
    def price(self):
        print("Price deleted")
        self._price = 0

item = Item(50)
print(item.price)
item.price = 75
print(item.price)
del item.price
print(item.price)
```

??? success "Solution to Exercise 2"
    The output is:

    ```
    50
    75
    Price deleted
    0
    ```

    The getter returns `_price`. The setter validates and updates `_price`. The deleter prints a message and resets `_price` to 0.

---

**Exercise 3.** Create a `FullName` class where `name` is a property. The getter returns the stored name. The setter accepts a string with first and last names separated by a space and stores them internally as `_first` and `_last`. The getter joins them back together. The deleter clears both.

??? success "Solution to Exercise 3"
    ```python
    class FullName:
        def __init__(self, name):
            self.name = name

        @property
        def name(self):
            return f"{self._first} {self._last}"

        @name.setter
        def name(self, value):
            parts = value.split(maxsplit=1)
            self._first = parts[0]
            self._last = parts[1] if len(parts) > 1 else ""

        @name.deleter
        def name(self):
            self._first = ""
            self._last = ""

    fn = FullName("Alice Smith")
    print(fn.name)    # Alice Smith

    fn.name = "Bob Jones"
    print(fn.name)    # Bob Jones

    del fn.name
    print(repr(fn.name))  # ' '
    ```

---

**Exercise 4.** Write a `CachedSquare` class with a `value` property. The setter stores the value and also pre-computes and caches the square in a private attribute. The getter returns the stored value. Add a read-only `square` property that returns the cached square. Demonstrate that changing `value` updates the cached square.

??? success "Solution to Exercise 4"
    ```python
    class CachedSquare:
        def __init__(self, value=0):
            self.value = value

        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, v):
            self._value = v
            self._square = v ** 2

        @property
        def square(self):
            return self._square

    cs = CachedSquare(5)
    print(cs.value)    # 5
    print(cs.square)   # 25

    cs.value = 12
    print(cs.square)   # 144
    ```
