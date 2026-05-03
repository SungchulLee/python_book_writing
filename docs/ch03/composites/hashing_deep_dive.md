# Hashability and Hash Tables

!!! tip "Mental Model"
    Hashability means one thing: the object has a `__hash__` method that returns a stable integer for its lifetime. Immutability is the easiest way to guarantee that stability, but they are not the same concept. A tuple of lists is immutable yet unhashable; a custom class with `__hash__` can be mutable yet hashable.

## Hashability vs Immutability

These are two distinct concepts that are often confused:

- **Immutability** — about *state*: can the object's value change after creation?
- **Hashability** — about *interface*: does the object have a valid `__hash__` method?

They are independent concepts that happen to correlate by Python's design convention:

```
Immutable → usually hashable    (not always: tuple containing a list)
Mutable   → usually unhashable  (not always: custom class with __hash__)
```

The cleanest one-line rule:

> **Hashable = `__hash__` exists and returns a stable integer. Nothing more, nothing less.**

Immutability is the most natural and common way to guarantee that stability — but it is neither necessary nor sufficient on its own.

```python
# Immutable but NOT hashable
t = (1, [2, 3])
hash(t)          # ✗ TypeError — immutable structure, but unhashable

# Mutable but hashable (custom __hash__)
class Mutable:
    def __hash__(self):
        return 42
    def __eq__(self, other):
        return self is other

m = Mutable(1)
hash(m)    # ✓ works
m.x = 99  # state changes → still mutable
```

---

## What Is a Hash Value?

The hash value is always an **integer** — the raw output of `hash()`:

```python
hash("hello")     # -8522010064543165804  (large integer)
hash(42)          # 42
hash(3.14)        # 322818021289917443
hash((1, 2, 3))   # 2528502973977326415
```

A few key properties:

- **Integers hash to themselves**: `hash(42) == 42`
- **Equal objects must have equal hashes**: `hash(1) == hash(1.0)` because `1 == 1.0`
- **Hash size**: on 64-bit systems, a 64-bit signed integer (~±9.2×10¹⁸)

### Why `1 == 1.0` Is True

Python's `==` compares **mathematical value**, not type. The integer `1` and the float `1.0` represent the same quantity, so Python considers them equal — this is a deliberate design choice consistent with most languages.

```python
1 == 1.0        # True  — same mathematical value
1 is 1.0        # False — different objects, different types
type(1) == type(1.0)  # False
```

Because `1 == 1.0`, it must also be true that `hash(1) == hash(1.0)` — otherwise dict lookups would break.

### Hash Randomization

Not all types produce stable hashes across Python sessions:

```python
hash((1, 2, 3))   # always the same value (given same Python version)
hash("hello")     # different every run  ← randomized by PYTHONHASHSEED
```

This is because `tuple.__hash__` and `str.__hash__` are **different implementations**:

| Type | Algorithm | Randomized? |
|---|---|---|
| `tuple.__hash__` | xxHash-based mixing | ✗ No |
| `str.__hash__` | SipHash-1-3 | ✓ Yes |
| `int.__hash__` | modular arithmetic | ✗ No |
| `frozenset.__hash__` | XOR-based | ✗ No |

String hashing was randomized in Python 3.3 as a **security fix** — without it, an attacker could craft input strings that all hash to the same bucket, causing a hash collision DoS attack on web servers.

---

## How Tuple Hashing Works

The hash of a tuple is computed **recursively from its elements**, combining their hash values using an xxHash-inspired algorithm:

```python
# Pseudocode approximation
def tuple_hash(t):
    acc = 2870177450012600261  # fixed initial seed (not randomized)
    for element in t:
        acc = mix(acc, hash(element))  # needs each element's hash
    return acc
```

This is why `(1, [2, 3])` fails — computing the tuple's hash requires `hash([2, 3])`, but lists are unhashable:

```python
hash((1, [2, 3]))   # ✗ TypeError — fails at runtime when it tries hash([2,3])
```

Order matters in tuples:

```python
hash((1, 2)) == hash((2, 1))               # False — order is part of the computation
hash(frozenset({1,2})) == hash(frozenset({2,1}))  # True  — frozenset is unordered
```

---

## Why Hashability Exists: Hash Table Lookup

Hash values exist primarily to enable **O(1) lookup** in hash tables. Python's `dict` and `set` are both hash tables underneath.

```
key → hash(key) → bucket index → value
bucket index = hash(key) % table_size
```

This is why:

- `dict` keys must be hashable — Python needs a bucket index to store and find them
- `set` members must be hashable — same reason
- `list` has `__hash__ = None` — it was never designed for hash table lookup

```python
# list — no hash table → linear scan
1000 in [0, 1, 2, ..., 999]   # O(n) — checks each element

# set — hash table → direct bucket lookup
1000 in {0, 1, 2, ..., 999}   # O(1) — hash(1000) → bucket → found
```

The hash value is a **large integer** that is a stable property of the key. The **bucket index** is a small integer derived at runtime from the current table size:

```python
hash("hello")          # -8522010064543165804  ← property of the key, stable
hash("hello") % 8      # 4                     ← bucket index, depends on table size
hash("hello") % 16     # 12                    ← different table size → different bucket
```

This separation is deliberate:

- `__hash__` is responsible for producing a **good, stable, large integer**
- The hash table maps that integer to a bucket via `%`

---

## Hash Table Internals

### Load Factor and Memory Overhead

Python's `dict` keeps the **load factor** (entries / table size) below **2/3**:

```
table size = 8
max entries before resize = 5   (8 × 2/3 ≈ 5)
```

The used area grows from 1/3 to 2/3, then resize kicks in:

```
used area 1/3 ────────────> used area 2/3 ──> resize ──> used area 1/3
```

This means at any time, at least **1/3 of the table is intentionally empty**. The memory overhead oscillates:

| Moment | Used | Empty (wasted) |
|---|---|---|
| Just after resize | ~1/3 | ~2/3 |
| Just before resize | ~2/3 | ~1/3 |
| Average | ~1/2 | ~1/2 |

In practice each empty slot is just 8 bytes (a null pointer), so the real memory cost is small. The O(1) lookup benefit far outweighs the memory overhead.

### Resize: Like List Resize, Plus Rehashing

When the 6th entry is inserted into a size-8 table, Python resizes:

```
List resize:  allocate new array → memcopy        → done   O(n)
Dict resize:  allocate new table → rehash + reinsert → done   O(n)
```

The extra step is necessary because bucket indices change with table size:

```python
hash("hello") % 8  = 3   # old table
hash("hello") % 16 = 11  # new table — different bucket!
```

Every key must be recomputed and repositioned. Both list and dict resize are **O(1) amortized** for the same reason — table size doubles each time, so resizes become exponentially rare.

### Collision Resolution: Open Addressing

When two keys land in the same bucket, Python uses **open addressing** — it probes for the next available slot rather than chaining a linked list.

**Simple linear probing** (not what Python does):
```
collision at bucket 3 → try 4 → try 5 → try 6 ...
```

Problem: this causes **clustering** — long occupied runs that make future collisions worse.

**Python's actual probing formula** (from CPython source):
```python
j = (5 * j + 1 + perturb) % table_size
perturb >>= 5
```

Here `j` on the right is the **current (occupied) bucket**, and `j` on the left is the **next bucket to probe**.

This jumps pseudo-randomly around the table:
```
simple linear:  3 → 4 → 5 → 6        # clustering
Python actual:  3 → 11 → 6 → 14      # spread out
```

The table is logically a **circular buffer** — the `%` operation causes wrap-around so no index ever goes out of bounds:

```
(7 + 1) % 8 = 0   ← wraps back to start
```

### The `perturb` Variable

`perturb` starts as the **full hash value** (before `% table_size`) and decays toward zero:

```python
perturb = hash(key)           # large integer — full hash value
j = perturb % table_size      # initial bucket

# each collision step:
j = (5 * j + 1 + perturb) % table_size
perturb >>= 5                  # right shift by 5: divide by 32
```

`>>=` is a compound bitwise shift — `perturb >>= 5` means `perturb = perturb >> 5`, dropping the 5 rightmost bits each step:

```
step 0: perturb = 12345678          (64 bits of randomness)
step 1: perturb = 385802            (÷ 32)
step 2: perturb = 12056             (÷ 32 again)
step 3: perturb = 376
step 4: perturb = 11
step 5: perturb = 0                 ← effectively dead
```

Once `perturb` reaches 0, the formula reduces to `j = (5*j + 1) % table_size` — a deterministic cycle guaranteed to visit every bucket, ensuring insertion always succeeds.

**Why use the full hash value instead of just the bucket index?**

Two keys can share the same initial bucket but have different full hash values:

```python
hash("hello") % 8 = 3    # full hash = -8522010064543165804
hash("world") % 8 = 3    # full hash =  1234567890123456789
# same bucket → collision!
```

Using the full hash in `perturb` gives them **different probe sequences**, resolving collisions quickly. Using only the bucket index (3) would send both down the same path.

### Deletion: Tombstones

You cannot simply empty a slot on deletion — it would break ongoing probe sequences:

```
delete "hello" at bucket 3 → empty slot

lookup "world": bucket 3 → empty → stop! → not found ✗  WRONG
```

Python uses a **tombstone** marker instead:

```
delete "hello" → bucket 3 → mark DELETED (tombstone)

lookup "world": bucket 3 → tombstone → keep probing
               → bucket 4 → found "world" ✓
```

---

## Summary

```
__hash__ exists
    → hash(key) returns a large integer
        → hash(key) % table_size returns bucket index
            → O(1) lookup is possible
                → can be used as dict key / set member

list has no __hash__
    → no bucket index computable
        → only linear O(n) scan possible
            → cannot be dict key / set member
```

People often say "dict keys must be immutable" — but the correct term is **hashable**. Immutability is just the most common way to guarantee a stable hash value. The actual technical requirement is always hashability.

---

## Runnable Example: `hashing_implementation_tutorial.py`

