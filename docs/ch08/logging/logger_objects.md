# Logger Objects

Create and configure logger objects for modular logging throughout your application.

!!! tip "Mental Model"
    Loggers form a tree rooted at the root logger. Each module creates its own logger with `logging.getLogger(__name__)`, and the dot-separated name mirrors the package hierarchy. A message propagates up the tree until a handler catches it, so configuring a parent logger automatically covers all its children.

## Creating Loggers

Create named loggers for different modules.

```python
import logging

# Get loggers for different modules
logger_app = logging.getLogger('app')
logger_db = logging.getLogger('app.database')
logger_api = logging.getLogger('app.api')

# Loggers have hierarchical names
print(f"App logger: {logger_app.name}")
print(f"DB logger: {logger_db.name}")
print(f"API logger: {logger_api.name}")
```

```
App logger: app
DB logger: app.database
API logger: app.api
```

## Logger Configuration

Configure individual loggers with handlers and formatters.

```python
import logging

# Create logger
logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG)

# Remove existing handlers
logger.handlers.clear()

# Create handler
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

# Create formatter
fmt = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(fmt)

# Add handler to logger
logger.addHandler(handler)

# Log messages
logger.info("Starting application")
logger.debug("Debug info")
```

```
myapp - INFO - Starting application
myapp - DEBUG - Debug info
```

---

## Exercises

**Exercise 1.**
Create a logger hierarchy with `"app"`, `"app.db"`, and `"app.api"`. Set the `"app"` logger to INFO level and add a handler. Log messages from each child logger and verify they propagate to the parent handler.

??? success "Solution to Exercise 1"

    ```python
    import logging

    # Parent logger
    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))
    app_logger.addHandler(handler)

    # Child loggers (no handlers needed — propagation)
    db_logger = logging.getLogger("app.db")
    api_logger = logging.getLogger("app.api")

    db_logger.info("Connected to database")
    api_logger.warning("Rate limit approaching")
    # app.db - INFO - Connected to database
    # app.api - WARNING - Rate limit approaching
    ```

---

**Exercise 2.**
Write a function `get_or_create_logger` that takes a name and level, and returns a logger. If the logger already has handlers, return it as-is; otherwise, add a `StreamHandler` with a standard format. This prevents duplicate handler accumulation.

??? success "Solution to Exercise 2"

    ```python
    import logging

    def get_or_create_logger(name, level=logging.INFO):
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.setLevel(level)
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter("%(name)s - %(levelname)s - %(message)s")
            )
            logger.addHandler(handler)
        return logger

    # Test
    log1 = get_or_create_logger("myservice")
    log2 = get_or_create_logger("myservice")  # Returns same, no new handler
    print(len(log1.handlers))  # 1
    ```

---

**Exercise 3.**
Write a function `logger_info` that takes a logger name and returns a dictionary with `"name"`, `"level"`, `"handler_count"`, and `"effective_level"` (the level inherited from parents if not set explicitly). Test with both configured and unconfigured loggers.

??? success "Solution to Exercise 3"

    ```python
    import logging

    def logger_info(name):
        logger = logging.getLogger(name)
        return {
            "name": logger.name,
            "level": logging.getLevelName(logger.level),
            "handler_count": len(logger.handlers),
            "effective_level": logging.getLevelName(logger.getEffectiveLevel()),
        }

    # Test
    logging.basicConfig(level=logging.WARNING)
    print(logger_info("root"))
    # {'name': 'root', 'level': 'WARNING', ...}
    print(logger_info("unset.child"))
    # effective_level inherits from root: WARNING
    ```
