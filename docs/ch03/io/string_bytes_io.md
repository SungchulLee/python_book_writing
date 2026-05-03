# io.StringIO and io.BytesIO

StringIO and BytesIO create in-memory file-like objects for text and binary data respectively. They are useful for testing, temporary buffers, and situations where file system I/O should be avoided.

!!! tip "Mental Model"
    `StringIO` and `BytesIO` are fake files that live in memory. They support the same `.read()`, `.write()`, and `.seek()` interface as real files, so any code that expects a file-like object works with them unchanged. This makes them perfect for testing I/O code without touching the filesystem.

---

## StringIO for Text

### In-Memory Text Buffer

```python
from io import StringIO

buffer = StringIO()
buffer.write("Hello ")
buffer.write("World!")

contents = buffer.getvalue()
print(contents)
```

Output:
```
Hello World!
```

### Reading from StringIO

```python
from io import StringIO

buffer = StringIO("line1\nline2\nline3")

for line in buffer:
    print(line.strip())
```

Output:
```
line1
line2
line3
```

## BytesIO for Binary

### In-Memory Binary Buffer

```python
from io import BytesIO

buffer = BytesIO()
buffer.write(b"Hello ")
buffer.write(b"World!")

contents = buffer.getvalue()
print(contents)
```

Output:
```
b'Hello World!'
```

### Binary Data Processing

```python
from io import BytesIO

image_data = BytesIO()
image_data.write(b'\x89PNG\r\n\x1a\n')
image_data.write(b'mock_image_data')

image_data.seek(0)
header = image_data.read(8)
print(f"PNG Header: {header}")
```

Output:
```
PNG Header: b'\x89PNG\r\n\x1a\n'
```

## Testing and Mocking

### Testing File Operations

```python
from io import StringIO
import sys

buffer = StringIO()
sys.stdout = buffer
print("Captured output")
sys.stdout = sys.__stdout__

result = buffer.getvalue()
print(f"Result: {result}")
```

Output:
```
Result: Captured output
```

### CSV Processing

```python
from io import StringIO
import csv

csv_data = StringIO()
writer = csv.writer(csv_data)
writer.writerow(['name', 'age'])
writer.writerow(['Alice', 30])
writer.writerow(['Bob', 25])

csv_data.seek(0)
reader = csv.reader(csv_data)
for row in reader:
    print(row)
```

Output:
```
['name', 'age']
['Alice', '30']
['Bob', '25']
```

---

## Exercises


**Exercise 1.**
Use `io.StringIO` to capture the output of multiple `print()` calls into a single string. Print the combined result.

??? success "Solution to Exercise 1"

        ```python
        import io

        buffer = io.StringIO()
        print("Hello", file=buffer)
        print("World", file=buffer)
        print("Python", file=buffer)

        result = buffer.getvalue()
        print(result)
        # Hello
        # World
        # Python
        ```

    `io.StringIO` acts as an in-memory text file. `print()` with `file=buffer` writes to it instead of stdout.

---

**Exercise 2.**
Write a function that takes a CSV string (e.g., `"name,age\nAlice,30\nBob,25"`) and uses `io.StringIO` with the `csv` module to parse it into a list of dictionaries.

??? success "Solution to Exercise 2"

        ```python
        import io
        import csv

        def parse_csv(csv_string):
            reader = csv.DictReader(io.StringIO(csv_string))
            return list(reader)

        data = "name,age\nAlice,30\nBob,25"
        records = parse_csv(data)
        print(records)
        # [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
        ```

    `io.StringIO` wraps the string as a file-like object that `csv.DictReader` can consume.

---

**Exercise 3.**
Demonstrate the difference between `io.StringIO` (works with `str`) and `io.BytesIO` (works with `bytes`). Show that writing bytes to `StringIO` raises an error and vice versa.

??? success "Solution to Exercise 3"

        ```python
        import io

        # StringIO works with str
        s = io.StringIO()
        s.write("hello")
        try:
            s.write(b"bytes")
        except TypeError as e:
            print(f"StringIO error: {e}")

        # BytesIO works with bytes
        b = io.BytesIO()
        b.write(b"hello")
        try:
            b.write("text")
        except TypeError as e:
            print(f"BytesIO error: {e}")
        ```

    `StringIO` accepts only `str`, and `BytesIO` accepts only `bytes`. Mixing them raises `TypeError`.
