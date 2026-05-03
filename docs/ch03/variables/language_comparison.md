# Language Models

!!! tip "Mental Model"
    Different languages use different mental pictures for variables. C variables are labeled boxes that hold values directly. Java splits: primitives are boxes, objects are references. Python is pure reference semantics: every variable is a name tag attached to a heap object. Understanding which model your language uses prevents entire categories of aliasing and copying bugs.

## Python Model

### 1. Reference Semantics

Names refer to objects:

```python
x = [1, 2, 3]
y = x  # Both refer to same object
```

| Characteristic | Behavior |
|---------------|----------|
| Assignment | Creates reference |
| Equality `==` | Compares values |
| Identity `is` | Compares references |
| Mutation | Affects all references |

### 2. Example

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)  # [1, 2, 3, 4]
```

## Java Model

### 1. Objects vs Primitives

**Objects**: Reference semantics

```java
List<Integer> x = new ArrayList<>();
List<Integer> y = x;  // Both refer to same
```

**Primitives**: Value semantics

```java
int a = 42;
int b = a;  // b gets copy
```

### 2. Key Differences

| Type | Assignment | Comparison |
|------|-----------|------------|
| Object | Reference | `.equals()` |
| Primitive | Copy | `==` |

## C Model

### 1. Direct Storage

Variables are memory locations:

```c
int x = 42;  // x is 4-byte container
```

### 2. Explicit Pointers

```c
int x = 42;
int* p = &x;   // Explicit pointer
int y = x;     // Copy value
```

| Aspect | Behavior |
|--------|----------|
| Variables | Direct storage |
| Pointers | Explicit `*` |
| Assignment | Copies value |
| Comparison | Value or pointer |

## C++ Model

### 1. Multiple Options

```cpp
int x = 42;        // Value
int* p = &x;       // Pointer
int& r = x;        // Reference
```

### 2. Choice Table

| Type | Storage | Assignment | Modification |
|------|---------|-----------|--------------|
| Value | Direct | Copy | Independent |
| Pointer | Address | Copy pointer | Through `*p` |
| Reference | Alias | Cannot reassign | Direct |

## Haskell Model

### 1. Immutable Bindings

```haskell
x = [1, 2, 3]  -- Immutable binding
-- x = [4, 5, 6]  -- Error: cannot rebind
```

### 2. Transparency

```haskell
-- Same expression always gives same result
f x = x + x
-- f 5 always returns 10
```

## Comparison Table

| Language | Variable Model | Memory Mgmt | Assignment |
|----------|---------------|-------------|------------|
| **Python** | Names → Objects | Auto (GC) | Ref binding |
| **Java** | Refs + Primitives | Auto (GC) | Ref/Copy |
| **C++** | Values/Ptrs/Refs | Manual | Value/Ptr |
| **C** | Direct values | Manual | Value copy |
| **Haskell** | Immutable | Auto (GC) | No reassign |

## Practical Examples

### 1. Aliasing

**Python**:
```python
x = [1, 2]
y = x  # Alias
y.append(3)
print(x)  # [1, 2, 3]
```

**C**:
```c
int x = 42;
int y = x;  // Copy
y = 100;
// x still 42
```

### 2. Parameter Passing

**Python**:
```python
def modify(lst):
    lst.append(4)  # Modifies original

x = [1, 2, 3]
modify(x)
print(x)  # [1, 2, 3, 4]
```

**C**:
```c
void modify(int val) {
    val = 100;  // Modifies copy only
}

int x = 42;
modify(x);
// x still 42
```

**C++ Reference**:
```cpp
void modify(int& val) {
    val = 100;  // Modifies original
}

int x = 42;
modify(x);
// x is now 100
```

## Key Insights

### 1. Python Advantages

- Simple mental model
- No pointer arithmetic
- Automatic memory management
- Flexible aliasing

### 2. Python Gotchas

- Unexpected sharing
- Mutable default arguments
- No explicit copy

### 3. Best Practices

```python
# Explicit copying when needed
import copy

original = [1, 2, [3, 4]]
shallow = original.copy()
deep = copy.deepcopy(original)

# Clear intent
def process(data):
    # Work with original
    data.append(5)
    
def process_copy(data):
    # Work with copy
    local_data = data.copy()
    local_data.append(5)
    return local_data
```


---

## Exercises


**Exercise 1.**
Create a list, assign it to another variable, and modify it through the second variable. Show that the original is also modified. Explain how this differs from C's value semantics.

??? success "Solution to Exercise 1"

    ```python
    x = [1, 2, 3]
    y = x
    y.append(4)
    print(x)  # [1, 2, 3, 4]
    ```

    In Python, `y = x` creates an alias (both refer to the same object). In C, `int y = x` copies the value, so modifications to `y` would not affect `x`.

---

**Exercise 2.**
Write a function that takes a list and appends an element. Show that the caller's list is modified. Then write a version that works on a copy so the caller's list is unchanged.

??? success "Solution to Exercise 2"

    ```python
    def modify_original(lst):
        lst.append(99)

    def modify_copy(lst):
        local = lst.copy()
        local.append(99)
        return local

    data = [1, 2, 3]
    modify_original(data)
    print(data)  # [1, 2, 3, 99]

    data = [1, 2, 3]
    result = modify_copy(data)
    print(data)    # [1, 2, 3] (unchanged)
    print(result)  # [1, 2, 3, 99]
    ```

    Python passes object references to functions. To avoid modifying the caller's data, explicitly copy it with `.copy()`.

---

**Exercise 3.**
Use `copy.deepcopy()` to create a completely independent copy of a nested list. Modify the copy and show the original is unchanged.

??? success "Solution to Exercise 3"

    ```python
    import copy

    original = [[1, 2], [3, 4]]
    deep = copy.deepcopy(original)

    deep[0].append(99)
    print(original)  # [[1, 2], [3, 4]] (unchanged)
    print(deep)      # [[1, 2, 99], [3, 4]]
    ```

    `deepcopy()` recursively copies all nested objects. A shallow copy (`list.copy()`) would only copy the outer list, leaving inner lists shared.
