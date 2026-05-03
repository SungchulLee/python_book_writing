# Curve Fitting with scipy.optimize.curve_fit

Curve fitting is one of the most practical applications of optimization: given noisy experimental data, find the best parameters of a mathematical model. The `scipy.optimize.curve_fit()` function makes this remarkably straightforward.

!!! tip "Mental Model"
    Imagine you have a flexible wire that you can bend by turning a few knobs (parameters). Curve fitting adjusts those knobs until the wire passes as close as possible to every data point. The covariance matrix tells you how wobbly each knob is -- a tight knob means the data pins down that parameter precisely, while a loose knob means different values fit almost equally well.

---

## Understanding Curve Fitting

Curve fitting solves this problem: Given data points $(x_i, y_i)$ and a model $y = f(x, \mathbf{p})$ with unknown parameters $\mathbf{p}$, find parameters that make the model best fit the data.

The standard approach is **least squares**: minimize the sum of squared residuals.

$$\chi^2 = \sum_{i=1}^{n} (y_i - f(x_i, \mathbf{p}))^2$$

### Simple Example: Linear Regression

```python
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Generate synthetic data: y = 2*x + 1 + noise
np.random.seed(42)
xdata = np.array([0, 1, 2, 3, 4, 5])
ydata = 2 * xdata + 1 + np.random.normal(0, 0.5, len(xdata))

# Define model: y = a*x + b
def linear_model(x, a, b):
    return a * x + b

# Fit the model
params, covariance = curve_fit(linear_model, xdata, ydata)
a_opt, b_opt = params

print(f"Optimal parameters:")
print(f"  a = {a_opt:.4f} (true: 2)")
print(f"  b = {b_opt:.4f} (true: 1)")

# Extract uncertainties from covariance matrix
perr = np.sqrt(np.diag(covariance))
print(f"\nParameter uncertainties (1 sigma):")
print(f"  a: {a_opt:.4f} ± {perr[0]:.4f}")
print(f"  b: {b_opt:.4f} ± {perr[1]:.4f}")

# Visualize
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(xdata, ydata, label='Data', s=50)
x_smooth = np.linspace(0, 5, 100)
ax.plot(x_smooth, linear_model(x_smooth, a_opt, b_opt), 'r-',
        label=f'Fit: y = {a_opt:.2f}x + {b_opt:.2f}')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## Basic curve_fit Usage

### Syntax

```python
from scipy.optimize import curve_fit

params, covariance = curve_fit(f, xdata, ydata)
# f: callable - model function with signature f(x, *p)
# xdata: array - independent variable (x values)
# ydata: array - dependent variable (y values)
# Returns: optimal parameters and covariance matrix
```

### Essential Arguments

```python
import numpy as np
from scipy.optimize import curve_fit

def model(x, a, b, c):
    return a * x**2 + b * x + c

xdata = np.array([1, 2, 3, 4, 5])
ydata = np.array([2.5, 5.0, 8.5, 14.0, 21.0])

# Basic call
params, cov = curve_fit(model, xdata, ydata)

# With initial guess
params, cov = curve_fit(model, xdata, ydata, p0=[1, 1, 1])

# With error/uncertainty for each data point
sigma = np.array([0.1, 0.2, 0.15, 0.3, 0.25])
params, cov = curve_fit(model, xdata, ydata, sigma=sigma)

# Absolute sigma (standard deviations of ydata)
params, cov = curve_fit(model, xdata, ydata, sigma=sigma,
                        absolute_sigma=True)

# With bounds on parameters
params, cov = curve_fit(model, xdata, ydata,
                        bounds=([0, -1, 0], [1, 1, 10]))
```

---

## Working with Covariance

The covariance matrix contains information about parameter uncertainties and correlations:

```python
import numpy as np
from scipy.optimize import curve_fit

def exponential(x, a, b):
    return a * np.exp(b * x)

# Generate data
np.random.seed(42)
xdata = np.array([0, 1, 2, 3, 4])
ydata = 2 * np.exp(0.5 * xdata) + np.random.normal(0, 0.5, len(xdata))

# Fit with initial guess
params, cov = curve_fit(exponential, xdata, ydata, p0=[2, 0.5])
a_opt, b_opt = params

# Standard deviations (square root of diagonal)
stddev = np.sqrt(np.diag(cov))
print(f"a = {a_opt:.4f} ± {stddev[0]:.4f}")
print(f"b = {b_opt:.4f} ± {stddev[1]:.4f}")

# Correlation matrix
correlation = np.zeros_like(cov)
for i in range(len(params)):
    for j in range(len(params)):
        correlation[i, j] = cov[i, j] / (stddev[i] * stddev[j])

print(f"\nCorrelation matrix:")
print(correlation)

