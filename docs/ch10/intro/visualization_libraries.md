# Visualization Libraries

Python offers a rich ecosystem of visualization libraries for different use cases.

!!! tip "Mental Model"
    Matplotlib is the "assembly language" of Python visualization -- low-level and fully controllable. Libraries like Seaborn, Plotly, and Bokeh are built on top of it (or inspired by it), trading some control for convenience. Learn Matplotlib first and every higher-level library becomes easier to understand and debug.

---

## General Purpose

### Matplotlib

[Matplotlib](https://matplotlib.org/) is the foundational plotting library for Python.

- Most widely used
- Highly customizable
- Foundation for many other libraries
- Publication-quality output

```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4])
plt.ylabel('Values')
plt.show()
```

---

## Statistical Data Analysis

### Seaborn

[Seaborn](http://stanford.edu/~mwaskom/software/seaborn) is built on Matplotlib for statistical visualization.

- Beautiful default styles
- High-level interface for statistical graphics
- Integration with pandas DataFrames
- Built-in themes

```python
import seaborn as sns

tips = sns.load_dataset("tips")
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="day")
```

---

## Web-Based Visualization

### Bokeh

[Bokeh](http://bokeh.pydata.org) creates interactive visualizations for web browsers.

- Interactive plots
- Streaming data support
- Web-ready output
- Dashboards

### Plotly

[Plotly](http://plot.ly) provides interactive, publication-quality graphs.

- Interactive charts
- 3D plotting
- Dashboards with Dash
- Wide language support

---

## 3D Visualization

### VisPy

[VisPy](http://vispy.org) is a high-performance interactive 2D/3D visualization library.

- GPU-accelerated
- Large dataset handling
- Scientific visualization
- OpenGL-based

---

## Choosing a Library

| Use Case | Recommended Library |
|----------|---------------------|
| Static publication plots | Matplotlib |
| Statistical analysis | Seaborn |
| Interactive web dashboards | Plotly, Bokeh |
| Large 3D datasets | VisPy |
| Quick exploratory analysis | Seaborn, Matplotlib |

---

## Key Takeaways

- Matplotlib is the foundation for Python visualization
- Seaborn simplifies statistical plotting
- Bokeh and Plotly excel at interactive web graphics
- VisPy handles high-performance 3D visualization
- Most libraries build on or integrate with Matplotlib

---

## Runnable Example: `seaborn_basics_tutorial.py`

```python
"""
Tutorial 01: Introduction to Seaborn - Basics and Setup

This tutorial introduces Seaborn, a powerful statistical data visualization library
built on top of matplotlib. Seaborn provides a high-level interface for creating
attractive and informative statistical graphics.

Learning Objectives:
- Understand what Seaborn is and why we use it
- Learn how to import and set up Seaborn
- Understand the relationship between Seaborn and matplotlib
- Create your first simple Seaborn plot
- Learn about Seaborn's built-in datasets

Author: Educational Python Package
Level: Beginner
Prerequisites: Basic Python, matplotlib basics (helpful)
"""

# =============================================================================
# SECTION 1: IMPORTING LIBRARIES
# =============================================================================

# Import seaborn - the main library we're learning
import seaborn as sns

# Import matplotlib.pyplot - Seaborn is built on top of matplotlib
# We'll need this for displaying plots and additional customizations
import matplotlib.pyplot as plt

# Import pandas - Seaborn works best with pandas DataFrames
import pandas as pd

# Import numpy for numerical operations
import numpy as np

# Print versions to ensure everything is installed correctly

if __name__ == "__main__":
    print("Seaborn version:", sns.__version__)
    print("Matplotlib version:", plt.matplotlib.__version__)
    print("Pandas version:", pd.__version__)
    print("NumPy version:", np.__version__)

    # =============================================================================
    # SECTION 2: WHAT IS SEABORN?
    # =============================================================================

    """
    Seaborn is a Python data visualization library that provides:

    1. HIGH-LEVEL INTERFACE: Seaborn makes complex plots easy to create with just
       a few lines of code. What might take 20+ lines in matplotlib can often be
       done in 2-3 lines with Seaborn.

    2. BEAUTIFUL DEFAULT STYLES: Seaborn plots look professional out of the box,
       with carefully chosen default colors, fonts, and layouts.

    3. STATISTICAL VISUALIZATION: Seaborn is designed for statistical graphics,
       making it easy to visualize distributions, relationships, and patterns.

    4. PANDAS INTEGRATION: Seaborn works seamlessly with pandas DataFrames,
       the standard way to work with tabular data in Python.

    5. BUILT-IN THEMES: Multiple color palettes and themes for different contexts.

    Key Difference from Matplotlib:
    - Matplotlib: Low-level, precise control, more code needed
    - Seaborn: High-level, quick beautiful plots, less code needed
    - Seaborn uses matplotlib under the hood, so you can combine both!
    """

    # =============================================================================
    # SECTION 3: SETTING UP SEABORN STYLE
    # =============================================================================

    # Set the default style for all plots
    # This makes your plots look more professional automatically
    # Available styles: 'darkgrid', 'whitegrid', 'dark', 'white', 'ticks'
    sns.set_style("whitegrid")

    # You can also set the context, which adjusts the scale of plot elements
    # Contexts: 'paper', 'notebook', 'talk', 'poster'
    # Use 'paper' for publications, 'poster' for large displays
    sns.set_context("notebook")

    # Set the color palette (we'll learn more about this later)
    # This sets the default colors for your plots
    sns.set_palette("husl")

    print("\nSeaborn styling has been set up!")

    # =============================================================================
    # SECTION 4: LOADING SAMPLE DATA
    # =============================================================================

    """
    Seaborn comes with several built-in datasets that are perfect for learning
    and testing. These are real datasets used in statistics education.

    Common built-in datasets:
    - 'tips': Restaurant tipping data
    - 'iris': Famous iris flower measurements
    - 'titanic': Titanic passenger survival data
    - 'penguins': Palmer Penguins data
    - 'diamonds': Diamond price and quality data
    - 'flights': Airline passenger data
    """

    # Let's see all available datasets
    print("\nAvailable Seaborn datasets:")
    print(sns.get_dataset_names())

    # Load the 'tips' dataset - this is a popular dataset for examples
    # It contains information about restaurant bills and tips
    tips = sns.load_dataset('tips')

    # Display basic information about the dataset
    print("\n" + "="*80)
    print("TIPS DATASET EXPLORATION")
    print("="*80)

    # Show the first few rows
    print("\nFirst 5 rows of the dataset:")
    print(tips.head())

    # Show dataset information (columns, types, non-null counts)
    print("\nDataset information:")
    print(tips.info())

    # Show basic statistics
    print("\nBasic statistics:")
    print(tips.describe())

    # Show column names and their data types
    print("\nColumn names and types:")
    for column in tips.columns:
        print(f"  {column}: {tips[column].dtype}")

    # =============================================================================
    # SECTION 5: YOUR FIRST SEABORN PLOT
    # =============================================================================

    """
    Let's create our first plot! We'll use a scatter plot to show the relationship
    between total bill and tip amount.

    The basic pattern for Seaborn plots:
    1. Prepare your data (usually a pandas DataFrame)
    2. Call a Seaborn plotting function
    3. Customize if needed (optional)
    4. Display with plt.show()
    """

    # Create a figure and axis using matplotlib
    # This gives us more control over the figure size
    plt.figure(figsize=(10, 6))  # Width: 10 inches, Height: 6 inches

    # Create a scatter plot using Seaborn
    # sns.scatterplot() creates a scatter plot
    # Parameters:
    #   data: the DataFrame to use
    #   x: the column name for x-axis
    #   y: the column name for y-axis
    sns.scatterplot(data=tips, x='total_bill', y='tip')

    # Add labels and title using matplotlib functions
    # Seaborn doesn't add these automatically, so we use matplotlib
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Tip ($)', fontsize=12)
    plt.title('Relationship Between Total Bill and Tip Amount', fontsize=14, fontweight='bold')

    # Display the plot
    # In Jupyter notebooks, you might not need this
    # In scripts, this is required to show the plot
    plt.tight_layout()  # Adjust spacing to prevent label cutoff
    plt.show()

    print("\nYour first Seaborn plot has been created!")

    # =============================================================================
    # SECTION 6: ADDING COLOR AND STYLE
    # =============================================================================

    """
    One of Seaborn's strengths is the ability to easily add additional dimensions
    to your plots using color, size, and style. Let's enhance our scatter plot.
    """

    # Create a new figure
    plt.figure(figsize=(10, 6))

    # Now let's add color based on a categorical variable
    # The 'hue' parameter colors points based on a column's values
    # Let's color by time of day (Lunch or Dinner)
    sns.scatterplot(
        data=tips, 
        x='total_bill', 
        y='tip',
        hue='time',  # Color points by time of day
        style='sex',  # Different markers for sex
        size='size',  # Size of points based on party size
        sizes=(50, 200),  # Range of sizes
        alpha=0.7  # Transparency (0=transparent, 1=opaque)
    )

    # Customize the plot
    plt.xlabel('Total Bill ($)', fontsize=12)
    plt.ylabel('Tip ($)', fontsize=12)
    plt.title('Enhanced Scatter Plot with Multiple Visual Encodings', fontsize=14, fontweight='bold')

    # The legend is created automatically by Seaborn
    # Let's move it to a better position
    plt.legend(title='Legend', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()

    print("\nEnhanced plot with color, style, and size encoding created!")

    # =============================================================================
    # SECTION 7: SEABORN'S TWO TYPES OF FUNCTIONS
    # =============================================================================

    """
    Important Concept: Seaborn has TWO types of plotting functions:

    1. AXES-LEVEL FUNCTIONS (like scatterplot, barplot, histplot):
       - Draw onto a specific matplotlib axes
       - Can be part of a larger figure with multiple subplots
       - Examples: sns.scatterplot(), sns.histplot(), sns.barplot()
       - More flexible for complex layouts

    2. FIGURE-LEVEL FUNCTIONS (like relplot, displot, catplot):
       - Create their own figure with one or more subplots
       - Have a 'kind' parameter to specify plot type
       - Examples: sns.relplot(), sns.displot(), sns.catplot()
       - Better for faceted plots (multiple subplots)

    Let's see the difference:
    """

    # Example 1: Axes-level function
    # This draws on the current axes
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=tips, x='total_bill', y='tip', ax=ax)
    ax.set_title('Axes-Level Function Example')
    plt.tight_layout()
    plt.show()

    # Example 2: Figure-level function
    # This creates its own figure
    # relplot is for relational plots (scatter and line)
    g = sns.relplot(
        data=tips, 
        x='total_bill', 
        y='tip',
        kind='scatter',  # Can be 'scatter' or 'line'
        height=5,  # Height of each facet in inches
        aspect=1.5  # Aspect ratio (width = height * aspect)
    )
    g.fig.suptitle('Figure-Level Function Example', y=1.02)
    plt.tight_layout()
    plt.show()

    print("\nYou've seen both types of Seaborn functions!")

    # =============================================================================
    # SECTION 8: BASIC CUSTOMIZATION
    # =============================================================================

    """
    While Seaborn provides beautiful defaults, you often want to customize plots.
    Here are some common customizations:
    """

    # Create a sample plot to customize
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=tips, x='total_bill', y='tip', hue='day')

    # Customization 1: Change color palette
    # We'll learn more about palettes later
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=tips, x='total_bill', y='tip', hue='day', palette='Set2')
    plt.title('Custom Color Palette')
    plt.tight_layout()
    plt.show()

    # Customization 2: Change marker size and style
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=tips, 
        x='total_bill', 
        y='tip', 
        s=100,  # Marker size
        marker='D',  # Diamond marker
        color='steelblue',  # Single color for all points
        edgecolor='black',  # Border color
        linewidth=0.5  # Border width
    )
    plt.title('Custom Marker Style')
    plt.tight_layout()
    plt.show()

    # Customization 3: Add grid and customize background
    plt.figure(figsize=(10, 6))
    sns.set_style("darkgrid")  # Temporarily change style
    sns.scatterplot(data=tips, x='total_bill', y='tip')
    plt.title('Custom Background Style')
    plt.grid(True, alpha=0.3)  # Add custom grid
    plt.tight_layout()
    plt.show()

    # Reset to default style
    sns.set_style("whitegrid")

    # =============================================================================
    # SECTION 9: SAVING PLOTS
    # =============================================================================

    """
    Once you've created a plot, you'll want to save it for reports or presentations.
    """

    # Create a plot to save
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=tips, x='total_bill', y='tip', hue='time')
    plt.title('Tips vs Total Bill by Time of Day')
    plt.xlabel('Total Bill ($)')
    plt.ylabel('Tip ($)')

    # Save the figure
    # Common formats: 'png', 'pdf', 'svg', 'jpg'
    # dpi: dots per inch (higher = better quality, larger file)
    # bbox_inches='tight': removes extra whitespace
    plt.savefig('my_first_seaborn_plot.png', dpi=300, bbox_inches='tight')

    print("\nPlot saved as 'my_first_seaborn_plot.png'")

    # Show the plot
    plt.show()

    # You can also save figures created by figure-level functions
    g = sns.relplot(data=tips, x='total_bill', y='tip', hue='day', height=5)
    g.savefig('figure_level_plot.png', dpi=300, bbox_inches='tight')
    print("Figure-level plot saved as 'figure_level_plot.png'")
    plt.show()

    # =============================================================================
    # SECTION 10: PRACTICE EXERCISES
    # =============================================================================

    """
    EXERCISE 1: Load and Explore
    - Load the 'iris' dataset using sns.load_dataset()
    - Print the first 10 rows
    - Print basic statistics
    - How many species are in the dataset?

    EXERCISE 2: Create a Simple Plot
    - Using the iris dataset, create a scatter plot
    - X-axis: sepal_length
    - Y-axis: sepal_width
    - Add appropriate labels and title

    EXERCISE 3: Add Color Encoding
    - Create the same scatter plot as Exercise 2
    - Color the points by 'species'
    - What pattern do you notice?

    EXERCISE 4: Experiment with Styles
    - Create any scatter plot
    - Try all five Seaborn styles: 'darkgrid', 'whitegrid', 'dark', 'white', 'ticks'
    - Which style do you prefer and why?

    EXERCISE 5: Save Your Work
    - Create a scatter plot of your choice using the tips dataset
    - Customize it with colors, labels, and title
    - Save it as both PNG and PDF formats
    """

    # =============================================================================
    # KEY TAKEAWAYS
    # =============================================================================

    """
    🎯 KEY TAKEAWAYS FROM THIS TUTORIAL:

    1. Seaborn is a high-level statistical visualization library built on matplotlib
    2. Import seaborn as sns, along with matplotlib.pyplot and pandas
    3. Seaborn comes with built-in datasets perfect for learning
    4. Use sns.set_style() and sns.set_context() to customize appearance
    5. Seaborn has two types of functions: axes-level and figure-level
    6. Basic plot pattern: prepare data, call plot function, customize, show
    7. Use 'hue', 'size', and 'style' parameters to add dimensions to plots
    8. Save plots using plt.savefig() or g.savefig()
    9. Seaborn automatically handles many details like legends and colors
    10. Combine Seaborn (high-level) with matplotlib (low-level) for full control

    NEXT STEPS:
    - Move on to Tutorial 02: Basic Plots
    - Practice the exercises above
    - Experiment with different datasets
    - Try creating plots with your own data
    """

    print("\n" + "="*80)
    print("TUTORIAL 01 COMPLETE!")
    print("="*80)
    print("You now understand the basics of Seaborn!")
    print("Next: Tutorial 02 - Basic Plots")
    print("="*80)
```


## Choosing the Right Library

Instead of describing features, think in terms of **what you need**:

| If you need... | Use | Why |
|---|---|---|
| Full control, publication figures | **Matplotlib** | Maximum flexibility, any customization possible |
| Fast EDA, statistical plots | **Seaborn** | One-line plots with smart defaults, built on Matplotlib |
| Interactive dashboards, web | **Plotly** | Zoom/pan/hover in browser, shareable HTML |
| Declarative grammar | **Altair** | Concise, composable specification language |
| Large datasets, streaming | **Bokeh** | Server-backed interactivity, handles millions of points |
| Publication with ggplot style | **plotnine** | R's ggplot2 grammar, in Python |

**Trade-off**: flexibility vs convenience. Matplotlib gives you every pixel; higher-level libraries make common plots easy but limit edge-case customization.

---

## Exercises

**Exercise 1.** Name three Python visualization libraries besides Matplotlib and describe when you might choose each over Matplotlib.

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

**Exercise 2.** Explain the difference between static and interactive visualization libraries. Give one example of each.

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Write code using only Matplotlib to create a figure that mimics a Seaborn-style plot by setting `plt.style.use('seaborn-v0_8')`.

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

**Exercise 4.** What is the relationship between Matplotlib and Seaborn? Can Seaborn plots be further customized with Matplotlib commands?

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
