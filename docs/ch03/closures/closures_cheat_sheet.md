# Python Closures - Quick Reference Cheat Sheet

!!! tip "Mental Model"
    Closures follow a simple recipe: an outer function defines state, an inner function uses it, and the outer function returns the inner one. The returned function "closes over" the enclosing variables, bundling code and data into a single callable. This cheat sheet gives you the patterns to recognize and apply that recipe quickly.

## Definition

A **closure** is a function that:
1. Is defined inside another function (nested)
2. References variables from the outer function's scope
3. Can be returned and called later, still remembering those variables

```python
def outer(x):
    def inner(y):
        return x + y  # inner "closes over" x
    return inner

add_5 = outer(5)  # add_5 is a closure
print(add_5(3))   # 8
```

## Basic Template

```python
def outer_function(outer_var):
    # outer_var is captured by the closure
    
    def inner_function(inner_var):
        # Can access both outer_var and inner_var
        return outer_var + inner_var
    
    return inner_function  # Return without calling ()

# Create closure
my_closure = outer_function(10)
result = my_closure(5)  # 15
```

## The nonlocal Keyword

Use `nonlocal` to modify variables from the enclosing scope:

```python
def make_counter():
    count = 0
    
    def increment():
        nonlocal count  # Required to modify count
        count += 1
        return count
    
    return increment

counter = make_counter()
print(counter())  # 1
print(counter())  # 2
```

**Without nonlocal:**
- Can READ outer variables ✓
- Cannot MODIFY outer variables ✗ (creates local variable instead)

**With nonlocal:**
- Can both READ and MODIFY outer variables ✓

## Common Patterns

### 1. Factory Functions
Create specialized functions:

```python
def make_multiplier(factor):
    def multiply(n):
        return n * factor
    return multiply

times_2 = make_multiplier(2)
times_10 = make_multiplier(10)
```

### 2. Data Encapsulation (Private Variables)
Hide implementation details:

```python
def make_account(balance):
    def deposit(amount):
        nonlocal balance
        balance += amount
        return balance
    
    def withdraw(amount):
        nonlocal balance
        balance -= amount
        return balance
    
    def get_balance():
        return balance
    
    return {'deposit': deposit, 'withdraw': withdraw, 'balance': get_balance}
```

### 3. Configuration Functions
Store settings:

```python
def make_formatter(prefix, suffix):
    def format(text):
        return f"{prefix}{text}{suffix}"
    return format

html_bold = make_formatter("<b>", "</b>")
html_italic = make_formatter("<i>", "</i>")
```

### 4. Callbacks with State
Event handlers that remember:

```python
def make_click_handler(element_id):
    click_count = 0
    
    def handle_click():
        nonlocal click_count
        click_count += 1
        print(f"{element_id}: {click_count} clicks")
    
    return handle_click
```

### 5. Memoization/Caching
Cache expensive results:

```python
def make_memoized(func):
    cache = {}
    
    def memoized(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    
    return memoized
```

### 6. Counters and Accumulators
Maintain state between calls:

```python
def make_counter(start=0):
    count = start
    
    def counter():
        nonlocal count
        count += 1
        return count
    
    return counter
```

## LEGB Rule (Variable Lookup Order)

Python searches for variables in this order:
1. **L**ocal: Inside current function
2. **E**nclosing: In enclosing functions (closures!)
3. **G**lobal: Module level
4. **B**uilt-in: Python built-ins

```python
x = "global"

def outer():
    x = "enclosing"
    
    def inner():
        x = "local"
        print(x)  # Prints "local"
    
    inner()
```

## Multiple Closures Sharing State

```python
def make_counter():
    count = 0
    
    def increment():
        nonlocal count
        count += 1
        return count
    
    def decrement():
        nonlocal count
        count -= 1
        return count
    
    def get():
        return count
    
    return increment, decrement, get

inc, dec, get = make_counter()
```

## Common Pitfall: Closures in Loops

