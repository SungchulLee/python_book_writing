# Memory Leaks

메모리 누수의 원인, 탐지, 예방 방법입니다.

!!! tip "Mental Model"
    A memory leak is like filling a bathtub with the drain plugged -- memory keeps rising because objects stay reachable even though your program no longer needs them. The usual culprits are global caches that grow forever, circular references with custom `__del__` methods, and closures that accidentally capture large objects.

## Common Causes

### 1. Global References

```python
# Bad: accumulates forever
cache = []

def process(data):
    cache.append(data)  # Never cleared!

# Better: limit size
from collections import deque

cache = deque(maxlen=100)
```

### 2. Circular References

```python
class Node:
    def __init__(self):
        self.ref = None

a = Node()
b = Node()
a.ref = b
b.ref = a
# Cycle keeps both alive
```

### 3. Closures Capturing Large Objects

```python
# Leak: large object captured
def process_data():
    large = [0] * 1000000
    
    def get_first():
        return large[0]  # Captures entire list
    
    return get_first  # Keeps large alive

# Better: capture only what's needed
def process_data():
    large = [0] * 1000000
    first = large[0]
    
    def get_first():
        return first  # Only captures the value
    
    return get_first
```

### 4. Event Handlers Not Removed

```python
# Leak: handler keeps object alive
class Widget:
    def __init__(self, event_system):
        event_system.subscribe('click', self.handle)
    
    def handle(self, event):
        pass
    # Widget never collected until unsubscribed
```

---

## Finalizers (`__del__`)

`__del__`은 신뢰할 수 없고 문제를 일으킬 수 있습니다.

### Problems with `__del__`

```python
class Resource:
    def __del__(self):
        self.cleanup()

# May not be called if:
# - Program exits abruptly
# - Circular references exist
# - Exceptions in __del__
```

### Object Resurrection

```python
saved = None

class Item:
    def __del__(self):
        global saved
        saved = self  # Resurrect!

obj = Item()
del obj
print(saved)  # Object still exists!
```

### Best Practices: Avoid `__del__`

```python
# Instead of __del__, use explicit cleanup
class Resource:
    def close(self):
        # Explicit cleanup
        pass

r = Resource()
try:
    use(r)
finally:
    r.close()
```

### Better: Context Managers

```python
class Resource:
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.cleanup()

# Guaranteed cleanup
with Resource() as r:
    use(r)
```

### Or: weakref Callbacks

```python
import weakref

def cleanup(ref):
    print("Object collected")

obj = SomeObject()
ref = weakref.ref(obj, cleanup)

# cleanup called on GC (more reliable than __del__)
```

---

## Detection

### 1. Track Memory Growth

```python
import tracemalloc

tracemalloc.start()

for i in range(100):
    process()
    
    if i % 10 == 0:
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current: {current / 10**6:.1f} MB")

tracemalloc.stop()
```

### 2. Monitor Object Count

```python
import gc

before = len(gc.get_objects())

process()

after = len(gc.get_objects())
print(f"Objects created: {after - before}")
```

### 3. Find Top Allocations

```python
import tracemalloc

tracemalloc.start()

# Run code
process()

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("Top 10 allocations:")
for stat in top_stats[:10]:
    print(stat)
```

---

## GC Performance

### Collection Pauses

```python
import gc
import time

start = time.time()
collected = gc.collect()
pause = time.time() - start

print(f"Pause: {pause*1000:.2f}ms")
print(f"Collected: {collected}")
```

### Disable During Critical Sections

```python
import gc

gc.disable()
try:
    # Performance-critical code
    compute()
finally:
    gc.enable()
    gc.collect()
```

### Manual Collection Control

```python
import gc

gc.disable()

for i in range(1000):
    process()
    
    if i % 100 == 0:
        gc.collect()

gc.enable()
```

---

## GC Tuning

### Adjust Thresholds

```python
import gc

# Default: (700, 10, 10)
# Fewer collections, longer pauses:
gc.set_threshold(10000, 100, 100)

# More collections, shorter pauses:
gc.set_threshold(100, 5, 5)
```

### Reduce Allocations

```python
# Bad: many allocations
result = []
for i in range(1000):
    result.append([i])

# Better: pre-allocate
result = [None] * 1000
for i in range(1000):
    result[i] = i
```

### Monitor GC Impact

```python
import gc

# Before
before = gc.get_count()

process()

# After
after = gc.get_count()
print(f"Gen0 delta: {after[0] - before[0]}")
```

---

## Prevention Checklist

