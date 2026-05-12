# operator Module

The `operator` module provides function equivalents for Python's built-in operators. These are faster than lambdas and cleaner for functional programming.

!!! tip "Mental Model"
    Every Python operator (`+`, `[]`, `.attr`) has a function twin in the `operator` module. These named functions are faster than equivalent lambdas (they're implemented in C) and make functional code more readable -- `itemgetter('name')` says what it does more clearly than `lambda x: x['name']`.

```python
import operator
# or
from operator import itemgetter, attrgetter, methodcaller
```

---

## Why Use operator?

```python
from operator import add, mul

# Lambda (slower, verbose)
result = reduce(lambda x, y: x + y, numbers)

# operator (faster, cleaner)
result = reduce(add, numbers)
```

Benefits:

- **Faster**: Implemented in C
- **Cleaner**: More readable than lambdas
- **Documented**: Clear intent from function name

---

## itemgetter

Retrieve items by index or key. Returns a callable.

### Single Item

```python
from operator import itemgetter

# Get item at index 1
get_second = itemgetter(1)

print(get_second([10, 20, 30]))  # 20
print(get_second("hello"))       # 'e'
print(get_second({'a': 1, 'b': 2, 1: 'x'}))  # 'x'
```

### Multiple Items

```python
from operator import itemgetter

# Get multiple items
get_first_and_third = itemgetter(0, 2)

print(get_first_and_third([10, 20, 30, 40]))  # (10, 30)
print(get_first_and_third("hello"))           # ('h', 'l')
```

### Sorting with itemgetter

```python
from operator import itemgetter

# Sort list of tuples by second element
pairs = [(1, 'b'), (3, 'a'), (2, 'c')]
sorted(pairs, key=itemgetter(1))
# [(3, 'a'), (1, 'b'), (2, 'c')]

# Sort by multiple keys
data = [(1, 'b', 30), (2, 'a', 20), (1, 'a', 10)]
sorted(data, key=itemgetter(0, 1))
# [(1, 'a', 10), (1, 'b', 30), (2, 'a', 20)]
```

### With Dictionaries

```python
from operator import itemgetter

records = [
    {'name': 'Alice', 'age': 30, 'score': 85},
    {'name': 'Bob', 'age': 25, 'score': 92},
    {'name': 'Charlie', 'age': 35, 'score': 78},
]

# Sort by score
sorted(records, key=itemgetter('score'))
# [{'name': 'Charlie'...}, {'name': 'Alice'...}, {'name': 'Bob'...}]

# Get specific fields
get_name_and_score = itemgetter('name', 'score')
[get_name_and_score(r) for r in records]
# [('Alice', 85), ('Bob', 92), ('Charlie', 78)]
```

---

## attrgetter

Retrieve attributes from objects. Returns a callable.

### Single Attribute

```python
from operator import attrgetter

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

people = [
    Person('Alice', 30),
    Person('Bob', 25),
    Person('Charlie', 35),
]

# Sort by age
get_age = attrgetter('age')
sorted(people, key=get_age)
# [Bob(25), Alice(30), Charlie(35)]

# Equivalent lambda (slower)
sorted(people, key=lambda p: p.age)
```

### Multiple Attributes

```python
from operator import attrgetter

# Get multiple attributes
get_name_and_age = attrgetter('name', 'age')

for person in people:
    print(get_name_and_age(person))
# ('Alice', 30)
# ('Bob', 25)
# ('Charlie', 35)
```

### Nested Attributes

```python
from operator import attrgetter

class Address:
    def __init__(self, city):
        self.city = city

class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address

people = [
    Person('Alice', Address('NYC')),
    Person('Bob', Address('LA')),
]

# Access nested attribute
get_city = attrgetter('address.city')
[get_city(p) for p in people]
# ['NYC', 'LA']

# Equivalent lambda
[p.address.city for p in people]
```

### Sorting by Multiple Attributes

```python
from operator import attrgetter

class Student:
    def __init__(self, name, grade, age):
        self.name = name
        self.grade = grade
        self.age = age

students = [
    Student('Alice', 85, 20),
    Student('Bob', 92, 19),
    Student('Charlie', 85, 21),
]

# Sort by grade, then by age
sorted(students, key=attrgetter('grade', 'age'))
# [Alice(85, 20), Charlie(85, 21), Bob(92, 19)]
```

---

## methodcaller

Call a method with specified arguments. Returns a callable.

### Basic Usage

```python
from operator import methodcaller

# Create a method caller
upper = methodcaller('upper')
strip_x = methodcaller('strip', 'x')

print(upper('hello'))      # 'HELLO'
print(strip_x('xxhelloxx'))  # 'hello'
```

### With Collections

```python
from operator import methodcaller

strings = ['  hello  ', '  world  ', '  python  ']

# Strip all strings
list(map(methodcaller('strip'), strings))
# ['hello', 'world', 'python']

# Split all strings
sentences = ['a b c', 'x y z']
list(map(methodcaller('split'), sentences))
# [['a', 'b', 'c'], ['x', 'y', 'z']]
```

### Sorting with Methods

```python
from operator import methodcaller

# Sort strings by lowercase
words = ['Banana', 'apple', 'Cherry']
sorted(words, key=methodcaller('lower'))
# ['apple', 'Banana', 'Cherry']

# Sort by custom method
class Task:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority
    
    def get_sort_key(self):
        return (-self.priority, self.name)

tasks = [Task('A', 1), Task('B', 2), Task('C', 1)]
sorted(tasks, key=methodcaller('get_sort_key'))
```

---

## Arithmetic Operators

```python
from operator import add, sub, mul, truediv, floordiv, mod, pow, neg

add(2, 3)       # 5       (2 + 3)
sub(5, 2)       # 3       (5 - 2)
mul(3, 4)       # 12      (3 * 4)
truediv(7, 2)   # 3.5     (7 / 2)
floordiv(7, 2)  # 3       (7 // 2)
mod(7, 3)       # 1       (7 % 3)
pow(2, 3)       # 8       (2 ** 3)
neg(5)          # -5      (-5)
```

### With reduce

```python
from functools import reduce
from operator import add, mul

numbers = [1, 2, 3, 4, 5]

# Sum
reduce(add, numbers)  # 15

# Product
reduce(mul, numbers)  # 120
```

---

## Comparison Operators

```python
from operator import eq, ne, lt, le, gt, ge

eq(2, 2)   # True   (2 == 2)
ne(2, 3)   # True   (2 != 3)
lt(2, 3)   # True   (2 < 3)
le(2, 2)   # True   (2 <= 2)
gt(3, 2)   # True   (3 > 2)
ge(3, 3)   # True   (3 >= 3)
```

### Filtering with Comparisons

```python
from operator import lt
from functools import partial

# Filter values less than 5
is_small = partial(lt, 5)  # Note: lt(5, x) means 5 < x
# This is actually "is greater than 5"!

# For "less than 5", use:
from operator import gt
is_less_than_5 = partial(gt, 5)  # gt(5, x) means 5 > x

numbers = [1, 3, 5, 7, 9]
list(filter(is_less_than_5, numbers))  # [1, 3]
```

---

## Logical Operators

```python
from operator import and_, or_, not_, xor

# Bitwise operations
and_(5, 3)   # 1  (0b101 & 0b011 = 0b001)
or_(5, 3)    # 7  (0b101 | 0b011 = 0b111)
xor(5, 3)    # 6  (0b101 ^ 0b011 = 0b110)
not_(0)      # True

# Note: and_, or_ are BITWISE, not logical!
# For logical operations, use: all(), any()
```

---

## Sequence Operators

```python
from operator import concat, contains, countOf, indexOf

concat([1, 2], [3, 4])      # [1, 2, 3, 4]
concat('hello', ' world')    # 'hello world'

contains([1, 2, 3], 2)       # True
contains('hello', 'ell')     # True

countOf([1, 2, 2, 3, 2], 2)  # 3
indexOf([1, 2, 3], 2)        # 1
```

---

## In-Place Operators

```python
from operator import iadd, isub, imul

# These modify mutable objects in place
lst = [1, 2]
iadd(lst, [3, 4])  # lst is now [1, 2, 3, 4]

# For immutables, they return new objects
x = 5
x = iadd(x, 3)  # x is now 8
```

---

## Practical Examples

### Extract Multiple Fields

```python
from operator import itemgetter

data = [
    ('Alice', 30, 'NYC', 85),
    ('Bob', 25, 'LA', 92),
    ('Charlie', 35, 'SF', 78),
]

# Extract name and score
extract = itemgetter(0, 3)
[extract(row) for row in data]
# [('Alice', 85), ('Bob', 92), ('Charlie', 78)]
```

### Sort Dictionary by Value

```python
from operator import itemgetter

scores = {'Alice': 85, 'Bob': 92, 'Charlie': 78}

# Sort by value (ascending)
sorted(scores.items(), key=itemgetter(1))
# [('Charlie', 78), ('Alice', 85), ('Bob', 92)]

# Sort by value (descending)
sorted(scores.items(), key=itemgetter(1), reverse=True)
# [('Bob', 92), ('Alice', 85), ('Charlie', 78)]
```

### Group and Sort Objects

```python
from operator import attrgetter
from itertools import groupby

class Task:
    def __init__(self, category, priority, name):
        self.category = category
        self.priority = priority
        self.name = name

tasks = [
    Task('work', 1, 'Email'),
    Task('home', 2, 'Laundry'),
    Task('work', 2, 'Meeting'),
    Task('home', 1, 'Dishes'),
]

# Sort by category, then priority
tasks.sort(key=attrgetter('category', 'priority'))

# Group by category
for category, group in groupby(tasks, key=attrgetter('category')):
    print(f"{category}: {[t.name for t in group]}")
```

### Calculate with reduce

```python
from functools import reduce
from operator import mul, add

# Factorial
def factorial(n):
    return reduce(mul, range(1, n + 1), 1)

print(factorial(5))  # 120

# Dot product
def dot_product(v1, v2):
    return reduce(add, map(mul, v1, v2))

print(dot_product([1, 2, 3], [4, 5, 6]))  # 32
```

---

## Performance Comparison

```python
import timeit
from operator import itemgetter, attrgetter

data = [(i, str(i)) for i in range(1000)]

# Lambda vs itemgetter
lambda_time = timeit.timeit(
    lambda: sorted(data, key=lambda x: x[1]),
    number=1000
)
itemgetter_time = timeit.timeit(
    lambda: sorted(data, key=itemgetter(1)),
    number=1000
)

print(f"lambda:     {lambda_time:.3f}s")
print(f"itemgetter: {itemgetter_time:.3f}s")
# itemgetter is typically 10-20% faster
```

---

## Summary

| Function | Purpose | Example |
|----------|---------|---------|
| `itemgetter(k)` | Get item by key/index | `itemgetter(1)(lst)` |
| `attrgetter(a)` | Get attribute | `attrgetter('name')(obj)` |
| `methodcaller(m)` | Call method | `methodcaller('upper')(s)` |
| `add`, `mul`, etc. | Arithmetic | `reduce(add, nums)` |
| `eq`, `lt`, etc. | Comparison | `filter(partial(lt, 5), nums)` |

**Key Takeaways**:

- `itemgetter` and `attrgetter` are faster than lambdas
- Use for sorting: `sorted(data, key=itemgetter('field'))`
- Support multiple keys: `itemgetter(0, 2)`, `attrgetter('a', 'b')`
- `attrgetter` supports nested attributes: `attrgetter('a.b.c')`
- Arithmetic operators work with `reduce` for aggregations
- All functions are implemented in C for performance

---

## Exercises

**Exercise 1.**
Given a list of tuples `[("Alice", 88), ("Bob", 95), ("Charlie", 72)]`, use `operator.itemgetter` to sort them by score (index 1). Then use `itemgetter` to extract just the names from the sorted list. Print both results.

??? success "Solution to Exercise 1"

        from operator import itemgetter

        students = [("Alice", 88), ("Bob", 95), ("Charlie", 72)]

        by_score = sorted(students, key=itemgetter(1))
        print(by_score)
        # [('Charlie', 72), ('Alice', 88), ('Bob', 95)]

        names = list(map(itemgetter(0), by_score))
        print(names)  # ['Charlie', 'Alice', 'Bob']

---

**Exercise 2.**
Use `functools.reduce` with `operator.mul` to compute the factorial of a number `n`. Write a `factorial(n)` function that handles `n == 0` (returns 1) and positive integers. Compare with using a lambda.

??? success "Solution to Exercise 2"

        from functools import reduce
        from operator import mul

        def factorial(n):
            if n == 0:
                return 1
            return reduce(mul, range(1, n + 1))

        print(factorial(0))   # 1
        print(factorial(5))   # 120
        print(factorial(10))  # 3628800

        # Lambda version for comparison
        factorial_lambda = lambda n: 1 if n == 0 else reduce(lambda a, b: a * b, range(1, n + 1))
        print(factorial_lambda(5))  # 120

---

**Exercise 3.**
Create a list of objects with a `.name` and `.score` attribute (use a simple class or `namedtuple`). Use `operator.attrgetter("score")` to sort them by score, then use `operator.methodcaller("upper")` to convert all names to uppercase. Print the sorted names.

??? success "Solution to Exercise 3"

        from operator import attrgetter, methodcaller
        from collections import namedtuple

        Student = namedtuple("Student", ["name", "score"])
        students = [
            Student("alice", 88),
            Student("bob", 95),
            Student("charlie", 72),
        ]

        by_score = sorted(students, key=attrgetter("score"))
        print(by_score)

        upper = methodcaller("upper")
        names = [upper(s.name) for s in by_score]
        print(names)  # ['CHARLIE', 'ALICE', 'BOB']
