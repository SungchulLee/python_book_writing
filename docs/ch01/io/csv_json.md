
# CSV and JSON Basics

Many programs exchange data using common text formats such as **CSV** and **JSON**.

These formats allow data to be stored and shared between systems.

```mermaid
flowchart LR
    A[Program] --> B[CSV]
    A --> C[JSON]
    B --> D[Spreadsheet tools]
    C --> E[Web APIs]
````

!!! note "Encoding"
    CSV and JSON are text formats. When working with non-ASCII data (accented
    characters, CJK text, etc.), open files with an explicit encoding:
    `open("data.csv", encoding="utf-8")`. UTF-8 is the most common choice and
    the default on most modern systems, but older files may use `latin-1` or
    `cp1252`.

!!! tip "Mental Model"
    CSV is a flat table stored as text---rows are lines, columns are separated by commas. JSON is a nested structure stored as text---it maps directly to Python dicts and lists. Use CSV when your data is tabular and JSON when your data is hierarchical. Python's `csv` and `json` modules handle the parsing so you work with native Python objects.

---

## 1. CSV Files

CSV stands for **Comma-Separated Values**.

Example file:

```text
name,age
Alice,25
Bob,30
```

---

## 2. Reading CSV

Python provides the `csv` module. The simplest reader is `csv.reader`, which
returns each row as a list of strings.

```python
import csv

with open("data.csv") as f:
    reader = csv.reader(f)

    for row in reader:
        print(row)
```

### Reading with `csv.DictReader`

`csv.DictReader` uses the first row as dictionary keys, making field access
more readable than numeric indices.

```python
import csv

with open("data.csv") as f:
    reader = csv.DictReader(f)

    for row in reader:
        print(row["name"], int(row["age"]))
```

Each row is a dictionary such as `{"name": "Alice", "age": "25"}`. Values are
still strings, so numeric fields must be converted explicitly.

---

## 3. Writing CSV

When opening a CSV file for writing, always pass `newline=""` to prevent the
`csv` module from producing extra blank lines on Windows. This is a
cross-platform best practice.

```python
import csv

with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow(["name", "age"])
    writer.writerow(["Alice", 25])
```

### Writing with `csv.DictWriter`

`csv.DictWriter` mirrors `csv.DictReader`. You specify the field names once,
then write rows as dictionaries.

```python
import csv

fields = ["name", "age"]

