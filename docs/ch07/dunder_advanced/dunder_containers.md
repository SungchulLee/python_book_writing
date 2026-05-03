# Container Protocol

Container dunder methods enable your objects to behave like built-in collections. This is part of Python's protocol-based design --- Python doesn't check your type, only whether you implement the right methods. See also [Iteration Protocol](dunder_iterables.md), [Callable Objects](dunder_callable.md), and [Context Managers](dunder_context.md).

!!! tip "Mental Model"
    A container is any object that answers three questions: "how many items?" (`__len__`), "give me this item" (`__getitem__`), and "is this item here?" (`__contains__`). Implement these methods and your object works with `len()`, `[]`, and `in` -- Python never checks whether it is "really" a list or dict.

There are two main container protocols:

- **Sequence protocol** (list-like): integer indices, ordering, slicing. Implement `__getitem__` with `int`/`slice` keys, `__len__`.
- **Mapping protocol** (dict-like): arbitrary keys, no inherent ordering. Implement `__getitem__` with hashable keys, `__len__`, `__contains__`.

## Core Container Methods

| Method | Called By | Description |
|--------|-----------|-------------|
| `__len__` | `len(obj)` | Return number of items |
| `__getitem__` | `obj[key]` | Get item by key/index |
| `__setitem__` | `obj[key] = value` | Set item by key/index |
| `__delitem__` | `del obj[key]` | Delete item by key/index |
| `__contains__` | `item in obj` | Check membership |

## __len__: Collection Length

```python
class Playlist:
    def __init__(self, songs=None):
        self._songs = songs or []
    
    def __len__(self):
        return len(self._songs)
    
    def add(self, song):
        self._songs.append(song)

playlist = Playlist(['Song A', 'Song B', 'Song C'])
print(len(playlist))  # 3

# Also enables bool() if __bool__ not defined
empty = Playlist()
if not empty:
    print("Playlist is empty")  # Prints this
```

## __getitem__: Item Access

### Index-Based Access

```python
class Sentence:
    def __init__(self, text):
        self._words = text.split()
    
    def __getitem__(self, index):
        return self._words[index]
    
    def __len__(self):
        return len(self._words)

s = Sentence("Hello World from Python")
print(s[0])      # Hello
print(s[-1])     # Python
print(s[1:3])    # ['World', 'from'] (slicing works!)
```

### Key-Based Access

```python
class Config:
    def __init__(self):
        self._data = {}
    
    def __getitem__(self, key):
        return self._data[key]
    
    def __setitem__(self, key, value):
        self._data[key] = value
    
    def __contains__(self, key):
        return key in self._data

config = Config()
config['debug'] = True
config['host'] = 'localhost'

print(config['debug'])      # True
print('debug' in config)    # True
print('missing' in config)  # False
```

### Handling Slices

```python
class MyList:
    def __init__(self, data):
        self._data = list(data)
    
    def __getitem__(self, index):
        if isinstance(index, slice):
            # Return a new MyList for slices
            return MyList(self._data[index])
        return self._data[index]
    
    def __setitem__(self, index, value):
        if isinstance(index, slice):
            self._data[index] = value
        else:
            self._data[index] = value
    
    def __repr__(self):
        return f"MyList({self._data})"

lst = MyList([1, 2, 3, 4, 5])
print(lst[1:4])       # MyList([2, 3, 4])
print(lst[::2])       # MyList([1, 3, 5])

lst[1:3] = [20, 30]
print(lst)            # MyList([1, 20, 30, 4, 5])
```

### Multi-Dimensional Access

```python
class Matrix:
    def __init__(self, rows, cols):
        self._data = [[0] * cols for _ in range(rows)]
        self._rows = rows
        self._cols = cols
    
    def __getitem__(self, key):
        if isinstance(key, tuple):
            row, col = key
            return self._data[row][col]
        # Single index returns entire row
        return self._data[key]
    
    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            row, col = key
            self._data[row][col] = value
        else:
            self._data[key] = value
    
    def __repr__(self):
        return f"Matrix({self._data})"

m = Matrix(3, 3)
m[0, 0] = 1
m[1, 1] = 5
m[2, 2] = 9
print(m[1, 1])   # 5
print(m[0])      # [1, 0, 0] (entire row)
```

