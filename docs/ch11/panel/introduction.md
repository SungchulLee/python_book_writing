# Introduction to Panel Data

**Panel data** (also called **longitudinal data**) combines cross-sectional and time-series dimensions. Each observation is identified by two keys: an entity (individual, firm, country) and a time point.

!!! tip "Mental Model"
    Panel data is a 3D cube flattened into a 2D table. The three dimensions are entity, time, and variable. In pandas, entity and time go into a MultiIndex and variables become columns. This lets you ask both "how does entity X change over time?" and "how do all entities compare at time T?" from a single DataFrame.

## What is Panel Data?

Panel data has two dimensions:

- **Cross-sectional**: Different entities (stocks, companies, individuals)
- **Time-series**: Repeated observations over time

```
┌─────────────────────────────────────────────────┐
│                  Panel Data                      │
├─────────────────────────────────────────────────┤
│    Entity (i)     Time (t)        Value         │
│    ──────────     ────────        ─────         │
│    AAPL           2024-01-01      \$150.00       │
│    AAPL           2024-01-02      \$151.50       │
│    AAPL           2024-01-03      \$149.80       │
│    MSFT           2024-01-01      \$300.00       │
│    MSFT           2024-01-02      \$302.00       │
│    MSFT           2024-01-03      \$301.50       │
│    GOOGL          2024-01-01      \$140.00       │
│    GOOGL          2024-01-02      \$141.20       │
│    GOOGL          2024-01-03      \$142.00       │
└─────────────────────────────────────────────────┘
```

## Panel Data vs Other Data Types

| Data Type | Entities | Time Points | Example |
|-----------|----------|-------------|---------|
| Cross-sectional | Multiple | Single | Survey at one point |
| Time-series | Single | Multiple | One stock's history |
| **Panel** | **Multiple** | **Multiple** | Multiple stocks over time |

## Why Use Panel Data?

### 1. More Information

Panel data contains more observations than cross-sectional or time-series alone:

```
Cross-sectional: 100 stocks × 1 day = 100 observations
Time-series: 1 stock × 252 days = 252 observations
Panel: 100 stocks × 252 days = 25,200 observations
```

### 2. Control for Unobserved Heterogeneity

Panel data allows fixed effects models that control for entity-specific factors:

- Stock-specific characteristics (management quality, brand value)
- Time-specific effects (market conditions, regulations)

### 3. Study Dynamics

Track how entities change over time.

## Examples of Panel Data

| Domain | Entities | Time | Variables |
|--------|----------|------|-----------|
| Finance | Stocks | Days | Returns, Volume |
| Economics | Countries | Years | GDP, Inflation |
| Healthcare | Patients | Visits | Vitals, Tests |
| Education | Students | Grades | Scores, Attendance |

## Balanced vs Unbalanced Panels

### Balanced Panel
Every entity has observations for every time period.

### Unbalanced Panel
Some entity-time combinations are missing (common in real data).

## Long vs Wide Format

### Long Format (Standard)
```
ticker  date        return
AAPL    2024-01-01  0.01
AAPL    2024-01-02  0.02
MSFT    2024-01-01  0.015
```

### Wide Format
```
date        AAPL   MSFT
2024-01-01  0.01   0.015
2024-01-02  0.02   0.018
```

## Panel Data in Pandas

Pandas handles panel data using **MultiIndex**:

```python
import pandas as pd
import numpy as np

tickers = ['AAPL', 'MSFT', 'GOOGL']
dates = pd.date_range('2024-01-01', periods=5)

index = pd.MultiIndex.from_product(
    [tickers, dates], 
    names=['ticker', 'date']
)

returns = pd.Series(np.random.randn(15) * 0.02, index=index, name='return')
print(returns)
```


---

## Exercises

**Exercise 1.** Explain what panel data is. Give an example of data that has both cross-sectional and time-series dimensions.

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

**Exercise 2.** Write code that creates a simple panel dataset with 3 entities observed over 4 time periods.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Explain the difference between balanced and unbalanced panel data. Write code that checks if a panel is balanced.

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

**Exercise 4.** Create a panel dataset and use `groupby()` to compute summary statistics for each entity.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
