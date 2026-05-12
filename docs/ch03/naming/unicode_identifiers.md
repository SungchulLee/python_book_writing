# Unicode Identifiers

!!! tip "Mental Model"
    Python 3 lets you name variables using Unicode letters, so identifiers like `nombre`, `alpha`, or even Korean and Chinese characters are syntactically valid. This is powerful for mathematical code or localized teaching, but in production it is best to stick to ASCII names for cross-team readability and tool compatibility.

## Unicode Support

### 1. Python 3 Allows

Python 3+ supports Unicode in identifiers:

```python
# Korean
이름 = "John"
나이 = 30

# Chinese  
姓名 = "Alice"
年齢 = 25

# Greek
π = 3.14159
α = 0.05
```

### 2. Valid Starters

- Unicode letter
- Underscore

```python
# Valid
名前 = "name"
_프라이빗 = "private"  
Übersetzer = "translator"
```

## Best Practices

### 1. Use ASCII

For international code:

```python
# Recommended
name = "이름"
age = 30

# Not recommended for shared code
이름 = "value"
나이 = 30
```

### 2. Local Projects

OK for local-language projects:

```python
# Korean education app
학생_이름 = "김철수"
학생_나이 = 15
학년 = 3
```

### 3. Math Variables

```python
# Greek letters OK
α = 0.05  # alpha
β = 0.8   # beta  
μ = 100   # mu
σ = 15    # sigma
```

## Why Avoid

### 1. Readability

Hard for non-native speakers:

```python
# Hard to read
def 计算总和(数据):
    总和 = 0
    for 项目 in 数据:
        总和 += 项目
    return 总和

# Better
def calculate_sum(data):
    total = 0
    for item in data:
        total += item
    return total
```

### 2. Encoding Issues

May cause problems with:

- Text editors
- Version control
- CI/CD pipelines

### 3. Typing

Difficult to type special characters

---

## Exercises


**Exercise 1.**
Create variables using non-ASCII Unicode names (e.g., Greek letters, CJK characters). Verify they work as expected.

??? success "Solution to Exercise 1"

        ```python
        # Greek letters for math
        pi = 3.14159

        # CJK characters
        name = "Python"

        print(pi)
        print(name)
        ```

    Python 3 supports Unicode identifiers, allowing mathematical notation and localized variable names.

---

**Exercise 2.**
Explain why using Unicode identifiers can be both useful and problematic. Give one good use case and one potential pitfall.

??? success "Solution to Exercise 2"

    **Good use case**: Mathematical code where Greek letters match the formulas:

        ```python
        delta = x1 - x0
        ```

    **Pitfall**: Team members may not be able to type the characters, and visually similar characters (e.g., Latin `a` vs Cyrillic `a`) can create confusing bugs.

---

**Exercise 3.**
Test whether emoji characters are valid Python identifiers using `str.isidentifier()`.

??? success "Solution to Exercise 3"

        ```python
        print("hello".isidentifier())  # True
        print("变量".isidentifier())    # True

        # Most emoji are NOT valid identifiers
        print("\U0001F600".isidentifier())  # False (😀)
        ```

    Emoji are classified as symbols, not letters, so they cannot be used as identifiers.
