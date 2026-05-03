# Stack Overflow

!!! tip "Mental Model"
    A stack overflow happens when you pile up more function call frames than the stack can hold -- like stacking books until the shelf breaks. Python prevents actual crashes by raising `RecursionError` before the OS limit is reached. The fix is almost always to ensure your recursion has a valid base case, or to convert the algorithm to an iterative loop.

## The Problem

### 1. Too Deep

```python
def infinite():
    return infinite()

try:
    infinite()
except RecursionError:
    print("Stack overflow!")
```

### 2. Recursion Limit

```python
import sys

print(sys.getrecursionlimit())  # 1000
```

## Causes

### 1. Infinite Recursion

```python
def bad_factorial(n):
    return n * bad_factorial(n - 1)
    # Missing base case!

# Stack overflow
```

### 2. Deep Recursion

```python
def deep(n):
    if n == 0:
        return 0
    return deep(n - 1)

deep(2000)  # May overflow
```

## Solutions

### 1. Base Case

```python
def factorial(n):
    if n <= 1:      # Base case!
        return 1
    return n * factorial(n - 1)
```

### 2. Increase Limit

```python
import sys

sys.setrecursionlimit(2000)

# Use carefully!
```

### 3. Use Iteration

```python
# Better than recursion
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
```

### 4. Explicit Stack

```python
def iterative_dfs(root):
    stack = [root]
    
    while stack:
        node = stack.pop()
        process(node)
        
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
```

## Summary

### 1. Stack Overflow

- Too many frames
- Recursion limit
- No tail optimization

### 2. Prevention

- Check base cases
- Use iteration
- Explicit stack
- Increase limit (careful)

---


## Runnable Example: `aliasing_via_mutable_parameters.py`

