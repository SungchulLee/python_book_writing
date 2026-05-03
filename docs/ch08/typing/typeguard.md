# TypeGuard and Type Narrowing

`TypeGuard` helps type checkers narrow down types within function bodies, improving type safety.

!!! tip "Mental Model"
    Type narrowing is how a type checker learns more precise types inside conditional branches. After `if isinstance(x, int):`, the checker knows `x` is `int` in that block. `TypeGuard` extends this to custom predicates: you write a function that returns `bool`, annotate it with `TypeGuard[T]`, and the checker treats a `True` result as proof that the argument is of type `T`.

## Type Narrowing with Isinstance

Use isinstance to narrow types within conditional blocks.

```python
from typing import Union

def process_value(value: Union[int, str]) -> str:
    if isinstance(value, int):
        # Type checker knows value is int here
        return f"Integer: {value * 2}"
    else:
        # Type checker knows value is str here
        return f"String: {value.upper()}"

print(process_value(5))
print(process_value("hello"))
```

```
Integer: 10
String: HELLO
```

## TypeGuard for Custom Type Checks

Create custom type guards for more complex type narrowing.

```python
from typing import TypeGuard

def is_list_of_ints(value: list) -> TypeGuard[list[int]]:
    return all(isinstance(item, int) for item in value)

def process_numbers(value: list) -> int:
    if is_list_of_ints(value):
        # Type checker narrows to list[int]
        return sum(value)
    else:
        return 0

print(process_numbers([1, 2, 3]))
print(process_numbers([1, "two", 3]))
```

```
6
0
```


---

## Exercises

**Exercise 1.** Write a type guard function `is_str_list(val: list[object]) -> TypeGuard[list[str]]` that checks whether all elements in a list are strings. Use it to narrow the type before calling `.upper()` on each element.

??? success "Solution to Exercise 1"
    ```python
    from typing import TypeGuard

    def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
        return all(isinstance(item, str) for item in val)

    def process(data: list[object]) -> None:
        if is_str_list(data):
            # type checker knows data is list[str] here
            for item in data:
                print(item.upper())

    process(["hello", "world"])
    ```

---

**Exercise 2.** Explain why a regular `isinstance` check is sometimes insufficient for type narrowing with complex types, and how `TypeGuard` solves this.

??? success "Solution to Exercise 2"
    `isinstance(x, list)` tells the type checker that `x` is a `list`, but not what it contains. You cannot write `isinstance(x, list[str])` at runtime. `TypeGuard` lets you write a custom function that performs the element-level check and tells the type checker the precise generic type.

---

**Exercise 3.** Write a function `is_positive_int(x: int | str) -> TypeGuard[int]` that returns `True` only if `x` is a positive integer. Then use it in an `if` block where the type checker narrows `x` to `int`.

??? success "Solution to Exercise 3"
    ```python
    from typing import TypeGuard

    def is_positive_int(x: int | str) -> TypeGuard[int]:
        return isinstance(x, int) and x > 0

    def process(val: int | str) -> None:
        if is_positive_int(val):
            # type checker narrows val to int
            print(val + 1)
        else:
            print("Not a positive int")

    process(5)       # 6
    process("hello") # Not a positive int
    ```

---

**Exercise 4.** Compare `TypeGuard` with `TypeIs` (Python 3.13+). What is the key difference in how they narrow types?

??? success "Solution to Exercise 4"
    `TypeGuard[T]` tells the type checker that if the function returns `True`, the argument has type `T`. However, the `else` branch does not get narrowed — the original type is preserved.

    `TypeIs[T]` (Python 3.13+) provides symmetric narrowing: in the `True` branch the type narrows to `T`, and in the `False` branch it narrows to the complement. This enables more precise type checking in both branches.
