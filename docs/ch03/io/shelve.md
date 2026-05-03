# shelve Module

The shelve module provides persistent dictionary storage using DBM backend. It is simpler than databases for small data persistence needs, storing Python objects as pickled values.

!!! tip "Mental Model"
    A shelf is a persistent dictionary: it looks and feels like a `dict`, but the key-value pairs are saved to disk automatically. Under the hood it pickles each value, so anything you can pickle you can shelve. Use it for quick-and-dirty persistence of small datasets; for anything larger or multi-user, reach for a real database.

---

## Basic Usage

### Creating a Shelf

```python
import shelve
import tempfile
import os

tmpdir = tempfile.mkdtemp()
shelf_path = os.path.join(tmpdir, 'myshelf')

with shelve.open(shelf_path) as shelf:
    shelf['key1'] = 'value1'
    shelf['key2'] = [1, 2, 3]
    shelf['key3'] = {'nested': 'dict'}

with shelve.open(shelf_path) as shelf:
    print(shelf['key1'])
    print(shelf['key2'])

for f in os.listdir(tmpdir):
    os.remove(os.path.join(tmpdir, f))
os.rmdir(tmpdir)
```

Output:
```
value1
[1, 2, 3]
```

## Shelf Operations

### Dictionary-like Interface

```python
import shelve
import tempfile
import os

tmpdir = tempfile.mkdtemp()
shelf_path = os.path.join(tmpdir, 'test')

with shelve.open(shelf_path) as shelf:
    shelf['name'] = 'Alice'
    shelf['age'] = 30
    
    print(f"Keys: {list(shelf.keys())}")
    print(f"Values: {list(shelf.values())}")
    print(f"'name' in shelf: {'name' in shelf}")

for f in os.listdir(tmpdir):
    os.remove(os.path.join(tmpdir, f))
os.rmdir(tmpdir)
```

Output:
```
Keys: ['name', 'age']
Values: ['Alice', 30]
'name' in shelf: True
```

## Mutable Objects

### Updating Nested Data

```python
import shelve
import tempfile
import os

tmpdir = tempfile.mkdtemp()
shelf_path = os.path.join(tmpdir, 'test')

with shelve.open(shelf_path) as shelf:
    shelf['data'] = {'count': 0}

with shelve.open(shelf_path) as shelf:
    data = shelf['data']
    data['count'] += 1
    shelf['data'] = data

with shelve.open(shelf_path) as shelf:
    print(f"Updated: {shelf['data']}")

for f in os.listdir(tmpdir):
    os.remove(os.path.join(tmpdir, f))
os.rmdir(tmpdir)
```

Output:
```
Updated: {'count': 1}
```

## Practical Applications

### Configuration Storage

```python
import shelve
import tempfile
import os

tmpdir = tempfile.mkdtemp()
shelf_path = os.path.join(tmpdir, 'config')

with shelve.open(shelf_path) as config:
    config['theme'] = 'dark'
    config['language'] = 'en'

with shelve.open(shelf_path) as config:
    theme = config.get('theme', 'light')
    print(f"Theme: {theme}")

for f in os.listdir(tmpdir):
    os.remove(os.path.join(tmpdir, f))
os.rmdir(tmpdir)
```

Output:
```
Theme: dark
```

---

## Exercises


**Exercise 1.**
Use `shelve` to create a persistent key-value store. Store three records with string keys and dictionary values. Close the shelf, reopen it, and verify the data persists.

??? success "Solution to Exercise 1"

        ```python
        import shelve

        with shelve.open("/tmp/mydata") as db:
            db["alice"] = {"age": 30, "city": "Seoul"}
            db["bob"] = {"age": 25, "city": "Tokyo"}
            db["carol"] = {"age": 35, "city": "NYC"}

        with shelve.open("/tmp/mydata") as db:
            print(db["alice"])  # {'age': 30, 'city': 'Seoul'}
            print(list(db.keys()))  # ['alice', 'bob', 'carol']
        ```

    `shelve` provides a dictionary-like interface to persistent storage. Data survives between program runs.

---

**Exercise 2.**
Demonstrate the writeback problem: open a shelf without `writeback=True`, modify a mutable value, and show that the change is lost. Then fix it using `writeback=True`.

??? success "Solution to Exercise 2"

        ```python
        import shelve

        # Without writeback - changes lost
        with shelve.open("/tmp/test_shelf") as db:
            db["data"] = [1, 2, 3]

        with shelve.open("/tmp/test_shelf") as db:
            db["data"].append(4)  # Modifies a temporary copy

        with shelve.open("/tmp/test_shelf") as db:
            print(db["data"])  # [1, 2, 3] - append was lost!

        # With writeback - changes preserved
        with shelve.open("/tmp/test_shelf", writeback=True) as db:
            db["data"].append(4)

        with shelve.open("/tmp/test_shelf") as db:
            print(db["data"])  # [1, 2, 3, 4]
        ```

    Without `writeback=True`, accessing `db["data"]` returns a deserialized copy. Mutations to this copy are not automatically saved back.

---

**Exercise 3.**
Write a simple address book using `shelve` with functions `add_contact(name, phone)`, `get_contact(name)`, and `list_contacts()`.

??? success "Solution to Exercise 3"

        ```python
        import shelve

        DB_PATH = "/tmp/addressbook"

        def add_contact(name, phone):
            with shelve.open(DB_PATH) as db:
                db[name] = phone

        def get_contact(name):
            with shelve.open(DB_PATH) as db:
                return db.get(name, "Not found")

        def list_contacts():
            with shelve.open(DB_PATH) as db:
                return dict(db)

        add_contact("Alice", "555-1234")
        add_contact("Bob", "555-5678")
        print(get_contact("Alice"))   # 555-1234
        print(list_contacts())        # {'Alice': '555-1234', 'Bob': '555-5678'}
        ```
