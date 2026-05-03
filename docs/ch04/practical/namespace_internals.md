# Namespace Internals

Understanding Python's namespace system and the Global Interpreter Lock.

!!! tip "Mental Model"
    `globals()` gives you a live, writable dictionary of the module's namespace; `locals()` gives you a snapshot that is read-only inside functions. The GIL serializes bytecode execution across threads, so pure-Python code is thread-safe at the bytecode level but not at the logic level.

## Namespace Access

### `globals()` Function

Access and modify the global namespace:

```python
# View global namespace
print(globals().keys())

# Add to global namespace
globals()['dynamic_var'] = 42
print(dynamic_var)  # 42

# Dynamic variable creation
name = 'my_variable'
globals()[name] = 100
print(my_variable)  # 100
```

### `locals()` Function

View the local namespace (read-only in functions):

```python
def function():
    x = 10
    y = 20
    
    # View locals
    print(locals())  # {'x': 10, 'y': 20}
    
    # CANNOT modify locals this way
    locals()['z'] = 30
    # z is NOT defined

# At module level, locals() == globals()
print(locals() is globals())  # True (at module level)
```

### `vars()` Function

Access object's `__dict__`:

```python
class MyClass:
    def __init__(self):
        self.x = 10
        self.y = 20

obj = MyClass()
print(vars(obj))  # {'x': 10, 'y': 20}

# Modify via vars
vars(obj)['z'] = 30
print(obj.z)  # 30
```

---

## Namespace Manipulation

### Dynamic Attribute Access

```python
# setattr/getattr
class Config:
    pass

config = Config()
setattr(config, 'debug', True)
print(getattr(config, 'debug'))  # True
print(getattr(config, 'verbose', False))  # False (default)

# Check existence
print(hasattr(config, 'debug'))  # True
```

### Dynamic Module Imports

```python
import importlib

# Import module by name
module_name = 'json'
module = importlib.import_module(module_name)

# Import from package
submodule = importlib.import_module('os.path')
```

### Exec and Eval

```python
# Execute code string
code = """
x = 10
y = 20
result = x + y
"""
namespace = {}
exec(code, namespace)
print(namespace['result'])  # 30

# Evaluate expression
result = eval('2 + 3 * 4')
print(result)  # 14

# With custom namespace
namespace = {'x': 10, 'y': 20}
result = eval('x + y', namespace)
print(result)  # 30
```

**Warning**: `exec` and `eval` are security risks with untrusted input.

---

## Global Interpreter Lock (GIL)

### What is the GIL?

The GIL is a mutex in CPython that allows only one thread to execute Python bytecode at a time.

```python
import threading

counter = 0

def increment():
    global counter
    for _ in range(1000000):
        counter += 1

# Even with threads, they don't run truly parallel
threads = [threading.Thread(target=increment) for _ in range(2)]
for t in threads:
    t.start()
for t in threads:
    t.join()

# Result may not be 2000000 due to race conditions
# (counter += 1 is not atomic at bytecode level)
```

### Thread Safety

Most Python operations are thread-safe due to the GIL:

```python
# These are atomic (thread-safe)
x = 42                    # Simple assignment
y = x                     # Simple read
lst.append(item)          # Some built-in operations

# These are NOT atomic
counter += 1              # Read-modify-write
lst[0] = lst[1] + 1       # Multiple operations
```

### Working Around the GIL

**For CPU-bound tasks, use multiprocessing:**

```python
from multiprocessing import Pool

def cpu_intensive(n):
    return sum(i * i for i in range(n))

# Uses multiple processes (bypasses GIL)
with Pool(4) as pool:
    results = pool.map(cpu_intensive, [1000000] * 4)
```

**For I/O-bound tasks, threading works well:**

```python
import threading
import requests

def fetch_url(url):
    return requests.get(url).text

# GIL released during I/O operations
urls = ['http://example.com'] * 10
threads = [threading.Thread(target=fetch_url, args=(url,)) for url in urls]
```

**For async I/O:**

```python
import asyncio
import aiohttp

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
```

---

## Memory and Namespace Interaction

### Reference Counting

```python
import sys

x = [1, 2, 3]
print(sys.getrefcount(x))  # Reference count (includes temp ref from getrefcount)

y = x  # Another reference
print(sys.getrefcount(x))  # Count increased

del y  # Remove reference
print(sys.getrefcount(x))  # Count decreased
```

