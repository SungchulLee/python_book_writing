# sys.argv and sys.exit

Process command-line arguments with sys.argv and control program termination with sys.exit.

!!! tip "Mental Model"
    `sys.argv` is a list of strings the OS hands to your script — `argv[0]` is the script name, and the rest are whatever the user typed after it. `sys.exit()` is the clean way to stop the program with a status code (0 = success, nonzero = error). Together they form the minimal interface between a Python script and the shell that launched it.

## sys.argv - Command-Line Arguments

Access command-line arguments passed to the script.

```python
import sys

print(f"Script name: {sys.argv[0]}")
print(f"All arguments: {sys.argv}")
print(f"Number of arguments: {len(sys.argv)}")

# Example with arguments
if len(sys.argv) > 1:
    print(f"First argument: {sys.argv[1]}")

# Process arguments
def process_args():
    if len(sys.argv) < 2:
        print("Usage: script.py <name>")
        return
    name = sys.argv[1]
    print(f"Hello, {name}")

process_args()
```

```
Script name: script.py
All arguments: ['script.py']
Number of arguments: 1
Usage: script.py <name>
```

## sys.exit - Program Termination

Exit the program with a specific exit code.

```python
import sys

def safe_divide(a, b):
    if b == 0:
        print("Error: division by zero")
        sys.exit(1)  # Exit with error code
    return a / b

# Successful execution
result = safe_divide(10, 2)
print(f"Result: {result}")

# Demonstrate exit code
print("Program completed successfully")
sys.exit(0)  # Exit with success code
```

```
Result: 5.0
Program completed successfully
```

---

## Exercises

**Exercise 1.**
Write a script that uses `sys.argv` to accept a filename and an optional `--count` flag. If `--count` is provided, print the number of characters in the filename string (not the file content). Otherwise, print the filename. Simulate by setting `sys.argv` manually.

??? success "Solution to Exercise 1"

    ```python
    import sys

    # Simulate command line args
    sys.argv = ["script.py", "data.txt", "--count"]

    filename = sys.argv[1] if len(sys.argv) > 1 else None
    count_flag = "--count" in sys.argv

    if filename:
        if count_flag:
            print(f"Character count: {len(filename)}")
        else:
            print(f"Filename: {filename}")
    # Character count: 8
    ```

---

**Exercise 2.**
Write a function `parse_key_value_args` that takes `sys.argv[1:]` and parses arguments in the format `key=value`. Return a dictionary of the parsed pairs. For example, `["host=localhost", "port=8080"]` should return `{"host": "localhost", "port": "8080"}`.

??? success "Solution to Exercise 2"

    ```python
    def parse_key_value_args(args):
        result = {}
        for arg in args:
            if "=" in arg:
                key, value = arg.split("=", 1)
                result[key] = value
        return result

    # Test
    args = ["host=localhost", "port=8080", "debug=true"]
    print(parse_key_value_args(args))
    # {'host': 'localhost', 'port': '8080', 'debug': 'true'}
    ```

---

**Exercise 3.**
Write a function `validate_and_exit` that takes an integer exit code and an optional error message. If the exit code is non-zero, print the error message to `sys.stderr` and call `sys.exit(code)`. Otherwise, print `"Success"` to `sys.stdout`. Use `sys.stderr.write()` for errors.

??? success "Solution to Exercise 3"

    ```python
    import sys

    def validate_and_exit(code, message=None):
        if code != 0:
            if message:
                sys.stderr.write(f"Error: {message}\n")
            # sys.exit(code)  # Uncomment in real usage
            print(f"Would exit with code {code}")
        else:
            print("Success")

    # Test
    validate_and_exit(0)          # Success
    validate_and_exit(1, "Failed")  # Error: Failed
    ```
