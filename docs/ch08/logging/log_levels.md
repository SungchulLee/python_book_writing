# Log Levels

Understanding log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) and when to use each.

!!! tip "Mental Model"
    Log levels are a volume knob. DEBUG is the loudest (everything), CRITICAL is the quietest (only catastrophes). Setting a logger to WARNING silences everything below it — DEBUG and INFO vanish. In development you crank it to DEBUG; in production you set it to WARNING or ERROR so only actionable events get recorded.

## Log Level Hierarchy

Log levels control which messages are recorded.

```python
import logging

logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s: %(message)s'
)

logging.debug("Debug: detailed info")
logging.info("Info: confirmation")
logging.warning("Warning: something unexpected")
logging.error("Error: something failed")
logging.critical("Critical: serious problem")
```

```
WARNING: something unexpected
ERROR: something failed
CRITICAL: serious problem
```

## Level Values

Each level has a numeric value controlling filtering.

```python
import logging

levels = [
    (logging.DEBUG, "DEBUG"),
    (logging.INFO, "INFO"),
    (logging.WARNING, "WARNING"),
    (logging.ERROR, "ERROR"),
    (logging.CRITICAL, "CRITICAL")
]

for value, name in levels:
    print(f"{name}: {value}")
```

```
DEBUG: 10
INFO: 20
WARNING: 30
ERROR: 40
CRITICAL: 50
```

---

## Runnable Example: `logging_levels_tutorial.py`

