# Box Plot Anatomy

Understanding the visual components of a box plot is essential for proper interpretation of distributional data.

!!! tip "Mental Model"
    Read a box plot from inside out: the median line shows center, the box shows where the middle half of data lives (IQR), the whiskers reach to the farthest non-outlier points, and individual dots beyond the whiskers flag unusual values. Each component maps to a specific statistical summary, so one glance tells you center, spread, and skewness.

## Visual Components

A box plot consists of five primary visual elements that summarize the distribution.

### 1. The Box

The rectangular box spans from the first quartile (Q1, 25th percentile) to the third quartile (Q3, 75th percentile). This range is called the Interquartile Range (IQR).

```python
IQR = Q3 - Q1
```

### 2. The Median Line

The horizontal line inside the box represents the median (Q2, 50th percentile). Its position within the box indicates skewness.

### 3. The Whiskers

Vertical lines extend from the box to show the range of non-outlier data. By default, whiskers extend to 1.5 × IQR from the box edges.

```python
lower_whisker = Q1 - 1.5 * IQR
upper_whisker = Q3 + 1.5 * IQR
```

### 4. The Fliers (Outliers)

Points beyond the whiskers are plotted individually as outliers (fliers). These represent extreme values in the distribution.

### 5. The Caps

Short horizontal lines at whisker ends mark the extent of non-outlier data.

## Statistical Interpretation

The box plot encodes the five-number summary plus outlier detection.

### 1. Five-Number Summary

```python
import numpy as np

data = np.random.normal(100, 15, 200)

minimum = np.min(data)
q1 = np.percentile(data, 25)
median = np.percentile(data, 50)
q3 = np.percentile(data, 75)
maximum = np.max(data)
```

### 2. Spread Indicators

The box width (IQR) shows the middle 50% of data. Tall boxes indicate high variability; short boxes indicate consistency.

### 3. Skewness Detection

When the median line is not centered in the box, the distribution is skewed. Median closer to Q1 indicates right skew; closer to Q3 indicates left skew.

## Comparison with Histogram

Box plots and histograms both show distributions but emphasize different aspects.

### 1. Box Plot Strengths

Box plots excel at comparing multiple distributions side-by-side, identifying outliers, and showing quartile information compactly.

### 2. Histogram Strengths

Histograms reveal the shape of the distribution, multimodality, and density patterns that box plots cannot show.

### 3. Combined View

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
data = np.random.normal(100, 15, 200)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.hist(data, bins=20, edgecolor='black', alpha=0.7)
ax1.set_title('Histogram')

ax2.boxplot(data)
ax2.set_title('Box Plot')

plt.tight_layout()
plt.show()
```

---

## Exercises

**Exercise 1.**
Create a box plot from 100 samples of a normal distribution and manually annotate the five key components (minimum, Q1, median, Q3, maximum) using `ax.annotate` with arrows pointing to each part. Print the actual values of Q1, median, Q3, and the IQR.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        data = np.random.randn(100)

        q1 = np.percentile(data, 25)
        median = np.median(data)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        whisker_low = max(data.min(), q1 - 1.5 * iqr)
        whisker_high = min(data.max(), q3 + 1.5 * iqr)

        print(f"Q1={q1:.3f}, Median={median:.3f}, Q3={q3:.3f}, IQR={iqr:.3f}")

        fig, ax = plt.subplots(figsize=(6, 8))
        ax.boxplot(data)

        annotations = [
            (whisker_low, 'Min (whisker)'),
            (q1, 'Q1 (25th percentile)'),
            (median, 'Median'),
            (q3, 'Q3 (75th percentile)'),
            (whisker_high, 'Max (whisker)'),
        ]

        for val, label in annotations:
            ax.annotate(f'{label}: {val:.2f}', xy=(1, val), xytext=(1.4, val),
                        fontsize=8, arrowprops=dict(arrowstyle='->', color='red'))

        ax.set_title('Box Plot Anatomy')
        ax.set_xlim(0.5, 2.5)
        plt.show()

---

**Exercise 2.**
Generate data with known outliers: 100 samples from `N(0, 1)` plus 5 manually added outliers at values `[-4, -3.5, 3.5, 4, 5]`. Create a box plot and use the returned dictionary to access the outlier points (`fliers`). Print the number of detected outliers and their values.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        data = np.concatenate([np.random.randn(100), [-4, -3.5, 3.5, 4, 5]])

        fig, ax = plt.subplots(figsize=(6, 6))
        bp = ax.boxplot(data)

        fliers = bp['fliers'][0]
        outlier_values = fliers.get_ydata()
        print(f"Number of outliers: {len(outlier_values)}")
        print(f"Outlier values: {outlier_values}")

        ax.set_title(f'Box Plot with {len(outlier_values)} Outliers')
        plt.show()

---

**Exercise 3.**
Create a side-by-side comparison showing the same data with `whis=1.5` (default) and `whis=3.0`. Use 500 samples from a standard normal distribution. Annotate the whisker extents on each plot and explain how changing `whis` affects outlier detection.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        data = np.random.randn(500)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))

        bp1 = ax1.boxplot(data, whis=1.5)
        n_outliers_1 = len(bp1['fliers'][0].get_ydata())
        ax1.set_title(f'whis=1.5 (default)\n{n_outliers_1} outliers')

        bp2 = ax2.boxplot(data, whis=3.0)
        n_outliers_2 = len(bp2['fliers'][0].get_ydata())
        ax2.set_title(f'whis=3.0\n{n_outliers_2} outliers')

        plt.suptitle('Effect of whis Parameter on Outlier Detection')
        plt.tight_layout()
        plt.show()