| Strategy | Implementation |
|----------|----------------|
| Limit caches | `functools.lru_cache(maxsize=128)` |
| Break cycles | `obj.parent = None` |
| Weak references | `weakref.WeakValueDictionary()` |
| Context managers | `with open_resource() as r:` |
| Explicit cleanup | `try/finally` with `.close()` |
| Avoid `__del__` | Use context managers instead |

---

## Summary

- **Causes**: globals, cycles, closures, event handlers
- **Detection**: `tracemalloc`, `gc.get_objects()`
- **Prevention**: limit caches, break cycles, use weak refs
- **Finalizers**: avoid `__del__`, use context managers
- **Performance**: tune thresholds, control collection timing

---

## Exercises

**Exercise 1.**
Create a class `EventSystem` that stores callbacks in a plain list (creating a memory leak because callbacks hold references to large objects). Demonstrate the leak by registering 1,000 callbacks that each capture a 10,000-element list. Measure memory with `tracemalloc`, then fix the leak using `weakref.WeakMethod` or `weakref.ref` and show the memory improvement.

??? success "Solution to Exercise 1"
        ```python
        import tracemalloc
        import weakref
        import gc

        class EventSystem:
            def __init__(self):
                self.callbacks = []

            def register(self, callback):
                self.callbacks.append(callback)

        class EventSystemWeak:
            def __init__(self):
                self.callbacks = []

            def register(self, callback):
                self.callbacks.append(weakref.ref(callback))

        # Leaky version
        tracemalloc.start()
        es = EventSystem()
        holders = []
        for i in range(1_000):
            data = list(range(10_000))
            def cb(d=data):
                return d[0]
            es.register(cb)
            holders.append(cb)
        _, peak_leak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Fixed version using bounded approach
        tracemalloc.start()
        es2 = EventSystemWeak()
        for i in range(1_000):
            data = list(range(10_000))
            first = data[0]  # capture only what's needed
            def cb2(v=first):
                return v
            es2.register(cb2)
        _, peak_fixed = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"Leaky peak:  {peak_leak / 1024 / 1024:.1f} MB")
        print(f"Fixed peak:  {peak_fixed / 1024 / 1024:.1f} MB")
        ```

---

**Exercise 2.**
Write a `BoundedCache` class that wraps a dictionary and limits it to a maximum of 100 entries using a FIFO eviction policy (use `collections.OrderedDict`). Demonstrate that unlike an unbounded dictionary, the cache's memory stays constant after inserting 10,000 items. Use `sys.getsizeof()` to compare sizes.

??? success "Solution to Exercise 2"
        ```python
        import sys
        from collections import OrderedDict

        class BoundedCache:
            def __init__(self, maxsize=100):
                self.maxsize = maxsize
                self.cache = OrderedDict()

            def put(self, key, value):
                if key in self.cache:
                    self.cache.move_to_end(key)
                self.cache[key] = value
                if len(self.cache) > self.maxsize:
                    self.cache.popitem(last=False)

            def get(self, key):
                return self.cache.get(key)

        # Unbounded dict
        unbounded = {}
        for i in range(10_000):
            unbounded[i] = f"value_{i}" * 10

        # Bounded cache
        bounded = BoundedCache(maxsize=100)
        for i in range(10_000):
            bounded.put(i, f"value_{i}" * 10)

        print(f"Unbounded dict size: {sys.getsizeof(unbounded):,} bytes, "
              f"entries: {len(unbounded)}")
        print(f"Bounded cache size:  {sys.getsizeof(bounded.cache):,} bytes, "
              f"entries: {len(bounded.cache)}")
        ```

---

**Exercise 3.**
Write a function that intentionally creates a closure-based memory leak: an inner function captures a large list but only uses its first element. Use `tracemalloc` to show the leak, then refactor to capture only the needed value. Compare peak memory before and after the fix.

??? success "Solution to Exercise 3"
        ```python
        import tracemalloc

        # Leaky version: closure captures entire large list
        def make_getter_leaky():
            large = list(range(1_000_000))
            def getter():
                return large[0]
            return getter

        # Fixed version: capture only the needed value
        def make_getter_fixed():
            large = list(range(1_000_000))
            first = large[0]
            def getter():
                return first
            return getter

        tracemalloc.start()
        getters_leaky = [make_getter_leaky() for _ in range(10)]
        _, peak_leaky = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tracemalloc.start()
        getters_fixed = [make_getter_fixed() for _ in range(10)]
        _, peak_fixed = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"Leaky closures peak: {peak_leaky / 1024 / 1024:.1f} MB")
        print(f"Fixed closures peak: {peak_fixed / 1024 / 1024:.1f} MB")
        ```
