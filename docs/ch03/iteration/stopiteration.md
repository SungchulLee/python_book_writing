# StopIteration Mechanics

StopIteration is the protocol-level signal that an iterator has no more values. Understanding StopIteration is fundamental to Python's iteration protocol and generator behavior.

!!! tip "Mental Model"
    `StopIteration` is not an error -- it is the "end of tape" signal. When `__next__()` raises it, the `for` loop knows to stop gracefully. In generators, falling off the end of the function or executing a bare `return` automatically raises `StopIteration`. You almost never catch it yourself; the `for` loop does that for you.

---

## Iterator Protocol

### Raising StopIteration

```python
class CountUp:
    def __init__(self, max):
        self.max = max
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current < self.max:
            self.current += 1
            return self.current
        else:
            raise StopIteration

counter = CountUp(3)
for value in counter:
    print(value)
```

Output:
```
1
2
3
```

### Manual Iteration

```python
numbers = iter([1, 2, 3])

try:
    print(next(numbers))
    print(next(numbers))
    print(next(numbers))
    print(next(numbers))  # Raises StopIteration
except StopIteration:
    print("Iterator exhausted")
```

Output:
```
1
2
3
Iterator exhausted
```

## Generators and StopIteration

### Implicit StopIteration

```python
def count_up(max):
    current = 0
    while current < max:
        current += 1
        yield current

gen = count_up(3)
try:
    while True:
        print(next(gen))
except StopIteration:
    print("Generator finished")
```

Output:
```
1
2
3
Generator finished
```

## Return Values in StopIteration

### PEP 380 Return Mechanism

```python
def search(items, target):
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1

result = search([1, 2, 3, 4], 3)
print(f"Found at index: {result}")
```

Output:
```
Found at index: 2
```

## Best Practices

### Catching StopIteration Safely

```python
def safe_next(iterator, default=None):
    try:
        return next(iterator)
    except StopIteration:
        return default

gen = (x for x in [1, 2, 3])
next(gen)
next(gen)
next(gen)
result = safe_next(gen, "exhausted")
print(result)
```

Output:
```
exhausted
```

---

## Runnable Example: `iterator_protocol_sentence.py`