```python
"""
TUTORIAL: Hashing Fundamentals - __hash__ and __eq__ Working Together

Why this matters:
  When you put objects in a dict or set, Python uses HASHING to find them quickly.
  The hash value determines where to store the object. But here's the catch:
  __hash__ and __eq__ MUST work together consistently. If they disagree,
  lookups fail even when the object exists!

  This tutorial shows:
  1. What happens with default hash (identity-based)
  2. What you get with custom __hash__ and __eq__
  3. Why BOTH methods matter and must be consistent

Core lesson:
  If you override __eq__ to define equality by value, you MUST override __hash__
  to hash by the same values. Otherwise, equal objects won't be treated as equal
  in sets and dicts.
"""


# ============ Example 1: Default Hash (Identity-based) ============
# Without custom __hash__ and __eq__, two Point(1,1) objects are different
# because they're different objects in memory. Python uses the object's
# memory address (identity) for the default hash.

class Point:
    """Point with no custom hash or equality. Uses object identity."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


# ============ Example 2: Custom Hash and Equality ============
# By defining __hash__ and __eq__ based on coordinates, two Point objects
# with the same x and y are treated as equal and hash to the same value.

class PointHash:
    """Point with custom hash and equality based on coordinates."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        """Hash based on coordinates, not object identity."""
        return hash((self.x, self.y))

    def __eq__(self, other):
        """Two points are equal if they have same coordinates."""
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"PointHash({self.x}, {self.y})"


def demo_default_hash():
    """Show how default hash fails for equality by value."""
    print("\n" + "=" * 70)
    print("Example 1: Default Hash (Identity-based)")
    print("=" * 70)

    p1 = Point(1, 1)
    p2 = Point(1, 1)

    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    print(f"\np1 == p2: {p1 == p2}  (False, different objects)")
    print(f"p1 is p2: {p1 is p2}  (False, different memory addresses)")

    # Create a set with both points
    points = set([p1, p2])
    print(f"\nset([p1, p2]) = {points}")
    print(f"Set has {len(points)} items (both points are stored separately)")

    # Try to find a point with same coordinates
    p3 = Point(1, 1)
    found = p3 in points
    print(f"\nPoint(1, 1) in set([p1, p2]) = {found}")
    print("WHY: p3 is a different object, different hash, lookup fails!")

    print("""
    PROBLEM with default hash:
    - Hash is based on object identity (memory address)
    - Two objects with same data get different hashes
    - Sets/dicts can't find equal objects
    """)


def demo_custom_hash():
    """Show how custom hash/eq enables value-based equality."""
    print("\n" + "=" * 70)
    print("Example 2: Custom Hash and Equality (Value-based)")
    print("=" * 70)

    p1 = PointHash(1, 1)
    p2 = PointHash(1, 1)

    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    print(f"\np1 == p2: {p1 == p2}  (True, same coordinates!)")
    print(f"hash(p1) == hash(p2): {hash(p1) == hash(p2)}  (True, same hash!)")

    # Create a set with both points
    points = set([p1, p2])
    print(f"\nset([p1, p2]) = {points}")
    print(f"Set has {len(points)} item (duplicate detected and removed!)")

    # Try to find a point with same coordinates
    p3 = PointHash(1, 1)
    found = p3 in points
    print(f"\nPointHash(1, 1) in set([p1, p2]) = {found}")
    print("SUCCESS: p3 has same hash and is equal to p1/p2, found in set!")

    print("""
    SOLUTION with custom hash/eq:
    - Hash is based on coordinates (the actual data)
    - Two objects with same data get same hash
    - Sets/dicts find equal objects correctly
    """)


def demo_hash_eq_consistency():
    """Show why __hash__ and __eq__ must be consistent."""
    print("\n" + "=" * 70)
    print("Example 3: Why __hash__ and __eq__ Must Be Consistent")
    print("=" * 70)

    p1 = PointHash(1, 1)
    p2 = PointHash(1, 1)
    p3 = PointHash(2, 2)

    print("Rule: If a == b, then hash(a) == hash(b)")
    print()

    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    print(f"p3 = {p3}")
    print()

    print(f"p1 == p2: {p1 == p2}")
    print(f"hash(p1) = {hash(p1)}")
    print(f"hash(p2) = {hash(p2)}")
    print(f"hash(p1) == hash(p2): {hash(p1) == hash(p2)} ✓ CONSISTENT")
    print()

    print(f"p1 == p3: {p1 == p3}")
    print(f"hash(p1) = {hash(p1)}")
    print(f"hash(p3) = {hash(p3)}")
    print(f"hash(p1) == hash(p3): {hash(p1) == hash(p3)} ✓ CONSISTENT")
    print()

    print("""
    WHY consistency matters:
    - Dict/set uses hash to find bucket
    - Then uses == to find exact item in bucket
    - If p1 == p2 but hash(p1) != hash(p2), they go to different buckets
    - Lookup fails even though object exists!
    """)


def demo_use_in_dict():
    """Show that custom hash enables dict use."""
    print("\n" + "=" * 70)
    print("Example 4: Using Custom Hash in Dictionaries")
    print("=" * 70)

    p1 = PointHash(1, 1)
    p2 = PointHash(1, 1)  # Equal to p1
    p3 = PointHash(2, 2)

    # Create a dict with point coordinates as keys
    distances = {}
    distances[p1] = 1.41  # Distance from origin

    print(f"distances[PointHash(1, 1)] = {distances[p1]}")
    print(f"distances[p2] = {distances[p2]}")  # p2 is equal to p1, so same key
    print(f"distances[p3] = {distances.get(p3, 'NOT FOUND')}")

    print(f"\nDict has {len(distances)} entry (p1 and p2 are the same key)")


if __name__ == "__main__":
    print("=" * 70)
    print("TUTORIAL: Hashing - __hash__ and __eq__")
    print("=" * 70)

    demo_default_hash()
    demo_custom_hash()
    demo_hash_eq_consistency()
    demo_use_in_dict()

    # -------- KEY INSIGHTS --------
    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print("""
1. DEFAULT HASH is identity-based:
   - Two objects with same data get different hashes
   - Sets and dicts treat them as different items
   - Use default hash only when object identity matters

2. CUSTOM HASH must be value-based:
   - Hash based on the attributes that define equality
   - Equal objects must have equal hashes
   - Different objects should (usually) have different hashes

3. __HASH__ and __EQ__ are a pair:
   - Always override both together
   - They must be consistent (see Rule above)
   - Violating consistency causes hard-to-find bugs

4. HASH MUST BE IMMUTABLE:
   - Hash value must never change after object creation
   - Only hash immutable attributes (strings, ints, tuples)
   - Don't hash mutable attributes (lists, dicts, sets)

5. PRACTICAL RULE:
   - If you override __eq__, override __hash__ too
   - Think about which attributes define equality
   - Hash those exact attributes using tuple or XOR
   - Test that equal objects have equal hashes
    """)
```


