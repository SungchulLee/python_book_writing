# Quiver Plots

Quiver plots visualize vector fields using arrows to show direction and magnitude.

!!! tip "Mental Model"
    `ax.quiver(X, Y, U, V)` draws an arrow at each (X, Y) point with direction and length determined by the (U, V) vector components. Think of it as placing tiny wind vanes on a grid -- each arrow shows which way the "wind" blows and how strong it is at that location. It is the standard tool for visualizing gradients, flow fields, and force diagrams.

## Basic Quiver Plot

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 5, 1)
y = np.arange(0, 5, 1)
X, Y = np.meshgrid(x, y)

U = np.ones_like(X)  # x-component
V = np.ones_like(Y)  # y-component

fig, ax = plt.subplots()
ax.quiver(X, Y, U, V)
ax.set_title('Basic Quiver Plot')
plt.show()
```

## Vector Field Example

```python
x = np.linspace(-2, 2, 10)
y = np.linspace(-2, 2, 10)
X, Y = np.meshgrid(x, y)

# Circular field: F = (-y, x)
U = -Y
V = X

fig, ax = plt.subplots()
ax.quiver(X, Y, U, V)
ax.set_aspect('equal')
ax.set_title('Circular Vector Field')
plt.show()
```

## Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `X, Y` | Arrow positions | Required |
| `U, V` | Arrow components | Required |
| `scale` | Arrow length scaling | Auto |
| `width` | Arrow shaft width | 0.005 |
| `headwidth` | Head width | 3 |
| `headlength` | Head length | 5 |
| `color` | Arrow color | 'k' |

## Color by Magnitude

```python
x = np.linspace(-2, 2, 15)
y = np.linspace(-2, 2, 15)
X, Y = np.meshgrid(x, y)

U = -Y
V = X
magnitude = np.sqrt(U**2 + V**2)

fig, ax = plt.subplots()
q = ax.quiver(X, Y, U, V, magnitude, cmap='viridis')
plt.colorbar(q, label='Magnitude')
ax.set_aspect('equal')
plt.show()
```

## Normalized Arrows (Direction Only)

```python
magnitude = np.sqrt(U**2 + V**2)
U_norm = U / magnitude
V_norm = V / magnitude

fig, ax = plt.subplots()
ax.quiver(X, Y, U_norm, V_norm)
ax.set_aspect('equal')
plt.show()
```

## Add Legend (quiverkey)

```python
fig, ax = plt.subplots()
q = ax.quiver(X, Y, U, V)
ax.quiverkey(q, X=0.85, Y=1.05, U=2, label='2 units', labelpos='E')
plt.show()
```

## Practical Example: Gradient Field

```python
x = np.linspace(-3, 3, 15)
y = np.linspace(-3, 3, 15)
X, Y = np.meshgrid(x, y)

# Gradient of f(x,y) = x² + y²
U = 2 * X
V = 2 * Y

fig, ax = plt.subplots()

# Contours
contours = ax.contour(X, Y, X**2 + Y**2, levels=10, cmap='coolwarm')
ax.clabel(contours, inline=True, fontsize=8)

# Gradient vectors (normalized)
mag = np.sqrt(U**2 + V**2)
ax.quiver(X, Y, U/mag, V/mag, alpha=0.6)

