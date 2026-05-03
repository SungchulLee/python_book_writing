# TypeVar and Generic

`TypeVar` defines type variables for generic functions and classes, allowing flexible yet type-safe code.

!!! tip "Mental Model"
    A `TypeVar` is a placeholder for "some type to be determined later." When you write `def first(items: list[T]) -> T`, the `T` binds to whatever type the caller passes — `list[int]` makes it `int`, `list[str]` makes it `str`. This lets you write one function that is generic yet fully type-checked, without resorting to `Any`.

## TypeVar - Generic Type Variables

Use TypeVar to write generic functions that work with any type.

```python
from typing import TypeVar

T = TypeVar('T')

def first(items: list[T]) -> T:
    return items[0]

def last(items: list[T]) -> T:
    return items[-1]

nums = [1, 2, 3]
strs = ['a', 'b', 'c']

print(first(nums))  # int
print(last(strs))   # str
```

```
1
c
```

## Constrained TypeVar

Restrict TypeVar to specific types.

```python
from typing import TypeVar

# Only int or str
T = TypeVar('T', int, str)

def process(value: T) -> T:
    if isinstance(value, int):
        return value * 2  # type: ignore
    else:
        return value.upper()  # type: ignore

print(process(5))
print(process("hello"))
```

```
10
HELLO
```

## Generic Classes

Create generic classes with type parameters.

```python
from typing import Generic, TypeVar

T = TypeVar('T')

class Container(Generic[T]):
    def __init__(self, item: T):
        self.item = item
    
    def get(self) -> T:
        return self.item

int_container = Container[int](42)
str_container = Container[str]("hello")

print(int_container.get())
print(str_container.get())
```

```
42
hello
```

---

## Runnable Example: `generics_tutorial.py`

```python
"""
Tutorial 07: Generic Types and TypeVar
======================================

Level: Advanced

This tutorial covers generic types, TypeVar, and how to create
flexible, reusable functions and classes that work with multiple types.

Learning Objectives:
- Understand and use TypeVar
- Create generic functions
- Build generic classes
- Use constraints and bounds on TypeVars
- Work with multiple TypeVars

Prerequisites:
- All previous tutorials
"""

from typing import TypeVar, Generic, List, Optional, Sequence, Callable

# =============================================================================
# SECTION 1: TypeVar Basics
# =============================================================================

# TypeVar creates a type variable that can represent any type
T = TypeVar('T')

def identity(value: T) -> T:
    """Return the same value - preserves type."""
    return value

# Usage:
x: int = identity(5)  # T is int
y: str = identity("hello")  # T is str


def get_first(items: Sequence[T]) -> Optional[T]:
    """Get first item, preserving type."""
    return items[0] if items else None


def reverse_list(items: List[T]) -> List[T]:
    """Reverse a list, preserving element type."""
    return list(reversed(items))


# =============================================================================
# SECTION 2: Multiple TypeVars
# =============================================================================

T1 = TypeVar('T1')
T2 = TypeVar('T2')

def pair(first: T1, second: T2) -> tuple[T1, T2]:
    """Create a pair of potentially different types."""
    return (first, second)


def map_pair(pair: tuple[T1, T2], func1: Callable[[T1], T1], func2: Callable[[T2], T2]) -> tuple[T1, T2]:
    """Apply functions to both elements of a pair."""
    return (func1(pair[0]), func2(pair[1]))


# =============================================================================
# SECTION 3: Generic Classes
# =============================================================================

class Stack(Generic[T]):
    """Generic stack data structure."""
    
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        """Push an item onto the stack."""
        self._items.append(item)
    
    def pop(self) -> T:
        """Pop an item from the stack."""
        if not self._items:
            raise IndexError("Pop from empty stack")
        return self._items.pop()
    
    def peek(self) -> Optional[T]:
        """Peek at top item without removing."""
        return self._items[-1] if self._items else None
    
    def is_empty(self) -> bool:
        """Check if stack is empty."""
        return len(self._items) == 0


class Pair(Generic[T1, T2]):
    """Generic pair of two potentially different types."""
    
    def __init__(self, first: T1, second: T2) -> None:
        self.first = first
        self.second = second
    
    def get_first(self) -> T1:
        return self.first
    
    def get_second(self) -> T2:
        return self.second
    
    def swap(self) -> 'Pair[T2, T1]':
        """Return a new pair with swapped elements."""
        return Pair(self.second, self.first)


# =============================================================================
# SECTION 4: Constrained TypeVars
# =============================================================================

from typing import Union

# TypeVar with constraints
NumberType = TypeVar('NumberType', int, float)

def add(x: NumberType, y: NumberType) -> NumberType:
    """Add two numbers (int or float)."""
    return x + y  # type: ignore


def multiply(x: NumberType, y: NumberType) -> NumberType:
    """Multiply two numbers."""
    return x * y  # type: ignore


# =============================================================================
# SECTION 5: Bounded TypeVars
# =============================================================================

class Comparable:
    """Base class for comparable objects."""
    def __lt__(self, other: 'Comparable') -> bool:
        raise NotImplementedError

ComparableType = TypeVar('ComparableType', bound=Comparable)

def find_min(items: Sequence[ComparableType]) -> Optional[ComparableType]:
    """Find minimum item (must be comparable)."""
    if not items:
        return None
    return min(items)


# =============================================================================
# SECTION 6: Practical Examples
# =============================================================================

class Box(Generic[T]):
    """A container that holds a value."""
    
    def __init__(self, value: T) -> None:
        self._value = value
    
    def get(self) -> T:
        """Get the contained value."""
        return self._value
    
    def set(self, value: T) -> None:
        """Set a new value."""
        self._value = value
    
    def map(self, func: Callable[[T], T]) -> 'Box[T]':
        """Apply a function to the contained value."""
        return Box(func(self._value))


def filter_list(items: List[T], predicate: Callable[[T], bool]) -> List[T]:
    """Filter items using a predicate."""
    return [item for item in items if predicate(item)]


if __name__ == "__main__":
    print("=== Generic Types Examples ===\n")
    
    # Basic TypeVar
    print("TypeVar:")
    print(f"  identity(5): {identity(5)}")
    print(f"  identity('hello'): {identity('hello')}")
    print(f"  get_first([1,2,3]): {get_first([1,2,3])}")
    print()
    
    # Generic classes
    print("Generic Classes:")
    int_stack: Stack[int] = Stack()
    int_stack.push(1)
    int_stack.push(2)
    print(f"  Stack pop: {int_stack.pop()}")
    
    str_stack: Stack[str] = Stack()
    str_stack.push("hello")
    print(f"  String stack peek: {str_stack.peek()}")
    print()
    
    # Pair
    p = Pair(10, "hello")
    print(f"  Pair: ({p.get_first()}, {p.get_second()})")
    swapped = p.swap()
    print(f"  Swapped: ({swapped.get_first()}, {swapped.get_second()})")
```

