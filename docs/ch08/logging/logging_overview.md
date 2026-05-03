# logging Overview

The `logging` module provides a flexible framework for emitting log messages from Python programs.

!!! tip "Mental Model"
    The `logging` module replaces `print()` debugging with a structured pipeline: your code emits messages at a severity level, loggers filter by that level, handlers route surviving messages to destinations (console, file, network), and formatters stamp each line with context (time, module, line number). Once set up, you change *where* and *how much* you log without touching any application code.

## Basic Logging

Start logging with minimal configuration.

```python
import logging

# Basic configuration
logging.basicConfig(level=logging.DEBUG)

# Log messages at different levels
logging.debug("Debug message")
logging.info("Info message")
logging.warning("Warning message")
logging.error("Error message")
logging.critical("Critical message")
```

```
DEBUG:root:Debug message
INFO:root:Info message
WARNING:root:Warning message
ERROR:root:Error message
CRITICAL:root:Critical message
```

## Logger Objects

Use named loggers for better organization.

```python
import logging

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handler
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Log messages
logger.info("Application started")
logger.warning("Low memory")
```

```
2026-02-12 12:34:56,789 - __main__ - INFO - Application started
2026-02-12 12:34:56,789 - __main__ - WARNING - Low memory
```

---

## Runnable Example: `basic_logging_tutorial.py`

