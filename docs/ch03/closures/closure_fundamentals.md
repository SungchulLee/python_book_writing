# Closure Fundamentals

클로저는 자신이 정의된 스코프의 변수를 캡처하는 함수입니다.

!!! tip "Mental Model"
    A closure is a function that remembers the room it was born in. Even after the enclosing function finishes and its local scope is gone, the inner function keeps a living reference to the variables it captured. This is what lets factory functions produce customized workers that each carry their own private state.

## What is a Closure?

### Definition

```python
def outer():
    x = 10  # Enclosing variable
    
    def inner():
        return x  # Captures x
    
    return inner

f = outer()
print(f())  # 10 — x is still accessible
```

`outer()`가 반환된 후에도 `inner`는 `x`에 접근할 수 있습니다. 이것이 클로저입니다.

### Key Terms

| Term | Definition |
|------|------------|
| **Closure** | Function with captured variables from enclosing scope |
| **Free Variable** | Variable used in function but defined in enclosing scope |
| **Cell** | CPython object that stores captured variable |
| **Enclosing Scope** | Parent function's local scope |

---

## Free Variables and Cells

### Free Variables

변수가 함수 내에서 사용되지만 로컬에서 정의되지 않은 경우:

```python
def outer():
    x = 10
    
    def inner():
        return x  # x is "free" in inner
    
    return inner

f = outer()
print(f.__code__.co_freevars)  # ('x',)
```

### Cell Objects

CPython은 캡처된 변수를 cell 객체에 저장합니다:

```python
def outer():
    x = 10
    
    def inner():
        return x
    
    return inner

f = outer()
print(f.__closure__)  # (<cell at 0x...>,)
print(f.__closure__[0].cell_contents)  # 10
```

---

## Cellvars vs Freevars

같은 변수가 두 가지 관점에서 보입니다:

```python
def outer():
    x = 10  # cellvar in outer
    
    def inner():
        return x  # freevar in inner
    
    return inner

# In outer: x is a cellvar (being captured)
print(outer.__code__.co_cellvars)  # ('x',)

# In inner: x is a freevar (captured from outside)
f = outer()
print(f.__code__.co_freevars)  # ('x',)
```

| Perspective | Variable Type | Meaning |
|-------------|--------------|---------|
| Enclosing function | `cellvar` | "I'm being captured" |
| Inner function | `freevar` | "I captured this" |

---

## Multi-Level Nesting

### Three-Level Example

```python
def level1():
    x = "L1"
    
    def level2():
        y = "L2"
        
        def level3():
            return x, y  # Both are free variables
        
        return level3
    
    return level2()

f = level1()
print(f())  # ('L1', 'L2')
print(f.__code__.co_freevars)  # ('x', 'y')
```

### Only Used Variables Are Captured

```python
def outer():
    x = "used"
    y = "unused"
    
    def inner():
        return x  # Only x is captured
    
    return inner

f = outer()
print(f.__code__.co_freevars)  # ('x',) — y not captured
```

### Variable Shadowing

```python
def outer():
    x = "outer"
    
    def middle():
        x = "middle"  # Shadows outer's x
        
        def inner():
            return x  # Gets nearest x
        
        return inner
    
    return middle()

f = outer()
print(f())  # 'middle'
```

Python은 **안쪽에서 바깥쪽으로** 변수를 찾습니다.

---

## Scope Chain (LEGB)

변수 조회 순서:

```
Local → Enclosing → Global → Builtin
```

```python
x = "global"

def level1():
    x = "level1"
    
    def level2():
        x = "level2"
        
        def level3():
            print(x)  # "level2" (nearest enclosing)
        
        level3()
    
    level2()

level1()
```

### Skipping Levels

```python
def outer():
    x = 10
    
    def middle():
        # No x defined here
        
        def inner():
            return x  # Skips middle, uses outer's x
        
        return inner
    
    return middle()

f = outer()
print(f())  # 10
```

---

## Closure Inspection

