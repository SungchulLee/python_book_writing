# Iterables and Iterators

Iteration is a core concept in Python. Understanding **iterables** and **iterators** explains how `for` loops, comprehensions, and many built-ins work.

!!! tip "Mental Model"
    An iterable is anything you can loop over; an iterator is the cursor that tracks your position in that loop. Calling `iter()` on an iterable creates an iterator; calling `next()` on that iterator advances it by one step. When there are no more items, the iterator raises `StopIteration` and the `for` loop ends.

---

## Iterables

An **iterable** is any object that can be looped over.

Examples:
- lists, tuples, strings
- dictionaries
- sets
- files

Formally, an object is iterable if it implements `__iter__()`.

```python
iter([1, 2, 3])
```

---

## Iterators

An **iterator** is an object that:
- produces values one at a time,
- remembers its state,
- raises `StopIteration` when exhausted.

It implements:
- `__iter__()` — returns itself
- `__next__()` — returns next value

---

## Iterable vs Iterator

| Feature | Iterable | Iterator |
|---------|----------|----------|
| Has `__iter__()` | ✅ | ✅ |
| Has `__next__()` | ❌ | ✅ |
| Can use in `for` | ✅ | ✅ |
| Can call `next()` | ❌ (need `iter()`) | ✅ |

```python
nums = [1, 2, 3]           # Iterable
it = iter(nums)            # Iterator

print("__iter__" in dir(nums))  # True
print("__next__" in dir(nums))  # False
print("__next__" in dir(it))    # True
```

---

## How `for` Loop Works

When you write:

```python
for x in [1, 2, 3]:
    print(x)
```

Python does this internally:

```python
it = iter([1, 2, 3])
while True:
    try:
        x = next(it)
        print(x)
    except StopIteration:
        break
```

---

## Built-in Iterators

These functions return **iterators** (lazy evaluation):

| Function | Description |
|----------|-------------|
| `zip()` | Pairs elements from multiple iterables |
| `enumerate()` | Pairs index with element |
| `map()` | Applies function to each element |
| `filter()` | Filters elements by predicate |
| `reversed()` | Reverses a sequence |

```python
# All return iterators
z = zip([1, 2], ['a', 'b'])
e = enumerate(['x', 'y'])
m = map(str.upper, ['a', 'b'])
f = filter(lambda x: x > 0, [-1, 2, 3])

print(next(z))  # (1, 'a')
print(next(e))  # (0, 'x')
print(next(m))  # 'A'
print(next(f))  # 2
```

---

## Custom Iterator

Create your own iterator by implementing the protocol:

```python
class CountUp:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.limit:
            raise StopIteration
        self.current += 1
        return self.current

for n in CountUp(3):
    print(n)  # 1, 2, 3
```

---

## Single-pass Nature

Iterators are **consumed** as you iterate:

```python
it = iter([1, 2, 3])
list(it)   # [1, 2, 3]
list(it)   # [] (exhausted)
```

---

## Key Takeaways

- **Iterables** can produce iterators via `iter()`
- **Iterators** yield values lazily via `next()`
- Iterators are single-use
- `for` loop uses `iter()` and `next()` internally
- `zip`, `map`, `filter`, `enumerate` return iterators

---

## Runnable Example: `iteration_basics.py`

