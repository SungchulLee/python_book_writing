# Python Decorators - Quick Reference Cheat Sheet

!!! tip "Mental Model"
    Decorators are function transformers: they take a function in, add behavior, and return a new function out. Every pattern on this page is a variation of that single idea -- the differences are in what gets wrapped (functions vs. classes) and how the wrapper is configured (plain decorator vs. factory).

## Basic Syntax

### Simple Decorator
```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        # Do something before
        result = func(*args, **kwargs)
        # Do something after
        return result
    return wrapper

@my_decorator
def my_function():
    pass
```

### With functools.wraps (ALWAYS USE THIS!)
```python
from functools import wraps

def my_decorator(func):
    @wraps(func)  # Preserves function metadata
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

## Decorator Patterns

### 1. Basic Decorator Template
```python
from functools import wraps

def decorator_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Before function execution
        result = func(*args, **kwargs)
        # After function execution
        return result
    return wrapper
```

### 2. Decorator with Parameters
```python
def decorator_with_params(param1, param2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Use param1, param2
            return func(*args, **kwargs)
        return wrapper
    return decorator

@decorator_with_params("value1", "value2")
def my_function():
    pass
```

### 3. Class-Based Decorator
```python
from functools import update_wrapper

class MyDecorator:
    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func
    
    def __call__(self, *args, **kwargs):
        # Your logic here
        return self.func(*args, **kwargs)

@MyDecorator
def my_function():
    pass
```

## Common Use Cases

### Timing
```python
import time

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end-start:.4f}s")
        return result
    return wrapper
```

### Logging
```python
def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper
```

### Debug
```python
def debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result
    return wrapper
```

### Caching/Memoization
```python
def memoize(func):
    cache = {}
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

# Or use built-in:
from functools import lru_cache

@lru_cache(maxsize=128)
def my_function(n):
    pass
```

### Exception Handling
```python
def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
            return None
    return wrapper
