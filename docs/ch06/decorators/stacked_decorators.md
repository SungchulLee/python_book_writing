# Stacked Decorators

Multiple decorators can be applied to a single function. The order of application matters.

!!! tip "Mental Model"
    Stacking decorators is like nesting Russian dolls: the bottom decorator wraps the function first, then each decorator above wraps the previous result. They apply inside-out but execute outside-in, so the topmost decorator's wrapper runs first on every call.

## Basic Stacking

Decorators are applied bottom-up (inner first), but execute top-down.

```python
@decorator_a
@decorator_b
@decorator_c
def func():
    pass

# Equivalent to:
func = decorator_a(decorator_b(decorator_c(func)))
```

**Application order**: `decorator_c` → `decorator_b` → `decorator_a`

**Execution order**: `decorator_a`'s wrapper runs first

---

## Visualizing the Stack

```python
from functools import wraps

def decorator_a(func):
    @wraps(func)
    def wrapper(*args):
        print("A: before")
        result = func(*args)
        print("A: after")
        return result
    return wrapper

def decorator_b(func):
    @wraps(func)
    def wrapper(*args):
        print("B: before")
        result = func(*args)
        print("B: after")
        return result
    return wrapper

@decorator_a
@decorator_b
def greet(name):
    print(f"Hello, {name}!")
    return name

greet("Alice")
```

Output:
```
A: before
B: before
Hello, Alice!
B: after
A: after
```

The outer decorator (`decorator_a`) wraps the inner decorator (`decorator_b`), which wraps the original function.

---

## Example: Logger and Timer

```python
import time
from functools import wraps

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[LOG] Finished {func.__name__}")
        return result
    return wrapper

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[TIME] {func.__name__}: {end - start:.4f}s")
        return result
    return wrapper
```

### Order 1: Logger Outside

```python
@logger
@timer
def compute(n):
    return sum(range(n))

compute(1000000)
```

Output:
```
[LOG] Calling compute
[TIME] compute: 0.0234s
[LOG] Finished compute
```

The timing is logged as part of the function execution.

### Order 2: Timer Outside

```python
@timer
@logger
def compute(n):
    return sum(range(n))

compute(1000000)
```

Output:
```
[LOG] Calling compute
[LOG] Finished compute
[TIME] compute: 0.0234s
```

The timer includes the logging overhead.

---

## Practical Example: Auth + Logging

```python
from functools import wraps

def require_auth(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        if not user.get('authenticated'):
            raise PermissionError("Authentication required")
        return func(user, *args, **kwargs)
    return wrapper

def log_access(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        print(f"[ACCESS] {user.get('name')} called {func.__name__}")
        return func(user, *args, **kwargs)
    return wrapper

@log_access
@require_auth
def get_secret_data(user):
    return "Secret: 42"

# Auth check happens first (inner), then logging (outer)
user = {'name': 'Alice', 'authenticated': True}
get_secret_data(user)
# [ACCESS] Alice called get_secret_data
```

---

## Common Stacking Patterns

| Outer | Inner | Use Case |
|-------|-------|----------|
| `@logger` | `@timer` | Log includes timing info |
| `@timer` | `@logger` | Time includes logging overhead |
| `@cache` | `@validate` | Validate before caching |
| `@log` | `@auth` | Log only authenticated calls |
| `@retry` | `@timeout` | Retry timed-out operations |

---

## Order Matters: Real Examples

### Caching with Validation

```python
@cache        # Cache validated results
@validate     # Validate first
def compute(x):
    pass
```

If reversed, invalid inputs might be cached.

### Rate Limiting with Auth

```python
@rate_limit   # Apply rate limit
@require_auth # Check auth first
def api_endpoint(user):
    pass
```

Unauthenticated requests shouldn't count against rate limit.

### Metrics with Error Handling

```python
@track_errors  # Track errors
@track_timing  # Time the operation
def process():
    pass
```

Error tracking wraps timing to catch timing-related issues.

---

## Debugging Stacked Decorators

### Check the Wrapper Chain

