# Running Python

Execution is how expressions come to life. Everything you write is eventually evaluated step-by-step by the Python interpreter. Before writing programs, we must understand how this process works.

When you run a program, you are interacting with a loop: **write, run, observe, modify**. Understanding this cycle bridges theory and practice.

Python code can be run in several ways:

| Method                                    | Description                      |
| ----------------------------------------- | -------------------------------- |
| Interactive interpreter                   | run commands one line at a time  |
| Script execution                          | run `.py` files                  |
| Jupyter notebooks                         | interactive code + documentation |
| Integrated development environments (IDE) | full programming environment     |

!!! tip "Mental Model"
    The Python interpreter is a machine that reads your code one statement at a time, executes it, and moves on. Whether you type into a REPL or run a script file, the underlying process is the same: read, evaluate, continue. Understanding this loop is the key to predicting what your program will do.

---

## 1. Interactive Interpreter

The Python interpreter allows immediate evaluation of expressions.

Example session:

```python
>>> 2 + 3
5
>>> "hello".upper()
'HELLO'
```

Each line entered into the interpreter is evaluated immediately.

---

## 2. Running a Script

Python programs are commonly stored in `.py` files.

Example file:

```python
print("Hello, Python!")
```

Run it from the command line:

```bash
python hello.py
```

Output:

```
Hello, Python!
```

---

## 3. Program Execution Model

When Python runs a script, it performs the following steps:

```mermaid
flowchart TD
    A[Python source code] --> B[Compilation]
    B --> C[Bytecode]
    C --> D[Python Virtual Machine]
    D --> E[Machine Code Execution (CPU)]
    E --> F[Program output]
```

### Python Execution Pipeline

```
code → compile → bytecode → VM → machine code → CPU → result
```

### Compile Time vs Run Time

**Compile time (before execution):**

- Python parses the code
- Generates bytecode
- **Determines variable scope (very important)**
- Detects syntax errors

**Run time (during execution):**

- Bytecode is executed by the Python Virtual Machine (PVM)
- Values are computed
- Runtime errors may occur

> Key idea:  
> **Compile time decides *where to look* (scope)**  
> **Run time determines *what value is found***

---

### Bytecode vs Machine Code

These may look similar, but they are fundamentally different:

| Type | Executed by | Description |
|------|------------|-------------|
| Bytecode | Python VM | Intermediate instructions |
| Machine code | CPU | Hardware-level instructions |

**Pipeline difference:**

- C/C++:
  ```
  code → machine code → CPU
  ```

- Python:
  ```
  code → bytecode → VM → CPU
  ```

> Bytecode is portable (same across systems),  
> machine code is hardware-specific.

---

### Role of the Python Virtual Machine (PVM)

The PVM acts as a **translator**:

- Reads bytecode
- Converts it into machine-level operations
- Sends instructions to the CPU

You can think of it as:

```
bytecode → (interpreted by VM) → machine actions → CPU
```

---

Python reports errors at two different stages:

| Error type | When | Example |
|---|---|---|
| `SyntaxError` | during compilation (before any code runs) | `x = 10 +` |
| `TypeError` | during execution (at runtime) | `"1" + 2` |

A syntax error prevents the entire script from running. A runtime error only occurs when the faulty line is reached.

Learning to read **tracebacks** is one of the most practical debugging skills:

```text
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    total = price + tax
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

Read from the bottom up: the last line tells you *what* failed, the line above tells you *where*, and the chain above that tells you *how execution got there*.

You can inspect bytecode using the `dis` module:

```python
import dis
dis.dis(lambda x, y: x + y)
```

This shows the low-level instructions the PVM executes.

---

## 4. Practical Workflow

In practice, the development cycle looks like this:

1. **Write** code in an editor or notebook
2. **Run** the script or cell
3. **Observe** the output or error traceback
4. **Modify** the code based on what you learned

The interactive interpreter is ideal for exploring small ideas. Scripts are better for complete programs. Most real work alternates between the two.

!!! tip "One thing to remember"
    Python compiles your code to bytecode, then executes it via a virtual machine before reaching the CPU.


---

## 5. Why Python Uses a Virtual Machine

Python does not execute bytecode directly on the CPU. Instead, it uses a **Virtual Machine (PVM)** as an intermediate layer.

### Key Idea

```
bytecode → VM → CPU
```

### Why add this extra layer?

#### 1. Portability
- Same Python code runs on different systems (Windows, Mac, Linux)
- Only the VM needs to adapt to the underlying CPU

> Write once, run anywhere

---

#### 2. Simpler Language Design
Python does not need to deal with:

- CPU instruction sets
- Registers
- Low-level memory handling

The VM abstracts these details away.

---

#### 3. Dynamic Features
Python supports:
```python
x = 10
x = "hello"
```

and even:

```python
def f():
    return 42

