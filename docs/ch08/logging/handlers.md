# Handlers (Stream, File, Rotating)

Handlers determine where log messages go: console, files, or rotating files.

!!! tip "Mental Model"
    A handler is a delivery truck for log messages — it picks up a formatted log record and drops it at a destination. `StreamHandler` delivers to the console, `FileHandler` to a file, and `RotatingFileHandler` to a file that automatically rolls over when it gets too large. Attach multiple handlers to a single logger and every message goes to all destinations simultaneously.

## Stream Handler (Console)

Log to console with StreamHandler.

```python
import logging

logger = logging.getLogger('console_demo')
logger.setLevel(logging.DEBUG)

# StreamHandler outputs to console
handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("Message to console")
logger.warning("Warning to console")
```

```
INFO - Message to console
WARNING - Warning to console
```

## File Handler

Log to file with FileHandler.

```python
import logging
import tempfile
import os

# Create temporary file
temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.log')
log_path = temp_file.name
temp_file.close()

try:
    logger = logging.getLogger('file_demo')
    logger.setLevel(logging.DEBUG)
    
    handler = logging.FileHandler(log_path)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    logger.info("Message to file")
    
    # Read the log file
    with open(log_path) as f:
        print(f.read())
finally:
    os.unlink(log_path)
```

```
2026-02-12 12:34:56,789 - INFO - Message to file
```

## RotatingFileHandler

Automatically rotate log files by size or time.

```python
import logging
from logging.handlers import RotatingFileHandler
import tempfile
import os

temp_dir = tempfile.mkdtemp()
log_path = os.path.join(temp_dir, 'app.log')

try:
    logger = logging.getLogger('rotating_demo')
    logger.setLevel(logging.DEBUG)
    
    # Max 1KB per file, keep 3 backups
    handler = RotatingFileHandler(
        log_path,
        maxBytes=1024,
        backupCount=3
    )
    
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    for i in range(5):
        logger.info(f"Log message {i}")
    
    print("Rotating file handler created successfully")
finally:
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
```

```
Rotating file handler created successfully
```

---

## Runnable Example: `handlers_tutorial.py`