# If correlation close to ±1, parameters are highly correlated
# (likely can't independently determine both)
```

---

## Practical Example: Fitting Exponential Growth

```python
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Real-world-like data: bacterial population
time = np.array([0, 1, 2, 3, 4, 5, 6])
population = np.array([1000, 1800, 3100, 5500, 9600, 17000, 30000])

def exponential_growth(t, N0, r):
    """Exponential growth: N(t) = N0 * exp(r*t)."""
    return N0 * np.exp(r * t)

# Fit
try:
    params, cov = curve_fit(exponential_growth, time, population,
                           p0=[1000, 0.7],
                           maxfev=10000)
    N0, r = params
    sigma = np.sqrt(np.diag(cov))

    print(f"Initial population: {N0:.0f} ± {sigma[0]:.0f}")
    print(f"Growth rate: {r:.4f} ± {sigma[1]:.4f}")
    print(f"Doubling time: {np.log(2)/r:.2f} hours")

    # Compute residuals
    yhat = exponential_growth(time, N0, r)
    residuals = population - yhat
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((population - np.mean(population))**2)
    r_squared = 1 - ss_res / ss_tot

    print(f"R² = {r_squared:.6f}")

    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Data and fit
    t_smooth = np.linspace(0, 6, 100)
    ax1.scatter(time, population, s=100, label='Data', alpha=0.6)
    ax1.plot(t_smooth, exponential_growth(t_smooth, N0, r), 'r-',
            label=f'Fit: N(t) = {N0:.0f} exp({r:.3f}t)', linewidth=2)
    ax1.set_xlabel('Time (hours)')
    ax1.set_ylabel('Population')
    ax1.set_title('Exponential Growth Fit')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Residuals
    ax2.scatter(time, residuals)
    ax2.axhline(y=0, color='r', linestyle='--')
    ax2.set_xlabel('Time (hours)')
    ax2.set_ylabel('Residuals')
    ax2.set_title('Residual Plot')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

except RuntimeError as e:
    print(f"Curve fit failed: {e}")
```

---

## Handling Non-Uniform Errors

Data points often have different uncertainties. Include this in the fit via the `sigma` parameter:

```python
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Data with known errors
x = np.array([1, 2, 3, 4, 5])
y = np.array([2.1, 3.9, 6.2, 7.8, 10.1])
sigma = np.array([0.1, 0.3, 0.2, 0.4, 0.5])  # Known uncertainties

def linear(x, a, b):
    return a * x + b

# Fit with weights (inverse of error²)
params1, _ = curve_fit(linear, x, y)
print(f"Unweighted: a = {params1[0]:.4f}, b = {params1[1]:.4f}")

# Weighted fit: points with smaller sigma have more influence
params2, cov2 = curve_fit(linear, x, y, sigma=sigma, absolute_sigma=True)
print(f"Weighted: a = {params2[0]:.4f}, b = {params2[1]:.4f}")

# Visualization
fig, ax = plt.subplots(figsize=(10, 6))
ax.errorbar(x, y, yerr=sigma, fmt='o', capsize=5, label='Data with error')

x_smooth = np.linspace(0.5, 5.5, 100)
ax.plot(x_smooth, linear(x_smooth, params2[0], params2[1]), 'r-',
        label=f'Weighted fit: y = {params2[0]:.3f}x + {params2[1]:.3f}')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## Dealing with Initial Guesses

A good initial guess helps the optimizer converge:

```python
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Noisy damped oscillation
t = np.linspace(0, 5, 50)
y_true = 2.0 * np.exp(-0.3 * t) * np.cos(2 * np.pi * 0.5 * t)
y_data = y_true + np.random.normal(0, 0.1, len(t))

def damped_oscillation(t, A, gamma, freq, phase):
    """A * exp(-gamma*t) * cos(2π*freq*t + phase)."""
    return A * np.exp(-gamma * t) * np.cos(2 * np.pi * freq * t + phase)

# Try different initial guesses
p0_list = [
    [1, 0.1, 0.5, 0],      # Poor guess
    [2, 0.3, 0.5, 0],      # Better guess
    [2, 0.3, 0.5, 0.1],    # Best guess
]

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for ax, p0 in zip(axes, p0_list):
    try:
        params, _ = curve_fit(damped_oscillation, t, y_data, p0=p0,
                             maxfev=10000)
        y_fit = damped_oscillation(t, *params)
        residual_ss = np.sum((y_data - y_fit)**2)

        ax.scatter(t, y_data, s=20, alpha=0.6, label='Data')
        ax.plot(t, y_fit, 'r-', linewidth=2, label='Fit')
        ax.set_title(f'p0={p0}\nResidual SS: {residual_ss:.3f}')
        ax.set_xlabel('t')
        ax.set_ylabel('y')
        ax.legend()
        ax.grid(True, alpha=0.3)

    except RuntimeError:
        ax.text(0.5, 0.5, 'Failed to converge', ha='center', va='center',
               transform=ax.transAxes)
        ax.set_title(f'p0={p0}\nFAILED')

plt.tight_layout()
plt.show()

print("Tip: Use the initial guess p0 to provide information about")
print("the scale and rough values of parameters.")
```