## __setitem__: Item Assignment

```python
class DefaultDict:
    def __init__(self, default_factory):
        self._data = {}
        self._default = default_factory
    
    def __getitem__(self, key):
        if key not in self._data:
            self._data[key] = self._default()
        return self._data[key]
    
    def __setitem__(self, key, value):
        self._data[key] = value
    
    def __repr__(self):
        return f"DefaultDict({self._data})"

# Auto-create list for missing keys
dd = DefaultDict(list)
dd['fruits'].append('apple')
dd['fruits'].append('banana')
dd['vegetables'].append('carrot')

print(dd)  # DefaultDict({'fruits': ['apple', 'banana'], 'vegetables': ['carrot']})
```

## __delitem__: Item Deletion

```python
class Registry:
    def __init__(self):
        self._items = {}
    
    def __setitem__(self, key, value):
        self._items[key] = value
    
    def __getitem__(self, key):
        return self._items[key]
    
    def __delitem__(self, key):
        if key not in self._items:
            raise KeyError(f"'{key}' not found")
        del self._items[key]
    
    def __contains__(self, key):
        return key in self._items
    
    def __repr__(self):
        return f"Registry({self._items})"

reg = Registry()
reg['user1'] = 'Alice'
reg['user2'] = 'Bob'
print(reg)          # Registry({'user1': 'Alice', 'user2': 'Bob'})

del reg['user1']
print(reg)          # Registry({'user2': 'Bob'})
print('user1' in reg)  # False
```

## __contains__: Membership Test

```python
class Range:
    """Efficient range membership testing."""
    
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
    
    def __contains__(self, value):
        return self.start <= value < self.stop

r = Range(1, 100)
print(50 in r)   # True
print(100 in r)  # False
print(0 in r)    # False
```

### Membership Check Protocol Chain

When you write `item in obj`, Python follows a cascade of fallbacks:

!!! tip "Protocol Cascade for `in`"
    ```text
    item in obj
        → obj.__contains__(item)           # First: explicit membership test
        → else: iterate via obj.__iter__() # Second: scan via iteration
        → else: fallback to obj.__getitem__(0, 1, 2, ...)  # Third: legacy sequence
    ```
    This means you get `in` support for free if you implement either `__iter__` or `__getitem__`, even without defining `__contains__`. However, `__contains__` lets you optimize: a `set`-based container can check membership in O(1) instead of O(n) iteration.

### Without __contains__

If `__contains__` isn't defined, Python falls back to iteration:

```python
class NoContains:
    def __init__(self, data):
        self._data = data
    
    def __iter__(self):
        return iter(self._data)

nc = NoContains([1, 2, 3])
print(2 in nc)  # True (iterates through all items)
```

## __missing__: Dict Subclass Hook

`__missing__` is called by dict subclasses when a key isn't found.

```python
class AutoDict(dict):
    def __missing__(self, key):
        # Auto-create nested dicts
        self[key] = AutoDict()
        return self[key]

d = AutoDict()
d['a']['b']['c'] = 42
print(d)  # {'a': {'b': {'c': 42}}}
```

```python
class CountingDict(dict):
    def __init__(self):
        super().__init__()
        self.access_count = {}
    
    def __missing__(self, key):
        return 0  # Default value for missing keys
    
    def __getitem__(self, key):
        self.access_count[key] = self.access_count.get(key, 0) + 1
        return super().__getitem__(key) if key in self else self.__missing__(key)

cd = CountingDict()
cd['a'] = 1
print(cd['a'])     # 1
print(cd['a'])     # 1
print(cd['b'])     # 0 (missing, returns default)
print(cd.access_count)  # {'a': 2, 'b': 1}
```

## Practical Example: Sparse Matrix