```python
"""
TUTORIAL: Aliasing via Mutable Parameters

This tutorial demonstrates another way that Python's reference semantics can
cause subtle bugs: ALIASING VIA MUTABLE PARAMETERS.

The problem is simpler than mutable defaults, but just as dangerous:
When you accept a mutable parameter and assign it directly to an instance
variable WITHOUT making a copy, you create an alias - both the caller and
your object share the same data structure.

This means the caller can modify your object's internal state by changing
their copy of the list. "Twilight Bus" makes passengers vanish through this
aliasing bug!
"""

if __name__ == "__main__":

    print("=" * 70)
    print("TUTORIAL: Aliasing via Mutable Parameters")
    print("=" * 70)

    # ============ EXAMPLE 1: The Problem - Aliasing Through Parameters
    print("\n# ============ EXAMPLE 1: The Problem - Aliasing Through Parameters")
    print("When you assign a mutable parameter directly, both sides share the list:\n")


    class TwilightBus:
        """A bus where passengers mysteriously vanish (ANTI-PATTERN)"""

        def __init__(self, passengers=None):
            # WRONG: If passengers is a list, self.passengers points to THE SAME list!
            # The caller can modify our internal state by modifying their list!
            if passengers is None:
                self.passengers = []
            else:
                self.passengers = passengers  # ALIASING! Shared reference!

        def pick(self, name):
            """Add a passenger"""
            self.passengers.append(name)

        def drop(self, name):
            """Remove a passenger"""
            self.passengers.remove(name)


    print("Scenario: Basketball team gets on a bus")
    basketball_team = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
    print(f"basketball_team = {basketball_team}")

    print("\nCreating a TwilightBus with the team:")
    bus = TwilightBus(basketball_team)
    print(f"bus.passengers = {bus.passengers}")
    print(f"basketball_team and bus.passengers are the same object: {basketball_team is bus.passengers}")

    print("\nDropping 'Tina' from the bus:")
    bus.drop('Tina')
    print(f"bus.passengers = {bus.passengers}")

    print("\nDropping 'Pat' from the bus:")
    bus.drop('Pat')
    print(f"bus.passengers = {bus.passengers}")

    print("\nBut LOOK what happened to the original list:")
    print(f"basketball_team = {basketball_team}")
    print("ALIASING BUG! Modifying the bus's passengers modified the original list!")

    # ============ EXAMPLE 2: Understanding the Aliasing Mechanism
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 2: Understanding the Aliasing Mechanism")
    print("How aliasing corrupts external data:\n")

    print("""
    THE MECHANISM:

    1. Caller creates a list:
       my_list = [1, 2, 3]

    2. Caller passes it to function:
       obj = MyClass(my_list)

    3. Function assigns directly (NO COPY):
       self.items = my_list

       Result: my_list and self.items now point to THE SAME list object

    4. Function modifies through its variable:
       self.items.remove(1)

       Result: my_list ALSO shows [2, 3] because it's the same object!

    KEY INSIGHT:
    In Python, assignment (=) never copies data. It only creates a new variable
    that points to the same object. To break the alias, you must explicitly
    make a copy.
    """)

    # ============ EXAMPLE 3: Object Identity vs Equality
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 3: Object Identity vs Equality")
    print("Understanding 'is' vs '==':\n")

    list1 = [1, 2, 3]
    list2 = [1, 2, 3]
    list3 = list1

    print(f"list1 = {list1}")
    print(f"list2 = {list2}")
    print(f"list3 = list1")

    print("\nEquality (==) checks if contents are the same:")
    print(f"list1 == list2: {list1 == list2}  (same contents)")

    print("\nIdentity (is) checks if they're the SAME object:")
    print(f"list1 is list2: {list1 is list2}  (different objects)")
    print(f"list1 is list3: {list1 is list3}  (same object!)")

    print("\nModifying list1 affects list3 but not list2:")
    list1.append(4)
    print(f"After list1.append(4):")
    print(f"list1 = {list1}")
    print(f"list2 = {list2}")
    print(f"list3 = {list3}  (changed because it's the same object as list1)")

    # ============ EXAMPLE 4: The Correct Solution - Defensive Copying
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 4: The Correct Solution - Defensive Copying")
    print("Use defensive copying to break the alias:\n")


    class SafeBus:
        """A bus that makes a defensive copy of passenger list"""

        def __init__(self, passengers=None):
            # CORRECT: Make a copy! list(passengers) creates a NEW list
            # Now self.passengers is independent from the caller's list
            if passengers is None:
                self.passengers = []
            else:
                self.passengers = list(passengers)  # Make a defensive copy!

        def pick(self, name):
            self.passengers.append(name)

        def drop(self, name):
            self.passengers.remove(name)


    print("Same scenario with SafeBus:")
    basketball_team = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
    print(f"basketball_team = {basketball_team}")

    safe_bus = SafeBus(basketball_team)
    print(f"\nsafe_bus.passengers = {safe_bus.passengers}")
    print(f"basketball_team and safe_bus.passengers are the same object: {basketball_team is safe_bus.passengers}")

    print("\nDropping 'Tina' and 'Pat' from the safe_bus:")
    safe_bus.drop('Tina')
    safe_bus.drop('Pat')
    print(f"safe_bus.passengers = {safe_bus.passengers}")

    print("\nCheck the original list:")
    print(f"basketball_team = {basketball_team}")
    print("PROTECTED! The original list remains unchanged!")

    # ============ EXAMPLE 5: How list() Creates a Copy
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 5: How list() Creates a Copy")
    print("Understanding shallow copying with the list() constructor:\n")

    original = ['A', 'B', 'C']
    copy_via_list = list(original)

    print(f"original = {original}")
    print(f"copy_via_list = list(original) = {copy_via_list}")

    print("\nAre they equal?")
    print(f"copy_via_list == original: {copy_via_list == original}  (same contents)")

    print("\nAre they the same object?")
    print(f"copy_via_list is original: {copy_via_list is original}  (different objects)")

    print("\nModifying the copy doesn't affect the original:")
    copy_via_list.append('D')
    print(f"After copy_via_list.append('D'):")
    print(f"original = {original}")
    print(f"copy_via_list = {copy_via_list}")
    print("They are completely independent!")

    # ============ EXAMPLE 6: Real-World Aliasing Bugs
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 6: Real-World Aliasing Bugs")
    print("Where aliasing bugs commonly occur:\n")

    # Example 1: Data store without defensive copying
    class BuggyDataStore:
        """Store that accidentally aliases caller's data"""

        def __init__(self, records=None):
            if records is None:
                self.records = []
            else:
                self.records = records  # BUG: Direct assignment!

        def add_record(self, record):
            self.records.append(record)

        def clear(self):
            self.records.clear()


    print("Buggy version - direct assignment:")
    company_records = ['Alice', 'Bob', 'Charlie']
    print(f"company_records = {company_records}")

    buggy_store = BuggyDataStore(company_records)
    print(f"buggy_store.records = {buggy_store.records}")

    print("\nClearing the store (intentionally):")
    buggy_store.clear()
    print(f"buggy_store.records = {buggy_store.records}")

    print("\nBUT the original list is also cleared!")
    print(f"company_records = {company_records}")
    print("-> The external data was corrupted!")

    # Safe version
    class SafeDataStore:
        """Store that makes defensive copies"""

        def __init__(self, records=None):
            if records is None:
                self.records = []
            else:
                self.records = list(records)  # SAFE: Make a copy!

        def add_record(self, record):
            self.records.append(record)

        def clear(self):
            self.records.clear()


    print("\n" + "-" * 70)
    print("Safe version - defensive copying:")
    print("-" * 70)

    company_records = ['Alice', 'Bob', 'Charlie']
    print(f"company_records = {company_records}")

    safe_store = SafeDataStore(company_records)
    print(f"safe_store.records = {safe_store.records}")

    print("\nClearing the store:")
    safe_store.clear()
    print(f"safe_store.records = {safe_store.records}")

    print("\nThe original list is unchanged:")
    print(f"company_records = {company_records}")
    print("-> Protected by defensive copying!")

    # ============ EXAMPLE 7: Comparing Buggy vs Safe Approach
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 7: Comparing Buggy vs Safe Approach")
    print("Side-by-side comparison:\n")


    class GroupBuggy:
        """Group without defensive copying"""

        def __init__(self, members=None):
            if members is None:
                self.members = []
            else:
                self.members = members  # BUG!


    class GroupSafe:
        """Group with defensive copying"""

        def __init__(self, members=None):
            if members is None:
                self.members = []
            else:
                self.members = list(members)  # SAFE!


    print("Scenario: We have a list of people")
    people = ['Alice', 'Bob']
    print(f"people = {people}")

    print("\nWith buggy version:")
    buggy_group = GroupBuggy(people)
    people.append('Charlie')  # Caller modifies their list
    print(f"After people.append('Charlie'):")
    print(f"people = {people}")
    print(f"buggy_group.members = {buggy_group.members}")
    print("-> Group's members unexpectedly changed!")

    people = ['Alice', 'Bob']
    print("\nWith safe version:")
    safe_group = GroupSafe(people)
    people.append('Charlie')  # Caller modifies their list
    print(f"After people.append('Charlie'):")
    print(f"people = {people}")
    print(f"safe_group.members = {safe_group.members}")
    print("-> Group's members protected from external changes!")

    # ============ EXAMPLE 8: When Parameters Shouldn't be Copied
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 8: When Parameters Shouldn't be Copied")
    print("Sometimes aliasing is intentional - always document it:\n")

    print("""
    RULE: Copy mutable parameters when you STORE them as instance state.

    Examples where copying IS necessary:
      - __init__(self, items=[]):        Store items -> COPY!
      - add_items(self, items=[]):       Store items -> COPY!
      - set_config(self, config=None):   Store config -> COPY!

    Examples where copying is NOT needed:
      - process_items(self, items=[]):   Just iterate over items, don't store
      - count_items(self, items=[]):     Just read items, don't store
      - contains(self, items=[]):        Just check items, don't store

    KEY: If you're storing the parameter for later use, COPY IT.
         If you're just using it immediately and discarding it, you might not need to copy.
    """)


    def bad_processor(items):
        """This just processes items, doesn't store them"""
        # No need to copy here - we're not storing the parameter
        return sum(items)  # Just using it, then discarding


    def bad_storage(items):
        """This stores items - should copy!"""
        # WRONG: Aliasing! We stored a reference to the caller's list
        self.items = items  # BUG: Should be list(items)


    # ============ EXAMPLE 9: Detecting Aliasing Bugs
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 9: Detecting Aliasing Bugs")
    print("How to spot aliasing bugs in your code:\n")

    print("""
    RED FLAGS:

    1. Direct assignment of mutable parameters:
       def __init__(self, items=[]):
           self.items = items                  <- RED FLAG!

    2. Unexpected changes to external data:
       "I didn't modify my list, why did it change?"
       -> You probably passed it to an object that aliases it

    3. State mysteriously changing:
       obj.items changed without calling obj methods
       -> Probably someone has access to the list and is modifying it

    4. Problems with shallow copies of objects:
       obj2 = copy.copy(obj1)
       "They're supposed to be independent, why do they share items?"
       -> Because obj1 and obj2 share the same list via aliasing!

    HOW TO FIX:
       1. Always copy mutable parameters in __init__
       2. Use: list(param), dict(param), set(param)
       3. Consider copying in other methods too
       4. Document when aliasing is intentional
    """)

    # ============ EXAMPLE 10: Summary of Copying Strategies
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 10: Summary of Copying Strategies")
    print("Different ways to copy mutable collections:\n")

    original_list = [1, 2, 3]
    original_dict = {'a': 1, 'b': 2}
    original_set = {1, 2, 3}

    print("SHALLOW COPIES (copy just the container, not the contents):")
    print(f"  list(original_list) = {list(original_list)}")
    print(f"  dict(original_dict) = {dict(original_dict)}")
    print(f"  set(original_set) = {set(original_set)}")

    print("\nOther shallow copy methods:")
    print(f"  original_list[:] = {original_list[:]}")
    print(f"  original_list.copy() = {original_list.copy()}")

    import copy
    print("\nDEEP COPIES (copy container AND contents recursively):")
    nested = [[1, 2], [3, 4]]
    print(f"  original nested = {nested}")
    print(f"  copy.copy(nested) = {copy.copy(nested)}")
    print(f"  copy.deepcopy(nested) = {copy.deepcopy(nested)}")

    print("\nFor most cases, shallow copy is sufficient:")
    print("  Use list(param) for lists")
    print("  Use dict(param) for dicts")
    print("  Use set(param) for sets")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    KEY TAKEAWAYS:

    1. ALIASING: When you assign a mutable parameter directly to an instance
       variable, both the caller and your object share the same data.

    2. THE PROBLEM: The caller can modify your object's internal state by
       modifying their copy of the parameter.

    3. THE SOLUTION: Use defensive copying in __init__:
       def __init__(self, passengers=None):
           if passengers is None:
               self.passengers = []
           else:
               self.passengers = list(passengers)  # Make a copy!

    4. COPY STRATEGIES:
       - list(param)  - for lists
       - dict(param)  - for dicts
       - set(param)   - for sets
       - param[:]     - for lists (alternate)
       - param.copy() - for lists/dicts (alternate)

    5. WHEN TO COPY:
       - Always in __init__ with mutable parameters
       - When you store parameters as instance variables
       - When external code might modify the parameter

    6. WHY IT MATTERS:
       - Prevents data corruption
       - Provides data isolation
       - Makes objects more predictable
       - Essential for reliable code
    """)
```


