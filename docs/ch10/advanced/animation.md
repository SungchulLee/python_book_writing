# Animation with FuncAnimation

The `matplotlib.animation` module provides tools for creating animated visualizations. `FuncAnimation` is the primary class for creating animations by repeatedly calling a function.

!!! note "Visual Encoding Framework"
    Each tool in this section encodes a different aspect of data into a visual:

    | Tool | What it encodes |
    |---|---|
    | Animation | Change over **time** |
    | [axhline/axvline](axhline_axvline.md) | **Thresholds** and reference points |
    | [fill_between](fill_between.md) | **Regions** — area, uncertainty, difference |
    | [Polar plots](polar_plots.md) | **Periodicity** and direction |
    | [Quiver plots](quiver_plots.md) | **Vector fields** — direction + magnitude |
    | [Secondary axes](secondary_axes.md) | **Unit reinterpretation** of same data |
    | [Twin axes](twin_axes.md) | **Multi-variable comparison** |

    The unifying idea: **visualization = choosing what to emphasize**. Each tool highlights a different structure in the data.

!!! tip "Mental Model"
    `FuncAnimation` works like a flipbook: it repeatedly calls your update function with a new frame number, and each call modifies the Artists on the Axes (e.g., `line.set_ydata(new_y)`). The init function sets up the blank frame, the update function draws each page, and `interval` controls the flip speed in milliseconds.

## Basic FuncAnimation

### Minimal Example

```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, ax = plt.subplots()
x = np.linspace(0, 2 * np.pi, 100)
line, = ax.plot(x, np.sin(x))
ax.set_ylim(-1.5, 1.5)

def update(frame):
    """Update function called for each frame."""
    line.set_ydata(np.sin(x + frame * 0.1))
    return line,

ani = animation.FuncAnimation(
    fig=fig,
    func=update,
    frames=100,
    interval=50,  # milliseconds between frames
    blit=True
)

plt.show()
```

### Understanding the Components

```python
# 1. Create figure and initial plot
fig, ax = plt.subplots()
line, = ax.plot([], [])  # Empty line to update

# 2. Define init function (optional but recommended)
def init():
    """Set up the initial empty frame."""
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-1.5, 1.5)
    line.set_data([], [])
    return line,

# 3. Define update function
def update(frame):
    """Update the plot for each frame."""
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x + frame * 0.1)
    line.set_data(x, y)
    return line,

# 4. Create animation
ani = animation.FuncAnimation(
    fig=fig,
    func=update,
    init_func=init,
    frames=200,
    interval=20,
    blit=True
)
```

## Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `fig` | Figure to animate | Required |
| `func` | Function called each frame | Required |
| `frames` | Number of frames or iterable | None |
| `init_func` | Initialization function | None |
| `interval` | Delay between frames (ms) | 200 |
| `blit` | Optimize drawing | False |
| `repeat` | Loop animation | True |
| `repeat_delay` | Delay before repeat (ms) | 0 |

## The Update Function

The update function receives the frame number (or value from frames iterable) and must return an iterable of artists to redraw.

### Frame as Integer

```python
def update(frame):
    # frame is 0, 1, 2, ..., frames-1
    line.set_ydata(np.sin(x + frame * 0.1))
    return line,
```

### Frame from Iterable

```python
# Use custom frame values
frames = np.linspace(0, 4 * np.pi, 200)

def update(phase):
    # phase comes from the frames iterable
    line.set_ydata(np.sin(x + phase))
    return line,

ani = animation.FuncAnimation(fig, update, frames=frames, interval=20)
```

### Returning Multiple Artists

```python
def update(frame):
    line1.set_ydata(np.sin(x + frame * 0.1))
    line2.set_ydata(np.cos(x + frame * 0.1))
    title.set_text(f'Frame: {frame}')
    return line1, line2, title
```

## Blitting for Performance

Blitting redraws only the changed parts, significantly improving performance.

```python
# With blit=True:
# - init_func must return all artists to animate
# - update must return all artists that changed
# - Artists must have set_animated(True) called

def init():
    line.set_data([], [])
    return line,

def update(frame):
    line.set_ydata(np.sin(x + frame * 0.1))
    return line,

ani = animation.FuncAnimation(
    fig, update,
    init_func=init,
    frames=100,
    blit=True  # Enable blitting
)
```

**Note:** Blitting may not work in all backends (especially notebook environments). Set `blit=False` if you encounter issues.

## Saving Animations

### Save as GIF

```python
ani.save('animation.gif', writer='pillow', fps=30)
```

### Save as MP4

```python
# Requires ffmpeg installed
ani.save('animation.mp4', writer='ffmpeg', fps=30)
```

### Save Options

```python
ani.save(
    'animation.mp4',
    writer='ffmpeg',
    fps=30,
    dpi=100,
    bitrate=1800,
    extra_args=['-vcodec', 'libx264']
)
```

### Available Writers

```python
# Check available writers
print(animation.writers.list())
# Common: ['pillow', 'ffmpeg', 'html']
```

