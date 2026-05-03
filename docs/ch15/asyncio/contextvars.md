# Context Variables (contextvars)

`contextvars` provides context-local state that works correctly with both threads and async tasks.

!!! tip "Mental Model"
    Think of a context variable as an invisible backpack that each async task carries independently. Unlike `threading.local()`, which attaches data to threads, `contextvars` attaches data to logical tasks -- so when multiple coroutines share the same thread but take turns running, each one still sees its own private data after every `await`.

## Why contextvars?

### The Problem with threading.local in Async

```python
import threading
import asyncio

# threading.local() doesn't work properly with async
local = threading.local()

async def task(name):
    local.name = name
    await asyncio.sleep(0.1)
    # BUG: May see wrong value after await!
    print(f"Task: {local.name}")

async def main():
    await asyncio.gather(
        task("task1"),
        task("task2")
    )

# Both might print "task2" because they share the same thread
```

### The Solution: contextvars

```python
import contextvars
import asyncio

# contextvars works correctly with async
name_var = contextvars.ContextVar('name')

async def task(name):
    name_var.set(name)
    await asyncio.sleep(0.1)
    # Correct: Each task sees its own value
    print(f"Task: {name_var.get()}")

async def main():
    await asyncio.gather(
        task("task1"),
        task("task2")
    )
    # Output: "task1" and "task2" correctly

asyncio.run(main())
```

## Basic Usage

### Creating and Using ContextVar

```python
import contextvars

# Create a context variable
request_id = contextvars.ContextVar('request_id', default=None)

# Set value
request_id.set('req-123')

# Get value
print(request_id.get())  # 'req-123'

# Get with default (if not set)
other_var = contextvars.ContextVar('other')
print(other_var.get('default'))  # 'default'
print(other_var.get())  # Raises LookupError if no default
```

### Token-Based Reset

```python
import contextvars

var = contextvars.ContextVar('var', default='initial')

# set() returns a token
token = var.set('new_value')
print(var.get())  # 'new_value'

# Reset to previous value using token
var.reset(token)
print(var.get())  # 'initial'
```

## Context Management

### Working with Context Objects

```python
import contextvars

var = contextvars.ContextVar('var')

# Get current context
ctx = contextvars.copy_context()

# Run function in context
def show_value():
    return var.get('not set')

# Set in current context
var.set('hello')
print(ctx.run(show_value))  # 'not set' (ctx was copied before set)

# Create new context with modifications
ctx2 = contextvars.copy_context()
print(ctx2.run(show_value))  # 'hello'
```

### Running in Isolated Context

```python
import contextvars

request_id = contextvars.ContextVar('request_id')

def process_request(req_id):
    request_id.set(req_id)
    # ... do work ...
    return request_id.get()

# Run in isolated context
ctx = contextvars.copy_context()
result = ctx.run(process_request, 'req-123')

# Original context unaffected
print(request_id.get('not set'))  # 'not set'
```

## Async Task Context

### Automatic Context Copying

```python
import asyncio
import contextvars

user_id = contextvars.ContextVar('user_id')

async def get_user_data():
    # Each task has its own copy of context
    uid = user_id.get()
    await asyncio.sleep(0.1)
    return f"Data for user {uid}"

async def handle_request(uid):
    user_id.set(uid)
    # Task created here inherits context
    task = asyncio.create_task(get_user_data())
    return await task

async def main():
    results = await asyncio.gather(
        handle_request('user-1'),
        handle_request('user-2')
    )
    print(results)
    # ['Data for user user-1', 'Data for user user-2']

asyncio.run(main())
```

### Context in Callbacks

```python
import asyncio
import contextvars

var = contextvars.ContextVar('var')

async def main():
    var.set('main_value')
    
    loop = asyncio.get_running_loop()
    
    def callback():
        # Callback runs in context where it was scheduled
        print(f"Callback: {var.get()}")
    
    # Schedule callback - captures current context
    loop.call_soon(callback)
    
    await asyncio.sleep(0.1)

asyncio.run(main())  # Prints: "Callback: main_value"
```