### ❌ WRONG:
```python
def create_funcs():
    funcs = []
    for i in range(3):
        funcs.append(lambda x: x * i)
    return funcs

f = create_funcs()
print(f[0](2))  # Expected: 0, Got: 4
print(f[1](2))  # Expected: 2, Got: 4
print(f[2](2))  # Expected: 4, Got: 4
# All closures share the same 'i' which is 2 after loop!
```

### ✅ SOLUTION 1: Default Argument
```python
def create_funcs():
    funcs = []
    for i in range(3):
        funcs.append(lambda x, i=i: x * i)  # Capture current i
    return funcs
```

### ✅ SOLUTION 2: Factory Function
```python
def make_multiplier(i):
    return lambda x: x * i

def create_funcs():
    return [make_multiplier(i) for i in range(3)]
```

## Closures vs Classes

### Use Closure When:
- ✓ Simple, single-method behavior
- ✓ Private data without class overhead
- ✓ Functional programming style
- ✓ Quick factory functions

### Use Class When:
- ✓ Multiple related methods
- ✓ Complex state management
- ✓ Need inheritance
- ✓ Need special methods (`__str__`, `__repr__`, etc.)

### Example Comparison:

**Closure:**
```python
def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment
```

**Class:**
```python
class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
        return self.count
```

## Inspecting Closures

```python
def outer(x):
    def inner(y):
        return x + y
    return inner

f = outer(5)

# See captured variables
print(f.__closure__)          # (<cell at 0x...: int object at 0x...>,)
print(f.__code__.co_freevars) # ('x',)

# Get value
print(f.__closure__[0].cell_contents)  # 5
```

## Decorators (Built on Closures)

Decorators are just closures used to wrap functions:

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper

@my_decorator
def greet(name):
    print(f"Hello, {name}!")
```

## Partial Application

Create specialized functions from general ones:

```python
def partial(func, *fixed_args):
    def wrapper(*args):
        return func(*fixed_args, *args)
    return wrapper

def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
cube = partial(power, exp=3)
```

## Function Composition

Combine functions:

```python
def compose(f, g):
    def composed(x):
        return f(g(x))
    return composed

def add_10(x):
    return x + 10

def multiply_2(x):
    return x * 2

add_then_multiply = compose(multiply_2, add_10)
print(add_then_multiply(5))  # 30: (5 + 10) * 2
```

## Best Practices

### ✅ DO:
- Keep closures simple and focused
- Use descriptive names for captured variables
- Document what the closure captures
- Use `nonlocal` only when necessary
- Consider readability

### ❌ DON'T:
- Create deeply nested closures (2-3 levels max)
- Capture mutable objects without care
- Use closures for complex state (use classes)
- Forget about the loop variable pitfall
- Sacrifice clarity for cleverness

## Quick Reference Table

| Feature | Syntax | Use Case |
|---------|--------|----------|
| Basic closure | `def outer(): def inner(): pass` | Remember variables |
| Modify outer var | `nonlocal var` | Change enclosing scope |
| Multiple returns | `return f1, f2, f3` | Multiple closures |
| Private data | Return dict of functions | Encapsulation |
| Factory | `make_thing(config)` | Specialized functions |
| Decorator | `def deco(func): def wrap(): pass` | Wrap functions |

## Common Use Cases Summary

```python
# 1. Counter
def make_counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc

# 2. Adder
def make_adder(n):
    return lambda x: x + n

# 3. Formatter
def make_formatter(pre, suf):
    return lambda text: f"{pre}{text}{suf}"

# 4. Range checker
def make_range_checker(min, max):
    return lambda x: min <= x <= max

