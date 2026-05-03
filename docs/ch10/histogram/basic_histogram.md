# Basic Histogram

A histogram groups numerical data into bins and displays the count (or density) of observations in each bin, revealing the shape of the underlying distribution. Whether the data is symmetric, skewed, or multimodal becomes immediately visible, making histograms one of the most common first steps in exploratory data analysis. The `ax.hist()` method in Matplotlib creates histogram visualizations from data arrays.

!!! tip "Mental Model"
    A histogram is a bar chart where the x-axis is a continuous number line divided into bins and the y-axis counts how many data points fall into each bin. Unlike a bar chart for categories, the bins must be contiguous -- gaps would distort the distribution shape. More bins reveal more detail; fewer bins show broader trends.

    The core pipeline: **data → bins → counts → shape.** Everything else —
    density normalization, styling, PDF overlays — builds on this foundation.

## Basic Usage

The following example generates 10,000 samples from a standard normal distribution and plots the histogram with 100 bins.

```python
import matplotlib.pyplot as plt
import numpy as np

def main():
    # data generation
    n_samples = 10_000
    data = np.random.randn(n_samples)  # (10_000,)

    # plot histogram
    fig, ax = plt.subplots()
    ax.hist(data, bins=100)
    plt.show()

if __name__ == "__main__":
    main()
```

## Method Signature

The most commonly used parameters are `bins`, `density`, and `histtype`. The full signature is shown below for reference.

```python
ax.hist(x, bins=None, range=None, density=False, weights=None,
        cumulative=False, bottom=None, histtype='bar', align='mid',
        orientation='vertical', rwidth=None, log=False, color=None,
        label=None, stacked=False, **kwargs)
```

## Key Parameters Overview

| Parameter | Type | Description |
|-----------|------|-------------|
| `x` | array-like | Input data |
| `bins` | int or sequence | Number of bins or bin edges (default: `rcParams["hist.bins"]`, typically 10) |
| `density` | bool | If True, normalize so that the total area equals 1. Each bin height equals count / (total count × bin width) |
| `histtype` | str | Type of histogram: `'bar'`, `'barstacked'`, `'step'`, `'stepfilled'` |
| `alpha` | float | Transparency (0.0 to 1.0), passed via `**kwargs` to the underlying patch artist |

