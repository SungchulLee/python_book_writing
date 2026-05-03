# Formatting and Pretty Printing

Control JSON output formatting with indentation, sorting, and separators.

!!! tip "Mental Model"
    By default `json.dumps` produces compact, single-line output optimized for machines. The `indent`, `sort_keys`, and `separators` parameters let you trade compactness for human readability. Think of formatting as a presentation layer — the data is identical; only the whitespace and key order change.

## Pretty Printing with Indentation

Format JSON for readability with indentation.

```python
import json

data = {
    "name": "Alice",
    "age": 30,
    "hobbies": ["reading", "coding"],
    "address": {"city": "NYC", "zip": "10001"}
}

# Compact (default)
compact = json.dumps(data)
print("Compact:")
print(compact)

# Pretty-printed with indent
pretty = json.dumps(data, indent=2)
print("\nPretty:")
print(pretty)
```

```
Compact:
{"name": "Alice", "age": 30, "hobbies": ["reading", "coding"], "address": {"city": "NYC", "zip": "10001"}}

Pretty:
{
  "name": "Alice",
  "age": 30,
  "hobbies": [
    "reading",
    "coding"
  ],
  "address": {
    "city": "NYC",
    "zip": "10001"
  }
}
```

## Sorting and Separators

Control key order and output formatting.

```python
import json

data = {"zebra": 1, "apple": 2, "monkey": 3}

# Sorted keys
sorted_json = json.dumps(data, sort_keys=True, indent=2)
print("Sorted:")
print(sorted_json)

# Custom separators
compact_sep = json.dumps(data, separators=(',', ':'))
print("\nCompact separators:")
print(compact_sep)
```

```
Sorted:
{
  "apple": 2,
  "monkey": 3,
  "zebra": 1
}

Compact separators:
{"zebra":1,"apple":2,"monkey":3}
```

---

## Exercises

**Exercise 1.**
Write a function `pretty_print_json` that takes a Python object and prints it as formatted JSON with 4-space indentation and sorted keys. Test with a nested dictionary.

??? success "Solution to Exercise 1"

    ```python
    import json

    def pretty_print_json(obj):
        print(json.dumps(obj, indent=4, sort_keys=True))

    # Test
    data = {"users": [{"name": "Alice", "age": 30}], "count": 1}
    pretty_print_json(data)
    # {
    #     "count": 1,
    #     "users": [
    #         {
    #             "age": 30,
    #             "name": "Alice"
    #         }
    #     ]
    # }
    ```

---

**Exercise 2.**
Write a function `minify_json` that takes a JSON string (possibly pretty-printed) and returns the most compact form possible using custom separators `(",", ":")`. For example, a pretty-printed JSON string should be reduced to a single line with no extra whitespace.

??? success "Solution to Exercise 2"

    ```python
    import json

    def minify_json(json_str):
        data = json.loads(json_str)
        return json.dumps(data, separators=(",", ":"))

    # Test
    pretty = '''{
        "name": "Alice",
        "age": 30
    }'''
    print(minify_json(pretty))
    # {"name":"Alice","age":30}
    ```

---

**Exercise 3.**
Write a function `json_size_comparison` that takes a Python dictionary and returns a dictionary with three keys: `"pretty"`, `"default"`, and `"compact"`, each mapping to the byte size of the JSON string in that format. Demonstrate the size difference.

??? success "Solution to Exercise 3"

    ```python
    import json

    def json_size_comparison(data):
        pretty = json.dumps(data, indent=2)
        default = json.dumps(data)
        compact = json.dumps(data, separators=(",", ":"))
        return {
            "pretty": len(pretty.encode()),
            "default": len(default.encode()),
            "compact": len(compact.encode()),
        }

    # Test
    data = {"name": "Alice", "scores": [95, 87, 92], "active": True}
    sizes = json_size_comparison(data)
    for fmt, size in sizes.items():
        print(f"{fmt}: {size} bytes")
    # pretty: ~80 bytes, default: ~55 bytes, compact: ~50 bytes
    ```
