# Weak References

Weak references allow referencing objects without preventing garbage collection.

!!! tip "Mental Model"
    A normal reference is like holding an object's hand -- as long as you hold on, it cannot be collected. A weak reference is like watching the object from across the room: you can see it and interact with it while it exists, but you are not preventing it from leaving. When the object is collected, your weak reference simply returns `None`.

## Basic Weak References

```python
import weakref

class MyClass:
    pass

obj = MyClass()
weak_ref = weakref.ref(obj)

# Access via call
print(weak_ref())  # <MyClass object>

# After deletion
del obj
print(weak_ref())  # None (object was collected)
```

## WeakValueDictionary

A dictionary that doesn't prevent values from being garbage collected:

```python
import weakref

class Data:
    def __init__(self, value):
        self.value = value

cache = weakref.WeakValueDictionary()

obj = Data(42)
cache['key'] = obj

print(cache['key'].value)  # 42

del obj
# cache['key'] no longer exists (auto-removed)
```

## WeakKeyDictionary

A dictionary that doesn't prevent keys from being garbage collected:

```python
import weakref

cache = weakref.WeakKeyDictionary()

key = MyClass()
cache[key] = "value"

del key
# Entry auto-removed when key is collected
```

---

## Advanced Features

### WeakMethod

For weak references to bound methods:

```python
import weakref

class MyClass:
    def method(self):
        return "called"

obj = MyClass()
weak_method = weakref.WeakMethod(obj.method)

# Call the weak method
result = weak_method()()  # First () gets method, second () calls it
print(result)  # "called"
```

### Proxy Objects

Transparent weak references that act like the original object:

```python
import weakref

obj = [1, 2, 3]
proxy = weakref.proxy(obj)

# Use like normal object
print(proxy[0])  # 1
print(len(proxy))  # 3
proxy.append(4)
print(obj)  # [1, 2, 3, 4]

# After deletion
del obj
# proxy[0]  # ReferenceError: weakly-referenced object no longer exists
```

### Callbacks

Execute code when referenced object is collected:

```python
import weakref

def callback(ref):
    print("Object was collected!")

obj = MyClass()
weak_ref = weakref.ref(obj, callback)

del obj  # Prints: "Object was collected!"
```

---

## Limitations

### Types That Support Weak References

Most objects can be weakly referenced:

```python
import weakref

# These work
ref = weakref.ref([1, 2, 3])      # list
ref = weakref.ref({1, 2, 3})      # set
ref = weakref.ref({'a': 1})       # dict
ref = weakref.ref(MyClass())      # user-defined classes
```

### Types That Don't Support Weak References

Built-in immutable types cannot be weakly referenced:

```python
import weakref

# These raise TypeError
# weakref.ref(42)           # int
# weakref.ref("hello")      # str
# weakref.ref((1, 2, 3))    # tuple
# weakref.ref(None)         # NoneType
# weakref.ref(True)         # bool
```

### Enabling Weak References in Custom Classes

By default, classes with `__slots__` don't support weak references:

```python
class NoWeakRef:
    __slots__ = ['x', 'y']

# weakref.ref(NoWeakRef())  # TypeError

# Add __weakref__ to slots to enable
class WithWeakRef:
    __slots__ = ['x', 'y', '__weakref__']

ref = weakref.ref(WithWeakRef())  # Works
```

---

## Use Cases

### Caching

```python
import weakref

class ExpensiveObject:
    pass

_cache = weakref.WeakValueDictionary()

def get_cached(key):
    if key not in _cache:
        _cache[key] = ExpensiveObject()
    return _cache[key]

# Objects removed from cache when no longer referenced elsewhere
```

### Observer Pattern

```python
import weakref

class Subject:
    def __init__(self):
        self._observers = weakref.WeakSet()
    
    def attach(self, observer):
        self._observers.add(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update()

# Observers auto-removed when deleted
```

### Parent-Child References

```python
import weakref

class Child:
    def __init__(self, parent):
        self._parent = weakref.ref(parent)
    
    @property
    def parent(self):
        return self._parent()

# Avoids circular reference preventing garbage collection
```

---

## Summary

| Type | Description | Use Case |
|------|-------------|----------|
| `weakref.ref()` | Basic weak reference | General use |
| `WeakValueDictionary` | Dict with weak values | Caching |
| `WeakKeyDictionary` | Dict with weak keys | Metadata storage |
| `WeakSet` | Set with weak members | Observer pattern |
| `WeakMethod` | Weak reference to bound method | Callbacks |
| `proxy()` | Transparent weak reference | Drop-in replacement |

Key points:

- Weak references don't prevent garbage collection
- Useful for caches and avoiding circular references
- Not all types support weak references
- Add `__weakref__` to `__slots__` if needed

---

## Exercises

**Exercise 1.**
Create a class `Trackable` and demonstrate the lifecycle of a `weakref.ref` with a callback. Create an instance, make a weak reference with a callback that prints `"Collected!"`, verify `weak_ref()` returns the object, then delete the object and verify `weak_ref()` returns `None`.

??? success "Solution to Exercise 1"
        ```python
        import weakref

        class Trackable:
            def __init__(self, name):
                self.name = name

        def on_collect(ref):
            print("Collected!")

        obj = Trackable("test")
        weak = weakref.ref(obj, on_collect)

        print(f"Before del: {weak()}")       # <Trackable object>
        print(f"Is None: {weak() is None}")  # False

        del obj  # Prints: Collected!
        print(f"After del: {weak()}")        # None
        print(f"Is None: {weak() is None}")  # True
        ```

---

**Exercise 2.**
Write a `WeakCache` class using `WeakValueDictionary` that caches the results of an expensive function. Call the function 5 times with the same key (showing cache hits), then delete the external reference and call again (showing the entry was evicted and recomputed).

??? success "Solution to Exercise 2"
        ```python
        import weakref

        class WeakCache:
            def __init__(self, factory):
                self._cache = weakref.WeakValueDictionary()
                self._factory = factory

            def get(self, key):
                obj = self._cache.get(key)
                if obj is None:
                    print(f"  Cache miss for '{key}', computing...")
                    obj = self._factory(key)
                    self._cache[key] = obj
                else:
                    print(f"  Cache hit for '{key}'")
                return obj

        class Result:
            def __init__(self, value):
                self.value = value

        cache = WeakCache(lambda k: Result(k.upper()))

        # First call: cache miss
        r = cache.get("hello")
        # Next 4 calls: cache hits
        for _ in range(4):
            cache.get("hello")

        # Delete external reference
        del r

        # Next call: cache miss (evicted)
        r2 = cache.get("hello")
        ```

---

**Exercise 3.**
Create a slotted class `SlottedNode` with `__slots__ = ('value', '__weakref__')`. Demonstrate that (a) you can create a `weakref.ref` to it, (b) a `weakref.proxy` works transparently, and (c) after deleting the object, accessing the proxy raises `ReferenceError`.

??? success "Solution to Exercise 3"
        ```python
        import weakref

        class SlottedNode:
            __slots__ = ('value', '__weakref__')

            def __init__(self, value):
                self.value = value

        node = SlottedNode(42)

        # (a) weakref.ref works
        ref = weakref.ref(node)
        print(f"ref() value: {ref().value}")  # 42

        # (b) proxy works transparently
        proxy = weakref.proxy(node)
        print(f"proxy.value: {proxy.value}")  # 42

        # (c) After deletion, proxy raises ReferenceError
        del node
        try:
            print(proxy.value)
        except ReferenceError as e:
            print(f"ReferenceError: {e}")
        ```
