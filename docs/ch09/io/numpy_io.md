# Array I/O: save, load, savez

NumPy provides efficient binary formats for saving and loading arrays. These are faster and more compact than text formats like CSV.

!!! tip "Mental Model"
    `np.save` writes a single array to a `.npy` file — a binary dump that preserves dtype, shape, and byte order exactly. `np.savez` bundles multiple arrays into one `.npz` archive (literally a zip of `.npy` files). These formats are faster than CSV because there is no parsing: the bytes on disk are the same bytes in memory.

    At its core, **I/O is serialization**: converting an in-memory array (data +
    dtype + shape) into a byte sequence on disk, and deserializing it back. The
    `.npy` format serializes the exact memory layout, which is why it preserves
    every property and loads instantly.

!!! note "Array Persistence System — Choosing a Format"
    | Format | Speed | Size | Preserves dtype | Interoperable | Use when |
    |--------|-------|------|----------------|---------------|----------|
    | `.npy` | Fastest | Compact | Yes | NumPy only | Single array, speed matters |
    | `.npz` | Fast | Compact | Yes | NumPy only | Multiple named arrays |
    | `.npz` (compressed) | Moderate | Smallest | Yes | NumPy only | Storage-constrained |
    | CSV / text | Slow | Large | No (parsed) | Universal | Sharing with non-Python tools |
    | `memmap` | Instant (lazy) | On disk | Yes | NumPy only | Data larger than RAM |

!!! tip "The Data Lifecycle"
    ```text
    1. COMPUTE → arrays live in memory
    2. SAVE    → np.save / np.savez writes to disk
    3. LOAD    → np.load restores without recomputation
    4. SCALE   → np.memmap for data larger than RAM
    ```
    Every function on this page serves one of these four stages. Choosing the right format is a decision about speed, size, interoperability, and memory constraints.

```python
import numpy as np
```

---

## Why Use NumPy's Binary Format?

!!! note "Why Binary Is Faster"
    ```text
    CSV:  bytes on disk → decode text → parse delimiters → convert strings to floats → allocate array
    NPY:  bytes on disk → copy directly into array (same memory layout)
    ```
    CSV requires CPU-intensive string parsing and type conversion. The `.npy` format stores the raw memory representation, so loading is essentially a single `memcpy` — orders of magnitude faster.

| Format | Speed | Size | Preserves dtype | Multiple arrays |
|--------|-------|------|-----------------|-----------------|
| `.npy` | Fast | Compact | Yes | No |
| `.npz` | Fast | Compact | Yes | Yes |
| CSV | Slow | Large | No | No |
| Pickle | Medium | Medium | Yes | Yes |

```python
# Comparison: 1 million floats
arr = np.random.randn(1_000_000)

# Binary: ~8 MB, loads in milliseconds
np.save('data.npy', arr)

# CSV: ~25 MB, loads in seconds
np.savetxt('data.csv', arr)
```

---

!!! tip "Format Decision Guide"
    | Need | Use |
    |---|---|
    | Save a single array for later reuse | `np.save` (`.npy`) |
    | Save multiple related arrays together | `np.savez` (`.npz`) |
    | Disk space is limited | `np.savez_compressed` |
    | Share with Excel, R, or other tools | `np.savetxt` (CSV) |
    | Array is too large for RAM | `np.memmap` |

---

## np.save() — Save Single Array

Save one array to a `.npy` file. Use this for single-array checkpoints, intermediate results, or fast caching:

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

# Save to file
np.save('my_array.npy', arr)

# File extension .npy is added automatically if missing
np.save('my_array', arr)  # Creates my_array.npy
```

### Parameters

```python
np.save(
    file,           # Filename or file object
    arr,            # Array to save
    allow_pickle=True,  # Allow pickling objects
    fix_imports=True    # Python 2/3 compatibility
)
```

---

## np.load() — Load Array

Load arrays from `.npy` or `.npz` files:

```python
# Load single array
arr = np.load('my_array.npy')
print(arr)
# [[1 2 3]
#  [4 5 6]]

# dtype is preserved
print(arr.dtype)  # int64
```

### Security Warning

```python
# allow_pickle=False is safer for untrusted files
arr = np.load('untrusted.npy', allow_pickle=False)

# Default changed in NumPy 1.16.3 for security
# Pickle can execute arbitrary code!
```

---

## np.savez() — Save Multiple Arrays

Save multiple arrays to a single `.npz` file (uncompressed):

```python
x = np.array([1, 2, 3])
y = np.array([4, 5, 6])
z = np.array([[1, 2], [3, 4]])

