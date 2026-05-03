# Formatters

Formatters control the output format of log messages with customizable fields and styles.

!!! tip "Mental Model"
    A formatter is a template string for log lines. It decides which fields appear (timestamp, logger name, level, message) and in what order. Every handler has exactly one formatter, and changing it instantly reshapes all output going through that handler without touching any log calls in your code.

## Common Format Codes

Use format codes to customize log output.

```python
import logging

# Create logger with different formatters
logger = logging.getLogger('format_demo')
logger.setLevel(logging.DEBUG)
logger.handlers.clear()

handler = logging.StreamHandler()

# Format with various codes
formats = [
    '%(message)s',
    '%(levelname)s - %(message)s',
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    '[%(filename)s:%(lineno)d] %(levelname)s: %(message)s'
]

for fmt_str in formats:
    formatter = logging.Formatter(fmt_str)
    handler.setFormatter(formatter)
    logger.handlers = [handler]
    logger.info("Test message")
    print()
```

```
Test message

INFO - Test message

2026-02-12 12:34:56,789 - format_demo - INFO - Test message

[logging_demo.py:15] INFO: Test message
```

## Custom Attributes

Add custom attributes to log records.

```python
import logging

class ContextFilter(logging.Filter):
    def filter(self, record):
        record.user_id = 123
        record.request_id = 'req-456'
        return True

logger = logging.getLogger('context_demo')
logger.setLevel(logging.DEBUG)
logger.handlers.clear()

handler = logging.StreamHandler()
formatter = logging.Formatter(
    '[%(user_id)s:%(request_id)s] %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
handler.addFilter(ContextFilter())
logger.addHandler(handler)

logger.info("Processing request")
```

```
[123:req-456] INFO - Processing request
```

---

## Runnable Example: `formatters_tutorial.py`