---

## Exercises

**Exercise 1.** Write a generic function `first(items: Sequence[T]) -> T` using `TypeVar` that returns the first element of any sequence. Demonstrate it with both a list of ints and a tuple of strings.

??? success "Solution to Exercise 1"
    ```python
    from typing import TypeVar, Sequence

    T = TypeVar("T")

    def first(items: Sequence[T]) -> T:
        return items[0]

    print(first([1, 2, 3]))         # 1 (int)
    print(first(("a", "b", "c")))   # a (str)
    ```

---

**Exercise 2.** Create a generic class `Stack[T]` with `push(item: T)`, `pop() -> T`, and `peek() -> T` methods. Annotate everything properly.

??? success "Solution to Exercise 2"
    ```python
    from typing import TypeVar, Generic

    T = TypeVar("T")

    class Stack(Generic[T]):
        def __init__(self) -> None:
            self._items: list[T] = []

        def push(self, item: T) -> None:
            self._items.append(item)

        def pop(self) -> T:
            return self._items.pop()

        def peek(self) -> T:
            return self._items[-1]

    s: Stack[int] = Stack()
    s.push(1)
    s.push(2)
    print(s.peek())  # 2
    print(s.pop())   # 2
    ```

---

**Exercise 3.** Explain the difference between `TypeVar("T")` and `TypeVar("T", bound=Comparable)`. When would you use a bounded `TypeVar`?

??? success "Solution to Exercise 3"
    `TypeVar("T")` is unconstrained — it can be any type. `TypeVar("T", bound=Comparable)` restricts `T` to types that are subtypes of `Comparable`.

    Use a bounded `TypeVar` when you need to call methods or use operations that only certain types support. For example, `TypeVar("T", bound=SupportsLessThan)` ensures `T` has a `__lt__` method, which is needed for sorting.

---

**Exercise 4.** Write a function `merge_sorted(a: list[T], b: list[T]) -> list[T]` using `TypeVar` that merges two sorted lists into one sorted list. Test it with integers and strings.

??? success "Solution to Exercise 4"
    ```python
    from typing import TypeVar

    T = TypeVar("T")

    def merge_sorted(a: list[T], b: list[T]) -> list[T]:
        result: list[T] = []
        i = j = 0
        while i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        result.extend(a[i:])
        result.extend(b[j:])
        return result

    print(merge_sorted([1, 3, 5], [2, 4, 6]))    # [1, 2, 3, 4, 5, 6]
    print(merge_sorted(["a", "c"], ["b", "d"]))   # ['a', 'b', 'c', 'd']
    ```

---

**Exercise 5.** Use `TypeVar` with constraints (`TypeVar("T", int, float)`) to write a function `add(a: T, b: T) -> T` that only works with numeric types. Show that passing strings would be flagged by mypy.

??? success "Solution to Exercise 5"
    ```python
    from typing import TypeVar

    T = TypeVar("T", int, float)

    def add(a: T, b: T) -> T:
        return a + b

    print(add(1, 2))      # 3
    print(add(1.5, 2.5))  # 4.0
    # add("a", "b")  # mypy error: Value of type variable "T" cannot be "str"
    ```
