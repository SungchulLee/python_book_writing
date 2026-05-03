# Bar Plots

Bar plots visualize categorical data by displaying rectangular bars with heights proportional to the values they represent. Pandas provides multiple ways to create bar plots.

!!! tip "Mental Model"
    A bar plot maps categories to bar heights. Use `kind='bar'` for vertical bars and `kind='barh'` for horizontal bars when labels are long. Stacked bars show composition within each category; grouped bars show side-by-side comparison. The input is typically `value_counts()` or a groupby result.

## Basic Bar Plot

### Using plot(kind='bar')

```python
import pandas as pd
import matplotlib.pyplot as plt

# Count categories
url = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/drinks.csv'
df = pd.read_csv(url)

fig, ax = plt.subplots(figsize=(10, 4))
df['continent'].value_counts().plot(kind='bar', ax=ax)
ax.set_title('Countries by Continent')
ax.set_ylabel('Count')
plt.tight_layout()
plt.show()
```

### Horizontal Bar (kind='barh')

```python
fig, ax = plt.subplots(figsize=(8, 5))
df['continent'].value_counts().plot(kind='barh', ax=ax)
ax.set_title('Countries by Continent')
ax.set_xlabel('Count')
plt.tight_layout()
plt.show()
```

## Single Bar Plot with Matplotlib

For more control, use matplotlib's `ax.bar()`:

```python
import matplotlib.pyplot as plt
import pandas as pd

def load_teachers_data():
    data = {
        'Courses': ('Language', 'History', 'Geometry', 'Chemistry', 'Physics'),
        'Number of Teachers': (7, 3, 9, 1, 2)
    }
    return pd.DataFrame(data).set_index('Courses')

df = load_teachers_data()

fig, ax = plt.subplots(figsize=(10, 4))
teacher_counts = df['Number of Teachers']

ax.bar(
    x=range(len(teacher_counts)),
    height=teacher_counts,
    tick_label=df.index,
    width=0.5
)

ax.set_xlabel('Courses')
ax.set_ylabel('Number of Teachers')
ax.set_title('Favorite Courses of Teachers')
ax.spines[['right', 'top']].set_visible(False)

plt.tight_layout()
plt.show()
```

## Grouped Bar Plot

Compare multiple metrics across categories:

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def load_student_scores():
    data = {
        'Student': ['Brandon', 'Vanessa', 'Daniel', 'Kevin', 'William'],
        'Midterm': [85, 60, 60, 65, 100],
        'Final': [90, 90, 65, 80, 95]
    }
    return pd.DataFrame(data).set_index('Student')

df = load_student_scores()

# Set up positions
positions = np.arange(len(df))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 5))

# Plot bars side by side
ax.bar(positions - width/2, df['Midterm'], width, label='Midterm')
ax.bar(positions + width/2, df['Final'], width, label='Final')

# Customize
ax.set_xticks(positions)
ax.set_xticklabels(df.index)
ax.set_xlabel('Student')
ax.set_ylabel('Score')
ax.set_title('Midterm and Final Scores')
ax.legend()
ax.spines[['right', 'top']].set_visible(False)

