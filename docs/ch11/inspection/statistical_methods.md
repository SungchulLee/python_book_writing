# Statistical Methods

DataFrame methods for computing statistical measures.

!!! tip "Mental Model"
    Statistical methods reduce a column to a single number: `mean()` for center, `std()` for spread, `median()` for a robust center, `corr()` for pairwise relationships. `describe()` bundles the most common statistics into one call. All of these skip NaN by default.

## Central Tendency

Measures of central location.

### 1. mean

```python
import pandas as pd

df = pd.read_csv('housing.csv')

# Single column
print(df['median_income'].mean())

# All numeric columns
print(df.mean())
```

### 2. median

```python
print(df['median_income'].median())
print(df.median())
```

### 3. mode

```python
print(df['ocean_proximity'].mode())  # Most frequent value
```

## Dispersion

Measures of spread.

### 1. std (Standard Deviation)

```python
print(df['median_income'].std())
print(df.std())
```

### 2. var (Variance)

```python
print(df['median_income'].var())
print(df.var())
```

### 3. Range

```python
# Calculate range manually
range_val = df['median_income'].max() - df['median_income'].min()
```

## Correlation and Covariance

Relationships between columns.

### 1. corr (Correlation)

```python
# Correlation matrix
print(df.corr())
```

```
                    housing_median_age  total_rooms  median_income
housing_median_age            1.000000    -0.361262      -0.119034
total_rooms                  -0.361262     1.000000       0.198050
median_income                -0.119034     0.198050       1.000000
```

### 2. Two Columns

```python
print(df['median_income'].corr(df['median_house_value']))
```

### 3. cov (Covariance)

```python
print(df.cov())
```

## Quantiles

Distribution percentiles.

### 1. quantile

```python
# Single quantile
q1 = df['median_income'].quantile(0.25)
q2 = df['median_income'].quantile(0.50)  # Median
q3 = df['median_income'].quantile(0.75)

print(f"Q1: {q1}, Q2: {q2}, Q3: {q3}")
```

### 2. Multiple Quantiles

```python
quantiles = df['median_income'].quantile([0.25, 0.5, 0.75])
print(quantiles)
```

### 3. IQR (Interquartile Range)

```python
iqr = q3 - q1
```

## Cumulative Methods

Running totals and products.

### 1. cumsum

```python
df['cumulative_sales'] = df['sales'].cumsum()
```

### 2. cumprod

```python
# Cumulative returns
df['cumulative_return'] = (1 + df['daily_return']).cumprod()
```

### 3. cummax and cummin

```python
df['running_max'] = df['price'].cummax()
df['running_min'] = df['price'].cummin()
```

## Summary Statistics

### 1. describe

```python
print(df.describe())
```

### 2. Custom Percentiles

```python
print(df.describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9]))
```

### 3. Include All Types

```python
print(df.describe(include='all'))
```

## Financial Example

Income distribution analysis.

### 1. Load Data

```python
url = 'https://raw.githubusercontent.com/gedeck/practical-statistics-for-data-scientists/master/data/loans_income.csv'
loans = pd.read_csv(url)
```

### 2. Calculate Statistics

```python
mean_income = loans['x'].mean()
median_income = loans['x'].median()
std_income = loans['x'].std()

print(f"Mean: {mean_income:.2f}")
print(f"Median: {median_income:.2f}")
print(f"Std: {std_income:.2f}")
```

### 3. Outlier Detection

```python
# Values beyond 3 standard deviations
lower = mean_income - 3 * std_income
upper = mean_income + 3 * std_income

outliers = loans[(loans['x'] < lower) | (loans['x'] > upper)]
print(f"Outliers: {len(outliers)}")
```

## Normal Distribution Check

Verify 68-95-99.7 rule.

### 1. One Standard Deviation

```python
n = len(df['x'])
within_1std = len(df['x'][(mean - std < df['x']) & (df['x'] < mean + std)])
print(f"Within 1 std: {within_1std/n*100:.1f}%")  # ~68%
```

### 2. Two Standard Deviations

```python
within_2std = len(df['x'][(mean - 2*std < df['x']) & (df['x'] < mean + 2*std)])
print(f"Within 2 std: {within_2std/n*100:.1f}%")  # ~95%
```

### 3. Three Standard Deviations

```python
within_3std = len(df['x'][(mean - 3*std < df['x']) & (df['x'] < mean + 3*std)])
print(f"Within 3 std: {within_3std/n*100:.1f}%")  # ~99.7%
```

## Skewness and Kurtosis

Distribution shape.

### 1. skew

```python
print(df['median_income'].skew())
# Positive: right-skewed
# Negative: left-skewed
# Zero: symmetric
```

### 2. kurtosis

```python
print(df['median_income'].kurtosis())
# High: heavy tails
# Low: light tails
```

### 3. Interpretation

```python
skewness = df['x'].skew()
if abs(skewness) < 0.5:
    print("Approximately symmetric")
elif skewness > 0:
    print("Right-skewed")
else:
    print("Left-skewed")
```

---

## Exercises

**Exercise 1.**
Create a DataFrame with columns `'A'` and `'B'` containing 1000 random values. Compute the mean, median, and standard deviation for each column. Verify that the median equals the 0.5 quantile using `.quantile(0.5)`.

??? success "Solution to Exercise 1"
    Compute central tendency measures and verify quantile.

        import pandas as pd
        import numpy as np

        np.random.seed(42)
        df = pd.DataFrame({
            'A': np.random.randn(1000),
            'B': np.random.randn(1000) * 2 + 5
        })
        print("Mean:\n", df.mean())
        print("Median:\n", df.median())
        print("Std:\n", df.std())
        assert df['A'].median() == df['A'].quantile(0.5)
        print("Median equals 0.5 quantile: True")

---

**Exercise 2.**
Given a numeric Series, use `.cumsum()` to compute the cumulative sum and `.cummax()` to compute the running maximum. Create a new column that shows the difference between the running maximum and the current value (a "drawdown" measure).

??? success "Solution to Exercise 2"
    Compute cumulative sum, running max, and drawdown.

        import pandas as pd
        import numpy as np

        np.random.seed(42)
        s = pd.Series(np.random.randn(20).cumsum(), name='price')
        df = pd.DataFrame({'price': s})
        df['cumsum'] = df['price'].cumsum()
        df['running_max'] = df['price'].cummax()
        df['drawdown'] = df['running_max'] - df['price']
        print(df)

---

**Exercise 3.**
Create a DataFrame with two numeric columns. Compute the correlation between them using `.corr()`. Then compute skewness and kurtosis for one column and interpret whether the distribution is approximately symmetric.

??? success "Solution to Exercise 3"
    Compute correlation, skewness, and kurtosis.

        import pandas as pd
        import numpy as np

        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.randn(500),
            'y': np.random.randn(500) + 1
        })
        print("Correlation:\n", df.corr())
        skew = df['x'].skew()
        kurt = df['x'].kurtosis()
        print(f"Skewness of x: {skew:.4f}")
        print(f"Kurtosis of x: {kurt:.4f}")
        if abs(skew) < 0.5:
            print("Distribution is approximately symmetric")
        else:
            print("Distribution is skewed")