ax.set_aspect('equal')
ax.set_title('Gradient Field')
plt.show()
```

## Streamplot Alternative

For smoother flow visualization:

```python
fig, ax = plt.subplots()
ax.streamplot(X, Y, U, V, density=1.5, color=magnitude, cmap='viridis')
ax.set_aspect('equal')
ax.set_title('Streamplot')
plt.show()
```

## Common Use Cases

- Fluid flow visualization
- Electric/magnetic fields
- Wind patterns
- Gradient visualization
- Force diagrams

!!! info "In Machine Learning"

    Quiver plots visualize **gradient fields** in optimization. Plot the gradient of a loss function on a meshgrid to see how gradient descent navigates the loss surface — arrows point "downhill." This reveals saddle points, flat regions, and why some initializations converge faster than others.

---

## Exercises

**Exercise 1.**
Visualize the gradient field of the function $f(x, y) = x^2 + y^2$ using a quiver plot. Compute the partial derivatives analytically ($\nabla f = (2x, 2y)$) on a grid over $[-3, 3] \times [-3, 3]$. Color the arrows by their magnitude.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-3, 3, 15)
        y = np.linspace(-3, 3, 15)
        X, Y = np.meshgrid(x, y)

        U = 2 * X
        V = 2 * Y
        M = np.hypot(U, V)

        fig, ax = plt.subplots(figsize=(8, 6))
        q = ax.quiver(X, Y, U, V, M, cmap='viridis')
        plt.colorbar(q, ax=ax, label='Gradient Magnitude')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(r'Gradient Field of $f(x, y) = x^2 + y^2$')
        ax.set_aspect('equal')
        plt.show()

---

**Exercise 2.**
Create a quiver plot of a rotational vector field $\vec{F} = (-y, x)$ on the grid $[-3, 3] \times [-3, 3]$. Normalize all arrows to unit length using the `np.hypot` function and display the magnitude using a colormap on the arrows.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-3, 3, 15)
        y = np.linspace(-3, 3, 15)
        X, Y = np.meshgrid(x, y)

        U = -Y
        V = X
        M = np.hypot(U, V)
        U_norm = U / M
        V_norm = V / M

        fig, ax = plt.subplots(figsize=(8, 6))
        q = ax.quiver(X, Y, U_norm, V_norm, M, cmap='plasma')
        plt.colorbar(q, ax=ax, label='Magnitude')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Rotational Field F = (-y, x)')
        ax.set_aspect('equal')
        plt.show()

---

**Exercise 3.**
Plot the electric field of two point charges: a positive charge at $(-1, 0)$ and a negative charge at $(1, 0)$. The field from each charge is $\vec{E} = q \cdot \frac{\vec{r}}{|\vec{r}|^3}$ where $\vec{r}$ is the displacement vector. Use a grid over $[-3, 3] \times [-3, 3]$ and overlay a `streamplot` on top of the quiver plot.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-3, 3, 20)
        y = np.linspace(-3, 3, 20)
        X, Y = np.meshgrid(x, y)

        # Positive charge at (-1, 0), negative at (1, 0)
        charges = [(1, -1, 0), (-1, 1, 0)]
        Ex, Ey = np.zeros_like(X), np.zeros_like(Y)

        for q, cx, cy in charges:
            dx = X - cx
            dy = Y - cy
            r = np.hypot(dx, dy)
            r = np.maximum(r, 0.3)
            Ex += q * dx / r**3
            Ey += q * dy / r**3

        M = np.hypot(Ex, Ey)
        Ex_n = Ex / M
        Ey_n = Ey / M

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.quiver(X, Y, Ex_n, Ey_n, M, cmap='inferno', alpha=0.6)

        x_s = np.linspace(-3, 3, 100)
        y_s = np.linspace(-3, 3, 100)
        Xs, Ys = np.meshgrid(x_s, y_s)
        Exs, Eys = np.zeros_like(Xs), np.zeros_like(Ys)
        for q, cx, cy in charges:
            dx = Xs - cx
            dy = Ys - cy
            r = np.hypot(dx, dy)
            r = np.maximum(r, 0.3)
            Exs += q * dx / r**3
            Eys += q * dy / r**3

        ax.streamplot(x_s, y_s, Exs, Eys, color='gray', density=1.5, linewidth=0.5)
        ax.plot(-1, 0, 'ro', ms=10, label='+q')
        ax.plot(1, 0, 'bo', ms=10, label='-q')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Electric Dipole Field')
        ax.legend()
        ax.set_aspect('equal')
        plt.show()

---

**Exercise 4.**
Create a quiver plot of the gradient of `f(x, y) = sin(x) * cos(y)` over a grid on `[-π, π] × [-π, π]`. Compute the partial derivatives analytically (`∂f/∂x = cos(x)cos(y)`, `∂f/∂y = -sin(x)sin(y)`), plot the gradient field, and overlay a contour plot of `f` itself.

??? success "Solution to Exercise 4"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-np.pi, np.pi, 15)
        y = np.linspace(-np.pi, np.pi, 15)
        X, Y = np.meshgrid(x, y)

        # Function and its gradient
        F = np.sin(X) * np.cos(Y)
        dFdx = np.cos(X) * np.cos(Y)
        dFdy = -np.sin(X) * np.sin(Y)

        fig, ax = plt.subplots(figsize=(8, 8))
        # Contour of f
        xf = np.linspace(-np.pi, np.pi, 100)
        yf = np.linspace(-np.pi, np.pi, 100)
        Xf, Yf = np.meshgrid(xf, yf)
        ax.contour(Xf, Yf, np.sin(Xf) * np.cos(Yf), levels=10, alpha=0.5)
        # Gradient arrows
        ax.quiver(X, Y, dFdx, dFdy, color='red', alpha=0.7)
        ax.set_title(r'$\nabla(sin(x)cos(y))$ with Contours')
        ax.set_aspect('equal')
        plt.show()

---

**Exercise 5.**
Explain the difference between `quiver` and `streamplot`. When would you use each? Create a side-by-side comparison of the same vector field `(u, v) = (-Y, X)` (rotation) displayed as a quiver plot and a streamplot.

??? success "Solution to Exercise 5"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-2, 2, 10)
        y = np.linspace(-2, 2, 10)
        X, Y = np.meshgrid(x, y)
        U, V = -Y, X

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        ax1.quiver(X, Y, U, V)
        ax1.set_title('Quiver (discrete arrows)')
        ax1.set_aspect('equal')

        xs = np.linspace(-2, 2, 50)
        ys = np.linspace(-2, 2, 50)
        Xs, Ys = np.meshgrid(xs, ys)
        ax2.streamplot(xs, ys, -Ys, Xs)
        ax2.set_title('Streamplot (flow lines)')
        ax2.set_aspect('equal')

        plt.tight_layout()
        plt.show()

        # Quiver: shows discrete vectors at sample points. Good for seeing
        # local magnitude and direction at specific locations.
        # Streamplot: shows continuous flow lines that follow the field.
        # Good for understanding global flow patterns and topology.
        # Use quiver for precise local measurements, streamplot for
        # understanding the overall flow structure.
