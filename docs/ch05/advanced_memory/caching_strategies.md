# Caching Strategies

Effective caching can significantly improve performance by avoiding redundant computation and object creation.

!!! tip "Mental Model"
    Think of caching as keeping a notepad of answers you have already computed. Instead of re-solving the same math problem every time, you glance at your notepad first. The trade-off is always memory for speed -- you are renting shelf space to avoid re-doing work.

## LRU Cache

The built-in `functools.lru_cache` provides a simple Least Recently Used cache:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(x):
    print(f"Computing {x}...")
    return x ** 2

# First call computes
result = expensive_computation(10)  # Prints: Computing 10...

# Second call uses cache
result = expensive_computation(10)  # No print (cached)

# Check cache stats
print(expensive_computation.cache_info())
# CacheInfo(hits=1, misses=1, maxsize=128, currsize=1)
```

### Cache Configuration

```python
# Unlimited cache
@lru_cache(maxsize=None)
def unlimited_cache(x):
    return x ** 2

# Small cache
@lru_cache(maxsize=32)
def small_cache(x):
    return x ** 2

# Clear cache
expensive_computation.cache_clear()
```

### Typed Cache

```python
# typed=True: treat different types as different keys
@lru_cache(maxsize=128, typed=True)
def typed_cache(x):
    return x ** 2

typed_cache(10)    # Cached separately
typed_cache(10.0)  # Different cache entry
```

---

## Weak Value Cache

Automatically removes entries when values are garbage collected:

```python
import weakref

class ExpensiveObject:
    def __init__(self, data):
        self.data = data

cache = weakref.WeakValueDictionary()

def get_or_create(key):
    if key in cache:
        return cache[key]
    obj = ExpensiveObject(key)
    cache[key] = obj
    return obj

obj = get_or_create("key1")
# When obj is deleted, cache entry auto-removed
```

---

## Custom Cache Implementation

### Size-Limited Cache

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, maxsize=128):
        self.maxsize = maxsize
        self.cache = OrderedDict()
    
    def get(self, key):
        if key in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.maxsize:
            # Remove oldest (least recently used)
            self.cache.popitem(last=False)
    
    def clear(self):
        self.cache.clear()
```

### Time-Based Cache

```python
import time

class TTLCache:
    def __init__(self, ttl_seconds=60):
        self.ttl = ttl_seconds
        self.cache = {}
    
    def get(self, key):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            del self.cache[key]
        return None
    
    def put(self, key, value):
        self.cache[key] = (value, time.time())
```

---

## Object Pools

Object pools reuse expensive objects instead of creating new ones.

### Basic Object Pool

```python
class ObjectPool:
    def __init__(self, cls, size=10):
        self.cls = cls
        self.available = [cls() for _ in range(size)]
    
    def acquire(self):
        if self.available:
            return self.available.pop()
        return self.cls()  # Create new if pool empty
    
    def release(self, obj):
        self.available.append(obj)
```

### Usage Pattern

```python
class ExpensiveObject:
    def __init__(self):
        # Expensive initialization
        self.data = [0] * 10000
    
    def reset(self):
        # Reset state for reuse
        for i in range(len(self.data)):
            self.data[i] = 0

pool = ObjectPool(ExpensiveObject, size=10)

# Use object from pool
obj = pool.acquire()
try:
    # Use obj...
    obj.data[0] = 42
finally:
    obj.reset()
    pool.release(obj)
```

### Context Manager Pool

```python
from contextlib import contextmanager

class ObjectPool:
    def __init__(self, cls, size=10):
        self.cls = cls
        self.available = [cls() for _ in range(size)]
    
    @contextmanager
    def acquire(self):
        obj = self.available.pop() if self.available else self.cls()
        try:
            yield obj
        finally:
            self.available.append(obj)

# Clean usage
pool = ObjectPool(ExpensiveObject)

with pool.acquire() as obj:
    # Use obj...
    pass  # Automatically returned to pool
```

### Benefits of Object Pools

```python
import time

class HeavyObject:
    def __init__(self):
        time.sleep(0.01)  # Simulate expensive init

# Without pool: many allocations
start = time.time()
for i in range(100):
    obj = HeavyObject()
print(f"Without pool: {time.time() - start:.2f}s")

# With pool: reuse objects
pool = ObjectPool(HeavyObject, size=10)
start = time.time()
for i in range(100):
    obj = pool.acquire()
    pool.release(obj)
print(f"With pool: {time.time() - start:.2f}s")
```