```python
"""
02_logging_levels.py - Deep Dive into Logging Levels

LEARNING OBJECTIVES:
- Understand each logging level in detail
- Learn when to use each level appropriately
- Master level hierarchy and filtering
- Implement level-based conditional logic

DIFFICULTY: Beginner
ESTIMATED TIME: 45 minutes
PREREQUISITES: 01_basic_logging.py
"""

import logging
import sys

# Configure logging for this tutorial
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)-8s - %(message)s'
)

# ============================================================================
# PART 1: LOGGING LEVEL HIERARCHY IN DEPTH
# ============================================================================

print("=" * 80)
print("PART 1: Understanding the Logging Level Hierarchy")
print("=" * 80)

"""
NUMERIC VALUES OF LOGGING LEVELS:
Each logging level has a numeric value. This determines which messages get displayed.
When you set a logging level, all messages at that level AND HIGHER are shown.

Level Name    | Numeric Value | Typical Use Case
--------------|---------------|------------------------------------------
NOTSET        | 0            | Special value meaning "inherit from parent"
DEBUG         | 10           | Detailed diagnostic information
INFO          | 20           | Confirmation messages
WARNING       | 30           | Warning about potential issues
ERROR         | 40           | Error occurred, operation failed
CRITICAL      | 50           | Severe error, program may crash

HIERARCHY RULE:
If you set level to INFO (20), you get:
- INFO (20) ✓
- WARNING (30) ✓
- ERROR (40) ✓
- CRITICAL (50) ✓
- DEBUG (10) ✗ (because 10 < 20)
"""

print("\nNumeric values of logging levels:")
print(f"DEBUG: {logging.DEBUG}")
print(f"INFO: {logging.INFO}")
print(f"WARNING: {logging.WARNING}")
print(f"ERROR: {logging.ERROR}")
print(f"CRITICAL: {logging.CRITICAL}")

# ============================================================================
# PART 2: DEBUG LEVEL - Detailed Diagnostic Information
# ============================================================================

print("\n" + "=" * 80)
print("PART 2: DEBUG Level - For Developers During Development")
print("=" * 80)

"""
DEBUG LEVEL (10):
Purpose: Detailed information for diagnosing problems
When to use:
- Tracking variable values during execution
- Understanding program flow
- Debugging complex logic
- Tracing function calls and returns
- Monitoring loop iterations

When NOT to use:
- Never in production (performance impact)
- For messages users should see
- For important business events

Rule of thumb: If you're tempted to use print() for debugging, use DEBUG logging instead.
"""

def calculate_fibonacci(n):
    """
    Calculate the nth Fibonacci number with DEBUG logging.
    Demonstrates detailed diagnostic information.
    """
    logging.debug(f"calculate_fibonacci() called with n={n}")
    
    if n < 0:
        logging.debug(f"Invalid input: n={n} is negative")
        return None
    
    if n <= 1:
        logging.debug(f"Base case reached: n={n}, returning {n}")
        return n
    
    logging.debug(f"Calculating fibonacci for n={n}")
    fib_prev2 = 0
    fib_prev1 = 1
    
    for i in range(2, n + 1):
        fib_current = fib_prev1 + fib_prev2
        logging.debug(f"  Iteration {i}: fib[{i}] = {fib_current}")
        fib_prev2 = fib_prev1
        fib_prev1 = fib_current
    
    result = fib_prev1
    logging.debug(f"Final result for fib({n}) = {result}")
    return result

print("\nExample: Fibonacci with DEBUG logging")
result = calculate_fibonacci(7)
print(f"Fibonacci(7) = {result}")

"""
NOTICE: DEBUG messages give us a complete trace of what happened.
This is invaluable during development but too verbose for production.
"""

# ============================================================================
# PART 3: INFO LEVEL - Confirmation Messages
# ============================================================================

print("\n" + "=" * 80)
print("PART 3: INFO Level - Confirming Normal Operation")
print("=" * 80)

"""
INFO LEVEL (20):
Purpose: Confirm that things are working as expected
When to use:
- Program startup and shutdown
- Major milestones or phase completions
- Successful completion of important operations
- Configuration information
- Connection establishment/termination

When NOT to use:
- For every function call (too verbose)
- For detailed debugging information
- For errors or warnings

Rule of thumb: INFO messages should tell the story of what your program is doing.
"""

class DataProcessor:
    """
    Example class demonstrating INFO level logging.
    """
    
    def __init__(self, name):
        self.name = name
        logging.info(f"DataProcessor '{name}' initialized")
    
    def load_data(self, filename):
        """Simulate loading data from a file."""
        logging.info(f"Loading data from '{filename}'")
        # Simulate loading (in real code, this would read from file)
        data = [1, 2, 3, 4, 5]
        logging.info(f"Successfully loaded {len(data)} records from '{filename}'")
        return data
    
    def process_data(self, data):
        """Simulate processing data."""
        logging.info(f"Starting data processing on {len(data)} records")
        # Simulate processing
        processed = [x * 2 for x in data]
        logging.info(f"Data processing complete. Processed {len(processed)} records")
        return processed
    
    def save_data(self, data, filename):
        """Simulate saving data to a file."""
        logging.info(f"Saving {len(data)} records to '{filename}'")
        # Simulate saving (in real code, this would write to file)
        logging.info(f"Successfully saved data to '{filename}'")

print("\nExample: Data processing pipeline with INFO logging")
processor = DataProcessor("StudentGradeProcessor")
data = processor.load_data("grades.csv")
processed_data = processor.process_data(data)
processor.save_data(processed_data, "processed_grades.csv")

"""
NOTICE: INFO messages provide a clear narrative of what the program is doing,
without overwhelming detail. This is perfect for monitoring production systems.
"""

# ============================================================================
# PART 4: WARNING LEVEL - Potential Issues
# ============================================================================

print("\n" + "=" * 80)
print("PART 4: WARNING Level - Something Unexpected But Not Critical")
print("=" * 80)

"""
WARNING LEVEL (30):
Purpose: Indicate something unexpected happened, but program continues
When to use:
- Deprecated features being used
- Unusual but handled situations
- Resource constraints (but not critical)
- Configuration issues that have defaults
- Potential problems that don't stop execution

When NOT to use:
- For actual errors that cause operation failure
- For normal but important events (use INFO)
- For critical situations

Rule of thumb: Use WARNING when something is wrong but the program can continue.
"""

def process_user_age(age):
    """
    Process user age with appropriate warnings.
    """
    logging.debug(f"process_user_age() called with age={age}")
    
    # Check for unrealistic ages
    if age < 0:
        logging.warning(f"Negative age provided: {age}. Using absolute value.")
        age = abs(age)
    
    if age > 120:
        logging.warning(f"Unusually high age: {age}. This may be a data entry error.")
    
    if age < 13:
        logging.warning(f"User age is {age}. May need parental consent.")
    
    logging.info(f"Processing age: {age}")
    return age

def load_configuration(config_dict):
    """
    Load configuration with default values and warnings.
    """
    default_timeout = 30
    default_retries = 3
    
    timeout = config_dict.get('timeout')
    if timeout is None:
        logging.warning(f"'timeout' not specified in config. Using default: {default_timeout}s")
        timeout = default_timeout
    
    retries = config_dict.get('retries')
    if retries is None:
        logging.warning(f"'retries' not specified in config. Using default: {default_retries}")
        retries = default_retries
    
    logging.info(f"Configuration loaded: timeout={timeout}s, retries={retries}")
    return {'timeout': timeout, 'retries': retries}

print("\nExample 1: Processing unusual ages")
process_user_age(150)
process_user_age(-5)
process_user_age(10)

print("\nExample 2: Loading incomplete configuration")
config = load_configuration({'timeout': 60})  # Missing 'retries'

"""
NOTICE: WARNING messages alert us to issues, but the program continues.
These should be reviewed but don't necessarily require immediate action.
"""

# ============================================================================
# PART 5: ERROR LEVEL - Operation Failed
# ============================================================================

print("\n" + "=" * 80)
print("PART 5: ERROR Level - Something Failed")
print("=" * 80)

"""
ERROR LEVEL (40):
Purpose: A serious problem occurred; an operation failed
When to use:
- Exceptions and errors
- Failed operations
- Data validation failures
- Connection failures
- File I/O errors
- Any situation where a requested operation could not be completed

When NOT to use:
- For warnings that don't prevent operation
- For critical system failures (use CRITICAL)
- For expected conditions

Rule of thumb: Use ERROR when an operation failed but the program can continue.
"""

def divide_safely(a, b):
    """
    Perform division with proper error logging.
    """
    logging.debug(f"divide_safely({a}, {b}) called")
    
    try:
        result = a / b
        logging.info(f"Division successful: {a} / {b} = {result}")
        return result
    except ZeroDivisionError:
        logging.error(f"Division by zero: attempted to divide {a} by {b}")
        return None
    except TypeError as e:
        logging.error(f"Type error in division: {e}")
        return None

def read_file_safely(filename):
    """
    Attempt to read a file with error handling.
    """
    logging.info(f"Attempting to read file: {filename}")
    
    try:
        with open(filename, 'r') as f:
            content = f.read()
        logging.info(f"Successfully read {len(content)} characters from {filename}")
        return content
    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
        return None
    except PermissionError:
        logging.error(f"Permission denied when reading: {filename}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error reading {filename}: {e}")
        return None

print("\nExample 1: Division errors")
divide_safely(10, 2)
divide_safely(10, 0)
divide_safely("10", 2)

print("\nExample 2: File reading errors")
read_file_safely("nonexistent_file.txt")

"""
NOTICE: ERROR messages clearly indicate operation failures.
The program continues but the specific operation could not complete.
"""

# ============================================================================
# PART 6: CRITICAL LEVEL - Severe System Errors
# ============================================================================

print("\n" + "=" * 80)
print("PART 6: CRITICAL Level - Severe Problems")
print("=" * 80)

"""
CRITICAL LEVEL (50):
Purpose: A very serious error; the program may not be able to continue
When to use:
- System crashes
- Data corruption
- Critical resource exhaustion
- Security breaches
- Situations requiring immediate attention
- Program must shut down

When NOT to use:
- For regular errors (use ERROR)
- For expected failures
- For anything that doesn't threaten program stability

Rule of thumb: Use CRITICAL for catastrophic failures.
"""

def initialize_critical_system():
    """
    Initialize a critical system component.
    """
    database_connected = False  # Simulate failure
    cache_connected = False  # Simulate failure
    
    if not database_connected:
        logging.critical("CRITICAL: Cannot connect to database! Application cannot start.")
        logging.critical("Check database server status and connection settings.")
        # In real code, you might sys.exit(1) here
    
    if not cache_connected:
        logging.critical("CRITICAL: Cannot connect to cache server! Performance will be severely degraded.")

def check_disk_space():
    """
    Check for critical disk space issues.
    """
    # Simulate checking disk space
    available_space_gb = 0.5  # Less than 1 GB
    
    if available_space_gb < 1:
        logging.critical(f"CRITICAL: Disk space critically low! Only {available_space_gb}GB remaining.")
        logging.critical("Immediate action required: Free up disk space or add storage.")

print("\nExample 1: Critical system initialization failure")
initialize_critical_system()

print("\nExample 2: Critical resource exhaustion")
check_disk_space()

"""
NOTICE: CRITICAL messages indicate severe problems requiring immediate action.
These should trigger alerts and may require program shutdown.
"""

# ============================================================================
# PART 7: CHOOSING THE RIGHT LEVEL - Decision Tree
# ============================================================================

print("\n" + "=" * 80)
print("PART 7: Decision Tree for Choosing Logging Level")
print("=" * 80)

"""
DECISION TREE:

1. Is this for detailed debugging information?
   └─YES→ Use DEBUG
   └─NO→ Go to 2

2. Did something fail or go wrong?
   └─YES→ Go to 3
   └─NO→ Go to 4

3. How severe is the problem?
   └─Program must shut down→ Use CRITICAL
   └─Operation failed but program continues→ Use ERROR
   └─Unexpected but handled→ Use WARNING

4. Is this a normal, successful operation?
   └─YES→ Use INFO
   └─NO→ Use DEBUG

EXAMPLES WITH DECISION TREE:

Situation: "User logged in successfully"
- Nothing failed → Not ERROR/CRITICAL
- Normal operation → INFO

Situation: "Variable x = 42 in loop iteration 7"
- Detailed debugging info → DEBUG

Situation: "Configuration file has typo, using default value"
- Something wrong but handled → WARNING

Situation: "Failed to send email notification"
- Operation failed → ERROR

Situation: "Out of memory, application crashing"
- Program must shut down → CRITICAL
"""

def demonstrate_level_choices(scenario):
    """
    Demonstrate appropriate logging level for different scenarios.
    """
    scenarios = {
        'user_login': lambda: logging.info("User 'john_doe' logged in successfully"),
        'loop_variable': lambda: logging.debug("Loop iteration 5: processing item 'data.txt'"),
        'missing_config': lambda: logging.warning("Config key 'max_retries' not found, using default value 3"),
        'email_fail': lambda: logging.error("Failed to send notification email to admin@example.com"),
        'memory_critical': lambda: logging.critical("Out of memory! Cannot allocate buffer. Shutting down."),
    }
    
    if scenario in scenarios:
        print(f"\nScenario: {scenario}")
        scenarios[scenario]()

print("\nDemonstrating appropriate level choices:")
demonstrate_level_choices('user_login')
demonstrate_level_choices('loop_variable')
demonstrate_level_choices('missing_config')
demonstrate_level_choices('email_fail')
demonstrate_level_choices('memory_critical')

# ============================================================================
# PART 8: LEVEL FILTERING IN PRACTICE
# ============================================================================

print("\n" + "=" * 80)
print("PART 8: Practical Level Filtering")
print("=" * 80)

"""
In production, you typically set different logging levels for different environments:

DEVELOPMENT:
- Level: DEBUG
- Rationale: See everything for debugging

STAGING/TESTING:
- Level: INFO
- Rationale: Monitor operations without excessive detail

PRODUCTION:
- Level: WARNING
- Rationale: Only see issues and errors, minimize performance impact

TROUBLESHOOTING:
- Level: DEBUG (temporarily)
- Rationale: Diagnose production issues
"""

def simulate_environment_logging(environment):
    """
    Demonstrate logging at different environment levels.
    """
    # Create a logger for this environment
    env_logger = logging.getLogger(f'app.{environment}')
    
    # Set level based on environment
    if environment == 'development':
        env_logger.setLevel(logging.DEBUG)
    elif environment == 'staging':
        env_logger.setLevel(logging.INFO)
    elif environment == 'production':
        env_logger.setLevel(logging.WARNING)
    
    # Add handler
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(f'[{environment.upper()}] %(levelname)s - %(message)s'))
    env_logger.addHandler(handler)
    
    # Log at all levels
    print(f"\nLogging in {environment.upper()} environment:")
    env_logger.debug("Debug: Variable inspection")
    env_logger.info("Info: Request processed")
    env_logger.warning("Warning: Slow query detected")
    env_logger.error("Error: Database connection failed")
    
    # Clean up
    env_logger.handlers.clear()

simulate_environment_logging('development')
simulate_environment_logging('staging')
simulate_environment_logging('production')

"""
NOTICE: Different environments show different amounts of information.
This is controlled by the logging level without changing any code!
"""

# ============================================================================
# PART 9: CHECKING LOGGING LEVEL PROGRAMMATICALLY
# ============================================================================

print("\n" + "=" * 80)
print("PART 9: Conditional Logging Based on Level")
print("=" * 80)

"""
Sometimes you want to avoid expensive operations if logging won't output them.
You can check if a level is enabled before doing expensive work.
"""

def expensive_debug_operation():
    """
    Simulate an expensive operation (like formatting large data structures).
    """
    # Imagine this takes time: generating a detailed report
    return "Very detailed debug information that took time to generate"

def smart_logging_example():
    """
    Demonstrate checking if logging level is enabled.
    """
    logger = logging.getLogger('performance')
    logger.setLevel(logging.INFO)  # DEBUG won't be shown
    
    # BAD: Always does expensive work, even if DEBUG is disabled
    logger.debug(expensive_debug_operation())  # Work is done even though message won't show
    
    # GOOD: Only do expensive work if DEBUG is enabled
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(expensive_debug_operation())
    else:
        print("Skipped expensive debug operation because DEBUG level is not enabled")

smart_logging_example()

"""
PERFORMANCE TIP:
For expensive string formatting or calculations in DEBUG messages,
always check if the level is enabled first using isEnabledFor().
"""

# ============================================================================
# PART 10: KEY TAKEAWAYS
# ============================================================================

print("\n" + "=" * 80)
print("KEY TAKEAWAYS")
print("=" * 80)

"""
1. LOGGING LEVEL HIERARCHY:
   DEBUG < INFO < WARNING < ERROR < CRITICAL
   Setting a level shows that level and everything above it

2. LEVEL USAGE GUIDELINES:
   DEBUG: Detailed diagnostic (development only)
   INFO: Normal operations (production monitoring)
   WARNING: Unexpected but handled (review periodically)
   ERROR: Operation failed (needs attention)
   CRITICAL: Severe failure (immediate action required)

3. ENVIRONMENT-SPECIFIC LEVELS:
   Development: DEBUG
   Staging: INFO
   Production: WARNING

4. PERFORMANCE CONSIDERATION:
   Use isEnabledFor() before expensive operations in DEBUG/INFO messages

5. CONSISTENCY:
   Be consistent in your team about when to use each level
   Document your logging standards

NEXT STEPS:
- Learn about logging to files (03_logging_to_file.py)
- Explore custom formatting (04_formatters.py)
- Study handlers for different outputs (05_handlers.py)
"""

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TUTORIAL COMPLETE!")
    print("=" * 80)
    print("\nYou now understand:")
    print("✓ All five logging levels in depth")
    print("✓ When to use each level")
    print("✓ Level hierarchy and filtering")
    print("✓ Environment-specific logging")
    print("✓ Performance considerations")
    print("\nNext: Study 03_logging_to_file.py to learn about file logging!")
```