## Exercises

**Exercise 1.**
Write a recursive function `count_down(n)` that counts from n to 0. Wrap the call in a `try/except RecursionError` block. Call it with increasing values of n (100, 500, 1000, 2000) and print which values succeed and which hit the recursion limit.

??? success "Solution to Exercise 1"
        ```python
        import sys

        def count_down(n):
            if n <= 0:
                return
            count_down(n - 1)

        limit = sys.getrecursionlimit()
        print(f"Recursion limit: {limit}")

        for n in [100, 500, 1000, 2000]:
            try:
                count_down(n)
                print(f"  count_down({n}): OK")
            except RecursionError:
                print(f"  count_down({n}): RecursionError!")
        ```

---

**Exercise 2.**
Implement a recursive depth-first search on a binary tree using a `Node` class. Then implement the same DFS using an explicit stack (a Python list). Build a tree of depth 20 and verify both approaches produce the same traversal order. Print the maximum stack depth used by the iterative version.

??? success "Solution to Exercise 2"
        ```python
        class Node:
            def __init__(self, val, left=None, right=None):
                self.val = val
                self.left = left
                self.right = right

        def build_tree(depth, counter=[0]):
            if depth == 0:
                return None
            counter[0] += 1
            return Node(
                counter[0],
                build_tree(depth - 1, counter),
                build_tree(depth - 1, counter),
            )

        def dfs_recursive(node, result=None):
            if result is None:
                result = []
            if node is None:
                return result
            result.append(node.val)
            dfs_recursive(node.left, result)
            dfs_recursive(node.right, result)
            return result

        def dfs_iterative(root):
            if root is None:
                return []
            result = []
            stack = [root]
            max_depth = 0
            while stack:
                max_depth = max(max_depth, len(stack))
                node = stack.pop()
                result.append(node.val)
                if node.right:
                    stack.append(node.right)
                if node.left:
                    stack.append(node.left)
            return result, max_depth

        tree = build_tree(10)
        r1 = dfs_recursive(tree)
        r2, max_d = dfs_iterative(tree)

        print(f"Same order: {r1 == r2}")
        print(f"Max stack depth (iterative): {max_d}")
        ```

---

**Exercise 3.**
Write a script that temporarily increases the recursion limit with `sys.setrecursionlimit()`, runs a recursive function that requires depth 5000, then restores the original limit. Use `tracemalloc` to measure the peak memory used by the deep recursion.

??? success "Solution to Exercise 3"
        ```python
        import sys
        import tracemalloc

        original_limit = sys.getrecursionlimit()

        def deep_recurse(n):
            if n == 0:
                return 0
            return 1 + deep_recurse(n - 1)

        sys.setrecursionlimit(6000)
        tracemalloc.start()

        result = deep_recurse(5000)

        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        sys.setrecursionlimit(original_limit)

        print(f"Depth reached: {result}")
        print(f"Peak memory: {peak / 1024:.1f} KB")
        print(f"Limit restored to: {sys.getrecursionlimit()}")
        ```

---