```python
"""
05_handlers.py - Working with Logging Handlers

LEARNING OBJECTIVES:
- Understand what handlers are and why they're needed
- Use FileHandler, StreamHandler, and other built-in handlers
- Configure multiple handlers for one logger
- Direct different log levels to different destinations

DIFFICULTY: Intermediate
ESTIMATED TIME: 50 minutes
PREREQUISITES: 01-04 files
"""

import logging
import sys
import os

print("=" * 80)
print("Python Logging - Handlers")
print("=" * 80)

# ============================================================================
# PART 1: WHAT ARE HANDLERS?
# ============================================================================

print("\n" + "=" * 80)
print("PART 1: Understanding Handlers")
print("=" * 80)

"""
WHAT IS A HANDLER?

A handler determines WHERE log messages go. Think of handlers as "destinations"
for your log messages.

LOGGING FLOW:
1. You call logger.info("message")
2. Logger determines if message should be logged (based on level)
3. Logger passes message to all attached handlers
4. Each handler decides if it should handle the message (based on handler's level)
5. Handler formats the message (using its formatter)
6. Handler sends the message to its destination

KEY CONCEPTS:
- Loggers can have multiple handlers
- Each handler can have its own level and format
- Handlers are independent - one handler failing doesn't affect others
- Common pattern: console handler for INFO+, file handler for DEBUG+
"""

print("""
Common Handlers:
- StreamHandler: Output to console (stdout/stderr)
- FileHandler: Output to a file
- RotatingFileHandler: Output to file with size-based rotation
- TimedRotatingFileHandler: Output to file with time-based rotation
- SMTPHandler: Send logs via email
- HTTPHandler: Send logs to web server
- SysLogHandler: Send to syslog (Unix)
- NullHandler: Discard all logs (for libraries)
""")

# ============================================================================
# PART 2: StreamHandler - Console Output
# ============================================================================

print("=" * 80)
print("PART 2: StreamHandler - Logging to Console")
print("=" * 80)

"""
StreamHandler sends output to streams (file-like objects).
By default, it uses sys.stderr, but you can specify sys.stdout or any stream.

WHY sys.stderr BY DEFAULT?
- Errors should go to error stream
- Allows separating normal output from logs
- Standard practice in Unix/Linux
"""

# Create a logger
console_logger = logging.getLogger('console_demo')
console_logger.setLevel(logging.DEBUG)

# Create handler for stderr (default)
stderr_handler = logging.StreamHandler()  # Uses sys.stderr by default
stderr_handler.setLevel(logging.WARNING)  # Only WARNING and above
stderr_formatter = logging.Formatter('STDERR | %(levelname)s - %(message)s')
stderr_handler.setFormatter(stderr_formatter)

# Create handler for stdout
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)  # DEBUG and above
stdout_formatter = logging.Formatter('STDOUT | %(levelname)s - %(message)s')
stdout_handler.setFormatter(stdout_formatter)

console_logger.addHandler(stderr_handler)
console_logger.addHandler(stdout_handler)

print("\nLogging to both stdout and stderr:")
print("(Notice DEBUG/INFO go to STDOUT, WARNING+ go to BOTH)\n")

console_logger.debug("Debug message")
console_logger.info("Info message")
console_logger.warning("Warning message")  # Goes to both!
console_logger.error("Error message")       # Goes to both!

"""
OBSERVATION: WARNING and ERROR appear twice!
This is because both handlers accept these levels.
Each handler independently decides whether to handle a message.
"""

# Clean up
console_logger.handlers.clear()

# ============================================================================
# PART 3: FileHandler - Logging to Files
# ============================================================================

print("\n" + "=" * 80)
print("PART 3: FileHandler - Logging to Files")
print("=" * 80)

"""
FileHandler writes logs to a file.

KEY PARAMETERS:
- filename: Path to log file
- mode: 'a' (append) or 'w' (overwrite)
- encoding: Character encoding (usually 'utf-8')
- delay: If True, file opening is deferred until first emit()
"""

# Create logger
file_logger = logging.getLogger('file_demo')
file_logger.setLevel(logging.DEBUG)

# Create file handler
file_handler = logging.FileHandler(
    filename='application.log',
    mode='w',  # Overwrite for this demo
    encoding='utf-8'
)
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(file_formatter)
file_logger.addHandler(file_handler)

# Log some messages
file_logger.debug("Application starting")
file_logger.info("Configuration loaded")
file_logger.warning("Using default settings")
file_logger.error("Failed to connect to database")

print("\nWrote logs to 'application.log'")
print("File contents:\n")
with open('application.log', 'r') as f:
    print(f.read())

# Clean up
file_logger.handlers.clear()
if os.path.exists('application.log'):
    os.remove('application.log')

# ============================================================================
# PART 4: MULTIPLE HANDLERS - Console + File
# ============================================================================

print("=" * 80)
print("PART 4: Multiple Handlers - Console and File")
print("=" * 80)

"""
COMMON PATTERN:
- Console: Show INFO and above (for monitoring)
- File: Show DEBUG and above (for troubleshooting)

This gives you:
- Quick feedback in console
- Detailed logs in file for later analysis
"""

# Create logger
app_logger = logging.getLogger('myapp')
app_logger.setLevel(logging.DEBUG)  # Logger accepts everything

# Console handler - INFO and above
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
console_handler.setFormatter(console_formatter)

# File handler - DEBUG and above
file_handler = logging.FileHandler('debug.log', mode='w')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(
    '%(asctime)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s'
)
file_handler.setFormatter(file_formatter)

# Add both handlers
app_logger.addHandler(console_handler)
app_logger.addHandler(file_handler)

def process_data(data):
    """Example function with logging."""
    app_logger.debug(f"process_data called with {len(data)} items")
    
    for i, item in enumerate(data):
        app_logger.debug(f"Processing item {i}: {item}")
    
    app_logger.info(f"Successfully processed {len(data)} items")
    return True

print("\nProcessing data with dual logging (console + file):")
print("-" * 60)
process_data(['item1', 'item2', 'item3'])

print("\n" + "=" * 60)
print("debug.log contents (more detailed):")
print("=" * 60)
with open('debug.log', 'r') as f:
    print(f.read())

# Clean up
app_logger.handlers.clear()
if os.path.exists('debug.log'):
    os.remove('debug.log')

# ============================================================================
# PART 5: HANDLER LEVELS VS LOGGER LEVELS
# ============================================================================

print("=" * 80)
print("PART 5: Understanding Logger Level vs Handler Level")
print("=" * 80)

"""
TWO-LEVEL FILTERING:

1. LOGGER LEVEL (first filter):
   - If message level < logger level, message is discarded immediately
   - No handlers see it

2. HANDLER LEVEL (second filter):
   - Each handler has its own level
   - If message level >= handler level, handler processes it
   - Different handlers can have different levels

RULE:
A message must pass BOTH the logger level AND the handler level.

EXAMPLE:
- Logger level: DEBUG (10)
- Handler1 level: INFO (20)
- Handler2 level: WARNING (30)

Message levels:
- DEBUG (10): Blocked by logger? NO. Reaches handlers? Handler1: NO, Handler2: NO
- INFO (20): Blocked by logger? NO. Reaches handlers? Handler1: YES, Handler2: NO
- WARNING (30): Blocked by logger? NO. Reaches handlers? Handler1: YES, Handler2: YES
"""

# Demonstrate two-level filtering
filter_logger = logging.getLogger('filter_demo')
filter_logger.setLevel(logging.INFO)  # Logger blocks DEBUG

h1 = logging.StreamHandler()
h1.setLevel(logging.INFO)
h1.setFormatter(logging.Formatter('H1 (INFO+): %(levelname)s - %(message)s'))

h2 = logging.StreamHandler()
h2.setLevel(logging.WARNING)
h2.setFormatter(logging.Formatter('H2 (WARNING+): %(levelname)s - %(message)s'))

filter_logger.addHandler(h1)
filter_logger.addHandler(h2)

print("\nLogger level: INFO, Handler1 level: INFO, Handler2 level: WARNING\n")

filter_logger.debug("Debug message")      # Blocked by logger
filter_logger.info("Info message")        # H1 shows, H2 blocks
filter_logger.warning("Warning message")  # Both show
filter_logger.error("Error message")      # Both show

filter_logger.handlers.clear()

# ============================================================================
# PART 6: SPECIALIZED HANDLERS
# ============================================================================

print("\n" + "=" * 80)
print("PART 6: Other Built-in Handlers")
print("=" * 80)

"""
Python provides many specialized handlers:

1. NullHandler:
   - Discards all log messages
   - Used by libraries to avoid "No handler" warnings
   - Application can add real handlers later

2. SocketHandler:
   - Sends logs over network via TCP
   - Useful for centralized logging

3. DatagramHandler:
   - Sends logs over network via UDP
   - Faster but less reliable than SocketHandler

4. SMTPHandler:
   - Sends logs via email
   - Good for critical errors
   - Don't overuse (email flooding)

5. SysLogHandler:
   - Sends to syslog (Unix/Linux)
   - Integrates with system logging

6. HTTPHandler:
   - POSTs logs to HTTP endpoint
   - Good for cloud logging services

7. QueueHandler (3.2+):
   - Adds logs to queue
   - Another thread/process handles actual logging
   - Prevents logging from blocking application

8. MemoryHandler:
   - Buffers logs in memory
   - Flushes when buffer full or on critical error
   - Good for performance

We'll focus on the most commonly used ones.
"""

# Example: NullHandler (for libraries)
print("\nExample: NullHandler for library code")

lib_logger = logging.getLogger('mylib')
lib_logger.addHandler(logging.NullHandler())  # Prevents "No handlers" warning
lib_logger.info("This goes nowhere - library shouldn't force logging on users")

print("NullHandler discarded the message (no output expected)")

lib_logger.handlers.clear()

# ============================================================================
# PART 7: PRACTICAL EXAMPLE - APPLICATION WITH MULTIPLE HANDLERS
# ============================================================================

print("\n" + "=" * 80)
print("PART 7: Complete Application Example")
print("=" * 80)

"""
Let's build a realistic application logger with:
- Console: INFO and above, simple format
- All logs file: DEBUG and above, detailed format
- Error logs file: ERROR and above, very detailed format
"""

class Application:
    """Example application with comprehensive logging setup."""
    
    def __init__(self, name='MyApp'):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()
        
        # 1. Console handler - INFO+
        console_h = logging.StreamHandler(sys.stdout)
        console_h.setLevel(logging.INFO)
        console_h.setFormatter(logging.Formatter(
            '%(levelname)-8s | %(message)s'
        ))
        self.logger.addHandler(console_h)
        
        # 2. General log file - DEBUG+
        general_h = logging.FileHandler('app.log', mode='w')
        general_h.setLevel(logging.DEBUG)
        general_h.setFormatter(logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        self.logger.addHandler(general_h)
        
        # 3. Error log file - ERROR+
        error_h = logging.FileHandler('errors.log', mode='w')
        error_h.setLevel(logging.ERROR)
        error_h.setFormatter(logging.Formatter(
            '%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(funcName)s() | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        self.logger.addHandler(error_h)
        
        self.logger.info(f"{name} initialized")
    
    def run(self):
        """Simulate application running."""
        self.logger.debug("Starting main application loop")
        self.logger.info("Application is running")
        
        # Simulate some processing
        self.logger.debug("Processing task 1")
        self.logger.info("Task 1 completed")
        
        # Simulate a warning
        self.logger.warning("Database connection slow (3.5s)")
        
        # Simulate an error
        self.logger.error("Failed to save file: permission denied")
        
        # Simulate critical error
        self.logger.critical("Cannot connect to database - shutting down")
        
        self.logger.info("Application shutting down")

print("\nRunning application with multiple handlers:")
print("=" * 60)

app = Application('DemoApp')
app.run()

print("\n" + "=" * 60)
print("Contents of app.log (all levels):")
print("=" * 60)
with open('app.log', 'r') as f:
    print(f.read())

print("=" * 60)
print("Contents of errors.log (ERROR+ only):")
print("=" * 60)
with open('errors.log', 'r') as f:
    print(f.read())

# Clean up
if os.path.exists('app.log'):
    os.remove('app.log')
if os.path.exists('errors.log'):
    os.remove('errors.log')

# ============================================================================
# PART 8: HANDLER BEST PRACTICES
# ============================================================================

print("=" * 80)
print("PART 8: Handler Best Practices")
print("=" * 80)

"""
BEST PRACTICES:

1. ALWAYS ADD FORMATTERS:
   - Handlers without formatters use default (often insufficient)
   - Always explicitly set formatter

2. SET APPROPRIATE LEVELS:
   - Console: INFO or WARNING (not too noisy)
   - File: DEBUG (detailed for troubleshooting)
   - Error file: ERROR (quick access to problems)

3. USE DIFFERENT FORMATS:
   - Console: Simple, readable
   - General file: Detailed but not overwhelming
   - Error file: Very detailed (file, line, function)

4. CLOSE HANDLERS PROPERLY:
   - FileHandlers should be closed when done
   - Use try/finally or context managers
   - Important for file locking issues

5. AVOID DUPLICATE MESSAGES:
   - Don't add handlers repeatedly
   - Clear handlers before reconfiguring
   - Use propagate=False carefully (covered later)

6. CONSIDER PERFORMANCE:
   - File I/O can be slow
   - Use QueueHandler for high-throughput apps
   - Consider async logging for real-time apps

7. HANDLER PER PURPOSE:
   - Separate handlers for separate concerns
   - Don't try to do everything with one handler
   - Examples: audit log, access log, error log, debug log

COMMON PITFALLS:

1. Adding handlers multiple times:
   # BAD
   def setup_logging():
       logger.addHandler(handler)  # Called multiple times = duplicate logs!
   
   # GOOD
   def setup_logging():
       logger.handlers.clear()  # Clear first
       logger.addHandler(handler)

2. Not setting formatter:
   # BAD
   handler = logging.FileHandler('app.log')
   logger.addHandler(handler)  # Uses default format
   
   # GOOD
   handler = logging.FileHandler('app.log')
   handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
   logger.addHandler(handler)

3. Wrong level on logger:
   # BAD
   logger.setLevel(logging.WARNING)  # Blocks DEBUG and INFO completely!
   handler.setLevel(logging.DEBUG)   # Handler never sees DEBUG/INFO
   
   # GOOD
   logger.setLevel(logging.DEBUG)    # Logger lets everything through
   handler.setLevel(logging.WARNING) # Handler filters

"""

# ============================================================================
# PART 9: KEY TAKEAWAYS
# ============================================================================

print("\n" + "=" * 80)
print("KEY TAKEAWAYS")
print("=" * 80)

"""
1. WHAT ARE HANDLERS:
   - Determine WHERE logs go
   - Logger can have multiple handlers
   - Each handler is independent

2. COMMON HANDLERS:
   - StreamHandler: Console output
   - FileHandler: File output
   - RotatingFileHandler: Size-based rotation (covered later)
   - TimedRotatingFileHandler: Time-based rotation (covered later)

3. TWO-LEVEL FILTERING:
   - Message must pass logger level
   - Then must pass each handler's level
   - Both filters must pass for output

4. TYPICAL SETUP:
   - Console: INFO+, simple format
   - General file: DEBUG+, detailed format
   - Error file: ERROR+, very detailed format

5. BEST PRACTICES:
   - Always set formatter explicitly
   - Set appropriate levels
   - Clear handlers before reconfiguring
   - Close file handlers when done
   - One handler per purpose

6. NEXT TOPICS:
   - Logger hierarchy (06_logger_hierarchy.py)
   - Configuration methods (07_configuration_methods.py)
   - Rotating file handlers (08_rotating_logs.py)

"""

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TUTORIAL COMPLETE!")
    print("=" * 80)
    print("\nYou now understand:")
    print("✓ What handlers are and why they're needed")
    print("✓ StreamHandler and FileHandler")
    print("✓ Multiple handlers for one logger")
    print("✓ Logger level vs handler level")
    print("✓ Handler best practices")
    print("\nNext: Study 06_logger_hierarchy.py to understand logger organization!")
```

