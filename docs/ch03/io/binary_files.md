# Binary Files

Binary files store raw bytes rather than human-readable text. Working with binary mode is essential for images, audio, executables, and custom data formats.

!!! tip "Mental Model"
    Text mode (`'r'`/`'w'`) gives you strings with automatic encoding/decoding and newline translation. Binary mode (`'rb'`/`'wb'`) gives you raw `bytes` with no translation at all. If the file is not meant for humans to read (images, audio, serialized data), always use binary mode to avoid corruption from encoding conversions.

## Opening Binary Files

Use `'b'` mode flag to read and write files as raw bytes.

### 1. Mode Flags

Combine `'b'` with read, write, or append modes.

```python
# Read binary
with open("image.png", "rb") as f:
    data = f.read()

# Write binary
with open("output.bin", "wb") as f:
    f.write(data)

# Append binary
with open("log.bin", "ab") as f:
    f.write(b"\x00\x01\x02")

# Read and write binary
with open("data.bin", "r+b") as f:
    content = f.read()
    f.seek(0)
    f.write(modified)
```

### 2. Bytes vs Strings

Binary mode works with `bytes`, not `str`.

```python
# Text mode returns str
with open("text.txt", "r") as f:
    data = f.read()
    print(type(data))  # <class 'str'>

# Binary mode returns bytes
with open("text.txt", "rb") as f:
    data = f.read()
    print(type(data))  # <class 'bytes'>
```

### 3. No Encoding

Binary mode bypasses text encoding entirely.

```python
# Text mode uses encoding
with open("file.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Binary mode: raw bytes, no encoding
with open("file.txt", "rb") as f:
    raw = f.read()
    text = raw.decode("utf-8")  # Manual decode
```

## Reading Binary Data

Methods for reading raw bytes from files.

### 1. Read Entire File

Load complete file contents into memory.

```python
with open("photo.jpg", "rb") as f:
    image_data = f.read()

print(len(image_data))        # File size in bytes
print(image_data[:10])        # First 10 bytes
```

### 2. Read Fixed Chunks

Read specific number of bytes at a time.

```python
with open("large_file.bin", "rb") as f:
    # Read first 1024 bytes
    header = f.read(1024)
    
    # Read next chunk
    chunk = f.read(4096)
    
    # Empty bytes means EOF
    while chunk := f.read(4096):
        process(chunk)
```

### 3. Read Into Buffer

Use `readinto()` for memory-efficient reading.

```python
buffer = bytearray(4096)

with open("data.bin", "rb") as f:
    # Read into existing buffer
    bytes_read = f.readinto(buffer)
    print(f"Read {bytes_read} bytes")
    
    # Process buffer[:bytes_read]
```

## Writing Binary Data

Methods for writing raw bytes to files.

### 1. Write Bytes

Write bytes objects directly to file.

```python
data = b"\x89PNG\r\n\x1a\n"  # PNG header

with open("header.bin", "wb") as f:
    f.write(data)

# Write bytearray
buffer = bytearray([0, 1, 2, 3, 4])
with open("buffer.bin", "wb") as f:
    f.write(buffer)
```

### 2. Write Multiple Chunks

Write data in segments for large files.

```python
chunks = [b"chunk1", b"chunk2", b"chunk3"]

with open("output.bin", "wb") as f:
    for chunk in chunks:
        f.write(chunk)

# Using writelines (no separator added)
with open("output.bin", "wb") as f:
    f.writelines(chunks)
```

### 3. Buffered Writing

Control write buffering behavior.

```python
# Unbuffered (immediate writes)
with open("log.bin", "wb", buffering=0) as f:
    f.write(b"immediate")

# Line buffered (not for binary)
# buffering=1 only works for text mode

# Custom buffer size
with open("data.bin", "wb", buffering=8192) as f:
    f.write(b"buffered")
```

## File Position

Navigate within binary files using seek and tell.

### 1. Current Position

Use `tell()` to get current byte position.

```python
with open("data.bin", "rb") as f:
    print(f.tell())      # 0 (start)
    
    f.read(10)
    print(f.tell())      # 10
    
    f.read(5)
    print(f.tell())      # 15
```

### 2. Seek Absolute

Move to specific byte position with `seek()`.

```python
with open("data.bin", "rb") as f:
    f.seek(100)          # Go to byte 100
    chunk = f.read(50)   # Read bytes 100-149
    
    f.seek(0)            # Back to start
    header = f.read(10)
```

### 3. Seek Relative

Use whence parameter for relative seeking.