---

## Exercises

**Exercise 1.**
Write a function `log_at_level` that takes a logger, a level name string (e.g., `"DEBUG"`, `"INFO"`), and a message, and logs the message at the specified level. Use `getattr` to dynamically call the correct logging method. Test with all five standard levels.

??? success "Solution to Exercise 1"

    ```python
    import logging

    def log_at_level(logger, level_name, message):
        level_method = getattr(logger, level_name.lower())
        level_method(message)

    # Test
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
    logger = logging.getLogger("level_test")

    for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        log_at_level(logger, level, f"Message at {level}")
    ```

---

**Exercise 2.**
Write a function `count_log_levels` that takes a list of log record level names and returns a dictionary counting how many of each level appear. For example, `count_log_levels(["INFO", "DEBUG", "INFO", "ERROR"])` should return `{"INFO": 2, "DEBUG": 1, "ERROR": 1}`.

??? success "Solution to Exercise 2"

    ```python
    from collections import Counter

    def count_log_levels(levels):
        return dict(Counter(levels))

    # Test
    levels = ["INFO", "DEBUG", "INFO", "ERROR", "INFO", "DEBUG"]
    print(count_log_levels(levels))
    # {'INFO': 3, 'DEBUG': 2, 'ERROR': 1}
    ```

---

**Exercise 3.**
Write a function `filter_by_level` that takes a list of `(level, message)` tuples and a minimum level string, and returns only the messages at or above that level. Use the numeric level values from `logging.getLevelName()`. For example, filtering `[("DEBUG", "d"), ("INFO", "i"), ("ERROR", "e")]` with minimum `"INFO"` should return `[("INFO", "i"), ("ERROR", "e")]`.

??? success "Solution to Exercise 3"

    ```python
    import logging

    def filter_by_level(records, min_level):
        min_numeric = logging.getLevelName(min_level)
        return [
            (level, msg)
            for level, msg in records
            if logging.getLevelName(level) >= min_numeric
        ]

    # Test
    records = [("DEBUG", "d"), ("INFO", "i"), ("WARNING", "w"), ("ERROR", "e")]
    print(filter_by_level(records, "INFO"))
    # [('INFO', 'i'), ('WARNING', 'w'), ('ERROR', 'e')]
    ```
