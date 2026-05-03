# Iterator Chaining

Iterator chaining combines multiple iterators or transformation functions into a pipeline. The itertools module provides powerful tools for creating complex iteration patterns with minimal memory overhead.

!!! tip "Mental Model"
    Think of chained iterators as an assembly line: each stage takes one item at a time from the previous stage, transforms it, and passes it along. No stage needs to see the full dataset at once. This pipeline approach composes naturally -- you build complex transformations by snapping simple stages together.

---

## Basic Chaining

### Composing Generators

```python
def add_one(iterable):
    for value in iterable:
        yield value + 1

def double(iterable):
    for value in iterable:
        yield value * 2

numbers = range(1, 4)
result = double(add_one(numbers))
print(list(result))
```

Output:
```
[4, 6, 8]
```

### Iterator Chaining Order

```python
numbers = [1, 2, 3]

# Different order, different result
result1 = double(add_one(numbers))
result2 = add_one(double(numbers))

print(f"Add then double: {list(result1)}")
print(f"Double then add: {list(result2)}")
```

Output:
```
Add then double: [4, 6, 8]
Double then add: [3, 5, 7]
```

## itertools Chains

### Chaining Iterables

```python
from itertools import chain

list1 = [1, 2, 3]
list2 = [4, 5, 6]
list3 = [7, 8, 9]

combined = chain(list1, list2, list3)
print(list(combined))
```

Output:
```
[1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Chain from Iterable

```python
from itertools import chain

nested = [[1, 2], [3, 4], [5, 6]]
flattened = chain.from_iterable(nested)
print(list(flattened))
```

Output:
```
[1, 2, 3, 4, 5, 6]
```

## Complex Pipelines

### Multi-Step Processing

```python
from itertools import filter, map

numbers = range(1, 11)
result = filter(lambda x: x % 2 == 0, map(lambda x: x ** 2, numbers))
print(list(result))
```

Output:
```
[4, 16, 36, 64, 100]
```

### Real-World Example

```python
import itertools

def read_lines():
    data = ["hello world", "foo bar", "test data"]
    for line in data:
        yield line

def split_words(lines):
    for line in lines:
        yield from line.split()

def uppercase(words):
    for word in words:
        yield word.upper()

pipeline = uppercase(split_words(read_lines()))
print(list(pipeline))
```

Output:
```
['HELLO', 'WORLD', 'FOO', 'BAR', 'TEST', 'DATA']
```

---

## Runnable Example: `practical_applications.py`

```python
"""
PYTHON GENERATORS & ITERATORS - PRACTICAL APPLICATIONS
======================================================

Topic: Real-World Generator Applications
----------------------------------------

This module covers:
1. File processing and streaming data
2. Working with large datasets
3. Memory-efficient data pipelines
4. Custom iteration protocols
5. Integration with standard library
6. Performance optimization techniques

Learning Objectives:
- Apply generators to real-world problems
- Build efficient data processing pipelines
- Handle large files and datasets
- Integrate generators with Python stdlib
- Optimize memory usage and performance
- Implement custom iteration patterns

Prerequisites:
- Completion of beginner, intermediate, and advanced levels
- Strong understanding of all generator concepts
- Familiarity with Python standard library
- Understanding of file I/O and data processing
"""

import os
import csv
import json
import itertools
import functools
from collections import deque
import time
import sys