---

## Runnable Example: `hash_function_performance.py`

```python
"""
TUTORIAL: How Hash Function Quality Impacts Dictionary Performance

Why this matters:
  A HASH FUNCTION distributes keys across buckets in a dict or set. A BAD hash
  function sends most keys to the same bucket, turning O(1) lookup into O(n).
  A GOOD hash function spreads keys evenly, keeping O(1) fast.

  This tutorial shows:
  1. How a bad hash (returning constant 42) destroys performance
  2. How a good hash spreads values and stays fast
  3. Why hash quality matters for real-world dicts/sets

Core lesson:
  Hash functions seem invisible, but quality determines whether your dict
  lookups are O(1) or O(n). Always ensure custom hashes distribute evenly.
"""

import string
import timeit


# ============ Example 1: A Bad Hash Function ============
# This hash always returns 42. All keys hash to the same value, so they
# all go in the same bucket. Lookup becomes a linear search through that bucket.

class BadHash(str):
    """String subclass with terrible hash function."""

    def __hash__(self):
        """Always return 42. All keys collide into same bucket!"""
        return 42


# ============ Example 2: A Good Hash Function ============
# This hash distributes two-letter strings evenly based on their characters.
# Keys spread across buckets, keeping lookups fast even with many items.

class GoodHash(str):
    """String subclass with good hash function."""

    def __hash__(self):
        """
        Hash based on first two letters.
        Spread all 26x26=676 combinations across different buckets.
        """
        # Use character ordinals to create distinct hash values
        # Simplified formula, but demonstrates good distribution
        return ord(self[1]) + 26 * ord(self[0]) - 2619


def demo_hash_distribution():
    """Visualize how hash functions distribute keys."""
    print("\n" + "=" * 70)
    print("Example 1: How Hash Functions Distribute Keys")
    print("=" * 70)

    bad_hashes = set()
    good_hashes = set()

    # Generate all two-letter combinations
    for i in string.ascii_lowercase:
        for j in string.ascii_lowercase:
            key = i + j
            bad_hash_val = 42  # BadHash always returns 42
            good_hash_val = ord(j) + 26 * ord(i) - 2619

            bad_hashes.add(bad_hash_val)
            good_hashes.add(good_hash_val)

    print(f"Generated {26 * 26} two-letter combinations")
    print()
    print(f"BadHash unique values:  {len(bad_hashes)}")
    print(f"  All 676 keys hash to: 42 (TERRIBLE collision!)")
    print()
    print(f"GoodHash unique values: {len(good_hashes)}")
    print(f"  Keys spread across {len(good_hashes)} different hash values")
    print(f"  Much better distribution!")


def demo_lookup_performance():
    """Compare lookup speed with bad vs good hash."""
    print("\n" + "=" * 70)
    print("Example 2: Lookup Performance - Bad vs Good Hash")
    print("=" * 70)

    # Create a set of all two-letter combinations
    baddict = set()
    gooddict = set()

    print("Building sets with 676 two-letter combinations...")
    for i in string.ascii_lowercase:
        for j in string.ascii_lowercase:
            key = i + j
            baddict.add(BadHash(key))
            gooddict.add(GoodHash(key))

    print(f"  baddict size:  {len(baddict)}")
    print(f"  gooddict size: {len(gooddict)}")
    print()

    # Time lookups in baddict (all keys hash to same bucket)
    print("Timing 100,000 lookups for 'zz' in each set...")
    print()

    badtime = timeit.repeat(
        stmt="key in baddict",
        setup="from __main__ import baddict, BadHash; key = BadHash('zz')",
        repeat=3,
        number=100_000,
    )

    goodtime = timeit.repeat(
        stmt="key in gooddict",
        setup="from __main__ import gooddict, GoodHash; key = GoodHash('zz')",
        repeat=3,
        number=100_000,
    )

    bad_min = min(badtime)
    good_min = min(goodtime)
    slowdown = bad_min / good_min

    print(f"BadHash  min time: {bad_min:.4f} seconds")
    print(f"GoodHash min time: {good_min:.4f} seconds")
    print()
    print(f"BadHash is {slowdown:.1f}x SLOWER than GoodHash!")
    print()
    print("""
    WHY this huge difference:

    BadHash (constant 42):
    - All 676 keys collide in the same bucket
    - Lookup must scan through 676 comparisons
    - O(n) time where n = bucket size

    GoodHash (distributed):
    - Keys spread across ~650+ different buckets
    - Average bucket has ~1 item
    - Lookup finds item immediately (O(1))
    """)


def demo_hash_quality_rules():
    """Show the properties of good hash functions."""
    print("\n" + "=" * 70)
    print("Example 3: What Makes a Good Hash Function")
    print("=" * 70)

    print("""
    PROPERTIES OF GOOD HASH FUNCTIONS:

    1. DETERMINISTIC:
       - Same input always gives same hash
       - hash(obj) must never change for the same object

    2. FAST:
       - Hashing should be quick (O(1) time)
       - If hash is slow, lookups become slow

    3. UNIFORMLY DISTRIBUTED:
       - Different inputs should hash to different buckets
       - Spread keys across many hash values
       - Minimize collisions (multiple keys per bucket)

    4. AVALANCHE PROPERTY:
       - Small change in input → big change in hash
       - If two keys are similar, hashes should differ
       - Prevents clustering of similar keys

    WHAT BAD HASHES DO:
    - Return constants (all keys → same bucket)
    - Return predictable patterns (collisions cluster)
    - Are slow to compute
    - Ignore important attributes of the data
    """)

    # Demonstrate clustering issue
    print("\n" + "-" * 70)
    print("Example of clustering:")
    print("-" * 70)

    print("\nBadHash clustering:")
    bad_examples = [BadHash('aa'), BadHash('ab'), BadHash('zz')]
    for ex in bad_examples:
        print(f"  hash({repr(ex)}) = {hash(ex)}")

    print("\nGoodHash distribution:")
    good_examples = [GoodHash('aa'), GoodHash('ab'), GoodHash('zz')]
    for ex in good_examples:
        print(f"  hash({repr(ex)}) = {hash(ex)}")

    print("\nNotice: GoodHash values are spread far apart (different buckets)")
    print("        BadHash values are identical (same bucket, linear search)")


def demo_real_world_impact():
    """Show impact on real operations."""
    print("\n" + "=" * 70)
    print("Example 4: Real-World Impact on Operations")
    print("=" * 70)

    print("""
    Scenario: You have a set of 1,000 API endpoints (usernames, IDs, etc.)

    With GOOD hash:
    - Lookup: ~1,000,000 operations, instant
    - Add: Insert at correct bucket, instant
    - Remove: Find and remove, instant
    - Memory: Buckets distributed, moderate

    With BAD hash (all keys → same bucket):
    - Lookup: Must scan ~1,000 items linearly, SLOW
    - Add: Must check all existing items, SLOW
    - Remove: Must scan entire bucket, SLOW
    - Memory: Everything in one bucket, cache-bad

    With 10,000 requests/second:
    - Good hash: Sub-millisecond response
    - Bad hash: Multiple second response (unusable!)
    """)


if __name__ == "__main__":
    print("=" * 70)
    print("TUTORIAL: Hash Function Quality and Performance")
    print("=" * 70)

    demo_hash_distribution()
    demo_lookup_performance()
    demo_hash_quality_rules()
    demo_real_world_impact()

    # -------- KEY INSIGHTS --------
    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print("""
1. HASH FUNCTION is INVISIBLE but CRITICAL:
   - It determines if dict/set is O(1) or O(n)
   - Bad hash turns fast lookups into slow scans
   - You usually don't think about it, but quality matters

2. COLLISIONS destroy performance:
   - Collision = multiple keys hash to same value
   - When collision happens, must do linear search
   - Good hash minimizes collisions

3. EVEN DISTRIBUTION is essential:
   - Hash values should spread across all buckets
   - Each bucket should have ~1 item on average
   - Large buckets mean slow lookups for those items

4. CUSTOM HASHES often perform poorly:
   - Easy to accidentally create clustering
   - Must think carefully about value distribution
   - Test your custom hash on realistic data

5. BUILT-IN HASHES are highly optimized:
   - Python's hash for str, int, tuple is excellent
   - Use built-in types when possible
   - Only custom hash when necessary

6. MEASURE BEFORE OPTIMIZING:
   - Profile your code to find bottlenecks
   - Bad hash is only a problem if it's slow
   - But when it is, slowdown is dramatic
    """)
```

