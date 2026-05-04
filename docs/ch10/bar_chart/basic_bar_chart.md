# Basic Bar Chart

Bar charts display categorical data with rectangular bars, where bar length represents the value for each category.

!!! tip "Mental Model"
    `ax.bar(categories, values)` draws one rectangle per category, with height proportional to the value. Think of it as a scatter plot for categorical x-axes -- instead of dots, you get bars that make magnitude differences visually obvious. Use `ax.barh()` for horizontal bars when category labels are long.

!!! note "When to Use Bar Charts"
    Bar charts are for **discrete comparison**, not continuous relationships. Choose your plot type by the question you are answering:

    | Question | Plot |
    |----------|------|
    | How do categories compare? | **Bar chart** |
    | How does a value change over a continuous domain? | Line plot |
    | What is the relationship between two variables? | Scatter plot |
    | How is a single variable distributed? | Histogram |

    If your x-axis is categorical (names, groups, labels), bars are almost always the right choice.

!!! info "Why Bar Charts Are So Effective"
    Bar charts encode value as **length**, which is one of the most accurate visual channels humans have. We compare lengths far more precisely than areas (pie charts), angles, or colors. This perceptual advantage is why bar charts remain the default for categorical comparison.

!!! warning "Readability Limits"
    - **More than ~10 categories** → the chart becomes cluttered and hard to read. Consider grouping, filtering, or switching to a horizontal layout.
    - **Long category labels** → use `ax.barh()` (horizontal bars) so labels read naturally left-to-right.

## Simple Bar Chart

Create a basic vertical bar chart with `ax.bar()`.

### 1. Import and Setup

```python
import matplotlib.pyplot as plt
import numpy as np
```

### 2. Define Categories and Values

```python
categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 56, 78, 32]
```

### 3. Create Bar Chart

```python
fig, ax = plt.subplots()
ax.bar(categories, values)
ax.set_xlabel('Category')
ax.set_ylabel('Value')
ax.set_title('Basic Bar Chart')
plt.show()
```

## Horizontal Bar Chart

Use `ax.barh()` for horizontal orientation.

### 1. Basic Horizontal Bars

```python
fig, ax = plt.subplots()
ax.barh(categories, values)
ax.set_xlabel('Value')
ax.set_ylabel('Category')
plt.show()
```

### 2. Long Category Names

```python
categories = ['Category Alpha', 'Category Beta', 'Category Gamma', 
              'Category Delta', 'Category Epsilon']
values = [23, 45, 56, 78, 32]

fig, ax = plt.subplots()
ax.barh(categories, values)
plt.tight_layout()
plt.show()
```

### 3. Reversed Order

```python
fig, ax = plt.subplots()
ax.barh(categories[::-1], values[::-1])
plt.show()
```

## Pandas Plot Method

Use DataFrame's built-in plotting for quick visualizations.

### 1. Single Column

```python
import pandas as pd

data = {'Courses': ['Language', 'History', 'Math', 'Chemistry', 'Physics'],
        'Number of Teachers': [7, 3, 9, 3, 4]}
df = pd.DataFrame(data).set_index('Courses')

fig, ax = plt.subplots(figsize=(12, 3))
df.plot(kind='bar', ax=ax)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.show()
```

### 2. Multiple Columns

```python
data = {'Student': ['Brandon', 'Vanessa', 'Daniel', 'Kevin', 'William'],
        'Midterm': [85, 60, 60, 65, 100],
        'Final': [90, 90, 65, 80, 95]}
df = pd.DataFrame(data).set_index('Student')

fig, ax = plt.subplots(figsize=(12, 3))
df.plot(kind='bar', ax=ax)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.show()
```

### 3. Horizontal with Pandas

```python
fig, ax = plt.subplots(figsize=(12, 3))
df.plot(kind='barh', ax=ax)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.show()
```

## Numeric X-Axis

Use numeric positions instead of categorical labels.

### 1. Integer Positions

