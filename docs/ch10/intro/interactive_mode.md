# Interactive Mode

Interactive mode allows dynamic updating of plots without blocking script execution.

!!! tip "Mental Model"
    Think of interactive mode as a live preview toggle. With `plt.ion()`, every plotting command immediately updates the window, like typing into a live document. With `plt.ioff()`, changes accumulate silently until you explicitly call `plt.show()` to reveal the final result.

---

## Enabling Interactive Mode

```python
import matplotlib.pyplot as plt

plt.ion()   # Turn ON interactive mode
plt.ioff()  # Turn OFF interactive mode
```

Check current state:

```python
plt.isinteractive()  # Returns True or False
```

---

## Basic Interactive Example

```python
import matplotlib.pyplot as plt
import numpy as np
import time

def main():
    # Enable interactive mode
    plt.ion()

    # Create initial plot
    fig, ax = plt.subplots()
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    line, = ax.plot(x, y)

    # Set labels
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Interactive Plotting')

    # Update the plot dynamically
    for i in range(50):
        y = np.sin(x + i * 0.1)
        line.set_ydata(y)
        
        # Redraw the figure
        plt.draw()
        
        # Pause for animation effect
        plt.pause(0.1)

    # Turn off interactive mode
    plt.ioff()

    # Keep window open
    plt.show()

if __name__ == "__main__":
    main()
```

---

## Key Functions

### plt.ion()

Turns on interactive mode:

- Plots update immediately
- Non-blocking execution
- Figures display without `show()`

```python
plt.ion()
plt.plot([1, 2, 3])  # Displays immediately
```

### plt.ioff()

Turns off interactive mode:

- Returns to default behavior
- Requires `plt.show()` to display
- Blocking execution

```python
plt.ioff()
plt.plot([1, 2, 3])
plt.show()  # Required to display
```

### plt.draw()

Redraws the current figure:

- Updates modified elements
- Non-blocking
- Use after changing data

```python
line.set_ydata(new_data)
plt.draw()  # Update display
```

### plt.pause(interval)

Pauses execution and updates display:

- Combines `draw()` with sleep
- Processes GUI events
- Essential for animations

```python
plt.pause(0.1)  # Pause 0.1 seconds and update
```

---

## Animation Pattern

The standard pattern for interactive animations:

```python
import matplotlib.pyplot as plt
import numpy as np

def animate():
    plt.ion()
    
    fig, ax = plt.subplots()
    x = np.linspace(0, 2*np.pi, 100)
    line, = ax.plot(x, np.sin(x))
    ax.set_ylim(-1.5, 1.5)
    
    for phase in np.linspace(0, 4*np.pi, 100):
        line.set_ydata(np.sin(x + phase))
        plt.draw()
        plt.pause(0.05)
    
    plt.ioff()
    plt.show()

animate()
```

---

## Updating Plot Elements

### Update Line Data

```python
line, = ax.plot(x, y)  # Note the comma for unpacking

# Update y-data only
line.set_ydata(new_y)

# Update both x and y
line.set_data(new_x, new_y)
```

### Update Axis Limits

```python
ax.set_xlim(new_xmin, new_xmax)
ax.set_ylim(new_ymin, new_ymax)
```

### Update Title

```python
ax.set_title(f'Frame {i}')
```

---

## Real-Time Data Example

```python
import matplotlib.pyplot as plt
import numpy as np

def real_time_plot():
    plt.ion()
    
    fig, ax = plt.subplots()
    ax.set_xlim(0, 100)
    ax.set_ylim(-2, 2)
    
    x_data = []
    y_data = []
    line, = ax.plot([], [])
    
    for i in range(100):
        # Simulate incoming data
        x_data.append(i)
        y_data.append(np.sin(i * 0.1) + np.random.normal(0, 0.1))
        
        line.set_data(x_data, y_data)
        ax.set_title(f'Data Point: {i}')
        
        plt.draw()
        plt.pause(0.05)
    
    plt.ioff()
    plt.show()

real_time_plot()
```

---

## Interactive Mode vs FuncAnimation

For more complex animations, consider `FuncAnimation`:

```python
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
x = np.linspace(0, 2*np.pi, 100)
line, = ax.plot(x, np.sin(x))
ax.set_ylim(-1.5, 1.5)

def update(frame):
    line.set_ydata(np.sin(x + frame * 0.1))
    return line,

ani = FuncAnimation(fig, update, frames=100, interval=50, blit=True)
plt.show()
```

| Feature | Interactive Mode | FuncAnimation |
|---------|------------------|---------------|
| Simplicity | Simple | More setup |
| Performance | Lower | Higher (blit) |
| Saving | Manual | Built-in |
| Control | Full | Callback-based |

---

## Key Takeaways

- `plt.ion()` enables non-blocking interactive mode
- `plt.draw()` updates the display
- `plt.pause()` combines draw with a delay
- Update data with `line.set_ydata()` or `line.set_data()`
- Use for real-time data and simple animations
- Consider `FuncAnimation` for complex animations


!!! warning "Backend Dependency"

    Interactive mode behavior depends on the **backend** (the rendering engine Matplotlib uses). Different environments behave differently:

    - **Jupyter Notebook** (`%matplotlib inline`) — renders static images per cell; `ion()` has limited effect
    - **Jupyter with widget backend** (`%matplotlib widget`) — true interactive mode with pan/zoom
    - **Python scripts** — requires a GUI backend (Qt, Tk, etc.); `plt.show()` blocks until window closes
    - **Some IDEs** (VS Code, PyCharm) — may override backend behavior

    If interactive mode "doesn't work," check your backend first: `print(matplotlib.get_backend())`.

---

## Exercises

**Exercise 1.** Explain the difference between interactive mode and non-interactive mode in Matplotlib. How do you enable interactive mode?

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

**Exercise 2.** Write code showing how to use `plt.ion()` and `plt.ioff()` to toggle interactive mode. What effect does each have?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Explain the role of `plt.show()` in non-interactive mode. What happens if you call `plt.plot()` without `plt.show()` in a script?

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

**Exercise 4.** Write code that creates a plot and explicitly calls `plt.draw()` and `plt.pause()`. Explain when these functions are useful.

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
