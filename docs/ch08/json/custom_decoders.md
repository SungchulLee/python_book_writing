# Custom Decoders (object_hook)

Use object_hook to transform JSON objects during deserialization.

!!! tip "Mental Model"
    By default, `json.loads` turns every JSON object into a plain Python dict. An `object_hook` intercepts each dict as it is created and lets you return something richer — a dataclass, a namedtuple, or a domain object. Think of it as a post-processing filter on the JSON parser's output, converting raw dicts into typed objects automatically.

## Basic object_hook Usage

Transform JSON objects with a custom function.

```python
import json
from datetime import datetime

def parse_date(obj):
    if 'date' in obj and isinstance(obj['date'], str):
        obj['date'] = datetime.fromisoformat(obj['date'])
    return obj

json_str = '{"event": "Meeting", "date": "2024-12-25T14:30:00"}'
data = json.loads(json_str, object_hook=parse_date)
print(data)
print(f"Date type: {type(data['date'])}")
```

```
{'event': 'Meeting', 'date': datetime.datetime(2024, 12, 25, 14, 30)}
Date type: <class 'datetime.datetime'>
```

## Creating Custom Classes from JSON

Convert JSON objects to custom Python classes.

```python
import json
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int

def user_decoder(obj):
    if 'name' in obj and 'age' in obj:
        return User(obj['name'], obj['age'])
    return obj

json_str = '{"name": "Alice", "age": 30}'
user = json.loads(json_str, object_hook=user_decoder)
print(user)
print(f"Type: {type(user)}")
```

```
User(name='Alice', age=30)
Type: <class '__main__.User'>
```

---

## Exercises

**Exercise 1.**
Write a custom `object_hook` function that converts JSON objects containing a `"_type": "date"` field into `datetime.date` objects. The JSON object will also have `"year"`, `"month"`, and `"day"` fields. Parse the string `'{"_type": "date", "year": 2024, "month": 12, "day": 25}'` and verify the result is a `date` object.

??? success "Solution to Exercise 1"

    ```python
    import json
    from datetime import date

    def date_decoder(obj):
        if obj.get("_type") == "date":
            return date(obj["year"], obj["month"], obj["day"])
        return obj

    json_str = '{"_type": "date", "year": 2024, "month": 12, "day": 25}'
    result = json.loads(json_str, object_hook=date_decoder)
    print(result)           # 2024-12-25
    print(type(result))     # <class 'datetime.date'>
    ```

---

**Exercise 2.**
Write a custom `object_hook` that converts JSON objects with a `"_type": "complex"` field into Python `complex` numbers, using `"real"` and `"imag"` fields. For example, `'{"_type": "complex", "real": 3, "imag": 4}'` should decode to `(3+4j)`.

??? success "Solution to Exercise 2"

    ```python
    import json

    def complex_decoder(obj):
        if obj.get("_type") == "complex":
            return complex(obj["real"], obj["imag"])
        return obj

    json_str = '{"_type": "complex", "real": 3, "imag": 4}'
    result = json.loads(json_str, object_hook=complex_decoder)
    print(result)       # (3+4j)
    print(type(result)) # <class 'complex'>
    ```

---

**Exercise 3.**
Write a decoder that handles nested custom types: a `"_type": "point"` with `"x"` and `"y"` fields, and a `"_type": "line"` with `"start"` and `"end"` fields (each being a point). Parse a JSON string representing a line and verify the structure.

??? success "Solution to Exercise 3"

    ```python
    import json
    from collections import namedtuple

    Point = namedtuple("Point", ["x", "y"])
    Line = namedtuple("Line", ["start", "end"])

    def geometry_decoder(obj):
        if obj.get("_type") == "point":
            return Point(obj["x"], obj["y"])
        if obj.get("_type") == "line":
            return Line(obj["start"], obj["end"])
        return obj

    json_str = '''
    {
        "_type": "line",
        "start": {"_type": "point", "x": 0, "y": 0},
        "end": {"_type": "point", "x": 5, "y": 10}
    }
    '''
    result = json.loads(json_str, object_hook=geometry_decoder)
    print(result)          # Line(start=Point(x=0, y=0), end=Point(x=5, y=10))
    print(result.start.x)  # 0
    print(result.end.y)    # 10
    ```