# ============================================================================
# SECTION 1: FILE PROCESSING
# ============================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SECTION 1: FILE PROCESSING")
    print("=" * 70)

    """
    Generators are ideal for file processing:
    - Process files larger than available memory
    - Stream data without loading entire file
    - Memory efficient line-by-line processing
    - Easy to chain processing operations
    """

    # Example 1.1: Reading large files
    print("\n--- Example 1.1: Memory-Efficient File Reading ---")


    def read_large_file(filepath, chunk_size=8192):
        """
        Read a large file in chunks.

        Args:
            filepath: Path to file
            chunk_size: Size of each chunk in bytes

        Yields:
            Chunks of file content
        """
        with open(filepath, 'r') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                yield chunk


    def read_lines(filepath):
        """
        Read file line by line.

        More memory efficient than readlines() for large files.
        """
        with open(filepath, 'r') as file:
            for line in file:
                yield line.strip()


    def read_lines_filtered(filepath, filter_func):
        """
        Read file with filtering.

        Args:
            filepath: Path to file
            filter_func: Function to filter lines (returns bool)

        Yields:
            Filtered lines
        """
        for line in read_lines(filepath):
            if filter_func(line):
                yield line


    print("File reading generators defined (see code)")


    # Example 1.2: Processing CSV files
    print("\n--- Example 1.2: CSV Processing ---")


    def csv_reader(filepath, skip_header=True):
        """
        Generator for reading CSV files row by row.

        Memory efficient for large CSV files.
        """
        with open(filepath, 'r') as file:
            reader = csv.reader(file)

            if skip_header:
                next(reader, None)

            for row in reader:
                yield row


    def csv_dict_reader(filepath):
        """
        Read CSV as dictionaries with column names as keys.
        """
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield dict(row)


    def filtered_csv(filepath, column_index, filter_value):
        """
        Filter CSV rows based on column value.

        Demonstrates combining file reading with filtering.
        """
        for row in csv_reader(filepath):
            if len(row) > column_index and row[column_index] == filter_value:
                yield row


    print("CSV processing generators defined")


    # Example 1.3: JSON streaming
    print("\n--- Example 1.3: JSON Line Processing ---")


    def json_lines_reader(filepath):
        """
        Read JSONL (JSON Lines) file.

        Each line is a separate JSON object.
        Memory efficient for large JSON datasets.
        """
        with open(filepath, 'r') as file:
            for line in file:
                try:
                    yield json.loads(line.strip())
                except json.JSONDecodeError:
                    continue


    def json_array_items(filepath):
        """
        Stream items from a JSON array file.

        Note: This simplified version loads the whole file.
        For true streaming of large JSON arrays, use ijson library.
        """
        with open(filepath, 'r') as file:
            data = json.load(file)
            if isinstance(data, list):
                for item in data:
                    yield item


    print("JSON streaming generators defined")


    # ============================================================================
    # SECTION 2: DATA PIPELINES
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 2: DATA PROCESSING PIPELINES")
    print("=" * 70)

    """
    Build complex data processing pipelines using generator composition.
    Each stage processes data and passes to the next stage.
    """

    # Example 2.1: ETL Pipeline (Extract, Transform, Load)
    print("\n--- Example 2.1: ETL Pipeline ---")


    def extract_data(source):
        """
        Extract stage: Read data from source.
        """
        for item in source:
            yield item


    def transform_data(data_stream, transform_func):
        """
        Transform stage: Apply transformation to each item.
        """
        for item in data_stream:
            try:
                yield transform_func(item)
            except Exception as e:
                # Skip items that fail transformation
                continue


    def filter_data(data_stream, filter_func):
        """
        Filter stage: Keep only items matching condition.
        """
        for item in data_stream:
            if filter_func(item):
                yield item


    def load_data(data_stream, batch_size=100):
        """
        Load stage: Batch data for efficient loading.
        """
        batch = []
        for item in data_stream:
            batch.append(item)
            if len(batch) >= batch_size:
                yield batch
                batch = []

        if batch:
            yield batch


    # Example usage
    print("ETL Pipeline example:")

    # Simulate data source
    source_data = range(1, 21)

    # Build pipeline
    extracted = extract_data(source_data)
    transformed = transform_data(extracted, lambda x: x * 2)
    filtered = filter_data(transformed, lambda x: x > 10)
    loaded = load_data(filtered, batch_size=5)

    # Process data
    for batch_num, batch in enumerate(loaded, 1):
        print(f"Batch {batch_num}: {batch}")


    # Example 2.2: Chained transformations
    print("\n--- Example 2.2: Chained Transformations ---")


    def map_values(data_stream, func):
        """Apply function to each item."""
        for item in data_stream:
            yield func(item)


    def filter_values(data_stream, predicate):
        """Keep items matching predicate."""
        for item in data_stream:
            if predicate(item):
                yield item


    def take_n(data_stream, n):
        """Take first n items."""
        for i, item in enumerate(data_stream):
            if i >= n:
                break
            yield item


    def skip_n(data_stream, n):
        """Skip first n items."""
        for i, item in enumerate(data_stream):
            if i >= n:
                yield item


    # Chain multiple operations
    print("Chained operations:")
    data = range(1, 51)
    result = take_n(
        map_values(
            filter_values(data, lambda x: x % 2 == 0),
            lambda x: x ** 2
        ),
        5
    )
    print(f"Result: {list(result)}")


    # Example 2.3: Parallel pipelines
    print("\n--- Example 2.3: Parallel Processing Streams ---")


    def split_stream(data_stream, condition):
        """
        Split data stream into two based on condition.

        Returns:
            Two generators: (true_stream, false_stream)
        """
        true_items = []
        false_items = []

        for item in data_stream:
            if condition(item):
                true_items.append(item)
            else:
                false_items.append(item)

        return iter(true_items), iter(false_items)


    def merge_streams(*streams):
        """
        Merge multiple streams into one.
        """
        for stream in streams:
            for item in stream:
                yield item


    print("Stream splitting and merging example:")
    data = range(1, 11)
    evens, odds = split_stream(data, lambda x: x % 2 == 0)

    print(f"Evens: {list(evens)}")
    print(f"Odds: {list(odds)}")


    # ============================================================================
    # SECTION 3: WORKING WITH LARGE DATASETS
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 3: LARGE DATASET HANDLING")
    print("=" * 70)

    """
    Techniques for efficiently processing datasets that don't fit in memory.
    """

    # Example 3.1: Sliding window analysis
    print("\n--- Example 3.1: Sliding Window ---")


    def sliding_window(iterable, window_size):
        """
        Create sliding window view of data.

        Useful for time-series analysis, moving averages.
        """
        iterator = iter(iterable)
        window = deque(maxlen=window_size)

        # Fill initial window
        for _ in range(window_size):
            try:
                window.append(next(iterator))
            except StopIteration:
                return

        yield tuple(window)

        # Slide the window
        for item in iterator:
            window.append(item)
            yield tuple(window)


    def moving_average(data_stream, window_size):
        """
        Calculate moving average.

        Memory efficient - only keeps window_size items in memory.
        """
        for window in sliding_window(data_stream, window_size):
            yield sum(window) / len(window)


    # Example usage
    print("Moving average example:")
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"Data: {data}")
    print(f"3-period moving average: {list(moving_average(data, 3))}")


    # Example 3.2: Chunking large datasets
    print("\n--- Example 3.2: Processing in Chunks ---")


    def chunk_data(iterable, chunk_size):
        """
        Split data into chunks of specified size.

        Useful for batch processing, API calls with rate limits.
        """
        chunk = []
        for item in iterable:
            chunk.append(item)
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []

        if chunk:
            yield chunk


    def process_chunks(data_source, chunk_size, process_func):
        """
        Process data in chunks.

        Args:
            data_source: Iterable data source
            chunk_size: Size of each chunk
            process_func: Function to apply to each chunk
        """
        for chunk in chunk_data(data_source, chunk_size):
            yield process_func(chunk)


    # Example usage
    print("Chunk processing example:")
    data = range(1, 26)
    chunks = chunk_data(data, 5)
    print("Chunks of 5:")
    for chunk_num, chunk in enumerate(chunks, 1):
        print(f"  Chunk {chunk_num}: {chunk}")


    # Example 3.3: Sampling large datasets
    print("\n--- Example 3.3: Data Sampling ---")


    def reservoir_sample(data_stream, k):
        """
        Reservoir sampling: Get k random samples from stream.

        Useful when:
        - Don't know total size in advance
        - Stream is too large to fit in memory
        - Need uniform random sampling

        Algorithm guarantees each item has equal probability of selection.
        """
        import random

        reservoir = []

        for i, item in enumerate(data_stream):
            if i < k:
                reservoir.append(item)
            else:
                # Random replacement
                j = random.randint(0, i)
                if j < k:
                    reservoir[j] = item

        return reservoir


    def every_nth(data_stream, n):
        """
        Sample every nth item from stream.

        Simple deterministic sampling.
        """
        for i, item in enumerate(data_stream):
            if i % n == 0:
                yield item


    print("Sampling examples:")
    data = range(1, 101)

    print(f"Every 10th item: {list(every_nth(data, 10))}")

    # Reservoir sampling
    import random
    random.seed(42)
    sample = reservoir_sample(range(1, 101), 5)
    print(f"5 random samples: {sample}")


    # ============================================================================
    # SECTION 4: INTEGRATION WITH STANDARD LIBRARY
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 4: ITERTOOLS INTEGRATION")
    print("=" * 70)

    """
    Combine generators with itertools for powerful data processing.
    """

    # Example 4.1: Common itertools patterns
    print("\n--- Example 4.1: Itertools Patterns ---")


    def demonstrate_itertools():
        """
        Show common itertools usage with generators.
        """
        data = range(1, 11)

        # islice - take a slice without creating list
        print("First 5 items:")
        print(list(itertools.islice(data, 5)))

        # chain - concatenate iterables
        gen1 = (x for x in range(1, 4))
        gen2 = (x for x in range(4, 7))
        print("\nChained generators:")
        print(list(itertools.chain(gen1, gen2)))

        # groupby - group consecutive items
        data = [1, 1, 2, 2, 2, 3, 3, 1, 1]
        print("\nGrouped by value:")
        for key, group in itertools.groupby(data):
            print(f"  {key}: {list(group)}")

        # cycle - repeat indefinitely
        print("\nFirst 10 from cycled [1, 2, 3]:")
        cycled = itertools.cycle([1, 2, 3])
        print(list(itertools.islice(cycled, 10)))

        # accumulate - running totals
        print("\nAccumulated sum of [1, 2, 3, 4, 5]:")
        print(list(itertools.accumulate([1, 2, 3, 4, 5])))


    demonstrate_itertools()


    # Example 4.2: Combining multiple iterables
    print("\n--- Example 4.2: Combining Iterables ---")


    def demonstrate_combinations():
        """Show various ways to combine iterables."""

        # zip_longest - zip with padding
        a = [1, 2, 3]
        b = ['a', 'b']
        print("zip_longest with padding:")
        result = itertools.zip_longest(a, b, fillvalue='X')
        print(list(result))

        # product - cartesian product
        print("\nCartesian product of [1,2] and ['a','b']:")
        result = itertools.product([1, 2], ['a', 'b'])
        print(list(result))

        # combinations and permutations
        print("\nCombinations of [1,2,3] taken 2 at a time:")
        print(list(itertools.combinations([1, 2, 3], 2)))

        print("\nPermutations of [1,2,3] taken 2 at a time:")
        print(list(itertools.permutations([1, 2, 3], 2)))


    demonstrate_combinations()


    # Example 4.3: Custom generator with itertools
    print("\n--- Example 4.3: Advanced Pipeline ---")


    def unique_items(data_stream):
        """
        Yield unique items from stream (maintains order).

        Memory efficient for streams with many duplicates.
        """
        seen = set()
        for item in data_stream:
            if item not in seen:
                seen.add(item)
                yield item


    def pairwise(iterable):
        """
        Generate pairs of consecutive items.

        s -> (s0,s1), (s1,s2), (s2, s3), ...
        """
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)


    # Example usage
    print("Unique items from [1, 2, 2, 3, 1, 4, 3, 5]:")
    data = [1, 2, 2, 3, 1, 4, 3, 5]
    print(list(unique_items(data)))

    print("\nPairs from [1, 2, 3, 4, 5]:")
    print(list(pairwise([1, 2, 3, 4, 5])))


    # ============================================================================
    # SECTION 5: PERFORMANCE OPTIMIZATION
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 5: PERFORMANCE OPTIMIZATION")
    print("=" * 70)

    """
    Techniques for optimizing generator performance.
    """

    # Example 5.1: Generator vs list performance
    print("\n--- Example 5.1: Performance Comparison ---")


    def measure_performance():
        """
        Compare performance of different approaches.
        """
        n = 100000

        # Method 1: List comprehension
        start = time.time()
        result = sum([x ** 2 for x in range(n)])
        time_list = time.time() - start

        # Method 2: Generator expression
        start = time.time()
        result = sum(x ** 2 for x in range(n))
        time_gen = time.time() - start

        # Method 3: Generator function
        def squares(n):
            for i in range(n):
                yield i ** 2

        start = time.time()
        result = sum(squares(n))
        time_gen_func = time.time() - start

        print(f"List comprehension: {time_list:.4f}s")
        print(f"Generator expression: {time_gen:.4f}s")
        print(f"Generator function: {time_gen_func:.4f}s")


    measure_performance()


    # Example 5.2: Memory efficiency
    print("\n--- Example 5.2: Memory Efficiency ---")


    def memory_comparison():
        """
        Compare memory usage.
        """
        n = 1000000

        # List - stores all values
        list_obj = [x for x in range(n)]
        list_size = sys.getsizeof(list_obj)

        # Generator - stores only state
        gen_obj = (x for x in range(n))
        gen_size = sys.getsizeof(gen_obj)

        print(f"List memory: {list_size:,} bytes")
        print(f"Generator memory: {gen_size:,} bytes")
        print(f"Savings: {list_size / gen_size:.0f}x")


    memory_comparison()


    # Example 5.3: Lazy evaluation benefits
    print("\n--- Example 5.3: Lazy Evaluation Benefits ---")


    def expensive_computation(x):
        """Simulate expensive operation."""
        return x ** 2


    def eager_approach(data):
        """Process all data immediately."""
        return [expensive_computation(x) for x in data]


    def lazy_approach(data):
        """Process data on-demand."""
        return (expensive_computation(x) for x in data)


    # Compare when we only need first few items
    print("When processing only first 3 items:")

    data = range(10000)

    start = time.time()
    eager = eager_approach(data)
    result = eager[:3]
    time_eager = time.time() - start

    start = time.time()
    lazy = lazy_approach(data)
    result = list(itertools.islice(lazy, 3))
    time_lazy = time.time() - start

    print(f"Eager: {time_eager:.4f}s (processed all items)")
    print(f"Lazy: {time_lazy:.4f}s (processed only 3 items)")


    # ============================================================================
    # SECTION 6: REAL-WORLD EXAMPLES
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 6: REAL-WORLD EXAMPLES")
    print("=" * 70)

    # Example 6.1: Log file analyzer
    print("\n--- Example 6.1: Log File Analyzer ---")


    def parse_log_line(line):
        """Parse a log line into structured data."""
        # Simplified parser
        parts = line.split(' - ')
        if len(parts) >= 3:
            return {
                'timestamp': parts[0],
                'level': parts[1],
                'message': parts[2]
            }
        return None


    def filter_log_level(log_stream, level):
        """Filter logs by level."""
        for entry in log_stream:
            if entry and entry.get('level') == level:
                yield entry


    def log_analyzer(filepath):
        """
        Analyze log file efficiently.

        Demonstrates real-world file processing pipeline.
        """
        # Read file line by line
        with open(filepath, 'r') as file:
            # Parse each line
            parsed = (parse_log_line(line.strip()) for line in file)

            # Filter out None values
            valid = (entry for entry in parsed if entry is not None)

            # Can now process stream
            for entry in valid:
                yield entry


    print("Log analyzer pattern defined (see code)")


    # Example 6.2: Data aggregation
    print("\n--- Example 6.2: Data Aggregation ---")


    def aggregate_by_key(data_stream, key_func):
        """
        Aggregate data by key.

        Args:
            data_stream: Stream of dictionaries
            key_func: Function to extract grouping key

        Yields:
            (key, group) tuples
        """
        # Group consecutive items by key
        for key, group in itertools.groupby(data_stream, key_func):
            yield key, list(group)


    def sum_by_key(data_stream, key_func, value_func):
        """
        Sum values grouped by key.
        """
        for key, group in aggregate_by_key(data_stream, key_func):
            total = sum(value_func(item) for item in group)
            yield key, total


    # Example usage
    print("Aggregation example:")
    sales_data = [
        {'date': '2024-01-01', 'amount': 100},
        {'date': '2024-01-01', 'amount': 150},
        {'date': '2024-01-02', 'amount': 200},
        {'date': '2024-01-02', 'amount': 250},
    ]

    totals = sum_by_key(
        sales_data,
        key_func=lambda x: x['date'],
        value_func=lambda x: x['amount']
    )

    for date, total in totals:
        print(f"  {date}: ${total}")


    # Example 6.3: Event stream processing
    print("\n--- Example 6.3: Event Stream Processor ---")


    def event_stream_processor(events):
        """
        Process stream of events.

        Demonstrates real-time event processing pattern.
        """
        window = deque(maxlen=100)  # Keep last 100 events

        for event in events:
            window.append(event)

            # Check for patterns
            if len(window) >= 3:
                last_three = list(window)[-3:]
                # Check for pattern (simplified)
                if all(e.get('type') == 'error' for e in last_three):
                    yield {
                        'alert': 'Multiple consecutive errors',
                        'events': last_three
                    }


    print("Event stream processor defined (see code)")


    # ============================================================================
    # SUMMARY AND BEST PRACTICES
    # ============================================================================

    print("\n" + "=" * 70)
    print("SUMMARY: PRACTICAL APPLICATIONS")
    print("=" * 70)

    print("""
    KEY APPLICATIONS:

    1. FILE PROCESSING:
       - Line-by-line reading for large files
       - CSV/JSON streaming
       - Log file analysis
       - Memory-efficient parsing

    2. DATA PIPELINES:
       - ETL workflows
       - Chained transformations
       - Filtering and mapping
       - Batch processing

    3. LARGE DATASETS:
       - Sliding windows
       - Chunking
       - Sampling
       - Streaming aggregation

    4. ITERTOOLS INTEGRATION:
       - islice, chain, groupby
       - zip_longest, product
       - combinations, permutations
       - accumulate

    5. PERFORMANCE:
       - Lazy evaluation
       - Memory efficiency
       - Process on-demand
       - Avoid unnecessary computation

    BEST PRACTICES:

    1. Use generators for:
       - Large files
       - Streaming data
       - Memory constraints
       - One-pass processing

    2. Combine with itertools:
       - Built-in optimizations
       - Tested implementations
       - Composable operations

    3. Build pipelines:
       - Small, focused generators
       - Easy to test
       - Reusable components
       - Clear data flow

    4. Handle resources:
       - Use context managers
       - Close generators properly
       - Clean up in finally blocks

    5. Optimize performance:
       - Profile first
       - Use generator expressions
       - Avoid premature conversion to lists
       - Process in chunks

    COMMON PATTERNS:

    1. File Processing:
       with open(file) as f:
           for line in f:
               yield process(line)

    2. Pipeline:
       stage3(stage2(stage1(source)))

    3. Filter-Map:
       (transform(x) for x in data if condition(x))

    4. Batching:
       for chunk in chunks(data, size):
           yield process_batch(chunk)

    5. Aggregation:
       for key, group in groupby(data, key_func):
           yield key, summarize(group)

    REMEMBER:
    - Generators excel at streaming data
    - Build pipelines for complex processing
    - Use lazy evaluation for efficiency
    - Integrate with itertools
    - Profile before optimizing
    - Keep generators focused and simple
    """)

    print("\n" + "=" * 70)
    print("END OF PRACTICAL APPLICATIONS")
    print("Now apply these patterns to the exercises!")
    print("=" * 70)
