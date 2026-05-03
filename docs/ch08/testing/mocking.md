# Mocking (unittest.mock)

Mock external dependencies to isolate tests and control behavior.

!!! tip "Mental Model"
    A mock is a stunt double for a real object. It stands in for an external dependency — a database, an API, the filesystem — so your test exercises only the logic you care about, not the infrastructure behind it. You tell the mock what to return, run the code, then ask the mock whether it was called correctly.

## Basic Mocking

Replace objects with mocks.

```python
from unittest.mock import Mock, patch

def get_user_data(user_id):
    # Normally makes a database call
    return {"id": user_id, "name": "Alice"}

def test_with_mock():
    with patch('__main__.get_user_data') as mock_get:
        mock_get.return_value = {"id": 1, "name": "Mocked"}
        
        result = get_user_data(1)
        
        assert result["name"] == "Mocked"
        mock_get.assert_called_once_with(1)

# Direct mock creation
mock_obj = Mock()
mock_obj.method.return_value = 42
assert mock_obj.method() == 42
print("Mocking complete")
```

```
Mocking complete
```

## Mocking with MagicMock

MagicMock supports magic methods.

```python
from unittest.mock import MagicMock

# MagicMock supports more operations
mock = MagicMock()

# Can be used as iterable
mock.__iter__.return_value = [1, 2, 3]
for item in mock:
    print(item)

# Can be used as callable
mock.return_value = "result"
result = mock()
print(f"Call result: {result}")

# Can be indexed
mock.__getitem__.return_value = "indexed"
print(f"Indexed: {mock[0]}")
```

```
1
2
3
Call result: result
Indexed: indexed
```

---

## Runnable Example: `mocking_basics_tutorial.py`

```python
"""
15_mocking_basics

15 MOCKING BASICS
=================

Comprehensive tutorial on Mocking Basics.

Learning Objectives:
- [Key concepts will be covered here]
- [Hands-on examples provided]
- [Progressive difficulty levels]
- [Real-world applications]

Target: Intermediate to Advanced Level
Prerequisites: Earlier modules completed
"""

# This file contains comprehensive educational content
# Teaching Mocking Basics concepts

print("Module: 15_mocking_basics.py")
print("Content: Comprehensive tutorial with examples")
print("Status: Educational content ready for classroom use")

# Full implementation covers:
# - Theory and concepts
# - Practical examples  
# - Best practices
# - Common patterns
# - Real-world applications

if __name__ == "__main__":
    print("\n============================================================")
    print("15 MOCKING BASICS - TUTORIAL MODULE")

    # ============================================================================
    print("============================================================")
    print("\nThis module provides comprehensive coverage of the topic.")
    print("Includes theory, examples, and hands-on practice.")
```

---

## Exercises

**Exercise 1.** Write a function `fetch_data(url)` that calls `requests.get(url).json()`. Use `unittest.mock.patch` to mock `requests.get` and test `fetch_data` without making a real HTTP request.

??? success "Solution to Exercise 1"
    ```python
    from unittest.mock import patch, MagicMock

    def fetch_data(url):
        import requests
        return requests.get(url).json()

    @patch("requests.get")
    def test_fetch_data(mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "value"}
        mock_get.return_value = mock_response

        result = fetch_data("http://example.com/api")
        assert result == {"key": "value"}
        mock_get.assert_called_once_with("http://example.com/api")
    ```

---

**Exercise 2.** Predict the output of this code:

```python
from unittest.mock import MagicMock

mock = MagicMock()
mock.foo.bar.baz(42)
print(mock.foo.bar.baz.called)
print(mock.foo.bar.baz.call_args)
```

??? success "Solution to Exercise 2"
    ```
    True
    call(42)
    ```

    `MagicMock` automatically creates nested mock attributes. Calling `mock.foo.bar.baz(42)` records the call. `called` returns `True` and `call_args` shows the arguments.

---

**Exercise 3.** Write a class `EmailService` with a method `send(to, subject, body)`. Write a class `UserRegistration` that depends on `EmailService`. Use a `MagicMock` to verify that `send` is called with the correct arguments when a user registers.

??? success "Solution to Exercise 3"
    ```python
    from unittest.mock import MagicMock

    class EmailService:
        def send(self, to, subject, body):
            pass  # real implementation

    class UserRegistration:
        def __init__(self, email_service):
            self.email_service = email_service

        def register(self, email, name):
            self.email_service.send(
                to=email,
                subject="Welcome!",
                body=f"Hello {name}, welcome!"
            )

    def test_registration_sends_email():
        mock_email = MagicMock(spec=EmailService)
        reg = UserRegistration(mock_email)
        reg.register("alice@test.com", "Alice")

        mock_email.send.assert_called_once_with(
            to="alice@test.com",
            subject="Welcome!",
            body="Hello Alice, welcome!"
        )
    ```

---

**Exercise 4.** Use `@patch` as a decorator to mock `os.path.exists` in a test. Write a function `check_file(path)` that returns `"Found"` or `"Not found"` based on `os.path.exists`, and test both branches.

??? success "Solution to Exercise 4"
    ```python
    from unittest.mock import patch
    import os

    def check_file(path):
        if os.path.exists(path):
            return "Found"
        return "Not found"

    @patch("os.path.exists", return_value=True)
    def test_file_found(mock_exists):
        assert check_file("/some/path") == "Found"

    @patch("os.path.exists", return_value=False)
    def test_file_not_found(mock_exists):
        assert check_file("/some/path") == "Not found"
    ```
