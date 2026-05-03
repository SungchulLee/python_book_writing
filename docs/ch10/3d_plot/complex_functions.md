# Complex Function Visualization

This document covers techniques for visualizing complex-valued functions in 3D, with emphasis on characteristic functions from probability theory and Euler's formula.

!!! tip "Mental Model"
    A complex function maps a real input to a complex output with two parts (real and imaginary), so you need three dimensions to see it: one for the input and two for the output. Plot the real part as one surface and the imaginary part as another, or use a single surface colored by phase. This makes abstract complex analysis tangible.

!!! note "Mathematical Visualization Pipeline"

    Every 3D visualization in this section follows the same pipeline:

    1. **Define the mathematical object** --- function, distribution, parametric curve
    2. **Choose a representation** --- curve (1D to 3D), surface (2D to 3D), or color-coded
    3. **Map variables to axes** --- input to x, real part to y, imaginary part to z
    4. **Choose visual encoding** --- height = magnitude, color = phase, separate real/imag
    5. **Choose viewpoint** --- `view_init(elev, azim)` to reveal specific structure

    The goal: reveal structure that is invisible in equations alone.

## Complex Numbers Review

A complex number $z = x + iy$ has real part $x$ and imaginary part $y$. In Python:

```python
import numpy as np

# Creating complex numbers
z = complex(3, 4)        # 3 + 4i
z = 3 + 4j               # Python notation
z = np.exp(1j * np.pi)   # Euler's formula: e^{iπ} = -1

# Accessing parts
z.real                   # Real part
z.imag                   # Imaginary part
np.abs(z)                # Magnitude |z|
np.angle(z)              # Phase angle
```

## Euler's Formula

$$e^{i\theta} = \cos(\theta) + i\sin(\theta)$$

### 1. Basic Visualization

```python
import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(0, 2 * np.pi, 500)
z = np.exp(1j * t)

fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot(t, np.real(z), np.imag(z), 'blue', linewidth=2)
ax.set_xlabel('θ')
ax.set_ylabel('cos(θ)')
ax.set_zlabel('sin(θ)')
ax.set_title("Euler's Formula: $e^{i\\theta}$")
ax.view_init(25, -60)
plt.show()
```

### 2. Multiple Rotations

```python
t = np.linspace(0, 6 * np.pi, 1000)
z = np.exp(1j * t)

fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': '3d'})
ax.plot(t, np.real(z), np.imag(z), 'blue', linewidth=1.5)
ax.set_xlabel('θ')
ax.set_ylabel('Re$(e^{i\\theta})$')
ax.set_zlabel('Im$(e^{i\\theta})$')
ax.set_title("Euler's Formula: Helix in Complex Space")
ax.view_init(20, -70)
plt.show()
```

### 3. Frequency Comparison

```python
t = np.linspace(0, 4 * np.pi, 500)

fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw={'projection': '3d'})

frequencies = [1, 2, 3]
colors = ['blue', 'green', 'red']

for ax, freq, color in zip(axes, frequencies, colors):
    z = np.exp(1j * freq * t)
    ax.plot(t, np.real(z), np.imag(z), color, linewidth=1.5)
    ax.set_title(f'$e^{{i \\cdot {freq} \\cdot t}}$')
    ax.set_xlabel('t')
    ax.set_ylabel('Re')
    ax.set_zlabel('Im')
    ax.view_init(25, -60)

plt.tight_layout()
plt.show()
```

---

## Characteristic Functions

The characteristic function of a random variable $X$ is defined as:

$$\varphi_X(t) = E[e^{itX}]$$

### Normal Distribution

For $X \sim N(\mu, \sigma^2)$:

$$\varphi_{N(\mu,\sigma^2)}(t) = e^{i\mu t - \frac{1}{2}\sigma^2 t^2}$$

### 1. Standard Normal Characteristic Function

```python
from scipy import stats

t = np.linspace(-10, 10, 1000)
chf = np.exp(-t**2 / 2)  # Standard normal: μ=0, σ=1

fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot(t, np.real(chf), np.imag(chf), 'blue', linewidth=2)
ax.set_xlabel('t')
ax.set_ylabel('Re(φ)')
ax.set_zlabel('Im(φ)')
ax.set_title('Standard Normal: $\\varphi(t) = e^{-t^2/2}$')
ax.view_init(30, -120)
plt.show()
```

### 2. General Normal Characteristic Function