```python
class SparseMatrix:
    """Memory-efficient matrix that only stores non-zero values."""
    
    def __init__(self, rows, cols, default=0):
        self._data = {}
        self.rows = rows
        self.cols = cols
        self.default = default
    
    def _validate_key(self, key):
        if not isinstance(key, tuple) or len(key) != 2:
            raise TypeError("Index must be a tuple (row, col)")
        row, col = key
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError("Index out of bounds")
    
    def __getitem__(self, key):
        self._validate_key(key)
        return self._data.get(key, self.default)
    
    def __setitem__(self, key, value):
        self._validate_key(key)
        if value == self.default:
            self._data.pop(key, None)  # Don't store default values
        else:
            self._data[key] = value
    
    def __delitem__(self, key):
        self._validate_key(key)
        self._data.pop(key, None)
    
    def __contains__(self, key):
        return key in self._data
    
    def __len__(self):
        return len(self._data)  # Number of non-default values
    
    def __repr__(self):
        return f"SparseMatrix({self.rows}x{self.cols}, {len(self)} non-zero)"

# Usage
m = SparseMatrix(1000, 1000)
m[0, 0] = 1
m[500, 500] = 42
m[999, 999] = -1

print(m[0, 0])      # 1
print(m[1, 1])      # 0 (default)
print(len(m))       # 3 (only 3 stored values)
print((500, 500) in m)  # True
print((1, 1) in m)      # False
```

## Sequence ABC Implementation

```python
from collections.abc import MutableSequence

class TypedList(MutableSequence):
    """List that only accepts items of a specific type."""
    
    def __init__(self, item_type, items=None):
        self._type = item_type
        self._data = []
        if items:
            for item in items:
                self.append(item)
    
    def _check_type(self, value):
        if not isinstance(value, self._type):
            raise TypeError(f"Expected {self._type.__name__}, got {type(value).__name__}")
    
    def __getitem__(self, index):
        return self._data[index]
    
    def __setitem__(self, index, value):
        self._check_type(value)
        self._data[index] = value
    
    def __delitem__(self, index):
        del self._data[index]
    
    def __len__(self):
        return len(self._data)
    
    def insert(self, index, value):
        self._check_type(value)
        self._data.insert(index, value)
    
    def __repr__(self):
        return f"TypedList[{self._type.__name__}]({self._data})"

# Usage
int_list = TypedList(int, [1, 2, 3])
int_list.append(4)
print(int_list)  # TypedList[int]([1, 2, 3, 4])

# int_list.append("five")  # TypeError: Expected int, got str
```

## Mapping ABC Implementation

```python
from collections.abc import MutableMapping

class CaseInsensitiveDict(MutableMapping):
    """Dictionary with case-insensitive string keys."""
    
    def __init__(self, data=None):
        self._data = {}
        if data:
            for key, value in data.items():
                self[key] = value
    
    def _normalize_key(self, key):
        if isinstance(key, str):
            return key.lower()
        return key
    
    def __getitem__(self, key):
        return self._data[self._normalize_key(key)]
    
    def __setitem__(self, key, value):
        self._data[self._normalize_key(key)] = value
    
    def __delitem__(self, key):
        del self._data[self._normalize_key(key)]
    
    def __iter__(self):
        return iter(self._data)
    
    def __len__(self):
        return len(self._data)
    
    def __repr__(self):
        return f"CaseInsensitiveDict({self._data})"

# Usage
headers = CaseInsensitiveDict()
headers['Content-Type'] = 'application/json'
print(headers['content-type'])  # application/json
print(headers['CONTENT-TYPE'])  # application/json
print('content-type' in headers)  # True
```

## Key Takeaways

- **Sequence vs mapping**: sequences use integer indices and support slicing; mappings use arbitrary hashable keys. Choose the right model for your data.
- `__len__` enables `len()` and boolean evaluation
- `__getitem__` enables indexing, slicing, and [iteration fallback](dunder_iterables.md)
- `__setitem__` enables item assignment with `[]`
- `__delitem__` enables item deletion with `del`
- `__contains__` enables `in` operator (falls back to iteration)
- `__missing__` is a dict-specific hook for missing keys
- Handle both integers and slices in `__getitem__` for sequence types
- Use `collections.abc` base classes for full protocol compliance
- Tuples as keys enable multi-dimensional access: `obj[row, col]`

