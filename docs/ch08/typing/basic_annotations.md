# Basic Annotations (int, str, list)

Basic type annotations include primitive types and built-in collection types, forming the foundation of type hinting.

!!! tip "Mental Model"
    Type annotations are labels you attach to variables, parameters, and return values — `x: int`, `names: list[str]`, `def greet(name: str) -> str`. Python ignores them at runtime, but tools like mypy read them to catch type mismatches before you run the code. Start by annotating function signatures; that alone catches the majority of type bugs.

## Primitive Type Annotations

Annotate variables with primitive types like int, str, float, and bool.

```python
# Primitive types
name: str = "Alice"
age: int = 30
height: float = 5.8
is_active: bool = True

print(f"{name}, {age}, {height}, {is_active}")
```

```
Alice, 30, 5.8, True
```

## Collection Type Annotations

Annotate collections and specify their element types.

```python
# Collection types (Python 3.9+)
numbers: list[int] = [1, 2, 3]
tags: set[str] = {"python", "typing"}
coords: tuple[float, float] = (10.5, 20.3)

# Dictionaries with key-value types
config: dict[str, int] = {"port": 8080, "timeout": 30}

print(f"Numbers: {numbers}")
print(f"Config: {config}")
```

```
Numbers: [1, 2, 3]
Config: {'port': 8080, 'timeout': 30}
```

## Function Annotations

Annotate function parameters and return types.

```python
def add(a: int, b: int) -> int:
    return a + b

def greet(name: str) -> str:
    return f"Hello, {name}"

result1 = add(5, 3)
result2 = greet("World")
print(result1, result2)
```

```
8 Hello, World
```


---

## Exercises

**Exercise 1.** Add type annotations to the following function and variable declarations:

```python
def greet(name, times):
    for i in range(times):
        print(f"Hello, {name}!")

age = 25
scores = [90, 85, 92]
active = True
```

??? success "Solution to Exercise 1"
    ```python
    def greet(name: str, times: int) -> None:
        for i in range(times):
            print(f"Hello, {name}!")

    age: int = 25
    scores: list[int] = [90, 85, 92]
    active: bool = True
    ```

---

**Exercise 2.** Write a function `average(numbers: list[float]) -> float` that returns the arithmetic mean. What happens if you pass an empty list? Add a docstring explaining the expected behavior.

??? success "Solution to Exercise 2"
    ```python
    def average(numbers: list[float]) -> float:
        """Return the arithmetic mean of numbers.

        Raises ZeroDivisionError if the list is empty.
        """
        return sum(numbers) / len(numbers)

    print(average([1.0, 2.0, 3.0]))  # 2.0
    ```

---

**Exercise 3.** Predict whether `mypy` would report an error for each line:

```python
x: int = "hello"
y: str = 42
z: list[int] = [1, 2, 3]
w: list[int] = [1, "two", 3]
```

??? success "Solution to Exercise 3"

    - `x: int = "hello"` — error: incompatible type `str` assigned to `int`
    - `y: str = 42` — error: incompatible type `int` assigned to `str`
    - `z: list[int] = [1, 2, 3]` — no error
    - `w: list[int] = [1, "two", 3]` — error: `"two"` is `str`, not `int`

---

**Exercise 4.** Annotate a function `create_user(name: str, age: int, email: str) -> dict[str, str | int]` and implement it. Then annotate a variable that stores the return value.

??? success "Solution to Exercise 4"
    ```python
    def create_user(name: str, age: int, email: str) -> dict[str, str | int]:
        return {"name": name, "age": age, "email": email}

    user: dict[str, str | int] = create_user("Alice", 30, "alice@example.com")
    print(user)
    ```