## Practical Examples

### 1. Traveling Wave

```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, ax = plt.subplots()
x = np.linspace(0, 4 * np.pi, 200)
line, = ax.plot(x, np.sin(x))
ax.set_ylim(-1.5, 1.5)
ax.set_title('Traveling Wave')

def update(frame):
    line.set_ydata(np.sin(x - frame * 0.1))
    return line,

ani = animation.FuncAnimation(fig, update, frames=200, interval=30, blit=True)
plt.show()
```

### 2. Growing Circle

```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, ax = plt.subplots()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')

circle = plt.Circle((0, 0), 0.1, fill=False)
ax.add_patch(circle)

def update(frame):
    radius = 0.1 + frame * 0.02
    circle.set_radius(radius)
    return circle,

ani = animation.FuncAnimation(fig, update, frames=80, interval=50, blit=True)
plt.show()
```

### 3. Real-Time Stock Price Simulation

```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, ax = plt.subplots()
ax.set_xlim(0, 100)
ax.set_ylim(90, 110)
ax.set_xlabel('Time')
ax.set_ylabel('Price')
ax.set_title('Stock Price Simulation')

prices = [100]
line, = ax.plot([], [], 'b-')

def update(frame):
    # Random walk
    change = np.random.normal(0, 1)
    prices.append(prices[-1] + change)
    
    # Keep last 100 points
    if len(prices) > 100:
        prices.pop(0)
    
    line.set_data(range(len(prices)), prices)
    ax.set_ylim(min(prices) - 5, max(prices) + 5)
    return line,

ani = animation.FuncAnimation(fig, update, interval=100, blit=False)
plt.show()
```

### 4. Scatter Plot Animation

```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, ax = plt.subplots()
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)

n_points = 50
positions = np.random.randn(n_points, 2)
velocities = np.random.randn(n_points, 2) * 0.1
scatter = ax.scatter(positions[:, 0], positions[:, 1])

def update(frame):
    global positions
    positions += velocities
    
    # Bounce off walls
    for i in range(2):
        mask = np.abs(positions[:, i]) > 5
        velocities[mask, i] *= -1
    
    scatter.set_offsets(positions)
    return scatter,

ani = animation.FuncAnimation(fig, update, frames=200, interval=30, blit=True)
plt.show()
```

### 5. Heatmap Evolution

```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, ax = plt.subplots()
data = np.random.rand(10, 10)
im = ax.imshow(data, cmap='hot', vmin=0, vmax=1)
plt.colorbar(im)

def update(frame):
    # Smooth random evolution
    global data
    data = data * 0.9 + np.random.rand(10, 10) * 0.1
    im.set_array(data)
    return im,

ani = animation.FuncAnimation(fig, update, frames=100, interval=100, blit=True)
plt.show()
```

### 6. Multiple Subplots Animation

```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

x = np.linspace(0, 2 * np.pi, 100)
line1, = ax1.plot(x, np.sin(x))
line2, = ax2.plot(x, np.cos(x))

ax1.set_ylim(-1.5, 1.5)
ax2.set_ylim(-1.5, 1.5)
ax1.set_title('sin(x + φ)')
ax2.set_title('cos(x + φ)')

def update(frame):
    phase = frame * 0.1
    line1.set_ydata(np.sin(x + phase))
    line2.set_ydata(np.cos(x + phase))
    return line1, line2

ani = animation.FuncAnimation(fig, update, frames=100, interval=50, blit=True)
plt.tight_layout()
plt.show()
```

## ArtistAnimation Alternative

For animations from a pre-computed list of frames:

```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, ax = plt.subplots()
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1.5, 1.5)

x = np.linspace(0, 2 * np.pi, 100)

# Pre-compute all frames
frames = []
for phase in np.linspace(0, 2 * np.pi, 50):
    line, = ax.plot(x, np.sin(x + phase), 'b-')
    frames.append([line])

ani = animation.ArtistAnimation(fig, frames, interval=50, blit=True)
plt.show()
```

## Embedding in Notebooks

### Using HTML Display

```python
from IPython.display import HTML

ani = animation.FuncAnimation(fig, update, frames=100, interval=50)
HTML(ani.to_jshtml())
```

### Using to_html5_video

```python
from IPython.display import HTML

HTML(ani.to_html5_video())
```

## Common Pitfalls

### 1. Animation Object Not Stored

```python
# WRONG: Animation is garbage collected
animation.FuncAnimation(fig, update, frames=100)
plt.show()

# CORRECT: Store reference
ani = animation.FuncAnimation(fig, update, frames=100)
plt.show()
```

### 2. Returning Wrong Type

```python
# WRONG: Not returning iterable
def update(frame):
    line.set_ydata(new_data)
    return line  # Missing comma!

# CORRECT: Return tuple/list
def update(frame):
    line.set_ydata(new_data)
    return line,  # Note the comma
```

### 3. Blit Issues

```python
# If animation doesn't update properly with blit=True:
# 1. Try blit=False
# 2. Ensure init_func returns all animated artists
# 3. Ensure update returns all changed artists
```

