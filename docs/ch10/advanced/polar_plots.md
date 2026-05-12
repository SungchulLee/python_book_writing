# Polar Plots

Polar plots display data in circular coordinates (angle and radius), useful for directional data, periodic phenomena, and radar charts.

!!! tip "Mental Model"
    A polar plot replaces the x-y grid with an angle-radius grid: the angle goes around the circle (in radians) and the radius goes outward from the center. Create polar axes with `projection='polar'` and then use the same `ax.plot()` and `ax.fill()` calls — only the coordinate interpretation changes.

!!! warning "When to Use Polar (and When Not To)"
    Use polar coordinates when the variable is **inherently cyclic** — wind direction, time of day, phase angles, or any quantity that wraps around. If the data is not cyclic, a polar plot distorts distances and makes comparison harder than a Cartesian plot. Do not use polar just because it looks interesting — use it because the circular structure reveals a pattern that Cartesian coordinates would hide.

## Creating Polar Axes

### Method 1: subplot with projection

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

theta = np.linspace(0, 2 * np.pi, 100)
r = 1 + np.sin(theta)

ax.plot(theta, r)
plt.show()
```

### Method 2: add_subplot with polar=True

```python
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.plot(theta, r)
plt.show()
```

### Method 3: plt.polar (pyplot interface)

```python
plt.polar(theta, r)
plt.show()
```

## Basic Polar Line Plot

```python
import matplotlib.pyplot as plt
import numpy as np

theta = np.linspace(0, 2 * np.pi, 100)
r = np.abs(np.sin(2 * theta) * np.cos(2 * theta))

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(theta, r, 'b-', linewidth=2)
ax.set_title('Rose Curve')
plt.show()
```

## Common Polar Curves

### Cardioid

```python
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
theta = np.linspace(0, 2 * np.pi, 100)
r = 1 + np.cos(theta)  # Cardioid: r = 1 + cos(θ)
ax.plot(theta, r)
ax.set_title('Cardioid')
plt.show()
```

### Rose Curves

```python
fig, axes = plt.subplots(1, 3, subplot_kw={'projection': 'polar'}, figsize=(12, 4))

theta = np.linspace(0, 2 * np.pi, 1000)

# n=2: 4 petals
axes[0].plot(theta, np.sin(2 * theta))
axes[0].set_title('r = sin(2θ)')

# n=3: 3 petals
axes[1].plot(theta, np.sin(3 * theta))
axes[1].set_title('r = sin(3θ)')

# n=5: 5 petals
axes[2].plot(theta, np.sin(5 * theta))
axes[2].set_title('r = sin(5θ)')

plt.tight_layout()
plt.show()
```

### Spiral

```python
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
theta = np.linspace(0, 6 * np.pi, 500)
r = theta  # Archimedean spiral

ax.plot(theta, r)
ax.set_title('Archimedean Spiral')
plt.show()
```

## Polar Scatter Plot

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
n = 100
theta = 2 * np.pi * np.random.rand(n)
r = np.random.rand(n)
colors = np.random.rand(n)
sizes = 100 * np.random.rand(n)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
scatter = ax.scatter(theta, r, c=colors, s=sizes, cmap='viridis', alpha=0.7)
plt.colorbar(scatter)
plt.show()
```

## Polar Bar Chart (Radar/Spider Chart)

### Basic Radar Chart

```python
import matplotlib.pyplot as plt
import numpy as np

categories = ['Speed', 'Reliability', 'Comfort', 'Safety', 'Efficiency']
n_cats = len(categories)

# Values for two products
values1 = [4, 3, 5, 4, 3]
values2 = [3, 5, 3, 5, 4]

# Compute angle for each category
angles = np.linspace(0, 2 * np.pi, n_cats, endpoint=False).tolist()

# Close the plot
values1 += values1[:1]
values2 += values2[:1]
angles += angles[:1]

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

ax.plot(angles, values1, 'o-', linewidth=2, label='Product A')
ax.fill(angles, values1, alpha=0.25)

ax.plot(angles, values2, 'o-', linewidth=2, label='Product B')
ax.fill(angles, values2, alpha=0.25)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)
ax.set_ylim(0, 5)
ax.legend(loc='upper right')
ax.set_title('Product Comparison')
plt.show()
```