---

## Bounds on Parameters

Restrict parameters to physically meaningful ranges:

```python
import numpy as np
from scipy.optimize import curve_fit

# Reaction kinetics data
time = np.array([0, 10, 20, 30, 40, 50])
concentration = np.array([1.0, 0.82, 0.67, 0.55, 0.45, 0.37])

def first_order_kinetics(t, C0, k):
    """C(t) = C0 * exp(-k*t)."""
    return C0 * np.exp(-k * t)

# Without bounds
params1, _ = curve_fit(first_order_kinetics, time, concentration,
                       p0=[1, 0.01])
print(f"Without bounds: C0 = {params1[0]:.4f}, k = {params1[1]:.6f}")

# With bounds: C0 > 0, k > 0
bounds = ([0.5, 0.001], [1.5, 0.1])
params2, _ = curve_fit(first_order_kinetics, time, concentration,
                       p0=[1, 0.01], bounds=bounds)
print(f"With bounds: C0 = {params2[0]:.4f}, k = {params2[1]:.6f}")
```

---

## Comparing Different Models

When multiple models might fit your data, use $R^2$ or Akaike Information Criterion (AIC):

```python
import numpy as np
from scipy.optimize import curve_fit

# Generate noisy data
np.random.seed(42)
x = np.linspace(0, 4, 30)
y = 1 + 2*x - 0.5*x**2 + np.random.normal(0, 0.5, len(x))

def linear_model(x, a, b):
    return a * x + b

def quadratic_model(x, a, b, c):
    return a + b*x + c*x**2

def cubic_model(x, a, b, c, d):
    return a + b*x + c*x**2 + d*x**3

# Fit each model
models = {
    'Linear': (linear_model, 2),
    'Quadratic': (quadratic_model, 3),
    'Cubic': (cubic_model, 4),
}

results = {}

for name, (model, n_params) in models.items():
    params, _ = curve_fit(model, x, y)
    y_fit = model(x, *params)

    # Residual sum of squares
    ss_res = np.sum((y - y_fit)**2)

    # R²
    ss_tot = np.sum((y - np.mean(y))**2)
    r_squared = 1 - ss_res / ss_tot

    # AIC: 2k + n*ln(RSS/n)
    aic = 2*n_params + len(x)*np.log(ss_res/len(x))

    results[name] = {
        'params': params,
        'R²': r_squared,
        'AIC': aic,
        'RSS': ss_res,
        'n_params': n_params
    }

# Compare
print("Model Comparison:")
print("-" * 60)
print(f"{'Model':<12} {'R²':<10} {'AIC':<15} {'RSS':<15}")
print("-" * 60)
for name, res in results.items():
    print(f"{name:<12} {res['R²']:.6f}   {res['AIC']:>12.3f}    {res['RSS']:>12.3f}")

print("\nNote: Higher R², lower AIC is better.")
print("AIC penalizes models with more parameters.")
```

---

## Error Handling

`curve_fit` can fail if the problem is ill-conditioned or the initial guess is poor:

```python
import numpy as np
from scipy.optimize import curve_fit

x = np.array([1, 2, 3, 4, 5])
y = np.array([1, 4, 9, 16, 25])

def model(x, a, b, c):
    return a + b*x + c*x**2

try:
    # This might fail if singular matrix
    params, cov = curve_fit(model, x, y, maxfev=10000)
    print(f"Success: {params}")

except RuntimeError as e:
    print(f"Optimization failed: {e}")
    print("Try:")
    print("  - Better initial guess (p0)")
    print("  - Fewer parameters (simpler model)")
    print("  - More data points")
    print("  - Better scaled data")

except ValueError as e:
    print(f"Invalid input: {e}")
```

---

## Connection to Least Squares

`curve_fit` is a convenience wrapper around least squares optimization. For more control, use `scipy.optimize.least_squares()`:

```python
import numpy as np
from scipy.optimize import least_squares

x = np.array([1, 2, 3, 4, 5])
y = np.array([2.1, 3.9, 6.2, 7.8, 10.1])

def residuals(params, x, y):
    """Residuals: predicted - observed."""
    a, b = params
    return (a*x + b) - y

# Least squares (minimizes sum of squared residuals)
result = least_squares(residuals, x0=[1, 0], args=(x, y))
params = result.x

print(f"Optimal parameters: {params}")
print(f"Final residual sum of squares: {result.cost}")

# Compare with curve_fit
from scipy.optimize import curve_fit
def model(x, a, b):
    return a*x + b

params2, _ = curve_fit(model, x, y)
print(f"curve_fit result: {params2}")
```