```python
@decorator_a
@decorator_b
def func():
    pass

# See the chain
print(func.__name__)       # Should be 'func' if @wraps used
print(func.__wrapped__)    # The next layer
print(func.__wrapped__.__wrapped__)  # Original function
```

### Temporarily Disable

```python
# Comment out decorators to isolate issues
# @decorator_a
@decorator_b
def func():
    pass
```

---

## Summary

| Aspect | Description |
|--------|-------------|
| Application | Bottom-up (inner decorator applied first) |
| Execution | Top-down (outer wrapper runs first) |
| Nesting | Each decorator wraps the previous result |
| Metadata | Use `@wraps(func)` at each level |

**Key Rules**:
- Decorators apply bottom-up, execute top-down
- Order affects both behavior and measurements
- Inner decorators are "closer" to the original function
- Always use `@wraps(func)` to preserve metadata through the stack
---

## Runnable Example: `decorator_mini_project.py`

```python
"""
Decorators Mini-Project: API Request Handler
This project demonstrates how to use multiple decorators to create
a robust API request handler with logging, timing, retry logic, and validation.
"""

import time
import functools
import random
from datetime import datetime

if __name__ == "__main__":

    print("=" * 70)
    print("DECORATORS MINI-PROJECT: API REQUEST HANDLER")
    print("=" * 70)

    # ============================================================================
    # DECORATOR DEFINITIONS
    # ============================================================================

    def log_request(func):
        """Log function calls with timestamp"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n[{timestamp}] Calling {func.__name__}")
            result = func(*args, **kwargs)
            print(f"[{timestamp}] {func.__name__} completed")
            return result
        return wrapper


    def timer(func):
        """Measure execution time"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"⏱️  Execution time: {end - start:.3f} seconds")
            return result
        return wrapper


    def retry(max_attempts=3, delay=1):
        """Retry function on failure"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(1, max_attempts + 1):
                    try:
                        print(f"🔄 Attempt {attempt}/{max_attempts}")
                        return func(*args, **kwargs)
                    except Exception as e:
                        if attempt == max_attempts:
                            print(f"❌ All attempts failed")
                            raise
                        print(f"⚠️  Attempt {attempt} failed: {e}")
                        print(f"   Waiting {delay}s before retry...")
                        time.sleep(delay)
            return wrapper
        return decorator


    def validate_response(func):
        """Validate API response"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result is None:
                raise ValueError("Response is None")
            if not isinstance(result, dict):
                raise TypeError("Response must be a dictionary")
            if "status" not in result:
                raise KeyError("Response missing 'status' field")
            print(f"✅ Validation passed")
            return result
        return wrapper


    def rate_limit(calls_per_minute=10):
        """Limit API calls per minute"""
        def decorator(func):
            calls = []

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                now = time.time()
                # Remove calls older than 1 minute
                calls[:] = [call_time for call_time in calls if now - call_time < 60]

                if len(calls) >= calls_per_minute:
                    wait_time = 60 - (now - calls[0])
                    print(f"⏸️  Rate limit reached. Waiting {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    calls[:] = []

                calls.append(time.time())
                return func(*args, **kwargs)
            return wrapper
        return decorator


    def cache_result(ttl=5):
        """Cache results for specified time-to-live (seconds)"""
        def decorator(func):
            cache = {}

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = str(args) + str(kwargs)
                now = time.time()

                if key in cache:
                    result, timestamp = cache[key]
                    if now - timestamp < ttl:
                        print(f"💾 Returning cached result")
                        return result

                result = func(*args, **kwargs)
                cache[key] = (result, now)
                return result
            return wrapper
        return decorator


    def handle_errors(func):
        """Gracefully handle errors"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"🚫 Error handled: {type(e).__name__}: {e}")
                return {"status": "error", "message": str(e)}
        return wrapper


    # ============================================================================
    # SIMULATED API FUNCTIONS
    # ============================================================================

    # Simulate unreliable network
    call_count = 0

    @handle_errors
    @log_request
    @timer
    @retry(max_attempts=3, delay=0.5)
    @validate_response
    def fetch_user_data(user_id):
        """Simulate fetching user data from API"""
        global call_count
        call_count += 1

        # Simulate network delay
        time.sleep(random.uniform(0.1, 0.3))

        # Simulate occasional failures
        if call_count < 2:
            raise ConnectionError("Network timeout")

        # Return mock user data
        return {
            "status": "success",
            "user_id": user_id,
            "name": f"User {user_id}",
            "email": f"user{user_id}@example.com"
        }


    @log_request
    @timer
    @cache_result(ttl=3)
    @validate_response
    def get_cached_data(data_id):
        """Simulate fetching cached data"""
        time.sleep(0.2)  # Simulate processing
        return {
            "status": "success",
            "data_id": data_id,
            "value": random.randint(1, 100)
        }


    @log_request
    @rate_limit(calls_per_minute=3)
    def rate_limited_request(endpoint):
        """Simulate rate-limited API endpoint"""
        time.sleep(0.1)
        print(f"📡 Request sent to {endpoint}")
        return {"status": "success", "endpoint": endpoint}


    # ============================================================================
    # DEMONSTRATION
    # ============================================================================

    print("\n" + "=" * 70)
    print("DEMONSTRATION 1: Retry with Validation")
    print("=" * 70)
    print("This function will fail initially but succeed after retry")

    result = fetch_user_data(123)
    print(f"\n📊 Final Result: {result}")


    print("\n" + "=" * 70)
    print("DEMONSTRATION 2: Caching")
    print("=" * 70)
    print("First call will fetch data, second call will use cache")

    print("\n--- First call ---")
    result1 = get_cached_data(456)
    print(f"Result: {result1}")

    print("\n--- Second call (should be cached) ---")
    result2 = get_cached_data(456)
    print(f"Result: {result2}")

    print("\n--- Wait for cache to expire (3 seconds) ---")
    time.sleep(3.5)

    print("\n--- Third call (cache expired) ---")
    result3 = get_cached_data(456)
    print(f"Result: {result3}")


    print("\n" + "=" * 70)
    print("DEMONSTRATION 3: Rate Limiting")
    print("=" * 70)
    print("Making 5 requests (limit is 3 per minute)")

    for i in range(5):
        print(f"\n--- Request {i+1} ---")
        rate_limited_request(f"/api/endpoint{i}")


    print("\n" + "=" * 70)
    print("DEMONSTRATION 4: Error Handling")
    print("=" * 70)

    @handle_errors
    @validate_response
    def buggy_function():
        """This function has a bug"""
        return None  # Invalid response

    result = buggy_function()
    print(f"\n📊 Result: {result}")


    # ============================================================================
    # REAL-WORLD EXAMPLE: Complete API Client
    # ============================================================================

    print("\n" + "=" * 70)
    print("REAL-WORLD EXAMPLE: Complete API Client")
    print("=" * 70)

    class APIClient:
        """Example API client using decorators"""

        @staticmethod
        @handle_errors
        @log_request
        @timer
        @cache_result(ttl=10)
        @validate_response
        def get_weather(city):
            """Fetch weather data"""
            time.sleep(0.2)  # Simulate API call
            return {
                "status": "success",
                "city": city,
                "temperature": random.randint(60, 80),
                "condition": random.choice(["Sunny", "Cloudy", "Rainy"])
            }

        @staticmethod
        @handle_errors
        @log_request
        @timer
        @retry(max_attempts=2, delay=0.5)
        @rate_limit(calls_per_minute=5)
        @validate_response
        def post_data(endpoint, data):
            """Post data to API"""
            time.sleep(0.1)
            return {
                "status": "success",
                "endpoint": endpoint,
                "data_received": data
            }


    print("\nFetching weather data...")
    weather = APIClient.get_weather("New York")
    print(f"🌤️  {weather}")

    print("\nFetching weather data again (should use cache)...")
    weather = APIClient.get_weather("New York")
    print(f"🌤️  {weather}")

    print("\nPosting data...")
    post_result = APIClient.post_data("/api/data", {"value": 42})
    print(f"📤 {post_result}")


    # ============================================================================
    # SUMMARY
    # ============================================================================

    print("\n" + "=" * 70)
    print("PROJECT SUMMARY")
    print("=" * 70)
    print("""
    This mini-project demonstrated practical decorator usage:

    ✅ Decorators Used:
       - @log_request: Activity logging with timestamps
       - @timer: Performance measurement
       - @retry: Automatic retry on failure
       - @validate_response: Response validation
       - @rate_limit: API call throttling
       - @cache_result: Result caching with TTL
       - @handle_errors: Graceful error handling

    ✅ Key Patterns:
       - Multiple decorators stacked on single function
       - Decorators with parameters (retry attempts, cache TTL)
       - Class-based decorators for stateful behavior
       - Error handling and validation layers

    ✅ Real-World Applications:
       - API clients (REST, GraphQL)
       - Microservices communication
       - Database query optimization
       - Web scraping with rate limiting
       - Caching expensive computations

    ✅ Benefits:
       - Separation of concerns (logging, validation separate from logic)
       - Reusable cross-cutting functionality
       - Clean, readable code
       - Easy to add/remove features

    Try extending this project by adding:
       - Authentication decorator
       - Request timeout decorator
       - Response transformation decorator
       - Metrics collection decorator
       - Circuit breaker pattern
    """)

    print("=" * 70)
    print("END OF MINI-PROJECT")
    print("=" * 70)
```

