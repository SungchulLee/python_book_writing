# json Overview

The `json` module provides tools for encoding and decoding JSON (JavaScript Object Notation) data.

!!! tip "Mental Model"
    JSON is the universal language for structured data exchange — nearly every web API speaks it. Python's `json` module is a two-way translator: it converts Python dicts, lists, and primitives into JSON strings (`dumps`/`dump`) and parses JSON strings back into Python objects (`loads`/`load`). Master these four functions and you can talk to almost any external service.

## What is JSON?

JSON is a lightweight data format for exchanging structured data.

```python
import json

# JSON basics
json_str = '{"name": "Alice", "age": 30, "city": "NYC"}'
print(f"JSON string: {json_str}")

# Parse JSON
data = json.loads(json_str)
print(f"Parsed data: {data}")
print(f"Name: {data['name']}
```

```
JSON string: {"name": "Alice", "age": 30, "city": "NYC"}
Parsed data: {'name': 'Alice', 'age': 30, 'city': 'NYC'}
Name: Alice
```

## JSON to Python Type Mapping

Understand how JSON types map to Python.

```python
import json

json_str = '''
{
    "string": "hello",
    "number": 42,
    "float": 3.14,
    "bool": true,
    "null": null,
    "array": [1, 2, 3],
    "object": {"key": "value"}
}
'''

data = json.loads(json_str)
for key, value in data.items():
    print(f"{key}: {value} ({type(value).__name__)}")
```

```
string: hello (str)
number: 42 (int)
float: 3.14 (float)
bool: True (bool)
null: None (NoneType)
array: [1, 2, 3] (list)
object: {'key': 'value'} (dict)
```

---

## Exercises

**Exercise 1.**
Write a function `is_valid_json` that takes a string and returns `True` if it is valid JSON, `False` otherwise. Test with valid JSON, invalid JSON, and empty strings.

??? success "Solution to Exercise 1"

    ```python
    import json

    def is_valid_json(text):
        try:
            json.loads(text)
            return True
        except (json.JSONDecodeError, TypeError):
            return False

    # Test
    print(is_valid_json('{"key": "value"}'))  # True
    print(is_valid_json('not json'))           # False
    print(is_valid_json(''))                   # False
    print(is_valid_json('null'))               # True
    ```

---

**Exercise 2.**
Write a function `extract_keys` that takes a JSON string representing an object and returns a sorted list of all top-level keys. For example, given `'{"b": 2, "a": 1, "c": 3}'`, return `["a", "b", "c"]`.

??? success "Solution to Exercise 2"

    ```python
    import json

    def extract_keys(json_str):
        data = json.loads(json_str)
        return sorted(data.keys())

    # Test
    print(extract_keys('{"b": 2, "a": 1, "c": 3}'))
    # ['a', 'b', 'c']
    ```

---

**Exercise 3.**
Write a function `json_type_info` that takes a JSON string and returns a dictionary mapping each top-level key to the Python type name of its value. For example, given `'{"name": "Alice", "age": 30, "active": true}'`, return `{"name": "str", "age": "int", "active": "bool"}`.

??? success "Solution to Exercise 3"

    ```python
    import json

    def json_type_info(json_str):
        data = json.loads(json_str)
        return {key: type(val).__name__ for key, val in data.items()}

    # Test
    result = json_type_info('{"name": "Alice", "age": 30, "active": true}')
    print(result)
    # {'name': 'str', 'age': 'int', 'active': 'bool'}
    ```