---

## Exercises


**Exercise 1.**
Verify the hash consistency rule: if `a == b`, then `hash(a) == hash(b)`. Test this with `1` and `1.0`, with `True` and `1`, and with two identical tuples.

??? success "Solution to Exercise 1"

        ```python
        # int and float
        print(1 == 1.0)                # True
        print(hash(1) == hash(1.0))    # True

        # bool and int
        print(True == 1)               # True
        print(hash(True) == hash(1))   # True

        # identical tuples
        t1 = (1, 2, 3)
        t2 = (1, 2, 3)
        print(t1 == t2)               # True
        print(hash(t1) == hash(t2))   # True
        ```

    The hash consistency rule is fundamental: equal objects must have equal hashes. This is required for correct behavior in sets and dictionaries.

---

**Exercise 2.**
Write a class `Color` with attributes `r`, `g`, `b` that is both hashable and supports equality comparison. Two `Color` objects should be equal if their RGB values match. Use it as a dictionary key.

??? success "Solution to Exercise 2"

        ```python
        class Color:
            def __init__(self, r, g, b):
                self.r = r
                self.g = g
                self.b = b

            def __eq__(self, other):
                return (self.r, self.g, self.b) == (other.r, other.g, other.b)

            def __hash__(self):
                return hash((self.r, self.g, self.b))

        palette = {Color(255, 0, 0): "red", Color(0, 255, 0): "green"}
        print(palette[Color(255, 0, 0)])  # red
        ```

    Both `__eq__` and `__hash__` must be implemented. The hash is based on the same fields used for equality.

---

**Exercise 3.**
Explain why lists are not hashable. Demonstrate the error that occurs when you try to use a list as a dictionary key, and show how converting it to a tuple solves the problem.

??? success "Solution to Exercise 3"

        ```python
        try:
            d = {[1, 2]: "value"}
        except TypeError as e:
            print(f"Error: {e}")  # unhashable type: 'list'

        # Convert to tuple
        d = {(1, 2): "value"}
        print(d[(1, 2)])  # value
        ```

    Lists are mutable, so their contents can change after insertion into a set or dict, which would break the hash consistency rule. Tuples are immutable and therefore hashable.
