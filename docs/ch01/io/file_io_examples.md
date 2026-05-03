
# File I/O Examples

This section presents three mini-projects that synthesize multiple I/O concepts: `pathlib` for path management, `with` for safe resource handling, error handling for robustness, and `csv`/`json` for structured data.

!!! tip "Mental Model"
    These examples show how individual I/O skills combine into real programs. Each mini-project follows the same pattern: open input, process data, write output, handle errors. Seeing the full pipeline from reading to writing helps you connect isolated concepts into practical workflows.

---

## 1. Config-Driven Text Processing

This mini-project reads a JSON configuration file that specifies an input file, an output file, and a processing mode. It then processes the input text file according to the config and writes a summary report.

### Configuration file

Create a file called `config.json` with the following contents:

```json
{
    "input_file": "source.txt",
    "output_file": "report.txt",
    "mode": "words"
}
```

The `mode` field accepts `"words"` (count words) or `"lines"` (count lines).

### Input file

Create a file called `source.txt` with some sample text:

```text
Python makes file handling straightforward.
The with statement ensures files are closed properly.
Structured formats like JSON and CSV are widely used.
```

### Processing script

```python
import json
from pathlib import Path


def load_config(config_path):
    """Load and validate a JSON configuration file."""
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path) as f:
        config = json.load(f)

    required_keys = {"input_file", "output_file", "mode"}
    missing = required_keys - config.keys()

    if missing:
        raise KeyError(f"Missing config keys: {missing}")

    if config["mode"] not in ("words", "lines"):
        raise ValueError(f"Invalid mode: {config['mode']}")

    return config


def process_file(input_path, mode):
    """Read a text file and return a count based on the mode."""
    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    with open(path) as f:
        text = f.read()

    if mode == "words":
        return len(text.split())
    else:
        return len(text.strip().splitlines())


def write_report(output_path, input_name, mode, count):
    """Write a summary report to the output file."""
    path = Path(output_path)

    with open(path, "w") as f:
        f.write(f"Report for: {input_name}\n")
        f.write(f"Mode: {mode}\n")
        f.write(f"Count: {count}\n")


# Main workflow
config = load_config("config.json")

count = process_file(config["input_file"], config["mode"])
write_report(config["output_file"], config["input_file"], config["mode"], count)

print(f"Report written to {config['output_file']}")
```

Running this script produces a file called `report.txt`:

```text
Report for: source.txt
Mode: words
Count: 18
```

The workflow ties together JSON parsing, text file reading, and file writing. The `load_config` function validates the configuration before processing begins, so errors are caught early.

---

## 2. Safe File Copy with Pathlib

This mini-project copies all `.txt` files from a source folder to a destination folder. It uses `pathlib` throughout, creates the destination directory if needed, and skips files that already exist to avoid accidental overwrites.

```python
from pathlib import Path


def copy_txt_files(source_dir, dest_dir, overwrite=False):
    """Copy all .txt files from source_dir to dest_dir.

    Parameters
    ----------
    source_dir : str or Path
        Directory to search for .txt files.
    dest_dir : str or Path
        Directory to copy files into. Created if it does not exist.
    overwrite : bool
        If False (default), skip files that already exist in dest_dir.

    Returns
    -------
    dict
        Counts of files copied and skipped.
    """
    src = Path(source_dir)
    dst = Path(dest_dir)

    if not src.is_dir():
        raise FileNotFoundError(f"Source directory not found: {src}")

    # Create destination directory (and parents) if needed
    dst.mkdir(parents=True, exist_ok=True)

    copied = 0
    skipped = 0

    for src_file in sorted(src.glob("*.txt")):
        dst_file = dst / src_file.name

        if dst_file.exists() and not overwrite:
            print(f"Skipped (already exists): {dst_file.name}")
            skipped += 1
            continue

        with open(src_file) as f_in:
            content = f_in.read()

        with open(dst_file, "w") as f_out:
            f_out.write(content)

        print(f"Copied: {src_file.name}")
        copied += 1

    return {"copied": copied, "skipped": skipped}


# Main workflow
results = copy_txt_files("source_folder", "backup_folder")

print(f"\nDone. Copied: {results['copied']}, Skipped: {results['skipped']}")
```

