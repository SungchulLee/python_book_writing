# Saving Figures

Exporting figures to files is essential for reports, papers, and presentations.

!!! tip "Mental Model"
    `fig.savefig()` renders the Figure to a file just as `plt.show()` renders it to the screen. The file format is inferred from the extension — `.png` for raster, `.pdf` or `.svg` for vector. Set `dpi` for resolution and `bbox_inches='tight'` to avoid clipped labels.

    Saving is the **final step of communication** — a poorly exported figure
    (low resolution, clipped labels, wrong format) can destroy an otherwise good
    visualization. Choose the format based on the audience:

    | Audience | Format | Why |
    |----------|--------|-----|
    | Screen / web | PNG | Universal raster, fixed resolution |
    | Paper / print | PDF | Vector, scales to any size, embeds fonts |
    | Web / interactive | SVG | Vector, DOM-manipulable, searchable text |

!!! warning "Common Pitfalls"

    - **Clipped labels:** without `bbox_inches='tight'`, axis labels and titles may be cut off. Always include it (or use `constrained_layout`).
    - **Low DPI for print:** screen resolution (72–100 DPI) looks blurry in print. Use 300 DPI minimum for papers and posters.
    - **Large SVG files:** vector plots with thousands of data points produce huge SVGs. For dense scatter plots or heatmaps, prefer PNG.
    - **Font embedding in PDF:** by default, Matplotlib embeds fonts in PDF. If you see substitution warnings, set `plt.rcParams['pdf.fonttype'] = 42` to embed TrueType fonts.

---

## Basic savefig

Save using the Figure object:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)

fig.savefig("sine_wave.png")
```

Or via pyplot:

```python
plt.savefig("sine_wave.png")
```

---

## File Formats

Common formats and their use cases:

| Format | Type | Best For |
|--------|------|----------|
| PNG | Raster | Screen display, presentations |
| PDF | Vector | Papers, high-quality print |
| SVG | Vector | Web, scalable graphics |
| EPS | Vector | LaTeX documents |
| JPEG | Raster | Photos (lossy compression) |

```python
fig.savefig("plot.png")
fig.savefig("plot.pdf")
fig.savefig("plot.svg")
```

---

## Resolution (DPI)

Control resolution with the `dpi` parameter:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2, 2, 1000)
y1 = np.cos(40 * x)
y2 = np.exp(-x**2)

fig = plt.figure(figsize=(8, 2.5), facecolor="#f1f1f1")
ax = fig.add_axes((0.1, 0.1, 0.8, 0.8), facecolor="#e1e1e1")

ax.plot(x, y1 * y2)
ax.plot(x, y2, 'g')
ax.set_xlabel("x")
ax.set_ylabel("y")

# Higher DPI = larger file, better quality
fig.savefig("graph_lowres.png", dpi=72)
fig.savefig("graph_highres.png", dpi=300)
```

DPI guidelines:

- Screen: 72-100 dpi
- Print: 300 dpi
- Publication: 300-600 dpi

---

## Background Options

Control background appearance:

```python
# White background (default)
fig.savefig("plot.png")

# Custom background color
fig.savefig("plot.png", facecolor="#f1f1f1")

# Transparent background
fig.savefig("plot.png", transparent=True)

# Edge color
fig.savefig("plot.png", edgecolor='black')
```

---

## Bounding Box

Control what portion of the figure is saved:

```python
# Tight bounding box (removes whitespace)
fig.savefig("plot.png", bbox_inches='tight')

# Add padding around tight box
fig.savefig("plot.png", bbox_inches='tight', pad_inches=0.1)
```

---

## Complete Example

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y_sin = np.sin(x)
y_cos = np.cos(x)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x, y_sin, label='sin(x)')
ax.plot(x, y_cos, label='cos(x)')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Trigonometric Functions')
ax.legend()
ax.grid(True, alpha=0.3)

# Save with all options
fig.savefig(
    "trig_functions.png",
    dpi=300,
    bbox_inches='tight',
    pad_inches=0.1,
    facecolor='white',
    transparent=False
)

plt.show()
```

---

## Saving Multiple Formats

Save the same figure in multiple formats:

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4])

for fmt in ['png', 'pdf', 'svg']:
    fig.savefig(f"output.{fmt}", dpi=300, bbox_inches='tight')
```

---

## Best Practices

