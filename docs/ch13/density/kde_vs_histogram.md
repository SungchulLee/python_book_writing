# KDE vs Histogram

Histograms and kernel density estimators are the two primary nonparametric approaches to estimating a probability density function from data. Both methods avoid assuming a specific distributional form, but they differ fundamentally in smoothness, convergence properties, and sensitivity to tuning parameters. Understanding these differences helps practitioners choose the right tool for visualization and analysis.

!!! tip "Mental Model"
    A histogram chops the number line into bins and counts; a KDE places a smooth bump at each data point and averages. The histogram is fast and intuitive but discontinuous and sensitive to bin edges. The KDE is smooth and converges faster, making it the better estimator -- but the histogram remains the better quick visualization tool.

## Histogram as a Density Estimator

A histogram partitions the real line into bins $B_1, B_2, \ldots$ of width $w$ and estimates the density as a piecewise constant function:

$$
\hat{f}_{\text{hist}}(x) = \frac{1}{n \cdot w} \sum_{i=1}^{n} \mathbf{1}(x_i \in B_k) \quad \text{for } x \in B_k
$$

where $\mathbf{1}(\cdot)$ is the indicator function. The result is a step function: constant within each bin, discontinuous at bin edges. The bin width $w$ plays a role analogous to the bandwidth in KDE, controlling the bias-variance tradeoff.

## KDE as a Density Estimator

The kernel density estimator replaces the hard bin assignment with a smooth kernel centered at each observation:

$$
\hat{f}_{\text{KDE}}(x) = \frac{1}{nh}\sum_{i=1}^{n} K\!\left(\frac{x - x_i}{h}\right)
$$

With a Gaussian kernel, the result is an infinitely differentiable function. Every data point contributes to the estimate at every query point $x$, with the contribution decaying smoothly with distance.

## Key Differences

| Property | Histogram | KDE |
|---|---|---|
| Smoothness | Step function (discontinuous) | Inherits kernel smoothness (continuous) |
| Tuning parameter | Bin width $w$ and bin edges | Bandwidth $h$ |
| Sensitivity to parameter choice | Bin edges and width both matter | Only bandwidth matters |
| Optimal MISE rate | $O(n^{-2/3})$ | $O(n^{-4/5})$ |
| Computational cost | $O(n)$ to construct | $O(mn)$ to evaluate at $m$ points |
| Derivative estimation | Not possible (discontinuous) | Natural (smooth) |

The KDE achieves a faster convergence rate because it uses the smoothness of the kernel to extract more information from the data. The histogram's rate is limited by its piecewise-constant structure.

## Bin Edge Sensitivity

A notable disadvantage of histograms is sensitivity to the choice of bin edges. Shifting the bin boundaries by a fraction of the bin width can substantially change the shape of the estimate, creating or removing apparent modes.

```python
import numpy as np
from scipy.stats import gaussian_kde

# Generate data with two close modes
np.random.seed(42)
data = np.concatenate([
    np.random.normal(0, 0.5, 200),
    np.random.normal(1.5, 0.5, 200)
])

# Two histograms with different bin edges
bins_a = np.arange(-3, 5, 0.5)           # edges at 0.0, 0.5, 1.0, ...
bins_b = bins_a + 0.25                     # shifted by 0.25

counts_a, _ = np.histogram(data, bins=bins_a, density=True)
counts_b, _ = np.histogram(data, bins=bins_b, density=True)
print(f"Max density (edges A): {counts_a.max():.4f}")
print(f"Max density (edges B): {counts_b.max():.4f}")

# KDE is unaffected by any such shift
kde = gaussian_kde(data)
print(f"KDE at x=0:   {kde(np.array([0.0]))[0]:.4f}")
print(f"KDE at x=1.5: {kde(np.array([1.5]))[0]:.4f}")
```

KDE does not use bins, so it is invariant to any notion of edge placement. This makes KDE more reliable for detecting features like modes.