```python
x = np.arange(5)
values = [23, 45, 56, 78, 32]

fig, ax = plt.subplots()
ax.bar(x, values)
ax.set_xticks(x)
ax.set_xticklabels(['A', 'B', 'C', 'D', 'E'])
plt.show()
```

### 2. Custom Spacing

```python
x = [0, 1, 3, 4, 6]  # Non-uniform spacing
values = [23, 45, 56, 78, 32]

fig, ax = plt.subplots()
ax.bar(x, values, width=0.8)
plt.show()
```

### 3. Centered Labels

```python
x = np.arange(5)
fig, ax = plt.subplots()
ax.bar(x, values)
ax.set_xticks(x)
ax.set_xticklabels(['A', 'B', 'C', 'D', 'E'], ha='center')
plt.show()
```

## Data Sources

Various ways to provide data to bar charts.

### 1. Lists

```python
categories = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
values = [10, 25, 15, 30, 20]
ax.bar(categories, values)
```

### 2. NumPy Arrays

```python
x = np.arange(5)
values = np.array([10, 25, 15, 30, 20])
ax.bar(x, values)
```

### 3. Pandas DataFrame

```python
import pandas as pd

df = pd.DataFrame({
    'day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
    'sales': [10, 25, 15, 30, 20]
})

fig, ax = plt.subplots()
ax.bar(df['day'], df['sales'])
plt.show()
```

## Adding Value Labels

Display values on top of bars.

### 1. Text Annotation

```python
fig, ax = plt.subplots()
bars = ax.bar(categories, values)

for bar, value in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            str(value), ha='center', va='bottom')

plt.show()
```

### 2. Using bar_label

```python
fig, ax = plt.subplots()
bars = ax.bar(categories, values)
ax.bar_label(bars)
plt.show()
```

### 3. Formatted Labels

```python
fig, ax = plt.subplots()
bars = ax.bar(categories, values)
ax.bar_label(bars, fmt='%.1f', padding=3)
plt.show()
```

## Sorted Bar Charts

Order bars by value for better visualization.

### 1. Ascending Order

```python
categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 56, 78, 32]

sorted_idx = np.argsort(values)
sorted_categories = [categories[i] for i in sorted_idx]
sorted_values = [values[i] for i in sorted_idx]

fig, ax = plt.subplots()
ax.barh(sorted_categories, sorted_values)
plt.show()
```

### 2. Descending Order

```python
sorted_idx = np.argsort(values)[::-1]
sorted_categories = [categories[i] for i in sorted_idx]
sorted_values = [values[i] for i in sorted_idx]

fig, ax = plt.subplots()
ax.barh(sorted_categories, sorted_values)
plt.show()
```

### 3. Pandas Sorting

```python
df = pd.DataFrame({'category': categories, 'value': values})
df_sorted = df.sort_values('value', ascending=True)

fig, ax = plt.subplots()
ax.barh(df_sorted['category'], df_sorted['value'])
plt.show()
```

## Practical Example

Create a complete bar chart with styling.

### 1. Prepare Data

```python
products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
sales = [150, 230, 180, 310, 275]
```

### 2. Create Styled Chart

```python
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(products, sales, color='steelblue', edgecolor='navy', linewidth=1.5)

ax.set_xlabel('Product', fontsize=12)
ax.set_ylabel('Sales ($K)', fontsize=12)
ax.set_title('Quarterly Sales by Product', fontsize=14)
ax.set_ylim(0, max(sales) * 1.15)
```

### 3. Add Annotations