# Save with automatic names (arr_0, arr_1, arr_2)
np.savez('arrays.npz', x, y, z)

# Save with custom names (recommended)
np.savez('arrays.npz', x_data=x, y_data=y, matrix=z)
```

### Loading .npz Files

```python
# Load returns NpzFile object (dict-like)
data = np.load('arrays.npz')

# Access by name
print(data['x_data'])  # [1 2 3]
print(data['y_data'])  # [4 5 6]
print(data['matrix'])  # [[1 2] [3 4]]

# List available arrays
print(data.files)  # ['x_data', 'y_data', 'matrix']

# Close when done (or use context manager)
data.close()
```

### Context Manager (Recommended)

```python
# Automatically closes file
with np.load('arrays.npz') as data:
    x = data['x_data']
    y = data['y_data']
    print(x + y)  # [5 7 9]
```

---

## np.savez_compressed() — Compressed Archive

Same as `savez()` but with zlib compression. An `.npz` file is literally a zip archive containing one `.npy` file per array:

```python
large_array = np.random.randn(1000, 1000)

# Uncompressed: ~8 MB
np.savez('uncompressed.npz', data=large_array)

# Compressed: ~6 MB (varies by data)
np.savez_compressed('compressed.npz', data=large_array)
```

### When to Compress

| Scenario | Recommendation |
|----------|----------------|
| Large arrays, infrequent access | Compress |
| Small arrays | Don't compress (overhead) |
| Frequent loading | Don't compress (slower) |
| Limited disk space | Compress |
| Random/incompressible data | Don't compress (no benefit) |

---

## Practical Examples

### Save Model Weights

```python
# Save neural network weights
weights = {
    'layer1': np.random.randn(784, 256),
    'layer2': np.random.randn(256, 128),
    'layer3': np.random.randn(128, 10),
    'biases1': np.zeros(256),
    'biases2': np.zeros(128),
    'biases3': np.zeros(10),
}

np.savez_compressed('model_weights.npz', **weights)

# Load weights
with np.load('model_weights.npz') as data:
    w1 = data['layer1']
    b1 = data['biases1']
```

### Checkpoint Training Progress

```python
def save_checkpoint(epoch, weights, optimizer_state, loss_history):
    np.savez(
        f'checkpoint_epoch_{epoch}.npz',
        weights=weights,
        optimizer_state=optimizer_state,
        loss_history=np.array(loss_history),
        epoch=np.array(epoch)
    )

def load_checkpoint(filename):
    with np.load(filename, allow_pickle=True) as data:
        return {
            'weights': data['weights'],
            'optimizer_state': data['optimizer_state'],
            'loss_history': data['loss_history'].tolist(),
            'epoch': int(data['epoch'])
        }
```

### Save Preprocessed Data

```python
# Preprocess once, save for reuse
def preprocess_and_save(raw_data_path, output_path):
    raw = np.loadtxt(raw_data_path, delimiter=',')
    
    # Normalize
    mean = raw.mean(axis=0)
    std = raw.std(axis=0)
    normalized = (raw - mean) / std
    
    # Save data and parameters
    np.savez(
        output_path,
        data=normalized,
        mean=mean,
        std=std
    )

# Load preprocessed data
with np.load('preprocessed.npz') as f:
    data = f['data']
    mean = f['mean']
    std = f['std']
```

---

## Text Alternatives

Use text formats when you need **interoperability** (Excel, R, pandas, other tools) or **human readability** (inspecting values in a text editor). For pure NumPy workflows, binary formats are always faster.

### np.savetxt() / np.loadtxt()

```python
arr = np.array([[1.5, 2.5], [3.5, 4.5]])

# Save as text
np.savetxt('data.csv', arr, delimiter=',', header='col1,col2')

# Load from text
loaded = np.loadtxt('data.csv', delimiter=',')
```

### np.genfromtxt() — Handle Missing Values

```python
# More flexible than loadtxt
data = np.genfromtxt(
    'data.csv',
    delimiter=',',
    missing_values='NA',
    filling_values=0.0
)
```

---

## Memory-Mapped Files

!!! tip "Mental Model"
    A memory-mapped array is an **array backed by a file on disk instead of RAM**. NumPy accesses data through the OS virtual memory system — only the pages you touch are loaded into physical memory. This lets you work with 100 GB arrays on a machine with 16 GB of RAM, as long as you only access small slices at a time.

For arrays too large to fit in memory:

```python
# Create memory-mapped file
large = np.memmap('large_array.dat', dtype='float64', 
                   mode='w+', shape=(10000, 10000))
