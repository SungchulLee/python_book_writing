# Callback Patterns

A callback is a function passed as an argument to another function, to be called later. Callbacks are fundamental to event-driven programming, asynchronous operations, and flexible APIs.

!!! tip "Mental Model"
    A callback is a "call me when you're done" contract: you hand a function to someone else's code, and that code invokes it at the right moment. The caller decides *what* to do; the callee decides *when*. This inversion of control is the foundation of event-driven and asynchronous programming.

---

## What is a Callback?

```python
def process_data(data, on_complete):
    """Process data and call on_complete when done."""
    result = [x * 2 for x in data]
    on_complete(result)  # Callback invocation

def print_result(result):
    print(f"Processing complete: {result}")

# Pass function as callback
process_data([1, 2, 3], print_result)
# Output: Processing complete: [2, 4, 6]
```

The key insight: **functions are first-class objects** in Python, so they can be passed around like any other value.

---

## Basic Callback Patterns

### Simple Callback

```python
def fetch_data(url, callback):
    """Simulate fetching data and calling back with result."""
    # Simulate network request
    data = {"status": "ok", "url": url}
    callback(data)

def handle_response(data):
    print(f"Received: {data}")

fetch_data("https://api.example.com", handle_response)
```

### Callback with Lambda

```python
def calculate(x, y, operation):
    """Apply operation callback to x and y."""
    return operation(x, y)

# Using lambdas as callbacks
calculate(10, 5, lambda a, b: a + b)  # 15
calculate(10, 5, lambda a, b: a * b)  # 50
calculate(10, 5, lambda a, b: a ** b) # 100000
```

### Multiple Callbacks

```python
def process(data, on_success, on_error):
    """Process with separate success and error callbacks."""
    try:
        result = [x * 2 for x in data]
        on_success(result)
    except Exception as e:
        on_error(e)

def success_handler(result):
    print(f"Success: {result}")

def error_handler(error):
    print(f"Error: {error}")

process([1, 2, 3], success_handler, error_handler)
# Success: [2, 4, 6]

process("not a list", success_handler, error_handler)
# Error: can't multiply sequence by non-int
```

---

## Callback with Context

### Passing Extra Arguments

```python
from functools import partial

def notify(message, callback, **context):
    """Notify with additional context."""
    callback(message, **context)

def log_message(message, level="INFO", timestamp=None):
    print(f"[{level}] {timestamp}: {message}")

notify("Server started", log_message, level="INFO", timestamp="10:30")
# [INFO] 10:30: Server started
```

### Using partial for Context

```python
from functools import partial

def send_email(to, subject, body):
    print(f"To: {to}\nSubject: {subject}\n{body}")

def process_order(order_id, on_complete):
    # Process order...
    on_complete(order_id)

# Create callback with pre-filled arguments
email_callback = partial(
    send_email,
    to="customer@example.com",
    subject="Order Confirmation"
)

def notify_order(order_id):
    email_callback(body=f"Your order #{order_id} is confirmed!")

process_order(12345, notify_order)
```

### Closure for Context

```python
def create_logger(prefix):
    """Create a callback with embedded context."""
    def log(message):
        print(f"[{prefix}] {message}")
    return log

debug_log = create_logger("DEBUG")
error_log = create_logger("ERROR")

def process(data, logger):
    logger(f"Processing {len(data)} items")
    # ... process data
    logger("Complete")

process([1, 2, 3], debug_log)
# [DEBUG] Processing 3 items
# [DEBUG] Complete
```

---

## Event Handler Pattern

### Simple Event System

```python
class EventEmitter:
    def __init__(self):
        self._callbacks = {}
    
    def on(self, event, callback):
        """Register a callback for an event."""
        if event not in self._callbacks:
            self._callbacks[event] = []
        self._callbacks[event].append(callback)
    
    def emit(self, event, *args, **kwargs):
        """Trigger all callbacks for an event."""
        for callback in self._callbacks.get(event, []):
            callback(*args, **kwargs)

# Usage
emitter = EventEmitter()

def on_user_login(user):
    print(f"User logged in: {user}")

def on_user_login_log(user):
    print(f"Logging: {user} login at {datetime.now()}")

emitter.on("login", on_user_login)
emitter.on("login", on_user_login_log)

emitter.emit("login", "alice")
# User logged in: alice
# Logging: alice login at 2024-01-15 10:30:00
```

### With Decorator Registration

```python
class EventSystem:
    _handlers = {}
    
    @classmethod
    def on(cls, event):
        """Decorator to register event handler."""
        def decorator(func):
            if event not in cls._handlers:
                cls._handlers[event] = []
            cls._handlers[event].append(func)
            return func
        return decorator
    
    @classmethod
    def emit(cls, event, *args, **kwargs):
        for handler in cls._handlers.get(event, []):
            handler(*args, **kwargs)

# Register handlers with decorator
@EventSystem.on("order_placed")
def send_confirmation(order):
    print(f"Sending confirmation for order {order['id']}")

@EventSystem.on("order_placed")
def update_inventory(order):
    print(f"Updating inventory for {order['items']}")

# Trigger event
EventSystem.emit("order_placed", {"id": 123, "items": ["book", "pen"]})
```