Sample output when the source folder contains three files and one already exists in the backup:

```
Copied: notes.txt
Skipped (already exists): readme.txt
Copied: todo.txt

Done. Copied: 2, Skipped: 1
```

Key points:

* `Path.glob("*.txt")` returns only matching files without manual filtering.
* `mkdir(parents=True, exist_ok=True)` safely creates any missing directories.
* Checking `dst_file.exists()` before writing prevents silent data loss.
* Reading and writing with `with` ensures files are always closed properly.

---

## 3. CSV to JSON Summary

This mini-project reads a CSV file containing numeric data, validates and cleans the values, computes summary statistics, and saves the result as a pretty-printed JSON file.

### Input CSV

Create a file called `sales.csv`:

```csv
product,quantity,price
Widget A,10,2.50
Widget B,25,1.75
Widget C,,3.00
Widget D,15,
Widget E,30,4.50
```

Some rows have missing values. The script handles these gracefully.

### Processing script

```python
import csv
import json
from pathlib import Path


def load_csv(csv_path):
    """Load a CSV file and return a list of dictionaries."""
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def parse_numeric(value, field_name):
    """Convert a string to a float, returning None for missing or invalid values."""
    if value is None or value.strip() == "":
        return None

    try:
        return float(value)
    except ValueError:
        print(f"Warning: invalid value '{value}' in field '{field_name}'")
        return None


def compute_summary(rows, field):
    """Compute min, max, and average for a numeric field."""
    values = []

    for row in rows:
        num = parse_numeric(row.get(field, ""), field)

        if num is not None:
            values.append(num)

    if not values:
        return {"field": field, "count": 0, "min": None, "max": None, "average": None}

    return {
        "field": field,
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "average": round(sum(values) / len(values), 2),
    }


def save_summary(summary, output_path):
    """Save a summary dictionary as pretty-printed JSON."""
    path = Path(output_path)

    with open(path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Summary saved to {path}")


# Main workflow
rows = load_csv("sales.csv")

summary = {
    "source_file": "sales.csv",
    "total_rows": len(rows),
    "statistics": [
        compute_summary(rows, "quantity"),
        compute_summary(rows, "price"),
    ],
}

save_summary(summary, "sales_summary.json")
```

Running this script produces `sales_summary.json`:

```json
{
  "source_file": "sales.csv",
  "total_rows": 5,
  "statistics": [
    {
      "field": "quantity",
      "count": 4,
      "min": 10.0,
      "max": 30.0,
      "average": 20.0
    },
    {
      "field": "price",
      "count": 4,
      "min": 1.75,
      "max": 4.5,
      "average": 2.94
    }
  ]
}
```

The script skips rows with missing values rather than crashing. The `count` field in each summary block shows how many valid values were used, making it clear when data was excluded.

---

## Summary

These mini-projects demonstrate how multiple I/O concepts work together in realistic workflows:

* `pathlib` for portable path construction, directory creation, and file discovery
* `with` statements for safe, exception-proof file handling
* `json` for reading configuration and writing structured output
* `csv.DictReader` for parsing tabular data into dictionaries
* Validation and error handling to catch problems before they propagate

Each project combines several of these techniques, reflecting the way file I/O is used in practice: rarely in isolation, usually as part of a larger data pipeline.

## Exercises

**Exercise 1.**
Write a program that creates a file called `names.txt` containing five names (one per line), then reads the file back and prints each name in uppercase.

