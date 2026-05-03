# Grouped and Stacked

Create multi-series bar charts to compare categories across groups or show composition of totals.

!!! tip "Mental Model"
    Grouped bars place multiple series side by side by offsetting their x-positions, while stacked bars pile series on top of each other using the `bottom` parameter. Grouped bars make it easy to compare values within a category; stacked bars make it easy to see each category's total and its composition.

!!! tip "Grouped vs Stacked = Different Questions"
    **Grouped bars** → "How do the components compare within each category?"
    **Stacked bars** → "What is each category's total, and how is it composed?"

    Choose grouped when the reader needs to compare individual series values. Choose stacked when the total and its breakdown matter more than precise per-series comparison.

## Grouped Bar Chart

Place bars side by side to compare multiple series.

### 1. Basic Grouped Bars

```python
import matplotlib.pyplot as plt
import numpy as np

categories = ['A', 'B', 'C', 'D', 'E']
series1 = [23, 45, 56, 78, 32]
series2 = [28, 40, 62, 70, 38]

x = np.arange(len(categories))
width = 0.35

fig, ax = plt.subplots()
ax.bar(x - width/2, series1, width, label='Series 1')
ax.bar(x + width/2, series2, width, label='Series 2')

ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()
plt.show()
```

### 2. Three Groups

```python
series1 = [23, 45, 56, 78, 32]
series2 = [28, 40, 62, 70, 38]
series3 = [20, 35, 50, 65, 30]

x = np.arange(len(categories))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - width, series1, width, label='2022')
ax.bar(x, series2, width, label='2023')
ax.bar(x + width, series3, width, label='2024')

ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()
plt.show()
```

### 3. Dynamic Width Calculation

```python
def grouped_bar(ax, data, labels, group_labels):
    n_groups = len(data)
    n_categories = len(data[0])
    
    total_width = 0.8
    bar_width = total_width / n_groups
    x = np.arange(n_categories)
    
    for i, (series, label) in enumerate(zip(data, labels)):
        offset = (i - n_groups/2 + 0.5) * bar_width
        ax.bar(x + offset, series, bar_width, label=label)
    
    ax.set_xticks(x)
    ax.set_xticklabels(group_labels)
    ax.legend()

fig, ax = plt.subplots()
data = [series1, series2, series3]
grouped_bar(ax, data, ['2022', '2023', '2024'], categories)
plt.show()
```

## Pandas Grouped Bars

Use DataFrame's built-in plotting for automatic grouped bars.

### 1. DataFrame with Multiple Columns

```python
import pandas as pd

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

### 2. Matplotlib Equivalent

```python
position = np.arange(df.shape[0])
student = df.index
midterm = df.Midterm
final = df.Final

fig, ax = plt.subplots(figsize=(12, 3))
width = 0.3
ax.bar(position - width/2, midterm, width=width, label='Midterm')
ax.bar(position + width/2, final, width=width, label='Final')
ax.set_xticks(position, student)
ax.set_xlabel('Student')
ax.legend()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.show()
```

### 3. Horizontal Grouped with Matplotlib

```python
fig, ax = plt.subplots(figsize=(12, 3))
height = 0.3
ax.barh(position - height/2, midterm, height=height, label='Midterm')
ax.barh(position + height/2, final, height=height, label='Final')
ax.set_yticks(position, student)
ax.set_ylabel('Student')
ax.legend()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.show()
```

## Stacked Bar Chart

Stack bars vertically to show composition.

### 1. Basic Stacked Bars

```python
categories = ['Q1', 'Q2', 'Q3', 'Q4']
product_a = [20, 25, 30, 35]
product_b = [15, 20, 25, 20]
product_c = [10, 15, 10, 15]

fig, ax = plt.subplots()
ax.bar(categories, product_a, label='Product A')
ax.bar(categories, product_b, bottom=product_a, label='Product B')
ax.bar(categories, product_c, bottom=np.array(product_a) + np.array(product_b), 
       label='Product C')

ax.legend()
ax.set_ylabel('Sales')
plt.show()
```

### 2. Using NumPy for Bottom

```python
product_a = np.array([20, 25, 30, 35])
product_b = np.array([15, 20, 25, 20])
product_c = np.array([10, 15, 10, 15])

fig, ax = plt.subplots()
ax.bar(categories, product_a, label='Product A')
ax.bar(categories, product_b, bottom=product_a, label='Product B')
ax.bar(categories, product_c, bottom=product_a + product_b, label='Product C')

ax.legend()
plt.show()
```

### 3. Dynamic Stacking

```python
def stacked_bar(ax, data, labels, categories):
    bottom = np.zeros(len(categories))
    
    for series, label in zip(data, labels):
        ax.bar(categories, series, bottom=bottom, label=label)
        bottom += np.array(series)
    
    ax.legend()