---

## Observer Pattern

```python
class Subject:
    """Observable that notifies observers of state changes."""
    
    def __init__(self):
        self._observers = []
        self._state = None
    
    def attach(self, observer):
        """Add an observer callback."""
        self._observers.append(observer)
    
    def detach(self, observer):
        """Remove an observer callback."""
        self._observers.remove(observer)
    
    def notify(self):
        """Notify all observers of state change."""
        for observer in self._observers:
            observer(self._state)
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        self._state = value
        self.notify()

# Usage
def observer_a(state):
    print(f"Observer A: state changed to {state}")

def observer_b(state):
    print(f"Observer B: state changed to {state}")

subject = Subject()
subject.attach(observer_a)
subject.attach(observer_b)

subject.state = "active"
# Observer A: state changed to active
# Observer B: state changed to active

subject.detach(observer_a)
subject.state = "inactive"
# Observer B: state changed to inactive
```

---

## Progress Callback Pattern

```python
def process_items(items, on_progress=None):
    """Process items with optional progress callback."""
    results = []
    total = len(items)
    
    for i, item in enumerate(items):
        # Process item
        result = item * 2
        results.append(result)
        
        # Report progress
        if on_progress:
            progress = (i + 1) / total * 100
            on_progress(progress, item, result)
    
    return results

def print_progress(percent, item, result):
    print(f"{percent:.0f}% - Processed {item} -> {result}")

process_items([1, 2, 3, 4, 5], on_progress=print_progress)
# 20% - Processed 1 -> 2
# 40% - Processed 2 -> 4
# 60% - Processed 3 -> 6
# 80% - Processed 4 -> 8
# 100% - Processed 5 -> 10
```

### Progress with Cancellation

```python
def process_items(items, on_progress=None):
    """Process items; callback returns False to cancel."""
    results = []
    total = len(items)
    
    for i, item in enumerate(items):
        result = item * 2
        results.append(result)
        
        if on_progress:
            progress = (i + 1) / total * 100
            should_continue = on_progress(progress, item, result)
            if should_continue is False:
                print("Processing cancelled")
                break
    
    return results

def limited_progress(percent, item, result):
    print(f"{percent:.0f}%")
    return percent < 50  # Cancel after 50%

process_items([1, 2, 3, 4, 5], on_progress=limited_progress)
# 20%
# 40%
# 60%
# Processing cancelled
```

---

## Retry with Callback

```python
import time
import random

def retry_operation(operation, max_attempts=3, on_retry=None):
    """Retry operation with callback on each retry."""
    last_error = None
    
    for attempt in range(1, max_attempts + 1):
        try:
            return operation()
        except Exception as e:
            last_error = e
            if on_retry and attempt < max_attempts:
                on_retry(attempt, e)
            time.sleep(0.1 * attempt)  # Exponential backoff
    
    raise last_error

def unreliable_operation():
    if random.random() < 0.7:
        raise ConnectionError("Network timeout")
    return "Success!"

def on_retry(attempt, error):
    print(f"Attempt {attempt} failed: {error}. Retrying...")

result = retry_operation(unreliable_operation, max_attempts=5, on_retry=on_retry)
```

---

## Validation Callback Pattern

```python
def create_user(username, email, validators=None):
    """Create user with validation callbacks."""
    validators = validators or []
    
    data = {"username": username, "email": email}
    
    # Run all validators
    errors = []
    for validator in validators:
        error = validator(data)
        if error:
            errors.append(error)
    
    if errors:
        raise ValueError(f"Validation failed: {errors}")
    
    return data

# Validator callbacks
def validate_username(data):
    if len(data["username"]) < 3:
        return "Username must be at least 3 characters"

def validate_email(data):
    if "@" not in data["email"]:
        return "Invalid email format"

def validate_no_spaces(data):
    if " " in data["username"]:
        return "Username cannot contain spaces"

# Usage
validators = [validate_username, validate_email, validate_no_spaces]

try:
    user = create_user("ab", "invalid", validators)
except ValueError as e:
    print(e)
# Validation failed: ['Username must be at least 3 characters', 'Invalid email format']
```

---

## Middleware Pattern

```python
def apply_middleware(data, middlewares):
    """Apply chain of middleware callbacks."""
    result = data
    for middleware in middlewares:
        result = middleware(result)
        if result is None:
            break  # Middleware can halt chain
    return result

# Middleware callbacks
def add_timestamp(data):
    data["timestamp"] = "2024-01-15"
    return data

def add_user_id(data):
    data["user_id"] = 123
    return data

def validate_data(data):
    if "name" not in data:
        print("Validation failed: missing name")
        return None  # Halt chain
    return data

# Apply middleware chain
middlewares = [add_timestamp, add_user_id, validate_data]

result = apply_middleware({"name": "test"}, middlewares)
print(result)
# {'name': 'test', 'timestamp': '2024-01-15', 'user_id': 123}

result = apply_middleware({}, middlewares)
# Validation failed: missing name
# None
```