# 5. Cache
def make_cached(func):
    cache = {}
    def cached(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return cached
```

## Memory Tip

**Closures = Functions + Their Environment**

Think of closures as a "backpack" that the function carries around, containing all the variables it needs from its birthplace.

---

**Key Insight**: Closures are not just about nested functions - they're about functions that **remember their environment**. Master this concept, and decorators, callbacks, and functional programming patterns become much easier!

---

## Runnable Example: `closures_mini_project.py`

```python
"""
Closures Mini-Project: Event Management System
This project demonstrates how to use closures to create a simple event
management system with event handlers, state management, and callbacks.
"""

import time
from datetime import datetime

if __name__ == "__main__":

    print("=" * 70)
    print("CLOSURES MINI-PROJECT: EVENT MANAGEMENT SYSTEM")
    print("=" * 70)

    # ============================================================================
    # EVENT EMITTER USING CLOSURES
    # ============================================================================
    print("\n1. EVENT EMITTER")
    print("-" * 70)

    def create_event_emitter():
        """
        Create an event emitter that allows subscribing to events and
        triggering callbacks. Uses closures to maintain the list of listeners.
        """
        listeners = {}  # Private to the closure

        def on(event_name, callback):
            """Subscribe to an event"""
            if event_name not in listeners:
                listeners[event_name] = []
            listeners[event_name].append(callback)
            print(f"✓ Subscribed to '{event_name}'")

        def off(event_name, callback):
            """Unsubscribe from an event"""
            if event_name in listeners and callback in listeners[event_name]:
                listeners[event_name].remove(callback)
                print(f"✓ Unsubscribed from '{event_name}'")

        def emit(event_name, *args, **kwargs):
            """Trigger an event and call all subscribers"""
            if event_name in listeners:
                print(f"📢 Emitting '{event_name}' event")
                for callback in listeners[event_name]:
                    callback(*args, **kwargs)
            else:
                print(f"⚠️  No listeners for '{event_name}'")

        def get_listener_count(event_name=None):
            """Get number of listeners"""
            if event_name:
                return len(listeners.get(event_name, []))
            return sum(len(v) for v in listeners.values())

        return {
            'on': on,
            'off': off,
            'emit': emit,
            'listener_count': get_listener_count
        }

    # Create an event emitter
    emitter = create_event_emitter()

    # Create event handlers using closures
    def make_user_handler(user_id):
        """Factory function to create user-specific handlers"""
        login_count = 0

        def on_login():
            nonlocal login_count
            login_count += 1
            print(f"  User {user_id} logged in (total: {login_count} times)")

        def on_logout():
            print(f"  User {user_id} logged out")

        return on_login, on_logout

    # Subscribe to events
    user1_login, user1_logout = make_user_handler("user_001")
    user2_login, user2_logout = make_user_handler("user_002")

    emitter['on']('user_login', user1_login)
    emitter['on']('user_logout', user1_logout)
    emitter['on']('user_login', user2_login)

    print(f"Total listeners: {emitter['listener_count']()}")

    # Trigger events
    print("\nSimulating user activity:")
    emitter['emit']('user_login')
    emitter['emit']('user_login')
    emitter['emit']('user_logout')

    # ============================================================================
    # STATE MACHINE USING CLOSURES
    # ============================================================================
    print("\n\n2. STATE MACHINE")
    print("-" * 70)

    def create_state_machine(initial_state, transitions):
        """
        Create a state machine using closures.
        Maintains current state privately.
        """
        current_state = initial_state
        history = [initial_state]

        def get_state():
            """Get current state"""
            return current_state

        def transition(event):
            """Attempt to transition to a new state"""
            nonlocal current_state

            if current_state in transitions and event in transitions[current_state]:
                new_state = transitions[current_state][event]
                print(f"  {current_state} --[{event}]--> {new_state}")
                current_state = new_state
                history.append(current_state)
                return True
            else:
                print(f"  ⚠️ Invalid transition: {event} from {current_state}")
                return False

        def get_history():
            """Get state history"""
            return history.copy()

        def reset():
            """Reset to initial state"""
            nonlocal current_state
            current_state = initial_state
            history.clear()
            history.append(initial_state)
            print(f"  Reset to {initial_state}")

        return {
            'state': get_state,
            'transition': transition,
            'history': get_history,
            'reset': reset
        }

    # Create a door state machine
    door_transitions = {
        'closed': {'open': 'open'},
        'open': {'close': 'closed'},
    }

    door = create_state_machine('closed', door_transitions)

    print(f"Initial state: {door['state']()}")
    print("\nDoor operations:")
    door['transition']('open')
    door['transition']('close')
    door['transition']('close')  # Invalid
    door['transition']('open')
    print(f"\nHistory: {' -> '.join(door['history']())}")

    # ============================================================================
    # RATE-LIMITED API CLIENT
    # ============================================================================
    print("\n\n3. RATE-LIMITED API CLIENT")
    print("-" * 70)

    def create_rate_limited_client(max_requests, time_window):
        """
        Create an API client with rate limiting using closures.
        Tracks request times privately.
        """
        request_times = []
        request_count = 0

        def make_request(endpoint):
            """Make an API request with rate limiting"""
            nonlocal request_count
            now = time.time()

            # Remove old requests outside the time window
            request_times[:] = [t for t in request_times if now - t < time_window]

            if len(request_times) >= max_requests:
                wait_time = time_window - (now - request_times[0])
                print(f"  ⏸️  Rate limit reached. Wait {wait_time:.1f}s")
                return None

            request_times.append(now)
            request_count += 1
            print(f"  ✓ Request #{request_count} to {endpoint}")
            return {"status": "success", "endpoint": endpoint}

        def get_stats():
            """Get request statistics"""
            return {
                'total_requests': request_count,
                'recent_requests': len(request_times),
                'limit': max_requests,
                'window': time_window
            }

        def reset_stats():
            """Reset request statistics"""
            nonlocal request_count
            request_times.clear()
            request_count = 0
            print("  Stats reset")

        return {
            'request': make_request,
            'stats': get_stats,
            'reset': reset_stats
        }

    # Create a rate-limited client (3 requests per 1 second)
    api_client = create_rate_limited_client(max_requests=3, time_window=1.0)

    print("Making API requests (max 3 per second):")
    for i in range(5):
        result = api_client['request'](f'/api/users/{i}')
        time.sleep(0.2)

    stats = api_client['stats']()
    print(f"\nStats: {stats}")

    # ============================================================================
    # CONFIGURABLE VALIDATORS
    # ============================================================================
    print("\n\n4. CONFIGURABLE VALIDATORS")
    print("-" * 70)

    def create_validator(rules):
        """
        Create a validator with configurable rules using closures.
        """
        validation_count = 0
        failed_count = 0

        def validate(data):
            """Validate data against rules"""
            nonlocal validation_count, failed_count
            validation_count += 1
            errors = []

            for field, rule in rules.items():
                if field not in data:
                    errors.append(f"Missing field: {field}")
                elif not rule['check'](data[field]):
                    errors.append(f"{field}: {rule['message']}")

            if errors:
                failed_count += 1
                return {'valid': False, 'errors': errors}

            return {'valid': True, 'errors': []}

        def get_stats():
            """Get validation statistics"""
            return {
                'total': validation_count,
                'failed': failed_count,
                'success_rate': f"{((validation_count - failed_count) / validation_count * 100):.1f}%"
                    if validation_count > 0 else "N/A"
            }

        return {
            'validate': validate,
            'stats': get_stats
        }

    # Create validators with different rules
    user_rules = {
        'username': {
            'check': lambda x: len(x) >= 3,
            'message': 'Must be at least 3 characters'
        },
        'email': {
            'check': lambda x: '@' in x and '.' in x,
            'message': 'Must be a valid email'
        },
        'age': {
            'check': lambda x: isinstance(x, int) and 18 <= x <= 120,
            'message': 'Must be between 18 and 120'
        }
    }

    user_validator = create_validator(user_rules)

    # Test validation
    test_users = [
        {'username': 'alice', 'email': 'alice@example.com', 'age': 25},
        {'username': 'bo', 'email': 'invalid', 'age': 15},
        {'username': 'charlie', 'email': 'charlie@test.com', 'age': 30},
    ]

    print("Validating users:")
    for user in test_users:
        result = user_validator['validate'](user)
        if result['valid']:
            print(f"  ✓ {user['username']}: Valid")
        else:
            print(f"  ✗ {user['username']}: {', '.join(result['errors'])}")

    print(f"\nValidation stats: {user_validator['stats']()}")

    # ============================================================================
    # CACHE WITH EXPIRATION
    # ============================================================================
    print("\n\n5. CACHE WITH EXPIRATION")
    print("-" * 70)

    def create_cache(ttl=5):
        """
        Create a cache with time-to-live using closures.
        """
        cache = {}
        hits = 0
        misses = 0

        def get(key):
            """Get value from cache"""
            nonlocal hits, misses

            if key in cache:
                value, timestamp = cache[key]
                if time.time() - timestamp < ttl:
                    hits += 1
                    print(f"  💾 Cache HIT for '{key}'")
                    return value
                else:
                    del cache[key]
                    print(f"  ⌛ Cache EXPIRED for '{key}'")

            misses += 1
            print(f"  ❌ Cache MISS for '{key}'")
            return None

        def set(key, value):
            """Set value in cache"""
            cache[key] = (value, time.time())
            print(f"  ✓ Cached '{key}'")

        def clear():
            """Clear all cache"""
            cache.clear()
            print(f"  🗑️  Cache cleared")

        def get_stats():
            """Get cache statistics"""
            total = hits + misses
            return {
                'hits': hits,
                'misses': misses,
                'hit_rate': f"{(hits / total * 100):.1f}%" if total > 0 else "N/A",
                'size': len(cache)
            }

        return {
            'get': get,
            'set': set,
            'clear': clear,
            'stats': get_stats
        }

    # Create cache with 2-second TTL
    cache = create_cache(ttl=2)

    print("Testing cache:")
    cache['set']('user_123', {'name': 'Alice', 'age': 30})
    cache['get']('user_123')  # Hit
    time.sleep(1)
    cache['get']('user_123')  # Hit
    time.sleep(1.5)
    cache['get']('user_123')  # Expired
    cache['set']('user_123', {'name': 'Alice', 'age': 30})
    cache['get']('user_123')  # Hit

    print(f"\nCache stats: {cache['stats']()}")

    # ============================================================================
    # COMMAND PATTERN WITH UNDO
    # ============================================================================
    print("\n\n6. COMMAND PATTERN WITH UNDO")
    print("-" * 70)

    def create_command_manager():
        """
        Create a command manager with undo/redo using closures.
        """
        history = []
        current_index = -1

        def execute(command, undo_command):
            """Execute a command and save for undo"""
            nonlocal current_index

            command()
            current_index += 1

            # Remove any commands after current index (for redo)
            history[:] = history[:current_index]
            history.append((command, undo_command))

            print(f"  ✓ Command executed (history size: {len(history)})")

        def undo():
            """Undo last command"""
            nonlocal current_index

            if current_index >= 0:
                _, undo_command = history[current_index]
                undo_command()
                current_index -= 1
                print(f"  ↶ Undo executed")
                return True

            print(f"  ⚠️ Nothing to undo")
            return False

        def redo():
            """Redo last undone command"""
            nonlocal current_index

            if current_index < len(history) - 1:
                current_index += 1
                command, _ = history[current_index]
                command()
                print(f"  ↷ Redo executed")
                return True

            print(f"  ⚠️ Nothing to redo")
            return False

        def get_history_size():
            """Get size of command history"""
            return len(history)

        return {
            'execute': execute,
            'undo': undo,
            'redo': redo,
            'history_size': get_history_size
        }

    # Create command manager
    cmd_manager = create_command_manager()

    # Simulate a simple text editor
    text = []

    def add_text(word):
        """Command to add text"""
        def do():
            text.append(word)
            print(f"    Added: '{word}' -> {text}")

        def undo():
            text.pop()
            print(f"    Removed: '{word}' -> {text}")

        cmd_manager['execute'](do, undo)

    print("Text editor simulation:")
    add_text("Hello")
    add_text("World")
    add_text("!")

    print("\nUndo operations:")
    cmd_manager['undo']()
    cmd_manager['undo']()

    print("\nRedo operations:")
    cmd_manager['redo']()

    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("\n" + "=" * 70)
    print("PROJECT SUMMARY")
    print("=" * 70)
    print("""
    This mini-project demonstrated practical closure usage:

    ✅ Patterns Demonstrated:
       1. Event Emitter - Subscribe/publish with private listener list
       2. State Machine - Maintain state with transition rules
       3. Rate Limiter - Track requests with time windows
       4. Validators - Configurable validation with statistics
       5. Cache - Time-based expiration with hit/miss tracking
       6. Command Pattern - Undo/redo functionality

    ✅ Key Closure Concepts:
       - Private variables (listeners, state, cache, history)
       - Multiple functions sharing state (nonlocal)
       - Factory functions (make_user_handler)
       - Encapsulation without classes
       - Stateful behavior

    ✅ Real-World Applications:
       - Event-driven systems (UI frameworks, game engines)
       - State management (workflows, processes)
       - API clients with rate limiting
       - Form validation systems
       - Caching layers
       - Undo/redo functionality (text editors, drawing apps)

    ✅ Benefits of Using Closures:
       - Clean, encapsulated code
       - No class boilerplate needed
       - Natural state management
       - Easy to test individual components
       - Functional programming style

    Try extending this project by adding:
       - Priority-based event emitters
       - State machine with entry/exit actions
       - LRU cache eviction policy
       - Async validators
       - Transaction support for commands
    """)

    print("=" * 70)
    print("END OF MINI-PROJECT")
    print("=" * 70)
```

---

## Exercises


**Exercise 1.**
Write a closure `make_filter(threshold)` that returns a function. The returned function takes a list of numbers and returns only those greater than `threshold`.

??? success "Solution to Exercise 1"

        ```python
        def make_filter(threshold):
            def filter_func(numbers):
                return [n for n in numbers if n > threshold]
            return filter_func

        above_10 = make_filter(10)
        print(above_10([5, 15, 8, 20, 3]))  # [15, 20]
        ```

    The closure captures `threshold` and uses it in the list comprehension filter.

---

**Exercise 2.**
Write a closure `make_logger(prefix)` that returns a function. The returned function takes a message and prints `f"[{prefix}] {message}"`. Also include a counter using `nonlocal` that tracks how many messages have been logged.

??? success "Solution to Exercise 2"

        ```python
        def make_logger(prefix):
            count = 0
            def log(message):
                nonlocal count
                count += 1
                print(f"[{prefix}] ({count}) {message}")
            return log

        info = make_logger("INFO")
        info("Server started")    # [INFO] (1) Server started
        info("Request received")  # [INFO] (2) Request received
        ```

    The closure captures both `prefix` (read-only) and `count` (modified via `nonlocal`).

---

**Exercise 3.**
Identify the bug in the following code. Fix it so that each function in the list returns its index (0, 1, 2, 3).

```python
funcs = []
for i in range(4):
    funcs.append(lambda: i)

print([f() for f in funcs])  # Expected: [0, 1, 2, 3]
```

??? success "Solution to Exercise 3"

    The bug is late binding: all lambdas capture the variable `i` by reference, and by the time they are called, `i` is `3`. Fix it by using a default argument to capture the current value:

        ```python
        funcs = []
        for i in range(4):
            funcs.append(lambda i=i: i)

        print([f() for f in funcs])  # [0, 1, 2, 3]
        ```

    The default argument `i=i` captures the value of `i` at the time each lambda is created, rather than referencing the loop variable.