fig, ax = plt.subplots()
data = [product_a, product_b, product_c]
stacked_bar(ax, data, ['Product A', 'Product B', 'Product C'], categories)
plt.show()
```

## Horizontal Stacked Bars

Stack bars horizontally using `barh`.

### 1. Basic Horizontal Stack

```python
categories = ['Team A', 'Team B', 'Team C', 'Team D']
wins = [15, 12, 18, 10]
losses = [5, 8, 2, 10]
draws = [2, 2, 2, 2]

fig, ax = plt.subplots()
ax.barh(categories, wins, label='Wins')
ax.barh(categories, losses, left=wins, label='Losses')
ax.barh(categories, draws, left=np.array(wins) + np.array(losses), label='Draws')

ax.legend()
ax.set_xlabel('Games')
plt.show()
```

### 2. Diverging Stacked Bar

```python
categories = ['Q1', 'Q2', 'Q3', 'Q4']
positive = [30, 40, 35, 45]
negative = [-20, -15, -25, -10]

fig, ax = plt.subplots()
ax.barh(categories, positive, label='Gains', color='green')
ax.barh(categories, negative, label='Losses', color='red')
ax.axvline(x=0, color='black', linewidth=0.8)
ax.legend()
plt.show()
```

### 3. Centered Diverging

```python
survey = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
responses = [10, 20, 15, 35, 20]

colors = ['darkred', 'red', 'gray', 'green', 'darkgreen']
starts = [0, 0, 0, 0, 0]

# Center on neutral
starts[0] = -responses[0] - responses[1] - responses[2]/2
starts[1] = -responses[1] - responses[2]/2
starts[2] = -responses[2]/2
starts[3] = responses[2]/2
starts[4] = responses[2]/2 + responses[3]

fig, ax = plt.subplots()
for i, (response, start, color, label) in enumerate(zip(responses, starts, colors, survey)):
    ax.barh(['Survey'], response, left=start, color=color, label=label)

ax.axvline(x=0, color='black', linewidth=0.8)
ax.legend(loc='lower right')
plt.show()
```

## Percentage Stacked Bars

Show proportions that sum to 100%.

### 1. Calculate Percentages

```python
categories = ['2021', '2022', '2023', '2024']
cat_a = np.array([20, 25, 30, 35])
cat_b = np.array([15, 20, 25, 20])
cat_c = np.array([10, 15, 10, 15])

totals = cat_a + cat_b + cat_c
pct_a = cat_a / totals * 100
pct_b = cat_b / totals * 100
pct_c = cat_c / totals * 100
```

### 2. Create Percentage Stack

```python
fig, ax = plt.subplots()
ax.bar(categories, pct_a, label='Category A')
ax.bar(categories, pct_b, bottom=pct_a, label='Category B')
ax.bar(categories, pct_c, bottom=pct_a + pct_b, label='Category C')

ax.set_ylabel('Percentage (%)')
ax.set_ylim(0, 100)
ax.legend()
plt.show()
```

### 3. Reusable Function

```python
def percentage_stacked_bar(ax, data, labels, categories):
    data = np.array(data)
    totals = data.sum(axis=0)
    percentages = data / totals * 100
    
    bottom = np.zeros(len(categories))
    for pct, label in zip(percentages, labels):
        ax.bar(categories, pct, bottom=bottom, label=label)
        bottom += pct
    
    ax.set_ylim(0, 100)
    ax.set_ylabel('Percentage (%)')
    ax.legend()

fig, ax = plt.subplots()
percentage_stacked_bar(ax, [cat_a, cat_b, cat_c], 
                       ['A', 'B', 'C'], categories)
plt.show()
```

## Adding Labels to Grouped/Stacked

Annotate bars with values.

### 1. Grouped Bar Labels

```python
x = np.arange(len(categories))
width = 0.35

fig, ax = plt.subplots()
bars1 = ax.bar(x - width/2, series1, width, label='2023')
bars2 = ax.bar(x + width/2, series2, width, label='2024')

ax.bar_label(bars1, padding=3)
ax.bar_label(bars2, padding=3)

ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()
plt.show()
```

### 2. Stacked Bar Labels

```python
fig, ax = plt.subplots()
bars1 = ax.bar(categories, product_a, label='Product A')
bars2 = ax.bar(categories, product_b, bottom=product_a, label='Product B')
bars3 = ax.bar(categories, product_c, bottom=product_a + product_b, label='Product C')

ax.bar_label(bars1, label_type='center')
ax.bar_label(bars2, label_type='center')
ax.bar_label(bars3, label_type='center')

ax.legend()
plt.show()
```

### 3. Total Labels on Stack

```python
fig, ax = plt.subplots()
bars1 = ax.bar(categories, product_a, label='Product A')
bars2 = ax.bar(categories, product_b, bottom=product_a, label='Product B')
bars3 = ax.bar(categories, product_c, bottom=product_a + product_b, label='Product C')

totals = product_a + product_b + product_c
for i, total in enumerate(totals):
    ax.text(i, total + 1, str(total), ha='center', fontweight='bold')