!!! warning "When NOT to Implement Container Methods"

    Don't implement `__getitem__` when your object has no natural indexing or key-based access. If `obj[x]` would be ambiguous — does `x` mean an index, a key, a label? — use named methods instead (`obj.get_by_id(x)`). Similarly, avoid `__contains__` when membership testing has no clear meaning for your domain. Container protocols should make access feel **natural**, not force a collection metaphor onto an object that isn't one.

---

## Runnable Example: `container_methods_tutorial.py`

```python
"""
Example 4: Container Magic Methods
Demonstrates: __len__, __getitem__, __setitem__, __delitem__, __contains__, __iter__
"""


class Playlist:
    """A custom playlist container."""
    
    def __init__(self, name):
        self.name = name
        self.songs = []
    
    def __repr__(self):
        return f"Playlist('{self.name}', {len(self.songs)} songs)"
    
    def __len__(self):
        """Return the number of songs in the playlist."""
        return len(self.songs)
    
    def __getitem__(self, index):
        """Get a song by index or slice."""
        return self.songs[index]
    
    def __setitem__(self, index, value):
        """Set a song at a specific index."""
        self.songs[index] = value
    
    def __delitem__(self, index):
        """Delete a song at a specific index."""
        del self.songs[index]
    
    def __contains__(self, song):
        """Check if a song is in the playlist."""
        return song in self.songs
    
    def __iter__(self):
        """Make the playlist iterable."""
        return iter(self.songs)
    
    def add_song(self, song):
        """Add a song to the playlist."""
        self.songs.append(song)


class CustomDict:
    """A custom dictionary-like class."""
    
    def __init__(self):
        self._data = {}
    
    def __repr__(self):
        return f"CustomDict({self._data})"
    
    def __len__(self):
        """Return number of items."""
        return len(self._data)
    
    def __getitem__(self, key):
        """Get value by key."""
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found")
        return self._data[key]
    
    def __setitem__(self, key, value):
        """Set value by key."""
        print(f"Setting {key} = {value}")
        self._data[key] = value
    
    def __delitem__(self, key):
        """Delete item by key."""
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found")
        del self._data[key]
    
    def __contains__(self, key):
        """Check if key exists."""
        return key in self._data
    
    def __iter__(self):
        """Iterate over keys."""
        return iter(self._data)


class Matrix:
    """A simple 2D matrix class."""
    
    def __init__(self, rows, cols, default=0):
        self.rows = rows
        self.cols = cols
        self._data = [[default for _ in range(cols)] for _ in range(rows)]
    
    def __repr__(self):
        return f"Matrix({self.rows}x{self.cols})"
    
    def __str__(self):
        """Pretty print the matrix."""
        lines = []
        for row in self._data:
            lines.append(" ".join(f"{val:6}" for val in row))
        return "\n".join(lines)
    
    def __getitem__(self, index):
        """Get item by [row, col] or [row]."""
        if isinstance(index, tuple):
            row, col = index
            return self._data[row][col]
        else:
            return self._data[index]
    
    def __setitem__(self, index, value):
        """Set item by [row, col] or [row]."""
        if isinstance(index, tuple):
            row, col = index
            self._data[row][col] = value
        else:
            self._data[index] = value
    
    def __len__(self):
        """Return number of rows."""
        return self.rows


# Examples
if __name__ == "__main__":

    # ============================================================================
    print("=== Playlist Examples ===")
    playlist = Playlist("My Favorites")
    
    # Add songs
    playlist.add_song("Song A")
    playlist.add_song("Song B")
    playlist.add_song("Song C")
    playlist.add_song("Song D")
    
    print(f"Playlist: {playlist}")
    print(f"Length: {len(playlist)}")
    
    # Access by index
    print(f"\nFirst song: {playlist[0]}")
    print(f"Last song: {playlist[-1]}")
    
    # Slicing
    print(f"First two songs: {playlist[0:2]}")
    
    # Modify
    playlist[1] = "Song B (Remix)"
    print(f"Modified second song: {playlist[1]}")
    
    # Check membership
    print(f"\n'Song A' in playlist: {'Song A' in playlist}")
    print(f"'Song Z' in playlist: {'Song Z' in playlist}")
    
    # Iterate
    print("\nAll songs:")
    for i, song in enumerate(playlist, 1):
        print(f"  {i}. {song}")
    
    # Delete
    del playlist[2]
    print(f"\nAfter deleting index 2: {len(playlist)} songs")
    for song in playlist:
        print(f"  - {song}")
    
    print("\n\n=== CustomDict Examples ===")
    cd = CustomDict()
    
    # Set items
    cd["name"] = "Alice"
    cd["age"] = 30
    cd["city"] = "New York"
    
    print(f"\nCustomDict: {cd}")
    print(f"Length: {len(cd)}")
    
    # Get items
    print(f"\nName: {cd['name']}")
    print(f"Age: {cd['age']}")
    
    # Check membership
    print(f"\n'name' in cd: {'name' in cd}")
    print(f"'country' in cd: {'country' in cd}")
    
    # Iterate
    print("\nAll keys:")
    for key in cd:
        print(f"  {key}: {cd[key]}")
    
    # Delete
    del cd["age"]
    print(f"\nAfter deleting 'age': {cd}")
    
    print("\n\n=== Matrix Examples ===")
    matrix = Matrix(3, 3, default=0)
    
    print(f"Matrix: {matrix}")
    print(f"Length (rows): {len(matrix)}")
    
    # Set values
    matrix[0, 0] = 1
    matrix[1, 1] = 5
    matrix[2, 2] = 9
    matrix[0, 2] = 3
    
    print("\nMatrix after setting values:")
    print(matrix)
    
    # Get values
    print(f"\nValue at [1, 1]: {matrix[1, 1]}")
    print(f"First row: {matrix[0]}")
    
    # Set entire row
    matrix[1] = [2, 4, 6]
    print("\nMatrix after setting row 1:")
    print(matrix)
```

