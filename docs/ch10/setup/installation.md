# Installation and Import

Matplotlib is the foundational plotting library for Python scientific computing.

!!! tip "Mental Model"
    Matplotlib has one required install (`matplotlib`) and one standard import convention (`import matplotlib.pyplot as plt`). The `plt` alias is universal -- virtually every tutorial, Stack Overflow answer, and textbook uses it. Memorize this single import line and you are ready to plot.

!!! note "Matplotlib Setup Layers"
    Matplotlib operates in layers, each controlling a different aspect:

    ```text
    1. Environment  (installation, backend)  → where plots render
    2. Defaults     (style sheets, rcParams)  → how plots look
    3. Structure    (subplots, GridSpec)       → how plots are arranged
    4. Content      (plot, scatter, etc.)      → what data is shown
    ```

    This section covers layers 1--2. The **backend** is the rendering engine that
    converts plotting instructions into pixels or files — Matplotlib separates
    plotting logic (your Python code) from rendering (the backend), which is why
    the same code works in Jupyter, scripts, and terminals.

---

## Installation

Install via pip:

```bash
pip install matplotlib
```

Or via conda:

```bash
conda install matplotlib
```

---

## Import Convention

The standard import convention uses `plt` as the alias:

```python
import matplotlib.pyplot as plt
```

For numerical data, NumPy is typically imported alongside:

```python
import matplotlib.pyplot as plt
import numpy as np
```

---

## Version Check

```python
import matplotlib
print(matplotlib.__version__)
```

---

## Backend Configuration

Matplotlib uses **backends** to turn your plotting commands into actual pixels. The rendering pipeline is:

```text
Python code → pyplot API → Backend → Renderer → Output (screen or file)
```

The backend determines *where* and *how* plots appear. Common backends include:

```python
import matplotlib
matplotlib.use('TkAgg')  # Must be called before importing pyplot
```

In Jupyter notebooks:

```python
%matplotlib inline    # Static images embedded in notebook
%matplotlib notebook  # Interactive (zoom, pan)
```

!!! warning "Common Gotchas"

    - **Plot window doesn't appear** → wrong backend for your environment. Try `matplotlib.use('TkAgg')` or `matplotlib.use('Agg')` for headless servers.
    - **Jupyter shows nothing** → add `%matplotlib inline` at the top of the notebook.
    - **Script vs Jupyter behavior differs** → scripts need `plt.show()` to display; Jupyter renders automatically at the end of each cell.

---

## Verifying Installation

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

plt.plot(x, y)
plt.show()
```

If a plot window appears (or renders inline in Jupyter), the installation is successful.

---

## Key Takeaways

- Install with `pip install matplotlib` or `conda install matplotlib`
- Import as `import matplotlib.pyplot as plt`
- Configure backend before importing pyplot if needed


---

## Exercises

**Exercise 1.** Write the standard import statement for Matplotlib's pyplot module and NumPy. Then write code that checks and prints the Matplotlib version.

??? success "Solution to Exercise 1"
        import matplotlib
        import matplotlib.pyplot as plt
        import numpy as np

        print(f"Matplotlib version: {matplotlib.__version__}")

---

**Exercise 2.** Explain the difference between `pip install matplotlib` and `conda install matplotlib`. When would you use each?

??? success "Solution to Exercise 2"
    `pip` installs from PyPI and works in any Python environment. `conda` installs from the Anaconda repository and manages non-Python dependencies (C libraries, system packages) automatically. Use `pip` in plain virtual environments (`venv`). Use `conda` when working inside Anaconda/Miniconda environments, especially if you also need compiled scientific libraries like MKL-optimized NumPy.

---

**Exercise 3.** Write code that creates a simple test plot to verify Matplotlib is installed correctly. Plot $y = \sin(x)$ for $x \in [0, 2\pi]$.

??? success "Solution to Exercise 3"
        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x)

        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_title('Verification: y = sin(x)')
        ax.set_xlabel('x')
        ax.set_ylabel('sin(x)')
        plt.show()

---

**Exercise 4.** List three Matplotlib backends and explain when you would use each. Write one line of code showing how to set the backend.

??? success "Solution to Exercise 4"
    Three common backends:

    - **TkAgg** — default interactive backend on most systems; opens a Tk window for pan/zoom.
    - **Agg** — non-interactive, renders to PNG files; use on headless servers or in scripts that only save figures.
    - **nbAgg / inline** — for Jupyter notebooks; `%matplotlib inline` embeds static PNGs in cells.

    Setting the backend in code (must be called before `import matplotlib.pyplot`):

        import matplotlib
        matplotlib.use('Agg')  # headless rendering