```python
"""
Iterator Protocol Implementation - Building a Sentence Class with __iter__
This tutorial demonstrates how to implement the iterator protocol by
creating a Sentence class that can be iterated over like a native Python object.
Run this file to see the iterator protocol in action!
"""

import re
import reprlib

if __name__ == "__main__":

    print("=" * 70)
    print("ITERATOR PROTOCOL - IMPLEMENTING __iter__")
    print("=" * 70)

    # ============================================================================
    # EXAMPLE 1: Understanding Iterables and Iterators
    # ============================================================================
    print("\n1. UNDERSTANDING ITERABLES AND ITERATORS")
    print("-" * 70)

    print("\nIn Python, there's an important distinction:")
    print("- ITERABLE: Object that implements __iter__() method")
    print("  Returns an iterator")
    print("  Examples: lists, tuples, strings, dicts")
    print("")
    print("- ITERATOR: Object that implements both:")
    print("  __iter__() - returns itself")
    print("  __next__() - returns the next value and raises StopIteration when done")
    print("")
    print("When you write 'for x in iterable:', Python:")
    print("  1. Calls iterable.__iter__() to get an iterator")
    print("  2. Repeatedly calls iterator.__next__() until StopIteration")

    # ============================================================================
    # EXAMPLE 2: The Sentence Class - A Custom Iterable
    # ============================================================================
    print("\n2. THE SENTENCE CLASS - MAKING TEXT ITERABLE")
    print("-" * 70)

    # Regular expression to find words (letters and digits)
    RE_WORD = re.compile(r'\w+')

    class Sentence:
        """
        A sequence of words extracted from a string.

        This class implements the iterable protocol, allowing you to:
        - Access words by index: sentence[0], sentence[1]
        - Get the number of words: len(sentence)
        - Iterate over words: for word in sentence
        """

        def __init__(self, text):
            """
            Initialize with a text string.

            We extract all words (sequences of alphanumeric chars) from the text.
            """
            self.text = text
            # Use regex to find all words - this does the hard work
            self.words = RE_WORD.findall(text)

        def __getitem__(self, index):
            """
            Allow indexing: sentence[0], sentence[1], etc.

            This makes Sentence a sequence-like object.
            Python uses this for iteration as a fallback if __iter__ isn't defined.
            """
            return self.words[index]

        def __len__(self):
            """Allow len() function: len(sentence)"""
            return len(self.words)

        def __repr__(self):
            """
            Nice string representation that abbreviates long text.

            reprlib.repr() shows a summary of the text.
            """
            return 'Sentence(%s)' % reprlib.repr(self.text)

    print("\nDefined the Sentence class with:")
    print("- __init__(text): Initializes and extracts words using regex")
    print("- __getitem__(index): Allows indexing like a list")
    print("- __len__(): Returns the number of words")
    print("- __repr__(): Nice representation")

    # ============================================================================
    # EXAMPLE 3: Using Sentence - Indexing and Length
    # ============================================================================
    print("\n3. USING SENTENCE - INDEXING AND LENGTH")
    print("-" * 70)

    text = 'To be, or not to be, that is the question'
    s = Sentence(text)

    print(f"\nCreated: s = Sentence('{text}')\n")

    print(f"s[0] = {s[0]!r} (first word)")
    print(f"s[1] = {s[1]!r} (second word)")
    print(f"s[5] = {s[5]!r} (sixth word)")
    print(f"\nlen(s) = {len(s)} (total words)")

    print(f"\nrepr(s) = {repr(s)}")

    print("\nWHY THIS WORKS:")
    print("- __getitem__ allows indexing notation [index]")
    print("- __len__ makes len() work on our custom object")
    print("- __repr__ shows a nice representation in the interpreter")

    # ============================================================================
    # EXAMPLE 4: Adding __iter__ - Making Sentence Iterable in for loops
    # ============================================================================
    print("\n4. IMPLEMENTING __iter__ - FOR LOOP SUPPORT")
    print("-" * 70)

    print("\nThe current Sentence class supports indexing, but what about for loops?")
    print("Python has a fallback: if __iter__ isn't defined, it tries __getitem__")
    print("But it's better to explicitly implement __iter__ for clarity!\n")

    print("Here's what we need to add:\n")

    code_example = '''
    def __iter__(self):
        """
        Make Sentence iterable.

        This method should return an iterator object.
        We could return a custom iterator, or use a generator.
        For this example, we'll use a helper iterator class.
        """
        return SentenceIterator(self.words)
    '''

    print(code_example)

    # ============================================================================
    # EXAMPLE 5: Creating a Custom Iterator Class
    # ============================================================================
    print("\n5. CUSTOM ITERATOR CLASS")
    print("-" * 70)

    class SentenceIterator:
        """
        An iterator for the Sentence class.

        This class implements the iterator protocol:
        - __iter__() returns itself
        - __next__() returns the next word or raises StopIteration
        """

        def __init__(self, words):
            """Store the words and initialize index to 0."""
            self.words = words
            self.index = 0

        def __iter__(self):
            """An iterator returns itself."""
            return self

        def __next__(self):
            """
            Return the next word, or raise StopIteration when done.

            This is the key method that makes iteration work!
            """
            try:
                word = self.words[self.index]
            except IndexError:
                # No more words, signal the end of iteration
                raise StopIteration
            self.index += 1
            return word

    print("Defined SentenceIterator class:")
    print("- __init__(words): Stores words and sets starting index to 0")
    print("- __iter__(): Returns itself (required by iterator protocol)")
    print("- __next__(): Returns next word or raises StopIteration")

    # ============================================================================
    # EXAMPLE 6: Adding __iter__ to Sentence
    # ============================================================================
    print("\n6. ADDING __iter__ TO SENTENCE")
    print("-" * 70)

    # Extend the Sentence class with __iter__
    class Sentence:
        """
        A sequence of words extracted from a string.
        Now with full iterator support!
        """

        def __init__(self, text):
            self.text = text
            self.words = RE_WORD.findall(text)

        def __getitem__(self, index):
            return self.words[index]

        def __len__(self):
            return len(self.words)

        def __repr__(self):
            return 'Sentence(%s)' % reprlib.repr(self.text)

        def __iter__(self):
            """
            Return an iterator for this sentence.

            This is the crucial method that makes 'for word in sentence' work!
            """
            return SentenceIterator(self.words)

    print("\nAdded __iter__ method to Sentence:")
    print("Now Sentence objects work with for loops!")

    # ============================================================================
    # EXAMPLE 7: Using the Iterable Sentence
    # ============================================================================
    print("\n7. USING SENTENCE WITH FOR LOOPS")
    print("-" * 70)

    s = Sentence(text)

    print(f"\nCreated: s = Sentence('{text}')\n")

    print("Iterating with for loop:")
    print("-" * 40)

    for i, word in enumerate(s, 1):
        print(f"  Word {i}: {word}")

    print("\nWHY THIS WORKS:")
    print("- for loop calls s.__iter__() to get an iterator")
    print("- Each iteration calls iterator.__next__() to get next word")
    print("- When StopIteration is raised, the loop ends")
    print("- No explicit iterator management needed!")

    # ============================================================================
    # EXAMPLE 8: Practical Example - Sentence Analysis
    # ============================================================================
    print("\n8. PRACTICAL EXAMPLE - SENTENCE ANALYSIS")
    print("-" * 70)

    def analyze_sentence(text):
        """Analyze a sentence and print various statistics."""
        s = Sentence(text)

        print(f"\nText: {text}")
        print(f"Number of words: {len(s)}")
        print(f"\nWords:")
        for i, word in enumerate(s, 1):
            print(f"  {i:2}. {word}")

        print(f"\nWord lengths:")
        for word in s:
            print(f"  '{word}' -> {len(word)} characters")

    test_texts = [
        "Hello world",
        "Python is awesome",
        "The quick brown fox jumps over the lazy dog"
    ]

    for test_text in test_texts:
        analyze_sentence(test_text)
        print()

    # ============================================================================
    # SUMMARY: The Iterator Protocol
    # ============================================================================
    print("\n" + "=" * 70)
    print("SUMMARY - THE ITERATOR PROTOCOL")
    print("=" * 70)

    print("""
    To make an object iterable (usable in for loops):

    1. Implement __iter__():
       - Should return an iterator object
       - This method is called at the start of a for loop

    2. Create an iterator class that implements:
       - __iter__(): Returns itself
       - __next__(): Returns next value or raises StopIteration

    EXAMPLE FLOW for 'for word in sentence':
       1. Python calls sentence.__iter__() -> gets iterator
       2. Python calls iterator.__next__() -> gets first word
       3. Process word in loop body
       4. Back to step 2, repeat until StopIteration
       5. Loop exits

    KEY BENEFITS:
    - Make custom objects work with Python's for loops
    - Compatible with other iteration tools (list comprehensions, etc.)
    - Elegant, Pythonic interface
    - Lazy evaluation (iterator can be memory efficient)

    REMEMBER:
    - Iterable: Has __iter__() method
    - Iterator: Has __iter__() and __next__() methods
    - You often need both for full iterator support!
    """)
```