!!! tip "Official Documentation"
    The full parameter descriptions, return values, and additional examples are available in the [Matplotlib API reference for `ax.hist()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.hist.html).

---

## Runnable Example: `complete_guide_hist.py`

```python
"""
Matplotlib Tutorial - Intermediate Level
========================================
Topic: Complete Guide to plt.hist() - Histogram Plotting
Author: Educational Python Course
Level: Intermediate

Learning Objectives:
-------------------
1. Master all parameters and options of plt.hist()
2. Understand the bins parameter (int vs list/array)
3. Understand density=True vs density=False
4. Learn to unpack histogram outputs (n, bins, patches)
5. Create professional histograms
6. Understand bin edges and boundaries
7. Master histogram customization

Prerequisites:
-------------
- Completion of all beginner tutorials
- Understanding of statistical concepts (frequency, probability density)
- Basic NumPy knowledge

IMPORTANT:
---------
plt.hist() and ax.hist() have IDENTICAL parameters and behavior.
Everything here applies to both styles!
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# SECTION 1: Basic Histogram - Understanding the Concept
# ============================================================================

if __name__ == "__main__":

    """
    What is a Histogram?
    -------------------
    A histogram shows the distribution of numerical data by dividing the data
    range into intervals (bins) and counting how many data points fall into
    each bin.

    Key Components:
    - Bins: Intervals that divide the data range
    - Frequency: Count of data points in each bin
    - Density: Probability density (normalized frequency)
    """

    # Generate random data from normal distribution
    np.random.seed(42)
    data = np.random.randn(1000)  # 1000 random numbers from N(0, 1)

    # Create a basic histogram
    plt.hist(data)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Basic Histogram: Default Settings')
    plt.show()

    print("Default behavior: 10 bins, frequency counts")

    # ============================================================================
    # SECTION 2: Complete Signature and Return Values
    # ============================================================================

    """
    Complete Signature:
    ------------------
    hist(x, bins=None, density=False, **kwargs)

    Essential Parameters:
    --------------------
    x : array-like or sequence of arrays
        Data to histogram

    bins : int or sequence or str (default: 10)
        - int: Number of equal-width bins
        - sequence: Bin edges (defines boundary points)
        - str: Method to calculate bins ('auto', 'sturges', 'sqrt', etc.)

    density : bool (default: False)
        - False: Returns counts (frequency)
        - True: Returns probability density (normalized so area = 1)

    Other Important Parameters:
    --------------------------
    range : tuple (min, max)
        Lower and upper range of bins (default: min and max of data)

    cumulative : bool (default: False)
        If True, creates cumulative histogram

    histtype : {'bar', 'barstacked', 'step', 'stepfilled'}
        Type of histogram to draw

    align : {'left', 'mid', 'right'} (default: 'mid')
        Controls bar alignment relative to bin edges

    color : color or array of colors
        Bar colors

    edgecolor : color
        Edge color of bars

    alpha : float (0.0 to 1.0)
        Transparency

    CRITICAL - Return Values:
    ------------------------
    n, bins, patches = plt.hist(...)

    n : array
        Values of the histogram (counts or probability density)
        Length = number of bins

    bins : array
        Bin edges (boundary points)
        Length = number of bins + 1
        bins[i] to bins[i+1] defines the i-th bin

    patches : list of Patches
        Container of individual bar artists
        Can be used to modify bar properties
    """

    # Demonstrate return values
    np.random.seed(42)
    data = np.random.randn(1000)

    n, bins, patches = plt.hist(data, bins=10)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram with Unpacked Return Values')
    plt.show()

    print("=" * 70)
    print("UNDERSTANDING RETURN VALUES")
    print("=" * 70)
    print(f"Type of n: {type(n)}")
    print(f"Type of bins: {type(bins)}")
    print(f"Type of patches: {type(patches)}")
    print()
    print(f"Length of n (number of bins): {len(n)}")
    print(f"Length of bins (number of edges): {len(bins)}")
    print(f"bins has one more element than n!")
    print()
    print("First 5 values of n (counts in each bin):")
    print(n[:5])
    print()
    print("First 6 values of bins (bin edges):")
    print(bins[:6])
    print()
    print("Bin 0: from", bins[0], "to", bins[1], "contains", n[0], "points")
    print("Bin 1: from", bins[1], "to", bins[2], "contains", n[1], "points")

    # ============================================================================
    # SECTION 3: The bins Parameter - Integer (Number of Bins)
    # ============================================================================

    """
    When bins is an INTEGER:
    -----------------------
    - Specifies the NUMBER of equal-width bins
    - Matplotlib automatically divides the data range evenly
    - Default is 10 bins
    """

    np.random.seed(42)
    data = np.random.randn(1000)

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    bin_counts = [5, 10, 20, 30, 50, 100]

    for ax, nbins in zip(axes, bin_counts):
        n, bins, patches = ax.hist(data, bins=nbins, edgecolor='black')
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        ax.set_title(f'bins = {nbins} (Number of bins)')

        # Show bin width
        bin_width = bins[1] - bins[0]
        ax.text(0.95, 0.95, f'Bin width: {bin_width:.3f}',
                transform=ax.transAxes, ha='right', va='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.show()

    print("\nWith integer bins:")
    print("- More bins = finer resolution but noisier")
    print("- Fewer bins = smoother but less detail")
    print("- Choice depends on data size and application")

    # ============================================================================
    # SECTION 4: The bins Parameter - List/Array (Explicit Bin Edges)
    # ============================================================================

    """
    When bins is a LIST or ARRAY:
    -----------------------------
    - Specifies the EXACT bin edges (boundaries)
    - Gives complete control over bin positions and widths
    - Bins don't have to be equal width!
    - Length of bins array = number of bins + 1

    Example: bins = [0, 1, 2, 5, 10]
    Creates 4 bins:
    - Bin 0: [0, 1)
    - Bin 1: [1, 2)
    - Bin 2: [2, 5)
    - Bin 3: [5, 10]

    Note: Last bin includes the right edge
    """

    np.random.seed(42)
    data = np.random.randn(1000)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Equal-width bins (using array)
    bins_equal = np.linspace(-3, 3, 11)  # 10 bins from -3 to 3
    n1, edges1, _ = axes[0, 0].hist(data, bins=bins_equal, edgecolor='black')
    axes[0, 0].set_title('Equal-width bins (linspace)')
    axes[0, 0].set_xlabel('Value')
    axes[0, 0].set_ylabel('Frequency')

    # Custom bins (unequal widths) - focus on center
    bins_custom = [-3, -2, -1, -0.5, 0, 0.5, 1, 2, 3]
    n2, edges2, _ = axes[0, 1].hist(data, bins=bins_custom, edgecolor='black')
    axes[0, 1].set_title('Custom bins (unequal widths)')
    axes[0, 1].set_xlabel('Value')
    axes[0, 1].set_ylabel('Frequency')

    # Very fine bins in center, coarse on edges
    bins_fine_center = np.concatenate([
        np.linspace(-3, -1, 5),     # Coarse on left
        np.linspace(-1, 1, 21),     # Fine in center
        np.linspace(1, 3, 5)        # Coarse on right
    ])
    n3, edges3, _ = axes[1, 0].hist(data, bins=bins_fine_center, edgecolor='black')
    axes[1, 0].set_title('Fine resolution in center')
    axes[1, 0].set_xlabel('Value')
    axes[1, 0].set_ylabel('Frequency')

    # Asymmetric bins
    bins_asym = [-3, -2, -1.5, -1, -0.5, 0, 1, 2, 3]
    n4, edges4, _ = axes[1, 1].hist(data, bins=bins_asym, edgecolor='black')
    axes[1, 1].set_title('Asymmetric bins')
    axes[1, 1].set_xlabel('Value')
    axes[1, 1].set_ylabel('Frequency')

    plt.tight_layout()
    plt.show()

    # Print bin edge information
    print("=" * 70)
    print("CUSTOM BINS EXAMPLE")
    print("=" * 70)
    print("bins array:", bins_custom)
    print(f"Number of bins: {len(bins_custom) - 1}")
    print(f"Bin widths:", [bins_custom[i+1] - bins_custom[i] for i in range(len(bins_custom)-1)])

    # ============================================================================
    # SECTION 5: Understanding Bin Edges (Boundaries)
    # ============================================================================

    """
    CRITICAL CONCEPT: Bin Edges vs Bin Centers

    When bins = [0, 1, 2, 3]:
    - 3 bins are created
    - Bin edges: [0, 1, 2, 3] (4 values)
    - Bin 0: [0, 1) - includes 0, excludes 1
    - Bin 1: [1, 2) - includes 1, excludes 2
    - Bin 2: [2, 3] - includes 2, includes 3 (last bin includes right edge!)

    The bins array returned by hist() gives you the EDGES, not centers.
    """

    # Generate simple data to understand binning
    data_simple = [0.5, 1.5, 1.8, 2.2, 2.7, 3.5, 4.1, 4.9]
    bins_simple = [0, 2, 4, 5]  # Creates 3 bins

    n, bins, patches = plt.hist(data_simple, bins=bins_simple, edgecolor='black')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Understanding Bin Edges')

    # Add vertical lines at bin edges
    for edge in bins:
        plt.axvline(edge, color='red', linestyle='--', alpha=0.7, linewidth=2)

    # Annotate bins
    for i in range(len(bins) - 1):
        mid = (bins[i] + bins[i+1]) / 2
        plt.text(mid, max(n) * 1.1, f'Bin {i}\n[{bins[i]}, {bins[i+1]}{")" if i < len(bins)-2 else "]"}',
                 ha='center', va='bottom', fontsize=10,
                 bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

    plt.ylim(0, max(n) * 1.5)
    plt.show()

    print("=" * 70)
    print("BIN EDGES DEMONSTRATION")
    print("=" * 70)
    print(f"Data: {data_simple}")
    print(f"Bin edges: {bins}")
    print(f"Counts: {n}")
    print()
    for i in range(len(bins) - 1):
        bracket = ")" if i < len(bins) - 2 else "]"
        print(f"Bin {i}: [{bins[i]}, {bins[i+1]}{bracket} contains {int(n[i])} values")

    # Calculate bin centers from edges
    bin_centers = (bins[:-1] + bins[1:]) / 2
    print(f"\nBin centers (calculated): {bin_centers}")

    # ============================================================================
    # SECTION 6: density=False vs density=True - THE CRITICAL DIFFERENCE
    # ============================================================================

    """
    density=False (default):
    -----------------------
    - Y-axis shows COUNTS (frequency)
    - Each bar height = number of data points in that bin
    - Sum of all bar heights = total number of data points
    - Units: "number of observations"

    density=True:
    ------------
    - Y-axis shows PROBABILITY DENSITY
    - Each bar represents density, not count
    - AREA of each bar = probability that a value falls in that bin
    - Total area under histogram = 1.0
    - Units: "probability per unit on x-axis"

    CRITICAL FORMULA:
    For each bin:
        density[i] = count[i] / (total_count × bin_width[i])

    Why normalize this way?
    - Allows comparison of histograms with different sample sizes
    - Allows overlaying with theoretical probability density functions
    - Bins with different widths are properly compared
    """

    np.random.seed(42)
    data = np.random.randn(1000)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # density=False (counts)
    n_count, bins_count, _ = axes[0].hist(data, bins=30, edgecolor='black', alpha=0.7)
    axes[0].set_xlabel('Value')
    axes[0].set_ylabel('Frequency (Count)')
    axes[0].set_title('density=False (Default): Shows Counts')
    axes[0].grid(True, alpha=0.3)

    # Add text showing sum
    total_count = n_count.sum()
    axes[0].text(0.95, 0.95, f'Sum of heights: {total_count:.0f}\n(Total data points)',
                 transform=axes[0].transAxes, ha='right', va='top',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # density=True (probability density)
    n_density, bins_density, _ = axes[1].hist(data, bins=30, density=True, 
                                               edgecolor='black', alpha=0.7)
    axes[1].set_xlabel('Value')
    axes[1].set_ylabel('Probability Density')
    axes[1].set_title('density=True: Shows Probability Density')
    axes[1].grid(True, alpha=0.3)

    # Calculate total area (should be close to 1.0)
    bin_widths = np.diff(bins_density)
    total_area = (n_density * bin_widths).sum()
    axes[1].text(0.95, 0.95, f'Total area: {total_area:.4f}\n(Should be ≈ 1.0)',
                 transform=axes[1].transAxes, ha='right', va='top',
                 bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

    plt.tight_layout()
    plt.show()

    print("=" * 70)
    print("DENSITY=FALSE VS DENSITY=TRUE")
    print("=" * 70)
    print(f"With density=False:")
    print(f"  Max height: {n_count.max():.1f}")
    print(f"  Sum of heights: {n_count.sum():.1f}")
    print()
    print(f"With density=True:")
    print(f"  Max height: {n_density.max():.4f}")
    print(f"  Total area: {total_area:.4f}")
    print()
    print("Note: With density=True, the area (not height) sums to 1.0")

    # ============================================================================
    # SECTION 7: Why density=True is Important - Overlaying Distributions
    # ============================================================================

    """
    density=True is essential when:
    1. Comparing histograms with different sample sizes
    2. Overlaying theoretical probability density functions (PDFs)
    3. Making probability statements about data
    """

    # Generate data from normal distribution
    np.random.seed(42)
    data = np.random.randn(1000)

    # Create histogram with density=True
    fig, ax = plt.subplots(figsize=(10, 6))
    n, bins, patches = ax.hist(data, bins=30, density=True, alpha=0.7,
                                edgecolor='black', label='Histogram (data)')

    # Overlay theoretical normal distribution PDF
    x = np.linspace(-4, 4, 1000)
    pdf = (1 / np.sqrt(2 * np.pi)) * np.exp(-x**2 / 2)
    ax.plot(x, pdf, 'r-', linewidth=3, label='Theoretical N(0,1) PDF')

    ax.set_xlabel('Value')
    ax.set_ylabel('Probability Density')
    ax.set_title('Histogram with density=True + Theoretical PDF')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.show()

    print("\nWith density=True, histogram and PDF are on the same scale!")
    print("This allows direct visual comparison with theory.")

    # ============================================================================
    # SECTION 8: Demonstrating the Relationship: Count → Density
    # ============================================================================

    """
    Let's verify the mathematical relationship:
        density[i] = count[i] / (N × bin_width[i])
    where N = total number of data points
    """

    np.random.seed(42)
    data = np.random.randn(1000)
    bins = np.linspace(-3, 3, 13)  # 12 bins

    # Get counts
    n_count, bins_edges, _ = plt.hist(data, bins=bins, density=False)
    plt.close()

    # Get density
    n_density, bins_edges, _ = plt.hist(data, bins=bins, density=True)
    plt.close()

    # Manual calculation of density from counts
    N = len(data)
    bin_widths = np.diff(bins_edges)
    n_density_manual = n_count / (N * bin_widths)

    # Verify they match
    print("=" * 70)
    print("VERIFYING COUNT → DENSITY CONVERSION")
    print("=" * 70)
    print(f"Total data points N: {N}")
    print()
    print("Bin | Count | Width | Density (hist) | Density (manual) | Match?")
    print("-" * 70)
    for i in range(len(n_count)):
        match = "✓" if np.isclose(n_density[i], n_density_manual[i]) else "✗"
        print(f"{i:3d} | {n_count[i]:5.0f} | {bin_widths[i]:5.2f} | "
              f"{n_density[i]:14.4f} | {n_density_manual[i]:16.4f} | {match}")

    # ============================================================================
    # SECTION 9: Complete Example - Unpacking and Using All Return Values
    # ============================================================================

    """
    Let's use all three return values: n, bins, patches
    """

    np.random.seed(42)
    data = np.random.randn(1000)

    # Create histogram and unpack all return values
    n, bins, patches = plt.hist(data, bins=30, density=False, edgecolor='black')

    # Use n (heights) to color bars by frequency
    # Normalize colors: high frequency = red, low frequency = blue
    colors = plt.cm.RdYlBu_r(n / n.max())  # RdYlBu_r = Red-Yellow-Blue reversed

    # Update each bar's color using patches
    for patch, color in zip(patches, colors):
        patch.set_facecolor(color)

    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram with Color-Coded Frequency')

    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=plt.cm.RdYlBu_r, 
                                norm=plt.Normalize(vmin=0, vmax=n.max()))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=plt.gca())
    cbar.set_label('Frequency', rotation=270, labelpad=20)

    plt.show()

    # Print statistics using n and bins
    print("=" * 70)
    print("USING HISTOGRAM RETURN VALUES")
    print("=" * 70)
    print(f"Number of bins: {len(n)}")
    print(f"Number of bin edges: {len(bins)}")
    print(f"Total count: {n.sum():.0f}")
    print(f"Max frequency: {n.max():.0f}")
    print(f"Min frequency: {n.min():.0f}")
    print(f"Mean frequency: {n.mean():.1f}")
    print()

    # Find the bin with maximum frequency
    max_bin_idx = n.argmax()
    print(f"Highest frequency bin: Bin {max_bin_idx}")
    print(f"  Range: [{bins[max_bin_idx]:.3f}, {bins[max_bin_idx + 1]:.3f})")
    print(f"  Count: {n[max_bin_idx]:.0f}")

    # ============================================================================
    # SECTION 10: Advanced Histogram Customization
    # ============================================================================

    """
    Additional parameters for customization
    """

    np.random.seed(42)
    data1 = np.random.randn(1000)
    data2 = np.random.randn(800) + 1  # Shifted distribution

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # histtype='bar' (default)
    axes[0, 0].hist(data1, bins=30, histtype='bar', edgecolor='black')
    axes[0, 0].set_title("histtype='bar' (default)")

    # histtype='step' (outline only)
    axes[0, 1].hist(data1, bins=30, histtype='step', linewidth=2)
    axes[0, 1].set_title("histtype='step'")

    # histtype='stepfilled'
    axes[0, 2].hist(data1, bins=30, histtype='stepfilled', alpha=0.7, edgecolor='black')
    axes[0, 2].set_title("histtype='stepfilled'")

    # Overlapping histograms with alpha
    axes[1, 0].hist(data1, bins=30, alpha=0.5, label='Data 1', edgecolor='black')
    axes[1, 0].hist(data2, bins=30, alpha=0.5, label='Data 2', edgecolor='black')
    axes[1, 0].set_title('Overlapping histograms')
    axes[1, 0].legend()

    # Cumulative histogram
    axes[1, 1].hist(data1, bins=30, cumulative=True, edgecolor='black')
    axes[1, 1].set_title('Cumulative histogram')
    axes[1, 1].set_ylabel('Cumulative frequency')

    # Custom colors and edge colors
    axes[1, 2].hist(data1, bins=30, color='skyblue', edgecolor='navy', linewidth=1.5)
    axes[1, 2].set_title('Custom colors')

    for ax in axes.flatten():
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('Value')

    plt.tight_layout()
    plt.show()

    # ============================================================================
    # KEY TAKEAWAYS
    # ============================================================================

    """
    1. hist() creates histograms showing data distribution
    2. Return values: n, bins, patches = hist(...)
       - n: histogram values (counts or densities)
       - bins: bin edges (length = number of bins + 1)
       - patches: bar objects for customization

    3. bins parameter:
       - int: number of equal-width bins
       - list/array: explicit bin edges (can be unequal widths)

    4. bins array contains EDGES, not centers:
       - bins[i] to bins[i+1] defines bin i
       - Length of bins = length of n + 1

    5. density parameter (CRITICAL):
       - density=False: y-axis shows counts
       - density=True: y-axis shows probability density
       - With density=True, total AREA = 1.0

    6. Use density=True when:
       - Overlaying with probability density functions
       - Comparing histograms with different sample sizes
       - Making probability statements

    7. Formula: density[i] = count[i] / (N × bin_width[i])

    8. Common parameters:
       - bins: number or edges
       - density: counts vs probability density
       - range: data range to histogram
       - cumulative: cumulative histogram
       - histtype: 'bar', 'step', 'stepfilled'
       - alpha: transparency
       - color, edgecolor: styling

    9. Use unpacked return values for:
       - Color-coding by frequency
       - Finding mode (most frequent bin)
       - Statistical analysis
       - Custom annotations
    """

    print("\n" + "=" * 70)
    print("SUMMARY: bins PARAMETER")
    print("=" * 70)
    print("bins=10          → 10 equal-width bins")
    print("bins=[0,1,2,5]   → 3 bins with edges at 0,1,2,5")
    print("bins array length = number of bins + 1")
    print()
    print("SUMMARY: density PARAMETER")
    print("=" * 70)
    print("density=False    → Y-axis: counts (frequency)")
    print("density=True     → Y-axis: probability density (area = 1)")
```


---

## Exercises

**Exercise 1.** Write code that generates 1000 samples from a normal distribution with mean 5 and standard deviation 2, and plots a histogram with 30 bins, `density=True`, and `alpha=0.7`.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    data = np.random.normal(5, 2, 1000)

    fig, ax = plt.subplots()
    ax.hist(data, bins=30, density=True, alpha=0.7, color='steelblue',
            edgecolor='black')
    ax.set_xlabel('Value')
    ax.set_ylabel('Density')
    ax.set_title('Histogram')
    plt.show()
    ```

---

**Exercise 2.** Predict the return values of `ax.hist()` when called with `bins=20` on 500 data points. What are the shapes of the returned arrays?

??? success "Solution to Exercise 2"
    `ax.hist()` returns `(n, bins, patches)` where `n` has shape `(20,)` containing the count or density in each bin, `bins` has shape `(21,)` containing the bin edges (one more than the number of bins), and `patches` is a list of 20 Rectangle objects.

---

**Exercise 3.** Create a figure with two subplots. The left subplot shows a histogram of data from a normal distribution. The right subplot shows a histogram of data from an exponential distribution. Use `density=True` on both.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    normal_data = np.random.normal(0, 1, 1000)
    exp_data = np.random.exponential(1, 1000)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    ax1.hist(normal_data, bins=30, density=True, alpha=0.7, color='steelblue')
    ax1.set_title('Normal Distribution')

    ax2.hist(exp_data, bins=30, density=True, alpha=0.7, color='coral')
    ax2.set_title('Exponential Distribution')

    plt.tight_layout()
    plt.show()
    ```

---

**Exercise 4.** Write code that overlays two histograms on the same axes (e.g., two normal distributions with different means) using `alpha=0.5` for transparency, and add a legend to distinguish them.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    data1 = np.random.normal(0, 1, 1000)
    data2 = np.random.normal(3, 1, 1000)

    fig, ax = plt.subplots()
    ax.hist(data1, bins=30, alpha=0.5, label='N(0, 1)', color='blue')
    ax.hist(data2, bins=30, alpha=0.5, label='N(3, 1)', color='red')
    ax.legend()
    ax.set_title('Overlaid Histograms')
    plt.show()
    ```
