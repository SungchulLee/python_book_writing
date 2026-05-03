# Weak Reference Patterns

!!! tip "Mental Model"
    Weak references let you observe an object without voting to keep it alive. In patterns like observer or cache, this is critical: you want to know about an object while it exists, but you don't want your reference to be the reason it can never be garbage collected. `WeakSet` and `WeakValueDictionary` are the standard tools for this.

## Observer Pattern

The observer pattern often creates memory leaks because observables hold strong references to observers. Use `WeakSet` to allow observers to be garbage collected when no longer needed elsewhere.

### Problem: Strong References

```python
class Observable:
    def __init__(self):
        self._observers = set()  # Strong references
    
    def subscribe(self, observer):
        self._observers.add(observer)
    
    def notify(self):
        for obs in self._observers:
            obs.update()

# Problem: observers never garbage collected
# even when no other references exist
```

### Solution: WeakSet

```python
import weakref

class Observable:
    def __init__(self):
        self._observers = weakref.WeakSet()
    
    def subscribe(self, observer):
        self._observers.add(observer)
    
    def unsubscribe(self, observer):
        self._observers.discard(observer)
    
    def notify(self):
        # Dead observers automatically removed
        for obs in self._observers:
            obs.update()

# Usage
class Observer:
    def update(self):
        print("Notified!")

subject = Observable()
obs = Observer()
subject.subscribe(obs)

subject.notify()  # "Notified!"

del obs  # Observer can now be garbage collected
subject.notify()  # Nothing happens — observer is gone
```

---

## Self-Cleaning Cache

Caches can consume unbounded memory. Use `WeakValueDictionary` to automatically evict entries when cached objects are no longer referenced elsewhere.

### Problem: Unbounded Cache

```python
cache = {}

def get_object(key):
    if key not in cache:
        obj = create_expensive_object(key)
        cache[key] = obj  # Stays forever!
    return cache[key]

# Cache grows without bound
```

### Solution: WeakValueDictionary

```python
import weakref

cache = weakref.WeakValueDictionary()

def get_object(key):
    obj = cache.get(key)
    if obj is None:
        obj = create_expensive_object(key)
        cache[key] = obj
    return obj

# When no other references to obj exist,
# it's automatically removed from cache
```

### Example: Image Cache

```python
import weakref

class ImageCache:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()
    
    def get_image(self, path):
        image = self._cache.get(path)
        if image is None:
            image = load_image(path)  # Expensive
            self._cache[path] = image
        return image

# Images are cached while in use
# Automatically evicted when no longer referenced
```

---

## Parent-Child Relationships

Bidirectional relationships create reference cycles. Use weak references for back-references (child → parent) to allow garbage collection.

### Problem: Reference Cycle

```python
class Parent:
    def __init__(self):
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self  # Strong back-reference

class Child:
    def __init__(self):
        self.parent = None  # Creates cycle when set

# Cycle: parent -> child -> parent
# Requires cycle GC, delays cleanup
```

### Solution: Weak Back-Reference

```python
import weakref

class Parent:
    def __init__(self):
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
        child.set_parent(self)

class Child:
    def __init__(self):
        self._parent_ref = None
    
    def set_parent(self, parent):
        self._parent_ref = weakref.ref(parent)
    
    @property
    def parent(self):
        if self._parent_ref is None:
            return None
        return self._parent_ref()  # Returns None if parent is dead

# No cycle: parent -> child -> weak_ref
# Parent can be garbage collected immediately
```

### Tree Structure Example

```python
import weakref

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []
        self._parent_ref = None
    
    def add_child(self, child):
        self.children.append(child)
        child._parent_ref = weakref.ref(self)
    
    @property
    def parent(self):
        if self._parent_ref is None:
            return None
        return self._parent_ref()
    
    def path_to_root(self):
        path = [self.value]
        node = self.parent
        while node is not None:
            path.append(node.value)
            node = node.parent
        return path[::-1]

# Usage
root = TreeNode("root")
child = TreeNode("child")
grandchild = TreeNode("grandchild")

root.add_child(child)
child.add_child(grandchild)

print(grandchild.path_to_root())  # ['root', 'child', 'grandchild']
```

