# Examples and Interview Questions

Real-world applications and common interview topics related to Python variables, scope, and memory.

!!! tip "Mental Model"
    Interview questions about Python internals almost always test one thing: do you understand that names are references, not boxes? If you can trace object identity through aliasing, closures, and mutable defaults, you can reason through any tricky snippet on the spot.

## Real-World Examples

### Configuration Management

```python
class Config:
    """Application configuration with defaults and overrides."""
    
    _defaults = {
        'debug': False,
        'log_level': 'INFO',
        'max_connections': 100,
    }
    
    def __init__(self):
        self._config = dict(self._defaults)
    
    def get(self, key, default=None):
        return self._config.get(key, default)
    
    def set(self, key, value):
        self._config[key] = value
    
    def update_from_env(self):
        import os
        for key in self._defaults:
            env_key = f'APP_{key.upper()}'
            if env_key in os.environ:
                self._config[key] = os.environ[env_key]

# Singleton pattern
_config = None

def get_config():
    global _config
    if _config is None:
        _config = Config()
    return _config
```

### Caching Decorator

```python
from functools import wraps
import time

def cached(ttl_seconds=60):
    """Cache function results with time-to-live."""
    def decorator(func):
        cache = {}
        
        @wraps(func)
        def wrapper(*args):
            now = time.time()
            
            # Check cache
            if args in cache:
                result, timestamp = cache[args]
                if now - timestamp < ttl_seconds:
                    return result
            
            # Compute and cache
            result = func(*args)
            cache[args] = (result, now)
            return result
        
        wrapper.cache_clear = lambda: cache.clear()
        return wrapper
    return decorator

@cached(ttl_seconds=300)
def expensive_api_call(user_id):
    # Simulated API call
    return fetch_user_data(user_id)
```

### Event System

```python
from collections import defaultdict
from weakref import WeakMethod, ref

class EventEmitter:
    """Publish-subscribe event system."""
    
    def __init__(self):
        self._handlers = defaultdict(list)
    
    def on(self, event, handler):
        """Register event handler."""
        # Use weak reference to avoid memory leaks
        if hasattr(handler, '__self__'):
            weak_handler = WeakMethod(handler)
        else:
            weak_handler = ref(handler)
        self._handlers[event].append(weak_handler)
    
    def emit(self, event, *args, **kwargs):
        """Emit event to all handlers."""
        handlers = self._handlers[event]
        # Clean up dead references
        self._handlers[event] = [
            h for h in handlers if h() is not None
        ]
        for weak_handler in self._handlers[event]:
            handler = weak_handler()
            if handler:
                handler(*args, **kwargs)

# Usage
emitter = EventEmitter()

def on_user_login(user):
    print(f"User logged in: {user}")

emitter.on('login', on_user_login)
emitter.emit('login', 'Alice')
```

### Object Pool

```python
from contextlib import contextmanager
from threading import Lock

class ConnectionPool:
    """Thread-safe database connection pool."""
    
    def __init__(self, create_conn, max_size=10):
        self._create = create_conn
        self._max_size = max_size
        self._pool = []
        self._in_use = 0
        self._lock = Lock()
    
    @contextmanager
    def connection(self):
        conn = self._acquire()
        try:
            yield conn
        finally:
            self._release(conn)
    
    def _acquire(self):
        with self._lock:
            if self._pool:
                return self._pool.pop()
            if self._in_use < self._max_size:
                self._in_use += 1
                return self._create()
        raise RuntimeError("Connection pool exhausted")
    
    def _release(self, conn):
        with self._lock:
            self._pool.append(conn)

# Usage
pool = ConnectionPool(lambda: create_db_connection(), max_size=5)

with pool.connection() as conn:
    conn.execute("SELECT * FROM users")
```

---

## Interview Questions

### Q1: What is the output?

```python
def create_multipliers():
    return [lambda x: i * x for i in range(5)]

multipliers = create_multipliers()
print([m(2) for m in multipliers])
```

**Answer**: `[8, 8, 8, 8, 8]`

**Explanation**: Due to late binding, all lambdas capture `i` by reference. When called, `i` has its final value of 4.

**Fix**: `[lambda x, i=i: i * x for i in range(5)]`

---

### Q2: Explain the output

```python
def append_to(element, to=[]):
    to.append(element)
    return to

print(append_to(1))
print(append_to(2))
print(append_to(3))
```

**Answer**: `[1]`, `[1, 2]`, `[1, 2, 3]`

**Explanation**: Mutable default arguments are evaluated once at function definition, not each call.

---

### Q3: What's the difference between `is` and `==`?

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)  # ?
print(a is b)  # ?
print(a is c)  # ?
```

**Answer**: `True`, `False`, `True`

**Explanation**: 
- `==` compares values (equality)
- `is` compares identity (same object in memory)

---

### Q4: What will this print?

```python
x = 10

def outer():
    x = 20
    def inner():
        x = 30
        print(x)
    inner()
    print(x)

outer()
print(x)
```

**Answer**: `30`, `20`, `10`

**Explanation**: Each function has its own local `x`. Without `global` or `nonlocal`, assignments create new local variables.

---

### Q5: Fix this closure

```python
def make_counter():
    count = 0
    def counter():
        count += 1  # UnboundLocalError!
        return count
    return counter