---

## Summary

**Key Points About Curve Fitting:**

1. **Define your model** as a function of (x, param1, param2, ...)
2. **Call curve_fit()** with data and model
3. **Use p0** to provide reasonable initial guesses
4. **Include sigma** if you have different uncertainties for each point
5. **Check covariance** to understand parameter correlations
6. **Examine residuals** to diagnose model quality
7. **Use bounds** to restrict parameters to physical ranges
8. **Compare models** using R², AIC, or residual analysis

Next section covers root finding: finding where functions equal zero.

---

## Exercises

**Exercise 1.**
Generate synthetic data from the model $y = A \sin(\omega x + \phi)$ with $A=3$, $\omega=2$, $\phi=0.5$, plus Gaussian noise with $\sigma=0.3$. Use `curve_fit` with an initial guess of `p0=[1, 1, 0]` to recover the parameters. Print the fitted values and their uncertainties from the covariance matrix.

??? success "Solution to Exercise 1"
        ```python
        import numpy as np
        from scipy.optimize import curve_fit

        np.random.seed(42)
        x = np.linspace(0, 2 * np.pi, 50)
        y_true = 3 * np.sin(2 * x + 0.5)
        y_data = y_true + np.random.normal(0, 0.3, len(x))

        def sine_model(x, A, omega, phi):
            return A * np.sin(omega * x + phi)

        params, cov = curve_fit(sine_model, x, y_data, p0=[1, 1, 0])
        sigma = np.sqrt(np.diag(cov))

        names = ['A', 'omega', 'phi']
        true_vals = [3, 2, 0.5]
        for name, p, s, t in zip(names, params, sigma, true_vals):
            print(f"{name}: {p:.4f} +/- {s:.4f} (true: {t})")
        ```

---

**Exercise 2.**
Fit a Gaussian function $f(x) = A \exp\left(-\frac{(x - \mu)^2}{2\sigma^2}\right)$ to the data points `x = [-3, -2, -1, 0, 1, 2, 3]`, `y = [0.05, 0.4, 1.5, 2.8, 1.6, 0.35, 0.04]`. Use bounds to enforce $A > 0$ and $\sigma > 0$. Compute the $R^2$ value of the fit.

??? success "Solution to Exercise 2"
        ```python
        import numpy as np
        from scipy.optimize import curve_fit

        x = np.array([-3, -2, -1, 0, 1, 2, 3])
        y = np.array([0.05, 0.4, 1.5, 2.8, 1.6, 0.35, 0.04])

        def gaussian(x, A, mu, sigma):
            return A * np.exp(-((x - mu)**2) / (2 * sigma**2))

        bounds = ([0, -5, 0.01], [10, 5, 10])
        params, cov = curve_fit(gaussian, x, y, p0=[3, 0, 1], bounds=bounds)

        y_fit = gaussian(x, *params)
        ss_res = np.sum((y - y_fit)**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        r_squared = 1 - ss_res / ss_tot

        print(f"A={params[0]:.4f}, mu={params[1]:.4f}, sigma={params[2]:.4f}")
        print(f"R^2 = {r_squared:.6f}")
        ```

---

**Exercise 3.**
Fit both an exponential decay $y = a e^{-bx}$ and a power law $y = a x^{-b}$ to the data `x = [1, 2, 3, 4, 5, 6, 7, 8]`, `y = [10.0, 5.1, 2.4, 1.3, 0.6, 0.35, 0.18, 0.09]`. Compare the two models using their AIC values and print which model is preferred.

??? success "Solution to Exercise 3"
        ```python
        import numpy as np
        from scipy.optimize import curve_fit

        x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
        y = np.array([10.0, 5.1, 2.4, 1.3, 0.6, 0.35, 0.18, 0.09])
        n = len(x)

        def exp_decay(x, a, b):
            return a * np.exp(-b * x)

        def power_law(x, a, b):
            return a * x**(-b)

        params_exp, _ = curve_fit(exp_decay, x, y, p0=[10, 0.5])
        params_pow, _ = curve_fit(power_law, x, y, p0=[10, 2])

        rss_exp = np.sum((y - exp_decay(x, *params_exp))**2)
        rss_pow = np.sum((y - power_law(x, *params_pow))**2)

        aic_exp = 2 * 2 + n * np.log(rss_exp / n)
        aic_pow = 2 * 2 + n * np.log(rss_pow / n)

        print(f"Exponential: a={params_exp[0]:.4f}, b={params_exp[1]:.4f}, AIC={aic_exp:.2f}")
        print(f"Power law: a={params_pow[0]:.4f}, b={params_pow[1]:.4f}, AIC={aic_pow:.2f}")
        print(f"Preferred: {'Exponential' if aic_exp < aic_pow else 'Power law'} (lower AIC)")
        ```