### Garbage Collection

```python
import gc

# Force garbage collection
gc.collect()

# Check for circular references
gc.set_debug(gc.DEBUG_LEAK)

# Disable GC temporarily (for performance)
gc.disable()
# ... performance critical code ...
gc.enable()
```

---

## Summary

| Function | Purpose | Modifiable |
|----------|---------|------------|
| `globals()` | Global namespace | Yes |
| `locals()` | Local namespace | No (in functions) |
| `vars(obj)` | Object's `__dict__` | Yes |
| `dir(obj)` | List attributes | N/A |

GIL implications:
- Only one thread executes Python bytecode at a time
- I/O-bound: Use threading (GIL released during I/O)
- CPU-bound: Use multiprocessing (separate processes)
- Most simple operations are thread-safe
- Compound operations need explicit locking

Key points:
- Use `globals()` for dynamic global variables
- `locals()` is read-only in functions
- GIL affects CPU-bound parallelism
- Use multiprocessing for CPU-bound tasks
- Use threading/asyncio for I/O-bound tasks

---

## Exercises

**Exercise 1.**
`globals()` and `locals()` behave differently at module level vs inside functions. Predict the output:

```python
# At module level
print(globals() is locals())

def f():
    x = 10
    print(globals() is locals())
    print("x" in globals())
    print("x" in locals())

f()
```

Why are `globals()` and `locals()` the same object at module level but different inside a function?

??? success "Solution to Exercise 1"
    Output:

    ```text
    True
    False
    False
    True
    ```

    At module level, there is no separate "local" scope -- the module's global scope **is** the local scope. So `globals()` and `locals()` return the same dictionary object.

    Inside a function, `locals()` returns a dictionary representing the function's local namespace (created from the fast-locals array), while `globals()` returns the module's global namespace. These are completely separate dictionaries. `x` exists only in `f`'s local scope, so it appears in `locals()` but not `globals()`.

---

**Exercise 2.**
`dir()` and `vars()` reveal different things about an object. Predict the output:

```python
class MyClass:
    class_var = 10
    def method(self):
        pass

obj = MyClass()
obj.instance_var = 20

print("class_var" in vars(obj))
print("class_var" in dir(obj))
print("instance_var" in vars(obj))
print("method" in dir(obj))
print("__class__" in dir(obj))
```

Why does `"class_var"` appear in `dir(obj)` but not in `vars(obj)`? What is the difference between these two functions?

??? success "Solution to Exercise 2"
    Output:

    ```text
    False
    True
    True
    True
    True
    ```

    `vars(obj)` returns `obj.__dict__`, which contains only the **instance** attributes: `{'instance_var': 20}`. `class_var` is defined on the class, not the instance, so it is not in `obj.__dict__`.

    `dir(obj)` walks the entire **Method Resolution Order** (MRO): it includes attributes from the instance, the class, and all base classes (including `object`). That is why `class_var`, `method`, and `__class__` all appear in `dir(obj)`.

    Rule: `vars()` shows what an object **directly owns**. `dir()` shows everything an object **can access** through the attribute lookup chain.

---

**Exercise 3.**
The GIL (Global Interpreter Lock) affects concurrent execution. Predict which scenario benefits from threading:

```python
import threading
import time

# Scenario A: CPU-bound
def compute():
    total = sum(range(10_000_000))

# Scenario B: I/O-bound
def fetch():
    time.sleep(1)  # Simulates network I/O
```

If you run 4 instances of `compute()` with threading, will it be faster than running them sequentially? What about 4 instances of `fetch()`? Why?

??? success "Solution to Exercise 3"
    **Scenario A (CPU-bound)**: Threading provides **no speedup**. The GIL ensures only one thread executes Python bytecode at a time. Running 4 CPU-bound threads takes roughly the same time as running them sequentially (often slightly slower due to context-switching overhead). Use `multiprocessing` for CPU-bound parallelism.

    **Scenario B (I/O-bound)**: Threading provides a **~4x speedup**. When a thread calls `time.sleep(1)` (or performs real I/O like network requests), it **releases the GIL**. Other threads can execute while one is waiting for I/O. Four threads each sleeping 1 second complete in ~1 second total, not 4.

    The GIL is released during I/O operations, system calls, and certain C-extension computations (like NumPy array operations). This is why threading works well for I/O-bound tasks but not for CPU-bound Python code.