## Performance Tips

1. **Use blitting** when possible for smoother animations
2. **Reduce data points** for complex plots
3. **Pre-compute data** if the computation is expensive
4. **Lower frame rate** (higher interval) for complex scenes
5. **Use tight_layout()** before animation, not during

```python
fig.tight_layout()  # Call once before animation
ani = animation.FuncAnimation(...)
```

---

## Exercises

**Exercise 1.**
Create a `FuncAnimation` that animates a sine wave scrolling across the screen. Initialize a line plot of `y = sin(x)` for `x` in $[0, 2\pi]$, then in each frame shift the phase by `0.1 * frame_number`. Use 100 frames and an interval of 50 ms.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.animation import FuncAnimation

        fig, ax = plt.subplots()
        x = np.linspace(0, 2 * np.pi, 200)
        line, = ax.plot(x, np.sin(x))
        ax.set_ylim(-1.5, 1.5)

        def update(frame):
            line.set_ydata(np.sin(x + 0.1 * frame))
            return line,

        ani = FuncAnimation(fig, update, frames=100, interval=50, blit=True)
        plt.show()

---

**Exercise 2.**
Create an `ArtistAnimation` that shows a sequence of 20 random heatmaps. In each frame, generate a 10x10 random matrix with `np.random.rand(10, 10)` and display it using `imshow`. Set a title that updates to show the frame number.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.animation import ArtistAnimation

        fig, ax = plt.subplots()
        artists = []

        for i in range(20):
            data = np.random.rand(10, 10)
            im = ax.imshow(data, cmap='viridis', animated=True)
            title = ax.text(0.5, 1.05, f'Frame {i}', transform=ax.transAxes,
                            ha='center', fontsize=12)
            artists.append([im, title])

        ani = ArtistAnimation(fig, artists, interval=200, blit=True)
        plt.show()

---

**Exercise 3.**
Create a `FuncAnimation` of a growing scatter plot. Start with an empty scatter plot and in each frame add a new random point with `np.random.randn(2)`. Accumulate points so that all previously added points remain visible. Use 100 frames and save the animation as a GIF using `PillowWriter`.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.animation import FuncAnimation, PillowWriter

        fig, ax = plt.subplots()
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        scat = ax.scatter([], [])

        xs, ys = [], []

        def update(frame):
            point = np.random.randn(2)
            xs.append(point[0])
            ys.append(point[1])
            scat.set_offsets(np.column_stack([xs, ys]))
            return scat,

        ani = FuncAnimation(fig, update, frames=100, interval=100, blit=True)
        ani.save('growing_scatter.gif', writer=PillowWriter(fps=10))

---

**Exercise 4.**
Create an animation of a bar chart that grows over time. Start with 5 bars at height 0, and in each frame (50 total) increase each bar's height by a random amount between 0 and 1. Use `ax.bar()` and update bar heights using `bar.set_height()` on each bar artist.

??? success "Solution to Exercise 4"

        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
        import numpy as np

        fig, ax = plt.subplots()
        n_bars = 5
        heights = np.zeros(n_bars)
        bars = ax.bar(range(n_bars), heights, color='steelblue')
        ax.set_ylim(0, 30)
        ax.set_title('Growing Bar Chart')

        def update(frame):
            nonlocal heights
            heights += np.random.rand(n_bars)
            for bar, h in zip(bars, heights):
                bar.set_height(h)
            return bars

        ani = animation.FuncAnimation(fig, update, frames=50, interval=100, blit=True)
        plt.show()

---

**Exercise 5.**
Explain why `blit=True` dramatically improves animation performance. What does blitting do, and when does it fail (hint: what happens if the axes limits change between frames)? Write a short animation that intentionally breaks blitting by changing `ax.set_ylim` in the update function, and show the fix.

??? success "Solution to Exercise 5"

    **What blitting does:** instead of redrawing the entire figure each frame, blitting saves the static background (axes, labels, gridlines) once, and only redraws the Artists that changed. This skips the expensive background rendering.

    **When it breaks:** if the axes limits, title, or any "background" element changes between frames, the saved background becomes stale and artifacts appear (old elements remain visible under new ones).

        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
        import numpy as np

        fig, ax = plt.subplots()
        line, = ax.plot([], [])
        ax.set_xlim(0, 10)

        def init():
            line.set_data([], [])
            return line,

        def update(frame):
            x = np.linspace(0, 10, 100)
            y = np.sin(x + frame * 0.1) * frame
            line.set_data(x, y)
            # This BREAKS blit=True — background is stale
            # ax.set_ylim(-frame, frame)
            # Fix: use blit=False when axes limits change
            return line,

        # blit=True works when only Artists change
        ani = animation.FuncAnimation(fig, update, init_func=init,
                                       frames=50, interval=50, blit=True)
        plt.show()

    **Rule:** use `blit=True` when only line/scatter data changes. Use `blit=False` when axes limits, titles, or legends change between frames.
        plt.show()