```

---

## Exercises


**Exercise 1.**
Use `itertools.chain` to combine three lists `[1, 2]`, `[3, 4]`, `[5, 6]` into a single iterable and print all elements.

??? success "Solution to Exercise 1"

        ```python
        from itertools import chain

        result = list(chain([1, 2], [3, 4], [5, 6]))
        print(result)  # [1, 2, 3, 4, 5, 6]
        ```

    `chain` lazily concatenates iterables without creating intermediate lists.

---

**Exercise 2.**
Use `itertools.islice` to get elements 5 through 10 from an infinite counter created with `itertools.count`.

??? success "Solution to Exercise 2"

        ```python
        from itertools import count, islice

        result = list(islice(count(0), 5, 11))
        print(result)  # [5, 6, 7, 8, 9, 10]
        ```

    `count(0)` generates 0, 1, 2, ... infinitely. `islice` selects a range without materializing the entire sequence.

---

**Exercise 3.**
Write a pipeline using `map`, `filter`, and `itertools.chain` that takes multiple lists of numbers, combines them, filters out negatives, and squares the remaining values.

??? success "Solution to Exercise 3"

        ```python
        from itertools import chain

        lists = [[-1, 2, 3], [4, -5, 6], [-7, 8]]

        result = list(
            map(lambda x: x ** 2,
                filter(lambda x: x >= 0,
                       chain(*lists)))
        )
        print(result)  # [4, 9, 16, 36, 64]
        ```

    The pipeline processes lazily: `chain` combines, `filter` removes negatives, `map` squares -- all without intermediate lists.
