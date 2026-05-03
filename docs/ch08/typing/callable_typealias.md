# Callable and TypeAlias

`Callable` annotates functions or callable objects, while `TypeAlias` creates named type aliases for complex type annotations.

!!! tip "Mental Model"
    `Callable[[ArgTypes], ReturnType]` is the type hint for "anything you can call like a function." Use it to annotate callbacks, strategy parameters, or decorator arguments. `TypeAlias` gives a name to a long or complex type expression so you can reuse it without repeating the full definition — like a variable for types.

## Callable - Function Type Hints

Use `Callable` to annotate functions and callbacks.

```python
from typing import Callable

# Function that takes a Callable
def apply_operation(a: int, b: int, op: Callable[[int, int], int]) -> int:
    return op(a, b)

# Callable with different signatures
def transform(data: list[str], processor: Callable[[str], int]) -> list[int]:
    return [processor(item) for item in data]

result1 = apply_operation(5, 3, lambda x, y: x + y)
result2 = transform(["hello", "world"], len)

print(result1)
print(result2)
```

```
8
[5, 5]
```

## TypeAlias - Named Type Aliases

Create reusable type definitions with TypeAlias.

```python
from typing import TypeAlias

# Create named aliases for complex types
UserId: TypeAlias = int
UserName: TypeAlias = str
UserData: TypeAlias = dict[UserId, UserName]

def get_user_name(users: UserData, user_id: UserId) -> UserName | None:
    return users.get(user_id)

users: UserData = {1: "Alice", 2: "Bob"}
print(get_user_name(users, 1))
print(get_user_name(users, 99))
```

```
Alice
None
```


---

## Exercises

**Exercise 1.** Write a type alias `Predicate` for a function that takes an `int` and returns a `bool`. Then write a function `filter_numbers(numbers: list[int], pred: Predicate) -> list[int]` that filters a list using the predicate.

??? success "Solution to Exercise 1"
    ```python
    from typing import Callable, TypeAlias

    Predicate: TypeAlias = Callable[[int], bool]

    def filter_numbers(numbers: list[int], pred: Predicate) -> list[int]:
        return [n for n in numbers if pred(n)]

    evens = filter_numbers([1, 2, 3, 4, 5], lambda x: x % 2 == 0)
    print(evens)  # [2, 4]
    ```

---

**Exercise 2.** Annotate a callback parameter using `Callable`. Write a function `apply_twice(func: Callable[[int], int], value: int) -> int` that applies `func` to `value` twice.

??? success "Solution to Exercise 2"
    ```python
    from typing import Callable

    def apply_twice(func: Callable[[int], int], value: int) -> int:
        return func(func(value))

    print(apply_twice(lambda x: x + 1, 5))  # 7
    print(apply_twice(lambda x: x * 2, 3))  # 12
    ```

---

**Exercise 3.** Create a `TypeAlias` called `Matrix` for `list[list[float]]`. Write a function `transpose(m: Matrix) -> Matrix` with proper annotations.

??? success "Solution to Exercise 3"
    ```python
    from typing import TypeAlias

    Matrix: TypeAlias = list[list[float]]

    def transpose(m: Matrix) -> Matrix:
        rows = len(m)
        cols = len(m[0])
        return [[m[r][c] for r in range(rows)] for c in range(cols)]

    mat: Matrix = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
    print(transpose(mat))  # [[1.0, 3.0, 5.0], [2.0, 4.0, 6.0]]
    ```

---

**Exercise 4.** Explain the difference between `Callable[[int, str], bool]` and `Callable[..., bool]`. When would you use each?

??? success "Solution to Exercise 4"
    `Callable[[int, str], bool]` specifies a function that takes exactly an `int` and a `str` and returns a `bool`. `Callable[..., bool]` specifies a function that returns `bool` but accepts any number and types of arguments.

    Use the first form when you know the exact signature of the callback. Use `...` when the function signature varies or you want maximum flexibility, such as when wrapping arbitrary functions in a decorator.
