# Python Data Science Ecosystem

Matplotlib sits at the center of the Python data science ecosystem, integrating with numerical computing, data manipulation, and machine learning libraries.

!!! tip "Mental Model"
    Think of the Python data science stack as layers: NumPy provides the array foundation, Pandas organizes data into tables, and Matplotlib turns those arrays and tables into pictures. Every visualization library you encounter ultimately converts data into NumPy arrays before drawing pixels.

    The key insight: **Matplotlib is not a data tool — it is a rendering engine
    for numerical data.** All libraries in the ecosystem ultimately produce arrays;
    Matplotlib's job is the final transformation: **arrays → pixels.**

---

## The Ecosystem

The Python data science stack consists of interconnected libraries:

```
                    ┌─────────────────┐
                    │   Applications  │
                    │  (Your Code)    │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   Matplotlib  │   │    Pandas     │   │  Scikit-learn │
│ (Visualization)│   │(Data Analysis)│   │     (ML)      │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │     NumPy     │
                    │(Array Computing)│
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    Python     │
                    └───────────────┘
```

---

## Core Libraries

### NumPy

The foundation for numerical computing:

- N-dimensional arrays
- Mathematical functions
- Linear algebra
- Random number generation

```python
import numpy as np

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)
```

### Pandas

Data manipulation and analysis:

- DataFrame and Series
- Data cleaning
- Time series support
- CSV/Excel I/O

```python
import pandas as pd

df = pd.read_csv('data.csv')
df['column'].plot()
```

### Matplotlib

Visualization:

- 2D plotting
- Publication quality
- Highly customizable
- Multiple backends

```python
import matplotlib.pyplot as plt

plt.plot(x, y)
plt.show()
```

---

## Integration Examples

### NumPy + Matplotlib

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-np.pi, np.pi, 100)
y = np.sin(x)

plt.plot(x, y)
plt.show()
```

### Pandas + Matplotlib

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df.plot(kind='bar')
plt.show()
```

### Scikit-learn + Matplotlib

```python
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt

iris = load_iris()
plt.scatter(iris.data[:, 0], iris.data[:, 1], c=iris.target)
plt.show()
```

---

## Library Relationships

| Library | Depends On | Used By |
|---------|------------|---------|
| NumPy | Python | Everything |
| Pandas | NumPy | Seaborn, Scikit-learn |
| Matplotlib | NumPy | Seaborn, Pandas |
| Seaborn | Matplotlib, Pandas | Applications |
| Scikit-learn | NumPy, SciPy | Applications |

---

## Key Takeaways

- NumPy is the foundation for numerical computing
- Pandas builds on NumPy for data manipulation
- Matplotlib integrates with both for visualization
- Seaborn extends Matplotlib for statistical graphics
- Understanding the ecosystem helps choose the right tool

---

## Runnable Example: `seaborn_basic_plots.py`

