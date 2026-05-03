# json.dump and json.load (File I/O)

`dump()` writes JSON to a file, while `load()` reads JSON from a file.

!!! tip "Mental Model"
    `dump` and `load` are the file-based siblings of `dumps` and `loads`. The "s" stands for "string" — without it, the functions read from and write to file-like objects directly. Use `dump`/`load` when you want to persist JSON to disk or read it back, and `dumps`/`loads` when you are working with strings in memory.

## dump - Write JSON to File

Write JSON data directly to a file.

```python
import json
import tempfile
import os

data = {
    "users": [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]
}

# Write to file
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump(data, f)
    temp_path = f.name

# Verify
with open(temp_path) as f:
    print(f.read())

os.unlink(temp_path)
```

```
{"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}
```

## load - Read JSON from File

Read JSON data directly from a file.

```python
import json
import tempfile
import os

# Create temporary JSON file
data = {"config": {"host": "localhost", "port": 8080}}
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump(data, f)
    temp_path = f.name

# Load from file
with open(temp_path) as f:
    loaded = json.load(f)
    print(loaded)
    print(f"Host: {loaded['config']['host']}")

os.unlink(temp_path)
```

```
{'config': {'host': 'localhost', 'port': 8080}}
Host: localhost
```

---

## Exercises

**Exercise 1.**
Write a function `save_and_load` that takes a Python dictionary, writes it to a temporary JSON file with pretty formatting (indent=2), reads it back, and returns the loaded dictionary. Verify the round-trip produces an equal dictionary.

??? success "Solution to Exercise 1"

    ```python
    import json
    import tempfile
    import os

    def save_and_load(data):
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False
        ) as f:
            json.dump(data, f, indent=2)
            path = f.name

        with open(path) as f:
            loaded = json.load(f)

        os.unlink(path)
        return loaded

    # Test
    original = {"name": "Alice", "scores": [95, 87, 92]}
    result = save_and_load(original)
    print(result)                    # {'name': 'Alice', 'scores': [95, 87, 92]}
    print(result == original)        # True
    ```

---

**Exercise 2.**
Write a function `merge_json_files` that takes a list of JSON file paths, loads each one, and merges them into a single dictionary (later files override earlier ones for duplicate keys). Return the merged dictionary.

??? success "Solution to Exercise 2"

    ```python
    import json

    def merge_json_files(file_paths):
        merged = {}
        for path in file_paths:
            with open(path) as f:
                data = json.load(f)
                merged.update(data)
        return merged

    # Usage example (with actual files):
    # merged = merge_json_files(["config1.json", "config2.json"])
    # print(merged)
    ```

---

**Exercise 3.**
Write a function `update_json_field` that takes a file path, a key, and a new value. It should load the JSON file, update the specified key, and write the file back. If the file does not exist, create it with just that key-value pair.

??? success "Solution to Exercise 3"

    ```python
    import json
    import os

    def update_json_field(file_path, key, value):
        if os.path.exists(file_path):
            with open(file_path) as f:
                data = json.load(f)
        else:
            data = {}

        data[key] = value

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

    # Usage example:
    # update_json_field("settings.json", "theme", "dark")
    ```
