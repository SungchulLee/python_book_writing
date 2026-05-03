# Encoding Issues

Text encoding mismatches are a common source of errors. Understanding character encodings and Python text handling prevents encoding-related bugs.

!!! tip "Mental Model"
    Encoding errors happen when the decoder guesses wrong about which encoding was used to write the bytes. The fix is always the same: know your encoding, specify it explicitly (`open(f, encoding='utf-8')`), and never rely on the platform default. When in doubt, UTF-8 is the right choice for nearly all modern text.

---

## UTF-8 Basics

### Default Encoding

```python
import sys

print(f"Default: {sys.getdefaultencoding()}")

text = "Hello 世界 🌍"
print(f"Text: {text}")
print(f"Bytes (UTF-8): {text.encode('utf-8')}")
```

Output:
```
Default: utf-8
Text: Hello 世界 🌍
Bytes (UTF-8): b'Hello \xe4\xb8\x96\xe7\x95\x8c \xf0\x9f\x8c\x8d'
```

## Encoding/Decoding

### Encoding Text to Bytes

```python
text = "café"

utf8 = text.encode('utf-8')
latin1 = text.encode('latin-1')
ascii_err = text.encode('ascii', errors='replace')

print(f"UTF-8: {utf8}")
print(f"Latin-1: {latin1}")
print(f"ASCII (replace): {ascii_err}")
```

Output:
```
UTF-8: b'caf\xc3\xa9'
Latin-1: b'caf\xe9'
ASCII (replace): b'caf?'
```

### Decoding Bytes to Text

```python
utf8_bytes = b'caf\xc3\xa9'
latin1_bytes = b'caf\xe9'

print(f"UTF-8: {utf8_bytes.decode('utf-8')}")
print(f"UTF-8 as Latin-1: {utf8_bytes.decode('latin-1')}")
```

Output:
```
UTF-8: café
UTF-8 as Latin-1: cafÃ©
```

## File Encoding

### Specifying File Encoding

```python
import io
import tempfile
import os

with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
    f.write("Hello 世界")
    temp_file = f.name

with open(temp_file, 'r', encoding='utf-8') as f:
    content = f.read()
    print(f"Read: {content}")

os.unlink(temp_file)
```

Output:
```
Read: Hello 世界
```

## Error Handling

### Encoding Error Strategies

```python
text = "café"

replace = text.encode('ascii', errors='replace')
ignore = text.encode('ascii', errors='ignore')

print(f"Replace: {replace}")
print(f"Ignore: {ignore}")
```

Output:
```
Replace: b'caf?'
Ignore: b'caf'
```

---

## Exercises


**Exercise 1.**
Write a script that writes the string `"Hello, world!"` to a file using UTF-8 encoding, then tries to read it back using ASCII encoding. What happens? Handle the error gracefully.

??? success "Solution to Exercise 1"

        ```python
        with open("/tmp/test.txt", "w", encoding="utf-8") as f:
            f.write("Hello, \u4e16\u754c!")  # Hello, 世界!

        try:
            with open("/tmp/test.txt", "r", encoding="ascii") as f:
                content = f.read()
        except UnicodeDecodeError as e:
            print(f"Error: {e}")

        # Read correctly with UTF-8
        with open("/tmp/test.txt", "r", encoding="utf-8") as f:
            print(f.read())  # Hello, 世界!
        ```

    ASCII cannot decode multi-byte UTF-8 characters, raising `UnicodeDecodeError`.

---

**Exercise 2.**
Write a function `detect_encoding(filepath)` that reads the first 100 bytes of a file and returns `"utf-8"` if they decode successfully as UTF-8, or `"unknown"` otherwise.

??? success "Solution to Exercise 2"

        ```python
        def detect_encoding(filepath):
            with open(filepath, "rb") as f:
                raw = f.read(100)
            try:
                raw.decode("utf-8")
                return "utf-8"
            except UnicodeDecodeError:
                return "unknown"
        ```

    This is a simple heuristic. For production use, consider the `chardet` library for more reliable detection.

---

**Exercise 3.**
Demonstrate the difference between `errors="ignore"`, `errors="replace"`, and `errors="strict"` when decoding bytes that contain invalid UTF-8 sequences.

??? success "Solution to Exercise 3"

        ```python
        data = b"Hello \xff\xfe World"

        print(data.decode("utf-8", errors="ignore"))   # Hello  World
        print(data.decode("utf-8", errors="replace"))  # Hello �� World
        try:
            data.decode("utf-8", errors="strict")
        except UnicodeDecodeError as e:
            print(f"strict: {e}")
        ```

    `"ignore"` silently skips invalid bytes. `"replace"` inserts replacement characters. `"strict"` (the default) raises an exception.
