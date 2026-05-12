# Python Execution Model

Is Python compiled or interpreted? The answer is **both** — Python compiles source code to bytecode, then interprets the bytecode. Understanding this model explains why some operations are fast and others are slow.

---

## Compiled vs Interpreted Languages

### Compiled Languages (C, C++, Rust)

```
Source Code (.c) → Compiler → Machine Code (.exe) → CPU
```

- Compiled once, runs directly on hardware
- Fast execution
- Platform-specific binaries
- Errors caught at compile time

### Interpreted Languages (Old BASIC)

```
Source Code → Interpreter → Execute line by line
```

- No compilation step
- Slower execution
- Cross-platform source code
- Errors found at runtime

### Python: Hybrid Approach

```
Source Code (.py) → Compiler → Bytecode (.pyc) → Interpreter (PVM) → CPU
```

Python compiles to **bytecode**, then the Python Virtual Machine (PVM) interprets it.

---

## Python's Execution Steps

### Step 1: Compilation to Bytecode

```python
# hello.py
print("Hello, World!")
```

When you run this, Python:

1. Parses the source code
2. Compiles it to bytecode
3. Stores bytecode in `.pyc` files (in `__pycache__/`)

### Step 2: Bytecode Interpretation

The Python Virtual Machine (PVM) reads bytecode instructions and executes them one by one. This per-instruction overhead is what makes Python slower than compiled languages.

---

## Viewing Bytecode

Use the `dis` module to disassemble Python code:

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
```

Output:
```
  2           0 LOAD_FAST                0 (a)
              2 LOAD_FAST                1 (b)
              4 BINARY_ADD
              6 RETURN_VALUE
```

This reveals the low-level operations executed by the VM.

---

## The `__pycache__` Directory

Python caches compiled bytecode:

```
my_project/
├── main.py
├── utils.py
└── __pycache__/
    ├── main.cpython-311.pyc
    └── utils.cpython-311.pyc
```

- `.pyc` files contain bytecode
- `cpython-311` indicates Python version
- Speeds up subsequent imports
- Automatically regenerated when source changes

### Creating `.pyc` Files Manually

```python
import py_compile

py_compile.compile('my_script.py')
```

Or compile entire directory:

```bash
python -m compileall .
```

---

## Why This Matters: Order of Definition

Because Python interprets line by line, **order matters**:

### Bug: Using Before Defining

```python
# This will fail!
ops = (add, subtract)  # NameError: name 'add' is not defined

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y
```

### Fix: Define Before Using

```python
# Define first
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

# Then use
ops = (add, subtract)  # Works!
```

Python executes top-to-bottom. When it sees `add` in the tuple, the function hasn't been defined yet.

---

## Running Python Scripts

### From Command Line

```bash
python script.py
```

### What Happens

1. Python reads `script.py`
2. Compiles to bytecode (in memory or `.pyc`)
3. PVM executes bytecode
4. Program runs

### The `if __name__ == "__main__":` Guard

```python
# my_module.py
def main():
    print("Running as script")

if __name__ == "__main__":
    main()
```

- When run directly: `__name__` is `"__main__"` → `main()` executes
- When imported: `__name__` is `"my_module"` → `main()` doesn't execute

---

## Performance: Where Python is Slow

Python is slow when:

- **Looping in pure Python**: Each iteration has VM overhead
- **Creating many small objects**: Memory allocation cost
- **Calling functions repeatedly in tight loops**: Function call overhead

```python
# Slow: Pure Python loop
total = 0
for i in range(1_000_000):
    total += i