??? success "Solution to Exercise 1"
    ```python
    # Write names
    with open("names.txt", "w") as f:
        for name in ["Alice", "Bob", "Carol", "Dave", "Eve"]:
            f.write(name + "\n")

    # Read and print in uppercase
    with open("names.txt") as f:
        for line in f:
            print(line.strip().upper())
    ```

    Output:

    ```
    ALICE
    BOB
    CAROL
    DAVE
    EVE
    ```

    `strip()` removes the trailing newline from each line before calling `upper()`.

---

**Exercise 2.**
Predict the output of the following program. What does the `get` method do when the key is not found?

```python
counts = {}
words = ["the", "cat", "sat", "on", "the", "mat", "the"]

for word in words:
    counts[word] = counts.get(word, 0) + 1

print(counts)
```

??? success "Solution to Exercise 2"
    Output:

    ```
    {'the': 3, 'cat': 1, 'sat': 1, 'on': 1, 'mat': 1}
    ```

    `counts.get(word, 0)` returns the current count for `word` if it exists, or `0` if the key is not yet in the dictionary. Adding 1 and assigning back increments the count. This is a standard word-counting pattern.

---

**Exercise 3.**
Write a program that reads a CSV string (not a file) and converts it into a list of dictionaries. Use the first row as headers.

```python
csv_text = """name,age,city
Alice,30,Paris
Bob,25,London
Carol,35,Tokyo"""
```

??? success "Solution to Exercise 3"
    ```python
    csv_text = """name,age,city
    Alice,30,Paris
    Bob,25,London
    Carol,35,Tokyo"""

    lines = csv_text.strip().split("\n")
    headers = lines[0].split(",")
    records = []

    for line in lines[1:]:
        values = line.strip().split(",")
        record = {}
        for h, v in zip(headers, values):
            record[h] = v
        records.append(record)

    print(records)
    ```

    Output:

    ```
    [{'name': 'Alice', 'age': '30', 'city': 'Paris'},
     {'name': 'Bob', 'age': '25', 'city': 'London'},
     {'name': 'Carol', 'age': '35', 'city': 'Tokyo'}]
    ```

    The first line provides the keys. Each subsequent line is split and zipped with the headers to form a dictionary.

---

**Exercise 4.**
Explain why the `with` statement is preferred over manually calling `f.close()`. Describe a scenario where forgetting to close a file could cause problems.

??? success "Solution to Exercise 4"
    The `with` statement is preferred because it guarantees the file is closed when the block exits, even if an exception occurs. For example:

    ```python
    with open("data.txt") as f:
        data = f.read()
        # If an error occurs here, the file is still closed
    ```

    Without `with`, you must call `f.close()` manually:

    ```python
    f = open("data.txt")
    data = f.read()
    f.close()  # Forgotten if an exception occurs above
    ```

    A scenario where this causes problems: if a program writes to a file without closing it, the data may remain in a memory buffer and never be flushed to disk. If the program crashes before `close()` is called, the file may be empty or incomplete. On some operating systems, an unclosed file also holds a lock that prevents other programs from accessing it.

---

**Exercise 5.**
Write a program that uses the `json` module to save a dictionary to a file and then load it back. Verify that the loaded data is equal to the original.

```python
import json

original = {"name": "Alice", "scores": [90, 85, 92], "active": True}
```

??? success "Solution to Exercise 5"
    ```python
    import json

    original = {"name": "Alice", "scores": [90, 85, 92], "active": True}

    # Save to file
    with open("data.json", "w") as f:
        json.dump(original, f)

    # Load from file
    with open("data.json") as f:
        loaded = json.load(f)

    print(loaded)
    print(original == loaded)
    ```

    Output:

    ```
    {'name': 'Alice', 'scores': [90, 85, 92], 'active': True}
    True
    ```

    `json.dump` serializes the dictionary to JSON format and writes it to the file. `json.load` reads the file and deserializes the JSON back into a Python dictionary. The `==` comparison confirms the round-trip preserves the data.
