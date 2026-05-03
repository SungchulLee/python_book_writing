# Custom Encoders (JSONEncoder)

Extend JSONEncoder to handle custom Python objects that aren't JSON serializable by default.

!!! tip "Mental Model"
    JSON only natively understands strings, numbers, booleans, null, arrays, and objects. A custom encoder teaches `json.dumps` how to convert Python types it doesn't recognize — like `datetime`, `Decimal`, or your own classes — into one of those six JSON-safe forms. Override `default()` in a `JSONEncoder` subclass and the serializer calls it for any object it can't handle on its own.

## Creating Custom Encoders

Subclass JSONEncoder to handle custom types.

```python
import json
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

data = {
    "event": "Conference",
    "date": datetime(2024, 12, 25, 14, 30)
}

json_str = json.dumps(data, cls=DateTimeEncoder)
print(json_str)
```

```
{"event": "Conference", "date": "2024-12-25T14:30:00"}
```

## Using default Parameter

Use the default parameter for simpler custom encoding.

```python
import json
from datetime import date

def encode_date(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

data = {
    "name": "Alice",
    "birth_date": date(1990, 5, 15)
}

json_str = json.dumps(data, default=encode_date)
print(json_str)
```

```
{"name": "Alice", "birth_date": "1990-05-15"}
```

---

## Exercises

**Exercise 1.**
Write a custom `JSONEncoder` subclass that can serialize `set` objects as sorted lists. For example, `json.dumps({"tags": {"python", "coding", "ai"}}, cls=SetEncoder)` should produce valid JSON with the set serialized as a sorted list.

??? success "Solution to Exercise 1"

    ```python
    import json

    class SetEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, set):
                return sorted(obj)
            return super().default(obj)

    data = {"tags": {"python", "coding", "ai"}}
    result = json.dumps(data, cls=SetEncoder)
    print(result)  # {"tags": ["ai", "coding", "python"]}
    ```

---

**Exercise 2.**
Write a `default` function that can serialize both `datetime` objects (as ISO format strings) and `Decimal` objects (as float values). Test it with a dictionary containing both types.

??? success "Solution to Exercise 2"

    ```python
    import json
    from datetime import datetime
    from decimal import Decimal

    def multi_encoder(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Object of type {type(obj)} is not serializable")

    data = {
        "timestamp": datetime(2024, 12, 25, 14, 30),
        "price": Decimal("19.99"),
    }
    result = json.dumps(data, default=multi_encoder)
    print(result)
    # {"timestamp": "2024-12-25T14:30:00", "price": 19.99}
    ```

---

**Exercise 3.**
Write a custom encoder that serializes a `dataclass` by converting it to a dictionary with an extra `"_class"` field containing the class name. For example, a `User(name="Alice", age=30)` should serialize as `{"_class": "User", "name": "Alice", "age": 30}`.

??? success "Solution to Exercise 3"

    ```python
    import json
    from dataclasses import dataclass, asdict

    @dataclass
    class User:
        name: str
        age: int

    class DataclassEncoder(json.JSONEncoder):
        def default(self, obj):
            if hasattr(obj, '__dataclass_fields__'):
                d = asdict(obj)
                d["_class"] = type(obj).__name__
                return d
            return super().default(obj)

    user = User(name="Alice", age=30)
    result = json.dumps(user, cls=DataclassEncoder)
    print(result)
    # {"name": "Alice", "age": 30, "_class": "User"}
    ```