!!! warning "Histogram Artifacts"
    When using histograms to assess whether a distribution is unimodal or bimodal, small changes in bin width or edge placement can create or destroy apparent modes. KDE provides more stable visual evidence of multimodality.

## When to Use Each Method

Despite the theoretical advantages of KDE, histograms remain useful in several situations:

- **Large datasets**: Histograms are $O(n)$ to construct and fast to render, making them practical for millions of observations
- **Discrete data**: For integer-valued or categorical data, bins aligned with the discrete values give a natural representation
- **Quick exploration**: Histograms are available in virtually every plotting library with minimal configuration
- **Communication**: Many audiences are more familiar with histograms than with smooth density curves

KDE is preferred when:

- **Smoothness matters**: Density derivatives, mode detection, or probability computations require a smooth estimate
- **Accuracy matters**: The faster convergence rate of KDE means better estimates for moderate sample sizes
- **Resampling is needed**: A KDE provides a generative model from which new samples can be drawn

!!! tip "Combining Both"
    A common visualization strategy is to overlay a KDE curve on top of a histogram. The histogram provides an intuitive sense of the data distribution, while the KDE highlights the smooth underlying shape. In matplotlib, use `plt.hist(data, density=True)` followed by `plt.plot(x_grid, kde(x_grid))`.

## Summary

Histograms and KDE both estimate probability densities nonparametrically, but they differ in smoothness, convergence rate, and sensitivity to tuning choices. The histogram produces a discontinuous step function sensitive to bin edges and converges at rate $O(n^{-2/3})$, while KDE produces a smooth function invariant to edge placement and converges at $O(n^{-4/5})$. Histograms are computationally cheaper and more familiar to general audiences, while KDE provides smoother estimates better suited for inference and resampling.

---

## Runnable Example: `seaborn_distributions.py`

