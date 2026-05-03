# Built-in Names

!!! tip "Mental Model"
    Python ships with roughly 150 names pre-loaded into every module: functions like `len` and `print`, types like `int` and `dict`, and exceptions like `ValueError`. These names live in the `builtins` module and are looked up last in the LEGB chain. Knowing what is built-in helps you avoid accidentally shadowing these names with your own variables.

## View Built-ins

### 1. List All

```python
# Access built-in namespace
print(dir(__builtins__))

# Count
print(len(dir(__builtins__)))
```

### 2. Check Built-in

```python
import builtins

print(hasattr(builtins, 'list'))    # True
print(hasattr(builtins, 'myvar'))   # False
```

## Don't Shadow

### 1. Type Constructors

```python
# Don't shadow these!
# int = 42        
# float = 3.14    
# str = "text"    
# list = []       
# dict = {}       
# tuple = ()      
# set = set()     
# bool = True     
```

### 2. Common Functions

```python
# Don't shadow
# len = 5       # Very bad!
# range = []    
# print = "x"   # Very bad!
# input = 42    
# sum = 0       # Common mistake!
# max = 10      # Common mistake!
# min = 1       # Common mistake!
```

### 3. Iteration

```python
# Don't shadow
# iter = []     
# next = 1      
# filter = []   
# map = {}      
# sorted = []   # Very common!
# reversed = [] 
```

## Recovery

### 1. Delete Shadow

```python
# Shadowed
list = [1, 2, 3]

# Recover
del list
list(range(5))  # Works
```

### 2. Access builtins

```python
import builtins

# Even if shadowed
len = 42
builtins.len([1, 2, 3])  # Works
```

## Safe Alternatives

| Don't Use | Use Instead |
|-----------|-------------|
| `sum` | `total` |
| `list` | `items`, `data_list` |
| `dict` | `mapping` |
| `type` | `kind`, `data_type` |
| `id` | `identifier` |
| `max` | `maximum` |
| `min` | `minimum` |
| `sorted` | `ordered` |

---

## Exercises


**Exercise 1.**
List five commonly shadowed built-in names. For each, suggest a better alternative variable name.

??? success "Solution to Exercise 1"

    | Built-in | Common misuse | Better name |
    |----------|---------------|-------------|
    | `list` | `list = [...]` | `items`, `values`, `data` |
    | `dict` | `dict = {...}` | `mapping`, `config`, `record` |
    | `str` | `str = "..."` | `text`, `name`, `message` |
    | `type` | `type = "admin"` | `kind`, `category`, `role` |
    | `id` | `id = 42` | `user_id`, `item_id`, `identifier` |

---

**Exercise 2.**
Write a function that accidentally shadows `input` inside its body. Show the resulting error, then fix it.

??? success "Solution to Exercise 2"

        ```python
        # Buggy version
        def get_name():
            input = "default"       # Shadows built-in input()
            name = input("Name: ")  # TypeError!
            return name

        # Fixed version
        def get_name():
            default_name = "default"
            name = input("Name: ")
            return name or default_name
        ```

    Once `input` is reassigned to a string, calling `input()` tries to call the string, raising `TypeError`.

---

**Exercise 3.**
Use `dir(builtins)` to count how many built-in names there are in Python. Filter to show only the ones that are commonly used as variable names by beginners.

??? success "Solution to Exercise 3"

        ```python
        import builtins

        all_builtins = dir(builtins)
        print(f"Total built-in names: {len(all_builtins)}")

        # Commonly misused as variable names
        common = {"list", "dict", "str", "int", "float", "type", "id",
                  "input", "print", "len", "max", "min", "sum", "set",
                  "map", "filter", "range", "open", "format", "hash"}

        found = [name for name in all_builtins if name in common]
        print(f"Commonly shadowed: {sorted(found)}")
        ```