```

**Fixed version**:

```python
def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter
```

---

### Q6: What's wrong with this code?

```python
class Cache:
    data = {}
    
    def set(self, key, value):
        self.data[key] = value

c1 = Cache()
c2 = Cache()
c1.set('a', 1)
print(c2.data)
```

**Answer**: Prints `{'a': 1}` - unintended sharing

**Explanation**: `data` is a class variable, shared by all instances.

**Fix**:

```python
class Cache:
    def __init__(self):
        self.data = {}  # Instance variable
```

---

### Q7: Memory question

```python
import sys

a = [1, 2, 3]
b = a
c = a[:]

print(sys.getsizeof(a))
print(a is b)
print(a is c)
print(a == c)
```

**Answer**: `~88` (varies), `True`, `False`, `True`

**Explanation**:
- `b = a` creates another reference to same object
- `c = a[:]` creates a shallow copy (new object)

---

### Q8: What does `__slots__` do?

```python
class Point:
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

**Answer**: `__slots__` eliminates the per-instance `__dict__`, reducing memory usage. Instances can only have the declared attributes.

---

### Q9: Generator vs List Comprehension

```python
# Which uses less memory?
squares_list = [x**2 for x in range(1000000)]
squares_gen = (x**2 for x in range(1000000))
```

**Answer**: The generator uses far less memory because it produces values on-demand instead of storing all in memory.

---

### Q10: Explain garbage collection

**Answer**:
- Python uses reference counting as primary mechanism
- Each object tracks how many references point to it
- When count reaches 0, memory is freed
- Cycle detector handles circular references
- `gc` module provides control over garbage collection

---

## Summary

### Key Interview Topics

| Topic | What to Know |
|-------|--------------|
| Late binding | Closures capture by reference |
| Mutable defaults | Evaluated once at definition |
| `is` vs `==` | Identity vs equality |
| Scope | LEGB rule, `global`, `nonlocal` |
| `__slots__` | Memory optimization |
| Generators | Lazy evaluation |
| GC | Reference counting + cycle detection |

### Red Flags to Watch For

1. Mutable default arguments
2. Late binding in loops
3. Class variables vs instance variables
4. Missing `nonlocal` or `global`
5. Using `is` for value comparison

---

## Exercises

**Exercise 1.**
A common interview question: what does this code print?

```python
def make_adders():
    return [lambda x: x + i for i in range(5)]

adders = make_adders()
print(adders[0](10))
print(adders[4](10))
print(adders[0](10) == adders[4](10))
```

Explain the bug and provide two different fixes. Which fix is more Pythonic?

??? success "Solution to Exercise 1"
    Output:

    ```text
    14
    14
    True
    ```

    All adders return the same result because the lambda captures `i` by reference. After the loop, `i` is `4`, so every lambda computes `x + 4`.

    **Fix 1** (default argument): `lambda x, i=i: x + i` -- captures the current value of `i` at each iteration.

    **Fix 2** (functools.partial): `from functools import partial; return [partial(lambda i, x: x + i, i) for i in range(5)]`.

    The default argument fix is more Pythonic and commonly used. The `partial` approach is cleaner when the captured value is not the last parameter.

---

**Exercise 2.**
Another classic: predict the output and explain the object model concepts involved:

```python
a = [[]] * 3
a[0].append(1)
print(a)

b = [[] for _ in range(3)]
b[0].append(1)
print(b)
```

Why do `a` and `b` behave differently? What is the difference between `*` repetition and a list comprehension for mutable objects?

??? success "Solution to Exercise 2"
    Output:

    ```text
    [[1], [1], [1]]
    [[1], [], []]
    ```

    `[[]] * 3` creates a list containing **three references to the same inner list**. Appending to `a[0]` mutates that shared list, so all three elements reflect the change.

    `[[] for _ in range(3)]` creates a list containing **three independent empty lists**. The comprehension evaluates `[]` fresh on each iteration, producing separate objects.

    The rule: `*` repetition with mutable objects creates **shallow copies of references**, not independent copies. This is one of the most common Python gotchas in interviews.

---

**Exercise 3.**
Scope and mutability interview question. Predict the output:

```python
x = [1, 2, 3]

def modify(lst):
    lst.append(4)
    lst = [10, 20, 30]
    lst.append(40)

modify(x)
print(x)
```

Why does `x` end up as `[1, 2, 3, 4]` and not `[10, 20, 30, 40]`? What does this reveal about Python's argument passing mechanism?

??? success "Solution to Exercise 3"
    Output:

    ```text
    [1, 2, 3, 4]
    ```

    Python passes arguments by **assignment** (pass-by-object-reference). When `modify(x)` is called, the parameter `lst` is bound to the same list object as `x`.

    - `lst.append(4)` mutates the shared object, so `x` sees the change.
    - `lst = [10, 20, 30]` **rebinds** the local name `lst` to a completely new list. This does not affect `x` -- it just makes `lst` point somewhere else.
    - `lst.append(40)` mutates the new local list, which has nothing to do with `x`.

    The key insight: **mutation** (`.append`) affects the original object because both names reference it. **Rebinding** (`=`) only changes what the local name points to, without affecting other names.
