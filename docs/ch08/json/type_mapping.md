# JSON and Python Type Mapping

Understanding the mapping between JSON data types and Python data types.

!!! tip "Mental Model"
    JSON has only six data types (string, number, object, array, boolean, null), while Python has many more. The `json` module maps each JSON type to a natural Python counterpart (object to dict, array to list, null to None) and vice versa. Knowing this mapping tells you exactly what comes out of `json.loads` and what goes into `json.dumps` without surprises.

## JSON to Python Mapping

How JSON types convert to Python types.

```python
import json

mapping = {
    '"string"': str,
    '42': int,
    '3.14': float,
    'true': bool,
    'false': bool,
    'null': type(None),
    '[]': list,
    '{}': dict
}

for json_val, py_type in mapping.items():
    obj = json.loads(json_val)
    print(f"{json_val:15} -> {type(obj).__name__:10} (expected: {py_type.__name__})")
```

```
"string"         -> str        (expected: str)
42              -> int        (expected: int)
3.14            -> float      (expected: float)
true            -> bool       (expected: bool)
false           -> bool       (expected: bool)
null            -> NoneType   (expected: NoneType)
[]              -> list       (expected: list)
{}              -> dict       (expected: dict)
```

## Python to JSON Mapping

How Python types convert to JSON.

```python
import json

data = {
    "string": "hello",
    "int": 42,
    "float": 3.14,
    "bool": True,
    "none": None,
    "list": [1, 2, 3],
    "dict": {"nested": "value"}
}

json_str = json.dumps(data)
print(json_str)

# Parse back to see types
parsed = json.loads(json_str)
for key, val in parsed.items():
    print(f"{key}: {type(val).__name__}")
```

```
{"string": "hello", "int": 42, "float": 3.14, "bool": true, "none": null, "list": [1, 2, 3], "dict": {"nested": "value"}}
string: str
int: int
float: float
bool: bool
none: NoneType
list: list
dict: dict
```

---

## Exercises

**Exercise 1.**
Write a function `python_to_json_types` that takes a Python dictionary and returns a new dictionary showing the JSON type each value will become. Map `int`/`float` to `"number"`, `str` to `"string"`, `bool` to `"boolean"`, `None` to `"null"`, `list` to `"array"`, and `dict` to `"object"`.

??? success "Solution to Exercise 1"

    ```python
    def python_to_json_types(d):
        type_map = {
            int: "number", float: "number",
            str: "string", bool: "boolean",
            type(None): "null", list: "array",
            dict: "object",
        }
        return {
            key: type_map.get(type(val), "unknown")
            for key, val in d.items()
        }

    # Test
    data = {"name": "Alice", "age": 30, "active": True, "data": None}
    print(python_to_json_types(data))
    # {'name': 'string', 'age': 'number', 'active': 'boolean', 'data': 'null'}
    ```

---

**Exercise 2.**
Write a function `find_type_mismatches` that takes a Python dictionary before and after a JSON round-trip (`dumps` then `loads`) and returns a list of keys where the type changed. For example, tuples become lists in JSON, so `{"data": (1, 2)}` would flag `"data"`.

??? success "Solution to Exercise 2"

    ```python
    import json

    def find_type_mismatches(original):
        json_str = json.dumps(original)
        loaded = json.loads(json_str)
        mismatches = []
        for key in original:
            if type(original[key]) != type(loaded[key]):
                mismatches.append(key)
        return mismatches

    # Test
    data = {"nums": (1, 2, 3), "name": "Alice", "count": 5}
    print(find_type_mismatches(data))  # ['nums'] (tuple -> list)
    ```

---

**Exercise 3.**
Write a function `ensure_json_compatible` that takes a Python dictionary and replaces any non-serializable values with their string representation. It should handle `set`, `tuple`, `bytes`, and other common types that JSON cannot serialize directly.

??? success "Solution to Exercise 3"

    ```python
    import json

    def ensure_json_compatible(d):
        result = {}
        for key, value in d.items():
            try:
                json.dumps(value)
                result[key] = value
            except (TypeError, ValueError):
                result[key] = str(value)
        return result

    # Test
    data = {
        "name": "Alice",
        "tags": {"python", "coding"},
        "data": b"bytes",
        "scores": [95, 87],
    }
    safe = ensure_json_compatible(data)
    print(json.dumps(safe))
    ```