---

## Runnable Example: `iterator_protocol_prime_fib.py`

```python
"""
Iterator Protocol: Prime Number and Fibonacci Iterators

Custom iterators implementing __iter__() and __next__() for
generating mathematical sequences on demand.

Topics covered:
- Iterator protocol (__iter__ / __next__)
- StopIteration for signaling end of iteration
- Lazy evaluation (values computed one at a time)
- itertools for combinatorial generation

Based on concepts from Python-100-Days example15 and ch02/iteration materials.
"""

import itertools
from math import sqrt


# =============================================================================
# Example 1: Prime Number Iterator
# =============================================================================

def is_prime(num: int) -> bool:
    """Check if a number is prime.

    >>> is_prime(7)
    True
    >>> is_prime(10)
    False
    """
    if num < 2:
        return False
    for factor in range(2, int(sqrt(num)) + 1):
        if num % factor == 0:
            return False
    return True


class PrimeIterator:
    """Iterator that yields prime numbers in a given range.

    Implements the iterator protocol:
    - __iter__() returns self (the iterator object)
    - __next__() returns the next prime or raises StopIteration

    >>> primes = list(PrimeIterator(2, 20))
    >>> primes
    [2, 3, 5, 7, 11, 13, 17, 19]
    """

    def __init__(self, start: int, end: int):
        if start < 2:
            start = 2
        self._current = start - 1  # Will be incremented before first check
        self._end = end

    def __iter__(self):
        return self

    def __next__(self) -> int:
        self._current += 1
        while self._current <= self._end:
            if is_prime(self._current):
                return self._current
            self._current += 1
        raise StopIteration()


# =============================================================================
# Example 2: Fibonacci Iterator
# =============================================================================

class FibonacciIterator:
    """Iterator that yields Fibonacci numbers.

    Fibonacci sequence: 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
    Each number is the sum of the two preceding ones.

    >>> list(FibonacciIterator(8))
    [1, 1, 2, 3, 5, 8, 13, 21]
    """

    def __init__(self, count: int):
        self._count = count
        self._a = 0
        self._b = 1
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self._index >= self._count:
            raise StopIteration()
        self._a, self._b = self._b, self._a + self._b
        self._index += 1
        return self._a


# =============================================================================
# Example 3: Using Iterators in for Loops
# =============================================================================

def demo_iterator_usage():
    """Show how custom iterators work with Python's iteration machinery."""
    print("=== Prime Iterator (primes from 2 to 50) ===")
    for prime in PrimeIterator(2, 50):
        print(prime, end=' ')
    print('\n')

    print("=== Fibonacci Iterator (first 15 numbers) ===")
    for fib in FibonacciIterator(15):
        print(fib, end=' ')
    print('\n')

    # Manual iteration with next()
    print("=== Manual next() calls ===")
    fib_iter = FibonacciIterator(5)
    print(f"next() -> {next(fib_iter)}")  # 1
    print(f"next() -> {next(fib_iter)}")  # 1
    print(f"next() -> {next(fib_iter)}")  # 2
    # Remaining values consumed by for loop
    print("for loop consumes rest:", list(fib_iter))
    print()


# =============================================================================
# Example 4: Iterator vs Generator Comparison
# =============================================================================

def fib_generator(count: int):
    """Generator function equivalent of FibonacciIterator.

    Generators are more concise than iterator classes but
    classes offer more control (reset, state inspection, etc.).
    """
    a, b = 0, 1
    for _ in range(count):
        a, b = b, a + b
        yield a


def demo_iterator_vs_generator():
    """Compare iterator class vs generator function."""
    print("=== Iterator Class vs Generator Function ===")

    # Both produce the same sequence
    from_class = list(FibonacciIterator(10))
    from_generator = list(fib_generator(10))

    print(f"Iterator class: {from_class}")
    print(f"Generator func: {from_generator}")
    print(f"Same result:    {from_class == from_generator}")
    print()


# =============================================================================
# Example 5: itertools with Custom Iterators
# =============================================================================

def demo_itertools():
    """Demonstrate itertools functions with our iterators."""
    print("=== itertools with Custom Iterators ===")

    # Take first 5 primes using islice
    first_5_primes = list(itertools.islice(PrimeIterator(2, 1000), 5))
    print(f"First 5 primes: {first_5_primes}")

    # Chain two iterators
    small_primes = PrimeIterator(2, 10)
    small_fibs = FibonacciIterator(5)
    combined = list(itertools.chain(small_primes, small_fibs))
    print(f"Primes(2-10) + Fib(5): {combined}")

    # Permutations and combinations
    print(f"Permutations of ABC: {list(itertools.permutations('ABC'))}")
    print(f"Combinations C(4,2): {list(itertools.combinations('ABCD', 2))}")
    print(f"Product of AB x 12:  {list(itertools.product('AB', '12'))}")
    print()


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    demo_iterator_usage()
    demo_iterator_vs_generator()
    demo_itertools()
```

