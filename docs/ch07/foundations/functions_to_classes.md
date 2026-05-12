# Functions to Classes

Understanding the evolution from functions → closures → classes reveals Python's design philosophy.

!!! tip "Mental Model"
    Functions bundle logic, closures bundle logic with captured state, and classes bundle logic with state *and* a public interface. Each step adds structure: a closure is a function that remembers its environment; a class is a closure that names its variables (attributes) and exposes multiple entry points (methods). When a closure starts feeling cramped, it is time for a class.

---

## The Evolution

$$\begin{array}{ccccccccccccccc}
\text{Function}&\Rightarrow&\text{Closure}&\Rightarrow&\text{Class}\\
&&\uparrow&&\uparrow&\\
&&\text{Free Variables}&&\text{Attributes}\\
&&&&\text{Methods}\\
\end{array}$$

---

## Functions

### 1. First-Class Objects

Functions can be assigned, passed, and returned.

```python
def square(x):
    return x * x

f = square
print(f(4))  # 16
```

### 2. Stateless

Functions don't retain state between calls.

```python
def add_ten(x):
    return x + 10

result = add_ten(5)  # 15
# No memory of previous calls
```

### 3. Limitations

Cannot encapsulate data with behavior.

---

## Closures

### 1. Capturing Variables

```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor  # factor is captured
    return multiply

times3 = make_multiplier(3)
print(times3(10))  # 30
```

### 2. Free Variables

`factor` is a **free variable** in `multiply`:

- Used inside the function
- Not defined locally
- Captured from enclosing scope

### 3. State Retention

```python
times3 = make_multiplier(3)
del make_multiplier  # Can delete outer function

print(times3(10))  # 30 - still works!
```

---

## Free Variables

### 1. Definition

A variable that is:

- Referenced in a function
- Not bound (defined) in that function
- Comes from an enclosing scope

### 2. Example

```python
x = 10  # global

def my_function(y):
    return x + y  # x is FREE, y is BOUND
```

### 3. Where They Live

Free variables are stored in **cell objects** attached to the function via `__closure__` — not in `__dict__` or `__globals__`. This is how closures retain state after the enclosing function returns.

```python
def outer(x):
    def inner(y):
        return x + y  # x is FREE in inner
    return inner

f = outer(10)
print(f.__code__.co_freevars)          # ('x',)
print(f.__closure__[0].cell_contents)  # 10
```

??? note "Function Object Structure"

    `__code__` stores names; runtime structures hold values.

    ```text
    function object (static)
    ├── __code__
    │   ├── co_varnames   → local variable names
    │   ├── co_freevars   → enclosing variable names
    │   └── co_names      → global variable names
    ├── __globals__       → global namespace (name → value)
    └── __closure__       → enclosing values (cell objects)

    execution frame (dynamic, per call)
    └── locals            → local variable values
    ```

    This maps directly to LEGB lookup:

    - **L** ocals → names in `co_varnames`, values in frame
    - **E** nclosing → names in `co_freevars`, values in `__closure__`
    - **G** lobals → names in `co_names`, values in `__globals__`
    - **B** uiltins → fallback from `__globals__["__builtins__"]`

---

## From Closure to Class

### 1. Closure Version

```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

times3 = make_multiplier(3)
print(times3(10))  # 30
```

### 2. Class Version

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor  # attribute instead of free variable
    
    def multiply(self, x):
        return x * self.factor
    
    def __call__(self, x):
        return self.multiply(x)

times3 = Multiplier(3)
print(times3(10))  # 30
```

### 3. Key Differences

- Closure: captures free variables
- Class: stores attributes explicitly

!!! tip "Key Insight"
    A class is a named, reusable closure with multiple behaviors. Closures store state in hidden cell objects (`__closure__`), while classes store state explicitly in instance attributes (`__dict__`). This is the fundamental difference: implicit vs explicit state.

---

## Class Advantages

### 1. Multiple Methods

```python
class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
    
    def decrement(self):
        self.count -= 1
    
    def reset(self):
        self.count = 0
```

### 2. Named State

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width   # explicit names
        self.height = height
```