with open("out.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)

    writer.writeheader()
    writer.writerow({"name": "Alice", "age": 25})
    writer.writerow({"name": "Bob", "age": 30})
```

---

## 4. CSV End-to-End Example

A realistic workflow: read a CSV file, filter rows, and write the results to a
new file.

```python
import csv

# Read student scores and keep only those who passed (score >= 60).

with open("scores.csv") as fin:
    reader = csv.DictReader(fin)
    rows = [row for row in reader if int(row["score"]) >= 60]

with open("passed.csv", "w", newline="") as fout:
    writer = csv.DictWriter(fout, fieldnames=["name", "score"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} passing students to passed.csv")
```

Given an input file `scores.csv`:

```text
name,score
Alice,92
Bob,55
Carol,78
Dave,43
```

the program writes `passed.csv` containing only Alice and Carol.

---

## 5. JSON Files

JSON (JavaScript Object Notation) is widely used for structured data.

Example JSON:

```json
{
  "name": "Alice",
  "age": 25
}
```

---

## 6. Reading JSON

The `json` module provides two pairs of functions:

| Function | Input | Output |
|---|---|---|
| `json.load(f)` | **file object** | Python object |
| `json.loads(s)` | **string** | Python object |
| `json.dump(obj, f)` | Python object | writes to **file** |
| `json.dumps(obj)` | Python object | returns **string** |

The trailing **s** stands for *string*. Use the file-based versions
(`load`/`dump`) when working with files, and the string-based versions
(`loads`/`dumps`) when working with in-memory data or network responses.

### Reading from a file

```python
import json

with open("data.json") as f:
    data = json.load(f)

print(data)
```

### Parsing a string

```python
import json

text = '{"name": "Alice", "age": 25}'
data = json.loads(text)
print(data["name"])
```

---

## 7. Writing JSON

Use `indent` to produce human-readable output. Without it, `json.dump` writes
everything on one line.

```python
import json

data = {"name": "Alice", "age": 25}

with open("data.json", "w") as f:
    json.dump(data, f, indent=2)
```

The resulting file:

```json
{
  "name": "Alice",
  "age": 25
}
```

To get a JSON string instead of writing to a file, use `json.dumps`:

```python
text = json.dumps(data, indent=2)
print(text)
```

---

## 8. JSON End-to-End Example

A common pattern is loading a JSON configuration file, updating a value, and
saving it back.

```python
import json

# Load application configuration.
with open("config.json") as f:
    config = json.load(f)

# Update a setting.
config["debug"] = False
config["max_retries"] = 5

# Write the updated configuration back.
with open("config.json", "w") as f:
    json.dump(config, f, indent=2)

print("Configuration updated.")
```

Given an initial `config.json`:

```json
{
  "debug": true,
  "max_retries": 3,
  "database": "production.db"
}
```

the program sets `debug` to `false`, changes `max_retries` to `5`, and
preserves the remaining keys.

---

## 9. Summary

Key ideas:

* CSV represents tabular data
* JSON represents structured data
* Python provides `csv` and `json` modules
* `csv.DictReader` and `csv.DictWriter` use named fields for clarity
* `json.load`/`json.dump` work with files; `json.loads`/`json.dumps` work with strings
* Pass `newline=""` when opening CSV files for writing
* Use `indent=2` for human-readable JSON output
* Always consider encoding when working with non-ASCII text data


## Exercises

**Exercise 1.**
`csv.reader` returns lists of strings, not typed values. Predict the output:

```python
import csv
import io

data = "name,age\nAlice,25\nBob,30"
reader = csv.reader(io.StringIO(data))
header = next(reader)
first_row = next(reader)
print(first_row)
print(type(first_row[1]))
print(first_row[1] + 5)
```

Why does the last line fail? What must you do to work with numeric CSV data? How does `csv.DictReader` improve upon `csv.reader`?

??? success "Solution to Exercise 1"
    Output:

    ```text
    ['Alice', '25']
    <class 'str'>
    ```

    Then `first_row[1] + 5` raises `TypeError: can only concatenate str (not "int") to str` because `first_row[1]` is the string `"25"`, not the integer `25`.

    CSV files are plain text -- the `csv` module reads all values as strings. To work with numeric data, you must convert explicitly: `int(first_row[1])` or `float(first_row[1])`.

    `csv.DictReader` improves upon `csv.reader` by using the header row as keys:

    ```python
    reader = csv.DictReader(io.StringIO(data))
    for row in reader:
        print(row["name"], int(row["age"]))
    ```

    Each row becomes a dictionary (`{"name": "Alice", "age": "25"}`), making field access clearer than numeric indices.

---

**Exercise 2.**
`json.loads()` converts JSON strings to Python objects. Predict the Python types:

```python
import json

data = json.loads('{"name": "Alice", "age": 25, "scores": [90, 85], "active": true, "address": null}')
print(type(data))
print(type(data["age"]))
print(type(data["scores"]))
print(type(data["active"]))
print(type(data["address"]))
```

How does JSON map to Python types? What JSON types have no direct Python equivalent, and vice versa?

??? success "Solution to Exercise 2"
    Output:

    ```text
    <class 'dict'>
    <class 'int'>
    <class 'list'>
    <class 'bool'>
    <class 'NoneType'>
    ```

    JSON to Python type mapping:

    | JSON | Python |
    |------|--------|
    | object `{}` | `dict` |
    | array `[]` | `list` |
    | string | `str` |
    | number (integer) | `int` |
    | number (decimal) | `float` |
    | `true`/`false` | `True`/`False` |
    | `null` | `None` |

    JSON types with no Python equivalent: none (all JSON types map to Python). Python types with no JSON equivalent: `tuple` (serialized as array), `set` (not serializable), `bytes`, `datetime`, `complex`, and custom objects. This asymmetry means you must handle these types specially when serializing.

---

**Exercise 3.**
A programmer tries to serialize a Python object to JSON:

```python
import json
from datetime import datetime

data = {"timestamp": datetime.now(), "values": {1, 2, 3}}
json.dumps(data)
```

This raises `TypeError`. Which values in the dictionary are not JSON-serializable? Why does JSON only support certain types? Show how to handle this by providing a custom serialization approach.

??? success "Solution to Exercise 3"
    Two values are not JSON-serializable: `datetime.now()` (a `datetime` object) and `{1, 2, 3}` (a `set`). JSON only supports strings, numbers, booleans, null, arrays, and objects.

    JSON supports only these types because it is a **data interchange format** designed for simplicity and cross-language compatibility. Every programming language can represent these basic types.

    Custom serialization approach:

    ```python
    import json
    from datetime import datetime

    def custom_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    data = {"timestamp": datetime.now(), "values": {1, 2, 3}}
    result = json.dumps(data, default=custom_serializer)
    print(result)
    ```

    The `default` parameter provides a function that converts non-serializable objects to serializable ones. This is the standard pattern for extending JSON serialization in Python.
