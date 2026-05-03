# functools.reduce

`reduce` applies a two-argument function cumulatively to the items of a sequence, reducing it to a single value. It was a built-in in Python 2 and moved to `functools` in Python 3.

!!! tip "Mental Model"
    `reduce` is a left fold: it takes the first two elements, combines them with your function, then combines that result with the next element, and so on until one value remains. Picture a snowball rolling downhill, accumulating each element as it goes. For most cases Python offers clearer alternatives (`sum`, `math.prod`, `str.join`), but `reduce` is the general-purpose tool when none of those fit.

```python
from functools import reduce
```

---

## Basic Usage

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]
total = reduce(lambda acc, x: acc + x, numbers)
print(total)  # 15
```

### Step-by-Step Execution

```
reduce(f, [a, b, c, d])

Step 1: result = f(a, b)
Step 2: result = f(result, c)
Step 3: result = f(result, d)
→ return result
```

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Trace execution
def add_verbose(acc, x):
    result = acc + x
    print(f"  f({acc}, {x}) = {result}")
    return result

reduce(add_verbose, numbers)
#   f(1, 2) = 3
#   f(3, 3) = 6
#   f(6, 4) = 10
#   f(10, 5) = 15
```

---

## Signature

```python
reduce(function, iterable[, initializer])
```

| Parameter | Description |
|-----------|-------------|
| `function` | Two-argument callable: `f(accumulator, current_item)` |
| `iterable` | Sequence to reduce |
| `initializer` | Optional starting value (placed before items) |

---

## With Initializer

The initializer is placed before the first item as the initial accumulator:

```python
from functools import reduce

# Without initializer: first element is the initial accumulator
result = reduce(lambda acc, x: acc + x, [1, 2, 3])
print(result)  # 6

# With initializer: starts from 10
result = reduce(lambda acc, x: acc + x, [1, 2, 3], 10)
print(result)  # 16 (10 + 1 + 2 + 3)
```

### Why Use an Initializer

```python
from functools import reduce

# 1. Handle empty sequences
reduce(lambda a, b: a + b, [])       # TypeError!
reduce(lambda a, b: a + b, [], 0)    # 0 — safe

# 2. Different accumulator type than elements
words = ["hello", "world", "python"]
result = reduce(lambda acc, w: acc + len(w), words, 0)
print(result)  # 16 (accumulator is int, elements are str)

# 3. Build a different structure
pairs = [("a", 1), ("b", 2), ("c", 3)]
result = reduce(lambda acc, pair: {**acc, pair[0]: pair[1]}, pairs, {})
print(result)  # {'a': 1, 'b': 2, 'c': 3}
```

---

## Practical Examples

### Product of All Elements

```python
from functools import reduce
import operator

numbers = [1, 2, 3, 4, 5]

# With lambda
product = reduce(lambda a, b: a * b, numbers)
print(product)  # 120

# Cleaner with operator.mul
product = reduce(operator.mul, numbers)
print(product)  # 120

# Note: Python 3.8+ has math.prod
import math
print(math.prod(numbers))  # 120
```

### Flatten Nested Lists

```python
from functools import reduce

nested = [[1, 2], [3, 4], [5, 6]]
flat = reduce(lambda acc, x: acc + x, nested)
print(flat)  # [1, 2, 3, 4, 5, 6]

# Note: this is O(n²) due to list concatenation
# Better alternative for large lists:
from itertools import chain
flat = list(chain.from_iterable(nested))
```

### Find Maximum / Minimum

```python
from functools import reduce

numbers = [3, 1, 4, 1, 5, 9, 2, 6]

maximum = reduce(lambda a, b: a if a > b else b, numbers)
print(maximum)  # 9

minimum = reduce(lambda a, b: a if a < b else b, numbers)
print(minimum)  # 1

# Built-ins are clearer:
print(max(numbers))  # 9
print(min(numbers))  # 1
```

### Compose Functions