```python
mu = 3.0
sigma = 2.6
t = np.linspace(-15, 15, 1000)

chf = np.exp(1j * mu * t - sigma**2 * t**2 / 2)

fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': '3d'})
ax.plot(t, np.real(chf), np.imag(chf), 'blue', linewidth=1.5)
ax.set_xlabel('t')
ax.set_ylabel('Re(φ)')
ax.set_zlabel('Im(φ)')
ax.set_title(f'Normal CF: $\\mu={mu}$, $\\sigma={sigma}$')
ax.view_init(30, -120)
plt.show()
```

### 3. Effect of Mean (μ)

Changing μ affects the oscillation frequency.

```python
t = np.linspace(-10, 10, 1000)
sigma = 1

fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw={'projection': '3d'})

mus = [0, 2, 4]

for ax, mu in zip(axes, mus):
    chf = np.exp(1j * mu * t - sigma**2 * t**2 / 2)
    ax.plot(t, np.real(chf), np.imag(chf), 'blue', linewidth=1.5)
    ax.set_title(f'μ = {mu}, σ = {sigma}')
    ax.set_xlabel('t')
    ax.set_ylabel('Re')
    ax.set_zlabel('Im')
    ax.view_init(30, -120)

plt.tight_layout()
plt.show()
```

### 4. Effect of Standard Deviation (σ)

Changing σ affects the decay rate.

```python
t = np.linspace(-10, 10, 1000)
mu = 0

fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw={'projection': '3d'})

sigmas = [0.5, 1, 2]

for ax, sigma in zip(axes, sigmas):
    chf = np.exp(1j * mu * t - sigma**2 * t**2 / 2)
    ax.plot(t, np.real(chf), np.imag(chf), 'green', linewidth=1.5)
    ax.set_title(f'μ = {mu}, σ = {sigma}')
    ax.set_xlabel('t')
    ax.set_ylabel('Re')
    ax.set_zlabel('Im')
    ax.view_init(30, -120)

plt.tight_layout()
plt.show()
```

---

## Complete Distribution Visualization

Visualize PDF, CDF, and characteristic function together.

### 1. Standard Normal

```python
mu = 0
sigma = 1
x = np.linspace(-4, 4, 200)
t = np.linspace(-10, 10, 1000)

pdf = stats.norm(mu, sigma).pdf(x)
cdf = stats.norm(mu, sigma).cdf(x)
chf = np.exp(1j * mu * t - sigma**2 * t**2 / 2)

fig = plt.figure(figsize=(15, 5))

# PDF
ax1 = fig.add_subplot(1, 3, 1)
ax1.plot(x, pdf, 'steelblue', linewidth=2)
ax1.fill_between(x, pdf, alpha=0.3)
ax1.set_xlabel('x')
ax1.set_ylabel('f(x)')
ax1.set_title('PDF')
ax1.grid(alpha=0.3)

# CDF
ax2 = fig.add_subplot(1, 3, 2)
ax2.plot(x, cdf, 'darkgreen', linewidth=2)
ax2.set_xlabel('x')
ax2.set_ylabel('F(x)')
ax2.set_title('CDF')
ax2.grid(alpha=0.3)

# Characteristic Function
ax3 = fig.add_subplot(1, 3, 3, projection='3d')
ax3.plot(t, np.real(chf), np.imag(chf), 'purple', linewidth=1.5)
ax3.set_xlabel('t')
ax3.set_ylabel('Re(φ)')
ax3.set_zlabel('Im(φ)')
ax3.set_title('Characteristic Function')
ax3.view_init(30, -120)

plt.suptitle(f'Standard Normal Distribution (μ={mu}, σ={sigma})', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

### 2. General Normal

```python
mu = 3.0
sigma = 2.6
x = np.linspace(-15, 20, 200)
t = np.linspace(-10, 10, 1000)

pdf = stats.norm(mu, sigma).pdf(x)
cdf = stats.norm(mu, sigma).cdf(x)
chf = np.exp(1j * mu * t - sigma**2 * t**2 / 2)

fig = plt.figure(figsize=(14, 5))

ax0 = fig.add_subplot(1, 3, 1)
ax0.plot(x, pdf, 'steelblue', linewidth=2)
ax0.fill_between(x, pdf, alpha=0.3, color='steelblue')
ax0.set_xlabel('$x$', fontsize=12)
ax0.set_ylabel('$f(x)$', fontsize=12)
ax0.set_title('PDF', fontsize=13)
ax0.grid(alpha=0.3)

ax1 = fig.add_subplot(1, 3, 2)
ax1.plot(x, cdf, 'darkgreen', linewidth=2)
ax1.set_xlabel('$x$', fontsize=12)
ax1.set_ylabel('$F(x)$', fontsize=12)
ax1.set_title('CDF', fontsize=13)
ax1.grid(alpha=0.3)

