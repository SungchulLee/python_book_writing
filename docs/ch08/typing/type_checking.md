# TYPE_CHECKING and Forward References

As projects grow, type hints sometimes create circular import chains — module A imports a type from module B, which imports a type from module A. Similarly, a class may need to reference itself in its own type annotations before the class definition is complete. Python's `TYPE_CHECKING` constant and forward references (string-quoted type names) solve both problems without sacrificing type safety.

!!! tip "Mental Model"
    `TYPE_CHECKING` is a gate that opens only for type checkers and stays closed at runtime. Imports placed inside `if TYPE_CHECKING:` exist for mypy but never execute, breaking circular import chains cleanly. Forward references (quoted type names like `"MyClass"`) let you annotate with a type that hasn't been defined yet. Together they decouple type analysis from runtime execution.

## TYPE_CHECKING for Conditional Imports

The `TYPE_CHECKING` constant from the `typing` module is `False` at runtime but treated as `True` by static type checkers like `mypy`. Wrapping an import in `if TYPE_CHECKING:` means the import only executes during type analysis, breaking the circular dependency at runtime. The type annotation must then use a string (forward reference) so Python does not try to evaluate it.

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # These imports only happen during type checking
    from some_module import SomeType

def process(value: 'SomeType') -> str:
    # Quotes make it a forward reference
    return str(value)

print("Code runs without importing SomeType at runtime")
```

```text
Code runs without importing SomeType at runtime
```

## Forward References with Quotes

A forward reference is a type annotation written as a string literal (e.g., `'Node'`) instead of the bare class name. Python evaluates annotations at class-definition time, so referencing a class that has not yet been fully defined raises a `NameError`. Quoting the name defers evaluation, letting the annotation resolve later.

```python
from typing import Optional

class Node:
    def __init__(self, value: int, next: Optional['Node'] = None):
        self.value = value
        self.next = next

# Create linked list
node1 = Node(1)
node2 = Node(2)
node1.next = node2

print(f"Node1: {node1.value}, Node2: {node1.next.value}")
```

```text
Node1: 1, Node2: 2
```

---

## Exercises

**Exercise 1.** Demonstrate a circular import problem caused by type hints, and fix it using `TYPE_CHECKING` and forward references.

??? success "Solution to Exercise 1"
    ```python
    # file: models.py
    from __future__ import annotations
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from services import UserService

    class User:
        def __init__(self, name: str):
            self.name = name

        def get_service(self) -> UserService:
            from services import UserService
            return UserService(self)
    ```

    The `TYPE_CHECKING` guard prevents the import at runtime, breaking the circular dependency. The actual import happens lazily inside the method.

---

**Exercise 2.** Explain the difference between a forward reference (`"MyClass"`) and using `from __future__ import annotations`. When is each approach necessary?

??? success "Solution to Exercise 2"
    A **forward reference** (`"MyClass"`) is a string that names a class not yet defined. It is needed when a class refers to itself or to a class defined later in the same file.

    `from __future__ import annotations` makes all annotations lazy strings automatically, so you never need explicit forward references. It also enables modern syntax (`list[int]`) in older Python versions.

    Use forward references for individual cases. Use `__future__` annotations when you want all annotations in a module to be lazy.

---

**Exercise 3.** Write a class `Node` that has an attribute `children: list["Node"]`. Create a small tree and verify it works at runtime.

??? success "Solution to Exercise 3"
    ```python
    from __future__ import annotations

    class Node:
        def __init__(self, value: str, children: list[Node] | None = None):
            self.value = value
            self.children = children or []

    root = Node("root", [
        Node("child1", [Node("grandchild1")]),
        Node("child2"),
    ])
    print(root.value)                        # root
    print(root.children[0].children[0].value) # grandchild1
    ```

---

**Exercise 4.** Use `TYPE_CHECKING` to import a type from another module only for type checking. Write the pattern and explain why it prevents circular imports.

??? success "Solution to Exercise 4"
    ```python
    from __future__ import annotations
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from other_module import HeavyClass

    def process(obj: HeavyClass) -> str:
        return str(obj)
    ```

    `TYPE_CHECKING` is `False` at runtime, so `other_module` is never imported during execution. Tools like `mypy` set `TYPE_CHECKING` to `True`, so they see the import and can validate the annotation. This prevents circular imports while preserving full type safety.
