# json.dumps and json.loads

`dumps()` converts Python objects to JSON strings, while `loads()` parses JSON strings into Python objects.

!!! tip "Mental Model"
    `dumps` and `loads` are a serialization round-trip. `dumps` ("dump string") takes a Python object and produces a JSON-formatted string; `loads` ("load string") takes a JSON string and reconstructs a Python object. They are the in-memory workhorses of the `json` module — no files involved, just strings in and out.

## dumps - Python to JSON String

Convert Python objects to JSON strings.

```python
import json

data = {
    "name": "Alice",
    "age": 30,
    "hobbies": ["reading", "coding"]
}

# Convert to JSON string
json_str = json.dumps(data)
print(json_str)
print(type(json_str))
```

```
{"name": "Alice", "age": 30, "hobbies": ["reading", "coding"]}
<class 'str'>
```

## loads - JSON String to Python

Parse JSON strings into Python objects.

```python
import json

json_str = '{"name": "Bob", "age": 25, "active": true}'

# Parse JSON string
data = json.loads(json_str)
print(data)
print(type(data))
print(f"Name: {data['name']}")
print(f"Active: {data['active']}")
```

```
{'name': 'Bob', 'age': 25, 'active': True}
<class 'dict'>
Name: Bob
Active: True
```

---

## Exercises

**Exercise 1.**
Write a function `dict_to_json_sorted` that takes a dictionary and returns a JSON string with keys sorted alphabetically. For example, `dict_to_json_sorted({"banana": 2, "apple": 1})` should return `'{"apple": 1, "banana": 2}'`.

??? success "Solution to Exercise 1"

    ```python
    import json

    def dict_to_json_sorted(d):
        return json.dumps(d, sort_keys=True)

    # Test
    print(dict_to_json_sorted({"banana": 2, "apple": 1}))
    # {"apple": 1, "banana": 2}
    ```

---

**Exercise 2.**
Write a function `safe_parse` that takes a string and attempts to parse it as JSON. If parsing fails, return a default dictionary `{"error": "invalid JSON"}`. Test with both valid and invalid JSON strings.

??? success "Solution to Exercise 2"

    ```python
    import json

    def safe_parse(text):
        try:
            return json.loads(text)
        except (json.JSONDecodeError, TypeError):
            return {"error": "invalid JSON"}

    # Test
    print(safe_parse('{"name": "Alice"}'))  # {'name': 'Alice'}
    print(safe_parse('not json'))            # {'error': 'invalid JSON'}
    print(safe_parse(''))                    # {'error': 'invalid JSON'}
    ```

---

**Exercise 3.**
Write a function `json_deep_equal` that takes two JSON strings, parses them both, and returns `True` if they represent the same data structure (regardless of key ordering in the JSON strings). For example, `json_deep_equal('{"a":1,"b":2}', '{"b":2,"a":1}')` should return `True`.

??? success "Solution to Exercise 3"

    ```python
    import json

    def json_deep_equal(json_str1, json_str2):
        return json.loads(json_str1) == json.loads(json_str2)

    # Test
    print(json_deep_equal('{"a":1,"b":2}', '{"b":2,"a":1}'))  # True
    print(json_deep_equal('{"a":1}', '{"a":2}'))                # False
    print(json_deep_equal('[1,2,3]', '[1,2,3]'))                 # True
    ```