---

## Choosing a Caching Strategy

| Strategy | Use When | Pros | Cons |
|----------|----------|------|------|
| `lru_cache` | Function memoization | Simple, built-in | Memory grows |
| Weak cache | Large objects | Auto-cleanup | Complex |
| TTL cache | Time-sensitive data | Fresh data | Stale window |
| Object pool | Expensive construction | Fast reuse | Manual management |

---

## Summary

Key points:

- Use `@lru_cache` for simple function memoization
- Use `WeakValueDictionary` for caches that auto-clean
- Implement custom caches for specific requirements (TTL, size)
- Use object pools when object creation is expensive
- Always consider memory vs. speed tradeoffs
- Clear caches when data becomes stale

---

## Runnable Example: `weakref_practical_example.py`

---

## Exercises

**Exercise 1.**
Implement a function `memoize(func)` that returns a decorated version of `func` using a plain dictionary as the cache. The decorator should cache results based on positional arguments. Then compare its behavior with `functools.lru_cache` by calling both on a recursive Fibonacci function with `n=30` and printing cache statistics (hit count, miss count).

??? success "Solution to Exercise 1"
        ```python
        from functools import lru_cache

        def memoize(func):
            cache = {}
            hits = 0
            misses = 0

            def wrapper(*args):
                nonlocal hits, misses
                if args in cache:
                    hits += 1
                    return cache[args]
                misses += 1
                result = func(*args)
                cache[args] = result
                return result

            def cache_info():
                return {"hits": hits, "misses": misses, "size": len(cache)}

            wrapper.cache_info = cache_info
            return wrapper

        @memoize
        def fib_manual(n):
            if n <= 1:
                return n
            return fib_manual(n - 1) + fib_manual(n - 2)

        @lru_cache(maxsize=None)
        def fib_lru(n):
            if n <= 1:
                return n
            return fib_lru(n - 1) + fib_lru(n - 2)

        print(fib_manual(30))
        print("Manual cache:", fib_manual.cache_info())

        print(fib_lru(30))
        print("lru_cache:", fib_lru.cache_info())
        ```

---

**Exercise 2.**
Build a `TTLCache` class that stores key-value pairs with a configurable time-to-live (in seconds). Implement `get(key)`, `put(key, value)`, and `cleanup()` (which removes all expired entries). Demonstrate that after sleeping past the TTL, entries are no longer retrievable and `cleanup()` reduces the internal dictionary size.

??? success "Solution to Exercise 2"
        ```python
        import time

        class TTLCache:
            def __init__(self, ttl_seconds=2):
                self.ttl = ttl_seconds
                self.cache = {}

            def put(self, key, value):
                self.cache[key] = (value, time.time())

            def get(self, key):
                if key in self.cache:
                    value, timestamp = self.cache[key]
                    if time.time() - timestamp < self.ttl:
                        return value
                    del self.cache[key]
                return None

            def cleanup(self):
                now = time.time()
                expired = [k for k, (v, t) in self.cache.items() if now - t >= self.ttl]
                for k in expired:
                    del self.cache[k]
                return len(expired)

        cache = TTLCache(ttl_seconds=1)
        cache.put("a", 100)
        cache.put("b", 200)

        print(cache.get("a"))  # 100
        print(f"Size before sleep: {len(cache.cache)}")

        time.sleep(1.1)

        print(cache.get("a"))  # None (expired)
        removed = cache.cleanup()
        print(f"Removed {removed} expired entries")
        print(f"Size after cleanup: {len(cache.cache)}")
        ```

---

**Exercise 3.**
Create a context-manager-based `ObjectPool` for a class called `Connection` (simulate an expensive `__init__` with `time.sleep(0.01)`). The pool should pre-allocate 5 objects. Write a loop that acquires and releases a connection 20 times using `with pool.acquire() as conn:`, and compare the elapsed time against creating 20 fresh `Connection()` instances without a pool.

