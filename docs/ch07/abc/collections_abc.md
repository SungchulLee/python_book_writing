# collections.abc

The `collections.abc` module provides abstract base classes for container types. Every built-in container — `list`, `dict`, `set` — follows implicit contracts defined by dunder methods like `__getitem__`, `__iter__`, and `__len__`. The `collections.abc` module formalizes these contracts: inherit from the right ABC, implement a handful of required methods, and Python gives you a complete, consistent container with many methods provided for free.

!!! tip "Mental Model"
    Think of `collections.abc` as a vending machine: you insert a few required methods (the coins), and the ABC dispenses a fully functional container with all the convenience methods included. The insight is that containers are not monolithic -- they are layered contracts, and each ABC defines exactly which layer you are buying into.

!!! tip "Key Insight"
    `collections.abc` turns the question from "which dunder methods does `list` use?" into "implement these 2–3 methods and get a full `Sequence` for free." This is the **minimal implementation → inherited power** principle.

---

## Built-in Types and Their ABCs

Before diving into the classes, it helps to see how built-in types relate to these ABCs:

| Built-in type | Satisfies ABC |
|---|---|
| `list`, `tuple`, `range`, `str` | `Sequence` |
| `list` | `MutableSequence` |
| `dict` | `MutableMapping` |
| `set` | `MutableSet` |
| `frozenset` | `Set` |
| functions, lambdas | `Callable` |

All built-in containers are already registered as virtual subclasses of the corresponding ABCs, so `isinstance([1,2,3], Sequence)` returns `True` without any extra work.

---

## Common Abstract Base Classes

```python
from collections.abc import Sequence, Mapping, Set

# Check if object is a Sequence
list_obj = [1, 2, 3]
print(isinstance(list_obj, Sequence))  # True

tuple_obj = (1, 2, 3)
print(isinstance(tuple_obj, Sequence))  # True

dict_obj = {'a': 1}
print(isinstance(dict_obj, Mapping))    # True

set_obj = {1, 2, 3}
print(isinstance(set_obj, Set))         # True
```

## Creating a Custom Sequence

```python
from collections.abc import Sequence

class CustomList(Sequence):
    def __init__(self, data):
        self._data = list(data)
    
    def __getitem__(self, index):
        return self._data[index]
    
    def __len__(self):
        return len(self._data)

custom = CustomList([10, 20, 30])
print(custom[0])           # 10
print(len(custom))         # 3
print(20 in custom)        # True  (inherited __contains__)
print(list(custom))        # [10, 20, 30]

# Supports iteration (inherited __iter__)
for item in custom:
    print(item)
```

!!! tip "Inherited for Free — How It Works"
    `CustomList` only implements `__getitem__` and `__len__`, yet it automatically
    gains `__contains__`, `__iter__`, `__reversed__`, `index()`, and `count()`. This
    works because `Sequence`'s mixin methods are built on top of the two core
    primitives:

    - `__contains__` iterates via `__getitem__` to check membership
    - `__iter__` calls `__getitem__` with indices `0, 1, 2, ...`
    - `index()` and `count()` iterate to find/count matches

    The same pattern applies across all `collections.abc` classes: each ABC defines
    a small set of required methods and derives everything else from them.

!!! warning "Performance caveat"
    The inherited mixin methods are correct but not always fast. Because they are
    generic implementations built on iteration, they are typically **O(n)**. For
    example, `__contains__` on a `Sequence` does a linear scan — unlike `set`'s
    O(1) lookup. If performance matters, override the inherited methods with
    optimized versions.

## Creating a Custom Mapping

```python
from collections.abc import Mapping

class DictWrapper(Mapping):
    def __init__(self, data):
        self._data = dict(data)
    
    def __getitem__(self, key):
        return self._data[key]
    
    def __iter__(self):
        return iter(self._data)
    
    def __len__(self):
        return len(self._data)

wrapper = DictWrapper({'a': 1, 'b': 2})
print(wrapper['a'])        # 1
print(len(wrapper))        # 2
print('b' in wrapper)      # True
print(dict(wrapper))       # {'a': 1, 'b': 2}
```

## Creating a Custom Set

```python
from collections.abc import Set

class UniqueList(Set):
    def __init__(self, data):
        self._data = set(data)
    
    def __contains__(self, item):
        return item in self._data
    
    def __iter__(self):
        return iter(self._data)
    
    def __len__(self):
        return len(self._data)

unique = UniqueList([1, 2, 2, 3, 3, 3])
print(len(unique))                    # 3
print(2 in unique)                    # True
print(unique & UniqueList([2, 3, 4])) # {2, 3} - set operations work!
```

## Iterator and Iterable

