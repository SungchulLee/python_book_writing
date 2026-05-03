# Descriptors in Python

Descriptors are the **core mechanism behind attribute access in Python**.

!!! tip "Mental Model"
    A descriptor is an object that hijacks attribute access on another object. When a class attribute defines `__get__`, `__set__`, or `__delete__`, Python calls those methods instead of simply reading or writing the attribute. This single mechanism powers properties, methods, `classmethod`, `staticmethod`, and ORMs -- understanding descriptors means understanding how Python's object model actually works.

They power:

- methods
- `@property`
- `classmethod` / `staticmethod`
- ORMs (Django, SQLAlchemy)

---

## 1. What is a Descriptor?

A descriptor is any object that implements one or more of:

```python
__get__(self, obj, objtype=None)
__set__(self, obj, value)
__delete__(self, obj)
```

---

## 2. Types of Descriptors

### Data Descriptor

Implements `__get__` AND `__set__` (or `__delete__`):

```python
class DataDescriptor:
    def __get__(self, obj, objtype=None):
        return obj._x

    def __set__(self, obj, value):
        obj._x = value
```

Takes precedence over instance attributes.

---

### Non-Data Descriptor

Implements only `__get__`:

```python
class NonDataDescriptor:
    def __get__(self, obj, objtype=None):
        return 42
```

Lower priority than instance attributes.

---

## 3. Descriptor in Action

```python
class A:
    x = NonDataDescriptor()

a = A()
print(a.x)  # calls x.__get__(a, A)
```

---

## 4. Where Descriptors Are Used

### 4.1 Methods

```python
class A:
    def f(self): pass
```

`f` is a **non-data descriptor**. Accessing `a.f` calls:

```python
A.__dict__['f'].__get__(a, A)
```

This returns a **bound method**.

---

### 4.2 Property

```python
class A:
    @property
    def x(self):
        return 10
```

`property` is a **data descriptor** --- it always intercepts access, even if a key of the same name exists in the instance `__dict__`.

---

### 4.3 Classmethod / Staticmethod

```python
class A:
    @classmethod
    def f(cls): pass

    @staticmethod
    def g(): pass
```

| Type | Descriptor Type |
|---|---|
| `classmethod` | non-data (binds to class) |
| `staticmethod` | non-data (returns raw function) |

---

## 5. Descriptor vs Instance Dictionary

With a non-data descriptor:

```python
class A:
    x = NonDataDescriptor()

a = A()
a.x = 100
print(a.x)  # 100 — instance dict wins
```

With a data descriptor:

```python
class A:
    x = DataDescriptor()

a = A()
a.x = 100
print(a.x)  # descriptor controls access
```

---

## 6. Descriptor Priority

```text
1. Data descriptor
2. Instance __dict__
3. Non-data descriptor
4. Class attribute
```

---

## 7. How Python Uses Descriptors

When you do:

```python
obj.attr
```

Python may call:

```python
descriptor.__get__(obj, type(obj))
```

Descriptors are triggered inside `__getattribute__`. See [`__getattribute__` vs `__getattr__`](getattribute_vs_getattr.md) for how this fits into the full pipeline.

---

## 8. Minimal Custom Descriptor Example

```python
class LoggedAttribute:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        print(f"Getting {self.name}")
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        print(f"Setting {self.name} = {value}")
        obj.__dict__[self.name] = value


class A:
    x = LoggedAttribute()

a = A()
a.x = 10      # Setting x = 10
print(a.x)    # Getting x → 10
```

---

## 9. Key Insight

Descriptors are the **engine behind Python attribute behavior**. They unify:

- methods → binding (`self`)
- properties → controlled access
- frameworks → dynamic fields

---

## Summary

- Descriptor = object controlling attribute access via `__get__`, `__set__`, `__delete__`
- Data descriptor > instance attribute > non-data descriptor
- Methods and properties are descriptors
- Core to Python OOP internals

---

## See Also

- [Attribute Lookup (Pipeline)](attribute_lookup.md)
- [`__getattribute__` vs `__getattr__`](getattribute_vs_getattr.md)
- [Properties as Descriptors](property_descriptor_connection.md)