```python
ax.bar_label(bars, fmt='$%.0fK', padding=3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Runnable Example: `seaborn_categorical_plots.py`

```python
"""
Tutorial 04: Categorical Plots in Seaborn

This tutorial covers plots designed specifically for categorical data.
These plots help compare distributions and values across different categories.

Learning Objectives:
- Create box plots and violin plots
- Use strip plots and swarm plots
- Build point plots and count plots
- Understand when to use each categorical plot
- Combine multiple plot types

Author: Educational Python Package
Level: Intermediate
Prerequisites: Tutorial 01-03
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

if __name__ == "__main__":

    sns.set_style("whitegrid")
    sns.set_context("notebook")

    # =============================================================================
    # SECTION 1: BOX PLOTS - SHOWING DISTRIBUTION SUMMARY
    # =============================================================================

    """
    BOX PLOTS display the five-number summary:
    - Minimum (excluding outliers)
    - First quartile (Q1, 25th percentile)
    - Median (Q2, 50th percentile)
    - Third quartile (Q3, 75th percentile)
    - Maximum (excluding outliers)
    - Outliers shown as individual points

    Box anatomy:
    - Box: Interquartile range (IQR = Q3 - Q1)
    - Line in box: Median
    - Whiskers: Extend to 1.5 * IQR
    - Points beyond whiskers: Outliers

    Function: sns.boxplot()
    """

    print("="*80)
    print("SECTION 1: BOX PLOTS")
    print("="*80)

    tips = sns.load_dataset('tips')

    # Example 1.1: Basic box plot
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=tips, x='day', y='total_bill')
    plt.title('Box Plot: Total Bill by Day', fontsize=14, fontweight='bold')
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Total Bill ($)', fontsize=12)
    plt.tight_layout()
    plt.show()

    print("✓ Basic box plot created")

    # Example 1.2: Box plot with grouping
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=tips, x='day', y='total_bill', hue='time')
    plt.title('Box Plot with Grouping: Bill by Day and Time', fontsize=14, fontweight='bold')
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Total Bill ($)', fontsize=12)
    plt.legend(title='Time of Day')
    plt.tight_layout()
    plt.show()

    print("✓ Grouped box plot created")

    # Example 1.3: Horizontal box plot
    plt.figure(figsize=(10, 8))
    sns.boxplot(data=tips, y='day', x='total_bill', orient='h')
    plt.title('Horizontal Box Plot', fontsize=14, fontweight='bold')
    plt.ylabel('Day of Week', fontsize=12)
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.tight_layout()
    plt.show()

    print("✓ Horizontal box plot created")

    # Example 1.4: Customized box plot
    plt.figure(figsize=(10, 6))
    sns.boxplot(
        data=tips, 
        x='day', 
        y='total_bill',
        palette='Set2',
        linewidth=2.5,
        width=0.6,  # Width of boxes
        fliersize=5  # Size of outlier points
    )
    plt.title('Customized Box Plot', fontsize=14, fontweight='bold')
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Total Bill ($)', fontsize=12)
    plt.tight_layout()
    plt.show()

    print("✓ Customized box plot created\n")

    # =============================================================================
    # SECTION 2: VIOLIN PLOTS - DISTRIBUTION SHAPE
    # =============================================================================

    """
    VIOLIN PLOTS combine box plots with KDE plots. They show:
    - Distribution shape (width of violin)
    - Quartiles and median (inner box)
    - Full data density

    Advantages over box plots:
    - Show bimodal distributions
    - Display distribution shape
    - More informative about data density

    Function: sns.violinplot()
    """

    print("="*80)
    print("SECTION 2: VIOLIN PLOTS")
    print("="*80)

    # Example 2.1: Basic violin plot
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=tips, x='day', y='total_bill')
    plt.title('Violin Plot: Total Bill by Day', fontsize=14, fontweight='bold')
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Total Bill ($)', fontsize=12)
    plt.tight_layout()
    plt.show()

    print("✓ Basic violin plot created")

    # Example 2.2: Violin plot with inner representation options
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Box: Shows box plot inside
    sns.violinplot(data=tips, x='day', y='total_bill', inner='box', ax=axes[0, 0])
    axes[0, 0].set_title("inner='box' - Box plot inside")

    # Quartile: Shows quartile lines
    sns.violinplot(data=tips, x='day', y='total_bill', inner='quartile', ax=axes[0, 1])
    axes[0, 1].set_title("inner='quartile' - Quartile lines")

    # Point: Shows all data points
    sns.violinplot(data=tips, x='day', y='total_bill', inner='point', ax=axes[1, 0])
    axes[1, 0].set_title("inner='point' - All data points")

    # Stick: Shows each observation
    sns.violinplot(data=tips, x='day', y='total_bill', inner='stick', ax=axes[1, 1])
    axes[1, 1].set_title("inner='stick' - Individual observations")

    plt.tight_layout()
    plt.show()

    print("✓ Violin plots with different inner types created")

    # Example 2.3: Split violin plot (comparing two groups)
    plt.figure(figsize=(10, 6))
    sns.violinplot(
        data=tips, 
        x='day', 
        y='total_bill', 
        hue='sex',
        split=True,  # Split violin in half for comparison
        palette='Set2'
    )
    plt.title('Split Violin Plot: Comparing by Gender', fontsize=14, fontweight='bold')
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Total Bill ($)', fontsize=12)
    plt.legend(title='Gender')
    plt.tight_layout()
    plt.show()

    print("✓ Split violin plot created\n")

    # =============================================================================
    # SECTION 3: STRIP AND SWARM PLOTS - INDIVIDUAL POINTS
    # =============================================================================

    """
    STRIP PLOTS show all individual data points, optionally with jitter.
    SWARM PLOTS arrange points to avoid overlap, showing density.

    When to use:
    - Strip: Simple, fast, good for small-medium datasets
    - Swarm: More informative about density, slower for large datasets

    Functions: sns.stripplot(), sns.swarmplot()
    """

    print("="*80)
    print("SECTION 3: STRIP AND SWARM PLOTS")
    print("="*80)

    # Example 3.1: Strip plot
    plt.figure(figsize=(10, 6))
    sns.stripplot(data=tips, x='day', y='total_bill', alpha=0.5)
    plt.title('Strip Plot: Individual Data Points', fontsize=14, fontweight='bold')
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Total Bill ($)', fontsize=12)
    plt.tight_layout()
    plt.show()

    print("✓ Strip plot created")

    # Example 3.2: Strip plot with jitter
    plt.figure(figsize=(10, 6))
    sns.stripplot(
        data=tips, 
        x='day', 
        y='total_bill',
        jitter=True,  # Add random noise to x-position
        alpha=0.5,
        size=4
    )
    plt.title('Strip Plot with Jitter', fontsize=14, fontweight='bold')
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Total Bill ($)', fontsize=12)
    plt.tight_layout()
    plt.show()

    print("✓ Strip plot with jitter created")

    # Example 3.3: Swarm plot
    plt.figure(figsize=(10, 6))
    sns.swarmplot(data=tips, x='day', y='total_bill', size=4)
    plt.title('Swarm Plot: Non-Overlapping Points', fontsize=14, fontweight='bold')
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Total Bill ($)', fontsize=12)
    plt.tight_layout()
    plt.show()

    print("✓ Swarm plot created")

    # Example 3.4: Swarm plot with grouping
    plt.figure(figsize=(12, 6))
    sns.swarmplot(data=tips, x='day', y='total_bill', hue='time', size=4)
    plt.title('Swarm Plot with Grouping', fontsize=14, fontweight='bold')
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Total Bill ($)', fontsize=12)
    plt.legend(title='Time of Day')
    plt.tight_layout()
    plt.show()

    print("✓ Grouped swarm plot created\n")

    # =============================================================================
    # SECTION 4: COMBINING PLOT TYPES
    # =============================================================================

    """
    Combining different plot types gives the most complete picture.
    Common combinations:
    - Box + Strip: Shows summary and individual points
    - Violin + Swarm: Shows distribution and all data
    """

    print("="*80)
    print("SECTION 4: COMBINING PLOT TYPES")
    print("="*80)

    # Example 4.1: Box plot with strip plot overlay
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=tips, x='day', y='total_bill', color='lightgray', width=0.5)
    sns.stripplot(data=tips, x='day', y='total_bill', color='black', alpha=0.3, size=3)
    plt.title('Box Plot with Strip Plot Overlay', fontsize=14, fontweight='bold')
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Total Bill ($)', fontsize=12)
    plt.tight_layout()
    plt.show()

    print("✓ Combined box and strip plot created")

    # Example 4.2: Violin plot with swarm plot overlay
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=tips, x='day', y='total_bill', inner=None, color='lightblue', alpha=0.6)
    sns.swarmplot(data=tips, x='day', y='total_bill', color='black', alpha=0.5, size=3)
    plt.title('Violin Plot with Swarm Plot Overlay', fontsize=14, fontweight='bold')
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Total Bill ($)', fontsize=12)
    plt.tight_layout()
    plt.show()

    print("✓ Combined violin and swarm plot created\n")

    # =============================================================================
    # KEY TAKEAWAYS
    # =============================================================================

    """
    🎯 KEY TAKEAWAYS:

    1. BOX PLOTS: Best for showing 5-number summary and outliers
    2. VIOLIN PLOTS: Show distribution shape, good for multimodal data
    3. STRIP PLOTS: Show all individual points, use jitter to reduce overlap
    4. SWARM PLOTS: Like strip plots but automatically avoid overlap
    5. COMBINE plots for comprehensive visualization
    6. Use 'hue' for grouping, 'split' for split violins
    7. Choose plot based on: data size, question, audience

    NEXT: Tutorial 05 - Regression Plots
    """

    print("="*80)
    print("TUTORIAL 04 COMPLETE!")
    print("="*80)
```

!!! info "In Machine Learning"

    Bar charts are the standard way to compare **model performance metrics** side by side: accuracy, precision, recall, and F1 score across multiple models. Grouped bar charts compare metrics within models; stacked bars show class-level contributions to overall performance.

---

## Exercises

**Exercise 1.**
Create a vertical bar chart showing the populations (in millions) of five countries: China (1412), India (1408), USA (332), Indonesia (276), and Brazil (215). Add value labels on top of each bar using `ax.bar_label()`.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt

        countries = ['China', 'India', 'USA', 'Indonesia', 'Brazil']
        populations = [1412, 1408, 332, 276, 215]

        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(countries, populations, color='steelblue', edgecolor='navy')
        ax.bar_label(bars, padding=3)
        ax.set_ylabel('Population (millions)')
        ax.set_title('Population by Country')
        plt.tight_layout()
        plt.show()

---

**Exercise 2.**
Create a horizontal bar chart of the same data from Exercise 1 using `ax.barh()`. Sort the bars by population in ascending order (smallest at top) and use a different color for each bar.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt

        countries = ['China', 'India', 'USA', 'Indonesia', 'Brazil']
        populations = [1412, 1408, 332, 276, 215]

        sorted_pairs = sorted(zip(populations, countries))
        sorted_pops, sorted_countries = zip(*sorted_pairs)

        colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(sorted_countries, sorted_pops, color=colors)
        ax.set_xlabel('Population (millions)')
        ax.set_title('Population by Country (Sorted)')
        plt.tight_layout()
        plt.show()

---

**Exercise 3.**
Create side-by-side vertical and horizontal bar charts in a 1x2 subplot layout. Use fruit sales data: categories `['Apples', 'Bananas', 'Cherries', 'Dates']` with values `[45, 62, 28, 51]`. Style the vertical chart with `color='coral'` and the horizontal chart with `color='steelblue'`. Add grid lines on the value axis for both.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt

        categories = ['Apples', 'Bananas', 'Cherries', 'Dates']
        values = [45, 62, 28, 51]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        ax1.bar(categories, values, color='coral', edgecolor='black')
        ax1.set_ylabel('Sales')
        ax1.set_title('Vertical Bar Chart')
        ax1.grid(axis='y', alpha=0.3)

        ax2.barh(categories, values, color='steelblue', edgecolor='black')
        ax2.set_xlabel('Sales')
        ax2.set_title('Horizontal Bar Chart')
        ax2.grid(axis='x', alpha=0.3)

        plt.tight_layout()
        plt.show()
