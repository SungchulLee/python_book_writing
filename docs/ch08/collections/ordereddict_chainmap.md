# OrderedDict and ChainMap

These are specialized dict types for specific use cases.

!!! tip "Mental Model"
    `OrderedDict` is a dict that treats key order as first-class — you can move keys to either end or compare two dicts by order, not just content. `ChainMap` is a stack of dicts searched top-down: the first dict containing a key wins. Think of it as layered configuration (command-line args shadow environment vars, which shadow defaults) without merging anything.

---

## OrderedDict

### History

Before Python 3.7, regular dicts didn't preserve insertion order. `OrderedDict` was created to guarantee order.

**Since Python 3.7**: Regular `dict` maintains insertion order. Use `OrderedDict` only for its extra features.

### Creating OrderedDict

```python
from collections import OrderedDict

od = OrderedDict()
od['a'] = 1
od['b'] = 2
od['c'] = 3

# Or from list of tuples
od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
```

### Special Features

#### move_to_end()

```python
od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])

od.move_to_end('a')             # Move to end
print(list(od.keys()))          # ['b', 'c', 'a']

od.move_to_end('c', last=False) # Move to beginning
print(list(od.keys()))          # ['c', 'b', 'a']
```

#### popitem() with last parameter

```python
od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])

od.popitem(last=True)   # Remove last: ('c', 3)
od.popitem(last=False)  # Remove first: ('a', 1)
```

### Use Case: LRU Cache

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # Mark as recently used
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Remove oldest

cache = LRUCache(2)
cache.put('a', 1)
cache.put('b', 2)
cache.get('a')      # Returns 1, moves 'a' to end
cache.put('c', 3)   # Evicts 'b' (oldest)
```

### OrderedDict vs dict

| Feature | dict (3.7+) | OrderedDict |
|---------|-------------|-------------|
| Preserves order | ✅ | ✅ |
| `move_to_end()` | ❌ | ✅ |
| `popitem(last=False)` | ❌ | ✅ |
| Equality considers order | ❌ | ✅ |
| Memory | Less | More |

```python
# Order matters for OrderedDict equality
from collections import OrderedDict

d1 = {'a': 1, 'b': 2}
d2 = {'b': 2, 'a': 1}
print(d1 == d2)  # True (dict ignores order)

od1 = OrderedDict([('a', 1), ('b', 2)])
od2 = OrderedDict([('b', 2), ('a', 1)])
print(od1 == od2)  # False (order matters!)
```

---

## ChainMap

A `ChainMap` groups multiple dicts into a single view without copying.

### Creating ChainMap

```python
from collections import ChainMap

defaults = {'color': 'red', 'size': 'medium'}
user_prefs = {'color': 'blue'}

combined = ChainMap(user_prefs, defaults)
```

### Lookup Behavior

Searches dicts in order, returns first match:

```python
combined = ChainMap(user_prefs, defaults)

print(combined['color'])  # 'blue' (from user_prefs)
print(combined['size'])   # 'medium' (from defaults)
```

### Modifications

Writes only affect the **first** dict:

```python
combined['new_key'] = 'value'
print(user_prefs)   # {'color': 'blue', 'new_key': 'value'}
print(defaults)     # {'color': 'red', 'size': 'medium'} (unchanged)
```

### Use Case: Config Layering

```python
from collections import ChainMap

# Priority: CLI > Environment > Config File > Defaults
cli_args = {'debug': True}
env_vars = {'port': 8080, 'host': '0.0.0.0'}
config_file = {'port': 3000, 'timeout': 30}
defaults = {'debug': False, 'port': 80, 'host': 'localhost', 'timeout': 60}

config = ChainMap(cli_args, env_vars, config_file, defaults)

print(config['debug'])    # True (from cli_args)
print(config['port'])     # 8080 (from env_vars)
print(config['timeout'])  # 30 (from config_file)
print(config['host'])     # '0.0.0.0' (from env_vars)
```

### Use Case: Scoped Variables

```python
from collections import ChainMap

# Simulate variable scoping (like Python's LEGB)
global_vars = {'x': 1, 'y': 2}
local_vars = {'x': 10}  # Shadows global x