large[:] = np.random.randn(10000, 10000)
large.flush()  # Write to disk

# Load as memory-mapped (doesn't load into RAM)
mapped = np.memmap('large_array.dat', dtype='float64',
                    mode='r', shape=(10000, 10000))
print(mapped[0, 0])  # Access without loading entire array
```

---

## Common Anti-Pattern

!!! danger "Don't Save and Load Inside a Loop"
    ```python
    # BAD — disk I/O in a training loop
    for epoch in range(1000):
        weights = train_one_epoch(weights)
        np.save(f'weights_{epoch}.npy', weights)  # Writes 1000 files!
    ```

    This creates thousands of files and is extremely slow. Instead, save checkpoints at intervals:

    ```python
    # GOOD — checkpoint every 100 epochs
    for epoch in range(1000):
        weights = train_one_epoch(weights)
        if epoch % 100 == 0:
            np.savez(f'checkpoint_{epoch}.npz', weights=weights, epoch=epoch)
    ```

---

## Common Issues

### Issue 1: File Not Found

```python
# Always use raw strings or forward slashes for paths
np.save(r'C:\data\array.npy', arr)  # Raw string
np.save('C:/data/array.npy', arr)   # Forward slashes
```

### Issue 2: Pickle Security

```python
# Untrusted .npy files can contain pickled objects
# Always use allow_pickle=False for untrusted sources
try:
    arr = np.load('untrusted.npy', allow_pickle=False)
except ValueError:
    print("File contains pickled objects - potentially unsafe!")
