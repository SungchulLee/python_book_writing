# islice

`islice()` extracts a slice from an iterator without consuming the entire iterator or materializing it into memory.

!!! tip "Mental Model"
    `islice` is the iterator equivalent of list slicing (`lst[start:stop:step]`). Regular slicing requires a sequence in memory, but `islice` works on any iterator — including infinite ones — by lazily skipping and yielding elements. It consumes elements it skips, so the iterator advances; it does not rewind.

## Basic Slicing with islice

Extract specific elements from an iterator using `islice(iterable, start, stop, step)`.

```python
from itertools import islice

numbers = range(10)

# Get elements from index 2 to 5
result1 = list(islice(numbers, 2, 5))
print(result1)

# Get first 4 elements
result2 = list(islice(numbers, 4))
print(result2)

# Get every 2nd element starting from index 1
result3 = list(islice(numbers, 1, None, 2))
print(result3)
```

```
[2, 3, 4]
[0, 1, 2, 3]
[1, 3, 5, 7, 9]
```

## Practical Use Case

Use `islice()` to paginate through large datasets efficiently.

```python
from itertools import islice

def paginate(iterable, page_size):
    it = iter(iterable)
    while True:
        page = list(islice(it, page_size))
        if not page:
            break
        yield page

# Paginate a range
data = range(10)
for i, page in enumerate(paginate(data, 3)):
    print(f"Page {i}: {page}")
```

```
Page 0: [0, 1, 2]
Page 1: [3, 4, 5]
Page 2: [6, 7, 8]
Page 3: [9]
```

---

## Exercises

**Exercise 1.**
Write a function `skip_header` that takes an iterator (e.g., lines from a file) and a number of header lines to skip, then returns the remaining items as a list. Use `islice`. For example, `skip_header(iter(["header1", "header2", "data1", "data2"]), 2)` should return `["data1", "data2"]`.

??? success "Solution to Exercise 1"

    ```python
    from itertools import islice

    def skip_header(iterator, n):
        return list(islice(iterator, n, None))

    # Test
    lines = iter(["header1", "header2", "data1", "data2"])
    print(skip_header(lines, 2))  # ['data1', 'data2']
    ```

---

**Exercise 2.**
Write a function `every_nth` that takes an iterable and an integer `n`, and returns every nth element using `islice`. For example, `every_nth(range(20), 5)` should return `[0, 5, 10, 15]`.

??? success "Solution to Exercise 2"

    ```python
    from itertools import islice

    def every_nth(iterable, n):
        return list(islice(iterable, 0, None, n))

    # Test
    print(every_nth(range(20), 5))  # [0, 5, 10, 15]
    print(every_nth("abcdefghij", 3))  # ['a', 'd', 'g', 'j']
    ```

---

**Exercise 3.**
Write a function `take_between` that takes an iterable, a start index, and an end index, and returns the elements between those indices (inclusive) using `islice`. For example, `take_between("abcdefgh", 2, 5)` should return `['c', 'd', 'e', 'f']`.

??? success "Solution to Exercise 3"

    ```python
    from itertools import islice

    def take_between(iterable, start, end):
        return list(islice(iterable, start, end + 1))

    # Test
    print(take_between("abcdefgh", 2, 5))  # ['c', 'd', 'e', 'f']
    print(take_between(range(100), 10, 13))  # [10, 11, 12, 13]
    ```