---

## Exercises

**Exercise 1.**
Create a `Phonebook` class that supports `__getitem__` (lookup by name), `__setitem__` (add/update entry), `__delitem__` (remove entry), `__contains__` (check if name exists), and `__len__` (number of entries). Demonstrate all five operations.

??? success "Solution to Exercise 1"

        class Phonebook:
            def __init__(self):
                self._entries = {}

            def __getitem__(self, name):
                return self._entries[name]

            def __setitem__(self, name, number):
                self._entries[name] = number

            def __delitem__(self, name):
                del self._entries[name]

            def __contains__(self, name):
                return name in self._entries

            def __len__(self):
                return len(self._entries)

        pb = Phonebook()
        pb["Alice"] = "555-0001"
        pb["Bob"] = "555-0002"
        print(pb["Alice"])       # 555-0001
        print("Bob" in pb)       # True
        print(len(pb))           # 2
        del pb["Bob"]
        print("Bob" in pb)       # False

---

**Exercise 2.**
Write a `CircularBuffer` class with a fixed capacity. Implement `__setitem__` (wraps index), `__getitem__` (wraps index), `__len__` (returns current size, not capacity), and `__iter__` (iterates through items in order). Show that accessing index beyond capacity wraps around.

??? success "Solution to Exercise 2"

        class CircularBuffer:
            def __init__(self, capacity):
                self.capacity = capacity
                self._data = [None] * capacity
                self._size = 0

            def __setitem__(self, index, value):
                self._data[index % self.capacity] = value
                if index >= self._size:
                    self._size = min(index + 1, self.capacity)

            def __getitem__(self, index):
                return self._data[index % self.capacity]

            def __len__(self):
                return self._size

            def __iter__(self):
                return iter(self._data[:self._size])

        buf = CircularBuffer(3)
        buf[0] = "a"
        buf[1] = "b"
        buf[2] = "c"
        print(buf[3])  # "a" — wraps around (3 % 3 = 0)
        print(len(buf))  # 3
        print(list(buf))  # ['a', 'b', 'c']