---

## Async Callback Simulation

```python
import threading
import time

def async_fetch(url, on_complete, on_error=None):
    """Simulate async operation with callbacks."""
    def do_fetch():
        try:
            time.sleep(1)  # Simulate network delay
            data = {"url": url, "status": "ok"}
            on_complete(data)
        except Exception as e:
            if on_error:
                on_error(e)
    
    thread = threading.Thread(target=do_fetch)
    thread.start()
    return thread

def handle_result(data):
    print(f"Received: {data}")

def handle_error(error):
    print(f"Error: {error}")

print("Starting async fetch...")
thread = async_fetch("https://api.example.com", handle_result, handle_error)
print("Continuing with other work...")
thread.join()  # Wait for completion
# Starting async fetch...
# Continuing with other work...
# (1 second later)
# Received: {'url': 'https://api.example.com', 'status': 'ok'}
```

---

## Best Practices

### Use Type Hints

```python
from typing import Callable, Optional

def process(
    data: list,
    on_complete: Callable[[list], None],
    on_error: Optional[Callable[[Exception], None]] = None
) -> None:
    """Process with typed callbacks."""
    try:
        result = [x * 2 for x in data]
        on_complete(result)
    except Exception as e:
        if on_error:
            on_error(e)
```

### Default No-Op Callback

```python
def process(data, callback=None):
    """Use no-op default instead of None check."""
    callback = callback or (lambda x: None)
    result = [x * 2 for x in data]
    callback(result)
    return result
```

### Document Callback Signatures

```python
def fetch_data(url, callback):
    """
    Fetch data from URL.
    
    Args:
        url: The URL to fetch
        callback: Function called with (data, error) where:
            - data: The response dict if successful, None on error
            - error: Exception if failed, None on success
    """
    pass
```

---

## Summary

| Pattern | Use Case |
|---------|----------|
| Simple callback | Basic async completion |
| Success/Error callbacks | Error handling |
| Event emitter | Multiple listeners |
| Observer | State change notifications |
| Progress callback | Long-running operations |
| Validation callbacks | Pluggable validation |
| Middleware | Request/response processing |

**Key Takeaways**:

- Callbacks enable flexible, extensible APIs
- Use multiple callbacks for success/error handling
- `functools.partial` and closures provide context
- Event systems allow multiple subscribers
- Progress callbacks should support cancellation
- Type hints document expected callback signatures
- Consider `async/await` for complex async patterns

---

## Exercises

**Exercise 1.**
Write a `download_file(url, on_progress, on_complete)` function that simulates downloading by iterating 10 times. On each iteration, call `on_progress(percent)` with the current percentage (10, 20, ..., 100). After the loop, call `on_complete(url)`. Demonstrate with callbacks that print progress and a completion message.

??? success "Solution to Exercise 1"

        def download_file(url, on_progress, on_complete):
            for i in range(1, 11):
                percent = i * 10
                on_progress(percent)
            on_complete(url)

        download_file(
            "https://example.com/file.zip",
            on_progress=lambda p: print(f"  Progress: {p}%"),
            on_complete=lambda url: print(f"  Download complete: {url}"),
        )

---

**Exercise 2.**
Create a simple `EventEmitter` class with `on(event, callback)` to register callbacks and `emit(event, *args)` to trigger all callbacks for that event. Register multiple callbacks for a `"data"` event and demonstrate that emitting the event calls all of them in order.

??? success "Solution to Exercise 2"

        class EventEmitter:
            def __init__(self):
                self.listeners = {}

            def on(self, event, callback):
                if event not in self.listeners:
                    self.listeners[event] = []
                self.listeners[event].append(callback)

            def emit(self, event, *args):
                for callback in self.listeners.get(event, []):
                    callback(*args)

        emitter = EventEmitter()
        emitter.on("data", lambda d: print(f"Logger: {d}"))
        emitter.on("data", lambda d: print(f"Processor: {d}"))
        emitter.on("data", lambda d: print(f"Archiver: {d}"))

        emitter.emit("data", {"temperature": 22.5})

---

**Exercise 3.**
Write a `retry_with_callback(func, max_attempts, on_failure, on_success)` function that calls `func()` up to `max_attempts` times. On each failure, call `on_failure(attempt, exception)`. On success, call `on_success(result)` and return the result. If all attempts fail, raise the last exception.

??? success "Solution to Exercise 3"

        def retry_with_callback(func, max_attempts, on_failure, on_success):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func()
                    on_success(result)
                    return result
                except Exception as e:
                    last_exc = e
                    on_failure(attempt, e)
            raise last_exc

        call_count = 0

        def flaky_operation():
            global call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("Timeout")
            return "OK"

        retry_with_callback(
            flaky_operation,
            max_attempts=5,
            on_failure=lambda a, e: print(f"  Attempt {a} failed: {e}"),
            on_success=lambda r: print(f"  Success: {r}"),
        )