f = 100
```

This flexibility is much easier to support with a VM than with direct machine code.

---

#### 4. Better Error Handling
Because execution is controlled by the VM:

- Python can provide detailed tracebacks
- Errors can be detected cleanly at runtime

---

#### 5. Memory Management
The VM manages:

- Object creation
- Reference counting
- Garbage collection

No manual memory management is required.

---

### Trade-off

Using a VM adds overhead:

```
bytecode → VM → CPU
```

So Python is slower than low-level languages like C, but much easier to use.

---

## 6. Python, Java, and C Execution Model Comparison

These languages differ mainly in **how code reaches the CPU**.

| Language | Pipeline | Main Strength |
|----------|----------|---------------|
| C | code → machine code → CPU | maximum performance and hardware control |
| Python | code → bytecode → VM → CPU | simplicity and flexibility |
| Java | code → bytecode → JVM → CPU | portability with stronger static structure |

### Comparison Box

!!! info "Python vs Java vs C"
    **C**

    - Compiles directly to **machine code**
    - CPU executes it directly
    - Very fast and close to hardware
    - Platform-specific after compilation

    ```text
    code → machine code → CPU
    ```

    **Python**

    - Compiles to **bytecode**
    - Bytecode is executed by the **Python Virtual Machine (PVM)**
    - Very flexible and easy to use, but slower

    ```text
    code → bytecode → PVM → CPU
    ```

    **Java**

    - Compiles to **bytecode**
    - Bytecode is executed by the **Java Virtual Machine (JVM)**
    - More portable than C, usually more structured and faster than Python in many cases

    ```text
    code → bytecode → JVM → CPU
    ```

### Why compare Python with Java and C?

Python and Java both use a virtual machine layer, so they share an important idea:

> The program does **not** talk directly to the CPU first.  
> It first runs through a virtual machine.

C is different:

> C is compiled to **machine code**, so the CPU can execute it directly.

This creates a useful three-way contrast:

- **Python** prioritizes readability, dynamic behavior, and ease of use
- **Java** prioritizes portability, structured design, and strong static checking
- **C** prioritizes direct hardware performance and low-level control

### Important nuance

Although both Python and Java use bytecode and a VM, they are not identical:

- Python is generally more dynamic at runtime
- Java is typically compiled with more static type information
- Modern JVMs often use advanced optimizations such as **JIT (Just-In-Time) compilation**
- CPython usually interprets bytecode more directly, which is one reason Python is often slower than Java

C is different from both:

- C code is compiled ahead of time into platform-specific machine code
- There is no Python-style or Java-style VM in the normal execution model
- The program runs much closer to the hardware

### One-line takeaway

> **C** aims to run close to the machine.
> **Python** aims to make programming easy and flexible.
> **Java** sits in between: portable like Python, but more performance-oriented and statically structured.

---



---

## Notebook Examples

```python
if __name__ == "__main__":
    main()
```

---

## Exercises

**Exercise 1.**
Open the Python interpreter and evaluate the following expressions one at a time. Write down the output of each before running them, then verify your predictions.

```python
>>> 10 + 20
>>> "hello" * 3
>>> type(3.14)
```

??? success "Solution to Exercise 1"
    ```python
    >>> 10 + 20
    30
    >>> "hello" * 3
    'hellohellohello'
    >>> type(3.14)
    <class 'float'>
    ```

    The interpreter evaluates each expression and prints the result immediately. `10 + 20` performs integer addition. `"hello" * 3` repeats the string three times. `type(3.14)` returns the type of the float literal.

---

**Exercise 2.**
A student runs this script and gets an error before any output appears:

```python
print("start")
x = 10 +
print("end")
```

Is this a compile-time error or a runtime error? Why does `"start"` never print?

??? success "Solution to Exercise 2"
    This is a **compile-time error** (`SyntaxError: invalid syntax`). Python compiles the entire script to bytecode before executing any of it. The syntax error on line 2 prevents compilation from completing, so the PVM never runs --- not even the first `print`.

    This demonstrates the two-stage execution model: compilation happens first (catches syntax errors), then execution (catches runtime errors like `TypeError`, `ValueError`). If compilation fails, nothing runs.

---

**Exercise 3.**
Explain the key difference between Python's execution model and C's. Why does Python use a virtual machine instead of compiling directly to machine code? Name one advantage and one disadvantage of this approach.

??? success "Solution to Exercise 3"
    **C** compiles source code directly to machine code that the CPU executes. **Python** compiles source code to bytecode, which is then interpreted by the Python Virtual Machine (PVM), which in turn issues instructions to the CPU.

    **Advantage**: Portability and flexibility. The same Python bytecode runs on any platform that has a PVM. Python can also support dynamic features (like changing a variable's type at runtime) more easily because the VM controls execution.

    **Disadvantage**: Performance overhead. The extra VM layer means Python code runs slower than equivalent C code, since every bytecode instruction must be interpreted rather than executed directly by the CPU.