### Radar Chart Function

```python
def radar_chart(categories, values_dict, title='Radar Chart'):
    """
    Create radar chart for multiple series.
    
    Parameters:
    - categories: list of category names
    - values_dict: dict mapping series names to value lists
    - title: chart title
    """
    n_cats = len(categories)
    angles = np.linspace(0, 2 * np.pi, n_cats, endpoint=False).tolist()
    angles += angles[:1]  # Close the plot
    
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
    
    for name, values in values_dict.items():
        vals = values + values[:1]  # Close the plot
        ax.plot(angles, vals, 'o-', linewidth=2, label=name)
        ax.fill(angles, vals, alpha=0.2)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax.set_title(title)
    
    return fig, ax

# Usage
categories = ['A', 'B', 'C', 'D', 'E']
values_dict = {
    'Series 1': [4, 3, 5, 2, 4],
    'Series 2': [3, 4, 3, 4, 5],
    'Series 3': [5, 2, 4, 3, 3]
}
radar_chart(categories, values_dict)
plt.show()
```

## Polar Fill

### Fill Between

```python
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

theta = np.linspace(0, 2 * np.pi, 100)
r1 = 1 + 0.5 * np.sin(3 * theta)
r2 = 2 + 0.5 * np.cos(3 * theta)

ax.fill_between(theta, r1, r2, alpha=0.3)
ax.plot(theta, r1, 'b-')
ax.plot(theta, r2, 'r-')
plt.show()
```

### Filled Area

```python
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
theta = np.linspace(0, 2 * np.pi, 100)
r = 1 + np.sin(theta)

ax.fill(theta, r, alpha=0.5, color='blue')
ax.plot(theta, r, 'b-', linewidth=2)
plt.show()
```

## Customizing Polar Axes

### Angular Ticks (Theta)

```python
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(theta, r)

# Set theta tick locations (in radians)
ax.set_xticks(np.linspace(0, 2*np.pi, 8, endpoint=False))

# Set theta tick labels
ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])

plt.show()
```

### Radial Ticks

```python
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(theta, r)

# Set radial limits
ax.set_rlim(0, 2)

# Set radial ticks
ax.set_rticks([0.5, 1, 1.5, 2])

plt.show()
```

### Theta Direction and Zero Position

```python
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(theta, r)

# Set zero position (default is 'E' = right)
ax.set_theta_zero_location('N')  # 0 degrees at top

# Set direction (default is counter-clockwise)
ax.set_theta_direction(-1)  # Clockwise

plt.show()
```

### Grid Styling

```python
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(theta, r)

ax.grid(True, linestyle='--', alpha=0.7)
ax.set_facecolor('lightyellow')

plt.show()
```

## Practical Examples

### 1. Wind Rose Diagram

```python
import matplotlib.pyplot as plt
import numpy as np

# Wind direction data (degrees)
directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
n_dirs = len(directions)
angles = np.linspace(0, 2*np.pi, n_dirs, endpoint=False)

# Wind frequency by direction and speed category
speeds = {
    '0-5 m/s': [10, 5, 8, 12, 15, 10, 7, 8],
    '5-10 m/s': [5, 8, 12, 8, 10, 7, 5, 6],
    '10+ m/s': [2, 3, 5, 3, 4, 2, 1, 2]
}

width = 2*np.pi / n_dirs * 0.8  # Bar width

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(10, 10))

bottom = np.zeros(n_dirs)
for speed, values in speeds.items():
    bars = ax.bar(angles, values, width=width, bottom=bottom, label=speed, alpha=0.7)
    bottom += values

ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_xticks(angles)
ax.set_xticklabels(directions)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
ax.set_title('Wind Rose Diagram')
plt.show()
```

### 2. Daily Activity Pattern