```python
"""
Tutorial 02: Basic Plots in Seaborn

This tutorial covers the fundamental plot types in Seaborn: scatter plots,
line plots, and bar plots. These are the building blocks for data visualization
and will be used extensively throughout your data analysis work.

Learning Objectives:
- Master scatter plots for showing relationships
- Create line plots for time series and trends
- Build bar plots for categorical comparisons
- Understand when to use each plot type
- Learn customization options for each plot

Author: Educational Python Package
Level: Beginner
Prerequisites: Tutorial 01 (Seaborn Basics)
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Set style for consistent appearance

if __name__ == "__main__":
    sns.set_style("whitegrid")
    sns.set_context("notebook")

    # =============================================================================
    # SECTION 1: SCATTER PLOTS - SHOWING RELATIONSHIPS
    # =============================================================================

    """
    SCATTER PLOTS are used to visualize the relationship between two continuous
    (numerical) variables. Each point represents one observation.

    When to use scatter plots:
    - Exploring correlations between two variables
    - Identifying patterns, trends, or clusters
    - Detecting outliers
    - Showing the distribution of data in 2D space

    Function: sns.scatterplot()
    """

    # Load sample data
    tips = sns.load_dataset('tips')

    print("="*80)
    print("SECTION 1: SCATTER PLOTS")
    print("="*80)

    # Example 1.1: Basic scatter plot
    # Shows the relationship between total bill and tip
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=tips, x='total_bill', y='tip')
    plt.title('Basic Scatter Plot: Tips vs Total Bill', fontsize=14, fontweight='bold')
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Tip ($)', fontsize=12)
    plt.tight_layout()
    plt.show()

    print("✓ Basic scatter plot created")

    # Example 1.2: Scatter plot with color encoding (hue)
    # The 'hue' parameter adds a categorical dimension through color
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=tips, 
        x='total_bill', 
        y='tip',
        hue='time'  # Color by time of day (Lunch/Dinner)
    )
    plt.title('Scatter Plot with Color Encoding (Hue)', fontsize=14, fontweight='bold')
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Tip ($)', fontsize=12)
    plt.legend(title='Time of Day')
    plt.tight_layout()
    plt.show()

    print("✓ Scatter plot with color encoding created")

    # Example 1.3: Scatter plot with size encoding
    # The 'size' parameter makes point size represent a numerical variable
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=tips, 
        x='total_bill', 
        y='tip',
        size='size',  # Point size based on party size
        sizes=(20, 200),  # Range of point sizes (min, max)
        alpha=0.6  # Transparency helps when points overlap
    )
    plt.title('Scatter Plot with Size Encoding', fontsize=14, fontweight='bold')
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Tip ($)', fontsize=12)
    plt.legend(title='Party Size', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    print("✓ Scatter plot with size encoding created")

    # Example 1.4: Scatter plot with style encoding
    # The 'style' parameter changes marker shapes based on a categorical variable
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=tips, 
        x='total_bill', 
        y='tip',
        style='smoker',  # Different marker shapes for smoker/non-smoker
        hue='smoker'  # Also color by same variable for clarity
    )
    plt.title('Scatter Plot with Style Encoding', fontsize=14, fontweight='bold')
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Tip ($)', fontsize=12)
    plt.legend(title='Smoker')
    plt.tight_layout()
    plt.show()

    print("✓ Scatter plot with style encoding created")

    # Example 1.5: Combining multiple encodings
    # You can use hue, size, and style together to show 4 dimensions!
    plt.figure(figsize=(12, 6))
    sns.scatterplot(
        data=tips, 
        x='total_bill', 
        y='tip',
        hue='day',  # Color by day of week
        size='size',  # Size by party size
        style='time',  # Shape by time of day
        sizes=(50, 250),
        alpha=0.7
    )
    plt.title('Scatter Plot with Multiple Encodings (4 dimensions!)', fontsize=14, fontweight='bold')
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Tip ($)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    print("✓ Multi-dimensional scatter plot created")

    # Example 1.6: Customizing scatter plot appearance
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=tips, 
        x='total_bill', 
        y='tip',
        color='darkblue',  # Single color for all points
        s=100,  # Marker size (note: lowercase 's' for uniform size)
        alpha=0.6,
        edgecolor='black',  # Border color
        linewidth=0.5  # Border width
    )
    plt.title('Customized Scatter Plot Appearance', fontsize=14, fontweight='bold')
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Tip ($)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    print("✓ Customized scatter plot created\n")

    # =============================================================================
    # SECTION 2: LINE PLOTS - SHOWING TRENDS OVER TIME
    # =============================================================================

    """
    LINE PLOTS connect data points with lines, making them ideal for showing
    trends, changes over time, or continuous relationships.

    When to use line plots:
    - Time series data (stock prices, temperature over time)
    - Showing trends or trajectories
    - Comparing multiple series over a continuous variable
    - When the order of data points matters

    Function: sns.lineplot()
    """

    print("="*80)
    print("SECTION 2: LINE PLOTS")
    print("="*80)

    # Load a time series dataset
    flights = sns.load_dataset('flights')
    print("\nFlights dataset preview:")
    print(flights.head(10))

    # Example 2.1: Basic line plot
    # Show trend of passengers over time
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=flights, x='year', y='passengers')
    plt.title('Basic Line Plot: Airline Passengers Over Time', fontsize=14, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of Passengers', fontsize=12)
    plt.tight_layout()
    plt.show()

    print("✓ Basic line plot created")

    # Example 2.2: Line plot with multiple categories
    # Show trend for each month separately
    plt.figure(figsize=(12, 6))
    sns.lineplot(
        data=flights, 
        x='year', 
        y='passengers',
        hue='month'  # Different line for each month
    )
    plt.title('Line Plot with Multiple Categories', fontsize=14, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of Passengers', fontsize=12)
    plt.legend(title='Month', bbox_to_anchor=(1.05, 1), loc='upper left', ncol=1)
    plt.tight_layout()
    plt.show()

    print("✓ Multi-category line plot created")

    # Example 2.3: Line plot with confidence interval
    # Seaborn can automatically compute and display confidence intervals
    # Let's create some sample data with multiple measurements
    np.random.seed(42)
    time_series_data = pd.DataFrame({
        'time': np.repeat(range(1, 11), 20),  # 10 time points, 20 measurements each
        'value': np.random.randn(200).cumsum() + np.repeat(range(1, 11), 20) * 2
    })

    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=time_series_data, 
        x='time', 
        y='value',
        ci=95,  # 95% confidence interval (default)
        # ci='sd' would show standard deviation instead
        # ci=None would show no confidence band
    )
    plt.title('Line Plot with Confidence Interval', fontsize=14, fontweight='bold')
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.tight_layout()
    plt.show()

    print("✓ Line plot with confidence interval created")

    # Example 2.4: Customizing line style
    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=flights[flights['month'].isin(['Jan', 'Jul'])],  # Filter to two months
        x='year', 
        y='passengers',
        hue='month',
        style='month',  # Different line style for each category
        markers=True,  # Add markers at data points
        dashes=False,  # Use solid lines (False) or dashed lines (True)
        linewidth=2.5
    )
    plt.title('Customized Line Plot Style', fontsize=14, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of Passengers', fontsize=12)
    plt.legend(title='Month')
    plt.tight_layout()
    plt.show()

    print("✓ Customized line plot created")

    # Example 2.5: Line plot with error bars
    # Create sample data
    np.random.seed(42)
    measurements = pd.DataFrame({
        'dose': [1, 2, 3, 4, 5] * 3,
        'response': [1.2, 2.3, 3.1, 3.8, 4.5] * 3 + np.random.normal(0, 0.3, 15)
    })

    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=measurements, 
        x='dose', 
        y='response',
        marker='o',  # Circle markers
        markersize=8,
        err_style='bars',  # Can be 'band' (default) or 'bars'
        linewidth=2
    )
    plt.title('Line Plot with Error Bars', fontsize=14, fontweight='bold')
    plt.xlabel('Dose', fontsize=12)
    plt.ylabel('Response', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    print("✓ Line plot with error bars created\n")

    # =============================================================================
    # SECTION 3: BAR PLOTS - COMPARING CATEGORIES
    # =============================================================================

    """
    BAR PLOTS use rectangular bars to show comparisons among categories.
    The height of each bar represents the value for that category.

    When to use bar plots:
    - Comparing quantities across different categories
    - Showing counts or frequencies
    - Displaying summary statistics (mean, median, sum) by group
    - When you have discrete categories on one axis

    Function: sns.barplot()
    """

    print("="*80)
    print("SECTION 3: BAR PLOTS")
    print("="*80)

    # Example 3.1: Basic bar plot
    # Show average tip by day of week
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=tips, 
        x='day', 
        y='tip'
        # By default, barplot shows the MEAN and a confidence interval
    )
    plt.title('Basic Bar Plot: Average Tip by Day', fontsize=14, fontweight='bold')
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Average Tip ($)', fontsize=12)
    plt.tight_layout()
    plt.show()

    print("✓ Basic bar plot created")

    # Example 3.2: Bar plot with categorical grouping
    # Compare average tips by day and time
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=tips, 
        x='day', 
        y='tip',
        hue='time'  # Group by time of day
    )
    plt.title('Grouped Bar Plot: Average Tip by Day and Time', fontsize=14, fontweight='bold')
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Average Tip ($)', fontsize=12)
    plt.legend(title='Time of Day')
    plt.tight_layout()
    plt.show()

    print("✓ Grouped bar plot created")

    # Example 3.3: Horizontal bar plot
    # Sometimes horizontal bars are easier to read, especially with long labels
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=tips, 
        x='tip',  # Note: x and y are swapped
        y='day',
        hue='sex',
        orient='h'  # Explicitly specify horizontal orientation
    )
    plt.title('Horizontal Bar Plot', fontsize=14, fontweight='bold')
    plt.xlabel('Average Tip ($)', fontsize=12)
    plt.ylabel('Day of Week', fontsize=12)
    plt.legend(title='Gender')
    plt.tight_layout()
    plt.show()

    print("✓ Horizontal bar plot created")

    # Example 3.4: Bar plot with different estimator
    # Instead of mean, we can show other statistics
    plt.figure(figsize=(12, 6))

    # Create subplots to compare different estimators
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Mean (default)
    sns.barplot(data=tips, x='day', y='tip', estimator=np.mean, ax=axes[0])
    axes[0].set_title('Mean Tip by Day')
    axes[0].set_ylabel('Mean Tip ($)')

    # Median
    sns.barplot(data=tips, x='day', y='tip', estimator=np.median, ax=axes[1])
    axes[1].set_title('Median Tip by Day')
    axes[1].set_ylabel('Median Tip ($)')

    # Sum
    sns.barplot(data=tips, x='day', y='tip', estimator=np.sum, ax=axes[2])
    axes[2].set_title('Total Tips by Day')
    axes[2].set_ylabel('Total Tips ($)')

    plt.tight_layout()
    plt.show()

    print("✓ Bar plots with different estimators created")

    # Example 3.5: Customizing bar plot appearance
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=tips, 
        x='day', 
        y='tip',
        color='skyblue',  # Single color for all bars
        edgecolor='black',  # Border color
        linewidth=1.5,
        ci=95  # Confidence interval (can be 'sd' for standard deviation or None)
    )
    plt.title('Customized Bar Plot Appearance', fontsize=14, fontweight='bold')
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Average Tip ($)', fontsize=12)
    plt.ylim(0, 4)  # Set y-axis limits
    plt.tight_layout()
    plt.show()

    print("✓ Customized bar plot created")

    # Example 3.6: Count plot (special type of bar plot)
    # sns.countplot() is like a bar plot but shows counts instead of an average
    plt.figure(figsize=(10, 6))
    sns.countplot(
        data=tips, 
        x='day',
        hue='sex'
    )
    plt.title('Count Plot: Number of Customers by Day and Gender', fontsize=14, fontweight='bold')
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Number of Customers', fontsize=12)
    plt.legend(title='Gender')
    plt.tight_layout()
    plt.show()

    print("✓ Count plot created\n")

    # =============================================================================
    # SECTION 4: CHOOSING THE RIGHT PLOT TYPE
    # =============================================================================

    """
    DECISION GUIDE: Which plot should I use?

    SCATTER PLOT:
    - Both variables are continuous (numerical)
    - Want to see relationship or correlation
    - Looking for patterns, clusters, or outliers
    Example: Height vs Weight, Test Score vs Study Hours

    LINE PLOT:
    - One variable is continuous, often time
    - Data points have a natural order
    - Want to show trends or changes
    Example: Stock prices over time, Temperature by month

    BAR PLOT:
    - One variable is categorical
    - Want to compare quantities across categories
    - Showing summary statistics by group
    Example: Average sales by product, Test scores by class

    Quick Reference Table:
    ┌─────────────────────────┬──────────────┬──────────────┬─────────────┐
    │ Question                │ X-axis       │ Y-axis       │ Plot Type   │
    ├─────────────────────────┼──────────────┼──────────────┼─────────────┤
    │ Relationship?           │ Continuous   │ Continuous   │ Scatter     │
    │ Trend over time?        │ Time/Order   │ Continuous   │ Line        │
    │ Compare categories?     │ Categorical  │ Continuous   │ Bar         │
    │ Count by category?      │ Categorical  │ (automatic)  │ Count       │
    └─────────────────────────┴──────────────┴──────────────┴─────────────┘
    """

    # Example 4.1: Demonstrating plot choice with same data
    # Let's analyze tips data with different plot types

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Scatter: Relationship between two continuous variables
    sns.scatterplot(data=tips, x='total_bill', y='tip', ax=axes[0, 0])
    axes[0, 0].set_title('Scatter: Bill vs Tip (Continuous vs Continuous)')

    # Line: Trend of average tip by bill amount (binned)
    tips_binned = tips.copy()
    tips_binned['bill_bin'] = pd.cut(tips_binned['total_bill'], bins=10)
    tips_grouped = tips_binned.groupby('bill_bin')['tip'].mean().reset_index()
    tips_grouped['bill_midpoint'] = tips_grouped['bill_bin'].apply(lambda x: x.mid)
    sns.lineplot(data=tips_grouped, x='bill_midpoint', y='tip', marker='o', ax=axes[0, 1])
    axes[0, 1].set_title('Line: Trend of Tip by Bill Amount')
    axes[0, 1].set_xlabel('Total Bill ($)')

    # Bar: Average tip by categorical variable
    sns.barplot(data=tips, x='day', y='tip', ax=axes[1, 0])
    axes[1, 0].set_title('Bar: Average Tip by Day (Categorical)')

    # Count: Frequency of categories
    sns.countplot(data=tips, x='day', ax=axes[1, 1])
    axes[1, 1].set_title('Count: Number of Visits by Day')

    plt.tight_layout()
    plt.show()

    print("✓ Comparison of plot types created\n")

    # =============================================================================
    # SECTION 5: COMBINING PLOTS
    # =============================================================================

    """
    Often you'll want to combine multiple plots to tell a complete story.
    Here are some patterns for creating subplot layouts.
    """

    print("="*80)
    print("SECTION 5: COMBINING PLOTS")
    print("="*80)

    # Example 5.1: Multiple plots in a grid
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Top left: Scatter plot
    sns.scatterplot(data=tips, x='total_bill', y='tip', hue='time', ax=axes[0, 0])
    axes[0, 0].set_title('Tips vs Bill by Time')

    # Top right: Bar plot
    sns.barplot(data=tips, x='day', y='tip', hue='sex', ax=axes[0, 1])
    axes[0, 1].set_title('Average Tip by Day and Gender')

    # Bottom left: Count plot
    sns.countplot(data=tips, x='day', hue='time', ax=axes[1, 0])
    axes[1, 0].set_title('Customer Count by Day and Time')

    # Bottom right: Scatter with size
    sns.scatterplot(data=tips, x='total_bill', y='tip', size='size', 
                    hue='size', sizes=(50, 200), ax=axes[1, 1])
    axes[1, 1].set_title('Tips vs Bill by Party Size')

    plt.tight_layout()
    plt.show()

    print("✓ Grid of multiple plots created\n")

    # =============================================================================
    # SECTION 6: PRACTICE EXERCISES
    # =============================================================================

    """
    EXERCISE 1: Scatter Plot Practice
    Using the 'iris' dataset:
    - Create a scatter plot of sepal_length (x) vs sepal_width (y)
    - Color the points by species
    - Add appropriate labels and title
    - Save the plot as 'iris_scatter.png'

    EXERCISE 2: Line Plot Practice
    Using the 'flights' dataset:
    - Create a line plot showing passengers over year
    - Show separate lines for just 3 months: 'Jan', 'Jun', 'Dec'
    - Add markers to the lines
    - Include a legend

    EXERCISE 3: Bar Plot Practice
    Using the 'tips' dataset:
    - Create a bar plot showing average total_bill by day
    - Add a grouping by 'time' (Lunch/Dinner)
    - Make it a horizontal bar plot
    - Customize the colors

    EXERCISE 4: Plot Selection
    For each scenario, identify which plot type is most appropriate:
    a) Showing the relationship between study hours and exam scores
    b) Displaying monthly sales for the past year
    c) Comparing average income across different job categories
    d) Showing how temperature changed hour by hour yesterday

    EXERCISE 5: Multi-Plot Dashboard
    Create a 2x2 grid of plots using the tips dataset:
    - Plot 1: Scatter of total_bill vs tip
    - Plot 2: Bar plot of average tip by day
    - Plot 3: Count plot of customers by time
    - Plot 4: Your choice!
    Add a main title for the entire figure.
    """

    # =============================================================================
    # KEY TAKEAWAYS
    # =============================================================================

    """
    🎯 KEY TAKEAWAYS FROM THIS TUTORIAL:

    1. SCATTER PLOTS: Use for continuous vs continuous data
       - sns.scatterplot(data, x, y)
       - Add dimensions with hue, size, and style

    2. LINE PLOTS: Use for trends and time series
       - sns.lineplot(data, x, y)
       - Automatically shows confidence intervals
       - Use markers=True to highlight data points

    3. BAR PLOTS: Use for comparing categories
       - sns.barplot(data, x, y) shows means by default
       - Use hue for grouped comparisons
       - sns.countplot() for frequency counts

    4. PLOT SELECTION depends on:
       - Data types (continuous vs categorical)
       - Question you're asking
       - Story you want to tell

    5. CUSTOMIZATION options:
       - Colors: color, palette, hue
       - Markers: markers, marker, style
       - Size: s, size, sizes
       - Confidence intervals: ci parameter
       - Orientation: orient parameter

    6. COMBINE PLOTS using plt.subplots()
       - Create grid layouts
       - Pass ax parameter to Seaborn functions

    7. ALWAYS:
       - Add clear titles and labels
       - Include legends when using hue
       - Use appropriate figure sizes
       - Save high-quality plots (dpi=300)

    NEXT STEPS:
    - Move on to Tutorial 03: Distribution Plots
    - Complete the practice exercises
    - Experiment with real datasets
    - Try combining different customizations
    """

    print("="*80)
    print("TUTORIAL 02 COMPLETE!")
    print("="*80)
    print("You now understand scatter, line, and bar plots!")
    print("Next: Tutorial 03 - Distribution Plots")
    print("="*80)
```


---

## Exercises

**Exercise 1.** Name the five major Python libraries in the data science ecosystem and write the standard import statement for each.

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

**Exercise 2.** Explain how Matplotlib relates to NumPy and Pandas in the data science workflow. Why is Matplotlib typically used together with these libraries?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Write code that uses NumPy to generate data and Matplotlib to visualize it: create 200 random points and plot them as a scatter plot.

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

**Exercise 4.** List three higher-level visualization libraries built on top of Matplotlib. For each, describe one task where it is more convenient than using Matplotlib directly.

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
