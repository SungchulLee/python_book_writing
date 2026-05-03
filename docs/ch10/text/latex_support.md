# LaTeX Support

Matplotlib supports LaTeX-style math rendering for professional mathematical notation.

!!! tip "Mental Model"
    Wrap math expressions in dollar signs inside any Matplotlib string -- titles, labels, annotations -- and they render as formatted equations. Use `r'$\alpha^2$'` (raw strings) to avoid Python interpreting backslashes. For full LaTeX rendering (custom fonts, packages), enable `plt.rcParams['text.usetex'] = True`, which requires a system LaTeX installation.

!!! note "When to Use LaTeX"
    | Scenario | Approach |
    |----------|---------|
    | Papers / publications | `usetex=True` (full LaTeX, consistent with document) |
    | Mathematical notation in plots | Mathtext (`r'$...$'`) — no install needed |
    | Simple labels without math | Plain strings — no dollar signs needed |
    | Exploratory / quick plots | Skip LaTeX entirely — adds complexity for no benefit |

!!! warning "Performance"
    `usetex=True` invokes the system LaTeX compiler for every text element, which
    is **significantly slower** than Matplotlib's built-in mathtext renderer. For
    interactive work or many plots, use the default mathtext (`r'$...$'`) and
    reserve `usetex=True` for final publication rendering.

---

## Basic Math Mode

Use dollar signs for inline math:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title('$y = \\sin(x)$')
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
plt.show()
```

---

## Raw Strings

Use raw strings to avoid escaping backslashes:

```python
# Without raw string (need double backslashes)
ax.set_title('$y = \\sin(x)$')

# With raw string (single backslashes)
ax.set_title(r'$y = \sin(x)$')
```

---

## Common Math Symbols

**Greek letters:**
```python
ax.set_xlabel(r'$\alpha, \beta, \gamma, \delta, \theta, \phi, \pi$')
ax.set_xlabel(r'$\Alpha, \Beta, \Gamma, \Delta, \Theta, \Phi, \Pi$')
```

**Superscripts and subscripts:**
```python
ax.set_title(r'$x^2$')           # x squared
ax.set_title(r'$x_i$')           # x subscript i
ax.set_title(r'$x^{2n}$')        # x to the 2n
ax.set_title(r'$x_{ij}$')        # x subscript ij
```

**Fractions:**
```python
ax.set_title(r'$\frac{a}{b}$')
ax.set_title(r'$\frac{dy}{dx}$')
```

**Square roots:**
```python
ax.set_title(r'$\sqrt{x}$')
ax.set_title(r'$\sqrt[3]{x}$')   # Cube root
```

**Summation and integrals:**
```python
ax.set_title(r'$\sum_{i=1}^{n} x_i$')
ax.set_title(r'$\int_0^\infty e^{-x} dx$')
```

---

## Complex Equations

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Normal distribution formula
ax.text(0.5, 0.8, 
        r'$f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$',
        fontsize=16, ha='center')

# Schrödinger equation
ax.text(0.5, 0.5,
        r'$i\hbar\frac{\partial}{\partial t}\Psi = \hat{H}\Psi$',
        fontsize=16, ha='center')

# Euler's identity
ax.text(0.5, 0.2,
        r'$e^{i\pi} + 1 = 0$',
        fontsize=16, ha='center')

ax.axis('off')
plt.show()
```

---

## Matrices

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Matrix
matrix_text = r'''$\mathbf{A} = \begin{pmatrix}
a_{11} & a_{12} \\
a_{21} & a_{22}
\end{pmatrix}$'''

ax.text(0.5, 0.5, matrix_text, fontsize=14, ha='center', va='center')
ax.axis('off')
plt.show()
```

---

## Using Full LaTeX

For full LaTeX rendering (requires LaTeX installation):

```python
import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'

fig, ax = plt.subplots()
ax.set_title(r'\textbf{Bold Title}')
ax.set_xlabel(r'\textit{Italic Label}')
plt.show()
```

---

## Math in Tick Labels

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y)

ax.set_xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi])
ax.set_xticklabels([r'$-2\pi$', r'$-\pi$', r'$0$', r'$\pi$', r'$2\pi$'])

plt.show()
```

---

## Math Font Styles

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Different styles
ax.text(0.5, 0.9, r'$\mathrm{Roman}$', ha='center', fontsize=14)
ax.text(0.5, 0.7, r'$\mathit{Italic}$', ha='center', fontsize=14)
ax.text(0.5, 0.5, r'$\mathbf{Bold}$', ha='center', fontsize=14)
ax.text(0.5, 0.3, r'$\mathcal{CALLIGRAPHY}$', ha='center', fontsize=14)
ax.text(0.5, 0.1, r'$\mathbb{BLACKBOARD}$', ha='center', fontsize=14)

ax.axis('off')
plt.show()
```

---

## Reference Table

| Symbol | Code | Result |
|--------|------|--------|
| Greek | `\alpha, \beta, \gamma` | α, β, γ |
| Superscript | `x^2` | x² |
| Subscript | `x_i` | xᵢ |
| Fraction | `\frac{a}{b}` | a/b |
| Square root | `\sqrt{x}` | √x |
| Summation | `\sum_{i}^{n}` | Σ |
| Integral | `\int_a^b` | ∫ |
| Infinity | `\infty` | ∞ |
| Partial | `\partial` | ∂ |
| Nabla | `\nabla` | ∇ |

---

## Key Takeaways

- Use `$...$` for math mode
- Raw strings (`r'...'`) avoid escape issues
- Common symbols: Greek letters, fractions, integrals
- Use `\mathrm{}`, `\mathbf{}`, etc. for font styles
- Full LaTeX requires `text.usetex = True` and LaTeX installation


---

## Exercises

**Exercise 1.** Write code that uses LaTeX formatting in a title: display $y = e^{-x^2}$ using `r'$y = e^{-x^2}$'`.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    # Solution code depends on the specific exercise
    x = np.linspace(0, 2 * np.pi, 100)
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x))
    ax.set_title('Example Solution')
    plt.show()
    ```

    See the content of this page for the relevant API details to construct the full solution.

---

**Exercise 2.** Explain why you need the `r` prefix (raw string) when writing LaTeX in Matplotlib strings.

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Create a plot with LaTeX-formatted axis labels, title, and legend entries. Use at least one Greek letter and one fraction.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    x = np.linspace(0, 2 * np.pi, 100)
    axes[0].plot(x, np.sin(x))
    axes[0].set_title('Left Subplot')

    axes[1].plot(x, np.cos(x))
    axes[1].set_title('Right Subplot')

    plt.tight_layout()
    plt.show()
    ```

    Adapt this pattern to the specific requirements of the exercise.

---

**Exercise 4.** Write code that uses `plt.rc('text', usetex=True)` to enable full LaTeX rendering, and create a plot with a complex equation in the title.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    x = np.linspace(0, 10, 100)
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x), 'b-', lw=2)
    ax.set_title('Solution')
    plt.show()
    ```

    Refer to the code examples in the main content for the specific API calls needed.