---

**Exercise 3.**
Build a `DataFrame` class that stores data as a list of dictionaries (rows). Implement `__getitem__` that supports both integer indexing (returns a row) and string indexing (returns a column as a list). Implement `__len__` (number of rows) and `__contains__` (checks if column name exists). Demonstrate both access patterns.

??? success "Solution to Exercise 3"

        class DataFrame:
            def __init__(self, data):
                self._data = data  # list of dicts

            def __getitem__(self, key):
                if isinstance(key, int):
                    return self._data[key]  # Row access
                elif isinstance(key, str):
                    return [row.get(key) for row in self._data]  # Column access
                raise TypeError(f"Invalid key type: {type(key)}")

            def __len__(self):
                return len(self._data)

            def __contains__(self, column_name):
                if not self._data:
                    return False
                return column_name in self._data[0]

        df = DataFrame([
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Charlie", "age": 35},
        ])

        print(df[0])          # {'name': 'Alice', 'age': 30}
        print(df["name"])     # ['Alice', 'Bob', 'Charlie']
        print(len(df))        # 3
        print("age" in df)    # True

---

**Exercise 4.**
Create a class `HistoryDict` that behaves like a dictionary but tracks the history of all values assigned to each key. Implement `__setitem__`, `__getitem__` (returns the current value), and add a `history(key)` method that returns the list of all values ever assigned to that key. Also implement `__contains__` and `__len__`.

??? success "Solution to Exercise 4"

        class HistoryDict:
            def __init__(self):
                self._current = {}
                self._history = {}

            def __setitem__(self, key, value):
                if key not in self._history:
                    self._history[key] = []
                self._history[key].append(value)
                self._current[key] = value

            def __getitem__(self, key):
                return self._current[key]

            def __contains__(self, key):
                return key in self._current

            def __len__(self):
                return len(self._current)

            def history(self, key):
                return self._history.get(key, [])

        hd = HistoryDict()
        hd["name"] = "Alice"
        hd["name"] = "Bob"
        hd["name"] = "Charlie"

        print(hd["name"])            # Charlie (current value)
        print(hd.history("name"))    # ['Alice', 'Bob', 'Charlie']
        print("name" in hd)          # True
        print(len(hd))               # 1 (one key)

---

**Exercise 5.**
Explain the membership check protocol chain by constructing a class that has `__getitem__` but neither `__contains__` nor `__iter__`. Show that `in` still works by falling back to `__getitem__`. Then add `__iter__` and show that `in` now uses iteration instead. Finally add `__contains__` and show it takes priority over both. What does this fallback chain tell you about how Python protocols compose?

??? success "Solution to Exercise 5"

        # Step 1: Only __getitem__ — in falls back to sequential indexing
        class OnlyGetitem:
            def __init__(self, data):
                self._data = data

            def __getitem__(self, index):
                return self._data[index]

        og = OnlyGetitem([10, 20, 30])
        print(20 in og)  # True — Python calls __getitem__(0), (1), (2), ...

        # Step 2: Add __iter__ — in now uses iteration
        class WithIter(OnlyGetitem):
            def __iter__(self):
                print("  (using __iter__)")
                return iter(self._data)

        wi = WithIter([10, 20, 30])
        print(20 in wi)  # True — uses __iter__, prints "(using __iter__)"

        # Step 3: Add __contains__ — takes priority
        class WithContains(WithIter):
            def __contains__(self, item):
                print("  (using __contains__)")
                return item in self._data

        wc = WithContains([10, 20, 30])
        print(20 in wc)  # True — uses __contains__, prints "(using __contains__)"

    The protocol chain is: `__contains__` → `__iter__` → `__getitem__`. Python tries the most specific method first and falls back to more general ones. This layered design means simple containers get `in` support for free (via `__getitem__`), while complex containers can override for performance (`__contains__` with O(1) set lookup). The same cascade principle applies throughout Python's data model.