```python
"""
PYTHON GENERATORS & ITERATORS - BEGINNER LEVEL
==============================================

Topic: Understanding Iteration Basics
--------------------------------------

This module covers:
1. What are iterables and iterators?
2. The iteration protocol in Python
3. Built-in iterators
4. Creating custom iterators with classes
5. The __iter__() and __next__() methods

Learning Objectives:
- Understand the difference between iterables and iterators
- Learn how Python's iteration protocol works
- Create custom iterator classes
- Handle StopIteration exceptions properly

Prerequisites:
- Basic Python (variables, functions, loops)
- Understanding of classes and objects
- Basic exception handling
"""

# ============================================================================
# SECTION 1: WHAT IS AN ITERABLE?
# ============================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SECTION 1: ITERABLES")
    print("=" * 70)

    """
    ITERABLE: An object that can return an iterator

    An iterable is any Python object that implements the __iter__() method,
    which returns an iterator object. Common iterables include:
    - Lists, tuples, strings, dictionaries, sets
    - Files
    - Custom objects that implement __iter__()

    Key point: An iterable is NOT the same as an iterator!
    """

    # Example 1.1: Common iterables
    print("\n--- Example 1.1: Common Iterables ---")

    # List is an iterable
    my_list = [1, 2, 3, 4, 5]
    print(f"List: {my_list}")
    print(f"Is it an iterable? {hasattr(my_list, '__iter__')}")  # True

    # String is an iterable
    my_string = "Hello"
    print(f"\nString: {my_string}")
    print(f"Is it an iterable? {hasattr(my_string, '__iter__')}")  # True

    # Tuple is an iterable
    my_tuple = (10, 20, 30)
    print(f"\nTuple: {my_tuple}")
    print(f"Is it an iterable? {hasattr(my_tuple, '__iter__')}")  # True

    # Dictionary is an iterable (iterates over keys by default)
    my_dict = {'a': 1, 'b': 2, 'c': 3}
    print(f"\nDictionary: {my_dict}")
    print(f"Is it an iterable? {hasattr(my_dict, '__iter__')}")  # True


    # Example 1.2: Iterating over iterables with for loop
    print("\n--- Example 1.2: For Loop Behind the Scenes ---")

    """
    When you use a for loop, Python:
    1. Calls iter() on the iterable to get an iterator
    2. Repeatedly calls next() on the iterator
    3. Catches StopIteration exception to know when to stop

    Let's see this in action:
    """

    # Using a for loop (the Pythonic way)
    print("Using for loop:")
    for item in [1, 2, 3]:
        print(item)

    # What Python actually does (manual iteration)
    print("\nManual iteration (what Python does internally):")
    my_list = [1, 2, 3]
    iterator = iter(my_list)  # Get an iterator from the iterable

    try:
        while True:
            item = next(iterator)  # Get next item
            print(item)
    except StopIteration:
        # This exception signals the end of iteration
        pass


    # ============================================================================
    # SECTION 2: WHAT IS AN ITERATOR?
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 2: ITERATORS")
    print("=" * 70)

    """
    ITERATOR: An object that represents a stream of data

    An iterator is an object that implements two methods:
    1. __iter__(): Returns the iterator object itself
    2. __next__(): Returns the next value in the sequence
                    or raises StopIteration when exhausted

    Key characteristics:
    - Iterators are also iterables (they have __iter__ method)
    - Iterators maintain state (remember their position)
    - Iterators can only be iterated once
    - Once exhausted, they remain exhausted
    """

    # Example 2.1: Getting an iterator from an iterable
    print("\n--- Example 2.1: Creating Iterators ---")

    my_list = [10, 20, 30]
    print(f"Original list: {my_list}")

    # Get an iterator from the list
    my_iterator = iter(my_list)
    print(f"Iterator object: {my_iterator}")
    print(f"Type: {type(my_iterator)}")

    # Check if it has required methods
    print(f"Has __iter__? {hasattr(my_iterator, '__iter__')}")
    print(f"Has __next__? {hasattr(my_iterator, '__next__')}")


    # Example 2.2: Using next() to iterate manually
    print("\n--- Example 2.2: Manual Iteration with next() ---")

    my_list = ['apple', 'banana', 'cherry']
    my_iterator = iter(my_list)

    # Get items one at a time using next()
    print(f"First call to next(): {next(my_iterator)}")   # apple
    print(f"Second call to next(): {next(my_iterator)}")  # banana
    print(f"Third call to next(): {next(my_iterator)}")   # cherry

    # What happens when we call next() after exhaustion?
    try:
        print(f"Fourth call to next(): {next(my_iterator)}")
    except StopIteration:
        print("StopIteration exception raised - iterator is exhausted")


    # Example 2.3: Iterators are consumed after one use
    print("\n--- Example 2.3: Iterators are One-Time Use ---")

    my_list = [1, 2, 3]
    my_iterator = iter(my_list)

    # First iteration
    print("First iteration:")
    for item in my_iterator:
        print(item)

    # Second iteration - nothing happens because iterator is exhausted
    print("\nSecond iteration (iterator already exhausted):")
    for item in my_iterator:
        print(item)  # This won't print anything

    # Note: We can create a new iterator to iterate again
    print("\nCreating new iterator:")
    new_iterator = iter(my_list)
    for item in new_iterator:
        print(item)


    # ============================================================================
    # SECTION 3: THE ITERATION PROTOCOL
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 3: THE ITERATION PROTOCOL")
    print("=" * 70)

    """
    The iteration protocol defines how iteration works in Python:

    ITERABLE PROTOCOL:
    - Object must implement __iter__() method
    - __iter__() returns an iterator object

    ITERATOR PROTOCOL:
    - Object must implement __iter__() and __next__() methods
    - __iter__() returns self (the iterator itself)
    - __next__() returns the next value or raises StopIteration
    """

    # Example 3.1: Understanding the protocol with built-in iter() and next()
    print("\n--- Example 3.1: The iter() and next() Functions ---")

    """
    iter(obj): Calls obj.__iter__() and returns an iterator
    next(iterator): Calls iterator.__next__() and returns next value
    """

    my_list = [100, 200, 300]

    # These are equivalent:
    iterator1 = iter(my_list)       # Calls my_list.__iter__()
    iterator2 = my_list.__iter__()  # Direct method call

    print(f"Using iter(): {next(iterator1)}")      # 100
    print(f"Using __iter__(): {next(iterator2)}")  # 100


    # Example 3.2: Iterator returns itself from __iter__()
    print("\n--- Example 3.2: Iterator Returns Itself ---")

    my_list = [1, 2, 3]
    my_iterator = iter(my_list)

    # Calling iter() on an iterator returns itself
    same_iterator = iter(my_iterator)

    print(f"Original iterator: {id(my_iterator)}")
    print(f"After iter(): {id(same_iterator)}")
    print(f"Same object? {my_iterator is same_iterator}")  # True

    # This is why iterators must implement __iter__() returning self
    print(f"\nNext from original: {next(my_iterator)}")  # 1
    print(f"Next from 'same': {next(same_iterator)}")    # 2 (shares state!)


    # ============================================================================
    # SECTION 4: CREATING CUSTOM ITERATORS
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 4: CUSTOM ITERATOR CLASSES")
    print("=" * 70)

    """
    To create a custom iterator, we need a class that implements:
    1. __iter__(self): Returns self
    2. __next__(self): Returns next value or raises StopIteration

    Let's build iterators from scratch to understand them deeply.
    """

    # Example 4.1: Simple counter iterator
    print("\n--- Example 4.1: Simple Counter Iterator ---")


    class Counter:
        """
        A simple iterator that counts from start to end.

        This iterator demonstrates the basic structure of an iterator class.
        It maintains internal state (current) and implements both required methods.
        """

        def __init__(self, start, end):
            """
            Initialize the counter with start and end values.

            Args:
                start: The starting number (inclusive)
                end: The ending number (inclusive)
            """
            self.current = start  # Current position in iteration
            self.end = end        # Where to stop

        def __iter__(self):
            """
            Return the iterator object (self).

            This method makes the object iterable. For iterators,
            it should always return self.
            """
            return self

        def __next__(self):
            """
            Return the next value in the iteration.

            Raises:
                StopIteration: When the iteration is complete
            """
            if self.current > self.end:
                # No more values, signal end of iteration
                raise StopIteration

            # Get current value, increment for next call, and return
            value = self.current
            self.current += 1
            return value


    # Using our custom iterator
    print("Using Counter iterator:")
    counter = Counter(1, 5)

    for num in counter:
        print(num)

    # Try to iterate again - won't work because iterator is exhausted
    print("\nTrying to iterate again:")
    for num in counter:
        print(num)  # Nothing prints - iterator is exhausted


    # Example 4.2: Creating a reusable iterable with separate iterator
    print("\n--- Example 4.2: Reusable Iterable (Better Design) ---")


    class CounterIterable:
        """
        An iterable that creates fresh iterators each time.

        This is the better design pattern: separate the iterable (which stores
        the configuration) from the iterator (which tracks state). This allows
        multiple iterations without creating a new object each time.
        """

        def __init__(self, start, end):
            """Store the configuration for iteration."""
            self.start = start
            self.end = end

        def __iter__(self):
            """
            Return a NEW iterator each time this is called.

            This allows the iterable to be used multiple times.
            """
            return CounterIterator(self.start, self.end)


    class CounterIterator:
        """
        The actual iterator that maintains state.

        This class is separate from the iterable, allowing multiple
        simultaneous iterations over the same data.
        """

        def __init__(self, start, end):
            self.current = start
            self.end = end

        def __iter__(self):
            """Return self - this is an iterator."""
            return self

        def __next__(self):
            """Return next value or raise StopIteration."""
            if self.current > self.end:
                raise StopIteration
            value = self.current
            self.current += 1
            return value


    # Using the reusable iterable
    print("Using CounterIterable:")
    counter = CounterIterable(1, 3)

    # First iteration
    print("First iteration:")
    for num in counter:
        print(num)

    # Second iteration - works because __iter__() creates a new iterator!
    print("\nSecond iteration:")
    for num in counter:
        print(num)

    # We can even have multiple simultaneous iterations
    print("\nSimultaneous iterations:")
    iter1 = iter(counter)
    iter2 = iter(counter)
    print(f"From iter1: {next(iter1)}")  # 1
    print(f"From iter2: {next(iter2)}")  # 1
    print(f"From iter1: {next(iter1)}")  # 2
    print(f"From iter2: {next(iter2)}")  # 2


    # Example 4.3: Iterator with more complex logic
    print("\n--- Example 4.3: Fibonacci Iterator ---")


    class Fibonacci:
        """
        Iterator that generates Fibonacci numbers up to a maximum value.

        Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, ...
        Each number is the sum of the previous two numbers.
        """

        def __init__(self, max_value):
            """
            Initialize the Fibonacci iterator.

            Args:
                max_value: Stop when the next number would exceed this value
            """
            self.max_value = max_value
            self.a = 0  # First Fibonacci number
            self.b = 1  # Second Fibonacci number

        def __iter__(self):
            """Return self - this is an iterator."""
            return self

        def __next__(self):
            """
            Return the next Fibonacci number.

            The algorithm:
            1. Check if current value exceeds max
            2. Save current value to return
            3. Calculate next two values for next iteration
            4. Return saved value
            """
            if self.a > self.max_value:
                raise StopIteration

            # Save current value
            value = self.a

            # Calculate next two values
            # New a is old b, new b is sum of old a and b
            self.a, self.b = self.b, self.a + self.b

            return value


    # Using the Fibonacci iterator
    print("Fibonacci numbers up to 100:")
    fib = Fibonacci(100)
    for num in fib:
        print(num, end=' ')
    print()


    # Example 4.4: Iterator for custom data structure
    print("\n--- Example 4.4: Custom Data Structure Iterator ---")


    class ReversedList:
        """
        An iterable that iterates over a list in reverse order.

        This demonstrates how to create custom iteration behavior
        for your own data structures.
        """

        def __init__(self, data):
            """
            Initialize with a list of data.

            Args:
                data: List to iterate over in reverse
            """
            self.data = data

        def __iter__(self):
            """Return a new iterator for reversed iteration."""
            return ReversedListIterator(self.data)


    class ReversedListIterator:
        """Iterator that traverses a list in reverse order."""

        def __init__(self, data):
            self.data = data
            # Start from the last index
            self.index = len(data) - 1

        def __iter__(self):
            return self

        def __next__(self):
            """Return items from end to beginning."""
            if self.index < 0:
                raise StopIteration

            value = self.data[self.index]
            self.index -= 1
            return value


    # Using the reversed list iterator
    print("Original list: [1, 2, 3, 4, 5]")
    rev_list = ReversedList([1, 2, 3, 4, 5])

    print("Reversed iteration:")
    for item in rev_list:
        print(item, end=' ')
    print()


    # ============================================================================
    # SECTION 5: PRACTICAL CONSIDERATIONS
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 5: PRACTICAL CONSIDERATIONS")
    print("=" * 70)

    # Example 5.1: When to use iterators
    print("\n--- Example 5.1: Use Cases for Custom Iterators ---")

    """
    Create custom iterators when:
    1. Working with large or infinite sequences (memory efficiency)
    2. Need custom iteration logic over your data structures
    3. Want to provide multiple ways to iterate over data
    4. Processing streaming data or files
    5. Need lazy evaluation (compute on demand)

    Don't create custom iterators when:
    1. A list comprehension is simpler and sufficient
    2. You need random access to elements
    3. You need to iterate multiple times (use iterable instead)
    4. Built-in tools (map, filter, zip) work fine
    """


    # Example 5.2: Memory efficiency demonstration
    print("\n--- Example 5.2: Memory Efficiency ---")


    class LargeRangeIterator:
        """
        Memory-efficient iterator for large ranges.

        Instead of storing all numbers in memory (like range() returns in Python 2),
        we generate them on-the-fly. This uses constant memory regardless of range size.
        """

        def __init__(self, start, end, step=1):
            self.current = start
            self.end = end
            self.step = step

        def __iter__(self):
            return self

        def __next__(self):
            if (self.step > 0 and self.current >= self.end) or \
               (self.step < 0 and self.current <= self.end):
                raise StopIteration
            value = self.current
            self.current += self.step
            return value


    # This uses very little memory even for huge ranges
    print("Creating iterator for range(0, 1000000):")
    large_range = LargeRangeIterator(0, 1000000)
    print(f"First 5 numbers: ", end='')
    for i, num in enumerate(large_range):
        if i >= 5:
            break
        print(num, end=' ')
    print()


    # Example 5.3: Practical file iterator example
    print("\n--- Example 5.3: File Line Iterator ---")


    class FileLineIterator:
        """
        Iterator for reading file lines with custom processing.

        This demonstrates a practical use case: processing large files
        line-by-line without loading the entire file into memory.
        """

        def __init__(self, filename, skip_empty=True):
            """
            Initialize file iterator.

            Args:
                filename: Path to file to read
                skip_empty: Whether to skip empty lines
            """
            self.filename = filename
            self.skip_empty = skip_empty
            self.file = None

        def __iter__(self):
            """Open file and return self."""
            self.file = open(self.filename, 'r')
            return self

        def __next__(self):
            """Return next non-empty line."""
            while True:
                line = self.file.readline()

                if not line:
                    # End of file reached
                    self.file.close()
                    raise StopIteration

                line = line.strip()

                # Skip empty lines if requested
                if self.skip_empty and not line:
                    continue

                return line


    # Note: We won't actually run this example as it requires a file
    print("Example file iterator created (see code for implementation)")


    # ============================================================================
    # SUMMARY AND KEY TAKEAWAYS
    # ============================================================================

    print("\n" + "=" * 70)
    print("SUMMARY: ITERABLES vs ITERATORS")
    print("=" * 70)

    print("""
    KEY CONCEPTS:

    1. ITERABLE:
       - Has __iter__() method that returns an iterator
       - Can be iterated over multiple times
       - Examples: list, tuple, string, dict, set
       - Can create new iterators each time

    2. ITERATOR:
       - Has both __iter__() (returns self) and __next__() methods
       - Maintains state during iteration
       - One-time use only (exhausted after iteration)
       - Raises StopIteration when done
       - Memory efficient (computes values on demand)

    3. ITERATION PROTOCOL:
       - for loop calls iter() to get iterator
       - Then repeatedly calls next() until StopIteration
       - This is how all Python loops work internally

    4. CUSTOM ITERATORS:
       - Implement __iter__() and __next__()
       - Use separate iterable/iterator classes for reusability
       - Great for large sequences, custom logic, lazy evaluation

    5. BEST PRACTICES:
       - Separate iterable (config) from iterator (state)
       - Always raise StopIteration when done
       - Use iterators for memory efficiency
       - Consider generators for simpler syntax (next lesson!)

    REMEMBER:
    - All iterators are iterables (but not vice versa)
    - Iterators remember their position
    - Iterables can be iterated multiple times
    - Iterators are exhausted after one use
    """)

    print("\n" + "=" * 70)
    print("END OF BEGINNER TUTORIAL")
    print("Next: Learn about GENERATORS for easier iterator creation!")
    print("=" * 70)
```

