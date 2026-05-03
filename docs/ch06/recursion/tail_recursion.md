# Tail Recursion

Tail recursion is an optimization where the recursive call is the last operation in a function. Some languages optimize tail calls, but Python doesn't support tail call optimization (TCO) by design.

!!! tip "Mental Model"
    In tail recursion, the recursive call is the very last thing the function does -- there is no pending work after it returns. This means the current stack frame is no longer needed and could, in theory, be reused. Python deliberately does not optimize this away (Guido values clear tracebacks), so in practice you convert tail-recursive Python code into a loop for the same benefit.

---

## Tail Recursive Pattern

In a tail recursive function, the recursive call is the final operation:

```python
# Tail recursive: recursive call is the last statement
def factorial_tail(n, accumulator=1):
    if n <= 1:
        return accumulator
    # The return of the recursive call is the last operation
    return factorial_tail(n - 1, n * accumulator)

print(factorial_tail(5))   # 120
print(factorial_tail(5, 1))  # 120
```

Compare with non-tail recursion:

```python
# Non-tail recursive: multiplication happens after recursive call
def factorial_non_tail(n):
    if n <= 1:
        return 1
    return n * factorial_non_tail(n - 1)  # Returns result of multiply, not recursion
```

## Why Tail Recursion Matters

In languages with TCO (Scheme, Scala, some functional languages), tail recursive functions don't grow the call stack:

```python
# Without TCO, this pattern uses O(n) stack space in any language
def count_down_tail(n):
    if n <= 0:
        print("Done!")
        return
    print(n)
    return count_down_tail(n - 1)  # Python: still uses O(n) stack

count_down_tail(5)
# Output:
# 5
# 4
# 3
# 2
# 1
# Done!
```

## Converting to Iterative (Python Best Practice)

Since Python doesn't optimize tail calls, convert tail recursive code to iteration:

```python
# Tail recursive version (uses stack)
def sum_tail_recursive(numbers, index=0, accumulator=0):
    if index >= len(numbers):
        return accumulator
    return sum_tail_recursive(numbers, index + 1, accumulator + numbers[index])

# Iterative version (better for Python)
def sum_iterative(numbers):
    accumulator = 0
    for num in numbers:
        accumulator += num
    return accumulator

numbers = [1, 2, 3, 4, 5]
print(sum_tail_recursive(numbers))  # 15
print(sum_iterative(numbers))        # 15
```

## Key Takeaway for Python

Python deliberately doesn't support TCO. When you identify tail recursive code:
1. Convert to iteration for better performance
2. Or use accumulator pattern if recursion is clearer
3. Accept the O(n) stack space usage if recursion adds clarity

---

## Exercises

**Exercise 1.**
Write a tail-recursive version of `sum_to(n)` that computes the sum from 1 to n using an accumulator parameter. Then convert it to an iterative version. Verify both produce the same result for `n = 1000`.

??? success "Solution to Exercise 1"

        # Tail recursive version
        def sum_to_tail(n, acc=0):
            if n <= 0:
                return acc
            return sum_to_tail(n - 1, acc + n)

        # Iterative version
        def sum_to_iter(n):
            acc = 0
            while n > 0:
                acc += n
                n -= 1
            return acc

        print(sum_to_tail(1000))  # 500500
        print(sum_to_iter(1000))  # 500500

---

**Exercise 2.**
Write a tail-recursive `reverse_list(lst, acc=None)` function that reverses a list using an accumulator. Then write the equivalent iterative version. Test both with `[1, 2, 3, 4, 5]`.

??? success "Solution to Exercise 2"

        # Tail recursive version
        def reverse_list(lst, acc=None):
            if acc is None:
                acc = []
            if not lst:
                return acc
            return reverse_list(lst[1:], [lst[0]] + acc)

        # Iterative version
        def reverse_list_iter(lst):
            acc = []
            for item in lst:
                acc.insert(0, item)
            return acc

        print(reverse_list([1, 2, 3, 4, 5]))       # [5, 4, 3, 2, 1]
        print(reverse_list_iter([1, 2, 3, 4, 5]))   # [5, 4, 3, 2, 1]

---

**Exercise 3.**
Convert the tail-recursive `gcd(a, b)` function (Euclidean algorithm) into an iterative version. The tail-recursive version is: if `b == 0`, return `a`; otherwise, return `gcd(b, a % b)`. Show both versions and verify with `gcd(48, 18)` (expected: 6).

??? success "Solution to Exercise 3"

        # Tail recursive version
        def gcd_recursive(a, b):
            if b == 0:
                return a
            return gcd_recursive(b, a % b)

        # Iterative version
        def gcd_iterative(a, b):
            while b != 0:
                a, b = b, a % b
            return a

        print(gcd_recursive(48, 18))   # 6
        print(gcd_iterative(48, 18))   # 6
        print(gcd_recursive(270, 192)) # 6
        print(gcd_iterative(270, 192)) # 6