## Practical Examples

### 1. Request Context in Web Framework

```python
import contextvars
from contextlib import contextmanager

# Context variables for request
request_id = contextvars.ContextVar('request_id')
current_user = contextvars.ContextVar('current_user')

@contextmanager
def request_context(req_id, user):
    """Set request context for the duration of handling."""
    token_id = request_id.set(req_id)
    token_user = current_user.set(user)
    try:
        yield
    finally:
        request_id.reset(token_id)
        current_user.reset(token_user)

def get_request_id():
    return request_id.get(None)

def get_current_user():
    return current_user.get(None)

# Usage in async handler
async def handle_request(req_id, user):
    with request_context(req_id, user):
        # All code here sees the context
        result = await process_request()
        log_request()  # Can access request_id
        return result

def log_request():
    print(f"Request {get_request_id()} by {get_current_user()}")
```

### 2. Database Transaction Context

```python
import contextvars
from contextlib import asynccontextmanager

_transaction = contextvars.ContextVar('transaction', default=None)

@asynccontextmanager
async def transaction(conn):
    """Provide transaction context."""
    tx = await conn.begin()
    token = _transaction.set(tx)
    try:
        yield tx
        await tx.commit()
    except Exception:
        await tx.rollback()
        raise
    finally:
        _transaction.reset(token)

def get_transaction():
    """Get current transaction or raise."""
    tx = _transaction.get()
    if tx is None:
        raise RuntimeError("No active transaction")
    return tx

async def save_user(user):
    tx = get_transaction()
    await tx.execute("INSERT INTO users ...")
```

### 3. Logging Context

```python
import contextvars
import logging

# Context for logging
log_context = contextvars.ContextVar('log_context', default={})

class ContextFilter(logging.Filter):
    def filter(self, record):
        ctx = log_context.get()
        for key, value in ctx.items():
            setattr(record, key, value)
        return True

def with_log_context(**kwargs):
    """Add context to all logs in this scope."""
    current = log_context.get().copy()
    current.update(kwargs)
    return log_context.set(current)

# Usage
async def handle_request(request_id, user_id):
    token = with_log_context(request_id=request_id, user_id=user_id)
    try:
        logger.info("Processing request")  # Includes context
        await do_work()
        logger.info("Request completed")
    finally:
        log_context.reset(token)
```

### 4. Timeout Context

```python
import contextvars
import asyncio
import time

deadline = contextvars.ContextVar('deadline', default=None)

def get_remaining_time():
    """Get remaining time until deadline."""
    dl = deadline.get()
    if dl is None:
        return float('inf')
    return max(0, dl - time.time())

@asynccontextmanager
async def timeout(seconds):
    """Set deadline for operations."""
    new_deadline = time.time() + seconds
    current = deadline.get()
    
    # Use earliest deadline
    if current is not None:
        new_deadline = min(new_deadline, current)
    
    token = deadline.set(new_deadline)
    try:
        yield
    finally:
        deadline.reset(token)

async def fetch_with_deadline(url):
    remaining = get_remaining_time()
    if remaining <= 0:
        raise asyncio.TimeoutError("Deadline exceeded")
    
    async with aiohttp.ClientSession() as session:
        async with asyncio.timeout(remaining):
            async with session.get(url) as r:
                return await r.text()
```

## Comparison: threading.local vs contextvars

| Feature | threading.local | contextvars |
|---------|-----------------|-------------|
| Thread isolation | ✅ | ✅ |
| Async task isolation | ❌ | ✅ |
| Automatic context copy | ❌ | ✅ |
| Reset to previous value | ❌ | ✅ (tokens) |
| Explicit context objects | ❌ | ✅ |
| Python version | 2.4+ | 3.7+ |

## Best Practices

### 1. Use Meaningful Names

