# Basic Box Plot

Box plots (box-and-whisker plots) visualize the distribution of data through quartiles, providing a compact summary of central tendency, spread, and outliers.

!!! tip "Mental Model"
    A box plot compresses an entire distribution into five numbers: minimum, Q1, median, Q3, and maximum. The box spans the interquartile range (middle 50% of data), the line inside marks the median, and whiskers extend to the extremes. Points beyond the whiskers are outliers, making them easy to spot at a glance.

!!! note "Distribution Visualization Model"
    All distribution plots answer the same question at different levels of detail:

    | Level of detail | Plot type | What it shows |
    |----------------|-----------|---------------|
    | Summary (5 numbers) | **Box plot** | Center, spread, outliers |
    | Full shape | **Histogram / Violin** | Density, skewness, multimodality |
    | Exact points | **Scatter / Strip** | Individual observations |

    Box plots are powerful for **comparison** across groups, but they compress data — a bimodal distribution and a unimodal one with the same quartiles produce identical box plots. When shape matters, pair with a histogram or violin.

    **Decision guide:**

    - Compare groups compactly → **box plot**
    - Reveal distributional shape → **histogram or violin**
    - Show raw data alongside summary → **combine** (box + scatter, violin + box)

    Different plots reveal different aspects of the same distribution —
    combining them gives the reader both the quick summary and the full picture.

## Single Data Set

The simplest box plot displays one distribution using `ax.boxplot()`.

### 1. Import and Setup

```python
import matplotlib.pyplot as plt
import numpy as np
```

### 2. Generate Data

```python
np.random.seed(42)
data = np.random.normal(100, 15, 200)
```

### 3. Create Box Plot

```python
fig, ax = plt.subplots()
ax.boxplot(data)
ax.set_ylabel('Value')
ax.set_title('Basic Box Plot')
plt.show()
```

## Multiple Data Sets

Compare multiple distributions side by side by passing a list of arrays.

### 1. Prepare Multiple Arrays

```python
np.random.seed(42)
data1 = np.random.normal(100, 10, 200)
data2 = np.random.normal(90, 20, 200)
data3 = np.random.normal(110, 15, 200)
```

### 2. Pass as List

```python
fig, ax = plt.subplots()
ax.boxplot([data1, data2, data3])
ax.set_xticklabels(['Group A', 'Group B', 'Group C'])
ax.set_ylabel('Value')
ax.set_title('Comparing Distributions')
plt.show()
```

### 3. Interpret Results

Each box represents one distribution. Boxes at different heights indicate different medians. Wider boxes (taller IQR) indicate greater variability.

## Method Signature

The `ax.boxplot()` method accepts various input formats.

### 1. Single Array

```python
ax.boxplot(data)  # One box
```

### 2. List of Arrays

```python
ax.boxplot([data1, data2, data3])  # Multiple boxes
```

### 3. 2D Array

```python
data_2d = np.random.randn(100, 4)
ax.boxplot(data_2d)  # Each column becomes a box
```

---

## Exercises

**Exercise 1.**
Generate three datasets from different distributions: normal (mean=0, std=1), uniform (low=-2, high=2), and exponential (scale=1) with 200 samples each. Create side-by-side box plots for all three and label each with the distribution name.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        normal_data = np.random.normal(0, 1, 200)
        uniform_data = np.random.uniform(-2, 2, 200)
        exponential_data = np.random.exponential(1, 200)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.boxplot([normal_data, uniform_data, exponential_data],
                    labels=['Normal(0,1)', 'Uniform(-2,2)', 'Exponential(1)'])
        ax.set_ylabel('Value')
        ax.set_title('Distribution Comparison')
        plt.show()

---

**Exercise 2.**
Create a horizontal box plot of test scores for four classes. Generate data with `np.random.normal` using means `[70, 75, 80, 85]` and standard deviation 10 for each class (100 students each). Add class labels and a vertical line at the overall mean.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        means = [70, 75, 80, 85]
        data = [np.random.normal(m, 10, 100) for m in means]
        overall_mean = np.mean([d.mean() for d in data])

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.boxplot(data, vert=False, labels=['Class A', 'Class B', 'Class C', 'Class D'])
        ax.axvline(x=overall_mean, color='red', linestyle='--', label=f'Overall Mean = {overall_mean:.1f}')
        ax.set_xlabel('Test Score')
        ax.set_title('Test Scores by Class')
        ax.legend()
        plt.show()

---

**Exercise 3.**
Create a box plot comparing the distributions of `sin(x)`, `cos(x)`, and `tan(x)` evaluated at 1000 random points uniformly distributed in $[0, 2\pi]$. Clip the `tan(x)` values to $[-10, 10]$. Show notched box plots to indicate confidence intervals around the median.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        x = np.random.uniform(0, 2 * np.pi, 1000)
        sin_vals = np.sin(x)
        cos_vals = np.cos(x)
        tan_vals = np.clip(np.tan(x), -10, 10)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.boxplot([sin_vals, cos_vals, tan_vals],
                    labels=['sin(x)', 'cos(x)', 'tan(x)'],
                    notch=True)
        ax.set_ylabel('Value')
        ax.set_title('Trig Function Distributions (Notched)')
        plt.show()