```

### Retry Logic
```python
def retry(max_attempts=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Retry {attempt + 1}/{max_attempts}")
        return wrapper
    return decorator
```

### Validation
```python
def validate_positive(func):
    @wraps(func)
    def wrapper(n):
        if n < 0:
            raise ValueError("Must be positive")
        return func(n)
    return wrapper

def validate_type(expected_type):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not isinstance(args[0], expected_type):
                raise TypeError(f"Expected {expected_type}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### Rate Limiting
```python
import time

def rate_limit(max_calls, time_period):
    def decorator(func):
        calls = []
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [t for t in calls if now - t < time_period]
            if len(calls) >= max_calls:
                return None
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### Authentication
```python
def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            raise PermissionError("Not authenticated")
        return func(*args, **kwargs)
    return wrapper

def require_role(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if user_role != role:
                raise PermissionError(f"Requires {role}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## Stacking Decorators

```python
@decorator1
@decorator2
@decorator3
def my_function():
    pass

# Equivalent to:
# my_function = decorator1(decorator2(decorator3(my_function)))
```

**Important**: Decorators are applied bottom-to-top!

### Example
```python
def uppercase(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

def exclaim(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) + "!"
    return wrapper

@uppercase  # Applied SECOND
@exclaim    # Applied FIRST
def greet():
    return "hello"

greet()  # Returns "HELLO!"
```

## Built-in Decorators

### @property
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Negative radius")
        self._radius = value
    
    @property
    def area(self):
        return 3.14159 * self._radius ** 2

c = Circle(5)
print(c.radius)  # Access like attribute
c.radius = 10    # Use setter
print(c.area)    # Computed property
```

### @staticmethod
```python
class MyClass:
    @staticmethod
    def static_method():
        # No access to self or cls
        return "Static!"

MyClass.static_method()  # Can call without instance
```

### @classmethod
```python
class MyClass:
    count = 0
    
    @classmethod
    def increment(cls):
        cls.count += 1

MyClass.increment()  # Access class variables
```

### @functools.lru_cache
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

## Best Practices

### ✅ DO:
- Use `@wraps` to preserve function metadata
- Use `*args, **kwargs` for flexibility
- Keep decorators simple and focused
- Document what decorators do
- Consider using built-in decorators when available

### ❌ DON'T:
- Forget to return the wrapper function
- Modify the original function
- Make decorators too complex
- Use decorators for core business logic
- Stack too many decorators (hard to debug)

## Common Patterns Summary

| Pattern | Use Case | Complexity |
|---------|----------|------------|
| Simple wrapper | Add behavior before/after | Easy |
| With parameters | Configurable behavior | Medium |
| Class-based | Need state/attributes | Medium |
| Stacked | Multiple behaviors | Easy |
| Memoization | Cache expensive calls | Easy |
| Timing | Performance monitoring | Easy |
| Validation | Input checking | Easy |
| Retry | Handle transient failures | Medium |
| Rate limiting | Control call frequency | Hard |

## Quick Tips

1. **Debugging**: Decorated functions can be hard to debug - use simple decorators
2. **Performance**: Each decorator adds overhead - use sparingly
3. **Order matters**: When stacking, decorators apply bottom-to-top
4. **Testing**: Test both the decorator and decorated function
5. **Documentation**: Always document what your decorator does

## Common Mistakes

```python
# ❌ Forgetting to return wrapper
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    # Missing: return wrapper

# ❌ Not using *args, **kwargs
def bad_decorator(func):
    def wrapper():  # Won't work with arguments!
        return func()
    return wrapper

# ❌ Not using @wraps
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper  # Loses func.__name__, __doc__, etc.

# ✅ Correct pattern
from functools import wraps

def good_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

## Real-World Examples

```python
# Flask route decorator
@app.route('/users/<id>')
def get_user(id):
    pass

# Django login required
@login_required
def profile(request):
    pass

# pytest fixture
@pytest.fixture
def database():
    pass

# Click CLI command
@click.command()
def hello():
    pass
```

---

**Remember**: Decorators are syntactic sugar for function wrapping. Master the basics before creating complex decorators!
---

## Runnable Example: `singledispatch_example.py`

```python
"""
TUTORIAL: Single Dispatch - Type-Based Function Polymorphism

This tutorial covers functools.singledispatch, a powerful decorator that enables
FUNCTION OVERLOADING based on the type of the first argument.

The Problem: In Python, we often need to handle the same operation differently
depending on the type of data. You could write a giant if/elif/else chain, but
that's ugly and hard to extend.

The Solution: @singledispatch lets you define a generic function, then register
type-specific implementations. When called, Python automatically dispatches to
the right implementation based on the argument type.

This is elegant, extensible, and Pythonic. The htmlize function demonstrates
this perfectly - one function that handles strings, lists, numbers, fractions,
and more, each with custom formatting.
"""

from functools import singledispatch
from collections import abc
import fractions
import decimal
import html
import numbers

if __name__ == "__main__":

    print("=" * 70)
    print("TUTORIAL: Single Dispatch - Type-Based Function Polymorphism")
    print("=" * 70)

    # ============ EXAMPLE 1: The Problem Without Singledispatch
    print("\n# ============ EXAMPLE 1: The Problem Without Singledispatch")
    print("Why we need singledispatch - handling multiple types with if/elif:\n")


    def htmlize_bad(obj):
        """Convert any object to HTML - WITHOUT singledispatch"""
        if isinstance(obj, str):
            # For strings, escape HTML and preserve newlines
            content = html.escape(obj).replace('\n', '<br/>\n')
            return f'<p>{content}</p>'
        elif isinstance(obj, abc.Sequence):
            # For sequences, create a list with each item htmlized
            inner = '</li>\n<li>'.join(htmlize_bad(item) for item in obj)
            return '<ul>\n<li>' + inner + '</li>\n</ul>'
        elif isinstance(obj, numbers.Integral):
            # For integers, show decimal and hex
            return f'<pre>{obj} (0x{obj:x})</pre>'
        else:
            # Default: escape the repr
            content = html.escape(repr(obj))
            return f'<pre>{content}</pre>'


    print("The bad approach - giant if/elif chain:")
    print("Problems:")
    print("  1. Hard to read - all cases mixed together")
    print("  2. Hard to extend - must modify the function itself")
    print("  3. Couples types together - adding a new type means rewriting the function")
    print("  4. No way for external code to add handlers")

    print("\nTest the bad version:")
    test_str = 'Hello\nWorld'
    print(f"htmlize_bad('Hello\\nWorld') = {htmlize_bad(test_str)}")
    test_list = [1, 2, 3]
    print(f"htmlize_bad([1, 2, 3]) = {htmlize_bad(test_list)}")
    print(f"htmlize_bad(42) = {htmlize_bad(42)}")

    # ============ EXAMPLE 2: Introduction to Singledispatch
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 2: Introduction to Singledispatch")
    print("The elegant solution - using @singledispatch:\n")

    print("""
    @singledispatch CREATES POLYMORPHIC FUNCTIONS

    Steps:
    1. Define a generic function with @singledispatch decorator
    2. Register type-specific implementations with @func.register
    3. When called, Python dispatches to the right implementation
    4. Much cleaner than if/elif chains!

    BENEFITS:
    - Each type's logic is separate and focused
    - Easy to add new types - just register them
    - Extensible - external code can register new types
    - Pythonic and elegant
    - Type specialization is clear and explicit
    """)


    # ============ EXAMPLE 3: Basic Singledispatch Example
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 3: Basic Singledispatch Example")
    print("Building htmlize step-by-step with singledispatch:\n")


    @singledispatch
    def htmlize(obj: object) -> str:
        """
        Generic function to convert any object to HTML.
        This is the BASE implementation - handles unknown types.
        """
        # For unknown types, just escape the repr
        content = html.escape(repr(obj))
        return f'<pre>{content}</pre>'


    print("Step 1: Define the generic base function")
    print(f"htmlize(42) = {htmlize(42)}")
    print(f"htmlize({{1, 2, 3}}) = {htmlize({1, 2, 3})}")


    @htmlize.register(str)
    def _(text: str) -> str:
        """Specialized handler for strings"""
        content = html.escape(text).replace('\n', '<br/>\n')
        return f'<p>{content}</p>'


    print("\nStep 2: Register a handler for str")
    print(f"htmlize('Hello') = {htmlize('Hello')}")
    hello_world = 'Hello\nWorld'
    print(f"htmlize('Hello\\nWorld') = {htmlize(hello_world)}")


    @htmlize.register(abc.Sequence)
    def _(seq: abc.Sequence) -> str:
        """Specialized handler for sequences (lists, tuples, etc.)"""
        inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
        return '<ul>\n<li>' + inner + '</li>\n</ul>'


    print("\nStep 3: Register a handler for Sequence")
    print(f"htmlize([1, 2, 3]) = {htmlize([1, 2, 3])}")
    print(f"htmlize(('a', 'b')) = {htmlize(('a', 'b'))}")


    @htmlize.register(numbers.Integral)
    def _(n: numbers.Integral) -> str:
        """Specialized handler for integers"""
        return f'<pre>{n} (0x{n:x})</pre>'


    print("\nStep 4: Register a handler for Integral")
    print(f"htmlize(42) = {htmlize(42)}")
    print(f"htmlize(255) = {htmlize(255)}")

    # ============ EXAMPLE 4: Handling Boolean Special Case
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 4: Handling Boolean Special Case")
    print("Important: bool is a subtype of int, handle it separately:\n")

    print("""
    GOTCHA: In Python, bool is a subclass of int!
      isinstance(True, int) -> True
      isinstance(True, bool) -> True

    If you don't register bool, it will use the int handler:
      htmlize(True) -> '<pre>1 (0x1)</pre>'  <- WRONG!

    Solution: Register bool specifically, it takes precedence.
    """)


    @htmlize.register(bool)
    def _(b: bool) -> str:
        """Specialized handler for booleans (registered AFTER int handler)"""
        return f'<pre>{b}</pre>'


    print("Testing boolean handler:")
    print(f"htmlize(True) = {htmlize(True)}")
    print(f"htmlize(False) = {htmlize(False)}")
    print(f"htmlize(42) = {htmlize(42)}")
    print("Note: bool handler takes precedence over int handler!")

    # ============ EXAMPLE 5: Registering With Explicit Types
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 5: Registering With Explicit Types")
    print("Alternative syntax using explicit type arguments:\n")

    print("""
    TWO WAYS TO REGISTER:

    Method 1 (type annotation in function signature):
      @htmlize.register(str)
      def _(text: str) -> str:
          ...

    Method 2 (explicit type as argument):
      @htmlize.register(fractions.Fraction)
      def _(x) -> str:
          ...

    Both work! Use whichever is clearer.
    """)


    @htmlize.register(fractions.Fraction)
    def _(x) -> str:
        """Specialized handler for fractions"""
        frac = fractions.Fraction(x)
        return f'<pre>{frac.numerator}/{frac.denominator}</pre>'


    print("Testing fraction handler:")
    result = htmlize(fractions.Fraction(2, 3))
    print(f"htmlize(Fraction(2, 3)) = {result}")

    # ============ EXAMPLE 6: Registering Multiple Types to Same Handler
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 6: Registering Multiple Types to Same Handler")
    print("Decorating one handler for multiple types:\n")

    print("""
    Sometimes you want the SAME handler for multiple types.
    You can stack @register decorators on a single function.

    Example: float and decimal.Decimal should both show with fractions
    """)


    @htmlize.register(decimal.Decimal)
    @htmlize.register(float)
    def _(x) -> str:
        """Specialized handler for floats and decimals"""
        frac = fractions.Fraction(x).limit_denominator()
        return f'<pre>{x} ({frac.numerator}/{frac.denominator})</pre>'


    print("Testing float and decimal handlers:")
    print(f"htmlize(2/3) = {htmlize(2/3)}")
    print(f"htmlize(0.6666666666666666) = {htmlize(0.6666666666666666)}")
    print(f"htmlize(Decimal('0.02380952')) = {htmlize(decimal.Decimal('0.02380952'))}")

    # ============ EXAMPLE 7: Complete htmlize Example
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 7: Complete htmlize Example")
    print("Using the complete htmlize function:\n")

    examples = [
        42,
        'Hello & goodbye',
        ['apple', 10, {3, 2, 1}],
        True,
        fractions.Fraction(2, 3),
        2/3,
        decimal.Decimal('0.02380952'),
        {1, 2, 3},
    ]

    print("Testing htmlize with various types:\n")
    for obj in examples:
        result = htmlize(obj)
        print(f"htmlize({obj!r})")
        print(f"  -> {result}\n")

    # ============ EXAMPLE 8: Understanding Dispatch Rules
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 8: Understanding Dispatch Rules")
    print("How Python decides which handler to call:\n")

    print("""
    DISPATCH ALGORITHM:
    1. Check the type of the first argument
    2. If exact match in registered types, use that handler
    3. Otherwise, check the MRO (Method Resolution Order)
    4. Use the most specific handler in the MRO
    5. If no match, use the @singledispatch base function

    EXAMPLE MRO FOR bool:
      bool -> int -> numbers.Integral -> numbers.Number -> object

    If you register handlers for:
      - bool: calls bool handler
      - int: calls int handler (if bool not registered)
      - numbers.Integral: calls Integral handler (if bool/int not registered)
      - object: calls base handler (default)

    WHY THIS MATTERS:
    Register specific types AFTER general types. The most specific handler wins.
    But the order of decorator application doesn't matter - dispatch is by type.
    """)

    # ============ EXAMPLE 9: Introspection - Exploring Registered Types
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 9: Introspection - Exploring Registered Types")
    print("Discovering what types are registered:\n")

    print("The dispatch registry is accessible as htmlize.registry:")
    print(f"Type(s): {type(htmlize.registry)}")
    print(f"Registered types: {list(htmlize.registry.keys())}")

    print("\nFor each type, you can get the handler:")
    print(f"Handler for str: {htmlize.register(str)}")
    print(f"Handler for list: {htmlize.register(abc.Sequence)}")

    print("\nCheck if a type has a handler:")
    print(f"str in registry: {str in htmlize.registry}")
    print(f"int in registry: {int in htmlize.registry}")

    # ============ EXAMPLE 10: Real-World Use Case - Data Serialization
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 10: Real-World Use Case - Data Serialization")
    print("Using singledispatch for type-based serialization:\n")


    @singledispatch
    def serialize(obj):
        """Serialize any Python object to a JSON-compatible format"""
        raise TypeError(f"Cannot serialize {type(obj).__name__}")


    @serialize.register(str)
    def _(s: str):
        return s


    @serialize.register(int)
    def _(i: int):
        return i


    @serialize.register(float)
    def _(f: float):
        return f


    @serialize.register(list)
    def _(lst: list):
        return [serialize(item) for item in lst]


    @serialize.register(dict)
    def _(d: dict):
        return {k: serialize(v) for k, v in d.items()}


    @serialize.register(tuple)
    def _(t: tuple):
        return [serialize(item) for item in t]


    print("Serialization examples:")
    data = {
        'name': 'Alice',
        'age': 30,
        'scores': [85.5, 92.0, 78.5],
        'tags': ('python', 'programming'),
    }

    print(f"Original: {data}")
    result = serialize(data)
    print(f"Serialized: {result}")

    # ============ EXAMPLE 11: When to Use Singledispatch
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 11: When to Use Singledispatch")
    print("Best practices and patterns:\n")

    print("""
    WHEN TO USE @singledispatch:

    ✓ When you need type-based behavior variation
      - Different processing for different types
      - Format, convert, validate based on type

    ✓ When you want clean, extensible code
      - Add new types without modifying existing code
      - Each type handler is self-contained
      - External code can register new types

    ✓ When you need to avoid if/elif chains
      - More Pythonic and readable
      - Type specialization is explicit

    EXAMPLES:
    - Format/serialize different types differently
    - Visitor pattern without visitor classes
    - Type-specific validation
    - Rendering/display by type
    - Database operations by type


    WHEN NOT TO USE:

    ✗ When you need multiple dispatch (multiple argument types matter)
      - Use multipledispatch library instead
      - Or use method dispatch on an object

    ✗ When a simple isinstance check is sufficient
      - If you only handle 2-3 types, if/else might be clearer

    ✗ When you need class method dispatch
      - Use @functools.singledispatchmethod instead (Python 3.8+)

    CAUTION: singledispatch dispatches on FIRST ARGUMENT ONLY
    If you need to dispatch on other arguments, use multipledispatch or another pattern.
    """)

    # ============ EXAMPLE 12: Common Gotchas
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 12: Common Gotchas")
    print("Things to watch out for:\n")

    print("""
    GOTCHA 1: Order of registration matters for subtypes
      bool is a subclass of int. Register bool AFTER int for correct dispatch.

    GOTCHA 2: Only the first argument is checked
      @singledispatch only looks at type of first argument.
      For other arguments, use isinstance checks inside the handler.

    GOTCHA 3: Non-registered types don't error by default
      They use the base @singledispatch function.
      If you want strict typing, raise TypeError in the base function.

    GOTCHA 4: Registering abstract types catches subtypes
      @htmlize.register(abc.Sequence) catches list, tuple, str, etc.
      This is powerful but can be surprising!

    GOTCHA 5: Can't override a registered type at runtime
      Once registered, the handler is locked in.
      You can't change it or unregister it.
      (Well, you can access registry.register() but it's not recommended)
    """)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    KEY TAKEAWAYS:

    1. @singledispatch ENABLES TYPE-BASED FUNCTION POLYMORPHISM
       One generic function, multiple type-specific implementations.

    2. BASIC PATTERN:
       @singledispatch
       def func(obj): ...          # Generic implementation

       @func.register(TypeA)
       def _(obj: TypeA): ...      # Type-specific handler A

       @func.register(TypeB)
       def _(obj: TypeB): ...      # Type-specific handler B

    3. DISPATCH RULES:
       - Check exact type match first
       - If not found, check MRO (Method Resolution Order)
       - Use most specific match
       - Fall back to base @singledispatch if no match

    4. BENEFITS:
       - Cleaner than if/elif chains
       - Extensible - add types without modifying function
       - Type specialization is explicit and clear
       - Pythonic and elegant

    5. IMPORTANT POINTS:
       - Only first argument is checked
       - All type handlers are separate functions
       - Subtypes are handled via MRO
       - Order matters for subtypes (e.g., bool vs int)
       - Use @func.register(Type) or type annotations

    6. PRACTICAL USES:
       - Format/serialize by type
       - Render/display by type
       - Validate by type
       - Process data differently per type
       - Extensible visitor patterns

    7. WHEN TO USE:
       - Type-based behavior variation
       - Want clean, extensible code
       - Avoiding complex if/elif chains
    """)
```

---

## Runnable Example: `function_registration_pattern.py`

```python
"""
TUTORIAL: Function Registration Pattern with Decorators

This tutorial covers the FUNCTION REGISTRATION PATTERN, a powerful way to use
decorators to dynamically build a registry of functions.

The Idea: You want to collect multiple functions into a central list or dict,
often for callbacks, plugins, or dispatch. Instead of manually maintaining the
registry, use a decorator to automatically register functions as they're defined.

The Pattern: When a function is decorated with @register, it's added to a
registry list/dict, then returned unchanged so it can still be called normally.

This is the foundation of plugin systems, event dispatchers, and dynamic dispatch
mechanisms. It's elegant because the registry is built naturally as the code runs.
"""

if __name__ == "__main__":

    print("=" * 70)
    print("TUTORIAL: Function Registration Pattern with Decorators")
    print("=" * 70)

    # ============ EXAMPLE 1: The Basic Registration Pattern
    print("\n# ============ EXAMPLE 1: The Basic Registration Pattern")
    print("The simplest registration decorator:\n")

    # Create a registry list to hold functions
    registry = []


    def register(func):
        """Decorator that registers a function in the registry"""
        print(f"running register({func.__name__})")
        registry.append(func)  # Add the function to the registry
        return func  # Return the function unchanged


    print("Define the registry and register decorator:")
    print(f"registry = {registry}")
    print()

    # Now define some functions using the @register decorator
    @register
    def f1():
        """First registered function"""
        print("running f1()")


    @register
    def f2():
        """Second registered function"""
        print("running f2()")


    def f3():
        """Not registered - no @register decorator"""
        print("running f3()")


    print("\nFunctions have been defined. Check the registry:")
    print(f"registry = {registry}")
    print(f"registry[0].__name__ = {registry[0].__name__}")
    print(f"registry[1].__name__ = {registry[1].__name__}")
    print("\nNotice: f3 is NOT in the registry (no @register decorator)")

    # ============ EXAMPLE 2: Using the Registered Functions
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 2: Using the Registered Functions")
    print("Call registered and non-registered functions:\n")

    print("Calling f1() directly:")
    f1()

    print("\nCalling f2() directly:")
    f2()

    print("\nCalling f3() directly (not registered):")
    f3()

    print("\nCalling all registered functions via the registry:")
    for func in registry:
        func()

    # ============ EXAMPLE 3: Understanding How Registration Works
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 3: Understanding How Registration Works")
    print("Step-by-step breakdown of what happens:\n")

    print("""
    WHEN YOU WRITE:

        @register
        def f1():
            print('running f1()')

    PYTHON DOES THIS:

        1. Define the function f1
        2. Call register(f1) <- decorator is applied
        3. Assign the return value back to f1

    INSIDE register():
        1. func = f1 (the function object)
        2. print(f'running register({func})') <- debug message
        3. registry.append(func) <- ADD TO REGISTRY
        4. return func <- return unchanged

    RESULT:
        - f1 is in the registry
        - f1 variable still points to the function
        - f1 can be called normally
        - It's also in the registry for batch operations
    """)

    # ============ EXAMPLE 4: Registry as a Dictionary
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 4: Registry as a Dictionary")
    print("Use a dict registry instead of list for named lookups:\n")

    # Create a dict registry
    command_registry = {}


    def register_command(func):
        """Register a function as a command by its name"""
        name = func.__name__
        print(f"Registering command: {name}")
        command_registry[name] = func
        return func


    @register_command
    def save():
        """Save current data"""
        print("Saving data...")


    @register_command
    def load():
        """Load data from disk"""
        print("Loading data...")


    @register_command
    def exit_program():
        """Exit the program"""
        print("Exiting...")


    print("Registered commands:")
    for name in command_registry:
        print(f"  {name}")

    print("\nCall a command by name:")
    command_registry['save']()

    print("\nCall all commands:")
    for name, cmd in command_registry.items():
        print(f"Calling {name}():")
        cmd()

    # ============ EXAMPLE 5: Real-World Example - Event Dispatcher
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 5: Real-World Example - Event Dispatcher")
    print("An event system where handlers register for specific events:\n")


    class EventDispatcher:
        """Simple event dispatcher with registered handlers"""

        def __init__(self):
            self.handlers = {}  # event_name -> list of handler functions

        def register_handler(self, event_name):
            """Decorator to register a handler for an event"""
            def decorator(func):
                if event_name not in self.handlers:
                    self.handlers[event_name] = []
                print(f"Registering {func.__name__} for event '{event_name}'")
                self.handlers[event_name].append(func)
                return func
            return decorator

        def emit(self, event_name, *args, **kwargs):
            """Trigger an event and call all registered handlers"""
            if event_name not in self.handlers:
                print(f"No handlers for event: {event_name}")
                return

            for handler in self.handlers[event_name]:
                handler(*args, **kwargs)


    # Create a dispatcher
    dispatcher = EventDispatcher()

    # Register handlers for 'user_login' event
    @dispatcher.register_handler('user_login')
    def log_login(username):
        print(f"  LOG: User {username} logged in")


    @dispatcher.register_handler('user_login')
    def send_welcome_email(username):
        print(f"  EMAIL: Sending welcome email to {username}")


    @dispatcher.register_handler('user_login')
    def update_last_seen(username):
        print(f"  DB: Updating last_seen for {username}")


    # Register handlers for 'user_logout' event
    @dispatcher.register_handler('user_logout')
    def log_logout(username):
        print(f"  LOG: User {username} logged out")


    print("\nDispatcher handlers registered:")
    for event, handlers in dispatcher.handlers.items():
        print(f"  {event}: {len(handlers)} handlers")

    print("\nEmitting 'user_login' event:")
    dispatcher.emit('user_login', 'alice')

    print("\nEmitting 'user_logout' event:")
    dispatcher.emit('user_logout', 'alice')

    # ============ EXAMPLE 6: Plugin System Pattern
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 6: Plugin System Pattern")
    print("Using registration for a simple plugin system:\n")


    class PluginRegistry:
        """Registry for plugins that process different file types"""

        def __init__(self):
            self.plugins = {}  # file_extension -> processor function

        def register(self, *extensions):
            """Decorator to register a plugin for file extensions"""
            def decorator(func):
                for ext in extensions:
                    print(f"Registering {func.__name__} for .{ext} files")
                    self.plugins[ext] = func
                return func
            return decorator

        def process(self, filename):
            """Process a file using the appropriate plugin"""
            # Extract file extension
            if '.' not in filename:
                print(f"No extension for file: {filename}")
                return

            ext = filename.split('.')[-1]

            if ext not in self.plugins:
                print(f"No processor for .{ext} files")
                return

            processor = self.plugins[ext]
            processor(filename)


    # Create a plugin registry
    plugins = PluginRegistry()


    @plugins.register('txt')
    def process_text(filename):
        print(f"Processing text file: {filename}")


    @plugins.register('jpg', 'jpeg', 'png')
    def process_image(filename):
        print(f"Processing image file: {filename}")


    @plugins.register('py')
    def process_python(filename):
        print(f"Processing Python file: {filename}")


    print("\nRegistered file processors:")
    for ext, processor in plugins.plugins.items():
        print(f"  .{ext} -> {processor.__name__}")

    print("\nProcessing various files:")
    plugins.process('document.txt')
    plugins.process('photo.jpg')
    plugins.process('script.py')
    plugins.process('backup.zip')  # No processor

    # ============ EXAMPLE 7: Comparison - Manual vs Registration Pattern
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 7: Comparison - Manual vs Registration Pattern")
    print("Why the registration pattern is better:\n")

    print("""
    MANUAL APPROACH (without registration):

    def process_files(files):
        processors = [
            process_txt,
            process_json,
            process_csv,
            # Must remember to add every processor here
            # Hard to extend from other modules
        ]
        for file in files:
            # Check type and call processor
            ...

    PROBLEMS:
    - Central list must be manually maintained
    - Hard to extend without modifying this function
    - Couples all processors together
    - External modules can't register processors


    REGISTRATION PATTERN:

    @register
    def process_txt():
        ...

    @register
    def process_json():
        ...

    # External module can do:
    @register
    def process_csv():
        ...

    BENEFITS:
    - Processors register themselves as they're defined
    - Easy to extend - just add @register
    - No central coupling
    - Each processor is independent
    - Works great with plugins from external modules
    """)

    # ============ EXAMPLE 8: Registration with Validation
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 8: Registration with Validation")
    print("Add validation/requirements to registration:\n")


    class ValidatedRegistry:
        """Registry that validates handlers before registration"""

        def __init__(self):
            self.handlers = {}

        def register(self, **requirements):
            """
            Decorator that registers with validation.
            Usage: @register(priority=1, required=True)
            """
            def decorator(func):
                # Validate the function
                if not callable(func):
                    raise ValueError(f"{func} is not callable")

                name = func.__name__
                meta = {'function': func, **requirements}

                print(f"Registering {name} with {requirements}")
                self.handlers[name] = meta
                return func

            return decorator

        def call_handler(self, name, *args, **kwargs):
            """Call a registered handler by name"""
            if name not in self.handlers:
                raise KeyError(f"Handler {name} not registered")

            handler = self.handlers[name]['function']
            return handler(*args, **kwargs)


    validated_registry = ValidatedRegistry()


    @validated_registry.register(priority=1, required=True)
    def database_check():
        print("  Checking database...")


    @validated_registry.register(priority=2)
    def cache_check():
        print("  Checking cache...")


    print("\nRegistered handlers with metadata:")
    for name, meta in validated_registry.handlers.items():
        print(f"  {name}: priority={meta.get('priority')}, "
              f"required={meta.get('required')}")

    print("\nCalling handlers:")
    validated_registry.call_handler('database_check')
    validated_registry.call_handler('cache_check')

    # ============ EXAMPLE 9: Decorator Chaining
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 9: Decorator Chaining")
    print("Combine registration with other decorators:\n")

    import time


    call_log = []


    def log_calls(func):
        """Decorator that logs when a function is called"""
        def wrapper(*args, **kwargs):
            print(f"  LOG: Calling {func.__name__}")
            result = func(*args, **kwargs)
            call_log.append(func.__name__)
            return result
        return wrapper


    def time_calls(func):
        """Decorator that times function execution"""
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            print(f"  TIME: {func.__name__} took {elapsed:.4f}s")
            return result
        return wrapper


    timed_registry = []


    def register_timed(func):
        """Register and apply timing decorator"""
        print(f"Registering {func.__name__}")
        timed_registry.append(func)
        return func


    @register_timed
    @time_calls
    @log_calls
    def operation_a():
        time.sleep(0.01)
        print("    Operation A complete")


    @register_timed
    @time_calls
    @log_calls
    def operation_b():
        time.sleep(0.02)
        print("    Operation B complete")


    print("\nRunning registered operations:")
    for op in timed_registry:
        op()

    print(f"\nAll operations called: {call_log}")

    # ============ EXAMPLE 10: Common Use Cases
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 10: Common Use Cases")
    print("Where the registration pattern shines:\n")

    print("""
    COMMON USE CASES:

    1. PLUGIN SYSTEMS
       - Plugins register themselves at import time
       - Main app calls all registered plugins
       - Easy to add/remove plugins

    2. EVENT SYSTEMS
       - Register handlers for events
       - When event occurs, call all handlers
       - Multiple handlers per event

    3. COMMAND DISPATCHERS
       - Commands register by name
       - Main loop dispatches to command by name
       - Easy to add new commands

    4. TESTING FRAMEWORKS
       - Test functions register themselves
       - Test runner discovers and runs all tests
       - No need to manually list tests

    5. API ENDPOINTS
       - Routes register themselves as they're defined
       - Server builds routing table automatically
       - Similar to Flask @app.route()

    6. PROTOCOL HANDLERS
       - Different handlers for different data types
       - Each handler registers for its type(s)
       - Extensible dispatch system

    7. MIDDLEWARE CHAINS
       - Middleware registers itself in order
       - Request passes through all middleware
       - Easy to add/remove middleware


    KEY PATTERN:

    1. Create a registry (list or dict)
    2. Define a register decorator that:
       - Adds function to registry
       - Optionally validates
       - Returns function unchanged
    3. Use @register on functions you want to collect
    4. Execute or dispatch to registered functions as needed
    """)

    # ============ EXAMPLE 11: Best Practices
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 11: Best Practices")
    print("Guidelines for using the registration pattern:\n")

    print("""
    BEST PRACTICES:

    1. ALWAYS RETURN THE FUNCTION
       @decorator should return the original function unchanged
       This way it can still be called and used normally

    2. DOCUMENT REGISTRATION REQUIREMENTS
       Make clear what a function must do to be registered
       Validate inputs and raise clear errors

    3. CONSIDER NAMING CONVENTIONS
       Functions registered the same way often have similar names
       Use decorators to discover and group related functions

    4. PROVIDE INTROSPECTION
       Make it easy to see what's registered
       offer ways to query the registry

    5. HANDLE REGISTRATION CONFLICTS
       What happens if two functions have the same name/key?
       Should you error, warn, or replace?
       Make policy clear

    6. USE DECORATOR FACTORIES FOR PARAMETERS
       If decorator needs parameters, use a factory:
       @register(name='custom_name')  <- factory
       def func(): ...

    7. KEEP DECORATORS FOCUSED
       Register decorator should only register
       Don't mix in validation, timing, etc.
       (Or do, but document it clearly)

    8. MAKE REGISTRATION EXPLICIT
       Use a clear name like @register, not @dec
       Makes it obvious what the decorator does

    ANTI-PATTERNS:

    X Don't lose the original function
      Don't do: register(func) then ignore return value

    X Don't silently fail
      Raise clear errors if registration fails

    X Don't make registry hard to inspect
      Expose it for debugging and introspection

    X Don't mix registration with side effects
      If decorator does registration, make that clear
    """)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    KEY TAKEAWAYS:

    1. REGISTRATION PATTERN BASICS
       - Create a registry (list or dict)
       - Create a @register decorator
       - Decorator adds function to registry and returns it
       - Use @register on functions you want to collect

    2. BASIC PATTERN:

       registry = []

       def register(func):
           registry.append(func)
           return func

       @register
       def my_function():
           ...

    3. COMMON VARIATIONS
       - Dict registry for named lookup: registry[name] = func
       - Decorator factory for parameters: @register(priority=1)
       - Validation: check requirements before registering
       - Metadata: attach extra info to registered functions

    4. BENEFITS
       - Automatic collection of functions
       - Easy to extend without modifying core code
       - Elegant way to build dispatch systems
       - Works great with plugins

    5. COMMON USES
       - Event systems and callbacks
       - Plugin architectures
       - Command dispatchers
       - API routing
       - Test discovery
       - Middleware chains

    6. KEY PRINCIPLE
       "Register functions as they're defined, not in a central list"
       This makes code more decoupled and extensible.

    7. REMEMBER
       - Always return the function unchanged
       - Keep decorator focused
       - Document registration requirements
       - Make registry inspectable
       - Handle conflicts clearly
    """)
```

---

## Exercises

**Exercise 1.**
Write a `@register` decorator that adds each decorated function to a dictionary keyed by function name. Then write a `dispatch(name, *args)` function that looks up a function by name in the registry and calls it. Register at least two functions and demonstrate dispatching by name.

??? success "Solution to Exercise 1"

        registry = {}

        def register(func):
            """Register a function by its name."""
            registry[func.__name__] = func
            return func

        def dispatch(name, *args):
            """Look up and call a registered function by name."""
            if name not in registry:
                raise KeyError(f"No function registered as '{name}'")
            return registry[name](*args)

        @register
        def add(a, b):
            return a + b

        @register
        def multiply(a, b):
            return a * b

        print(dispatch("add", 3, 4))       # 7
        print(dispatch("multiply", 3, 4))   # 12

---

**Exercise 2.**
Using `@singledispatch`, implement a `format_value` function that formats `int` values with commas (e.g., `1000` becomes `"1,000"`), `float` values to two decimal places (e.g., `3.1` becomes `"3.10"`), and `str` values with quotes (e.g., `hello` becomes `'"hello"'`). The base case should return `repr(obj)`.

??? success "Solution to Exercise 2"

        from functools import singledispatch

        @singledispatch
        def format_value(obj):
            """Base case: use repr."""
            return repr(obj)

        @format_value.register(int)
        def _(value):
            return f"{value:,}"

        @format_value.register(float)
        def _(value):
            return f"{value:.2f}"

        @format_value.register(str)
        def _(value):
            return f'"{value}"'

        print(format_value(1000))       # 1,000
        print(format_value(3.1))        # 3.10
        print(format_value("hello"))    # "hello"
        print(format_value([1, 2]))     # [1, 2]

---

**Exercise 3.**
Build a small plugin system using the registration pattern. Create a `PluginManager` class with a `register(name)` decorator factory and a `run_all()` method that calls every registered plugin function in order and collects their return values into a list. Demonstrate by registering three plugins.

??? success "Solution to Exercise 3"

        class PluginManager:
            """Simple plugin system using the registration pattern."""

            def __init__(self):
                self.plugins = {}

            def register(self, name):
                """Decorator factory that registers a plugin by name."""
                def decorator(func):
                    self.plugins[name] = func
                    return func
                return decorator

            def run_all(self):
                """Run every registered plugin and collect results."""
                results = []
                for name, func in self.plugins.items():
                    results.append((name, func()))
                return results

        pm = PluginManager()

        @pm.register("greet")
        def greet_plugin():
            return "Hello from greet plugin"

        @pm.register("stats")
        def stats_plugin():
            return {"users": 42, "active": 10}

        @pm.register("cleanup")
        def cleanup_plugin():
            return "Cleanup complete"

        for name, result in pm.run_all():
            print(f"{name}: {result}")