### Complete Inspection Example

```python
def make_counter(start=0):
    count = start
    
    def increment():
        nonlocal count
        count += 1
        return count
    
    return increment

counter = make_counter(10)

# Inspect
print(counter.__closure__)  # (<cell ...>,)
print(counter.__code__.co_freevars)  # ('count',)

for var, cell in zip(counter.__code__.co_freevars, counter.__closure__):
    print(f"{var} = {cell.cell_contents}")
# count = 10
```

---

## Summary

| Concept | Description |
|---------|-------------|
| Closure | Function + captured environment |
| Free variable | Referenced but not locally defined |
| Cell | CPython's storage for captured variables |
| Cellvar | Variable being captured (in outer function) |
| Freevar | Captured variable (in inner function) |
| LEGB | Local → Enclosing → Global → Builtin |

---

## Runnable Example: `closures_examples.py`

```python
"""
Python Closures - Practical Examples
This file contains various practical examples of closures in Python.
Run this file to see closures in action!
"""

if __name__ == "__main__":

    print("=" * 70)
    print("PYTHON CLOSURES - EXAMPLES")
    print("=" * 70)

    # ============================================================================
    # EXAMPLE 1: Basic Closure
    # ============================================================================
    print("\n1. BASIC CLOSURE")
    print("-" * 70)

    def outer(message):
        # message is captured by the closure
        def inner():
            print(message)
        return inner

    greet = outer("Hello, World!")
    greet()  # Prints: Hello, World!

    print("\nEven though outer() finished, inner() remembers 'message'")

    # ============================================================================
    # EXAMPLE 2: Multiple Closures with Different Environments
    # ============================================================================
    print("\n\n2. MULTIPLE CLOSURES WITH DIFFERENT ENVIRONMENTS")
    print("-" * 70)

    def make_multiplier(factor):
        def multiply(number):
            return number * factor
        return multiply

    times_2 = make_multiplier(2)
    times_3 = make_multiplier(3)
    times_10 = make_multiplier(10)

    print(f"5 * 2 = {times_2(5)}")
    print(f"5 * 3 = {times_3(5)}")
    print(f"5 * 10 = {times_10(5)}")
    print("\nEach closure maintains its own 'factor' value")

    # ============================================================================
    # EXAMPLE 3: Using nonlocal to Modify Enclosing Variables
    # ============================================================================
    print("\n\n3. USING NONLOCAL TO MODIFY ENCLOSING VARIABLES")
    print("-" * 70)

    def make_counter(start=0):
        count = start

        def increment():
            nonlocal count  # Allow modification of outer variable
            count += 1
            return count

        def decrement():
            nonlocal count
            count -= 1
            return count

        def get_count():
            return count

        return increment, decrement, get_count

    inc, dec, get = make_counter(10)
    print(f"Initial count: {get()}")
    print(f"After increment: {inc()}")
    print(f"After increment: {inc()}")
    print(f"After increment: {inc()}")
    print(f"After decrement: {dec()}")
    print(f"Final count: {get()}")

    # ============================================================================
    # EXAMPLE 4: Factory Functions
    # ============================================================================
    print("\n\n4. FACTORY FUNCTIONS")
    print("-" * 70)

    def make_power(exponent):
        def power(base):
            return base ** exponent
        return power

    square = make_power(2)
    cube = make_power(3)
    fourth_power = make_power(4)

    number = 3
    print(f"{number}^2 = {square(number)}")
    print(f"{number}^3 = {cube(number)}")
    print(f"{number}^4 = {fourth_power(number)}")

    # ============================================================================
    # EXAMPLE 5: Data Encapsulation (Private Variables)
    # ============================================================================
    print("\n\n5. DATA ENCAPSULATION (PRIVATE VARIABLES)")
    print("-" * 70)

    def make_account(initial_balance):
        balance = initial_balance  # Private variable

        def deposit(amount):
            nonlocal balance
            if amount > 0:
                balance += amount
                return f"Deposited ${amount}. New balance: ${balance}"
            return "Invalid amount"

        def withdraw(amount):
            nonlocal balance
            if amount > balance:
                return "Insufficient funds"
            if amount > 0:
                balance -= amount
                return f"Withdrew ${amount}. New balance: ${balance}"
            return "Invalid amount"

        def get_balance():
            return f"Current balance: ${balance}"

        return {
            'deposit': deposit,
            'withdraw': withdraw,
            'get_balance': get_balance
        }

    account = make_account(1000)
    print(account['get_balance']())
    print(account['deposit'](500))
    print(account['withdraw'](200))
    print(account['withdraw'](2000))  # Insufficient funds
    print(account['get_balance']())

    # Note: There's no way to directly access 'balance' from outside!

    # ============================================================================
    # EXAMPLE 6: Function Decorators (Built on Closures)
    # ============================================================================
    print("\n\n6. FUNCTION DECORATORS (BUILT ON CLOSURES)")
    print("-" * 70)

    def make_logger(func):
        def wrapper(*args, **kwargs):
            print(f"🔍 Calling {func.__name__} with args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            print(f"✅ {func.__name__} returned {result}")
            return result
        return wrapper

    @make_logger
    def add(a, b):
        return a + b

    @make_logger
    def multiply(x, y):
        return x * y

    result1 = add(3, 5)
    print(f"Result: {result1}\n")
    result2 = multiply(4, 7)
    print(f"Result: {result2}")

    # ============================================================================
    # EXAMPLE 7: Configuration Functions
    # ============================================================================
    print("\n\n7. CONFIGURATION FUNCTIONS")
    print("-" * 70)

    def make_formatter(prefix, suffix):
        def format_text(text):
            return f"{prefix}{text}{suffix}"
        return format_text

    html_bold = make_formatter("<b>", "</b>")
    html_italic = make_formatter("<i>", "</i>")
    parentheses = make_formatter("(", ")")
    quotes = make_formatter('"', '"')

    text = "Hello"
    print(f"Original: {text}")
    print(f"Bold: {html_bold(text)}")
    print(f"Italic: {html_italic(text)}")
    print(f"Parentheses: {parentheses(text)}")
    print(f"Quoted: {quotes(text)}")

    # ============================================================================
    # EXAMPLE 8: Closures with Multiple Free Variables
    # ============================================================================
    print("\n\n8. CLOSURES WITH MULTIPLE FREE VARIABLES")
    print("-" * 70)

    def make_linear_function(slope, intercept):
        """Create a linear function: y = slope * x + intercept"""
        def linear(x):
            return slope * x + intercept
        return linear

    line1 = make_linear_function(2, 3)   # y = 2x + 3
    line2 = make_linear_function(-1, 5)  # y = -x + 5

    x_value = 4
    print(f"For x = {x_value}:")
    print(f"  y = 2x + 3 = {line1(x_value)}")
    print(f"  y = -x + 5 = {line2(x_value)}")

    # ============================================================================
    # EXAMPLE 9: Closures for Callbacks with State
    # ============================================================================
    print("\n\n9. CLOSURES FOR CALLBACKS WITH STATE")
    print("-" * 70)

    def make_click_handler(element_id):
        click_count = 0

        def handle_click():
            nonlocal click_count
            click_count += 1
            print(f"  {element_id} clicked {click_count} time(s)")

        return handle_click

    button1 = make_click_handler("Button 1")
    button2 = make_click_handler("Button 2")

    print("Simulating button clicks:")
    button1()  # Button 1 clicked 1 time
    button1()  # Button 1 clicked 2 times
    button2()  # Button 2 clicked 1 time
    button1()  # Button 1 clicked 3 times
    button2()  # Button 2 clicked 2 times

    # ============================================================================
    # EXAMPLE 10: Closure vs Class Comparison
    # ============================================================================
    print("\n\n10. CLOSURE VS CLASS COMPARISON")
    print("-" * 70)

    # Using a closure
    def make_counter_closure(start=0):
        count = start
        def increment():
            nonlocal count
            count += 1
            return count
        return increment

    # Using a class
    class CounterClass:
        def __init__(self, start=0):
            self.count = start

        def increment(self):
            self.count += 1
            return self.count

    print("Closure implementation:")
    counter_closure = make_counter_closure(5)
    print(f"  {counter_closure()}")
    print(f"  {counter_closure()}")

    print("\nClass implementation:")
    counter_class = CounterClass(5)
    print(f"  {counter_class.increment()}")
    print(f"  {counter_class.increment()}")

    print("\nBoth achieve the same result!")

    # ============================================================================
    # EXAMPLE 11: Closures in Loops (Common Pitfall and Solution)
    # ============================================================================
    print("\n\n11. CLOSURES IN LOOPS (PITFALL AND SOLUTION)")
    print("-" * 70)

    # WRONG WAY
    print("❌ Common mistake:")
    def create_multipliers_wrong():
        multipliers = []
        for i in range(5):
            multipliers.append(lambda x: x * i)
        return multipliers

    funcs_wrong = create_multipliers_wrong()
    print(f"  Expected: 0 * 2 = 0, Got: {funcs_wrong[0](2)}")
    print(f"  Expected: 1 * 2 = 2, Got: {funcs_wrong[1](2)}")
    print("  All closures reference the same 'i', which is 4 after the loop!")

    # RIGHT WAY - Solution 1: Default argument
    print("\n✅ Solution 1: Default argument:")
    def create_multipliers_correct1():
        multipliers = []
        for i in range(5):
            multipliers.append(lambda x, i=i: x * i)  # Capture current i
        return multipliers

    funcs_correct1 = create_multipliers_correct1()
    print(f"  0 * 2 = {funcs_correct1[0](2)}")
    print(f"  1 * 2 = {funcs_correct1[1](2)}")
    print(f"  2 * 2 = {funcs_correct1[2](2)}")

    # RIGHT WAY - Solution 2: Factory function
    print("\n✅ Solution 2: Factory function:")
    def make_multiplier(i):
        return lambda x: x * i

    def create_multipliers_correct2():
        return [make_multiplier(i) for i in range(5)]

    funcs_correct2 = create_multipliers_correct2()
    print(f"  0 * 2 = {funcs_correct2[0](2)}")
    print(f"  1 * 2 = {funcs_correct2[1](2)}")
    print(f"  2 * 2 = {funcs_correct2[2](2)}")

    # ============================================================================
    # EXAMPLE 12: Memoization Using Closures
    # ============================================================================
    print("\n\n12. MEMOIZATION USING CLOSURES")
    print("-" * 70)

    def make_memoized(func):
        cache = {}

        def memoized(*args):
            if args in cache:
                print(f"  💾 Cache hit for {args}")
                return cache[args]
            print(f"  🔄 Computing for {args}")
            result = func(*args)
            cache[args] = result
            return result

        return memoized

    @make_memoized
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n-1) + fibonacci(n-2)

    print("Calculating fibonacci(5):")
    result = fibonacci(5)
    print(f"Result: {result}")

    print("\nCalculating fibonacci(5) again:")
    result = fibonacci(5)
    print(f"Result: {result}")

    # ============================================================================
    # EXAMPLE 13: Partial Function Application
    # ============================================================================
    print("\n\n13. PARTIAL FUNCTION APPLICATION")
    print("-" * 70)

    def partial(func, *fixed_args, **fixed_kwargs):
        def wrapper(*args, **kwargs):
            return func(*fixed_args, *args, **fixed_kwargs, **kwargs)
        return wrapper

    def greet(greeting, name, punctuation="!"):
        return f"{greeting}, {name}{punctuation}"

    # Create specialized greeting functions
    say_hello = partial(greet, "Hello")
    say_goodbye = partial(greet, "Goodbye")
    say_hi_excited = partial(greet, "Hi", punctuation="!!!")

    print(say_hello("Alice"))
    print(say_goodbye("Bob"))
    print(say_hi_excited("Charlie"))

    # ============================================================================
    # EXAMPLE 14: Function Composition
    # ============================================================================
    print("\n\n14. FUNCTION COMPOSITION")
    print("-" * 70)

    def compose(f, g):
        def composed(x):
            return f(g(x))
        return composed

    def add_10(x):
        return x + 10

    def multiply_2(x):
        return x * 2

    def square(x):
        return x ** 2

    # Create composed functions
    add_then_multiply = compose(multiply_2, add_10)
    multiply_then_square = compose(square, multiply_2)

    x = 5
    print(f"Input: {x}")
    print(f"Add 10, then multiply by 2: {add_then_multiply(x)}")  # (5+10)*2 = 30
    print(f"Multiply by 2, then square: {multiply_then_square(x)}")  # (5*2)^2 = 100

    # ============================================================================
    # EXAMPLE 15: Stateful Generators with Closures
    # ============================================================================
    print("\n\n15. STATEFUL GENERATORS WITH CLOSURES")
    print("-" * 70)

    def make_id_generator(prefix="ID"):
        counter = 0

        def generate_id():
            nonlocal counter
            counter += 1
            return f"{prefix}-{counter:04d}"

        return generate_id

    user_id = make_id_generator("USER")
    order_id = make_id_generator("ORDER")

    print("Generating user IDs:")
    for _ in range(3):
        print(f"  {user_id()}")

    print("\nGenerating order IDs:")
    for _ in range(3):
        print(f"  {order_id()}")

    print("\n" + "=" * 70)
    print("END OF EXAMPLES")
    print("=" * 70)
```