```python
"""
01_basic_logging.py - Introduction to Python Logging

LEARNING OBJECTIVES:
- Understand why logging is better than print() statements
- Learn the five standard logging levels
- Use basic logging functions
- Configure basic logging settings

DIFFICULTY: Beginner
ESTIMATED TIME: 30 minutes
"""

# ============================================================================
# PART 1: WHY USE LOGGING INSTEAD OF PRINT()?
# ============================================================================

"""
Before we dive into logging, let's understand why we need it.

PROBLEMS WITH print():
1. No severity levels - all messages look the same
2. Hard to turn on/off without changing code
3. Always goes to stdout (can't easily redirect)
4. No timestamps or context information
5. Difficult to filter messages
6. Not suitable for production applications

ADVANTAGES OF logging:
1. Five different severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
2. Easy to configure what gets displayed
3. Can output to multiple destinations (console, files, networks, etc.)
4. Automatic timestamps and other metadata
5. Can filter by severity or other criteria
6. Industry standard for production code
"""

# Import the logging module - this is built into Python, no installation needed
import logging

print("=" * 80)
print("EXAMPLE 1: Comparison between print() and logging")
print("=" * 80)

# Traditional approach with print() - not recommended
print("This is a print statement - no severity level")
print("Another print statement - can't tell if it's important or not")

# Logging approach - recommended
logging.warning("This is a warning message - you can see the severity!")
logging.error("This is an error message - clearly distinguished from warning")

"""
OUTPUT ANALYSIS:
- Notice that logging automatically includes:
  1. Severity level (WARNING, ERROR, etc.)
  2. Logger name (root is the default)
  3. Message text

- print() just shows plain text with no context
"""

# ============================================================================
# PART 2: THE FIVE LOGGING LEVELS
# ============================================================================

"""
Python's logging module has five standard levels, in increasing order of severity:

1. DEBUG (10): Detailed information for diagnosing problems
   - Use for: Variable values, function entry/exit, detailed state
   - Typically only enabled during development

2. INFO (20): Confirmation that things are working as expected
   - Use for: Major milestones, successful operations, program flow
   - Useful for understanding program behavior

3. WARNING (30): Something unexpected happened, but program continues
   - Use for: Deprecated features, unusual situations, potential issues
   - The program still works but something might need attention

4. ERROR (40): A serious problem, program couldn't perform a function
   - Use for: Exceptions, failed operations, serious issues
   - The program continues but some functionality failed

5. CRITICAL (50): A very serious error, program may not be able to continue
   - Use for: Program crash, data corruption, system failure
   - The program might need to shut down
"""

print("\n" + "=" * 80)
print("EXAMPLE 2: Demonstrating all five logging levels")
print("=" * 80)

# By default, only WARNING and above are shown
logging.debug("This is a DEBUG message - typically not shown by default")
logging.info("This is an INFO message - also not shown by default")
logging.warning("This is a WARNING message - shown by default")
logging.error("This is an ERROR message - shown by default")
logging.critical("This is a CRITICAL message - shown by default")

"""
IMPORTANT NOTE:
By default, Python only displays WARNING, ERROR, and CRITICAL messages.
DEBUG and INFO messages are ignored unless we change the configuration.
This is because in production, we usually don't want too much detail.
"""

# ============================================================================
# PART 3: CONFIGURING LOGGING LEVEL
# ============================================================================

"""
We can change which messages are displayed using basicConfig().
This function sets up the most basic logging configuration.

IMPORTANT: basicConfig() should be called ONCE at the start of your program.
Calling it multiple times has no effect after the first call!
"""

print("\n" + "=" * 80)
print("EXAMPLE 3: Changing the logging level to show all messages")
print("=" * 80)

# Configure logging to show DEBUG level and above (i.e., everything)
# NOTE: This only works the first time in a program!
logging.basicConfig(level=logging.DEBUG)

# Now let's try all levels again
logging.debug("DEBUG: This message will now appear!")
logging.info("INFO: This message will also appear!")
logging.warning("WARNING: Still appears as before")
logging.error("ERROR: Still appears")
logging.critical("CRITICAL: Still appears")

"""
UNDERSTANDING THE LEVEL PARAMETER:
- level=logging.DEBUG → Shows everything (DEBUG and above)
- level=logging.INFO → Shows INFO, WARNING, ERROR, CRITICAL
- level=logging.WARNING → Shows WARNING, ERROR, CRITICAL (default)
- level=logging.ERROR → Shows only ERROR and CRITICAL
- level=logging.CRITICAL → Shows only CRITICAL

The number in parentheses is the numeric value:
DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50
"""

# ============================================================================
# PART 4: CUSTOMIZING THE LOG FORMAT
# ============================================================================

"""
We can customize what information appears in log messages using the format parameter.
Common format attributes:

%(levelname)s - The logging level (DEBUG, INFO, etc.)
%(message)s - The actual log message
%(asctime)s - Date and time
%(name)s - Logger name
%(filename)s - Source file name
%(lineno)d - Line number where logging call was made
%(funcName)s - Function name

The 's' means string, 'd' means decimal (integer)
"""

print("\n" + "=" * 80)
print("EXAMPLE 4: Custom log format with timestamps")
print("=" * 80)

# Note: In a real program, we'd configure this at the start
# Here we're demonstrating, so we need to use a different logger
custom_logger = logging.getLogger('custom')
custom_logger.setLevel(logging.DEBUG)

# Create a handler (we'll learn more about handlers later)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

# Create a formatter with custom format
formatter = logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)
custom_logger.addHandler(handler)

# Now use the custom logger
custom_logger.debug("Debug with timestamp and custom format")
custom_logger.info("Info with timestamp and custom format")
custom_logger.warning("Warning with timestamp and custom format")

"""
FORMAT STRING BREAKDOWN:
%(asctime)s - Timestamp when log was created
%(levelname)s - Severity level
%(message)s - Your actual message

datefmt parameter controls how the timestamp looks:
%Y - 4-digit year
%m - 2-digit month
%d - 2-digit day
%H - 2-digit hour (24-hour format)
%M - 2-digit minute
%S - 2-digit second
"""

# ============================================================================
# PART 5: PRACTICAL EXAMPLE - A SIMPLE PROGRAM WITH LOGGING
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 5: Practical example - Division calculator with logging")
print("=" * 80)

# Reset logging configuration for this example
app_logger = logging.getLogger('calculator')
app_logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
app_logger.addHandler(console_handler)

def divide_numbers(a, b):
    """
    Divides two numbers with comprehensive logging.
    
    This function demonstrates how logging makes debugging and monitoring easier.
    """
    app_logger.debug(f"divide_numbers() called with a={a}, b={b}")
    
    # Log function entry for debugging
    app_logger.info(f"Attempting to divide {a} by {b}")
    
    # Check for potential issues
    if b == 0:
        app_logger.error("Division by zero attempted!")
        return None
    
    # Perform the operation
    result = a / b
    app_logger.info(f"Division successful: {a} / {b} = {result}")
    app_logger.debug(f"Returning result: {result}")
    
    return result

# Test the function with different inputs
print("\nTest 1: Normal division")
result1 = divide_numbers(10, 2)

print("\nTest 2: Division by zero")
result2 = divide_numbers(10, 0)

print("\nTest 3: Floating point division")
result3 = divide_numbers(7, 3)

"""
OBSERVATIONS:
1. DEBUG messages show detailed information (parameters, return values)
2. INFO messages show major operations (what the program is doing)
3. ERROR messages highlight problems (division by zero)
4. We can trace exactly what happened without print() statements
5. We could easily turn off DEBUG messages in production
"""

# ============================================================================
# PART 6: KEY TAKEAWAYS AND BEST PRACTICES
# ============================================================================

print("\n" + "=" * 80)
print("KEY TAKEAWAYS")
print("=" * 80)

"""
1. ALWAYS use logging instead of print() for any serious Python program
   - print() is fine for learning and quick scripts
   - logging is essential for anything that will run in production

2. Choose appropriate logging levels:
   - DEBUG: Detailed diagnostic information
   - INFO: General informational messages
   - WARNING: Warning about potential issues
   - ERROR: Error occurred, function failed
   - CRITICAL: Severe error, program may crash

3. Configure logging at the START of your program:
   - Use logging.basicConfig() once
   - Set appropriate level for your environment
   - Add custom format if needed

4. Be descriptive in your log messages:
   - BAD: logging.info("Done")
   - GOOD: logging.info("User authentication completed successfully")

5. Include relevant context:
   - BAD: logging.error("Failed")
   - GOOD: logging.error(f"Failed to connect to database at {db_url}")

6. Don't log sensitive information:
   - Never log passwords, API keys, or personal data
   - Be careful with user information

NEXT STEPS:
After mastering these basics, you're ready to learn about:
- More detailed exploration of logging levels (02_logging_levels.py)
- Writing logs to files (03_logging_to_file.py)
- Custom formatting and handlers (04_formatters.py, 05_handlers.py)
"""

# ============================================================================
# STUDENT EXERCISES (See exercise_01_basics.py)
# ============================================================================

"""
SUGGESTED EXERCISES:
1. Write a function that processes a list and logs each step
2. Create a simple calculator with appropriate logging
3. Modify an existing program to use logging instead of print
4. Experiment with different logging levels
5. Create custom format strings with different information

See exercise_01_basics.py for detailed exercises!
"""

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TUTORIAL COMPLETE!")
    print("=" * 80)
    print("\nYou've learned:")
    print("✓ Why logging is better than print()")
    print("✓ The five logging levels")
    print("✓ How to configure basic logging")
    print("✓ How to use custom formats")
    print("✓ Practical application of logging")
    print("\nNext: Study 02_logging_levels.py for deeper understanding!")
```