ax2 = fig.add_subplot(1, 3, 3, projection='3d')
ax2.plot(t, np.real(chf), np.imag(chf), 'darkviolet', linewidth=1.5)
ax2.set_xlabel('$t$', fontsize=11)
ax2.set_ylabel('Re$(\\varphi)$', fontsize=11)
ax2.set_zlabel('Im$(\\varphi)$', fontsize=11)
ax2.set_title('$\\varphi(t) = e^{i\\mu t - \\sigma^2 t^2/2}$', fontsize=12)
ax2.view_init(25, -130)

plt.suptitle(f'Normal Distribution: $\\mu={mu}$, $\\sigma={sigma}$', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

---

## Other Distribution Characteristic Functions

### 1. Exponential Distribution

$$\varphi(t) = \frac{\lambda}{\lambda - it}$$

```python
lam = 1.0
t = np.linspace(-5, 5, 1000)
chf = lam / (lam - 1j * t)

fig = plt.figure(figsize=(14, 5))

# PDF
x = np.linspace(0, 6, 200)
ax1 = fig.add_subplot(1, 3, 1)
ax1.plot(x, stats.expon(scale=1/lam).pdf(x), 'steelblue', linewidth=2)
ax1.set_xlabel('x')
ax1.set_ylabel('f(x)')
ax1.set_title('Exponential PDF')
ax1.grid(alpha=0.3)

# Real and Imaginary parts
ax2 = fig.add_subplot(1, 3, 2)
ax2.plot(t, np.real(chf), 'b-', label='Real', linewidth=2)
ax2.plot(t, np.imag(chf), 'r-', label='Imaginary', linewidth=2)
ax2.set_xlabel('t')
ax2.legend()
ax2.set_title('CF Components')
ax2.grid(alpha=0.3)

# 3D
ax3 = fig.add_subplot(1, 3, 3, projection='3d')
ax3.plot(t, np.real(chf), np.imag(chf), 'green', linewidth=1.5)
ax3.set_xlabel('t')
ax3.set_ylabel('Re')
ax3.set_zlabel('Im')
ax3.set_title('$\\varphi(t) = \\frac{\\lambda}{\\lambda - it}$')
ax3.view_init(30, -120)

plt.suptitle('Exponential Distribution (λ=1)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

### 2. Cauchy Distribution

$$\varphi(t) = e^{-|t|}$$

```python
t = np.linspace(-5, 5, 1000)
chf = np.exp(-np.abs(t))

fig = plt.figure(figsize=(14, 5))

# PDF
x = np.linspace(-10, 10, 500)
ax1 = fig.add_subplot(1, 3, 1)
ax1.plot(x, stats.cauchy.pdf(x), 'steelblue', linewidth=2)
ax1.set_xlabel('x')
ax1.set_ylabel('f(x)')
ax1.set_title('Cauchy PDF')
ax1.set_ylim(0, 0.35)
ax1.grid(alpha=0.3)

# Components
ax2 = fig.add_subplot(1, 3, 2)
ax2.plot(t, np.real(chf), 'b-', label='Real', linewidth=2)
ax2.plot(t, np.imag(chf), 'r-', label='Imaginary', linewidth=2)
ax2.set_xlabel('t')
ax2.legend()
ax2.set_title('CF Components')
ax2.grid(alpha=0.3)

# 3D
ax3 = fig.add_subplot(1, 3, 3, projection='3d')
ax3.plot(t, np.real(chf), np.imag(chf), 'red', linewidth=2)
ax3.set_xlabel('t')
ax3.set_ylabel('Re')
ax3.set_zlabel('Im')
ax3.set_title('$\\varphi(t) = e^{-|t|}$')
ax3.view_init(30, -120)

plt.suptitle('Cauchy Distribution', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

### 3. Uniform Distribution

For $X \sim U(a, b)$:

$$\varphi(t) = \frac{e^{itb} - e^{ita}}{it(b-a)}$$

```python
a, b = -1, 1
t = np.linspace(-10, 10, 1000)
t_safe = np.where(np.abs(t) < 1e-10, 1e-10, t)  # Avoid division by zero
chf = (np.exp(1j * t_safe * b) - np.exp(1j * t_safe * a)) / (1j * t_safe * (b - a))

fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot(t, np.real(chf), np.imag(chf), 'orange', linewidth=1.5)
ax.set_xlabel('t')
ax.set_ylabel('Re(φ)')
ax.set_zlabel('Im(φ)')
ax.set_title(f'Uniform CF: U({a}, {b})')
ax.view_init(30, -120)
plt.show()
```

---

## Damped and Growing Oscillations

### 1. Damped Oscillation

```python
t = np.linspace(0, 10, 500)
decay_rate = 0.3
z = np.exp((-decay_rate + 1j) * t)

fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': '3d'})
ax.plot(t, np.real(z), np.imag(z), 'green', linewidth=2)
ax.set_xlabel('t')
ax.set_ylabel('Re')
ax.set_zlabel('Im')
ax.set_title(f'Damped Oscillation: $e^{{(-{decay_rate}+i)t}}$')
ax.view_init(25, -60)
plt.show()
```

### 2. Damping Comparison

```python
t = np.linspace(0, 8, 500)

fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw={'projection': '3d'})

decay_rates = [0, 0.2, 0.5]
titles = ['No Damping', 'Light Damping', 'Heavy Damping']

for ax, decay, title in zip(axes, decay_rates, titles):
    z = np.exp((-decay + 1j) * t)
    ax.plot(t, np.real(z), np.imag(z), linewidth=2)
    ax.set_title(f'{title}\n$e^{{(-{decay}+i)t}}$')
    ax.set_xlabel('t')
    ax.set_ylabel('Re')
    ax.set_zlabel('Im')
    ax.view_init(25, -60)

plt.tight_layout()
plt.show()
```

---

## 3D Axes Customization

### Pane Colors

```python
t = np.linspace(-10, 10, 1000)
chf = np.exp(-t**2 / 2)

fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': '3d'})
ax.plot(t, np.real(chf), np.imag(chf), 'blue', linewidth=2)

# White panes
ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))

ax.set_xlabel('t')
ax.set_ylabel('Re(φ)')
ax.set_zlabel('Im(φ)')
ax.view_init(30, -120)
plt.show()
```

### Z-Label Rotation

```python
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': '3d'})
ax.plot(t, np.real(chf), np.imag(chf), 'blue', linewidth=2)

ax.set_xlabel('t')
ax.set_ylabel('Re(φ)')
ax.set_zlabel('Im(φ)', rotation=90)
ax.zaxis.set_rotate_label(False)
ax.view_init(30, -120)
plt.show()
```

---

## Publication-Quality Figure

```python
mu = 3.0
sigma = 2.6
x = np.linspace(-15, 20, 200)
t = np.linspace(-10, 10, 1000)

pdf = stats.norm(mu, sigma).pdf(x)
cdf = stats.norm(mu, sigma).cdf(x)
chf = np.exp(1j * mu * t - sigma**2 * t**2 / 2)

fig = plt.figure(figsize=(14, 4.5))

# PDF
ax0 = fig.add_subplot(1, 3, 1)
ax0.plot(x, pdf, 'steelblue', linewidth=2)
ax0.fill_between(x, pdf, alpha=0.25, color='steelblue')
ax0.set_xlabel('$x$', fontsize=12)
ax0.set_ylabel('$f(x)$', fontsize=12)
ax0.set_title('Probability Density Function', fontsize=12)
ax0.grid(alpha=0.3)
ax0.tick_params(labelsize=10)

# CDF
ax1 = fig.add_subplot(1, 3, 2)
ax1.plot(x, cdf, 'darkgreen', linewidth=2)
ax1.set_xlabel('$x$', fontsize=12)
ax1.set_ylabel('$F(x)$', fontsize=12)
ax1.set_title('Cumulative Distribution Function', fontsize=12)
ax1.grid(alpha=0.3)
ax1.tick_params(labelsize=10)

# Characteristic Function
ax2 = fig.add_subplot(1, 3, 3, projection='3d')
ax2.plot(t, np.real(chf), np.imag(chf), 'darkviolet', linewidth=1.5)
ax2.set_xlabel('$t$', fontsize=11, labelpad=8)
ax2.set_ylabel('Re$(\\varphi)$', fontsize=11, labelpad=8)
ax2.set_zlabel('Im$(\\varphi)$', fontsize=11, labelpad=8)
ax2.set_title('Characteristic Function', fontsize=12)
ax2.view_init(25, -130)

ax2.w_xaxis.set_pane_color((0.98, 0.98, 0.98, 1.0))
ax2.w_yaxis.set_pane_color((0.98, 0.98, 0.98, 1.0))
ax2.w_zaxis.set_pane_color((0.98, 0.98, 0.98, 1.0))
ax2.tick_params(labelsize=9)

plt.suptitle(f'Normal Distribution: $\\mu={mu}$, $\\sigma={sigma}$', 
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()
```

---

## Summary Table

| Distribution | Characteristic Function | Notes |
|--------------|------------------------|-------|
| Normal $N(\mu, \sigma^2)$ | $e^{i\mu t - \frac{1}{2}\sigma^2 t^2}$ | Oscillates with decay |
| Standard Normal | $e^{-t^2/2}$ | Real-valued, no oscillation |
| Exponential($\lambda$) | $\frac{\lambda}{\lambda - it}$ | Complex rational |
| Cauchy | $e^{-\|t\|}$ | Real-valued |
| Uniform$(a,b)$ | $\frac{e^{itb} - e^{ita}}{it(b-a)}$ | Sinc-like |

---

## Exercises

**Exercise 1.**
Visualize the complex function $f(z) = z^3$ as a 3D surface plot. Create a grid of complex numbers over the square $[-2, 2] \times [-2, 2]$, compute the magnitude $|f(z)|$ for the height and the phase $\arg(f(z))$ for the facecolor using the `hsv` colormap. Add a colorbar labeled "Phase (radians)" and set a descriptive title.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.colors import Normalize

        x = np.linspace(-2, 2, 200)
        y = np.linspace(-2, 2, 200)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y

        W = Z ** 3
        magnitude = np.abs(W)
        phase = np.angle(W)

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')

        norm = Normalize(vmin=-np.pi, vmax=np.pi)
        colors = plt.cm.hsv(norm(phase))

        ax.plot_surface(X, Y, magnitude, facecolors=colors, shade=False)
        ax.set_xlabel('Re(z)')
        ax.set_ylabel('Im(z)')
        ax.set_zlabel('|f(z)|')
        ax.set_title(r'$f(z) = z^3$: Magnitude Surface with Phase Coloring')

        mappable = plt.cm.ScalarMappable(cmap='hsv', norm=norm)
        plt.colorbar(mappable, ax=ax, shrink=0.6, label='Phase (radians)')
        plt.show()

---

**Exercise 2.**
Create a domain coloring plot for the function $f(z) = \frac{1}{z}$ over the region $[-2, 2] \times [-2, 2]$ using `imshow`. Map the phase angle to the `twilight` colormap and use the magnitude to modulate the brightness. Clip the magnitude to a maximum of 5 to avoid extreme values near the singularity at $z = 0$.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-2, 2, 500)
        y = np.linspace(-2, 2, 500)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y

        W = 1 / Z
        phase = np.angle(W)
        magnitude = np.abs(W)
        magnitude_clipped = np.clip(magnitude, 0, 5)

        brightness = magnitude_clipped / 5.0
        colors = plt.cm.twilight((phase + np.pi) / (2 * np.pi))
        colors[..., :3] *= brightness[..., np.newaxis]

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(colors, extent=[-2, 2, -2, 2], origin='lower')
        ax.set_xlabel('Re(z)')
        ax.set_ylabel('Im(z)')
        ax.set_title(r'Domain Coloring of $f(z) = 1/z$')
        plt.show()

---

**Exercise 3.**
Plot the real and imaginary parts of $f(z) = e^z$ as two separate 3D surface plots side by side using `plt.subplots(1, 2, subplot_kw={'projection': '3d'})`. Over the domain $[-2, 2] \times [-2, 2]$, show the real part $e^x \cos(y)$ on the left and the imaginary part $e^x \sin(y)$ on the right. Use different colormaps for each surface and include titles.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-2, 2, 200)
        y = np.linspace(-2, 2, 200)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y

        W = np.exp(Z)
        real_part = W.real
        imag_part = W.imag

        fig, axes = plt.subplots(1, 2, figsize=(14, 6),
                                  subplot_kw={'projection': '3d'})

        axes[0].plot_surface(X, Y, real_part, cmap='viridis', alpha=0.9)
        axes[0].set_xlabel('Re(z)')
        axes[0].set_ylabel('Im(z)')
        axes[0].set_zlabel('Re(f)')
        axes[0].set_title(r'Real Part of $e^z$: $e^x \cos(y)$')

        axes[1].plot_surface(X, Y, imag_part, cmap='plasma', alpha=0.9)
        axes[1].set_xlabel('Re(z)')
        axes[1].set_ylabel('Im(z)')
        axes[1].set_zlabel('Im(f)')
        axes[1].set_title(r'Imaginary Part of $e^z$: $e^x \sin(y)$')

        plt.tight_layout()
        plt.show()
