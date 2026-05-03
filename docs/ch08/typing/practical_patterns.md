# Practical Type Hint Patterns

Common patterns and best practices for applying type hints effectively in real-world Python code.

!!! tip "Mental Model"
    Practical type hinting follows a cost-benefit curve: annotate public API boundaries first (function signatures, class attributes), then work inward. Use `TypedDict` for JSON-shaped data, `Protocol` for duck-typed interfaces, and `overload` for functions with multiple signatures. The goal is not 100% coverage but maximum clarity at the points where bugs are most likely.

## API Response Typing

Type hint API responses and data structures clearly.

```python
from typing import TypeAlias
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str

ApiResponse: TypeAlias = dict[str, User]

def get_users() -> ApiResponse:
    return {
        "1": User(1, "Alice", "alice@example.com"),
        "2": User(2, "Bob", "bob@example.com")
    }

users = get_users()
print(users["1"])
```

```
User(id=1, name='Alice', email='alice@example.com')
```

## Variadic Arguments

Type hint functions with variable arguments.

```python
from typing import overload

@overload
def concat(sep: str) -> Callable[[str, ...], str]: ...

def concat(*items: str) -> str:
    return ",".join(items)

result = concat("apple", "banana", "cherry")
print(result)
```

```
apple,banana,cherry
```

## Decorators with Generics

Type hint decorators using generics.

```python
from typing import Callable, TypeVar, cast

F = TypeVar('F', bound=Callable)

def log_calls(func: F) -> F:
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return cast(F, wrapper)

@log_calls
def greet(name: str) -> str:
    return f"Hello {name}"

print(greet("Alice"))
```

```
Calling greet
Hello Alice
```


---

## Exercises

**Exercise 1.** Annotate a decorator `retry(func)` that takes a function with any signature and returns a function with the same signature. Use `Callable` and `TypeVar` (or `ParamSpec` if targeting Python 3.10+).

??? success "Solution to Exercise 1"
    ```python
    from typing import Callable, TypeVar
    from functools import wraps

    F = TypeVar("F", bound=Callable)

    def retry(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(3):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == 2:
                        raise
        return wrapper  # type: ignore

    @retry
    def fetch(url: str) -> str:
        return f"data from {url}"
    ```

---

**Exercise 2.** Write a `@dataclass` with type annotations for a `Product` with `name: str`, `price: float`, and `quantity: int`. Add a property `total` with a return type annotation.

??? success "Solution to Exercise 2"
    ```python
    from dataclasses import dataclass

    @dataclass
    class Product:
        name: str
        price: float
        quantity: int

        @property
        def total(self) -> float:
            return self.price * self.quantity

    p = Product("Widget", 9.99, 3)
    print(p.total)  # 29.97
    ```

---

**Exercise 3.** Create a `TypedDict` called `UserProfile` with keys `name` (str), `age` (int), and `email` (str). Write a function that accepts this TypedDict and returns a formatted string.

??? success "Solution to Exercise 3"
    ```python
    from typing import TypedDict

    class UserProfile(TypedDict):
        name: str
        age: int
        email: str

    def format_profile(user: UserProfile) -> str:
        return f"{user['name']} (age {user['age']}) - {user['email']}"

    profile: UserProfile = {"name": "Alice", "age": 30, "email": "alice@test.com"}
    print(format_profile(profile))
    ```

---

**Exercise 4.** Write a function `process_items(items: Iterable[T]) -> list[T]` using a `TypeVar` so that it preserves the element type. Demonstrate with both `int` and `str` inputs.

??? success "Solution to Exercise 4"
    ```python
    from typing import TypeVar, Iterable

    T = TypeVar("T")

    def process_items(items: Iterable[T]) -> list[T]:
        return sorted(items)

    ints: list[int] = process_items([3, 1, 2])
    strs: list[str] = process_items(["c", "a", "b"])
    print(ints)  # [1, 2, 3]
    print(strs)  # ['a', 'b', 'c']
    ```