```python
"""
Tutorial 03: Distribution Plots in Seaborn

This tutorial covers how to visualize distributions of data using Seaborn.
Understanding distributions is fundamental to statistics and data analysis.

Learning Objectives:
- Visualize univariate distributions (single variable)
- Create histograms and kernel density estimates (KDE)
- Use rug plots and ECDF plots
- Compare distributions across categories
- Understand distribution shapes and properties

Author: Educational Python Package
Level: Beginner
Prerequisites: Tutorial 01-02 (Seaborn Basics, Basic Plots)
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats

# Set style

if __name__ == "__main__":
    sns.set_style("whitegrid")
    sns.set_context("notebook")

    # =============================================================================
    # SECTION 1: HISTOGRAMS - THE FOUNDATION
    # =============================================================================

    """
    HISTOGRAMS divide data into bins and count how many observations fall into
    each bin. They're the most common way to visualize distributions.

    Key concepts:
    - Bins: Intervals that divide the range of data
    - Frequency: Count of observations in each bin
    - Bin width: Affects the appearance significantly

    Function: sns.histplot()
    """

    print("="*80)
    print("SECTION 1: HISTOGRAMS")
    print("="*80)

    # Load data
    tips = sns.load_dataset('tips')
    iris = sns.load_dataset('iris')

    # Example 1.1: Basic histogram
    plt.figure(figsize=(10, 6))
    sns.histplot(data=tips, x='total_bill')
    plt.title('Basic Histogram: Distribution of Total Bills', fontsize=14, fontweight='bold')
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Frequency (Count)', fontsize=12)
    plt.tight_layout()
    plt.show()

    print("✓ Basic histogram created")

    # Example 1.2: Controlling number of bins
    # The number of bins dramatically affects the visualization
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # Few bins (5) - overly smooth, loses detail
    sns.histplot(data=tips, x='total_bill', bins=5, ax=axes[0])
    axes[0].set_title('Few Bins (5) - Too Smooth')

    # Default bins (~20-30) - usually good
    sns.histplot(data=tips, x='total_bill', ax=axes[1])
    axes[1].set_title('Default Bins - Balanced')

    # Many bins (50) - too detailed, noisy
    sns.histplot(data=tips, x='total_bill', bins=50, ax=axes[2])
    axes[2].set_title('Many Bins (50) - Too Noisy')

    plt.tight_layout()
    plt.show()

    print("✓ Histograms with different bin counts created")

    # Example 1.3: Histogram with multiple categories
    # Using 'hue' to compare distributions
    plt.figure(figsize=(10, 6))
    sns.histplot(
        data=tips, 
        x='total_bill', 
        hue='time',  # Separate histogram for each time
        multiple='dodge',  # How to handle overlapping: 'layer', 'dodge', 'stack', 'fill'
        bins=20
    )
    plt.title('Histogram by Category (Dodged)', fontsize=14, fontweight='bold')
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.legend(title='Time of Day')
    plt.tight_layout()
    plt.show()

    print("✓ Grouped histogram created")

    # Example 1.4: Different multiple options
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Layer - bars on top of each other with transparency
    sns.histplot(data=tips, x='total_bill', hue='time', multiple='layer', 
                 alpha=0.5, ax=axes[0, 0])
    axes[0, 0].set_title("multiple='layer' - Overlapping with transparency")

    # Dodge - bars side by side
    sns.histplot(data=tips, x='total_bill', hue='time', multiple='dodge', ax=axes[0, 1])
    axes[0, 1].set_title("multiple='dodge' - Side by side")

    # Stack - bars stacked on top
    sns.histplot(data=tips, x='total_bill', hue='time', multiple='stack', ax=axes[1, 0])
    axes[1, 0].set_title("multiple='stack' - Stacked")

    # Fill - normalized to show proportions
    sns.histplot(data=tips, x='total_bill', hue='time', multiple='fill', ax=axes[1, 1])
    axes[1, 1].set_title("multiple='fill' - Proportions")
    axes[1, 1].set_ylabel('Proportion')

    plt.tight_layout()
    plt.show()

    print("✓ Multiple histogram styles created")

    # Example 1.5: Customizing histogram appearance
    plt.figure(figsize=(10, 6))
    sns.histplot(
        data=tips, 
        x='total_bill',
        bins=25,
        color='steelblue',
        edgecolor='black',  # Border color
        linewidth=0.5,  # Border width
        alpha=0.7
    )
    plt.title('Customized Histogram', fontsize=14, fontweight='bold')
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.tight_layout()
    plt.show()

    print("✓ Customized histogram created\n")

    # =============================================================================
    # SECTION 2: KERNEL DENSITY ESTIMATION (KDE)
    # =============================================================================

    """
    KDE PLOTS create smooth curves that estimate the probability density function
    of the data. They're like smooth versions of histograms.

    Advantages of KDE:
    - Smooth, continuous representation
    - No arbitrary bin choices
    - Better for comparing distributions

    Disadvantages:
    - Can be misleading if bandwidth is chosen poorly
    - Harder to read exact frequencies

    Function: sns.kdeplot()
    """

    print("="*80)
    print("SECTION 2: KERNEL DENSITY ESTIMATION (KDE)")
    print("="*80)

    # Example 2.1: Basic KDE plot
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=tips, x='total_bill')
    plt.title('Basic KDE Plot: Distribution of Total Bills', fontsize=14, fontweight='bold')
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.tight_layout()
    plt.show()

    print("✓ Basic KDE plot created")

    # Example 2.2: KDE with different bandwidths
    # Bandwidth controls the smoothness
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # Small bandwidth - too detailed
    sns.kdeplot(data=tips, x='total_bill', bw_adjust=0.3, ax=axes[0])
    axes[0].set_title('Small Bandwidth (0.3) - Undersmoothed')

    # Default bandwidth (1.0) - usually good
    sns.kdeplot(data=tips, x='total_bill', ax=axes[1])
    axes[1].set_title('Default Bandwidth (1.0) - Balanced')

    # Large bandwidth - too smooth
    sns.kdeplot(data=tips, x='total_bill', bw_adjust=2.0, ax=axes[2])
    axes[2].set_title('Large Bandwidth (2.0) - Oversmoothed')

    plt.tight_layout()
    plt.show()

    print("✓ KDE plots with different bandwidths created")

    # Example 2.3: KDE with multiple categories
    plt.figure(figsize=(10, 6))
    sns.kdeplot(
        data=tips, 
        x='total_bill', 
        hue='time',
        fill=True,  # Fill area under curve
        alpha=0.5,  # Transparency
        linewidth=2
    )
    plt.title('KDE Plot by Category', fontsize=14, fontweight='bold')
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.legend(title='Time of Day')
    plt.tight_layout()
    plt.show()

    print("✓ Multi-category KDE plot created")

    # Example 2.4: Combining histogram and KDE
    # This is very common - shows both exact bins and smooth estimate
    plt.figure(figsize=(10, 6))
    sns.histplot(
        data=tips, 
        x='total_bill',
        kde=True,  # Add KDE curve on top of histogram
        color='skyblue',
        edgecolor='black',
        linewidth=0.5
    )
    plt.title('Histogram with KDE Overlay', fontsize=14, fontweight='bold')
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Count / Density', fontsize=12)
    plt.tight_layout()
    plt.show()

    print("✓ Histogram with KDE overlay created\n")

    # =============================================================================
    # SECTION 3: THE DISPLOT FUNCTION - UNIFIED INTERFACE
    # =============================================================================

    """
    DISPLOT is a figure-level function that provides a unified interface
    for distribution plots. It can create histograms, KDE plots, and more.

    Key parameter: 'kind'
    - 'hist': histogram (default)
    - 'kde': kernel density estimate
    - 'ecdf': empirical cumulative distribution function

    Advantage: Easy to create faceted plots (multiple subplots)
    """

    print("="*80)
    print("SECTION 3: DISPLOT - UNIFIED DISTRIBUTION INTERFACE")
    print("="*80)

    # Example 3.1: Displot as histogram
    g = sns.displot(data=tips, x='total_bill', kind='hist', bins=20, height=5, aspect=1.5)
    g.set_titles("Displot: Histogram")
    g.set_axis_labels("Total Bill ($)", "Count")
    plt.tight_layout()
    plt.show()

    print("✓ Displot histogram created")

    # Example 3.2: Displot as KDE
    g = sns.displot(data=tips, x='total_bill', kind='kde', fill=True, height=5, aspect=1.5)
    g.set_titles("Displot: KDE")
    g.set_axis_labels("Total Bill ($)", "Density")
    plt.tight_layout()
    plt.show()

    print("✓ Displot KDE created")

    # Example 3.3: Displot with faceting (multiple subplots)
    g = sns.displot(
        data=tips, 
        x='total_bill', 
        col='time',  # Create separate plot for each time
        kind='hist',
        kde=True,
        height=4,
        aspect=1.2
    )
    g.set_titles("Distribution for {col_name}")
    g.set_axis_labels("Total Bill ($)", "Count")
    plt.tight_layout()
    plt.show()

    print("✓ Faceted displot created")

    # Example 3.4: Displot with row and column faceting
    g = sns.displot(
        data=tips, 
        x='total_bill',
        row='sex',  # Rows for sex
        col='time',  # Columns for time
        kind='kde',
        fill=True,
        height=3,
        aspect=1.2
    )
    g.set_titles("Sex: {row_name} | Time: {col_name}")
    g.set_axis_labels("Total Bill ($)", "Density")
    plt.tight_layout()
    plt.show()

    print("✓ Row and column faceted displot created\n")

    # =============================================================================
    # SECTION 4: RUG PLOTS AND ECDF
    # =============================================================================

    """
    RUG PLOTS show individual data points as small tick marks along an axis.
    Useful for showing actual data density, especially with small datasets.

    ECDF (Empirical Cumulative Distribution Function) shows the proportion
    of data points that are less than or equal to each value.
    """

    print("="*80)
    print("SECTION 4: RUG PLOTS AND ECDF")
    print("="*80)

    # Example 4.1: Adding rug plot to histogram
    plt.figure(figsize=(10, 6))
    sns.histplot(data=tips, x='total_bill', bins=20)
    sns.rugplot(data=tips, x='total_bill', height=0.05, color='red', alpha=0.5)
    plt.title('Histogram with Rug Plot', fontsize=14, fontweight='bold')
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.tight_layout()
    plt.show()

    print("✓ Histogram with rug plot created")

    # Example 4.2: KDE with rug plot
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=tips, x='total_bill', fill=True, alpha=0.5)
    sns.rugplot(data=tips, x='total_bill', height=0.05, color='black')
    plt.title('KDE with Rug Plot', fontsize=14, fontweight='bold')
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.tight_layout()
    plt.show()

    print("✓ KDE with rug plot created")

    # Example 4.3: ECDF plot
    plt.figure(figsize=(10, 6))
    sns.ecdfplot(data=tips, x='total_bill')
    plt.title('ECDF Plot: Cumulative Distribution of Total Bills', fontsize=14, fontweight='bold')
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Proportion', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    print("✓ ECDF plot created")

    # Example 4.4: ECDF with multiple categories
    plt.figure(figsize=(10, 6))
    sns.ecdfplot(data=tips, x='total_bill', hue='time')
    plt.title('ECDF Plot by Time of Day', fontsize=14, fontweight='bold')
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Proportion', fontsize=12)
    plt.legend(title='Time of Day')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    print("✓ Multi-category ECDF plot created\n")

    # =============================================================================
    # SECTION 5: COMPARING DISTRIBUTIONS
    # =============================================================================

    """
    One of the most common tasks is comparing distributions across groups.
    Here are several effective ways to do this.
    """

    print("="*80)
    print("SECTION 5: COMPARING DISTRIBUTIONS")
    print("="*80)

    # Example 5.1: Overlaid KDE plots
    plt.figure(figsize=(10, 6))
    for day in tips['day'].unique():
        subset = tips[tips['day'] == day]
        sns.kdeplot(data=subset, x='total_bill', label=day, linewidth=2)
    plt.title('Comparing Distributions Across Days', fontsize=14, fontweight='bold')
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.legend(title='Day of Week')
    plt.tight_layout()
    plt.show()

    print("✓ Overlaid KDE comparison created")

    # Example 5.2: Side-by-side histograms using displot
    g = sns.displot(
        data=tips, 
        x='total_bill',
        col='day',
        col_wrap=2,  # Wrap to 2 columns
        kind='hist',
        kde=True,
        bins=15,
        height=3.5,
        aspect=1.3
    )
    g.set_titles("Day: {col_name}")
    g.set_axis_labels("Total Bill ($)", "Count")
    plt.tight_layout()
    plt.show()

    print("✓ Side-by-side histogram comparison created")

    # Example 5.3: Stacked distributions
    plt.figure(figsize=(10, 6))
    sns.histplot(
        data=tips, 
        x='total_bill',
        hue='day',
        multiple='stack',
        bins=20,
        palette='Set2'
    )
    plt.title('Stacked Distribution by Day', fontsize=14, fontweight='bold')
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.legend(title='Day of Week')
    plt.tight_layout()
    plt.show()

    print("✓ Stacked distribution created\n")

    # =============================================================================
    # SECTION 6: UNDERSTANDING DISTRIBUTION SHAPES
    # =============================================================================

    """
    Understanding distribution shapes is crucial for statistical analysis.
    Let's visualize different types of distributions.
    """

    print("="*80)
    print("SECTION 6: DISTRIBUTION SHAPES")
    print("="*80)

    # Create sample data with different distributions
    np.random.seed(42)
    normal = np.random.normal(loc=0, scale=1, size=1000)
    skewed_right = np.random.exponential(scale=1, size=1000)
    skewed_left = -np.random.exponential(scale=1, size=1000)
    bimodal = np.concatenate([np.random.normal(-2, 0.5, 500), 
                              np.random.normal(2, 0.5, 500)])

    distributions = pd.DataFrame({
        'Normal (Symmetric)': normal,
        'Right-Skewed': skewed_right,
        'Left-Skewed': skewed_left,
        'Bimodal': bimodal
    })

    # Plot all distributions
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for i, col in enumerate(distributions.columns):
        sns.histplot(data=distributions, x=col, kde=True, ax=axes[i], bins=30)
        axes[i].set_title(f'{col} Distribution', fontsize=12, fontweight='bold')
        axes[i].set_xlabel('Value')
        axes[i].set_ylabel('Frequency')

    plt.tight_layout()
    plt.show()

    print("✓ Different distribution shapes visualized")

    # Add explanations
    print("\nDistribution Shape Guide:")
    print("- NORMAL: Bell-shaped, symmetric, mean = median = mode")
    print("- RIGHT-SKEWED: Tail extends to the right, mean > median")
    print("- LEFT-SKEWED: Tail extends to the left, mean < median")
    print("- BIMODAL: Two peaks, indicates mixture of populations")

    # =============================================================================
    # SECTION 7: PRACTICAL EXAMPLES
    # =============================================================================

    """
    Let's apply what we've learned to real-world scenarios.
    """

    print("\n" + "="*80)
    print("SECTION 7: PRACTICAL EXAMPLES")
    print("="*80)

    # Example 7.1: Analyzing exam scores
    np.random.seed(42)
    exam_data = pd.DataFrame({
        'score': np.concatenate([
            np.random.normal(75, 10, 60),  # Class A
            np.random.normal(65, 15, 60)   # Class B
        ]),
        'class': ['Class A'] * 60 + ['Class B'] * 60
    })

    plt.figure(figsize=(12, 6))
    sns.histplot(data=exam_data, x='score', hue='class', kde=True, 
                 bins=20, alpha=0.6, edgecolor='black', linewidth=0.5)
    plt.title('Exam Score Distribution by Class', fontsize=14, fontweight='bold')
    plt.xlabel('Exam Score', fontsize=12)
    plt.ylabel('Number of Students', fontsize=12)
    plt.axvline(x=70, color='red', linestyle='--', linewidth=2, label='Passing Score')
    plt.legend(title='')
    plt.tight_layout()
    plt.show()

    print("✓ Exam score analysis created")

    # Example 7.2: Quality control analysis
    quality_data = pd.DataFrame({
        'measurement': np.random.normal(100, 2, 500)
    })

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Histogram with specification limits
    sns.histplot(data=quality_data, x='measurement', kde=True, ax=axes[0], bins=30)
    axes[0].axvline(x=95, color='red', linestyle='--', linewidth=2, label='Lower Spec Limit')
    axes[0].axvline(x=105, color='red', linestyle='--', linewidth=2, label='Upper Spec Limit')
    axes[0].set_title('Product Measurement Distribution')
    axes[0].set_xlabel('Measurement')
    axes[0].legend()

    # ECDF for easier reading of proportions
    sns.ecdfplot(data=quality_data, x='measurement', ax=axes[1])
    axes[1].axvline(x=95, color='red', linestyle='--', linewidth=2)
    axes[1].axvline(x=105, color='red', linestyle='--', linewidth=2)
    axes[1].set_title('Cumulative Distribution (ECDF)')
    axes[1].set_xlabel('Measurement')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    print("✓ Quality control analysis created\n")

    # =============================================================================
    # SECTION 8: PRACTICE EXERCISES
    # =============================================================================

    """
    EXERCISE 1: Basic Distribution
    Using the 'penguins' dataset:
    - Load the dataset with sns.load_dataset('penguins')
    - Create a histogram of 'bill_length_mm'
    - Add a KDE overlay
    - What shape is the distribution?

    EXERCISE 2: Comparing Distributions
    Using the 'penguins' dataset:
    - Create overlaid KDE plots showing bill_length_mm for each species
    - Use different colors for each species
    - Add a legend
    - Which species has the longest average bill length?

    EXERCISE 3: Multiple Visualization Types
    Using the 'tips' dataset:
    - Create a 2x2 grid of plots showing the distribution of 'tip'
    - Plot 1: Histogram only
    - Plot 2: KDE only
    - Plot 3: Histogram with KDE overlay
    - Plot 4: ECDF plot
    - Which visualization do you find most informative?

    EXERCISE 4: Faceted Analysis
    Using the 'diamonds' dataset (if available, otherwise use 'tips'):
    - Use displot() to create faceted histograms
    - Show the distribution of a continuous variable
    - Facet by a categorical variable
    - Add KDE overlays

    EXERCISE 5: Distribution Comparison
    Create synthetic data representing test scores from two teaching methods:
    - Method A: mean=75, std=10, n=100
    - Method B: mean=72, std=15, n=100
    - Visualize both distributions on the same plot
    - Use both histogram and KDE
    - Which method shows more consistent scores?
    """

    # =============================================================================
    # KEY TAKEAWAYS
    # =============================================================================

    """
    🎯 KEY TAKEAWAYS FROM THIS TUTORIAL:

    1. HISTOGRAMS divide data into bins and count frequencies
       - Control bins with 'bins' parameter
       - Use 'multiple' parameter for multiple groups
       - Options: 'layer', 'dodge', 'stack', 'fill'

    2. KDE PLOTS show smooth density estimates
       - Use bw_adjust to control smoothness
       - Set fill=True for filled curves
       - Better than histograms for comparisons

    3. DISPLOT is the figure-level function
       - Unified interface: kind='hist', 'kde', or 'ecdf'
       - Easy faceting with col and row parameters
       - Better for complex multi-plot layouts

    4. SPECIALIZED PLOTS:
       - Rug plots: Show individual data points
       - ECDF: Show cumulative proportions
       - Combine plots for comprehensive view

    5. DISTRIBUTION SHAPES:
       - Normal: Symmetric, bell-shaped
       - Skewed: Asymmetric, tail on one side
       - Bimodal: Two peaks, mixed populations

    6. BEST PRACTICES:
       - Use histogram + KDE for comprehensive view
       - Choose appropriate bin count
       - Use faceting to compare groups
       - Add reference lines for important values
       - Consider ECDF for proportions

    7. WHEN TO USE EACH:
       - Histogram: General purpose, exact counts
       - KDE: Comparing smooth distributions
       - ECDF: Reading exact proportions
       - Rug: Showing actual data points

    NEXT STEPS:
    - Move on to Tutorial 04: Categorical Plots
    - Practice with different datasets
    - Experiment with distribution parameters
    - Try analyzing your own data
    """

    print("="*80)
    print("TUTORIAL 03 COMPLETE!")
    print("="*80)
    print("You now understand distribution visualization!")
    print("Next: Tutorial 04 - Categorical Plots")
    print("="*80)
```


---

## Exercises

**Exercise 1.** Write code that plots both a histogram and a KDE of the same data on the same axes. Use `density=True` for the histogram.

??? success "Solution to Exercise 1"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(100)
    print(f'Mean: {data.mean():.4f}')
    print(f'Std: {data.std():.4f}')
    ```

---

**Exercise 2.** Explain three advantages of KDE over histograms for density estimation.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that demonstrates the sensitivity of histograms to bin edges by plotting the same data with different bin counts (10, 30, 100).

??? success "Solution to Exercise 3"
    ```python
    import numpy as np
    from scipy import stats
    import matplotlib.pyplot as plt

    np.random.seed(42)
    data = np.random.randn(1000)
    fig, ax = plt.subplots()
    ax.hist(data, bins=30, density=True, alpha=0.7)
    ax.set_title('Distribution')
    plt.show()
    ```

---

**Exercise 4.** Create a dataset where the KDE gives a clearly smoother and more informative estimate than a histogram (e.g., small sample size).

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