---

## Summary

| Pattern | Weak Reference Type | Use Case |
|---------|---------------------|----------|
| Observer | `WeakSet` | Allow observers to be GC'd without explicit unsubscribe |
| Cache | `WeakValueDictionary` | Auto-evict cached objects when no longer used |
| Parent-Child | `weakref.ref()` | Break cycles in bidirectional relationships |

**Key Principle**: Use strong references for ownership (parent → child), weak references for back-references or non-owning relationships (child → parent, cache → cached object, observable → observer).

---

## Exercises

**Exercise 1.**
Implement an `EventBus` class that uses `weakref.WeakSet` to store subscribers. Write a test that subscribes 5 observer objects, deletes 3 of them, and then calls `notify()`. Print how many observers were actually notified and verify it equals 2.

??? success "Solution to Exercise 1"
        ```python
        import weakref
        import gc

        class EventBus:
            def __init__(self):
                self._subscribers = weakref.WeakSet()

            def subscribe(self, obj):
                self._subscribers.add(obj)

            def notify(self):
                count = 0
                for sub in self._subscribers:
                    sub.on_event()
                    count += 1
                return count

        class Subscriber:
            def __init__(self, name):
                self.name = name
            def on_event(self):
                print(f"  {self.name} notified")

        bus = EventBus()
        subs = [Subscriber(f"S{i}") for i in range(5)]
        for s in subs:
            bus.subscribe(s)

        # Delete 3 subscribers
        del subs[0], subs[1], subs[2]
        gc.collect()

        notified = bus.notify()
        print(f"Notified: {notified}")  # 2
        ```

---

**Exercise 2.**
Build an `ObjectCache` class backed by `weakref.WeakValueDictionary`. Write a test that inserts 10 objects, keeps strong references to only 3, and then triggers garbage collection. Print the cache length before and after to show automatic eviction.

??? success "Solution to Exercise 2"
        ```python
        import weakref
        import gc

        class ObjectCache:
            def __init__(self):
                self._cache = weakref.WeakValueDictionary()

            def put(self, key, value):
                self._cache[key] = value

            def __len__(self):
                return len(self._cache)

        class Heavy:
            def __init__(self, n):
                self.data = list(range(n))

        cache = ObjectCache()
        strong_refs = []

        for i in range(10):
            obj = Heavy(100)
            cache.put(f"key_{i}", obj)
            if i < 3:
                strong_refs.append(obj)

        print(f"Before GC: {len(cache)} entries")  # 10
        gc.collect()
        print(f"After GC:  {len(cache)} entries")  # 3
        ```

---

**Exercise 3.**
Create a `TreeNode` class with a `children` list (strong references) and a `parent` property backed by `weakref.ref`. Build a tree of depth 4, then delete the root. Use `weakref.ref` callbacks to print a message when each node is collected, and verify that all nodes are freed.

??? success "Solution to Exercise 3"
        ```python
        import weakref
        import gc

        class TreeNode:
            def __init__(self, value):
                self.value = value
                self.children = []
                self._parent_ref = None

            def add_child(self, child):
                self.children.append(child)
                child._parent_ref = weakref.ref(self)

            @property
            def parent(self):
                if self._parent_ref is None:
                    return None
                return self._parent_ref()

        collected = []

        def on_collect(ref):
            collected.append(ref)

        # Build tree of depth 4
        root = TreeNode("root")
        refs = [weakref.ref(root, on_collect)]

        current_level = [root]
        for depth in range(1, 4):
            next_level = []
            for parent in current_level:
                for i in range(2):
                    child = TreeNode(f"d{depth}-{i}")
                    parent.add_child(child)
                    refs.append(weakref.ref(child, on_collect))
                    next_level.append(child)
            current_level = next_level

        total_nodes = len(refs)
        del root, current_level, next_level, child, parent
        gc.collect()

        print(f"Total nodes: {total_nodes}")
        print(f"Collected:   {len(collected)}")
        print(f"All freed:   {len(collected) == total_nodes}")
        ```
