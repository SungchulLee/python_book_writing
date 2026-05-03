# pickle and Serialization

The pickle module serializes Python objects into bytes for storage or transmission. While convenient for Python-specific data, pickle has security implications and limitations compared to other formats.

!!! tip "Mental Model"
    Pickle is Python's way of freeze-drying an object into bytes and rehydrating it later. It can handle nearly any Python object, but the resulting bytes are Python-specific and can execute arbitrary code on load. Treat unpickling untrusted data like running untrusted code -- never do it.

---

## Basic Pickling

### Serializing Objects

```python
import pickle

data = {"name": "Alice", "age": 30, "scores": [95, 87, 92]}

pickled = pickle.dumps(data)
print(f"Pickled: {type(pickled)}")

restored = pickle.loads(pickled)
print(restored)
```

Output:
```
Pickled: <class 'bytes'>
{'name': 'Alice', 'age': 30, 'scores': [95, 87, 92]}
```

### File Persistence

```python
import pickle
import io

data = [1, 2, 3, 4, 5]
buffer = io.BytesIO()

pickle.dump(data, buffer)

buffer.seek(0)
restored = pickle.load(buffer)
print(restored)
```

Output:
```
[1, 2, 3, 4, 5]
```

## Custom Objects

### Pickling Classes

```python
import pickle
import io

class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __repr__(self):
        return f"Dog(name={self.name}, age={self.age})"

dog = Dog("Buddy", 5)
buffer = io.BytesIO()

pickle.dump(dog, buffer)
buffer.seek(0)
restored = pickle.load(buffer)
print(restored)
```

Output:
```
Dog(name=Buddy, age=5)
```

## Protocols and Versions

### Protocol Versions

```python
import pickle
import io

data = {"key": "value"}

for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
    buffer = io.BytesIO()
    pickle.dump(data, buffer, protocol=protocol)
    size = buffer.tell()
    print(f"Protocol {protocol}: {size} bytes")
```

Output:
```
Protocol 0: 27 bytes
Protocol 1: 17 bytes
Protocol 2: 17 bytes
Protocol 3: 16 bytes
Protocol 4: 15 bytes
Protocol 5: 10 bytes
```

## Security Considerations

### Pickle Security Warning

```python
import pickle
import json

data = {"name": "Alice", "age": 30}
safe_json = json.dumps(data)
restored = json.loads(safe_json)
print(restored)
```

Output:
```
{'name': 'Alice', 'age': 30}
```

---

## Exercises


**Exercise 1.**
Use `pickle` to serialize and deserialize a Python dictionary containing a list, a tuple, and a nested dictionary. Verify that the deserialized object equals the original.

??? success "Solution to Exercise 1"

        ```python
        import pickle

        data = {
            "list": [1, 2, 3],
            "tuple": (4, 5, 6),
            "nested": {"a": 1, "b": 2}
        }

        serialized = pickle.dumps(data)
        restored = pickle.loads(serialized)

        print(restored == data)  # True
        print(type(restored["tuple"]))  # <class 'tuple'>
        ```

    Pickle preserves Python types exactly, including tuples (which JSON would convert to lists).

---

**Exercise 2.**
Explain why unpickling data from an untrusted source is a security risk. Write a short example showing how `pickle.loads` can execute arbitrary code.

??? success "Solution to Exercise 2"

    Never unpickle untrusted data. A malicious pickle can execute arbitrary code:

        ```python
        import pickle
        import os

        # This is DANGEROUS - for educational purposes only
        class Exploit:
            def __reduce__(self):
                return (os.system, ("echo 'compromised'",))

        payload = pickle.dumps(Exploit())
        # pickle.loads(payload)  # Would execute os.system("echo 'compromised'")
        ```

    The `__reduce__` method tells pickle how to reconstruct the object. A malicious implementation can specify any callable, including `os.system`. Always use `json` for untrusted data.

---

**Exercise 3.**
Compare `pickle` with `json` for serializing `{"name": "Alice", "scores": [95, 87, 92]}`. What are the advantages of each format?

??? success "Solution to Exercise 3"

        ```python
        import pickle
        import json

        data = {"name": "Alice", "scores": [95, 87, 92]}

        # Pickle
        p = pickle.dumps(data)
        print(f"Pickle size: {len(p)} bytes")

        # JSON
        j = json.dumps(data)
        print(f"JSON size: {len(j)} bytes")
        print(f"JSON: {j}")
        ```

    **Pickle advantages**: preserves all Python types, handles circular references.
    **JSON advantages**: human-readable, language-agnostic, safe to load from untrusted sources.