---

## Exercises

**Exercise 1.**
Write two decorators, `@bold` and `@italic`, that wrap a function's string return value in `<b>...</b>` and `<i>...</i>` tags respectively. Stack them as `@bold` on top and `@italic` on bottom, then call the function and verify the output is `<b><i>hello</i></b>`. Explain the application order.

??? success "Solution to Exercise 1"

        from functools import wraps

        def bold(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return f"<b>{func(*args, **kwargs)}</b>"
            return wrapper

        def italic(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return f"<i>{func(*args, **kwargs)}</i>"
            return wrapper

        @bold      # Applied second (outermost)
        @italic    # Applied first (innermost)
        def greet():
            return "hello"

        print(greet())  # <b><i>hello</i></b>
        # italic wraps greet first, then bold wraps the result

---

**Exercise 2.**
Create `@log_entry` and `@log_exit` decorators. `@log_entry` prints `"Entering <name>"` before the call. `@log_exit` prints `"Exiting <name>"` after the call. Stack both on a function and demonstrate that the output order depends on which decorator is on top.

??? success "Solution to Exercise 2"

        from functools import wraps

        def log_entry(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print(f"Entering {func.__name__}")
                return func(*args, **kwargs)
            return wrapper

        def log_exit(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                print(f"Exiting {func.__name__}")
                return result
            return wrapper

        @log_entry
        @log_exit
        def compute(x):
            print(f"  Computing {x}")
            return x * 2

        print(compute(5))
        # Output:
        # Entering compute
        #   Computing 5
        # Exiting compute
        # 10

---

**Exercise 3.**
Write three decorators: `@authenticate` (checks that a `user` keyword argument is not `None`), `@log` (prints the function name and arguments), and `@timer` (prints execution time). Stack all three on a single function in an order where authentication is checked first, then the call is logged, then timing is measured. Verify the behavior with both valid and invalid `user` values.

??? success "Solution to Exercise 3"

        import time
        from functools import wraps

        def authenticate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if kwargs.get("user") is None:
                    raise PermissionError("Authentication required")
                return func(*args, **kwargs)
            return wrapper

        def log(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print(f"Calling {func.__name__}(args={args}, kwargs={kwargs})")
                return func(*args, **kwargs)
            return wrapper

        def timer(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                print(f"{func.__name__} took {time.perf_counter() - start:.4f}s")
                return result
            return wrapper

        @timer          # Outermost: measures total time
        @log            # Middle: logs the call
        @authenticate   # Innermost: checks auth first
        def get_data(query, user=None):
            return f"Results for '{query}'"

        print(get_data("SELECT *", user="admin"))
        try:
            get_data("SELECT *", user=None)
        except PermissionError as e:
            print(e)