The `Iterable` and `Iterator` ABCs formalize the two sides of Python's iteration
protocol. Every container ABC above (`Sequence`, `Mapping`, `Set`) is also an
`Iterable`, because they all provide `__iter__`. Understanding these two ABCs
directly clarifies how `for` loops, comprehensions, and `next()` work under the hood.

```python
from collections.abc import Iterator, Iterable

class CountUp(Iterable):
    def __init__(self, max):
        self.max = max
    
    def __iter__(self):
        return CountUpIterator(self.max)

class CountUpIterator(Iterator):
    def __init__(self, max):
        self.current = 1
        self.max = max
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current <= self.max:
            result = self.current
            self.current += 1
            return result
        else:
            raise StopIteration

counter = CountUp(3)
for num in counter:
    print(num)  # 1, 2, 3
```

## Callable

```python
from collections.abc import Callable

# Check if something is callable
print(callable(print))           # True
print(callable(int))             # True
print(callable([]))              # False

def my_function():
    pass

print(isinstance(my_function, Callable))  # True

class CallableClass:
    def __call__(self):
        return "Called!"

obj = CallableClass()
print(isinstance(obj, Callable))  # True
print(obj())                       # Called!
```

## Container

```python
from collections.abc import Container

class AllowList(Container):
    def __init__(self, allowed_items):
        self._allowed = set(allowed_items)
    
    def __contains__(self, item):
        return item in self._allowed

allowlist = AllowList(['admin', 'moderator', 'user'])
print('admin' in allowlist)    # True
print('guest' in allowlist)    # False
```

## Sized and Hashable

```python
from collections.abc import Sized, Hashable

# String is both Sized and Hashable
text = "hello"
print(isinstance(text, Sized))     # True
print(isinstance(text, Hashable))  # True

# List is Sized but not Hashable
lst = [1, 2, 3]
print(isinstance(lst, Sized))      # True
print(isinstance(lst, Hashable))   # False
```

## Practical Example: LRU Cache Using ABC

```python
from collections.abc import MutableMapping

class SimpleLRUCache(MutableMapping):
    def __init__(self, max_size=10):
        self._cache = {}
        self._access_order = []
        self.max_size = max_size
    
    def __getitem__(self, key):
        self._access_order.remove(key)
        self._access_order.append(key)
        return self._cache[key]
    
    def __setitem__(self, key, value):
        if len(self._cache) >= self.max_size and key not in self._cache:
            oldest = self._access_order.pop(0)
            del self._cache[oldest]
        
        if key in self._cache:
            self._access_order.remove(key)
        self._cache[key] = value
        self._access_order.append(key)
    
    def __delitem__(self, key):
        del self._cache[key]
        self._access_order.remove(key)
    
    def __iter__(self):
        return iter(self._cache)
    
    def __len__(self):
        return len(self._cache)

cache = SimpleLRUCache(3)
cache['a'] = 1
cache['b'] = 2
cache['c'] = 3
cache['d'] = 4  # Evicts 'a'
print(dict(cache))  # {'b': 2, 'c': 3, 'd': 4}
```

---

## Exercises

**Exercise 1.**
Create a class `SortedList` that inherits from `collections.abc.Sequence`. It should store items in sorted order internally. Implement `__getitem__` and `__len__`, then demonstrate that inherited methods like `__contains__`, `__iter__`, `index()`, and `count()` work automatically.

??? success "Solution to Exercise 1"

        from collections.abc import Sequence

        class SortedList(Sequence):
            def __init__(self, data):
                self._data = sorted(data)

            def __getitem__(self, index):
                return self._data[index]

            def __len__(self):
                return len(self._data)

        sl = SortedList([5, 2, 8, 1, 9, 3])
        print(list(sl))         # [1, 2, 3, 5, 8, 9]
        print(len(sl))          # 6
        print(3 in sl)          # True (__contains__ inherited)
        print(sl.index(5))      # 3 (index() inherited)
        print(sl.count(8))      # 1 (count() inherited)

        for item in sl:         # __iter__ inherited
            print(item, end=" ")
        # 1 2 3 5 8 9

---

**Exercise 2.**
Implement a `CaseInsensitiveDict` by inheriting from `collections.abc.MutableMapping`. Keys should be stored and looked up in lowercase. Implement all required abstract methods (`__getitem__`, `__setitem__`, `__delitem__`, `__iter__`, `__len__`). Show that inherited methods like `keys()`, `values()`, `items()`, and `get()` work correctly.

