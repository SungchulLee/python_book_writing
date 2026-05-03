# Sequence Comparison

Python compares sequences (strings, lists, tuples) **lexicographically** -- element by element from left to right.

!!! tip "Mental Model"
    Lexicographic comparison works like dictionary ordering: compare the first elements; if equal, move to the second, and so on. The first difference decides the result. If one sequence is a prefix of the other, the shorter one is "less than." For strings, comparison uses Unicode code point values, so uppercase letters sort before lowercase.

## String Comparison

Strings are compared character by character using ASCII/Unicode values.

```python
print("apple" < "banana")   # True
print("apple" < "apricot")  # True (5th char: 'l' < 'r')
print("Apple" < "apple")    # True (uppercase comes first)
```

### ASCII Order

Capital letters have lower ASCII values than lowercase:

```python
print(ord('A'))  # 65
print(ord('Z'))  # 90
print(ord('a'))  # 97
print(ord('z'))  # 122
```

This means:

```python
print("Zebra" < "apple")  # True (Z=90 < a=97)
print("Girl" < "boy")     # True (G=71 < b=98)
```

**Caution**: This differs from dictionary ordering where case is typically ignored.


## List Comparison

Lists are compared element by element:

```python
print([1, 2, 3] < [1, 2, 4])  # True (3 < 4)
print([1, 2, 3] < [1, 3, 0])  # True (2 < 3, rest ignored)
print([1, 2, 3] < [2, 0, 0])  # True (1 < 2, rest ignored)
```

### First Difference Wins

```python
print([0, 1, 2] < [5, 1, 2])          # True (0 < 5)
print([0, 1, 2000000] < [0, 1, 2])    # False (2000000 > 2)
```

### String Elements

```python
print(['Jones', 'Sally'] < ['Jones', 'Fred'])  # False ('S' > 'F')
print(['Jones', 'Sally'] < ['Adams', 'Sam'])   # False ('J' > 'A')
```


## Tuple Comparison

Tuples follow the same rules as lists:

```python
print((1, 2, 3) < (1, 2, 4))  # True
print((1, 2, 3) < (1, 3, 0))  # True
print((0, 1, 2) < (5, 1, 2))  # True
```


## Comparison Algorithm

1. Compare first elements
2. If equal, compare second elements
3. Continue until a difference is found or one sequence ends
4. Shorter sequence is "less than" if all compared elements are equal

```python
print([1, 2] < [1, 2, 3])     # True (shorter)
print("ab" < "abc")           # True (shorter)
print((1, 2) == (1, 2))       # True (all equal)
```


## Chained Comparisons

Python supports chained comparisons:

```python
print(1 < 2 < 3)              # True (1<2 and 2<3)
print("a" < "b" < "c")        # True
print(1 < 2 < 3 < 4 < 5)      # True
```

This is equivalent to:

```python
print(1 < 2 and 2 < 3)        # True
```


## Mixed Type Comparison

Comparing incompatible types raises `TypeError`:

```python
# Python 3
print([1, 2] < "ab")  # TypeError: '<' not supported
print((1, 2) < [1, 2])  # TypeError
```


## Practical Use: Sorting

Lexicographic comparison enables natural sorting:

```python
names = ["Charlie", "Alice", "Bob"]
print(sorted(names))  # ['Alice', 'Bob', 'Charlie']

# Tuples sort by first element, then second
records = [("Bob", 25), ("Alice", 30), ("Bob", 20)]
print(sorted(records))  # [('Alice', 30), ('Bob', 20), ('Bob', 25)]
```


## Summary

| Sequence | Comparison Basis |
|----------|------------------|
| String | Character ASCII/Unicode values |
| List | Element-by-element comparison |
| Tuple | Element-by-element comparison |

- Comparison stops at first difference
- Shorter sequence is "less than" if prefixes match
- Case matters: `'A' < 'a'` (ASCII order)


---

## Exercises


**Exercise 1.**
Without running the code, predict the result of each comparison and explain why:

```python
print([1, 2, 3] < [1, 2, 4])
print("banana" < "cherry")
print((1, 2) < (1, 2, 0))
```

??? success "Solution to Exercise 1"

    ```python
    print([1, 2, 3] < [1, 2, 4])   # True  (3 < 4 at index 2)
    print("banana" < "cherry")      # True  ('b' < 'c')
    print((1, 2) < (1, 2, 0))      # True  (prefix match, shorter is less)
    ```

    Lexicographic comparison proceeds element by element. If all compared elements are equal, the shorter sequence is considered less than the longer one.

---

**Exercise 2.**
Write a function `sort_names_case_insensitive(names)` that sorts a list of names lexicographically, ignoring case. For example, `["charlie", "Alice", "Bob"]` should become `["Alice", "Bob", "charlie"]`.

??? success "Solution to Exercise 2"

    ```python
    def sort_names_case_insensitive(names):
        return sorted(names, key=str.lower)

    result = sort_names_case_insensitive(["charlie", "Alice", "Bob"])
    print(result)  # ['Alice', 'Bob', 'charlie']
    ```

    Using `str.lower` as the key function ensures that comparison ignores case while preserving the original casing in the output.

---

**Exercise 3.**
Given a list of `(last_name, first_name)` tuples, sort them by last name first, then by first name. Demonstrate with at least 4 entries where some share the same last name.

??? success "Solution to Exercise 3"

    ```python
    people = [
        ("Smith", "Alice"),
        ("Jones", "Bob"),
        ("Smith", "Charlie"),
        ("Jones", "Alice"),
    ]

    sorted_people = sorted(people)
    for last, first in sorted_people:
        print(f"{last}, {first}")
    # Jones, Alice
    # Jones, Bob
    # Smith, Alice
    # Smith, Charlie
    ```

    Tuples are compared lexicographically, so sorting by the tuple itself sorts by last name first, then by first name when last names are equal.
