# Process Management (os)

Create and manage processes using os module functions.

!!! tip "Mental Model"
    Every running Python script is a process with a PID, a parent, and an environment. The `os` module lets you inspect your own process (`os.getpid()`), spawn new ones (`os.fork()`, `os.exec*()`), and send signals to others (`os.kill()`). For most use cases, prefer `subprocess.run()` — but understanding the underlying `os`-level primitives explains what `subprocess` does under the hood.

## Process Information

Get information about the current process.

```python
import os

# Process ID
pid = os.getpid()
print(f"Process ID: {pid}")

# Parent process ID
ppid = os.getppid()
print(f"Parent Process ID: {ppid}")

# User ID
uid = os.getuid()
print(f"User ID: {uid}")

# Environment
print(f"Process name: python")
```

```
Process ID: 12345
Parent Process ID: 1234
User ID: 1000
Process name: python
```

## Running External Commands

Execute system commands (use subprocess for most cases).

```python
import os
import sys

# For simple commands, use os.system (deprecated, prefer subprocess)
# os.system returns exit code

# Get directory listing
exit_code = os.system('ls -la /tmp > /dev/null 2>&1')
print(f"ls exit code: {exit_code}")

# More reliable: use subprocess
import subprocess
result = subprocess.run(['echo', 'Hello'], capture_output=True, text=True)
print(f"Output: {result.stdout}")
```

```
ls exit code: 0
Output: Hello
```

---

## Exercises

**Exercise 1.**
Write a function `run_command` that takes a shell command string, runs it using `subprocess.run`, and returns a dictionary with `"returncode"`, `"stdout"`, and `"stderr"`. Capture both stdout and stderr as text.

??? success "Solution to Exercise 1"

    ```python
    import subprocess

    def run_command(command):
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }

    # Test
    output = run_command("echo Hello")
    print(output)
    # {'returncode': 0, 'stdout': 'Hello', 'stderr': ''}
    ```

---

**Exercise 2.**
Write a function `get_python_version` that uses `subprocess.run` to execute `python3 --version` and returns the version string (e.g., `"Python 3.12.0"`). Strip whitespace from the output.

??? success "Solution to Exercise 2"

    ```python
    import subprocess

    def get_python_version():
        result = subprocess.run(
            ["python3", "--version"], capture_output=True, text=True
        )
        return result.stdout.strip()

    # Test
    print(get_python_version())  # Python 3.x.x
    ```

---

**Exercise 3.**
Write a function `process_info` that returns a dictionary with the current process ID (`os.getpid()`), parent process ID (`os.getppid()`), and current user (`os.getlogin()` or fallback to environment variable `USER`).

??? success "Solution to Exercise 3"

    ```python
    import os

    def process_info():
        try:
            user = os.getlogin()
        except OSError:
            user = os.environ.get("USER", "unknown")
        return {
            "pid": os.getpid(),
            "ppid": os.getppid(),
            "user": user,
        }

    # Test
    info = process_info()
    for key, value in info.items():
        print(f"{key}: {value}")
    ```