```python
import matplotlib.pyplot as plt
import numpy as np

hours = np.arange(0, 24)
angles = hours * 2 * np.pi / 24

# Activity levels throughout the day
activity = [2, 1, 1, 1, 1, 2, 4, 6, 8, 9, 8, 7,
            6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 3, 2]

# Close the loop
activity = activity + [activity[0]]
angles = np.append(angles, angles[0])

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

ax.plot(angles, activity, 'b-', linewidth=2)
ax.fill(angles, activity, alpha=0.3)

ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_xticks(np.linspace(0, 2*np.pi, 24, endpoint=False))
ax.set_xticklabels([f'{h:02d}:00' for h in range(24)])
ax.set_title('Daily Activity Pattern')
plt.show()
```

### 3. Antenna Radiation Pattern

```python
import matplotlib.pyplot as plt
import numpy as np

theta = np.linspace(0, 2*np.pi, 360)

# Dipole antenna pattern (simplified)
r_dipole = np.abs(np.sin(theta))

# Directional antenna pattern
r_directional = np.abs(np.cos(theta))**2

fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw={'projection': 'polar'}, figsize=(12, 5))

ax1.plot(theta, r_dipole)
ax1.fill(theta, r_dipole, alpha=0.3)
ax1.set_title('Dipole Pattern')

ax2.plot(theta, r_directional)
ax2.fill(theta, r_directional, alpha=0.3)
ax2.set_title('Directional Pattern')

plt.tight_layout()
plt.show()
```

### 4. Sector Performance

```python
import matplotlib.pyplot as plt
import numpy as np

sectors = ['Tech', 'Finance', 'Healthcare', 'Energy', 
           'Consumer', 'Industrial', 'Materials', 'Utilities']
n_sectors = len(sectors)
angles = np.linspace(0, 2*np.pi, n_sectors, endpoint=False)

# Performance metrics
returns = [15, 8, 12, -5, 7, 10, 3, 5]  # %

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(10, 10))

# Normalize for visualization (shift to positive)
r = np.array(returns) + 10

bars = ax.bar(angles, r, width=0.6, alpha=0.7,
              color=['green' if ret > 0 else 'red' for ret in returns])

ax.set_xticks(angles)
ax.set_xticklabels(sectors)
ax.set_ylim(0, 30)
ax.set_rticks([5, 10, 15, 20, 25])
ax.set_yticklabels(['-5%', '0%', '5%', '10%', '15%'])
ax.set_title('Sector Performance')
plt.show()
```

## Multiple Polar Subplots

```python
fig, axes = plt.subplots(2, 2, subplot_kw={'projection': 'polar'}, figsize=(10, 10))

theta = np.linspace(0, 2*np.pi, 100)

curves = [
    ('Cardioid', 1 + np.cos(theta)),
    ('Rose (n=3)', np.sin(3*theta)),
    ('Spiral', theta/10),
    ('Lemniscate', np.sqrt(np.abs(np.cos(2*theta))))
]

for ax, (name, r) in zip(axes.flat, curves):
    ax.plot(theta, r)
    ax.set_title(name)

plt.tight_layout()
plt.show()
```

## Key Methods for Polar Axes

| Method | Description |
|--------|-------------|
| `set_theta_zero_location(loc)` | Position of θ=0 ('N', 'E', 'S', 'W') |
| `set_theta_direction(direction)` | 1=counterclockwise, -1=clockwise |
| `set_rlim(min, max)` | Set radial limits |
| `set_rticks(ticks)` | Set radial tick positions |
| `set_xticks(ticks)` | Set angular tick positions |
| `set_xticklabels(labels)` | Set angular tick labels |
| `set_rgrids(radii)` | Set radial grid lines |
| `set_thetagrids(angles)` | Set angular grid lines |

---

## Exercises

**Exercise 1.**
Create a polar plot of a four-petaled rose curve defined by $r = \cos(2\theta)$ for $\theta \in [0, 2\pi]$. Fill the curve with a semi-transparent color using `fill` and add a descriptive title.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        theta = np.linspace(0, 2 * np.pi, 1000)
        r = np.cos(2 * theta)

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6, 6))
        ax.plot(theta, r, color='purple')
        ax.fill(theta, r, alpha=0.3, color='purple')
        ax.set_title('Four-Petaled Rose: r = cos(2θ)', pad=20)
        plt.show()