---

## Exercises


**Exercise 1.**
Write a class `Countdown` that implements the iterator protocol (`__iter__` and `__next__`). It should count down from a given number to 1.

??? success "Solution to Exercise 1"

        ```python
        class Countdown:
            def __init__(self, start):
                self.current = start

            def __iter__(self):
                return self

            def __next__(self):
                if self.current < 1:
                    raise StopIteration
                value = self.current
                self.current -= 1
                return value

        for n in Countdown(5):
            print(n, end=" ")
        # 5 4 3 2 1
        ```

    `__iter__` returns the iterator (itself), and `__next__` returns the next value or raises `StopIteration`.

---

**Exercise 2.**
Show that a list is iterable but not an iterator. Demonstrate by calling `iter()` on it to get an iterator, then calling `next()` on the iterator.

??? success "Solution to Exercise 2"

        ```python
        lst = [1, 2, 3]

        # List is iterable but not an iterator
        print(hasattr(lst, "__iter__"))    # True
        print(hasattr(lst, "__next__"))    # False

        # Get an iterator from the list
        it = iter(lst)
        print(hasattr(it, "__next__"))     # True
        print(next(it))  # 1
        print(next(it))  # 2
        print(next(it))  # 3
        ```

    An iterable has `__iter__`. An iterator has both `__iter__` and `__next__`. `iter()` converts an iterable to an iterator.

---

**Exercise 3.**
Write a function `is_iterable(obj)` that returns `True` if `obj` is iterable and `False` otherwise. Test it with a list, an integer, a string, and a generator.

??? success "Solution to Exercise 3"

        ```python
        def is_iterable(obj):
            try:
                iter(obj)
                return True
            except TypeError:
                return False

        print(is_iterable([1, 2]))       # True
        print(is_iterable(42))           # False
        print(is_iterable("hello"))      # True
        print(is_iterable(x for x in []))  # True
        ```

    Using `try`/`except` with `iter()` is the most reliable way to check iterability, following the EAFP (Easier to Ask Forgiveness than Permission) principle.
