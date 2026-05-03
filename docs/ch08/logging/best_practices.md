# Logging Best Practices

Guidelines for effective logging in production applications.

!!! tip "Mental Model"
    Good logging is like a flight recorder: it captures just enough detail at each level so you can reconstruct what happened after the fact. Use named loggers per module, log at the right level, never log sensitive data, and configure output in one place. These habits turn logs from noisy clutter into a reliable debugging tool.

## Use Named Loggers

Create loggers for each module using __name__.

```python
import logging

# In each module, use __name__ for the logger
logger = logging.getLogger(__name__)

def process_data(data):
    logger.debug(f"Processing data: {data}")
    try:
        result = sum(data)
        logger.info(f"Processed successfully: {result}")
        return result
    except Exception as e:
        logger.error(f"Error processing: {e}")
        raise

logging.basicConfig(level=logging.DEBUG)
process_data([1, 2, 3])
```

```
DEBUG:__main__:Processing data: [1, 2, 3]
INFO:__main__:Processed successfully: 6
```

## Structured Logging

Include context in log messages.

```python
import logging
import json

logger = logging.getLogger(__name__)

class StructuredFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'logger': record.name
        }
        return json.dumps(log_obj)

handler = logging.StreamHandler()
handler.setFormatter(StructuredFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("User login", extra={'user_id': 123})
```

```
{"timestamp": "2026-02-12 12:34:56,789", "level": "INFO", "message": "User login", "logger": "__main__"}
```

---

## Exercises

**Exercise 1.**
Create a named logger for a module called `"myapp.database"`. Configure it with a `StreamHandler` that uses the format `"%(name)s - %(levelname)s - %(message)s"`. Log an INFO message `"Connection established"` and a WARNING message `"Slow query detected"`. Verify the output includes the logger name.

??? success "Solution to Exercise 1"

    ```python
    import logging

    logger = logging.getLogger("myapp.database")
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info("Connection established")
    logger.warning("Slow query detected")
    # myapp.database - INFO - Connection established
    # myapp.database - WARNING - Slow query detected
    ```

---

**Exercise 2.**
Write a function `setup_file_logger` that creates a logger writing to a specified file path with rotation (using `RotatingFileHandler` with `maxBytes=1024` and `backupCount=3`). The format should include the timestamp, level, and message. Return the configured logger.

??? success "Solution to Exercise 2"

    ```python
    import logging
    from logging.handlers import RotatingFileHandler

    def setup_file_logger(name, file_path):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        handler = RotatingFileHandler(
            file_path, maxBytes=1024, backupCount=3
        )
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    # Usage:
    # logger = setup_file_logger("myapp", "app.log")
    # logger.info("Application started")
    ```

---

**Exercise 3.**
Write a context manager `log_execution_time` that logs the start and end of a code block, along with the elapsed time in seconds. Use a logger (not print) for all output. For example, `with log_execution_time(logger, "data processing"):` should log `"Starting data processing"` and `"Finished data processing in 0.5s"`.

??? success "Solution to Exercise 3"

    ```python
    import logging
    import time
    from contextlib import contextmanager

    @contextmanager
    def log_execution_time(logger, task_name):
        logger.info(f"Starting {task_name}")
        start = time.time()
        try:
            yield
        finally:
            elapsed = time.time() - start
            logger.info(f"Finished {task_name} in {elapsed:.2f}s")

    # Test
    logger = logging.getLogger("timer")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    with log_execution_time(logger, "data processing"):
        time.sleep(0.1)  # Simulate work
    ```