---

## Exercises

**Exercise 1.**
Replace the `print()` statements in the following code with appropriate logging calls. Use DEBUG for detailed info, INFO for normal operations, and ERROR for failures: `print("Starting process")`, `print(f"Processing item {i}")`, `print("Failed to connect")`.

??? success "Solution to Exercise 1"

    ```python
    import logging

    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
    logger = logging.getLogger(__name__)

    # Instead of print("Starting process")
    logger.info("Starting process")

    # Instead of print(f"Processing item {i}")
    for i in range(3):
        logger.debug(f"Processing item {i}")

    # Instead of print("Failed to connect")
    logger.error("Failed to connect")
    ```

---

**Exercise 2.**
Write a function `setup_basic_logging` that configures `basicConfig` with a custom format showing timestamp, level, and message, and sets the level to DEBUG. Log one message at each of the five standard levels and verify the output.

??? success "Solution to Exercise 2"

    ```python
    import logging

    def setup_basic_logging():
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    setup_basic_logging()

    logging.debug("Debug message")
    logging.info("Info message")
    logging.warning("Warning message")
    logging.error("Error message")
    logging.critical("Critical message")
    ```

---

**Exercise 3.**
Write a simple logging-based calculator that logs each operation at INFO level (e.g., `"Adding 5 + 3 = 8"`) and logs errors (like division by zero) at ERROR level. The calculator should have `add`, `subtract`, `multiply`, and `divide` methods.

??? success "Solution to Exercise 3"

    ```python
    import logging

    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
    logger = logging.getLogger("calculator")

    class Calculator:
        def add(self, a, b):
            result = a + b
            logger.info(f"Adding {a} + {b} = {result}")
            return result

        def subtract(self, a, b):
            result = a - b
            logger.info(f"Subtracting {a} - {b} = {result}")
            return result

        def multiply(self, a, b):
            result = a * b
            logger.info(f"Multiplying {a} * {b} = {result}")
            return result

        def divide(self, a, b):
            if b == 0:
                logger.error(f"Division by zero: {a} / {b}")
                return None
            result = a / b
            logger.info(f"Dividing {a} / {b} = {result}")
            return result

    calc = Calculator()
    calc.add(5, 3)
    calc.divide(10, 0)
    ```