---

## Exercises


**Exercise 1.**
Write a function `make_greeting(greeting)` that returns a closure. The closure should take a `name` parameter and return the string `f"{greeting}, {name}!"`. For example, `hello = make_greeting("Hello")` followed by `hello("Alice")` should return `"Hello, Alice!"`.

??? success "Solution to Exercise 1"

        ```python
        def make_greeting(greeting):
            def greet(name):
                return f"{greeting}, {name}!"
            return greet

        hello = make_greeting("Hello")
        print(hello("Alice"))  # Hello, Alice!
        print(hello("Bob"))    # Hello, Bob!

        hi = make_greeting("Hi")
        print(hi("Carol"))     # Hi, Carol!
        ```

    The inner function `greet` captures `greeting` from the enclosing scope. Each call to `make_greeting` creates a new closure with its own captured value.

---

**Exercise 2.**
Write a function `make_accumulator(initial=0)` that returns a closure. Each time the closure is called with a number, it adds that number to a running total and returns the new total. Use the `nonlocal` keyword.

??? success "Solution to Exercise 2"

        ```python
        def make_accumulator(initial=0):
            total = initial
            def add(n):
                nonlocal total
                total += n
                return total
            return add

        acc = make_accumulator()
        print(acc(5))    # 5
        print(acc(10))   # 15
        print(acc(3))    # 18

        acc2 = make_accumulator(100)
        print(acc2(1))   # 101
        ```

    `nonlocal total` allows the inner function to modify `total` in the enclosing scope. Each accumulator maintains its own independent total.

---

**Exercise 3.**
Inspect the closure created by `make_greeting("Hi")` from Exercise 1. Print the `__closure__` attribute and access the captured value using `cell_contents`. Verify that it holds the string `"Hi"`.

??? success "Solution to Exercise 3"

        ```python
        def make_greeting(greeting):
            def greet(name):
                return f"{greeting}, {name}!"
            return greet

        hi = make_greeting("Hi")

        print(hi.__closure__)                     # (<cell at 0x...>,)
        print(hi.__closure__[0].cell_contents)    # Hi
        ```

    The `__closure__` attribute is a tuple of cell objects, one for each captured variable. `cell_contents` reveals the actual captured value.