---

**Exercise 2.**
Build a radar chart (spider plot) for comparing three students across five subjects: Math, Science, English, History, and Art. Use scores like `[85, 90, 78, 92, 88]`, `[70, 85, 95, 80, 75]`, and `[90, 75, 80, 85, 95]`. Close each polygon by repeating the first value. Add a legend.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        categories = ['Math', 'Science', 'English', 'History', 'Art']
        n = len(categories)
        angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
        angles += angles[:1]

        students = {
            'Alice': [85, 90, 78, 92, 88],
            'Bob':   [70, 85, 95, 80, 75],
            'Carol': [90, 75, 80, 85, 95],
        }

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(7, 7))

        for name, scores in students.items():
            values = scores + scores[:1]
            ax.plot(angles, values, 'o-', label=name)
            ax.fill(angles, values, alpha=0.1)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 100)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        ax.set_title('Student Performance Radar Chart', pad=20)
        plt.show()

---

**Exercise 3.**
Plot the Archimedean spiral $r = \theta$ for $\theta \in [0, 6\pi]$ in polar coordinates. Color the line by the angle value using a colormap by plotting small segments with `plt.scatter` in polar mode. Add a colorbar labeled "Angle (radians)".

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        theta = np.linspace(0, 6 * np.pi, 1000)
        r = theta

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(7, 7))
        sc = ax.scatter(theta, r, c=theta, cmap='viridis', s=2)
        ax.set_title('Archimedean Spiral: r = θ', pad=20)
        plt.colorbar(sc, ax=ax, label='Angle (radians)', pad=0.1)

---

**Exercise 4.**
Create a radar chart (spider plot) comparing three students across 5 subjects. Each student has scores from 0–100 for Math, Science, English, History, and Art. Plot all three students on the same polar axes with different colors and use `ax.fill()` with low alpha. Explain why polar coordinates are natural for this comparison.

??? success "Solution to Exercise 4"

        import matplotlib.pyplot as plt
        import numpy as np

        categories = ['Math', 'Science', 'English', 'History', 'Art']
        n = len(categories)
        angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
        angles += angles[:1]  # close the polygon

        students = {
            'Alice': [90, 85, 70, 65, 80],
            'Bob':   [60, 75, 85, 90, 70],
            'Carol': [80, 80, 80, 80, 80],
        }

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        for name, scores in students.items():
            values = scores + scores[:1]
            ax.plot(angles, values, label=name)
            ax.fill(angles, values, alpha=0.1)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.legend(loc='upper right')
        ax.set_title('Student Comparison')
        plt.show()

        # Polar is natural here because each category is equidistant around
        # a circle — there is no inherent ordering (Math is not "before"
        # Science). The circular layout treats all subjects equally and makes
        # shape comparison intuitive: a balanced student is a regular polygon.

---

**Exercise 5.**
Explain why plotting `y = sin(x)` for `x` in `[0, 10]` in polar coordinates looks strange and misleading. What kind of data is polar appropriate for? Give one example of data that should NEVER be plotted in polar and explain why.

??? success "Solution to Exercise 5"

    `sin(x)` for `x in [0, 10]` in polar interprets `x` as an angle (radians) and `sin(x)` as a radius. The result is a looping curve that does not convey the periodic nature of sine — it distorts the familiar wave into an unrecognizable shape. The problem: `x` here represents a continuous independent variable, not a cyclic angle.

    **Polar is appropriate for:**

    - Wind direction frequency (angle = compass bearing, radius = frequency)
    - Time-of-day activity (angle = hour, radius = count)
    - Phase angles in signal processing

    **Never use polar for:**

    - Time series where time is linear (not cyclic) — e.g., stock prices over 5 years. Plotting this in polar wraps the time axis into a circle, destroying the chronological structure and making trends impossible to read. If the x-axis has a natural start and end (not a cycle), use Cartesian coordinates.
        plt.show()