```python
# Good: Descriptive names
request_id = contextvars.ContextVar('request_id')
current_user = contextvars.ContextVar('current_user')

# Bad: Generic names
var1 = contextvars.ContextVar('var1')
```

### 2. Provide Defaults When Appropriate

```python
# With default
log_level = contextvars.ContextVar('log_level', default='INFO')

# Without default (requires explicit set)
auth_token = contextvars.ContextVar('auth_token')
```

### 3. Always Reset in Finally

```python
token = var.set('value')
try:
    # ... do work ...
finally:
    var.reset(token)

# Or use context manager
@contextmanager
def scoped_var(var, value):
    token = var.set(value)
    try:
        yield
    finally:
        var.reset(token)
```

### 4. Document Context Dependencies

```python
def process_order():
    """Process the current order.
    
    Requires:
        - current_user context variable to be set
        - request_id context variable to be set
    """
    user = current_user.get()  # Raises if not set
    req_id = request_id.get()
```

## Key Takeaways

- Use `contextvars` for state that should be isolated per async task
- Each `asyncio.create_task()` gets a copy of the current context
- Use tokens from `set()` to `reset()` values properly
- Works for both sync and async code
- Replaces `threading.local()` for async-aware context
- Essential for request context, transactions, logging in async apps

---

## Exercises

**Exercise 1.**
Create a `ContextVar` called `request_id`. Write an async function `handle_request(rid)` that sets the variable, awaits a helper coroutine `process()`, and prints the `request_id` after the helper returns. Run 3 concurrent `handle_request` calls with different IDs using `asyncio.gather()` and verify each task sees its own value.

??? success "Solution to Exercise 1"
        ```python
        import asyncio
        import contextvars

        request_id = contextvars.ContextVar("request_id", default=None)

        async def process():
            await asyncio.sleep(0.1)
            return f"processed by {request_id.get()}"

        async def handle_request(rid):
            request_id.set(rid)
            result = await process()
            print(f"Request {rid}: {result}")

        async def main():
            await asyncio.gather(
                handle_request("req-1"),
                handle_request("req-2"),
                handle_request("req-3"),
            )

        asyncio.run(main())
        ```

---

**Exercise 2.**
Demonstrate the token-based reset mechanism. Create a `ContextVar` with default `"initial"`. Set it to `"first"`, save the token, then set it to `"second"`. Reset using the token and verify the value is back to `"first"`. Reset again (if applicable) and verify it returns to `"initial"`.

??? success "Solution to Exercise 2"
        ```python
        import contextvars

        var = contextvars.ContextVar("var", default="initial")

        token1 = var.set("first")
        print(f"After set 'first': {var.get()}")

        token2 = var.set("second")
        print(f"After set 'second': {var.get()}")

        var.reset(token2)
        print(f"After reset token2: {var.get()}")  # "first"

        var.reset(token1)
        print(f"After reset token1: {var.get()}")  # "initial"
        ```

---

**Exercise 3.**
Write a `request_context` context manager (using `contextlib.contextmanager`) that accepts `user` and `trace_id`, sets two `ContextVar` values on entry, and resets them on exit. Verify that after exiting the context, the variables return to their defaults.

??? success "Solution to Exercise 3"
        ```python
        import contextvars
        from contextlib import contextmanager

        current_user = contextvars.ContextVar("current_user", default=None)
        trace_id = contextvars.ContextVar("trace_id", default=None)

        @contextmanager
        def request_context(user, tid):
            token_user = current_user.set(user)
            token_trace = trace_id.set(tid)
            try:
                yield
            finally:
                current_user.reset(token_user)
                trace_id.reset(token_trace)

        # Verify defaults before
        print(f"Before: user={current_user.get()}, trace={trace_id.get()}")

        with request_context("alice", "trace-123"):
            print(f"Inside: user={current_user.get()}, trace={trace_id.get()}")

        # Verify defaults restored
        print(f"After: user={current_user.get()}, trace={trace_id.get()}")
        ```