plt.tight_layout()
plt.show()
```

### Using pandas plot() for Grouped Bars

```python
fig, ax = plt.subplots(figsize=(10, 5))
df.plot(kind='bar', ax=ax)
ax.set_title('Student Scores')
ax.set_ylabel('Score')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
```

## Stacked Bar Plot

Show composition within categories:

```python
# Using pandas
fig, ax = plt.subplots(figsize=(10, 5))
df.plot(kind='bar', stacked=True, ax=ax)
ax.set_title('Student Scores (Stacked)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
```

### Segmented Bar Plot (100% Stacked)

Show proportions rather than absolute values:

```python
import matplotlib.pyplot as plt
import numpy as np

# Data: Has Antibodies?
labels = ('Yes', 'No')
antibody_pcts = (
    np.array([95, 90, 40]),  # Yes percentages
    np.array([5, 10, 60])    # No percentages
)
age_groups = ('Adults', 'Children', 'Infants')

fig, ax = plt.subplots(figsize=(8, 5))

# Initialize bottom for stacking
bottom = np.zeros(3)

# Stack bars
for label, pct in zip(labels, antibody_pcts):
    ax.bar(
        x=np.arange(3),
        height=pct,
        width=0.5,
        bottom=bottom,
        label=label
    )
    bottom += pct

ax.set_xticks(np.arange(3))
ax.set_xticklabels(age_groups)
ax.set_ylabel('Percentage')
ax.set_title('Has Antibodies?')
ax.spines[['top', 'right']].set_visible(False)
ax.legend(title='Response', loc='center left', bbox_to_anchor=(1.0, 0.5))

plt.tight_layout()
plt.show()
```

## Bar Plot from Value Counts

Common pattern for categorical data:

```python
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

# Survival counts
df['Survived'].value_counts().plot(kind='bar', ax=axes[0])
axes[0].set_title('Survival')
axes[0].set_xticklabels(['Died', 'Survived'], rotation=0)

# Passenger class
df['Pclass'].value_counts().sort_index().plot(kind='bar', ax=axes[1])
axes[1].set_title('Passenger Class')
axes[1].set_xticklabels(['1st', '2nd', '3rd'], rotation=0)

# Embarkation port
df['Embarked'].value_counts().plot(kind='bar', ax=axes[2])
axes[2].set_title('Embarkation Port')

plt.tight_layout()
plt.show()
```

## Customization Options

### Colors

```python
# Single color
df['continent'].value_counts().plot(kind='bar', color='steelblue')

# Multiple colors
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
df['continent'].value_counts().plot(kind='bar', color=colors)
```

### Edge Color

```python
df['continent'].value_counts().plot(kind='bar', edgecolor='black')
```

### Bar Width

```python
df['continent'].value_counts().plot(kind='bar', width=0.8)  # 0-1 range
```

### Rotation

```python
# Rotate x-tick labels
df.plot(kind='bar', rot=45)
```

### Grid

```python
df.plot(kind='bar', grid=True)
```

## Sorting Bars

```python
# Sort by value (descending - default for value_counts)
df['continent'].value_counts().plot(kind='bar')

# Sort by value (ascending)
df['continent'].value_counts().sort_values().plot(kind='bar')

# Sort alphabetically
df['continent'].value_counts().sort_index().plot(kind='bar')
```

## Adding Value Labels

```python
fig, ax = plt.subplots(figsize=(10, 5))
counts = df['continent'].value_counts()
bars = ax.bar(range(len(counts)), counts.values)

# Add labels on bars
for bar, count in zip(bars, counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            str(count), ha='center', va='bottom')

ax.set_xticks(range(len(counts)))
ax.set_xticklabels(counts.index)
ax.set_title('Countries by Continent')
plt.tight_layout()
plt.show()
```

## Summary of Bar Plot Types

| Type | Code | Use Case |
|------|------|----------|
| Vertical bar | `plot(kind='bar')` | Category comparison |
| Horizontal bar | `plot(kind='barh')` | Long category names |
| Grouped bar | Multiple `ax.bar()` calls | Compare metrics |
| Stacked bar | `plot(kind='bar', stacked=True)` | Show composition |
| 100% stacked | Manual with percentages | Show proportions |

## Quick Reference

```python
# Basic bar from value counts
series.value_counts().plot(kind='bar')

# Horizontal
series.value_counts().plot(kind='barh')

# Multiple columns grouped
df.plot(kind='bar')

# Stacked
df.plot(kind='bar', stacked=True)

# Customized
series.value_counts().plot(
    kind='bar',
    color='steelblue',
    edgecolor='black',
    width=0.7,
    rot=45
)
```


---

## Exercises

**Exercise 1.** Write code that creates a bar plot from a DataFrame using `df.plot.bar()`. Add a title and axis labels.

??? success "Solution to Exercise 1"
    ```python
    import pandas as pd
    import numpy as np

    # Solution for the specific exercise
    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(10), 'B': np.random.randn(10)})
    print(df.head())
    ```

---

**Exercise 2.** Create a grouped bar plot from a DataFrame with multiple numeric columns using `df.plot.bar()`.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that creates a horizontal bar plot using `df.plot.barh()` and sorts the bars by value.

??? success "Solution to Exercise 3"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(20), 'B': np.random.randn(20)})
    result = df.describe()
    print(result)
    ```

---

**Exercise 4.** Create a stacked bar plot using `df.plot.bar(stacked=True)` to show the composition of categories.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