```python
import os

with open("data.bin", "rb") as f:
    # From start (default, whence=0)
    f.seek(10, os.SEEK_SET)
    
    # From current position (whence=1)
    f.seek(5, os.SEEK_CUR)   # Now at 15
    
    # From end (whence=2)
    f.seek(-10, os.SEEK_END)  # 10 bytes before end
```

## Struct Module

Pack and unpack binary data with defined formats.

### 1. Basic Packing

Convert Python values to bytes.

```python
import struct

# Pack integer and float
data = struct.pack("if", 42, 3.14)
print(data)        # b'*\x00\x00\x00\xc3\xf5H@'
print(len(data))   # 8 bytes

# Format characters: i=int, f=float, d=double
# h=short, b=byte, s=string
```

### 2. Basic Unpacking

Convert bytes back to Python values.

```python
import struct

data = b'*\x00\x00\x00\xc3\xf5H@'

# Unpack to tuple
values = struct.unpack("if", data)
print(values)      # (42, 3.140000104904175)

# Unpack single value
num = struct.unpack("i", data[:4])[0]
print(num)         # 42
```

### 3. Byte Order

Specify endianness in format string.

```python
import struct

num = 0x12345678

# Native byte order (system-dependent)
native = struct.pack("I", num)

# Little-endian
little = struct.pack("<I", num)
print(little.hex())   # 78563412

# Big-endian (network order)
big = struct.pack(">I", num)
print(big.hex())      # 12345678
```

## Common Patterns

Practical binary file operations.

### 1. File Header Reading

Parse structured file headers.

```python
import struct

def read_bmp_header(filename):
    """Read BMP image header."""
    with open(filename, "rb") as f:
        # BMP signature
        sig = f.read(2)
        if sig != b"BM":
            raise ValueError("Not a BMP file")
        
        # File size, reserved, data offset
        size, _, _, offset = struct.unpack("<IHHI", f.read(12))
        
        return {"size": size, "offset": offset}

# header = read_bmp_header("image.bmp")
```

### 2. Copy Binary File

Efficiently copy large binary files.

```python
def copy_binary(src, dst, chunk_size=8192):
    """Copy binary file in chunks."""
    with open(src, "rb") as fin:
        with open(dst, "wb") as fout:
            while chunk := fin.read(chunk_size):
                fout.write(chunk)

copy_binary("source.bin", "dest.bin")
```

### 3. Modify In Place

Update specific bytes within a file.

```python
def patch_byte(filename, offset, value):
    """Change single byte at offset."""
    with open(filename, "r+b") as f:
        f.seek(offset)
        f.write(bytes([value]))

# patch_byte("data.bin", 100, 0xFF)
```

---

## Exercises


**Exercise 1.**
Write a script that creates a binary file containing the bytes `b'\x00\x01\x02\x03'`, then reads it back and prints each byte as a hexadecimal value.

??? success "Solution to Exercise 1"

        ```python
        # Write binary file
        with open("/tmp/test.bin", "wb") as f:
            f.write(b'\x00\x01\x02\x03')

        # Read and print hex values
        with open("/tmp/test.bin", "rb") as f:
            data = f.read()
            for byte in data:
                print(f"0x{byte:02x}", end=" ")
        # 0x00 0x01 0x02 0x03
        ```

    Binary mode (`"rb"`, `"wb"`) reads/writes raw bytes without text encoding.

---

**Exercise 2.**
Write a function `copy_file(src, dst)` that copies a binary file from `src` to `dst` by reading and writing in 4096-byte chunks. Use `"rb"` and `"wb"` modes.

??? success "Solution to Exercise 2"

        ```python
        def copy_file(src, dst, chunk_size=4096):
            with open(src, "rb") as fin, open(dst, "wb") as fout:
                while True:
                    chunk = fin.read(chunk_size)
                    if not chunk:
                        break
                    fout.write(chunk)
        ```

    Reading in chunks avoids loading the entire file into memory, making this suitable for large files.

---

**Exercise 3.**
Use the `struct` module to write two integers (42 and 100) to a binary file in little-endian format, then read them back and print them.

??? success "Solution to Exercise 3"

        ```python
        import struct

        # Write
        with open("/tmp/ints.bin", "wb") as f:
            f.write(struct.pack("<ii", 42, 100))

        # Read
        with open("/tmp/ints.bin", "rb") as f:
            data = f.read()
            a, b = struct.unpack("<ii", data)
            print(a, b)  # 42 100
        ```

    `"<ii"` means little-endian (`<`) with two signed integers (`i`). `struct.pack` converts to bytes and `struct.unpack` converts back.