1. **Use vector formats for print**: PDF or SVG scale without quality loss
2. **Use PNG for web/screen**: Good quality, universal support
3. **Set DPI before plotting**: `fig = plt.figure(dpi=300)`
4. **Use bbox_inches='tight'**: Removes unwanted whitespace
5. **Be consistent**: Use the same settings across all figures in a document

---

## Key Takeaways

- Use `fig.savefig()` to export figures
- Choose format based on use case (PNG for screen, PDF for print)
- Higher DPI means better quality but larger files
- Use `bbox_inches='tight'` to remove whitespace
- Use `transparent=True` for overlay graphics


---

## Exercises

**Exercise 1.** Write code that creates a simple plot and saves it to a PNG file with `dpi=200` and a tight bounding box. Use `fig.savefig()`.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 2 * np.pi, 100)
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x), 'b-', lw=2)
    ax.set_title('Saved Figure')

    fig.savefig('my_plot.png', dpi=200, bbox_inches='tight')
    plt.show()
    ```

---

**Exercise 2.** Explain the difference between saving a figure as PNG versus SVG. When would you choose each format?

??? success "Solution to Exercise 2"
    **PNG** is a raster format that stores pixels. It is best for web display, quick sharing, and when file size matters. The quality depends on DPI -- higher DPI means larger files but sharper images.

    **SVG** is a vector format that stores shapes and curves as mathematical descriptions. It is best for publication-quality figures, presentations, and documents because it scales to any size without losing quality. However, SVG files can be larger and slower to render for plots with very many data points (e.g., scatter plots with millions of points).

    Choose PNG for screen display and web. Choose SVG (or PDF) for print and publication.

---

**Exercise 3.** Write code that saves the same figure in three formats (PNG, PDF, SVG) by calling `fig.savefig()` three times with different file extensions. Set `dpi=150` for the raster format.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 10, 100)
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x), 'r-', lw=2)
    ax.set_title('Multi-Format Save')

    fig.savefig('plot.png', dpi=150, bbox_inches='tight')
    fig.savefig('plot.pdf', bbox_inches='tight')
    fig.savefig('plot.svg', bbox_inches='tight')
    plt.show()
    ```

---

**Exercise 4.** Create a figure with a transparent background by passing `transparent=True` to `savefig()`. Explain why this is useful when embedding plots in presentations.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 2 * np.pi, 100)
    fig, ax = plt.subplots()
    ax.plot(x, np.cos(x), 'b-', lw=2)
    ax.set_title('Transparent Background')

    fig.savefig('transparent_plot.png', dpi=150,
                bbox_inches='tight', transparent=True)
    plt.show()
    ```

    Saving with `transparent=True` makes the figure and axes backgrounds transparent (alpha=0). This is useful for presentations and documents where you want to overlay the plot on a colored or image background without a white rectangle surrounding it.

---

**Exercise 5.** A colleague's saved figure has clipped axis labels and low resolution. Diagnose and fix: write a `savefig` call that (a) prevents clipping, (b) sets print-quality DPI, (c) uses vector format for a journal submission, and (d) embeds fonts. Explain each parameter choice.

??? success "Solution to Exercise 5"

    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    plt.rcParams['pdf.fonttype'] = 42  # (d) Embed TrueType fonts in PDF

    fig, ax = plt.subplots()
    x = np.linspace(0, 10, 100)
    ax.plot(x, np.sin(x))
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Amplitude (volts)')
    ax.set_title('Signal Measurement')

    fig.savefig(
        'figure_for_journal.pdf',   # (c) Vector format — scales to any size
        dpi=300,                     # (b) Print quality (affects raster elements)
        bbox_inches='tight',         # (a) Prevents clipped labels
        pad_inches=0.1               # Small padding around the figure
    )
    plt.show()
    ```

    - `bbox_inches='tight'` — recomputes the bounding box to include all artists (labels, titles, legends) that would otherwise be clipped by the default figure boundary.
    - `dpi=300` — journals require minimum 300 DPI; 600 for line art.
    - `.pdf` — vector format means no pixelation at any zoom level.
    - `pdf.fonttype=42` — embeds fonts as TrueType instead of Type 3, which some journals require for searchable/selectable text.

    Saving with `transparent=True` makes the figure and axes backgrounds transparent (alpha=0). This is useful for presentations and documents where you want to overlay the plot on a colored or image background without a white rectangle surrounding it.
