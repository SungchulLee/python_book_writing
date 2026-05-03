# groupby

`groupby()` groups consecutive elements with the same key, making it useful for processing sorted data. Unlike SQL-style GROUP BY or `pandas.groupby`, this function only groups elements that are adjacent in the input sequence. To group all matching elements together, sort the input by the key first. This iterator-based approach works well for streaming data where items arrive in order.

!!! tip "Mental Model"
    `groupby` draws boundaries in a sequence wherever the key changes — like dividing a sorted deck of cards into piles by suit. It only looks at consecutive runs, so if you want all matching elements grouped together, sort first. Think "consecutive-run splitter," not SQL GROUP BY.

## Basic Grouping

Without a key function, `groupby()` groups consecutive elements that are equal. Note that the trailing `1` in the example forms its own group because it is separated from the earlier `1`s by other values.

```python
from itertools import groupby

data = [1, 1, 1, 2, 2, 3, 3, 3, 3, 1]
grouped = groupby(data)

for key, group in grouped:
    print(f"{key}: {list(group)}")
```

```
1: [1, 1, 1]
2: [2, 2]
3: [3, 3, 3, 3]
1: [1]
```

The trailing `1` appears as a separate group because `groupby()` only groups consecutive elements. To group all `1`s together, sort the data first.

## Grouping with Key Function

A key function maps each element to a grouping value. `groupby()` starts a new group whenever the key value changes, so the input should be sorted by the same key for exhaustive grouping.

```python
from itertools import groupby

words = ['apple', 'apricot', 'banana', 'blueberry', 'cherry']
# Group by first letter
grouped = groupby(words, key=lambda x: x[0])

for letter, items in grouped:
    print(f"{letter}: {list(items)}")
```

```
a: ['apple', 'apricot']
b: ['banana', 'blueberry']
c: ['cherry']
```

---

## Exercises

**Exercise 1.**
Given a sorted list of `(name, department)` tuples, use `groupby` to group employees by department and return a dictionary mapping each department to a list of employee names. For example, given `[("Alice", "eng"), ("Bob", "eng"), ("Carol", "sales")]`, return `{"eng": ["Alice", "Bob"], "sales": ["Carol"]}`.

??? success "Solution to Exercise 1"

    ```python
    from itertools import groupby

    employees = [("Alice", "eng"), ("Bob", "eng"), ("Carol", "sales")]
    # Already sorted by department

    result = {}
    for dept, group in groupby(employees, key=lambda x: x[1]):
        result[dept] = [name for name, _ in group]

    print(result)
    # {'eng': ['Alice', 'Bob'], 'sales': ['Carol']}
    ```

---

**Exercise 2.**
Write a function `compress_string` that uses `groupby` to perform run-length encoding on a string. For example, `compress_string("aaabbcccc")` should return `"a3b2c4"`.

??? success "Solution to Exercise 2"

    ```python
    from itertools import groupby

    def compress_string(s):
        parts = []
        for char, group in groupby(s):
            count = sum(1 for _ in group)
            parts.append(f"{char}{count}")
        return "".join(parts)

    # Test
    print(compress_string("aaabbcccc"))  # a3b2c4
    print(compress_string("aabba"))       # a2b2a1
    ```

---

**Exercise 3.**
Write a function `group_consecutive` that takes a list of integers and groups consecutive numbers together. For example, `group_consecutive([1, 2, 3, 5, 6, 8, 9, 10])` should return `[[1, 2, 3], [5, 6], [8, 9, 10]]`. Hint: use `enumerate` and `groupby` with a key based on the difference between value and index.

??? success "Solution to Exercise 3"

    ```python
    from itertools import groupby

    def group_consecutive(nums):
        result = []
        for _, group in groupby(enumerate(nums), lambda x: x[1] - x[0]):
            result.append([val for _, val in group])
        return result

    # Test
    print(group_consecutive([1, 2, 3, 5, 6, 8, 9, 10]))
    # [[1, 2, 3], [5, 6], [8, 9, 10]]
    ```