```

### Why Python is "Slow"

1. **Dynamic typing**: Type checks at runtime
2. **Interpretation**: Bytecode interpreted, not native machine code
3. **GIL**: Global Interpreter Lock limits multi-threading

---

## Performance: Where Python is Fast

Python is fast when:

- **Delegating to C extensions**: NumPy, pandas, etc.
- **Using built-in functions**: Implemented in C
- **Minimizing Python-level loops**: Vectorized operations

```python
# Fast: NumPy vectorized (C extension)
import numpy as np
total = np.arange(1_000_000).sum()
```

### Mental Model for Performance

Think in terms of:

- Reducing Python-level operations
- Pushing work into optimized libraries
- Clarity before optimization (profile first!)

---

## Python Implementations

### CPython (Standard)

- Reference implementation
- Written in C
- Compiles to bytecode, interprets with PVM
- What you get from python.org

### PyPy

- JIT (Just-In-Time) compiler
- Much faster for long-running programs
- Compatible with most Python code

### Jython

- Python on the Java Virtual Machine
- Compiles to Java bytecode

### IronPython

- Python on .NET
- Compiles to .NET bytecode

---

## Python 2 vs Python 3

Python 2 reached end-of-life in 2020. Key differences:

| Feature | Python 2 | Python 3 |
|---------|----------|----------|
| Print | `print "hello"` | `print("hello")` |
| Division | `5/2 = 2` (int) | `5/2 = 2.5` (float) |
| Strings | ASCII default | Unicode default |
| `range()` | Returns list | Returns iterator |
| `input()` | Evaluates input | Returns string |

### Always Use Python 3

```bash
python --version    # Should be 3.x
python3 --version   # Explicitly Python 3
```

---


## Summary

| Aspect | Details |
|--------|---------|
| Compilation | Source → Bytecode → PVM execution |
| Bytecode cache | `__pycache__/*.pyc` files |
| Order | Define before using (top-to-bottom execution) |
| Slow operations | Pure Python loops, many small objects, tight function calls |
| Fast operations | C extensions, built-ins, vectorized operations |
| Standard implementation | CPython (from python.org) |
| Faster alternative | PyPy (JIT compilation) |

**Key Takeaways**:

- Python is **compiled to bytecode**, then **interpreted** by the PVM
- The VM executes instruction by instruction, introducing overhead
- **Order matters**: Define before using
- Use `dis` module to inspect bytecode
- Use `if __name__ == "__main__":` for script entry points
- **Performance** comes from pushing work to C extensions and built-ins
- **Always use Python 3** (Python 2 is EOL)

---

## Runnable Example: `code_object_anatomy.py`

```python
"""
Code Object Anatomy: Bytecode, co_* Attributes, and Disassembly

Every function in Python is compiled into a code object that the
CPython virtual machine executes. This tutorial explores code object
attributes, manual bytecode decoding, and the line number table.

Topics covered:
1. Code object attributes (co_argcount, co_varnames, co_cellvars, etc.)
2. Manual bytecode decoding from co_code
3. Line number table (co_lnotab) mapping
4. Nested code objects (closures)
5. Code object flags (co_flags)
6. Comparing code objects across functions

Based on CPython-Internals Interpreter/code/code.md examples.
"""

import dis
import opcode
import types


# =============================================================================
# 1. Code Object Attributes Overview
# =============================================================================

def demo_code_attributes():
    """Explore all major attributes of a code object.

    Access a function's code object via func.__code__.
    """
    print("=== Code Object Attributes ===\n")

    def example(x, y, *args, z=3, **kwargs):
        """Function with diverse parameter types."""
        def inner():
            inner_local = 4
            print(x, k, inner_local)
        k = 4
        print(x, y, args, kwargs)

    code = example.__code__

    attrs = [
        ('co_name',           'Function name'),
        ('co_argcount',       'Positional arg count (excludes *args, **kwargs)'),
        ('co_kwonlyargcount', 'Keyword-only arg count'),
        ('co_nlocals',        'Total local variables'),
        ('co_stacksize',      'Max stack depth needed'),
        ('co_flags',          'Flags bitmap (see section 5)'),
        ('co_firstlineno',    'First line number in source'),
        ('co_varnames',       'Local variable names (params first)'),
        ('co_cellvars',       'Variables also used in nested functions'),
        ('co_freevars',       'Variables from enclosing scope'),
        ('co_consts',         'Constants used (including nested code objects)'),
        ('co_names',          'Names used (globals, attributes)'),
        ('co_filename',       'Source filename'),
    ]

    for attr, description in attrs:
        val = getattr(code, attr)
        print(f"  {attr:25s} = {val!r}")
        print(f"  {'':25s}   # {description}")
        print()


# =============================================================================
# 2. Manual Bytecode Decoding
# =============================================================================

def demo_bytecode_decoding():
    """Decode raw bytecode (co_code) into human-readable instructions.

    CPython bytecode uses 2-byte instructions: opcode + argument.
    Opcodes >= HAVE_ARGUMENT (90) use the argument byte.
    Opcodes < 90 ignore the argument byte.
    """
    print("=== Manual Bytecode Decoding ===\n")

    def add(a, b):
        return a + b

    code = add.__code__
    raw = code.co_code
    print(f"Raw co_code bytes: {raw!r}")
    print(f"As integers: {list(raw)}")
    print()

    # Decode manually
    print("Manual decode:")
    print(f"  {'Offset':>6}  {'Opcode':>6}  {'Arg':>4}  {'Name':<20}  Detail")
    print(f"  {'------':>6}  {'------':>6}  {'----':>4}  {'----':<20}  ------")

    i = 0
    while i < len(raw):
        op = raw[i]
        arg = raw[i + 1] if i + 1 < len(raw) else 0
        name = opcode.opname[op]

        detail = ""
        if op >= opcode.HAVE_ARGUMENT:
            if op in opcode.hasconst:
                detail = f"({code.co_consts[arg]!r})"
            elif op in opcode.haslocal:
                detail = f"({code.co_varnames[arg]})"
            elif op in opcode.hasname:
                detail = f"({code.co_names[arg]})"
        else:
            arg = None  # type: ignore[assignment]

        print(f"  {i:>6}  {op:>6}  {str(arg):>4}  {name:<20}  {detail}")
        i += 2

    # Compare with dis output
    print(f"\ndis.dis() output for verification:")
    dis.dis(add)
    print()


# =============================================================================
# 3. Line Number Table (co_lnotab)
# =============================================================================

def demo_lnotab():
    """Decode co_lnotab: maps bytecode offsets to source line numbers.

    co_lnotab is a sequence of (bytecode_increment, line_increment) pairs.
    Starting from co_firstlineno, accumulate increments to find which
    source line each bytecode offset corresponds to.
    """
    print("=== Line Number Table (co_lnotab) ===\n")

    def multi_line(x):
        x = 3
        y = 4
        z = x + y
        return z

    code = multi_line.__code__
    lnotab = list(code.co_lnotab)

    print(f"co_firstlineno: {code.co_firstlineno}")
    print(f"co_lnotab bytes: {lnotab}")
    print()

    # Decode the table
    print("Decoded line number table:")
    print(f"  {'Byte offset':>12}  {'Source line':>12}")
    print(f"  {'----------':>12}  {'----------':>12}")

    byte_offset = 0
    line_number = code.co_firstlineno
    print(f"  {byte_offset:>12}  {line_number:>12}  (start)")

    for i in range(0, len(lnotab), 2):
        byte_incr = lnotab[i]
        line_incr = lnotab[i + 1]
        byte_offset += byte_incr
        line_number += line_incr
        print(f"  {byte_offset:>12}  {line_number:>12}  "
              f"(+{byte_incr} bytes, +{line_incr} lines)")

    # Compare with dis output
    print(f"\ndis.dis() for verification:")
    dis.dis(multi_line)
    print()


# =============================================================================
# 4. Nested Code Objects (Closures)
# =============================================================================

def demo_nested_code_objects():
    """Nested functions create child code objects stored in co_consts.

    co_cellvars: variables captured BY nested functions (in the outer).
    co_freevars: variables FROM enclosing scope (in the inner).
    """
    print("=== Nested Code Objects (Closures) ===\n")

    def outer(x):
        k = 10
        def inner():
            return x + k
        return inner

    outer_code = outer.__code__

    print(f"outer() code object:")
    print(f"  co_varnames:  {outer_code.co_varnames}")
    print(f"  co_cellvars:  {outer_code.co_cellvars}")
    print(f"  co_freevars:  {outer_code.co_freevars}")
    print()

    # Find inner's code object in co_consts
    inner_code = None
    for const in outer_code.co_consts:
        if isinstance(const, types.CodeType):
            inner_code = const
            break

    if inner_code:
        print(f"inner() code object (found in outer.co_consts):")
        print(f"  co_name:      {inner_code.co_name}")
        print(f"  co_varnames:  {inner_code.co_varnames}")
        print(f"  co_cellvars:  {inner_code.co_cellvars}")
        print(f"  co_freevars:  {inner_code.co_freevars}")
        print()
        print("  Note: inner.co_freevars matches outer.co_cellvars")
        print("  This is how closures capture variables from enclosing scope.")
    print()


# =============================================================================
# 5. Code Object Flags (co_flags)
# =============================================================================

def demo_code_flags():
    """co_flags is a bitmap encoding function properties.

    Common flags (from Include/cpython/code.h):
      0x01  CO_OPTIMIZED     — uses fast locals
      0x02  CO_NEWLOCALS     — creates new locals dict
      0x04  CO_VARARGS       — has *args
      0x08  CO_VARKEYWORDS   — has **kwargs
      0x20  CO_GENERATOR     — is a generator function
      0x40  CO_NOFREE        — no free/cell variables
      0x100 CO_COROUTINE     — is an async function
      0x200 CO_ITERABLE_COROUTINE
    """
    print("=== Code Object Flags ===\n")

    flag_names = {
        0x01:  'CO_OPTIMIZED',
        0x02:  'CO_NEWLOCALS',
        0x04:  'CO_VARARGS',
        0x08:  'CO_VARKEYWORDS',
        0x20:  'CO_GENERATOR',
        0x40:  'CO_NOFREE',
        0x100: 'CO_COROUTINE',
    }

    def regular(x): return x
    def with_args(*args): return args
    def with_kwargs(**kw): return kw
    def gen_func(): yield 1
    async def async_func(): pass

    functions = [
        ('regular(x)',      regular),
        ('with_args(*args)', with_args),
        ('with_kwargs(**kw)', with_kwargs),
        ('gen_func()',      gen_func),
        ('async_func()',    async_func),
    ]

    for label, func in functions:
        flags = func.__code__.co_flags
        active = [name for bit, name in sorted(flag_names.items())
                  if flags & bit]
        print(f"  {label:25s}  flags=0x{flags:04x}  {active}")
    print()


# =============================================================================
# 6. Comparing Code Objects
# =============================================================================

def demo_code_comparison():
    """Compare code objects from similar functions to see
    what changes and what stays the same.
    """
    print("=== Comparing Code Objects ===\n")

    def add(a, b):
        return a + b

    def multiply(a, b):
        return a * b

    def add_three(a, b, c):
        return a + b + c

    pairs = [
        ('add vs multiply', add.__code__, multiply.__code__),
        ('add vs add_three', add.__code__, add_three.__code__),
    ]

    compare_attrs = [
        'co_argcount', 'co_nlocals', 'co_stacksize',
        'co_varnames', 'co_code',
    ]

    for label, c1, c2 in pairs:
        print(f"  --- {label} ---")
        for attr in compare_attrs:
            v1 = getattr(c1, attr)
            v2 = getattr(c2, attr)
            match = "==" if v1 == v2 else "!="
            print(f"    {attr:20s}  {match}  "
                  f"{v1!r} vs {v2!r}")
        print()


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    demo_code_attributes()
    demo_bytecode_decoding()
    demo_lnotab()
    demo_nested_code_objects()
    demo_code_flags()
    demo_code_comparison()
```


## Exercises

**Exercise 1.**
Python compiles source code to bytecode before executing it. Predict the output:

```python
import dis

def greet(name):
    return "Hello, " + name + "!"

print(type(greet.__code__))
print(greet.__code__.co_varnames)
print(greet.__code__.co_consts)
dis.dis(greet)
```

What is a code object? Why does Python compile to bytecode rather than interpreting source text directly or compiling to machine code?

??? success "Solution to Exercise 1"
    The output shows:

    ```text
    <class 'code'>
    ('name',)
    (None, 'Hello, ', '!')
    ```

    Followed by the bytecode disassembly showing `LOAD_CONST`, `LOAD_FAST`, `BINARY_ADD`, and `RETURN_VALUE` instructions.

    A **code object** (`types.CodeType`) is the compiled representation of a block of Python code. It contains: the bytecode instructions (`co_code`), constants used (`co_consts`), variable names (`co_varnames`), and metadata like line numbers.

    Python compiles to bytecode as a middle ground: interpreting raw source text would require re-parsing every execution (slow), while compiling to machine code would sacrifice portability and dynamic features (no runtime `eval`, no dynamic typing). Bytecode is platform-independent and faster to interpret than raw text, while preserving Python's dynamic nature.

---

**Exercise 2.**
Python executes top-to-bottom, and `def` is an executable statement. Predict the output:

```python
print(type(f))  # Line 1

def f():
    return 42

print(type(f))  # Line 2
print(f())      # Line 3
```

Why does Line 1 raise a `NameError`? In what sense is `def` not a "declaration" but an "assignment statement"? How does this differ from languages like C or Java where functions exist before execution begins?

??? success "Solution to Exercise 2"
    Line 1 raises `NameError: name 'f' is not defined`.

    In Python, `def f():` is an **executable statement** that creates a function object and binds it to the name `f` in the current namespace. Before that statement executes, the name `f` simply does not exist. Python executes statements sequentially from top to bottom.

    This differs fundamentally from C/Java where the compiler processes the entire source file before execution begins, making all function definitions available everywhere (in C, with forward declarations; in Java, unconditionally). Python has no "declaration phase" -- everything happens at runtime.

    This is why `def` is really just syntactic sugar for assignment: `def f(): return 42` is essentially `f = <create function object>`. The name binding happens at the exact moment the `def` statement is reached during execution.

---

**Exercise 3.**
`.pyc` files cache compiled bytecode. Predict what happens:

```python
# Scenario: you have module.py
# Step 1: import module  (creates __pycache__/module.cpython-311.pyc)
# Step 2: edit module.py  (modify a function)
# Step 3: import module  (in a new Python session)

# Question: does Step 3 use the old .pyc or recompile?
# What timestamp mechanism does Python use?

import py_compile
import importlib
import os

py_compile.compile('__init__.py')  # Manually compile
print(os.path.exists('__pycache__'))
```

Why does Python cache bytecode in `.pyc` files but not cache the final execution results? What problem does the `__pycache__` directory solve?

??? success "Solution to Exercise 3"
    Step 3 **recompiles** `module.py` because Python checks if the source file's modification timestamp is newer than the `.pyc` file's recorded timestamp. If the source is newer, Python recompiles and overwrites the `.pyc`.

    Python caches **bytecode** (the compilation result) because compilation is a fixed cost: parsing and compiling are deterministic -- the same source always produces the same bytecode. Caching avoids repeating this work on every import.

    Python does **not** cache execution results because execution depends on runtime state: user input, global variables, database contents, time of day, etc. The same bytecode can produce different results on each run.

    The `__pycache__` directory solves the version-collision problem: multiple Python versions can coexist because each `.pyc` file includes the version tag (e.g., `cpython-311`). This prevents Python 3.11 from accidentally loading bytecode compiled by Python 3.10.
