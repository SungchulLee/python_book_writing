# Type Introspection

!!! tip "Mental Model"
    `type(x)` tells you exactly which class `x` is -- no more, no less. `isinstance(x, SomeClass)` is more flexible: it returns `True` for `SomeClass` and all its subclasses. Prefer `isinstance()` for type checks in real code because it respects inheritance; reserve `type()` for debugging and exact-class comparisons.

## type() Function

### 1. Basic Usage

```python
x = 42
print(type(x))             # <class 'int'>

y = "hello"
print(type(y))             # <class 'str'>
```

### 2. Compare Types

```python
x = 42

if type(x) == int:
    print("x is integer")

if type(x) == str:
    print("Won't print")
```

## isinstance()

### 1. Better Check

```python
x = 42

if isinstance(x, int):
    print("x is int")

# Multiple types
if isinstance(x, (int, float)):
    print("x is number")
```

### 2. Inheritance

```python
class Animal:
    pass

class Dog(Animal):
    pass

dog = Dog()

print(isinstance(dog, Dog))     # True
print(isinstance(dog, Animal))  # True

print(type(dog) == Dog)         # True
print(type(dog) == Animal)      # False
```

## issubclass()

### 1. Check Hierarchy

```python
class Animal:
    pass

class Dog(Animal):
    pass

print(issubclass(Dog, Animal))  # True
print(issubclass(Animal, Dog))  # False
```

## Callable Check

### 1. Is Callable

```python
def my_func():
    return 42

print(callable(my_func))        # True
print(callable(42))             # False
print(callable(lambda: 1))      # True
```

## hasattr()

### 1. Check Attributes

```python
class MyClass:
    def __init__(self):
        self.value = 42

obj = MyClass()

print(hasattr(obj, 'value'))    # True
print(hasattr(obj, 'missing'))  # False
```

## dir() and vars()

### 1. List Attributes

```python
class MyClass:
    def __init__(self):
        self.x = 1
        self.y = 2

obj = MyClass()

print(dir(obj))                 # All attributes
print(vars(obj))                # {'x': 1, 'y': 2}
```

## Practical Usage

### 1. Type Validation

```python
def validate_int(value):
    if not isinstance(value, int):
        raise TypeError("Must be int")
    return value * 2

print(validate_int(5))          # 10
```

### 2. Dynamic Dispatch

```python
def process(value):
    if isinstance(value, int):
        return value * 2
    elif isinstance(value, str):
        return value.upper()
    return None

print(process(5))               # 10
print(process("hi"))            # "HI"
```


---

## Exercises


**Exercise 1.**
Write a function `type_name(obj)` that returns the name of the object's type as a string (e.g., `"int"`, `"str"`, `"list"`). Test with at least 5 different types.

??? success "Solution to Exercise 1"

    ```python
    def type_name(obj):
        return type(obj).__name__

    print(type_name(42))         # int
    print(type_name("hello"))    # str
    print(type_name([1, 2]))     # list
    print(type_name((1, 2)))     # tuple
    print(type_name({1: 2}))     # dict
    ```

    `type(obj).__name__` accesses the name attribute of the type object, giving a clean string representation.

---

**Exercise 2.**
Demonstrate the difference between `type()` and `isinstance()` with class inheritance. Create a base class `Animal` and a subclass `Dog`, then show how each function behaves when checking a `Dog` instance against `Animal`.

??? success "Solution to Exercise 2"

    ```python
    class Animal:
        pass

    class Dog(Animal):
        pass

    dog = Dog()

    # type() checks exact type
    print(type(dog) == Dog)      # True
    print(type(dog) == Animal)   # False

    # isinstance() checks inheritance chain
    print(isinstance(dog, Dog))     # True
    print(isinstance(dog, Animal))  # True
    ```

    `type()` checks the exact type only. `isinstance()` checks the entire inheritance chain, making it the preferred choice for most type checking.

---

**Exercise 3.**
Write a function `describe(obj)` that uses `isinstance()` to return different descriptions based on the object's type: `"number"` for `int` or `float`, `"text"` for `str`, `"collection"` for `list`, `tuple`, or `set`, and `"unknown"` otherwise.

??? success "Solution to Exercise 3"

    ```python
    def describe(obj):
        if isinstance(obj, (int, float)):
            return "number"
        elif isinstance(obj, str):
            return "text"
        elif isinstance(obj, (list, tuple, set)):
            return "collection"
        else:
            return "unknown"

    print(describe(42))          # number
    print(describe("hello"))     # text
    print(describe([1, 2, 3]))   # collection
    print(describe(None))        # unknown
    ```

    Passing a tuple of types to `isinstance()` checks if the object is an instance of any of the listed types.
