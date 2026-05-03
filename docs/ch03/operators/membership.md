# Membership Operators

Membership operators test whether a value exists in a sequence (string, list, tuple, set, dict).

!!! tip "Mental Model"
    `in` is a membership question: "is this item in that container?" For lists and tuples it scans linearly (O(n)); for sets and dicts it hashes and jumps (O(1)). For strings, `in` checks substring containment, not just single characters. Choosing the right container type determines how fast `in` runs.

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `in` | Value found | `'a' in 'cat'` | `True` |
| `not in` | Value not found | `'z' not in 'cat'` | `True` |


## String Membership

Check if a substring exists:

```python
print('a' in 'cat')       # True
print('at' in 'cat')      # True
print('dog' in 'cat')     # False
print('z' not in 'cat')   # True
```


## List Membership

Check if an element exists:

```python
fruits = ['apple', 'banana', 'cherry']

print('apple' in fruits)    # True
print('grape' in fruits)    # False
print('grape' not in fruits) # True
```

### Boolean/Integer Gotcha

```python
print(True in [1])    # True (because True == 1)
print(False in [0])   # True (because False == 0)
print(True in [2])    # False
```

This happens because `True == 1` and `False == 0` in Python.


## Tuple Membership

Same as lists:

```python
colors = ('red', 'green', 'blue')

print('red' in colors)     # True
print('yellow' in colors)  # False
```


## Set Membership

Sets are optimized for membership testing (O(1)):

```python
numbers = {1, 2, 3, 4, 5}

print(3 in numbers)   # True
print(10 in numbers)  # False
```


## Dictionary Membership

By default, `in` checks **keys**:

```python
person = {'name': 'Alice', 'age': 30}

print('name' in person)     # True (key exists)
print('Alice' in person)    # False (not a key)
print('city' not in person) # True
```

### Check Values

```python
print('Alice' in person.values())  # True
```

### Check Key-Value Pairs

```python
print(('name', 'Alice') in person.items())  # True
```


## Performance Considerations

| Container | Time Complexity |
|-----------|-----------------|
| list | O(n) |
| tuple | O(n) |
| str | O(n) |
| set | O(1) average |
| dict | O(1) average |

For large collections with frequent lookups, use `set` or `dict`:

```python
# Slow for large lists
if item in large_list:  # O(n)
    ...

# Fast for sets
if item in large_set:   # O(1)
    ...
```


## Practical Examples

### Input Validation

```python
valid_options = {'yes', 'no', 'maybe'}

user_input = input("Enter choice: ").lower()
if user_input in valid_options:
    print("Valid choice")
else:
    print("Invalid choice")
```

### Filtering

```python
vowels = 'aeiou'
text = "Hello World"

# Filter vowels
result = [c for c in text.lower() if c in vowels]
print(result)  # ['e', 'o', 'o']
```

### Finding Missing Items

```python
required = {'name', 'email', 'phone'}
provided = {'name', 'email'}

missing = [field for field in required if field not in provided]
print(missing)  # ['phone']
```


## Range Membership

```python
print(5 in range(10))     # True
print(10 in range(10))    # False (exclusive end)
print(15 in range(0, 20, 5))  # True (0, 5, 10, 15)
```


## Custom Objects

Classes can define custom `in` behavior with `__contains__`:

```python
class EvenNumbers:
    def __contains__(self, n):
        return n % 2 == 0

evens = EvenNumbers()
print(4 in evens)   # True
print(5 in evens)   # False
```


## Summary

- `in` checks membership, `not in` checks absence
- Works with strings, lists, tuples, sets, dicts
- Dict membership checks **keys** by default
- Sets have O(1) lookup — use for frequent checks
- Use `__contains__` for custom membership logic


---

## Exercises


**Exercise 1.**
Write a function `find_missing(required, provided)` that takes two sets and returns a sorted list of items in `required` but not in `provided`. Use the `not in` operator.

??? success "Solution to Exercise 1"

    ```python
    def find_missing(required, provided):
        return sorted(item for item in required if item not in provided)

    required = {'name', 'email', 'phone', 'address'}
    provided = {'name', 'email'}
    print(find_missing(required, provided))  # ['address', 'phone']
    ```

    The function iterates over `required` and filters items absent from `provided`. Using sets for `provided` ensures O(1) lookup per check.

---

**Exercise 2.**
Demonstrate the performance difference between membership testing in a list versus a set. Create a list and set each containing numbers 0 to 99999, and time how long it takes to check if `99999` is in each.

??? success "Solution to Exercise 2"

    ```python
    import timeit

    setup_list = "lst = list(range(100000))"
    setup_set = "s = set(range(100000))"

    list_time = timeit.timeit("99999 in lst", setup=setup_list, number=1000)
    set_time = timeit.timeit("99999 in s", setup=setup_set, number=1000)

    print(f"List: {list_time:.4f}s")
    print(f"Set:  {set_time:.6f}s")
    print(f"Set is {list_time / set_time:.0f}x faster")
    ```

    List membership is O(n) because Python checks each element sequentially. Set membership is O(1) on average because sets use hash tables.

---

**Exercise 3.**
Given a dictionary `person = {'name': 'Alice', 'age': 30, 'city': 'NYC'}`, show three different membership tests: checking if a key exists, checking if a value exists, and checking if a key-value pair exists.

??? success "Solution to Exercise 3"

    ```python
    person = {'name': 'Alice', 'age': 30, 'city': 'NYC'}

    # Check key
    print('name' in person)                        # True

    # Check value
    print('Alice' in person.values())              # True

    # Check key-value pair
    print(('name', 'Alice') in person.items())     # True
    ```

    By default, `in` checks dictionary keys. Use `.values()` to check values and `.items()` to check key-value pairs.
