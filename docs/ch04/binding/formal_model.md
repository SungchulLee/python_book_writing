# Formal Model

!!! tip "Mental Model"
    An environment is just a dictionary that maps names to objects. Assignment writes an entry, lookup reads one, and scope nesting chains dictionaries together so inner scopes can fall through to outer ones.

## Environment

### 1. Name-Value Mapping

Environment (Γ) maps names to values:

```python
# Environment example:
# Γ = {x: 42, y: "hello", z: [1, 2, 3]}

x = 42
y = "hello"
z = [1, 2, 3]
```

### 2. Notation

Formal notation:

```
Γ[x ↦ v]  # Bind x to value v in Γ
Γ(x)      # Lookup x in Γ
```

## Binding Rules

### 1. Simple Binding

```python
# Before: Γ = {}
x = 42
# After: Γ = {x: 42}

# Before: Γ = {x: 42}
y = "hello"
# After: Γ = {x: 42, y: "hello"}
```

### 2. Rebinding

```python
# Before: Γ = {x: 42}
x = 100
# After: Γ = {x: 100}
```

## Evaluation

### 1. Expression Eval

```
Γ ⊢ e ⇓ v
```

Means: "In environment Γ, expression e evaluates to value v"

### 2. Example

```python
# Γ = {x: 10, y: 20}
# Γ ⊢ x + y ⇓ 30

x = 10
y = 20
result = x + y  # 30
```

## Scope Chain

### 1. Nested Environments

```python
# Global: Γ_global = {x: 10}
x = 10

def f():
    # Local: Γ_local = {y: 20}
    # Parent: Γ_global
    y = 20
    return x + y
```

### 2. Lookup Chain

```
Γ_local → Γ_enclosing → Γ_global → Γ_builtin
```

## Assignment Semantics

### 1. Create Binding

```python
# Γ ⊢ x = e ⇓ Γ[x ↦ v]
# where Γ ⊢ e ⇓ v

x = 42
# Evaluates 42, binds x
```

### 2. Multiple Assignment

```python
# Γ ⊢ x, y = e1, e2 ⇓ Γ[x ↦ v1, y ↦ v2]

x, y = 1, 2
```

## Function Application

### 1. Environment Extension

```python
def f(x, y):
    return x + y

# Call: f(10, 20)
# Creates: Γ_f = Γ_global[x ↦ 10, y ↦ 20]
```

### 2. Formal Rule

```
Γ ⊢ f(e1, e2) ⇓ v
where:
  Γ ⊢ e1 ⇓ v1
  Γ ⊢ e2 ⇓ v2
  Γ' = Γ[x ↦ v1, y ↦ v2]
  Γ' ⊢ body ⇓ v
```

## Summary

### 1. Core Concepts

- Environment: name → value mapping
- Binding: Γ[x ↦ v]
- Lookup: Γ(x)
- Evaluation: Γ ⊢ e ⇓ v

### 2. Operations

- Create binding
- Update binding
- Lookup value
- Extend environment

---

## Exercises

**Exercise 1.**
Assignment in Python creates a binding in the current environment. Predict the environment state after each line:

```python
x = 10
y = x
x = 20
print(y)
```

Using formal notation, trace the environment: what is Γ after each statement? Why does `y` remain `10` after `x` is rebound to `20`?

??? success "Solution to Exercise 1"
    Output:

    ```text
    10
    ```

    Environment trace:

    - `x = 10`: Γ = {x: 10}
    - `y = x`: Lookup x in Γ → 10. Γ = {x: 10, y: 10}
    - `x = 20`: Rebind x. Γ = {x: 20, y: 10}

    `y` remains `10` because `y = x` evaluated `x` (getting the integer object `10`) and bound `y` to **that object**. When `x` is later rebound to `20`, the binding of `y` is unaffected. Assignment binds a name to an object; it does not create a dependency between names. In formal terms: Γ[y ↦ Γ(x)] captures the **value** of `x` at that moment, not a reference to the name `x`.

---

**Exercise 2.**
Function calls create new environments that extend the calling environment. Predict the output:

```python
x = "global"

def f(x):
    y = x + "!"
    return y

result = f("local")
print(result)
print(x)
```

Using the formal rule for function application, what environment Γ' does `f("local")` create? Why does the global `x` remain `"global"` after the call?

??? success "Solution to Exercise 2"
    Output:

    ```text
    local!
    global
    ```

    When `f("local")` is called, Python creates a new environment:

    Γ' = Γ_global[x ↦ "local"]

    This local `x` shadows the global `x`. Inside `f`, `y = x + "!"` evaluates in Γ': lookup `x` → `"local"`, compute `"local" + "!"` → `"local!"`, bind `y` → Γ' = {x: "local", y: "local!"}.

    The global `x` remains `"global"` because function parameters create **new bindings** in the local environment. They do not modify the caller's environment. When `f` returns, Γ' is discarded, and we're back in Γ_global where `x` is still `"global"`.

---

**Exercise 3.**
Nested environments form a chain for variable lookup. Predict the output:

```python
x = 1

def outer():
    x = 2
    def inner():
        y = x + 10
        return y
    return inner()

print(outer())
print(x)
```

Trace the environment chain: what are Γ_global, Γ_outer, and Γ_inner? When `inner` evaluates `x + 10`, which environment provides the value of `x`?

??? success "Solution to Exercise 3"
    Output:

    ```text
    12
    1
    ```

    Environment chain:

    - Γ_global = {x: 1, outer: <func>}
    - When `outer()` executes: Γ_outer = {x: 2, inner: <func>}, parent = Γ_global
    - When `inner()` executes: Γ_inner = {y: ?}, parent = Γ_outer

    When `inner` evaluates `x + 10`:
    1. Look up `x` in Γ_inner → not found
    2. Look up `x` in parent Γ_outer → found: 2
    3. Compute 2 + 10 = 12, bind y: Γ_inner = {y: 12}

    The global `x` (= 1) is never reached because Γ_outer's `x` (= 2) is found first. This is the LEGB rule in formal terms: lookup walks Γ_local → Γ_enclosing → Γ_global → Γ_builtin, stopping at the first match.
