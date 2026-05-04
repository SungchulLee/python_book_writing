# Brownian Motion

Visualize stochastic processes with Matplotlib.

!!! tip "Mental Model"
    Brownian motion is a random walk with continuous time -- each step is a small random increment. Plotting many sample paths on one figure reveals the distribution of possible trajectories fanning out from the origin. Use `ax.plot()` in a loop for individual paths and `fill_between` to shade confidence bands.

!!! note "Theoretical Foundation"
    Standard Brownian motion $B_t$ has three defining properties:

    1. **Independent increments**: $B_t - B_s$ is independent of the history up to time $s$
    2. **Normal increments**: $B_t - B_s \sim N(0, t - s)$
    3. **Continuous paths**: $B_t$ is continuous in $t$ (with probability 1)

    Property 2 means variance grows linearly with time — this is why sample paths
    fan out as $\sqrt{t}$, and why the $\pm 2\sqrt{t}$ confidence band captures
    ~95% of paths (by the normal distribution's 2$\sigma$ rule).

!!! tip "Visual Intuition"
    Brownian motion is not a single path — it is a **distribution over paths.**
    Each plotted line is one possible realization; the collection of all lines
    represents the true stochastic object. At each time $t$, the vertical slice
    through the plot is a distribution: $B_t \sim N(0, t)$. As $t$ increases,
    this distribution spreads — which is why the plot "fans out." Brownian motion
    is a **moving distribution**, and plotting many paths makes that movement visible.

    **Geometric Brownian Motion** (GBM) models prices via $S_t = S_0 \exp((\mu - \tfrac{1}{2}\sigma^2)t + \sigma B_t)$.
    The drift correction $-\tfrac{1}{2}\sigma^2$ arises from Ito's lemma: applying
    $\exp$ to a process with quadratic variation shifts the mean. The result is
    that $S_t$ is log-normally distributed — it cannot go negative, matching the
    behavior of asset prices.

---

## Brownian Motion Class

```python
import matplotlib.pyplot as plt
import numpy as np

class BrownianMotion:

    def __init__(self, T=1):
        self.T = T

    def run_MC(self, num_paths=1, num_steps=None, seed=None):
        """
        Generate Brownian motion sample paths.
        
        Parameters
        ----------
        num_paths : int
            Number of paths to generate
        num_steps : int
            Number of time steps
        seed : int
            Random seed for reproducibility
            
        Returns
        -------
        t : array
            Time points
        dt : float
            Time step size
        sqrt_dt : float
            Square root of time step
        B : array
            Brownian motion paths (num_paths x num_steps+1)
        dB : array
            Increments (num_paths x num_steps)
        """
        if num_steps is None:
            num_steps = int(self.T * 12 * 21)  # Daily steps for 1 year
        if seed is not None:
            np.random.seed(seed)

        t = np.linspace(0, self.T, num_steps + 1)
        dt = t[1] - t[0]
        sqrt_dt = np.sqrt(dt)

        Z = np.random.standard_normal((num_paths, num_steps))
        # Note: we do NOT normalize Z here. Centering/rescaling
        # (Z - Z.mean()) / Z.std() would force zero mean and unit
        # variance per time step, breaking independence across paths
        # and invalidating the Monte Carlo sampling.

        dB = Z * sqrt_dt
        B = np.concatenate([np.zeros((num_paths, 1)), dB.cumsum(axis=1)], axis=1)
        
        return t, dt, sqrt_dt, B, dB
```

---

## Plotting Sample Paths

```python
import matplotlib.pyplot as plt
import numpy as np

def main():
    num_paths = 10
    num_steps = 1000

    bm = BrownianMotion()
    t, _, _, B, _ = bm.run_MC(num_paths, num_steps, seed=0)

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.set_title('Ten Sample Paths of Brownian Motion $B_t$')
    
    for i in range(num_paths):
        ax.plot(t, B[i], alpha=0.7)
    
    ax.set_xlabel('Time $t$')
    ax.set_ylabel('$B_t$')
    ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
    ax.grid(True, alpha=0.3)
    
    plt.show()

if __name__ == "__main__":
    main()
```

---

## Distribution at Terminal Time

```python
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def main():
    num_paths = 10000
    num_steps = 1000
    T = 1

    bm = BrownianMotion(T=T)
    t, _, _, B, _ = bm.run_MC(num_paths, num_steps, seed=42)

    # Terminal values
    terminal_values = B[:, -1]

    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Histogram
    ax.hist(terminal_values, bins=50, density=True, alpha=0.7, label='Simulated')
    
    # Theoretical distribution: N(0, T)
    x = np.linspace(-4, 4, 100)
    ax.plot(x, stats.norm(0, np.sqrt(T)).pdf(x), 'r-', lw=2, label=f'$N(0, {T})$')
    
    ax.set_xlabel('$B_T$')
    ax.set_ylabel('Density')
    ax.set_title(f'Distribution of $B_T$ at $T={T}$')
    ax.legend()
    
    plt.show()

if __name__ == "__main__":
    main()
```

---

## Geometric Brownian Motion

Stock price model:

```python
import matplotlib.pyplot as plt
import numpy as np

def simulate_gbm(S0, mu, sigma, T, num_paths, num_steps, seed=None):
    """
    Simulate Geometric Brownian Motion.
    
    S_t = S_0 * exp((mu - sigma^2/2)*t + sigma*B_t)
    """
    if seed is not None:
        np.random.seed(seed)
    
    dt = T / num_steps
    t = np.linspace(0, T, num_steps + 1)
    
    # Generate standard normal increments
    dW = np.random.randn(num_paths, num_steps) * np.sqrt(dt)
    W = np.concatenate([np.zeros((num_paths, 1)), dW.cumsum(axis=1)], axis=1)
    
    # GBM formula
    drift = (mu - 0.5 * sigma**2) * t
    diffusion = sigma * W
    S = S0 * np.exp(drift + diffusion)
    
    return t, S

def main():
    S0 = 100       # Initial price
    mu = 0.10      # Drift (10% annual return)
    sigma = 0.20   # Volatility (20%)
    T = 1          # Time horizon (1 year)
    num_paths = 20
    num_steps = 252  # Trading days

    t, S = simulate_gbm(S0, mu, sigma, T, num_paths, num_steps, seed=42)

    fig, ax = plt.subplots(figsize=(12, 5))
    
    for i in range(num_paths):
        ax.plot(t * 252, S[i], alpha=0.6)
    
    ax.axhline(S0, color='black', linestyle='--', label=f'$S_0={S0}$')
    ax.axhline(S0 * np.exp(mu * T), color='red', linestyle='--', 
               label=f'Expected: ${S0 * np.exp(mu * T):.1f}$')
    
    ax.set_xlabel('Trading Days')
    ax.set_ylabel('Stock Price')
    ax.set_title('Geometric Brownian Motion - Stock Price Simulation')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.show()

if __name__ == "__main__":
    main()
```

---

## Confidence Bands

```python
import matplotlib.pyplot as plt
import numpy as np

def main():
    num_paths = 1000
    num_steps = 252
    T = 1

    bm = BrownianMotion(T=T)
    t, _, _, B, _ = bm.run_MC(num_paths, num_steps, seed=42)

    # Calculate statistics
    mean = B.mean(axis=0)
    std = B.std(axis=0)
    
    # Theoretical standard deviation
    theoretical_std = np.sqrt(t)

    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Plot a few sample paths
    for i in range(5):
        ax.plot(t, B[i], alpha=0.3, color='blue')
    
    # Confidence bands
    ax.fill_between(t, mean - 2*std, mean + 2*std, 
                    alpha=0.2, color='blue', label='±2σ (empirical)')
    ax.plot(t, 2*theoretical_std, 'r--', label='±2σ (theoretical)')
    ax.plot(t, -2*theoretical_std, 'r--')
    
    ax.set_xlabel('Time $t$')
    ax.set_ylabel('$B_t$')
    ax.set_title('Brownian Motion with Confidence Bands')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.show()

if __name__ == "__main__":
    main()
```

---

## Key Takeaways

- Brownian motion is the foundation of stochastic calculus
- Use NumPy for efficient path generation
- Plot multiple paths to show distribution of outcomes
- GBM models stock prices with log-normal distribution
- Confidence bands show expected variation over time


---

## Exercises

**Exercise 1.** Write code that generates and plots 5 sample paths of standard Brownian motion over the interval $[0, 1]$ with 500 time steps. Add a horizontal dashed line at $y = 0$, label the axes, and include a grid.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    T, n_steps, n_paths = 1.0, 500, 5
    dt = T / n_steps
    t = np.linspace(0, T, n_steps + 1)

    dB = np.random.randn(n_paths, n_steps) * np.sqrt(dt)
    B = np.concatenate([np.zeros((n_paths, 1)), dB.cumsum(axis=1)], axis=1)

    fig, ax = plt.subplots(figsize=(10, 4))
    for i in range(n_paths):
        ax.plot(t, B[i], alpha=0.7)
    ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
    ax.set_xlabel('Time $t$')
    ax.set_ylabel('$B_t$')
    ax.set_title('Sample Paths of Brownian Motion')
    ax.grid(True, alpha=0.3)
    plt.show()
    ```

---

**Exercise 2.** Explain why the theoretical standard deviation of Brownian motion $B_t$ at time $t$ is $\sqrt{t}$. Write code that plots the empirical standard deviation of 1000 Brownian paths alongside the theoretical curve $\sqrt{t}$.

??? success "Solution to Exercise 2"
    Brownian motion increments $B_t - B_s \sim N(0, t - s)$ for $s < t$. Starting from $B_0 = 0$, we have $B_t \sim N(0, t)$, so $\text{Var}(B_t) = t$ and $\text{Std}(B_t) = \sqrt{t}$.

    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    T, n_steps, n_paths = 1.0, 500, 1000
    dt = T / n_steps
    t = np.linspace(0, T, n_steps + 1)

    dB = np.random.randn(n_paths, n_steps) * np.sqrt(dt)
    B = np.concatenate([np.zeros((n_paths, 1)), dB.cumsum(axis=1)], axis=1)

    empirical_std = B.std(axis=0)
    theoretical_std = np.sqrt(t)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(t, empirical_std, 'b-', label='Empirical Std')
    ax.plot(t, theoretical_std, 'r--', label=r'Theoretical $\sqrt{t}$')
    ax.set_xlabel('Time $t$')
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Empirical vs Theoretical Std of Brownian Motion')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()
    ```

---

**Exercise 3.** Simulate Geometric Brownian Motion (GBM) with parameters $S_0 = 100$, $\mu = 0.05$, $\sigma = 0.3$, and $T = 1$. Plot 10 sample paths and add a horizontal line at the initial price $S_0$.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    S0, mu, sigma, T = 100, 0.05, 0.3, 1.0
    n_steps, n_paths = 252, 10
    dt = T / n_steps
    t = np.linspace(0, T, n_steps + 1)

    dW = np.random.randn(n_paths, n_steps) * np.sqrt(dt)
    W = np.concatenate([np.zeros((n_paths, 1)), dW.cumsum(axis=1)], axis=1)
    S = S0 * np.exp((mu - 0.5 * sigma**2) * t + sigma * W)

    fig, ax = plt.subplots(figsize=(10, 5))
    for i in range(n_paths):
        ax.plot(t * 252, S[i], alpha=0.7)
    ax.axhline(S0, color='black', linestyle='--', label=f'$S_0 = {S0}$')
    ax.set_xlabel('Trading Days')
    ax.set_ylabel('Price')
    ax.set_title('Geometric Brownian Motion Paths')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()
    ```

---

**Exercise 4.** Create a figure with two subplots side by side. The left subplot shows 5 Brownian motion sample paths. The right subplot shows a histogram of the terminal values $B_T$ for 5000 paths, overlaid with the theoretical $N(0, T)$ density curve.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    T, n_steps = 1.0, 500
    dt = T / n_steps
    t = np.linspace(0, T, n_steps + 1)

    # For paths subplot
    dB5 = np.random.randn(5, n_steps) * np.sqrt(dt)
    B5 = np.concatenate([np.zeros((5, 1)), dB5.cumsum(axis=1)], axis=1)

    # For histogram subplot
    dB_many = np.random.randn(5000, n_steps) * np.sqrt(dt)
    B_many = np.concatenate([np.zeros((5000, 1)), dB_many.cumsum(axis=1)], axis=1)
    terminal = B_many[:, -1]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    for i in range(5):
        ax1.plot(t, B5[i], alpha=0.7)
    ax1.axhline(0, color='black', linestyle='--', linewidth=0.5)
    ax1.set_xlabel('Time $t$')
    ax1.set_ylabel('$B_t$')
    ax1.set_title('Sample Paths')
    ax1.grid(True, alpha=0.3)

    ax2.hist(terminal, bins=50, density=True, alpha=0.7, label='Simulated')
    x_range = np.linspace(-4, 4, 200)
    ax2.plot(x_range, stats.norm(0, np.sqrt(T)).pdf(x_range), 'r-', lw=2,
             label=f'$N(0, {T})$')
    ax2.set_xlabel('$B_T$')
    ax2.set_ylabel('Density')
    ax2.set_title(f'Terminal Distribution at $T={T}$')
    ax2.legend()

    plt.tight_layout()
    plt.show()
    ```