??? success "Solution to Exercise 2"

        from collections.abc import MutableMapping

        class CaseInsensitiveDict(MutableMapping):
            def __init__(self, data=None, **kwargs):
                self._data = {}
                if data:
                    for k, v in data.items():
                        self[k] = v
                for k, v in kwargs.items():
                    self[k] = v

            def __getitem__(self, key):
                return self._data[key.lower()]

            def __setitem__(self, key, value):
                self._data[key.lower()] = value

            def __delitem__(self, key):
                del self._data[key.lower()]

            def __iter__(self):
                return iter(self._data)

            def __len__(self):
                return len(self._data)

        d = CaseInsensitiveDict({"Name": "Alice", "AGE": 30})
        print(d["name"])          # Alice
        print(d["NAME"])          # Alice
        print(d.get("age", 0))   # 30 (inherited get())
        print(list(d.keys()))    # ['name', 'age']
        print(list(d.values())) # ['Alice', 30]

---

**Exercise 3.**
Build a `Countdown` iterable by creating two classes: `Countdown` inheriting from `collections.abc.Iterable` and `CountdownIterator` inheriting from `collections.abc.Iterator`. `Countdown(n)` should produce values from `n` down to `1` when iterated. Demonstrate that the same `Countdown` object can be iterated multiple times (each time producing a fresh iterator).

??? success "Solution to Exercise 3"

        from collections.abc import Iterable, Iterator

        class CountdownIterator(Iterator):
            def __init__(self, start):
                self._current = start

            def __next__(self):
                if self._current < 1:
                    raise StopIteration
                value = self._current
                self._current -= 1
                return value

        class Countdown(Iterable):
            def __init__(self, start):
                self._start = start

            def __iter__(self):
                return CountdownIterator(self._start)

        cd = Countdown(5)

        # First iteration
        print(list(cd))  # [5, 4, 3, 2, 1]

        # Second iteration (fresh iterator)
        print(list(cd))  # [5, 4, 3, 2, 1]

        # Use in a for loop
        for num in cd:
            print(num, end=" ")
        # 5 4 3 2 1

---

**Exercise 4.**
Using the `collections.abc` module, determine which ABCs the following built-in types satisfy: `list`, `tuple`, `dict`, `set`, `frozenset`, `str`. Test each with `isinstance()` against `Sequence`, `MutableSequence`, `Mapping`, `MutableMapping`, `Set`, `MutableSet`, and `Iterable`. Summarize your findings in a table and explain why `tuple` is a `Sequence` but not a `MutableSequence`.

??? success "Solution to Exercise 4"

        from collections.abc import (
            Sequence, MutableSequence,
            Mapping, MutableMapping,
            Set, MutableSet,
            Iterable,
        )

        types = [list, tuple, dict, set, frozenset, str]
        abcs = [Sequence, MutableSequence, Mapping, MutableMapping, Set, MutableSet, Iterable]

        for t in types:
            results = {abc.__name__: issubclass(t, abc) for abc in abcs}
            matches = [name for name, val in results.items() if val]
            print(f"{t.__name__:>12}: {', '.join(matches)}")

        # Output:
        #         list: Sequence, MutableSequence, Iterable
        #        tuple: Sequence, Iterable
        #         dict: Mapping, MutableMapping, Iterable
        #          set: Set, MutableSet, Iterable
        #    frozenset: Set, Iterable
        #          str: Sequence, Iterable

    `tuple` is a `Sequence` because it supports `__getitem__` and `__len__`, but it is **not** a `MutableSequence` because it lacks `__setitem__`, `__delitem__`, and `insert()` — tuples are immutable. The `MutableSequence` ABC requires these mutation methods, which is precisely how `collections.abc` distinguishes read-only containers from writable ones.

---

**Exercise 5.**
Explain what happens if you inherit from `collections.abc.MutableMapping` but forget to implement `__delitem__`. Write the code, attempt to instantiate it, and describe the error. Then explain the design benefit: why does Python catch this at instantiation time rather than when `__delitem__` is first called?

??? success "Solution to Exercise 5"

        from collections.abc import MutableMapping

        class PartialDict(MutableMapping):
            def __init__(self):
                self._data = {}

            def __getitem__(self, key):
                return self._data[key]

            def __setitem__(self, key, value):
                self._data[key] = value

            # __delitem__ is missing!

            def __iter__(self):
                return iter(self._data)

            def __len__(self):
                return len(self._data)

        try:
            d = PartialDict()
        except TypeError as e:
            print(e)
        # Can't instantiate abstract class PartialDict
        #   with abstract method __delitem__

    Python raises `TypeError` **at instantiation time**, not when `__delitem__` is eventually called. This is the core benefit of ABCs over plain duck typing: errors surface immediately when an object is created, making them far easier to diagnose. With duck typing, the missing method would only be discovered at runtime when some code path happens to call `del d[key]` — potentially much later and harder to trace.