```python
from functools import reduce

def compose(*funcs):
    """Compose functions right-to-left: compose(f, g, h)(x) = f(g(h(x)))"""
    return reduce(lambda f, g: lambda x: f(g(x)), funcs)

add_one = lambda x: x + 1
double = lambda x: x * 2
square = lambda x: x ** 2

pipeline = compose(square, double, add_one)
# square(double(add_one(x)))
print(pipeline(3))  # 64 = ((3+1)*2)^2
```

### Build a Dictionary

```python
from functools import reduce

# Count character frequencies
text = "hello world"
freq = reduce(
    lambda acc, ch: {**acc, ch: acc.get(ch, 0) + 1},
    text,
    {}
)
print(freq)  # {'h': 1, 'e': 1, 'l': 3, 'o': 2, ' ': 1, 'w': 1, 'r': 1, 'd': 1}

# Note: Counter is better for this:
from collections import Counter
print(Counter(text))
```

### Nested Dictionary Access

```python
from functools import reduce

data = {
    'user': {
        'profile': {
            'name': 'Alice',
            'settings': {'theme': 'dark'}
        }
    }
}

def deep_get(d, keys):
    """Safely navigate nested dicts."""
    return reduce(lambda acc, key: acc.get(key, {}) if isinstance(acc, dict) else None, keys, d)

print(deep_get(data, ['user', 'profile', 'name']))          # Alice
print(deep_get(data, ['user', 'profile', 'settings']))      # {'theme': 'dark'}
print(deep_get(data, ['user', 'nonexistent', 'key']))       # {}
```

### Boolean Logic

```python
from functools import reduce
import operator

values = [True, True, False, True]

# All true?
all_true = reduce(operator.and_, values)
print(all_true)  # False

# Any true?
any_true = reduce(operator.or_, values)
print(any_true)  # True

# Built-ins are clearer:
print(all(values))  # False
print(any(values))  # True
```

---

## reduce vs Built-in Alternatives

Many common uses of `reduce` have clearer built-in equivalents:

| Operation | reduce | Built-in |
|-----------|--------|----------|
| Sum | `reduce(operator.add, seq)` | `sum(seq)` |
| Product | `reduce(operator.mul, seq)` | `math.prod(seq)` (3.8+) |
| Maximum | `reduce(max, seq)` | `max(seq)` |
| Minimum | `reduce(min, seq)` | `min(seq)` |
| All true | `reduce(operator.and_, seq)` | `all(seq)` |
| Any true | `reduce(operator.or_, seq)` | `any(seq)` |
| Concatenate | `reduce(operator.add, lists)` | `list(chain(*lists))` |
| Join strings | `reduce(lambda a, b: a+b, strs)` | `"".join(strs)` |

**Rule of thumb**: if a built-in exists, prefer it. Use `reduce` for operations that don't have built-in equivalents.

---

## When reduce Shines

`reduce` is genuinely useful when there's no built-in alternative:

```python
from functools import reduce

# 1. Function composition
compose = lambda *fns: reduce(lambda f, g: lambda x: f(g(x)), fns)

# 2. Deep dictionary merging
def deep_merge(d1, d2):
    result = {**d1}
    for k, v in d2.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result

configs = [
    {'db': {'host': 'localhost'}},
    {'db': {'port': 5432}},
    {'db': {'host': 'prod.server'}},
]
merged = reduce(deep_merge, configs)
print(merged)  # {'db': {'host': 'prod.server', 'port': 5432}}

# 3. Cumulative operations with complex state
from functools import reduce

transactions = [100, -50, 200, -30, -80]
final_balance = reduce(
    lambda state, txn: {
        'balance': state['balance'] + txn,
        'min_balance': min(state['min_balance'], state['balance'] + txn),
        'n_transactions': state['n_transactions'] + 1
    },
    transactions,
    {'balance': 0, 'min_balance': 0, 'n_transactions': 0}
)
print(final_balance)
# {'balance': 140, 'min_balance': -30, 'n_transactions': 5}
```

---

## Edge Cases