```python
"""
04_formatters.py - Customizing Log Message Format

LEARNING OBJECTIVES:
- Understand LogRecord attributes
- Create custom format strings
- Format timestamps effectively
- Design readable log outputs

DIFFICULTY: Intermediate
ESTIMATED TIME: 45 minutes
PREREQUISITES: 01-03 basic files
"""

import logging
import sys
from datetime import datetime

print("=" * 80)
print("Python Logging - Custom Formatters")
print("=" * 80)

# ============================================================================
# PART 1: UNDERSTANDING LogRecord ATTRIBUTES
# ============================================================================

print("\n" + "=" * 80)
print("PART 1: Available LogRecord Attributes")
print("=" * 80)

"""
When you log a message, Python creates a LogRecord object with many attributes.
These attributes can be used in format strings with %(attribute)s syntax.

COMMONLY USED ATTRIBUTES:

%(asctime)s       - Human-readable time when LogRecord was created
%(created)f       - Time when LogRecord was created (Unix timestamp)
%(filename)s      - Filename portion of pathname
%(funcName)s      - Name of function containing the logging call
%(levelname)s     - Text logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
%(levelno)s       - Numeric logging level (10, 20, 30, 40, 50)
%(lineno)d        - Source line number where logging call was issued
%(message)s       - The logged message (after merging arguments)
%(module)s        - Module name (filename without extension)
%(name)s          - Name of the logger used to log the call
%(pathname)s      - Full pathname of the source file
$(process)d       - Process ID
%(processName)s   - Process name
%(thread)d        - Thread ID
%(threadName)s    - Thread name
%(msecs)d         - Millisecond portion of creation time
%(relativeCreated)d - Time in milliseconds since logging module was loaded

FORMAT SPECIFIERS:
- 's' = string
- 'd' = integer
- 'f' = float
"""

# Demonstrate all attributes
logger = logging.getLogger('demo.formatter')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()

# Create a comprehensive format showing many attributes
comprehensive_format = (
    '%(asctime)s | '
    '%(name)s | '
    '%(levelname)-8s | '
    '%(filename)s:%(lineno)d | '
    '%(funcName)s() | '
    '%(message)s'
)

formatter = logging.Formatter(comprehensive_format)
handler.setFormatter(formatter)
logger.addHandler(handler)

def example_function():
    """Demonstrate logging with full context."""
    logger.info("This message shows all the format attributes")
    logger.warning("Notice how each attribute provides context")

example_function()

"""
EXPLANATION OF OUTPUT:
- asctime: When the log was created
- name: Logger name (hierarchical)
- levelname: Severity level (padded to 8 chars for alignment)
- filename:lineno: Exact location in code
- funcName: Which function logged the message
- message: The actual message
"""

# ============================================================================
# PART 2: BASIC FORMAT PATTERNS
# ============================================================================

print("\n" + "=" * 80)
print("PART 2: Common Format Patterns")
print("=" * 80)

"""
Let's look at common format patterns for different use cases.
"""

def demonstrate_format(name, format_string, datefmt=None):
    """Helper function to demonstrate different formats."""
    print(f"\n{name}:")
    print("-" * 60)
    
    test_logger = logging.getLogger(f'format_test.{name}')
    test_logger.setLevel(logging.DEBUG)
    test_logger.handlers.clear()
    
    handler = logging.StreamHandler()
    formatter = logging.Formatter(format_string, datefmt=datefmt)
    handler.setFormatter(formatter)
    test_logger.addHandler(handler)
    
    test_logger.debug("Debug message")
    test_logger.info("Info message")
    test_logger.warning("Warning message")
    test_logger.error("Error message")

# Pattern 1: Minimal (for development)
demonstrate_format(
    "Minimal Format",
    '%(levelname)s - %(message)s'
)

# Pattern 2: Standard (for production)
demonstrate_format(
    "Standard Format",
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Pattern 3: Detailed (for debugging)
demonstrate_format(
    "Detailed Format",
    '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s'
)

# Pattern 4: JSON-like (for parsing)
demonstrate_format(
    "Structured Format",
    'time=%(asctime)s level=%(levelname)s module=%(module)s message=%(message)s'
)

"""
CHOOSING A FORMAT:

Development:
- Simple format is fine
- Focus on message content
- Example: '%(levelname)s - %(message)s'

Production:
- Include timestamp
- Include logger name
- Include level
- Example: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

Debugging:
- Include file location
- Include function name
- Include line number
- Example: '%(asctime)s | %(filename)s:%(lineno)d:%(funcName)s | %(levelname)s | %(message)s'

Log Aggregation:
- Structured format
- Easy to parse
- Consistent separators
- Example: 'timestamp=%(asctime)s level=%(levelname)s message=%(message)s'
"""

# ============================================================================
# PART 3: TIMESTAMP FORMATTING
# ============================================================================

print("\n" + "=" * 80)
print("PART 3: Customizing Timestamp Formats")
print("=" * 80)

"""
The datefmt parameter controls how %(asctime)s is formatted.
It uses the same format codes as datetime.strftime().

COMMON DATE/TIME FORMAT CODES:
%Y - 4-digit year (2024)
%m - 2-digit month (01-12)
%d - 2-digit day (01-31)
%H - Hour in 24-hour format (00-23)
%M - Minute (00-59)
%S - Second (00-59)
%I - Hour in 12-hour format (01-12)
%p - AM/PM
%b - Abbreviated month name (Jan, Feb, etc.)
%B - Full month name (January, February, etc.)
%a - Abbreviated weekday (Mon, Tue, etc.)
%A - Full weekday (Monday, Tuesday, etc.)
%f - Microsecond (000000-999999)
%z - UTC offset (+0000)
%Z - Timezone name
"""

def demo_timestamp_format(description, datefmt):
    """Demonstrate different timestamp formats."""
    print(f"\n{description}: {datefmt}")
    
    ts_logger = logging.getLogger(f'timestamp.{description}')
    ts_logger.setLevel(logging.INFO)
    ts_logger.handlers.clear()
    
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(message)s',
        datefmt=datefmt
    )
    handler.setFormatter(formatter)
    ts_logger.addHandler(handler)
    
    ts_logger.info("Sample message")

# Different timestamp formats
demo_timestamp_format("ISO 8601", '%Y-%m-%dT%H:%M:%S')
demo_timestamp_format("US Format", '%m/%d/%Y %I:%M:%S %p')
demo_timestamp_format("European", '%d-%m-%Y %H:%M:%S')
demo_timestamp_format("Readable", '%B %d, %Y at %I:%M:%S %p')
demo_timestamp_format("With Weekday", '%A, %Y-%m-%d %H:%M:%S')
demo_timestamp_format("With Milliseconds", '%Y-%m-%d %H:%M:%S.%f')

"""
BEST PRACTICES:
- Use ISO 8601 (%Y-%m-%dT%H:%M:%S) for logs that might be parsed internationally
- Include seconds for debugging
- Consider milliseconds for high-frequency logging
- Be consistent across your application
"""

# ============================================================================
# PART 4: ALIGNMENT AND PADDING
# ============================================================================

print("\n" + "=" * 80)
print("PART 4: Aligning and Padding Fields")
print("=" * 80)

"""
You can control field width and alignment using format specifiers:
%(levelname)-8s  - Left align, 8 characters wide
%(levelname)8s   - Right align, 8 characters wide

This creates neat, readable columns.
"""

def demo_alignment():
    """Demonstrate field alignment."""
    align_logger = logging.getLogger('alignment')
    align_logger.setLevel(logging.DEBUG)
    align_logger.handlers.clear()
    
    handler = logging.StreamHandler()
    # Note: -8 means left-align in 8-character field
    formatter = logging.Formatter('%(levelname)-8s | %(name)-20s | %(message)s')
    handler.setFormatter(formatter)
    align_logger.addHandler(handler)
    
    print("\nWith alignment (notice neat columns):")
    print("-" * 60)
    align_logger.debug("This is a debug message")
    align_logger.info("This is an info message")
    align_logger.warning("This is a warning message")
    align_logger.error("This is an error message")
    align_logger.critical("This is a critical message")

demo_alignment()

"""
ALIGNMENT BENEFITS:
- Makes logs easier to read
- Easier to scan for specific levels
- Professional appearance
- Easier to parse with scripts

RECOMMENDATION: Always pad levelname to 8 characters (length of "CRITICAL")
"""

# ============================================================================
# PART 5: CUSTOM FORMATTERS
# ============================================================================

print("\n" + "=" * 80)
print("PART 5: Creating Custom Formatter Classes")
print("=" * 80)

"""
For advanced needs, you can subclass logging.Formatter to create custom formatters.
This allows you to add custom logic, colors, or special formatting.
"""

class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds ANSI color codes to log levels.
    
    NOTE: This only works in terminals that support ANSI colors.
    Won't work in all environments (e.g., Windows cmd without special setup).
    """
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[1;31m', # Bold Red
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        """Format the log record with colors."""
        # Save original levelname
        original_levelname = record.levelname
        
        # Add color
        if record.levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelname]}"
                f"{record.levelname}"
                f"{self.COLORS['RESET']}"
            )
        
        # Format the message
        result = super().format(record)
        
        # Restore original levelname (important!)
        record.levelname = original_levelname
        
        return result

# Demonstrate colored output
print("\nColored logging (if your terminal supports ANSI colors):")
print("-" * 60)

color_logger = logging.getLogger('colored')
color_logger.setLevel(logging.DEBUG)
color_logger.handlers.clear()

handler = logging.StreamHandler()
formatter = ColoredFormatter('%(levelname)-8s - %(message)s')
handler.setFormatter(formatter)
color_logger.addHandler(handler)

color_logger.debug("Debug message in cyan")
color_logger.info("Info message in green")
color_logger.warning("Warning message in yellow")
color_logger.error("Error message in red")
color_logger.critical("Critical message in bold red")

"""
CUSTOM FORMATTER USE CASES:
- Adding colors (as shown)
- Redacting sensitive information
- Adding contextual information
- Custom date formatting logic
- Converting to JSON format
- Adding request IDs or correlation IDs
"""

# ============================================================================
# PART 6: PRACTICAL EXAMPLE - WEB APPLICATION FORMAT
# ============================================================================

print("\n" + "=" * 80)
print("PART 6: Practical Example - Web Application Logging")
print("=" * 80)

"""
In a web application, you often want to include request context in logs.
Here's a pattern for that.
"""

class WebAppFormatter(logging.Formatter):
    """
    Custom formatter for web applications.
    Includes request ID if available in log record.
    """
    
    def format(self, record):
        # Add request_id if not present
        if not hasattr(record, 'request_id'):
            record.request_id = 'N/A'
        
        if not hasattr(record, 'user_id'):
            record.user_id = 'anonymous'
        
        return super().format(record)

# Set up web app logger
webapp_logger = logging.getLogger('webapp')
webapp_logger.setLevel(logging.INFO)
webapp_logger.handlers.clear()

handler = logging.StreamHandler()
formatter = WebAppFormatter(
    '%(asctime)s | %(levelname)-8s | ReqID:%(request_id)s | User:%(user_id)s | %(message)s'
)
handler.setFormatter(formatter)
webapp_logger.addHandler(handler)

print("\nSimulating web application logging:")
print("-" * 60)

# Simulate handling a request
webapp_logger.info("Request received", extra={'request_id': 'req-12345', 'user_id': 'user-789'})
webapp_logger.info("Processing payment", extra={'request_id': 'req-12345', 'user_id': 'user-789'})
webapp_logger.error("Payment failed", extra={'request_id': 'req-12345', 'user_id': 'user-789'})

# Request without extra context
webapp_logger.info("System health check")

"""
KEY POINTS:
- 'extra' parameter adds custom attributes to LogRecord
- Custom formatter ensures missing attributes have defaults
- Request ID allows correlation of related log messages
- Essential for distributed systems and debugging production issues
"""

# ============================================================================
# PART 7: FORMAT STRING BEST PRACTICES
# ============================================================================

print("\n" + "=" * 80)
print("PART 7: Format String Best Practices")
print("=" * 80)

"""
RECOMMENDATIONS FOR PRODUCTION:

1. INCLUDE TIMESTAMP
   ✓ '%(asctime)s - %(message)s'
   ✗ '%(message)s'
   Why: Need to know when events occurred

2. INCLUDE LEVEL
   ✓ '%(asctime)s - %(levelname)s - %(message)s'
   ✗ '%(asctime)s - %(message)s'
   Why: Need to distinguish severity

3. PAD LEVELNAME
   ✓ '%(levelname)-8s'
   ✗ '%(levelname)s'
   Why: Creates aligned, readable columns

4. INCLUDE LOGGER NAME IN LARGE APPS
   ✓ '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   Why: Know which component logged the message

5. INCLUDE FILE/LINE IN DEVELOPMENT
   ✓ '%(filename)s:%(lineno)d - %(message)s'
   Why: Quickly locate source of log message

6. USE ISO 8601 TIMESTAMP FORMAT
   ✓ datefmt='%Y-%m-%d %H:%M:%S'
   Why: Internationally recognized, unambiguous

7. BE CONSISTENT
   Use the same format across your application
   Document your format choice
   Consider your team and tools
"""

# ============================================================================
# PART 8: COMPREHENSIVE EXAMPLE
# ============================================================================

print("\n" + "=" * 80)
print("PART 8: Complete Application with Professional Formatting")
print("=" * 80)

class UserManagementSystem:
    """
    Example system with professional logging format.
    """
    
    def __init__(self):
        # Set up logger
        self.logger = logging.getLogger('ums.core')
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()
        
        # Console handler with user-friendly format
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(asctime)s | %(name)-15s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        self.logger.info("User Management System initialized")
    
    def create_user(self, username, email):
        """Create a new user."""
        self.logger.debug(f"create_user() called: username={username}, email={email}")
        
        # Validate input
        if not username or len(username) < 3:
            self.logger.error(f"Invalid username: '{username}' (too short)")
            return False
        
        if '@' not in email:
            self.logger.error(f"Invalid email format: '{email}'")
            return False
        
        # Simulate user creation
        self.logger.info(f"Creating user: {username} ({email})")
        self.logger.debug(f"Hashing password for user: {username}")
        self.logger.debug(f"Sending confirmation email to: {email}")
        self.logger.info(f"User created successfully: {username}")
        
        return True
    
    def delete_user(self, username):
        """Delete a user."""
        self.logger.warning(f"User deletion requested: {username}")
        self.logger.info(f"Deleting all data for user: {username}")
        self.logger.info(f"User deleted: {username}")
        return True

print("\nUser Management System with professional formatting:")
print("-" * 60)

ums = UserManagementSystem()
ums.create_user("alice", "alice@example.com")
ums.create_user("b", "invalid-email")
ums.delete_user("alice")

# ============================================================================
# PART 9: KEY TAKEAWAYS
# ============================================================================

print("\n" + "=" * 80)
print("KEY TAKEAWAYS")
print("=" * 80)

"""
1. LOGRECORD ATTRIBUTES:
   - Many attributes available: %(asctime)s, %(levelname)s, %(name)s, etc.
   - Use appropriate attributes for your needs
   - Check documentation for complete list

2. FORMAT PATTERNS:
   - Minimal: '%(levelname)s - %(message)s'
   - Standard: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   - Detailed: Include %(filename)s, %(lineno)d, %(funcName)s

3. TIMESTAMP FORMATTING:
   - Use datefmt parameter
   - ISO 8601 recommended: '%Y-%m-%d %H:%M:%S'
   - Consider including milliseconds for precision

4. ALIGNMENT:
   - Use %(levelname)-8s for consistent width
   - Makes logs easier to read and parse
   - Essential for production systems

5. CUSTOM FORMATTERS:
   - Subclass logging.Formatter for advanced needs
   - Can add colors, redact data, include context
   - Override format() method

6. BEST PRACTICES:
   - Always include timestamp
   - Always include level
   - Pad levelname for alignment
   - Be consistent across application
   - Consider your audience (developers vs. operations)

NEXT STEPS:
- Learn about handlers (05_handlers.py)
- Explore logger hierarchy (06_logger_hierarchy.py)
- Study configuration methods (07_configuration_methods.py)
"""

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TUTORIAL COMPLETE!")
    print("=" * 80)
    print("\nYou now understand:")
    print("✓ LogRecord attributes")
    print("✓ Format string patterns")
    print("✓ Timestamp formatting")
    print("✓ Alignment and padding")
    print("✓ Custom formatters")
    print("✓ Professional logging formats")
    print("\nNext: Study 05_handlers.py to learn about different output handlers!")
```

