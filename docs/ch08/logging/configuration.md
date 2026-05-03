# Configuration (dictConfig, fileConfig)

Configure logging using dictConfig for Python dicts or fileConfig for configuration files.

!!! tip "Mental Model"
    Logging configuration wires together three things: *loggers* (who emits), *handlers* (where it goes), and *formatters* (how it looks). `dictConfig` lets you declare all three in a single dictionary, applied once at startup. This separates "what to log" in your code from "how to deliver it" in configuration — so you can redirect output without touching a single log call.

## dictConfig - Dictionary Configuration

Configure logging with a dictionary.

```python
import logging.config

config = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO'
        }
    },
    'loggers': {
        'myapp': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}

logging.config.dictConfig(config)
logger = logging.getLogger('myapp')
logger.info("Application started")
```

```
2026-02-12 12:34:56,789 - myapp - INFO - Application started
```

## fileConfig - Configuration File

Configure logging from an INI file.

```python
import logging.config
import tempfile
import os

# Create temporary config file
config_content = '''[loggers]
keys=root,myapp

[handlers]
keys=console

[formatters]
keys=standard

[logger_root]
level=WARNING
handlers=console

[logger_myapp]
level=DEBUG
handlers=console
qualname=myapp

[handler_console]
class=StreamHandler
level=DEBUG
formatter=standard
args=(sys.stdout,)

[formatter_standard]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
'''

# Write config to temp file
with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as f:
    f.write(config_content)
    config_path = f.name

try:
    logging.config.fileConfig(config_path)
    logger = logging.getLogger('myapp')
    logger.info("Configured from file")
finally:
    os.unlink(config_path)
```

```
2026-02-12 12:34:56,789 - myapp - INFO - Configured from file
```

---

## Exercises

**Exercise 1.**
Create a `dictConfig` configuration that sets up two handlers: a `StreamHandler` for WARNING and above, and a simulated `FileHandler` for DEBUG and above. Both should use different formatters. Apply the configuration and test by logging messages at DEBUG, INFO, and WARNING levels.

??? success "Solution to Exercise 1"

    ```python
    import logging
    import logging.config

    config = {
        "version": 1,
        "formatters": {
            "brief": {"format": "%(levelname)s: %(message)s"},
            "detailed": {
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "WARNING",
                "formatter": "brief",
            },
            "file": {
                "class": "logging.StreamHandler",  # Using stream for demo
                "level": "DEBUG",
                "formatter": "detailed",
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
        },
    }

    logging.config.dictConfig(config)
    logger = logging.getLogger()
    logger.debug("Debug message")    # Only in 'file' handler
    logger.warning("Warning message")  # In both handlers
    ```

---

**Exercise 2.**
Write a function `configure_from_dict` that takes a dictionary with keys `"level"`, `"format"`, and `"filename"` (optional), and returns a properly configured logger using `logging.config.dictConfig`. If `"filename"` is provided, log to a file; otherwise, log to the console.

??? success "Solution to Exercise 2"

    ```python
    import logging
    import logging.config

    def configure_from_dict(settings):
        handler_config = {
            "class": "logging.StreamHandler",
            "level": settings.get("level", "INFO"),
            "formatter": "default",
        }
        if "filename" in settings:
            handler_config["class"] = "logging.FileHandler"
            handler_config["filename"] = settings["filename"]

        config = {
            "version": 1,
            "formatters": {
                "default": {
                    "format": settings.get(
                        "format", "%(levelname)s - %(message)s"
                    )
                }
            },
            "handlers": {"main": handler_config},
            "root": {
                "level": settings.get("level", "INFO"),
                "handlers": ["main"],
            },
        }
        logging.config.dictConfig(config)
        return logging.getLogger()

    # Test
    logger = configure_from_dict({"level": "DEBUG", "format": "%(message)s"})
    logger.info("Hello from configured logger")
    ```

---

**Exercise 3.**
Write a logging configuration that creates a logger hierarchy: a root logger at WARNING, a `"myapp"` logger at INFO, and a `"myapp.debug"` logger at DEBUG. Demonstrate that each logger only processes messages at or above its configured level.

??? success "Solution to Exercise 3"

    ```python
    import logging

    # Root logger
    logging.basicConfig(level=logging.WARNING, format="%(name)s - %(levelname)s - %(message)s")

    # App logger
    app_logger = logging.getLogger("myapp")
    app_logger.setLevel(logging.INFO)

    # Debug logger
    debug_logger = logging.getLogger("myapp.debug")
    debug_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))
    debug_logger.addHandler(handler)

    debug_logger.debug("Debug detail")     # Shown (DEBUG level)
    app_logger.info("App info")            # Shown (INFO level)
    logging.warning("Root warning")         # Shown (WARNING level)
    ```
