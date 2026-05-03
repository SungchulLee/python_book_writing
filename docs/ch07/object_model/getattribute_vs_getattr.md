# `__getattribute__` vs `__getattr__`

Python provides two special methods to control attribute access:

- `__getattribute__` --- full control (intercepts everything)
- `__getattr__` --- fallback (only when lookup fails)

Understanding the difference is critical to mastering Python's object model.

!!! tip "Mental Model"
    `__getattribute__` is the front door -- every attribute access walks through it, even for attributes that exist. `__getattr__` is the back door -- it only opens when the front door fails to find the attribute. Override `__getattribute__` when you need total control (logging, proxying); override `__getattr__` when you only need a fallback for missing attributes.

---

## 1. The Attribute Access Pipeline

When you access:

```python
obj.attr
```

Python executes:

```python
type(obj).__getattribute__(obj, "attr")
```

Inside `__getattribute__`, the full lookup runs: data descriptors, instance `__dict__`, non-data descriptors, class attributes. If nothing is found, `__getattr__` is called as a last resort.

```text
obj.attr
   |
__getattribute__   <-- ALWAYS runs
   |
[1] data descriptor? --> yes --> __get__
   | no
[2] instance dict? --> yes --> return value
   | no
[3] class attr?
       |-- descriptor? --> __get__
       |-- plain value --> return
   | no
[4] __getattr__ or AttributeError
```

---

## 2. `__getattribute__`

```python
def __getattribute__(self, name):
    ...
```

### Key properties

- Called **for every attribute access**
- Runs **before any lookup**
- Controls the entire process

### Example

```python
class A:
    def __init__(self):
        self.x = 10

    def __getattribute__(self, name):
        print(f"Accessing {name}")
        return object.__getattribute__(self, name)

a = A()
print(a.x)
# Accessing x
# 10
```

### Avoid infinite recursion

```python
# WRONG --- triggers __getattribute__ again
def __getattribute__(self, name):
    return self.__dict__[name]  # infinite loop!

# CORRECT --- delegate to base implementation
def __getattribute__(self, name):
    return object.__getattribute__(self, name)
```

---

## 3. What `__getattribute__` Can Do

**Logging**: observe every attribute access for debugging.

**Modify returned values**:

```python
class A:
    def __init__(self):
        self.x = 10

    def __getattribute__(self, name):
        value = object.__getattribute__(self, name)
        if name == "x":
            return value * 2
        return value

a = A()
print(a.x)  # 20 (not 10)
```

**Block access**:

```python
def __getattribute__(self, name):
    if name == "secret":
        raise AttributeError("Access denied")
    return object.__getattribute__(self, name)
```

**Proxy / wrapper objects**: forward all access to another object.

---

## 4. `__getattr__` (Fallback Only)

```python
def __getattr__(self, name):
    ...
```

### Key properties

- Called **only if normal lookup fails**
- Does not interfere with existing attributes
- Safe extension point

### Example

```python
class A:
    def __getattr__(self, name):
        return f"{name} not found, but handled"

a = A()
a.x = 10
print(a.x)      # 10 --- normal lookup succeeds, __getattr__ not called
print(a.missing) # "missing not found, but handled"
```

---

## 5. Comparison

| Feature | `__getattribute__` | `__getattr__` |
|---|---|---|
| Called | Always | Only on failure |
| Control level | Full | Limited (fallback) |
| Risk | High (can break everything) | Low |
| Use case | Frameworks, proxies, logging | Default values, missing attrs |

---

## 6. How Descriptors Fit In

Descriptors (`__get__`, `__set__`) are triggered **inside `__getattribute__`**. If you override `__getattribute__` without calling `object.__getattribute__`:

- `@property` may stop working
- methods may not bind
- descriptor logic may break

Always delegate to `object.__getattribute__` unless you have a specific reason not to.

---

## 7. When to Use Which

**Use `__getattr__` when:**

- You want default values for missing attributes
- You are implementing lazy attributes
- You want safe, non-intrusive behavior

**Use `__getattribute__` when:**

- You need to intercept ALL access (including existing attributes)
- You are building frameworks, ORMs, or proxy objects
- You need logging or access control on every attribute read

---

## Summary

- `__getattribute__` is the engine of attribute access --- it runs for every `obj.attr` and triggers descriptors internally.
- `__getattr__` is the safety net --- it runs only when normal lookup fails.
- Override `__getattribute__` with care; always delegate to `object.__getattribute__` to preserve descriptor behavior.

---

## See Also

- [Attribute Lookup (Pipeline)](attribute_lookup.md)
- [Descriptors](descriptors.md)
- [Properties as Descriptors](property_descriptor_connection.md)
