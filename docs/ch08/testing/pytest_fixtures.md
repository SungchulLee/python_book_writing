# pytest Fixtures

Use pytest fixtures for setup/teardown and parameterized test data.

!!! tip "Mental Model"
    A fixture is a reusable setup recipe. You define it once as a function decorated with `@pytest.fixture`, and any test that names it as a parameter automatically receives its return value. Fixtures replace the `setUp`/`tearDown` ceremony of unittest with explicit dependency injection — each test declares exactly what it needs, nothing more.

## Creating and Using Fixtures

Define reusable test setup with fixtures.

```python
import pytest

@pytest.fixture
def sample_data():
    return {"users": ["Alice", "Bob"], "count": 2}

@pytest.fixture
def temp_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("test content")
    return file

def test_data_access(sample_data):
    assert len(sample_data["users"]) == 2
    assert sample_data["count"] == 2

def test_file_exists(temp_file):
    assert temp_file.exists()
    assert "test" in temp_file.read_text()

print("Fixtures can provide test data and resources")
```

```
Fixtures can provide test data and resources
```

## Fixture Scopes

Control when fixtures are created and destroyed.

```python
import pytest

@pytest.fixture(scope="function")  # Default, run for each test
def function_scope():
    return "function"

@pytest.fixture(scope="class")  # Shared per test class
def class_scope():
    return "class"

@pytest.fixture(scope="module")  # Shared per module
def module_scope():
    return "module"

@pytest.fixture(scope="session")  # Shared for entire session
def session_scope():
    return "session"

def test_scopes(function_scope):
    assert function_scope == "function"

print("Fixture scopes control resource lifecycle")
```

```
Fixture scopes control resource lifecycle
```


---

## Exercises

**Exercise 1.** Write a pytest fixture `sample_dict` that returns `{"name": "Alice", "age": 30}`. Use it in two tests: one that checks the `name` key and one that checks the `age` key.

??? success "Solution to Exercise 1"
    ```python
    import pytest

    @pytest.fixture
    def sample_dict():
        return {"name": "Alice", "age": 30}

    def test_name(sample_dict):
        assert sample_dict["name"] == "Alice"

    def test_age(sample_dict):
        assert sample_dict["age"] == 30
    ```

---

**Exercise 2.** Create a fixture `temp_file` that creates a temporary file with some content, yields its path, and deletes it in teardown. Write a test that reads the file and verifies the content.

??? success "Solution to Exercise 2"
    ```python
    import pytest
    import tempfile
    import os

    @pytest.fixture
    def temp_file():
        fd, path = tempfile.mkstemp()
        with os.fdopen(fd, 'w') as f:
            f.write("test content")
        yield path
        os.unlink(path)

    def test_read_temp_file(temp_file):
        with open(temp_file) as f:
            assert f.read() == "test content"
    ```

---

**Exercise 3.** Explain the difference between `scope="function"` and `scope="module"` for a pytest fixture. Give an example where module scope would be more appropriate.

??? success "Solution to Exercise 3"
    With `scope="function"` (the default), the fixture is created and destroyed for every test function. With `scope="module"`, the fixture is created once for the entire module and shared across all tests in that module.

    Module scope is appropriate for expensive resources like database connections:

    ```python
    @pytest.fixture(scope="module")
    def db_connection():
        conn = create_connection()  # expensive
        yield conn
        conn.close()
    ```

---

**Exercise 4.** Write a fixture `db_connection` that prints `"Connecting..."` on setup and `"Disconnecting..."` on teardown. Write two tests that use this fixture and verify the setup/teardown messages appear in the correct order.

??? success "Solution to Exercise 4"
    ```python
    import pytest

    @pytest.fixture
    def db_connection(capsys):
        print("Connecting...")
        yield "connection_object"
        print("Disconnecting...")

    def test_query(db_connection):
        assert db_connection == "connection_object"

    def test_insert(db_connection):
        assert db_connection is not None
    ```