---

## Exercises

**Exercise 1.**
Create a custom formatter that outputs log records in CSV format: `timestamp,level,logger_name,message`. Configure a logger with this formatter and log a few test messages.

??? success "Solution to Exercise 1"

    ```python
    import logging

    logger = logging.getLogger("csv_logger")
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s,%(levelname)s,%(name)s,%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info("Application started")
    logger.warning("Low memory")
    logger.error("Connection failed")
    ```

---

**Exercise 2.**
Create a formatter that includes the source file name and line number in the format `"[filename:lineno] LEVEL - message"`. Use the `%(filename)s` and `%(lineno)d` format attributes.

??? success "Solution to Exercise 2"

    ```python
    import logging

    logger = logging.getLogger("source_logger")
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(filename)s:%(lineno)d] %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info("This shows the source location")
    # [script.py:12] INFO - This shows the source location
    ```

---

**Exercise 3.**
Write a custom `logging.Formatter` subclass that adds a `[DURATION]` field showing the time elapsed since the logger was first used. Override the `format` method to include this computed field.

??? success "Solution to Exercise 3"

    ```python
    import logging
    import time

    class DurationFormatter(logging.Formatter):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.start_time = time.time()

        def format(self, record):
            elapsed = time.time() - self.start_time
            record.duration = f"{elapsed:.3f}s"
            return super().format(record)

    logger = logging.getLogger("duration_logger")
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = DurationFormatter(
        "[%(duration)s] %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info("First message")
    time.sleep(0.1)
    logger.info("Second message")
    ```
