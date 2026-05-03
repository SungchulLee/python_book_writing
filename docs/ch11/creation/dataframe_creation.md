# DataFrame Creation

DataFrames can be created from various data structures including dictionaries, lists, NumPy arrays, and other DataFrames.

!!! tip "Mental Model"
    Every DataFrame constructor answers the same question: "How should I interpret this raw data as rows and columns?" A dict of lists reads keys as column names. A list of dicts reads keys as column names per row. A 2D array needs explicit column labels. Choose the constructor that matches how your source data is already organized.

## From Dictionary of Lists

Column-oriented data with lists as values.

### 1. Basic Dictionary

```python
import pandas as pd

data = {
    'temperature': [32, 35, 28],
    'windspeed': [6, 7, 2],
    'event': ['Rain', 'Sunny', 'Snow']
}

df = pd.DataFrame(data)
print(df)
```

```
   temperature  windspeed  event
0           32          6   Rain
1           35          7  Sunny
2           28          2   Snow
```

### 2. With Custom Index

```python
day = ['1/1/2017', '1/2/2017', '1/3/2017']
df = pd.DataFrame(data, index=day)
print(df)
```

```
          temperature  windspeed  event
1/1/2017           32          6   Rain
1/2/2017           35          7  Sunny
1/3/2017           28          2   Snow
```

### 3. Access Attributes

```python
print(df.index)    # Index(['1/1/2017', '1/2/2017', '1/3/2017'])
print(df.columns)  # Index(['temperature', 'windspeed', 'event'])
```

## From Dictionary of Dictionaries

Row keys become the index automatically.

### 1. Nested Dictionaries

```python
temp  = {'1/1/2017': 32, '1/2/2017': 35, '1/3/2017': 28}
wind  = {'1/1/2017': 6, '1/2/2017': 7, '1/3/2017': 2}
event = {'1/1/2017': 'Rain', '1/2/2017': 'Sunny', '1/3/2017': 'Snow'}

data = {'temperature': temp, 'windspeed': wind, 'event': event}
df = pd.DataFrame(data)
print(df)
```

### 2. Automatic Index

Keys from inner dictionaries become the DataFrame index.

### 3. Handling Missing Keys

```python
# If inner dicts have different keys, NaN fills missing values
```

## From List of Lists

Row-oriented data with each inner list as a row.

### 1. Basic List of Lists

```python
data = [
    ['1/1/2017', 32, 6, 'Rain'],
    ['1/2/2017', 35, 7, 'Sunny'],
    ['1/3/2017', 28, 2, 'Snow']
]

columns = ['day', 'temperature', 'windspeed', 'event']
df = pd.DataFrame(data, columns=columns)
print(df)
```

### 2. Set Column as Index

```python
df = df.set_index('day')
```

### 3. Direct Index Assignment

```python
df = pd.DataFrame(data, columns=columns).set_index('day')
```

## From List of Dictionaries

Each dictionary represents a row.

### 1. Row Dictionaries

```python
data = [
    {'day': '1/1/2017', 'temperature': 32, 'windspeed': 6, 'event': 'Rain'},
    {'day': '1/2/2017', 'temperature': 35, 'windspeed': 7, 'event': 'Sunny'},
    {'day': '1/3/2017', 'temperature': 28, 'windspeed': 2, 'event': 'Snow'}
]

df = pd.DataFrame(data).set_index('day')
```

### 2. Automatic Column Detection

Column names are inferred from dictionary keys.

### 3. Missing Keys

```python
# Missing keys in some dicts result in NaN values
```

## From NumPy Array

Create DataFrame from 2D array.

### 1. Random Data

```python
import numpy as np

np.random.seed(0)
data = np.random.normal(size=(3, 4))

index = ['Jenny', 'Frank', 'Wenfei']
columns = list('ABCD')

df = pd.DataFrame(data, index=index, columns=columns)
print(df)
```

```
               A         B         C         D
Jenny   1.764052  0.400157  0.978738  2.240893
Frank   1.867558 -0.977278  0.950088 -0.151357
Wenfei -0.103219  0.410599  0.144044  1.454274
```

### 2. Specify dtype

```python
df = pd.DataFrame(data, dtype=float)
```

### 3. Shape Preservation

DataFrame shape matches array shape.

## LeetCode Example

Create DataFrame from list of student data.

### 1. Sample Data

```python
student_data = [
    [101, 20],
    [102, 22],
    [103, 21]
]
```

### 2. Create DataFrame

```python
df = pd.DataFrame(student_data, columns=['student_id', 'age'])
print(df)
```

```
   student_id  age
0         101   20
1         102   22
2         103   21
```

### 3. Type Annotation

```python
from typing import List

def createDataframe(student_data: List[List[int]]) -> pd.DataFrame:
    return pd.DataFrame(student_data, columns=['student_id', 'age'])
```

---

## Exercises

**Exercise 1.**
Create a DataFrame from a dictionary where keys are `'ticker'`, `'sector'`, and `'market_cap'` with at least four rows of sample stock data. Set the `'ticker'` column as the index after creation using `set_index`.

??? success "Solution to Exercise 1"
    Create from a dictionary and set the index.

        import pandas as pd

        df = pd.DataFrame({
            'ticker': ['AAPL', 'MSFT', 'GOOGL', 'AMZN'],
            'sector': ['Tech', 'Tech', 'Tech', 'Consumer'],
            'market_cap': [2800, 2400, 1800, 1500]
        })
        df = df.set_index('ticker')
        print(df)

---

**Exercise 2.**
Create a DataFrame from a list of dictionaries where each dictionary represents a student with keys `'name'`, `'grade'`, and `'score'`. One of the dictionaries should be missing the `'score'` key. Print the DataFrame and observe how pandas handles the missing value.

??? success "Solution to Exercise 2"
    Missing keys in dictionaries produce `NaN` in the DataFrame.

        import pandas as pd

        students = [
            {'name': 'Alice', 'grade': 'A', 'score': 95},
            {'name': 'Bob', 'grade': 'B', 'score': 85},
            {'name': 'Carol', 'grade': 'A'},  # Missing 'score'
        ]
        df = pd.DataFrame(students)
        print(df)
        # Carol's score will be NaN

---

**Exercise 3.**
Create a DataFrame from a 3x4 NumPy random array. Assign custom column names `['Q1', 'Q2', 'Q3', 'Q4']` and custom index labels `['2022', '2023', '2024']`. Then verify the shape is `(3, 4)`.

??? success "Solution to Exercise 3"
    Create from a NumPy array with custom labels.

        import pandas as pd
        import numpy as np

        np.random.seed(42)
        data = np.random.rand(3, 4)
        df = pd.DataFrame(
            data,
            columns=['Q1', 'Q2', 'Q3', 'Q4'],
            index=['2022', '2023', '2024']
        )
        print(df)
        print(f"Shape: {df.shape}")  # (3, 4)