??? success "Solution to Exercise 3"
        ```python
        import time
        from contextlib import contextmanager

        class Connection:
            def __init__(self):
                time.sleep(0.01)  # Simulate expensive init

            def reset(self):
                pass  # Reset state for reuse

        class ObjectPool:
            def __init__(self, cls, size=5):
                self.cls = cls
                self.available = [cls() for _ in range(size)]

            @contextmanager
            def acquire(self):
                obj = self.available.pop() if self.available else self.cls()
                try:
                    yield obj
                finally:
                    obj.reset()
                    self.available.append(obj)

        # With pool
        pool = ObjectPool(Connection, size=5)
        start = time.time()
        for _ in range(20):
            with pool.acquire() as conn:
                pass  # Use connection
        pool_time = time.time() - start

        # Without pool
        start = time.time()
        for _ in range(20):
            conn = Connection()
        no_pool_time = time.time() - start

        print(f"With pool:    {pool_time:.3f}s")
        print(f"Without pool: {no_pool_time:.3f}s")
        print(f"Speedup:      {no_pool_time / pool_time:.1f}x")
        ```

```python
"""
TUTORIAL: Weak References with WeakValueDictionary

This tutorial introduces WEAK REFERENCES, one of Python's advanced features
for controlling memory management and preventing memory leaks.

The Problem: Sometimes you want to keep a registry or cache of objects, but
you DON'T want to prevent those objects from being garbage collected. If you
use a normal dictionary, holding a reference to an object keeps it alive even
when no one else needs it.

The Solution: WeakValueDictionary - a special dictionary that holds "weak"
references to values. When an object is no longer referenced anywhere else,
it can be garbage collected, and the weak reference automatically disappears.

This is the Cheese example from Fluent Python, showing a stock registry where
cheese objects can be garbage collected when no longer needed.
"""

import weakref

if __name__ == "__main__":

    print("=" * 70)
    print("TUTORIAL: Weak References with WeakValueDictionary")
    print("=" * 70)

    # ============ EXAMPLE 1: The Basic Cheese Class
    print("\n# ============ EXAMPLE 1: The Basic Cheese Class")
    print("Define a simple Cheese class we'll track with weak references:\n")


    class Cheese:
        """A cheese object with a name"""

        def __init__(self, kind):
            self.kind = kind

        def __repr__(self):
            return f'Cheese({self.kind!r})'


    # Create some cheese objects
    print("Creating cheese objects:")
    brie = Cheese('Brie')
    cheddar = Cheese('Cheddar')
    parmesan = Cheese('Parmesan')

    print(f"brie = {brie}")
    print(f"cheddar = {cheddar}")
    print(f"parmesan = {parmesan}")

    # ============ EXAMPLE 2: Strong References (Normal Dictionary)
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 2: Strong References (Normal Dictionary)")
    print("Understand the problem with normal dictionaries:\n")

    print("""
    STRONG REFERENCES:
    When you store an object in a normal dictionary, the dictionary holds
    a STRONG reference to it. This prevents the object from being garbage
    collected even if you delete all your own references to it.

    PROBLEM: Memory leak - objects stay alive because the dictionary holds them.
    """)

    inventory = {}
    print("\nCreating a normal inventory dictionary:")
    inventory['Brie'] = brie
    inventory['Cheddar'] = cheddar
    print(f"inventory = {inventory}")

    print("\nDeleting our references to brie and cheddar:")
    del brie
    del cheddar

    print("\nBUT the dictionary still has them:")
    print(f"inventory['Brie'] = {inventory['Brie']}")
    print(f"inventory['Cheddar'] = {inventory['Cheddar']}")
    print("-> The dictionary's strong references keep them alive!")

    # ============ EXAMPLE 3: Weak References (WeakValueDictionary)
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 3: Weak References (WeakValueDictionary)")
    print("The solution: use WeakValueDictionary for automatic cleanup:\n")

    print("""
    WEAK REFERENCES:
    A weak reference to an object does NOT prevent it from being garbage collected.
    If an object has only weak references pointing to it, Python can delete it.
    When the object is deleted, the weak reference automatically becomes invalid.

    BENEFIT: Objects are garbage collected when no one else needs them, while
    still being accessible through the weak reference as long as they exist.
    """)

    # Create a new set of cheese objects
    cheese_list = [
        Cheese('Red Leicester'),
        Cheese('Tilsit'),
        Cheese('Brie'),
        Cheese('Parmesan')
    ]

    print("Creating cheese objects in a list:")
    for cheese in cheese_list:
        print(f"  {cheese}")

    # Create a weak-value stock dictionary
    stock = weakref.WeakValueDictionary()

    print("\nAdding cheeses to weak stock dictionary:")
    for cheese in cheese_list:
        stock[cheese.kind] = cheese
        print(f"  Added: {cheese.kind}")

    print(f"\nCurrent stock keys: {sorted(stock.keys())}")

    # ============ EXAMPLE 4: Garbage Collection with Weak References
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 4: Garbage Collection with Weak References")
    print("Watch objects disappear from weak dictionary when deleted:\n")

    print("Step 1: We have 4 cheeses in our stock")
    print(f"stock.keys() = {sorted(stock.keys())}")

    print("\nStep 2: Delete the cheese_list variable (strong reference)")
    print("This removes the strong references to all but one cheese...")
    # Keep Parmesan alive by assigning to a variable
    parmesan_ref = cheese_list[3]
    del cheese_list

    print(f"After del cheese_list:")
    print(f"stock.keys() = {sorted(stock.keys())}")
    print("Why? Only Parmesan remains because it has a strong reference (parmesan_ref)")
    print("The others are garbage collected, and their weak references disappear!")

    print("\nStep 3: Delete the last strong reference (parmesan_ref)")
    del parmesan_ref

    print(f"After del parmesan_ref:")
    print(f"stock.keys() = {sorted(stock.keys())}")
    print("Now the stock is empty! All cheeses have been garbage collected.")

    # ============ EXAMPLE 5: Demonstrating the Key Concept
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 5: Demonstrating the Key Concept")
    print("Compare normal dict vs WeakValueDictionary directly:\n")

    print("NORMAL DICTIONARY (Strong References):")
    normal_stock = {}
    normal_stock['Brie'] = Cheese('Brie')
    print(f"normal_stock = {normal_stock}")
    del Cheese  # We can still access it through the dict

    print("\nWEAKVALUEDICTIONARY (Weak References):")
    weak_stock = weakref.WeakValueDictionary()

    def create_cheese():
        """Create a temporary cheese object"""
        return Cheese('Cheddar')


    Cheese = type('Cheese', (), {'__init__': lambda self, kind: setattr(self, 'kind', kind),
                                  '__repr__': lambda self: f'Cheese({self.kind!r})'})

    cheese = create_cheese()
    weak_stock['Cheddar'] = cheese
    print(f"Before deleting cheese: weak_stock = {dict(weak_stock)}")

    del cheese
    print(f"After deleting cheese: weak_stock = {dict(weak_stock)}")
    print("-> The weak reference disappeared when cheese was garbage collected!")

    # Redefine Cheese for upcoming examples
    class Cheese:
        """A cheese object with a name"""

        def __init__(self, kind):
            self.kind = kind

        def __repr__(self):
            return f'Cheese({self.kind!r})'

    # ============ EXAMPLE 6: Practical Use Case - A Stock Registry
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 6: Practical Use Case - A Stock Registry")
    print("Real-world example: An inventory that auto-cleans expired items:\n")


    class StockRegistry:
        """A registry of items that supports automatic cleanup"""

        def __init__(self):
            self._stock = weakref.WeakValueDictionary()

        def add_item(self, name, item):
            """Add an item to the registry"""
            self._stock[name] = item

        def get_item(self, name):
            """Get an item from the registry"""
            return self._stock.get(name)

        def list_items(self):
            """List all items currently in registry"""
            return sorted(self._stock.keys())

        def __repr__(self):
            return f'StockRegistry({self.list_items()})'


    print("Creating a registry:")
    registry = StockRegistry()

    print("\nCreating cheese items and adding to registry:")
    items = {
        'Brie': Cheese('Brie'),
        'Cheddar': Cheese('Cheddar'),
        'Gouda': Cheese('Gouda'),
        'Mozzarella': Cheese('Mozzarella')
    }

    for name, cheese in items.items():
        registry.add_item(name, cheese)
        print(f"  Added: {name}")

    print(f"\nRegistry contents: {registry.list_items()}")

    print("\nNow we delete some items from our items dict:")
    del items['Cheddar']
    del items['Gouda']

    print(f"After deletion: {registry.list_items()}")
    print("-> The deleted items automatically disappeared from the registry!")

    print("\nWe can still access items with strong references:")
    brie = items['Brie']
    print(f"Get 'Brie': {registry.get_item('Brie')}")

    print("\nBut once we delete our reference:")
    del brie
    del items
    print(f"Registry contents: {registry.list_items()}")
    print("-> All items gone! Weak references auto-cleanup!")

    # ============ EXAMPLE 7: Understanding Garbage Collection
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 7: Understanding Garbage Collection")
    print("How Python decides what to garbage collect:\n")

    print("""
    REFERENCE COUNTING:
    Python uses reference counting for garbage collection. Each object has a
    count of how many references point to it. When the count drops to zero,
    the object is immediately garbage collected.

    STRONG REFERENCES (count towards the total):
      - Variable assignment: x = obj
      - Dictionary values: d['key'] = obj
      - List items: my_list.append(obj)
      - Function arguments: func(obj)
      - Return values: return obj

    WEAK REFERENCES (do NOT count):
      - Weak references created by weakref module
      - These are transparent - they don't count as real references

    EXAMPLE:

    obj = Cheese('Swiss')        # ref_count = 1 (obj)
    d = {'Swiss': obj}           # ref_count = 2 (obj + d['Swiss'])
    x = obj                      # ref_count = 3 (obj + d['Swiss'] + x)
    del obj                      # ref_count = 2 (d['Swiss'] + x)
    del x                        # ref_count = 1 (d['Swiss'])
    del d                        # ref_count = 0 -> GARBAGE COLLECTED!

    But with weak references:
    obj = Cheese('Swiss')                   # ref_count = 1
    weak_stock[obj.kind] = obj              # ref_count = 1 (weak ref doesn't count!)
    del obj                                 # ref_count = 0 -> GARBAGE COLLECTED!
    # weak_stock['Swiss'] now raises KeyError - reference is dead
    """)

    # ============ EXAMPLE 8: When to Use Weak References
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 8: When to Use Weak References")
    print("Best practices for using weak references:\n")

    print("""
    USE WEAKVALUEDICT when:
      1. You want to cache or track objects
      2. But you don't want to prevent garbage collection
      3. Objects should be auto-cleaned when they're no longer needed elsewhere
      4. Examples:
         - Object caches that auto-clean
         - Observer/listener registries
         - Reverse mappings (id -> object lookups)
         - Global object registries

    TYPICAL PATTERN:
      1. Object is created and used elsewhere
      2. Object is added to weak registry/cache for lookup
      3. When no one else needs the object, it's garbage collected
      4. Weak reference automatically disappears

    DON'T USE WEAKVALUEDICT when:
      1. You want to KEEP objects alive
      2. You need guaranteed access (object might disappear)
      3. The cost of checking for dead references is high
      4. You're dealing with primitive types (int, str, etc. - these aren't always collected)

    POTENTIAL PITFALL:
    You might expect to access weak_dict['key'] and get None if the object
    was garbage collected. Instead, you get a KeyError! The entry disappears.
    This is intentional - it keeps the dict clean.
    """)

    # ============ EXAMPLE 9: Real-World Scenario - Cache with Expiration
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 9: Real-World Scenario - Cache with Expiration")
    print("Cache that auto-expires when objects are no longer needed elsewhere:\n")


    class AutoExpireCache:
        """A cache that automatically expires unused items"""

        def __init__(self):
            self._cache = weakref.WeakValueDictionary()
            self._access_count = {}

        def store(self, key, value):
            """Store a value in cache"""
            self._cache[key] = value
            self._access_count[key] = 0

        def retrieve(self, key):
            """Retrieve a value from cache"""
            if key in self._cache:
                self._access_count[key] += 1
                return self._cache[key]
            return None

        def stats(self):
            """Show cache statistics"""
            return {
                'size': len(self._cache),
                'keys': sorted(self._cache.keys()),
                'access_count': dict(self._access_count)
            }


    print("Creating auto-expire cache:")
    cache = AutoExpireCache()

    print("\nStoring items in cache:")
    items = {}
    for i in range(3):
        key = f'item_{i}'
        value = Cheese(f'Cheese_{i}')
        items[key] = value
        cache.store(key, value)

    stats = cache.stats()
    print(f"Cache size: {stats['size']}")
    print(f"Cache keys: {stats['keys']}")

    print("\nAccessing some items:")
    cache.retrieve('item_0')
    cache.retrieve('item_0')
    cache.retrieve('item_1')

    stats = cache.stats()
    print(f"Access counts: {stats['access_count']}")

    print("\nRemoving one item from our items dict:")
    del items['item_0']

    print(f"Cache size: {cache.stats()['size']}")
    print(f"Cache keys: {cache.stats()['keys']}")
    print("-> item_0 disappeared from cache automatically!")

    # ============ EXAMPLE 10: Understanding Weak References Limitations
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 10: Understanding Weak References Limitations")
    print("Important limitations and gotchas:\n")

    print("""
    NOT ALL OBJECTS SUPPORT WEAK REFERENCES:
      - int, str, tuple, None: Do NOT support weak refs (built-in types)
      - Classes with __slots__: Might not support weak refs (depends on __weakref__)
      - Custom objects: Usually support weak refs by default

    EXAMPLE OF LIMITATION:
    """)

    try:
        weak_int = weakref.ref(42)
        print(f"Created weak ref to int 42: {weak_int}")
    except TypeError as e:
        print(f"ERROR: Can't create weak ref to int: {e}")

    print("""
    WHY THIS LIMITATION?
    Built-in immutable types are often cached and reused by Python.
    Multiple variables might point to the same int or str object.
    Weak references would be unreliable.

    SOLUTION: Only use weak refs with custom objects or custom collections.

    DEAD REFERENCES:
    Once the object is garbage collected, calling a dead weak ref returns None.
    """)

    print("\nExample of dead weak reference:")


    class Temporary:
        """A temporary object for demonstration"""
        pass


    temp = Temporary()
    weak_ref = weakref.ref(temp)

    print(f"While alive: weak_ref() = {weak_ref()}")
    del temp
    print(f"After deletion: weak_ref() = {weak_ref()}")
    print("-> Dead references return None")

    # ============ EXAMPLE 11: Advanced Pattern - Observer Pattern with Weak Refs
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 11: Advanced Pattern - Observer Pattern with Weak Refs")
    print("Using weak references to implement observer pattern:\n")


    class Subject:
        """A subject that notifies observers of changes"""

        def __init__(self):
            self._observers = weakref.WeakSet()

        def attach(self, observer):
            """Attach an observer"""
            self._observers.add(observer)

        def notify(self, message):
            """Notify all observers"""
            for observer in self._observers:
                observer.update(message)

        def observer_count(self):
            """Count active observers"""
            return len(self._observers)


    class Observer:
        """An observer that watches a subject"""

        def __init__(self, name):
            self.name = name

        def update(self, message):
            print(f"  {self.name} received: {message}")


    print("Creating a subject and observers:")
    subject = Subject()

    observers = {
        'obs1': Observer('Observer 1'),
        'obs2': Observer('Observer 2'),
        'obs3': Observer('Observer 3')
    }

    for obs in observers.values():
        subject.attach(obs)

    print(f"Active observers: {subject.observer_count()}")

    print("\nSubject notifies observers:")
    subject.notify("Hello observers!")

    print("\nDeleting one observer:")
    del observers['obs1']

    print(f"Active observers: {subject.observer_count()}")

    print("\nSubject notifies remaining observers:")
    subject.notify("Second notification")

    print("""
    WHY WEAK REFERENCES FOR OBSERVERS?
    - Observers are held only as long as someone else references them
    - When an observer is deleted, it automatically unsubscribes
    - No need to manually unsubscribe or manage observer lifetime
    - Prevents memory leaks from forgotten unsubscriptions
    """)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    KEY TAKEAWAYS:

    1. WEAK REFERENCES: References that don't prevent garbage collection
       Created with: weakref.ref(obj), WeakValueDictionary, WeakSet

    2. NORMAL REFERENCES ARE STRONG:
       - Holding a reference keeps an object alive
       - Storing in dict/list keeps object alive
       - Problem: Can cause memory leaks

    3. WEAKVALUEDICT BENEFITS:
       - Dictionary values are weak references
       - Objects auto-cleanup when no one else needs them
       - Perfect for caches, registries, object tracking
       - Automatic, clean, no manual cleanup needed

    4. WHEN TO USE:
       - Caches and registries
       - Observer/listener patterns
       - Reverse mappings
       - Anything where you want to track but not own objects

    5. IMPORTANT LIMITATIONS:
       - Not all objects support weak refs (int, str, None don't)
       - Dead references return None
       - Key disappears from dict when object is collected
       - Checking if object exists: if weak_ref() is not None

    6. MEMORY MANAGEMENT:
       - Strong refs: Count towards reference count
       - Weak refs: Don't count, transparent to object
       - When ref count hits 0: Object is garbage collected
       - Weak refs automatically become invalid

    7. PATTERN:
       1. Create object elsewhere (strong reference)
       2. Add to weak registry
       3. When done with object, delete it
       4. Weak reference auto-disappears
       5. Registry stays clean, no dead entries
    """)
```