### Single Element

```python
from functools import reduce

# Single element, no initializer: returns the element (function never called)
result = reduce(lambda a, b: a + b, [42])
print(result)  # 42

# Single element with initializer: function called once
result = reduce(lambda a, b: a + b, [42], 10)
print(result)  # 52
```

### Empty Sequence

```python
from functools import reduce

# Empty sequence without initializer: TypeError
# reduce(lambda a, b: a + b, [])  # TypeError!

# Empty sequence with initializer: returns initializer
result = reduce(lambda a, b: a + b, [], 0)
print(result)  # 0
```

---

## Performance Considerations

```python
from functools import reduce

# String concatenation with reduce: O(n²)
words = ["hello"] * 1000
result = reduce(lambda a, b: a + " " + b, words)  # Slow!

# str.join: O(n)
result = " ".join(words)  # Fast!

# List concatenation with reduce: O(n²)
lists = [[i] for i in range(1000)]
result = reduce(lambda a, b: a + b, lists)  # Slow!

# itertools.chain: O(n)
from itertools import chain
result = list(chain.from_iterable(lists))  # Fast!
```

---

## Summary

| Feature | Details |
|---------|---------|
| Import | `from functools import reduce` |
| Signature | `reduce(function, iterable[, initializer])` |
| Returns | Single accumulated value |
| Empty seq | TypeError without initializer; returns initializer with one |
| Single elem | Returns element (function not called) without initializer |

**Key Takeaways**:

- `reduce` folds a sequence into a single value using a two-argument function
- Always provide an initializer for empty sequences and mixed-type accumulations
- Prefer built-in alternatives (`sum`, `max`, `min`, `all`, `any`, `str.join`) when available
- `reduce` excels at function composition, deep merging, and complex accumulations
- Watch for O(n²) performance with string/list concatenation — use `join` or `chain` instead
- Guido van Rossum deliberately moved `reduce` out of built-ins because it's often less readable than loops or comprehensions

---

## Exercises

**Exercise 1.**
Use `functools.reduce` to flatten a list of lists into a single list. For example, `[[1, 2], [3, 4], [5]]` should become `[1, 2, 3, 4, 5]`. Provide an initializer of `[]` to handle the edge case of an empty input list.

??? success "Solution to Exercise 1"

        from functools import reduce

        nested = [[1, 2], [3, 4], [5]]
        flat = reduce(lambda acc, lst: acc + lst, nested, [])
        print(flat)  # [1, 2, 3, 4, 5]

        # Edge case
        empty = reduce(lambda acc, lst: acc + lst, [], [])
        print(empty)  # []

---

**Exercise 2.**
Use `reduce` to compose a list of single-argument functions into one function that applies them left to right. Given `[str.strip, str.lower, lambda s: s.replace(" ", "_")]`, the composed function applied to `"  Hello World  "` should produce `"hello_world"`.

??? success "Solution to Exercise 2"

        from functools import reduce

        def compose(*funcs):
            """Compose functions left to right using reduce."""
            return reduce(lambda f, g: lambda x: g(f(x)), funcs)

        pipeline = compose(
            str.strip,
            str.lower,
            lambda s: s.replace(" ", "_"),
        )

        print(pipeline("  Hello World  "))  # hello_world

---

**Exercise 3.**
Use `reduce` with an initializer to build a nested dictionary from a list of keys. For example, given `["a", "b", "c"]` and value `42`, produce `{"a": {"b": {"c": 42}}}`. Write this as a function `nest_keys(keys, value)`.

??? success "Solution to Exercise 3"

        from functools import reduce

        def nest_keys(keys, value):
            """Build nested dict from keys list and a leaf value."""
            return reduce(
                lambda acc, key: {key: acc},
                reversed(keys),
                value,
            )

        result = nest_keys(["a", "b", "c"], 42)
        print(result)  # {'a': {'b': {'c': 42}}}

        result2 = nest_keys(["x"], "hello")
        print(result2)  # {'x': 'hello'}