### 3. Special Methods

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
```

---

## Why Classes Scale Better

Closures work well for simple cases but hit limits as complexity grows:

!!! tip "Closures vs Classes at Scale"
    | Dimension | Closure | Class |
    |---|---|---|
    | State visibility | Implicit (hidden in `__closure__`) | Explicit (`self.attr`, `vars()`) |
    | Number of behaviors | Usually one function | Multiple methods |
    | Extensibility | Cannot inherit or compose | Inheritance, composition, protocols |
    | Introspection | `__closure__[0].cell_contents` | `vars(obj)`, `dir(obj)`, `isinstance()` |
    | Testing | Hard to mock or inspect | Easy to subclass, mock, inject |

    When you find yourself returning multiple functions from a closure, passing mutable containers as shared state, or wishing you could add a method — it is time to switch to a class.

## Closure Limitations

### 1. Single Function

Closures typically return one function.

### 2. Implicit State

State is captured implicitly through free variables.

### 3. Hidden Introspection

Closure state can be inspected via `__closure__`, but it is obscure compared to class attributes.

```python
times3 = make_multiplier(3)
print(times3.__closure__[0].cell_contents)  # 3 — accessible but buried
print(vars(Multiplier(3)))                  # {'factor': 3} — explicit
```

---

??? note "Advanced: Class After Deletion"

    Instances survive even if the class itself is deleted — but class-level
    features become inaccessible.

    ```python
    class Multiplier:
        class_var = "I exist"

        def __init__(self, factor):
            self.factor = factor

    times3 = Multiplier(3)
    del Multiplier  # Delete class

    print(times3.factor)     # ✅ Works: 3
    print(times3.class_var)  # ❌ AttributeError
    # new_obj = Multiplier(5)  # ❌ NameError
    ```

    This is an implementation detail of Python's reference model, not a
    pattern you should rely on in practice.

---

## When to Use Each

### 1. Use Functions

Simple, stateless operations.

### 2. Use Closures

Encapsulate simple state with single behavior.

### 3. Use Classes

- Multiple methods needed
- Complex state
- Need inheritance
- Need special methods

---

## The Unified Model

!!! tip "Functions, Closures, and Classes Are All Objects"
    In Python, functions, closures, and classes are not different paradigms — they are different layers of the same object model:

    - **Function** → object with code + reference to globals
    - **Closure** → function + captured state (`__closure__`)
    - **Class** → object that creates objects (via `__new__` + `__init__`)

    All behavior ultimately comes from attribute access, method calls, and object protocols. OOP is not separate from Python — it is built on the same data model that powers everything else.

## Key Takeaways

- Functions → Closures → Classes progression.
- Closures capture free variables.
- Classes provide explicit attributes.
- Classes offer more features (methods, inheritance).
- Choose based on complexity needs.
- All three are objects in Python's data model — different layers of the same system.

---

## Exercises

**Exercise 1.**
Start with a function `make_counter()` that returns a closure tracking a count. Then refactor it into a `Counter` class with `increment()`, `decrement()`, and `value()` methods. Show both implementations and discuss when the class version is preferable.

??? success "Solution to Exercise 1"

        # Closure version
        def make_counter():
            count = 0
            def increment():
                nonlocal count
                count += 1
                return count
            def decrement():
                nonlocal count
                count -= 1
                return count
            def value():
                return count
            return increment, decrement, value

        inc, dec, val = make_counter()
        print(inc())  # 1
        print(inc())  # 2
        print(dec())  # 1

        # Class version
        class Counter:
            def __init__(self):
                self._count = 0

            def increment(self):
                self._count += 1
                return self._count

            def decrement(self):
                self._count -= 1
                return self._count

            def value(self):
                return self._count

        c = Counter()
        print(c.increment())  # 1
        print(c.increment())  # 2
        print(c.decrement())  # 1
        # Class is better: easier to extend, inspect, and test

---

**Exercise 2.**
Write a function `create_greeter(greeting)` that returns a closure: a function accepting `name` and returning `f"{greeting}, {name}!"`. Then convert this into a `Greeter` class with `__init__` (accepts greeting) and `__call__` (accepts name). Show both produce the same results.

??? success "Solution to Exercise 2"

        # Closure version
        def create_greeter(greeting):
            def greet(name):
                return f"{greeting}, {name}!"
            return greet

        hello = create_greeter("Hello")
        print(hello("Alice"))  # Hello, Alice!

        # Class version
        class Greeter:
            def __init__(self, greeting):
                self.greeting = greeting

            def __call__(self, name):
                return f"{self.greeting}, {name}!"

        hi = Greeter("Hi")
        print(hi("Bob"))  # Hi, Bob!

        # Both produce same results
        assert hello("Alice") == create_greeter("Hello")("Alice")

---

**Exercise 3.**
Create three implementations of a simple accumulator (stores and sums numbers): (1) a function using a global variable, (2) a closure with `nonlocal`, and (3) a class with `add(n)` and `total()` methods. Compare the three approaches and explain why the class version is most maintainable.

??? success "Solution to Exercise 3"

        # 1. Global variable (worst)
        _total = 0
        def add_global(n):
            global _total
            _total += n
        def get_total():
            return _total

        # 2. Closure (better)
        def make_accumulator():
            total = 0
            def add(n):
                nonlocal total
                total += n
                return total
            return add

        acc = make_accumulator()
        print(acc(10))  # 10
        print(acc(20))  # 30

        # 3. Class (best)
        class Accumulator:
            def __init__(self):
                self._total = 0

            def add(self, n):
                self._total += n
                return self._total

            def total(self):
                return self._total

        a = Accumulator()
        print(a.add(10))  # 10
        print(a.add(20))  # 30
        print(a.total())  # 30
        # Class: inspectable, testable, extensible, multiple instances

---

**Exercise 4.**
Using the function object structure shown in the "Free Variables" section, inspect a closure's internals. Create a closure `make_adder(n)` that returns a function adding `n` to its argument. Then print `__code__.co_freevars`, `__closure__[0].cell_contents`, and `__code__.co_varnames` on the returned function. Explain what each reveals.

??? success "Solution to Exercise 4"

        def make_adder(n):
            def add(x):
                return x + n
            return add

        add5 = make_adder(5)

        print(add5.__code__.co_freevars)          # ('n',)
        print(add5.__closure__[0].cell_contents)  # 5
        print(add5.__code__.co_varnames)          # ('x',)

        # co_freevars: names of variables captured from the enclosing scope.
        #   Here 'n' is free — used inside add() but defined in make_adder().
        #
        # __closure__[0].cell_contents: the actual value captured for 'n'.
        #   This is how the closure retains state after make_adder() returns.
        #
        # co_varnames: names of local variables (parameters + locals).
        #   Here 'x' is the parameter of add().
        #
        # Together these map to LEGB:
        #   L = co_varnames (locals)
        #   E = co_freevars + __closure__ (enclosing)
        #   G = __globals__ (module-level)

---

**Exercise 5.**
A colleague writes the following closure-based "counter" that returns three functions. Explain why this design becomes awkward as requirements grow, and refactor it into a class. Add a `reset()` method and a `history` attribute that tracks all values — features that would be painful to add to the closure version.

```python
def make_counter(start=0):
    count = [start]  # mutable container to work around nonlocal
    def increment():
        count[0] += 1
        return count[0]
    def decrement():
        count[0] -= 1
        return count[0]
    def value():
        return count[0]
    return increment, decrement, value
```

??? success "Solution to Exercise 5"

    The closure returns three separate functions sharing a mutable list. This works but is fragile:

    - Adding `reset()` requires returning a fourth function.
    - Adding `history` requires sharing another mutable container across all functions.
    - The caller must unpack and track three (or more) unrelated variables: `inc, dec, val = make_counter()`.
    - There is no `isinstance()` check, no `repr`, and no way to inspect state cleanly.

    **Refactored as a class:**

        class Counter:
            def __init__(self, start=0):
                self._count = start
                self.history = [start]

            def increment(self):
                self._count += 1
                self.history.append(self._count)
                return self._count

            def decrement(self):
                self._count -= 1
                self.history.append(self._count)
                return self._count

            def value(self):
                return self._count

            def reset(self):
                self._count = 0
                self.history.append(0)

            def __repr__(self):
                return f"Counter({self._count})"

        c = Counter()
        c.increment()
        c.increment()
        c.decrement()
        print(c)           # Counter(1)
        print(c.history)   # [0, 1, 2, 1]
        c.reset()
        print(c.history)   # [0, 1, 2, 1, 0]

    The class version is a single object with a clear API, inspectable state, and easy extensibility. This is the moment when closures stop scaling and classes become the right tool.