---

## Exercises


**Exercise 1.**
Write an iterator class `RepeatN` that yields a given value exactly `n` times, then raises `StopIteration`.

??? success "Solution to Exercise 1"

        ```python
        class RepeatN:
            def __init__(self, value, n):
                self.value = value
                self.n = n
                self.count = 0

            def __iter__(self):
                return self

            def __next__(self):
                if self.count >= self.n:
                    raise StopIteration
                self.count += 1
                return self.value

        print(list(RepeatN("hello", 3)))  # ['hello', 'hello', 'hello']
        ```

    `StopIteration` signals that the iterator has no more values. The `for` loop and `list()` catch it automatically.

---

**Exercise 2.**
Show what happens when you call `next()` on an exhausted iterator. Demonstrate using both an explicit `next()` call and a `for` loop (which handles `StopIteration` automatically).

??? success "Solution to Exercise 2"

        ```python
        it = iter([1, 2])

        print(next(it))  # 1
        print(next(it))  # 2

        try:
            next(it)  # StopIteration
        except StopIteration:
            print("Iterator exhausted")

        # for loop handles it silently
        for val in iter([1, 2]):
            print(val)
        # 1
        # 2
        # (no error)
        ```

    `next()` raises `StopIteration` on an exhausted iterator. `for` loops catch it internally as the signal to stop.

---

**Exercise 3.**
Write a function `take(n, iterable)` that returns a list of the first `n` elements from an iterable. Handle the case where the iterable has fewer than `n` elements.

??? success "Solution to Exercise 3"

        ```python
        def take(n, iterable):
            result = []
            for i, item in enumerate(iterable):
                if i >= n:
                    break
                result.append(item)
            return result

        print(take(3, range(10)))      # [0, 1, 2]
        print(take(5, [1, 2]))         # [1, 2] (fewer than 5)
        print(take(3, (x*x for x in range(100))))  # [0, 1, 4]
        ```

    The function stops at `n` elements or when the iterable is exhausted, whichever comes first.
