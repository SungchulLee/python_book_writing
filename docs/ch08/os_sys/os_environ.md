# Environment Variables (os.environ)

Access and modify environment variables through os.environ.

!!! tip "Mental Model"
    `os.environ` is a dictionary that mirrors the process's environment variables. Reading a key is like asking the operating system for a configuration value; setting a key changes it for the current process and any child processes it spawns. Use it for secrets, paths, and feature flags that should live outside your source code.

## Reading Environment Variables

Access environment variables.

```python
import os

# Get specific variable
home = os.environ.get('HOME', 'Not set')
print(f"HOME: {home}")

# Check if variable exists
if 'PATH' in os.environ:
    print("PATH is set")

# Get with default
debug = os.environ.get('DEBUG', 'false')
print(f"DEBUG: {debug}")

# List all variables
vars_count = len(os.environ)
print(f"Total env variables: {vars_count}")
```

```
HOME: /home/user
PATH is set
DEBUG: false
Total env variables: 50+
```

## Setting Environment Variables

Set environment variables during program execution.

```python
import os

# Set variable for current process
os.environ['MY_VAR'] = 'hello'
print(f"MY_VAR: {os.environ['MY_VAR']}")

# Set multiple variables
os.environ.update({
    'VAR1': 'value1',
    'VAR2': 'value2'
})

print(f"VAR1: {os.environ.get('VAR1')}")
print(f"VAR2: {os.environ.get('VAR2')}")

# Note: Changes only affect current process
print("Environment updated")
```

```
MY_VAR: hello
VAR1: value1
VAR2: value2
Environment updated
```

---

## Exercises

**Exercise 1.**
Write a function `get_config` that reads configuration from environment variables with defaults: `"APP_HOST"` (default `"localhost"`), `"APP_PORT"` (default `"8080"`), and `"APP_DEBUG"` (default `"false"`). Return a dictionary with these values. Convert `APP_PORT` to int and `APP_DEBUG` to bool.

??? success "Solution to Exercise 1"

    ```python
    import os

    def get_config():
        return {
            "host": os.environ.get("APP_HOST", "localhost"),
            "port": int(os.environ.get("APP_PORT", "8080")),
            "debug": os.environ.get("APP_DEBUG", "false").lower() == "true",
        }

    # Test
    config = get_config()
    print(config)
    # {'host': 'localhost', 'port': 8080, 'debug': False}
    ```

---

**Exercise 2.**
Write a context manager `temp_env` that temporarily sets an environment variable, yields, and then restores the original value (or removes the variable if it did not exist before). Test by setting `"TEST_VAR"` inside the context and verifying it is gone after.

??? success "Solution to Exercise 2"

    ```python
    import os
    from contextlib import contextmanager

    @contextmanager
    def temp_env(key, value):
        old_value = os.environ.get(key)
        os.environ[key] = value
        try:
            yield
        finally:
            if old_value is None:
                del os.environ[key]
            else:
                os.environ[key] = old_value

    # Test
    with temp_env("TEST_VAR", "hello"):
        print(os.environ["TEST_VAR"])  # hello
    print("TEST_VAR" in os.environ)    # False
    ```

---

**Exercise 3.**
Write a function `env_summary` that returns a dictionary with the count of environment variables, the total character length of all values combined, and a list of any variables whose names start with `"PYTHON"`.

??? success "Solution to Exercise 3"

    ```python
    import os

    def env_summary():
        env = os.environ
        python_vars = [k for k in env if k.startswith("PYTHON")]
        total_length = sum(len(v) for v in env.values())
        return {
            "count": len(env),
            "total_value_length": total_length,
            "python_vars": python_vars,
        }

    # Test
    summary = env_summary()
    print(f"Variables: {summary['count']}")
    print(f"Python vars: {summary['python_vars']}")
    ```