```

### Issue 3: Version Compatibility

```python
# Old NumPy versions may not read new files
# Check NumPy version if sharing files
print(np.__version__)
```

---

## Summary

| Function | Purpose | File Type |
|----------|---------|-----------|
| `np.save()` | Save single array | `.npy` |
| `np.load()` | Load `.npy` or `.npz` | Both |
| `np.savez()` | Save multiple arrays | `.npz` |
| `np.savez_compressed()` | Save compressed | `.npz` |
| `np.savetxt()` | Save as text | `.csv`, `.txt` |
| `np.loadtxt()` | Load from text | `.csv`, `.txt` |
| `np.memmap()` | Memory-mapped I/O | `.dat` |

**Key Takeaways**:

- Use `.npy` for single arrays, `.npz` for multiple
- Binary format is faster and preserves dtypes
- Use `savez_compressed()` for large arrays with limited disk space
- Use context manager (`with`) when loading `.npz` files
- Set `allow_pickle=False` for untrusted files
- Use memory mapping for arrays too large for RAM

---

## Exercises

**Exercise 1.**
Create a 2D array `a = np.random.randn(100, 50)`. Save it with `np.save` to a file, load it back, and verify the loaded array matches the original exactly using `np.array_equal`. Print the file size in KB.

??? success "Solution to Exercise 1"

        import numpy as np
        import os

        a = np.random.randn(100, 50)
        np.save('/tmp/test_array.npy', a)
        loaded = np.load('/tmp/test_array.npy')

        print(f"Match: {np.array_equal(a, loaded)}")
        size_kb = os.path.getsize('/tmp/test_array.npy') / 1024
        print(f"File size: {size_kb:.1f} KB")
        os.remove('/tmp/test_array.npy')

---

**Exercise 2.**
Save three arrays (`x = np.arange(10)`, `y = np.linspace(0, 1, 10)`, and `z = np.eye(3)`) into a single `.npz` file with custom names. Load the file using a context manager, print the list of stored array names, and verify each loaded array matches the original.

??? success "Solution to Exercise 2"

        import numpy as np
        import os

        x = np.arange(10)
        y = np.linspace(0, 1, 10)
        z = np.eye(3)
        np.savez('/tmp/test_arrays.npz', x_data=x, y_data=y, z_data=z)

        with np.load('/tmp/test_arrays.npz') as data:
            print(f"Stored arrays: {data.files}")
            print(f"x match: {np.array_equal(data['x_data'], x)}")
            print(f"y match: {np.allclose(data['y_data'], y)}")
            print(f"z match: {np.array_equal(data['z_data'], z)}")
        os.remove('/tmp/test_arrays.npz')

---

**Exercise 3.**
Create a large array `a = np.random.randn(1000, 1000)`. Save it using both `np.savez` (uncompressed) and `np.savez_compressed`. Compare the file sizes and print the compression ratio.

??? success "Solution to Exercise 3"

        import numpy as np
        import os

        a = np.random.randn(1000, 1000)
        np.savez('/tmp/uncompressed.npz', data=a)
        np.savez_compressed('/tmp/compressed.npz', data=a)

        size_un = os.path.getsize('/tmp/uncompressed.npz')
        size_co = os.path.getsize('/tmp/compressed.npz')
        ratio = size_un / size_co

        print(f"Uncompressed: {size_un / 1e6:.2f} MB")
        print(f"Compressed:   {size_co / 1e6:.2f} MB")
        print(f"Compression ratio: {ratio:.2f}x")
        os.remove('/tmp/uncompressed.npz')
        os.remove('/tmp/compressed.npz')

---

**Exercise 4.**
Build a simple checkpoint-and-resume workflow. Write a function `save_checkpoint(path, epoch, weights, loss_history)` that saves all state to a single `.npz` file, and `load_checkpoint(path)` that restores it. Simulate 5 epochs of "training" (just random weights), save a checkpoint at epoch 3, then resume from the checkpoint and continue to epoch 5. Verify continuity.

??? success "Solution to Exercise 4"

        import numpy as np
        import os

        def save_checkpoint(path, epoch, weights, loss_history):
            np.savez(path, epoch=np.array(epoch),
                     weights=weights, loss_history=np.array(loss_history))

        def load_checkpoint(path):
            with np.load(path) as data:
                return {
                    'epoch': int(data['epoch']),
                    'weights': data['weights'],
                    'loss_history': data['loss_history'].tolist(),
                }

        # Simulate training
        weights = np.random.randn(10, 5)
        loss_history = []

        for epoch in range(1, 6):
            loss = 1.0 / epoch  # Fake decreasing loss
            loss_history.append(loss)
            weights = weights * 0.99  # Fake weight update

            if epoch == 3:
                save_checkpoint('/tmp/ckpt.npz', epoch, weights, loss_history)
                print(f"Checkpoint saved at epoch {epoch}")

        # Resume from checkpoint
        ckpt = load_checkpoint('/tmp/ckpt.npz')
        print(f"Resumed from epoch {ckpt['epoch']}")
        print(f"Loss history so far: {ckpt['loss_history']}")
        print(f"Weights shape: {ckpt['weights'].shape}")

        # Continue training from epoch 4
        weights = ckpt['weights']
        for epoch in range(ckpt['epoch'] + 1, 6):
            weights = weights * 0.99
            ckpt['loss_history'].append(1.0 / epoch)

        print(f"Final loss history: {ckpt['loss_history']}")
        os.remove('/tmp/ckpt.npz')

---

**Exercise 5.**
Compare load times for the same 1-million-element array saved in three formats: `.npy` (binary), `.csv` (text), and `.npz` (compressed). Use `time.perf_counter` to measure each. Explain why binary is fastest and when you might still choose CSV despite the speed penalty.

??? success "Solution to Exercise 5"

        import numpy as np
        import time
        import os

        arr = np.random.randn(1_000_000)

        # Save in three formats
        np.save('/tmp/bench.npy', arr)
        np.savetxt('/tmp/bench.csv', arr)
        np.savez_compressed('/tmp/bench.npz', data=arr)

        # Benchmark loads
        start = time.perf_counter()
        _ = np.load('/tmp/bench.npy')
        t_npy = time.perf_counter() - start

        start = time.perf_counter()
        _ = np.loadtxt('/tmp/bench.csv')
        t_csv = time.perf_counter() - start

        start = time.perf_counter()
        with np.load('/tmp/bench.npz') as f:
            _ = f['data']
        t_npz = time.perf_counter() - start

        # File sizes
        s_npy = os.path.getsize('/tmp/bench.npy') / 1e6
        s_csv = os.path.getsize('/tmp/bench.csv') / 1e6
        s_npz = os.path.getsize('/tmp/bench.npz') / 1e6

        print(f"{'Format':<12} {'Load time':>12} {'Size (MB)':>10}")
        print(f"{'NPY':<12} {t_npy:>12.4f}s {s_npy:>10.2f}")
        print(f"{'CSV':<12} {t_csv:>12.4f}s {s_csv:>10.2f}")
        print(f"{'NPZ (comp)':<12} {t_npz:>12.4f}s {s_npz:>10.2f}")

        # Cleanup
        for f in ['/tmp/bench.npy', '/tmp/bench.csv', '/tmp/bench.npz']:
            os.remove(f)

        # Binary (.npy) is fastest because it copies raw bytes directly
        # into the array — no text parsing, no type conversion.
        # CSV is slowest but may be necessary when:
        #   - Sharing data with non-Python tools (Excel, R, MATLAB)
        #   - Human readability is required (inspection, auditing)
        #   - The recipient does not have NumPy installed