ax.legend()
plt.show()
```

## Styling Grouped and Stacked

Apply consistent styling across multi-series charts.

### 1. Color Schemes

```python
colors = ['#2ecc71', '#3498db', '#9b59b6']

fig, ax = plt.subplots()
ax.bar(categories, product_a, label='A', color=colors[0])
ax.bar(categories, product_b, bottom=product_a, label='B', color=colors[1])
ax.bar(categories, product_c, bottom=product_a + product_b, label='C', color=colors[2])
ax.legend()
plt.show()
```

### 2. Edge and Hatch

```python
fig, ax = plt.subplots()
ax.bar(categories, product_a, label='A', color='white', edgecolor='blue', hatch='//')
ax.bar(categories, product_b, bottom=product_a, label='B', 
       color='white', edgecolor='green', hatch='\\\\')
ax.bar(categories, product_c, bottom=product_a + product_b, label='C', 
       color='white', edgecolor='red', hatch='xx')
ax.legend()
plt.show()
```

### 3. Complete Example

```python
fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(len(categories))
width = 0.25

bars1 = ax.bar(x - width, series1, width, label='2022', color='#3498db', edgecolor='navy')
bars2 = ax.bar(x, series2, width, label='2023', color='#2ecc71', edgecolor='darkgreen')
bars3 = ax.bar(x + width, series3, width, label='2024', color='#e74c3c', edgecolor='darkred')

ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(title='Year')
ax.set_ylabel('Value')
ax.set_title('Grouped Bar Chart Comparison')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Exercises

**Exercise 1.**
Create a stacked bar chart showing monthly sales of three products over four months. Use months `['Jan', 'Feb', 'Mar', 'Apr']` and values: Product A `[10, 15, 12, 18]`, Product B `[8, 12, 15, 10]`, Product C `[5, 8, 10, 12]`. Add a legend and value labels inside each bar segment.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        months = ['Jan', 'Feb', 'Mar', 'Apr']
        prod_a = [10, 15, 12, 18]
        prod_b = [8, 12, 15, 10]
        prod_c = [5, 8, 10, 12]

        fig, ax = plt.subplots(figsize=(8, 6))
        b1 = ax.bar(months, prod_a, label='Product A', color='steelblue')
        b2 = ax.bar(months, prod_b, bottom=prod_a, label='Product B', color='coral')
        bottom_c = [a + b for a, b in zip(prod_a, prod_b)]
        b3 = ax.bar(months, prod_c, bottom=bottom_c, label='Product C', color='mediumseagreen')

        ax.bar_label(b1, label_type='center', fontsize=9)
        ax.bar_label(b2, label_type='center', fontsize=9)
        ax.bar_label(b3, label_type='center', fontsize=9)

        ax.legend()
        ax.set_ylabel('Sales')
        ax.set_title('Stacked Bar Chart')
        plt.show()

---

**Exercise 2.**
Create a 100% stacked bar chart (normalized) from the same data in Exercise 1. Convert each month's values to percentages of the total, so each bar reaches 100%. Use `ax.bar` with computed `bottom` offsets and percentage labels.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        months = ['Jan', 'Feb', 'Mar', 'Apr']
        prod_a = np.array([10, 15, 12, 18])
        prod_b = np.array([8, 12, 15, 10])
        prod_c = np.array([5, 8, 10, 12])
        totals = prod_a + prod_b + prod_c

        pct_a = prod_a / totals * 100
        pct_b = prod_b / totals * 100
        pct_c = prod_c / totals * 100

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(months, pct_a, label='Product A', color='steelblue')
        ax.bar(months, pct_b, bottom=pct_a, label='Product B', color='coral')
        ax.bar(months, pct_c, bottom=pct_a + pct_b, label='Product C', color='mediumseagreen')

        ax.set_ylabel('Percentage (%)')
        ax.set_title('100% Stacked Bar Chart')
        ax.legend()
        ax.set_ylim(0, 100)
        plt.show()

---

**Exercise 3.**
Create a grouped horizontal bar chart using `ax.barh` for comparing exam scores of three students across four subjects. Students: Alice `[85, 90, 78, 92]`, Bob `[70, 88, 95, 80]`, Carol `[92, 75, 82, 88]`. Subjects: `['Math', 'Science', 'English', 'History']`. Use `height=0.25` for grouping.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        subjects = ['Math', 'Science', 'English', 'History']
        alice = [85, 90, 78, 92]
        bob = [70, 88, 95, 80]
        carol = [92, 75, 82, 88]

        y = np.arange(len(subjects))
        height = 0.25

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(y - height, alice, height, label='Alice', color='steelblue')
        ax.barh(y, bob, height, label='Bob', color='coral')
        ax.barh(y + height, carol, height, label='Carol', color='mediumseagreen')

        ax.set_yticks(y)
        ax.set_yticklabels(subjects)
        ax.set_xlabel('Score')
        ax.set_title('Exam Scores by Student')
        ax.legend()
        plt.tight_layout()
        plt.show()