scope = ChainMap(local_vars, global_vars)
print(scope['x'])  # 10 (local shadows global)
print(scope['y'])  # 2 (from global)
```

### ChainMap Methods

```python
combined = ChainMap(user_prefs, defaults)

# Access underlying dicts
combined.maps        # [user_prefs, defaults]

# Create new child scope
child = combined.new_child({'temp': 'value'})
print(child.maps)    # [{'temp': 'value'}, user_prefs, defaults]

# Get parent scope
parent = child.parents
print(parent.maps)   # [user_prefs, defaults]
```

### ChainMap vs dict.update()

| Aspect | `ChainMap` | `dict.update()` |
|--------|------------|-----------------|
| Copies data | ❌ No (view) | ✅ Yes |
| Reflects changes | ✅ Yes | ❌ No |
| Memory | Lower | Higher |
| Layered access | ✅ Yes | ❌ Flattened |

```python
# ChainMap reflects changes
d1 = {'a': 1}
d2 = {'b': 2}
cm = ChainMap(d1, d2)

d1['a'] = 100
print(cm['a'])  # 100 (reflects change!)

# dict.update() doesn't
merged = {}
merged.update(d2)
merged.update(d1)

d1['a'] = 200
print(merged['a'])  # 100 (snapshot, not live)
```

---

## Summary

| Type | Use When |
|------|----------|
| `OrderedDict` | Need `move_to_end()`, order-aware equality, or LRU cache |
| `ChainMap` | Layered config, scoped lookups, non-copying dict merge |
| Regular `dict` | Most other cases (ordered since 3.7) |

---

## Exercises

**Exercise 1.**
Write a simplified `LRUCache` class using `OrderedDict` that supports `get(key)` and `put(key, value)` with a given capacity. When the cache exceeds capacity, evict the least recently used item. Demonstrate by inserting keys `"a"`, `"b"`, `"c"` into a cache of capacity 2, then verify that `"a"` was evicted.

??? success "Solution to Exercise 1"

    ```python
    from collections import OrderedDict

    class LRUCache:
        def __init__(self, capacity):
            self.cache = OrderedDict()
            self.capacity = capacity

        def get(self, key):
            if key not in self.cache:
                return -1
            self.cache.move_to_end(key)
            return self.cache[key]

        def put(self, key, value):
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)

    # Test
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)  # Evicts "a"
    print(cache.get("a"))  # -1 (evicted)
    print(cache.get("b"))  # 2
    print(cache.get("c"))  # 3
    ```

---

**Exercise 2.**
Write a function `merge_configs` that takes any number of dictionaries (from lowest to highest priority) and returns a `ChainMap`. Then write a function `get_config_value` that takes the `ChainMap` and a key, returning the value or a default string `"NOT_SET"` if the key is not found.

??? success "Solution to Exercise 2"

    ```python
    from collections import ChainMap

    def merge_configs(*dicts):
        # Reverse so last dict has highest priority
        return ChainMap(*reversed(dicts))

    def get_config_value(config, key):
        return config.get(key, "NOT_SET")

    # Test
    defaults = {"host": "localhost", "port": 80, "debug": False}
    user = {"port": 8080}
    cli = {"debug": True}

    config = merge_configs(defaults, user, cli)
    print(get_config_value(config, "debug"))  # True (from cli)
    print(get_config_value(config, "port"))   # 8080 (from user)
    print(get_config_value(config, "host"))   # localhost (from defaults)
    print(get_config_value(config, "ssl"))    # NOT_SET
    ```

---

**Exercise 3.**
Write a function `ordered_unique` that takes a list of `(key, value)` pairs and returns an `OrderedDict` containing only the first occurrence of each key, preserving insertion order. For example, `ordered_unique([("a", 1), ("b", 2), ("a", 3), ("c", 4)])` should return `OrderedDict([("a", 1), ("b", 2), ("c", 4)])`.

??? success "Solution to Exercise 3"

    ```python
    from collections import OrderedDict

    def ordered_unique(pairs):
        result = OrderedDict()
        for key, value in pairs:
            if key not in result:
                result[key] = value
        return result

    # Test
    data = [("a", 1), ("b", 2), ("a", 3), ("c", 4)]
    result = ordered_unique(data)
    print(result)
    # OrderedDict([('a', 1), ('b', 2), ('c', 4)])
    ```