---

## Exercises

**Exercise 1.**
Configure a logger with two handlers: a `StreamHandler` that only shows WARNING and above, and a second `StreamHandler` (simulating a file) that shows all messages from DEBUG and above. Demonstrate that a DEBUG message appears in the second handler but not the first.

??? success "Solution to Exercise 1"

    ```python
    import logging

    logger = logging.getLogger("dual_handler")
    logger.setLevel(logging.DEBUG)

    # Console handler: WARNING+
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    console.setFormatter(logging.Formatter("CONSOLE: %(levelname)s - %(message)s"))

    # "File" handler: DEBUG+
    file_sim = logging.StreamHandler()
    file_sim.setLevel(logging.DEBUG)
    file_sim.setFormatter(logging.Formatter("FILE: %(levelname)s - %(message)s"))

    logger.addHandler(console)
    logger.addHandler(file_sim)

    logger.debug("Debug detail")    # Only in file_sim
    logger.warning("Important!")     # In both
    ```

---

**Exercise 2.**
Write a function `create_rotating_logger` that sets up a `RotatingFileHandler` with configurable `maxBytes` and `backupCount`. Return the logger. Include comments explaining when rotation occurs.

??? success "Solution to Exercise 2"

    ```python
    import logging
    from logging.handlers import RotatingFileHandler

    def create_rotating_logger(name, filename, max_bytes=5000, backup_count=3):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        # Rotation: when file exceeds max_bytes, it is renamed
        # to filename.1, and a new file is created. Up to
        # backup_count old files are kept.
        handler = RotatingFileHandler(
            filename, maxBytes=max_bytes, backupCount=backup_count
        )
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)
        return logger

    # Usage:
    # logger = create_rotating_logger("myapp", "app.log")
    ```

---

**Exercise 3.**
Write a function `add_handler_safely` that adds a handler to a logger only if a handler of the same type is not already attached (to prevent duplicate handlers). Test by calling it twice and verifying only one handler is added.

??? success "Solution to Exercise 3"

    ```python
    import logging

    def add_handler_safely(logger, handler):
        handler_type = type(handler)
        for existing in logger.handlers:
            if isinstance(existing, handler_type):
                return  # Already has this type
        logger.addHandler(handler)

    # Test
    logger = logging.getLogger("safe_logger")
    logger.setLevel(logging.DEBUG)

    h1 = logging.StreamHandler()
    h2 = logging.StreamHandler()

    add_handler_safely(logger, h1)
    add_handler_safely(logger, h2)  # Skipped
    print(f"Handler count: {len(logger.handlers)}")  # 1
    ```
