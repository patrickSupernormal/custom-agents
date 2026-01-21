# Data Analysis Methodology

---
name: Data Analysis Methodology
version: 1.0.0
used-by:
  - "@data-analyst"
---

## Overview

This skill defines comprehensive methodologies for data analysis, covering the complete lifecycle from initial dataset assessment through final reporting. Each section provides actionable frameworks, code patterns, and decision matrices for systematic analysis.

---

## 1. Dataset Assessment Framework

### Initial Reconnaissance Checklist

Before diving into analysis, systematically assess the dataset structure and characteristics.

```python
# Python/Pandas Assessment Template
import pandas as pd
import numpy as np

def assess_dataset(df):
    """Comprehensive dataset assessment."""
    assessment = {
        'shape': df.shape,
        'columns': list(df.columns),
        'dtypes': df.dtypes.to_dict(),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'missing_counts': df.isnull().sum().to_dict(),
        'missing_pct': (df.isnull().sum() / len(df) * 100).to_dict(),
        'duplicates': df.duplicated().sum(),
        'unique_counts': {col: df[col].nunique() for col in df.columns}
    }
    return assessment
```

```sql
-- SQL Assessment Queries
-- Row count and basic stats
SELECT
    COUNT(*) as total_rows,
    COUNT(DISTINCT id) as unique_ids,
    MIN(created_at) as earliest_record,
    MAX(created_at) as latest_record
FROM dataset;

-- Column nullability check
SELECT
    'column_name' as column,
    COUNT(*) as total,
    SUM(CASE WHEN column_name IS NULL THEN 1 ELSE 0 END) as null_count,
    ROUND(SUM(CASE WHEN column_name IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as null_pct
FROM dataset;
```

### Data Type Classification Matrix

| Raw Type | Semantic Type | Analysis Approach |
|----------|---------------|-------------------|
| int64/float64 | Continuous | Descriptive stats, distribution plots |
| int64 | Discrete/Count | Frequency analysis, Poisson tests |
| object/string | Categorical | Value counts, chi-square tests |
| datetime64 | Temporal | Time series analysis, seasonality |
| bool | Binary | Proportion tests, logistic patterns |
| object | Text/Unstructured | NLP techniques, keyword extraction |

### Assessment Report Template

```markdown
## Dataset Assessment Report

### Basic Information
- **File**: [filename]
- **Format**: [CSV/JSON/TSV/Parquet]
- **Size**: [X rows x Y columns]
- **Memory**: [Z MB]
- **Date Range**: [start] to [end]

### Column Inventory
| Column | Type | Non-Null | Unique | Sample Values |
|--------|------|----------|--------|---------------|
| col1   | int  | 99.5%    | 1000   | 1, 5, 10      |

### Initial Observations
- [Key observation 1]
- [Key observation 2]
- [Potential issues identified]
```

---

## 2. Exploratory Data Analysis Steps

### EDA Workflow (Sequential)

```
1. LOAD AND VALIDATE
   |
   v
2. STRUCTURAL OVERVIEW
   |
   v
3. UNIVARIATE ANALYSIS
   |
   v
4. BIVARIATE ANALYSIS
   |
   v
5. MULTIVARIATE ANALYSIS
   |
   v
6. HYPOTHESIS GENERATION
```

### Step-by-Step EDA Framework

#### Step 1: Load and Validate

```python
# Load with explicit parameters
df = pd.read_csv('data.csv',
                 parse_dates=['date_column'],
                 dtype={'category_col': 'category'},
                 na_values=['', 'NULL', 'N/A', '-'])

# Validate load success
assert df.shape[0] > 0, "Empty dataset loaded"
assert df.shape[1] == expected_columns, "Column count mismatch"
```

#### Step 2: Structural Overview

```python
# Quick structural summary
def structural_overview(df):
    print(f"Shape: {df.shape}")
    print(f"\nColumn Types:\n{df.dtypes.value_counts()}")
    print(f"\nMissing Values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    print(f"\nSample Rows:\n{df.head()}")
```

#### Step 3: Univariate Analysis

```python
# Numeric columns
def analyze_numeric(series):
    return {
        'count': series.count(),
        'mean': series.mean(),
        'median': series.median(),
        'std': series.std(),
        'min': series.min(),
        'max': series.max(),
        'q25': series.quantile(0.25),
        'q75': series.quantile(0.75),
        'skewness': series.skew(),
        'kurtosis': series.kurtosis()
    }

# Categorical columns
def analyze_categorical(series, top_n=10):
    return {
        'unique_count': series.nunique(),
        'top_values': series.value_counts().head(top_n).to_dict(),
        'mode': series.mode()[0] if len(series.mode()) > 0 else None,
        'missing_pct': series.isnull().sum() / len(series) * 100
    }
```

#### Step 4: Bivariate Analysis

```python
# Numeric vs Numeric: Correlation
correlation_matrix = df.select_dtypes(include=[np.number]).corr()

# Numeric vs Categorical: Group statistics
grouped_stats = df.groupby('category')['numeric_col'].agg(['mean', 'median', 'std'])

# Categorical vs Categorical: Crosstab
crosstab = pd.crosstab(df['cat1'], df['cat2'], normalize='all')
```

#### Step 5: Multivariate Analysis

```python
# Correlation heatmap data
full_corr = df.select_dtypes(include=[np.number]).corr()

# Grouped aggregations
pivot = df.pivot_table(
    values='metric',
    index='dimension1',
    columns='dimension2',
    aggfunc=['mean', 'count']
)
```

---

## 3. Statistical Analysis Patterns

### Descriptive Statistics Template

```python
def comprehensive_descriptive_stats(df, numeric_cols=None):
    """Generate comprehensive descriptive statistics."""
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns

    stats = {}
    for col in numeric_cols:
        data = df[col].dropna()
        stats[col] = {
            # Central Tendency
            'mean': data.mean(),
            'median': data.median(),
            'mode': data.mode().iloc[0] if len(data.mode()) > 0 else np.nan,

            # Dispersion
            'std': data.std(),
            'variance': data.var(),
            'range': data.max() - data.min(),
            'iqr': data.quantile(0.75) - data.quantile(0.25),
            'cv': data.std() / data.mean() if data.mean() != 0 else np.nan,

            # Shape
            'skewness': data.skew(),
            'kurtosis': data.kurtosis(),

            # Position
            'min': data.min(),
            'q1': data.quantile(0.25),
            'q3': data.quantile(0.75),
            'max': data.max(),

            # Percentiles
            'p5': data.quantile(0.05),
            'p95': data.quantile(0.95)
        }

    return pd.DataFrame(stats).T
```

### Common Statistical Tests Decision Matrix

| Scenario | Variables | Test | Python/SQL Pattern |
|----------|-----------|------|-------------------|
| Compare 2 group means | 1 numeric, 1 binary cat | t-test | `scipy.stats.ttest_ind()` |
| Compare 3+ group means | 1 numeric, 1 multi-cat | ANOVA | `scipy.stats.f_oneway()` |
| Association between categoricals | 2 categorical | Chi-square | `scipy.stats.chi2_contingency()` |
| Correlation between numerics | 2 numeric | Pearson/Spearman | `df.corr(method='pearson')` |
| Distribution normality | 1 numeric | Shapiro-Wilk | `scipy.stats.shapiro()` |
| Time series trend | 1 numeric + time | Mann-Kendall | `pymannkendall.original_test()` |

### SQL Statistical Patterns

```sql
-- Percentile calculation (PostgreSQL)
SELECT
    percentile_cont(0.25) WITHIN GROUP (ORDER BY value) as q1,
    percentile_cont(0.50) WITHIN GROUP (ORDER BY value) as median,
    percentile_cont(0.75) WITHIN GROUP (ORDER BY value) as q3
FROM dataset;

-- Standard deviation and variance
SELECT
    AVG(value) as mean,
    STDDEV(value) as std_dev,
    VARIANCE(value) as variance
FROM dataset;

-- Coefficient of variation by group
SELECT
    category,
    AVG(value) as mean,
    STDDEV(value) as std_dev,
    STDDEV(value) / NULLIF(AVG(value), 0) as cv
FROM dataset
GROUP BY category;
```

---

## 4. Data Quality Checks

### Quality Dimensions Checklist

| Dimension | Description | Check Method |
|-----------|-------------|--------------|
| Completeness | Missing values present | Null counts per column |
| Validity | Values within expected ranges | Range/domain validation |
| Accuracy | Values are correct | Sample verification |
| Consistency | No contradictions | Cross-field validation |
| Uniqueness | No unwanted duplicates | Duplicate detection |
| Timeliness | Data is current | Date range analysis |

### Comprehensive Quality Check Functions

```python
def data_quality_report(df):
    """Generate comprehensive data quality report."""
    report = {
        'completeness': {},
        'validity': {},
        'uniqueness': {},
        'consistency': []
    }

    # Completeness
    for col in df.columns:
        missing = df[col].isnull().sum()
        report['completeness'][col] = {
            'missing_count': missing,
            'missing_pct': round(missing / len(df) * 100, 2),
            'complete_pct': round((len(df) - missing) / len(df) * 100, 2)
        }

    # Validity - Numeric ranges
    for col in df.select_dtypes(include=[np.number]).columns:
        report['validity'][col] = {
            'min': df[col].min(),
            'max': df[col].max(),
            'negative_count': (df[col] < 0).sum(),
            'zero_count': (df[col] == 0).sum()
        }

    # Uniqueness
    report['uniqueness'] = {
        'total_rows': len(df),
        'duplicate_rows': df.duplicated().sum(),
        'duplicate_pct': round(df.duplicated().sum() / len(df) * 100, 2)
    }

    return report

def validate_column_rules(df, rules):
    """
    Validate columns against defined rules.

    rules = {
        'age': {'min': 0, 'max': 120, 'nullable': False},
        'email': {'pattern': r'^[\w\.-]+@[\w\.-]+\.\w+$', 'nullable': False},
        'status': {'allowed': ['active', 'inactive', 'pending'], 'nullable': True}
    }
    """
    violations = {}

    for col, rule in rules.items():
        if col not in df.columns:
            violations[col] = ['Column not found']
            continue

        col_violations = []

        # Null check
        if not rule.get('nullable', True) and df[col].isnull().any():
            col_violations.append(f"Contains {df[col].isnull().sum()} null values")

        # Range check
        if 'min' in rule:
            below_min = (df[col] < rule['min']).sum()
            if below_min > 0:
                col_violations.append(f"{below_min} values below minimum {rule['min']}")

        if 'max' in rule:
            above_max = (df[col] > rule['max']).sum()
            if above_max > 0:
                col_violations.append(f"{above_max} values above maximum {rule['max']}")

        # Allowed values check
        if 'allowed' in rule:
            invalid = ~df[col].isin(rule['allowed']) & df[col].notna()
            if invalid.sum() > 0:
                col_violations.append(f"{invalid.sum()} values not in allowed list")

        if col_violations:
            violations[col] = col_violations

    return violations
```

### SQL Quality Check Patterns

```sql
-- Completeness check
SELECT
    COUNT(*) as total_rows,
    SUM(CASE WHEN column1 IS NULL THEN 1 ELSE 0 END) as column1_nulls,
    SUM(CASE WHEN column2 IS NULL THEN 1 ELSE 0 END) as column2_nulls,
    SUM(CASE WHEN column3 IS NULL THEN 1 ELSE 0 END) as column3_nulls
FROM dataset;

-- Duplicate detection
SELECT
    key_column1,
    key_column2,
    COUNT(*) as occurrence_count
FROM dataset
GROUP BY key_column1, key_column2
HAVING COUNT(*) > 1
ORDER BY occurrence_count DESC;

-- Value range validation
SELECT
    SUM(CASE WHEN value < 0 THEN 1 ELSE 0 END) as negative_values,
    SUM(CASE WHEN value > 1000000 THEN 1 ELSE 0 END) as outlier_values,
    SUM(CASE WHEN value IS NULL THEN 1 ELSE 0 END) as null_values
FROM dataset;

-- Referential integrity
SELECT t1.id, t1.foreign_key
FROM table1 t1
LEFT JOIN table2 t2 ON t1.foreign_key = t2.id
WHERE t2.id IS NULL AND t1.foreign_key IS NOT NULL;
```

---

## 5. Visualization Selection Matrix

### Chart Selection Decision Tree

```
START: What is your analysis goal?
|
+-- COMPARISON
|   +-- Categories (few): Bar chart
|   +-- Categories (many): Horizontal bar chart
|   +-- Over time: Line chart
|   +-- Part-to-whole: Stacked bar / 100% stacked bar
|
+-- DISTRIBUTION
|   +-- Single variable: Histogram, Box plot, Violin plot
|   +-- Two variables: Scatter plot
|   +-- Density: KDE plot, Heatmap
|
+-- COMPOSITION
|   +-- Static: Pie chart (max 5-7 categories), Treemap
|   +-- Over time: Stacked area chart
|
+-- RELATIONSHIP
|   +-- Two numeric: Scatter plot
|   +-- Multiple numeric: Correlation heatmap, Pair plot
|   +-- Categorical + Numeric: Box plot by category
|
+-- TREND
|   +-- Time series: Line chart with trend line
|   +-- With seasonality: Decomposition plot
```

### Visualization Selection Matrix

| Data Type | Goal | Recommended Chart | Alternative |
|-----------|------|-------------------|-------------|
| 1 Numeric | Distribution | Histogram | Box plot, KDE |
| 1 Categorical | Frequency | Bar chart | Pie (if <= 5 cats) |
| 2 Numeric | Correlation | Scatter plot | Hexbin (large data) |
| 1 Numeric + 1 Cat | Comparison | Box plot | Violin plot |
| 2 Categorical | Association | Heatmap | Grouped bar |
| Time + Numeric | Trend | Line chart | Area chart |
| Multiple Numeric | Relationships | Correlation heatmap | Pair plot |
| Hierarchical | Composition | Treemap | Sunburst |

### Chart Configuration Best Practices

```python
# Standard chart configurations
CHART_CONFIGS = {
    'bar': {
        'orientation': 'vertical',  # horizontal for many categories
        'sort': True,  # sort by value
        'limit_categories': 10,  # group rest as "Other"
        'show_values': True  # data labels
    },
    'line': {
        'marker': True,  # show data points
        'smooth': False,  # avoid unless trend focus
        'fill_missing': 'interpolate'  # or 'zero', 'previous'
    },
    'histogram': {
        'bins': 'auto',  # or specify number
        'show_kde': True,  # overlay density curve
        'log_scale': False  # enable for skewed data
    },
    'scatter': {
        'alpha': 0.6,  # transparency for overlapping
        'trend_line': True,
        'size_by': None,  # third variable
        'color_by': None  # categorical grouping
    },
    'heatmap': {
        'annotate': True,  # show values
        'cmap': 'RdBu_r',  # diverging for correlations
        'center': 0  # for correlation matrices
    }
}
```

---

## 6. Pattern Detection Methods

### Trend Detection

```python
def detect_trend(series, window=7):
    """Detect trend direction and strength."""
    # Moving average
    ma = series.rolling(window=window).mean()

    # Linear regression slope
    from scipy import stats
    x = np.arange(len(series))
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, series.fillna(method='ffill'))

    # Trend classification
    if p_value > 0.05:
        trend = 'no significant trend'
    elif slope > 0:
        trend = 'upward'
    else:
        trend = 'downward'

    return {
        'trend_direction': trend,
        'slope': slope,
        'r_squared': r_value**2,
        'p_value': p_value,
        'moving_average': ma
    }
```

### Seasonality Detection

```python
def detect_seasonality(series, periods=[7, 30, 365]):
    """Detect seasonality patterns."""
    from scipy import signal

    # Remove trend
    detrended = signal.detrend(series.dropna())

    # Autocorrelation at different lags
    results = {}
    for period in periods:
        if len(series) > period * 2:
            autocorr = pd.Series(detrended).autocorr(lag=period)
            results[f'period_{period}'] = {
                'autocorrelation': autocorr,
                'likely_seasonal': abs(autocorr) > 0.3
            }

    return results
```

### Correlation Pattern Analysis

```python
def correlation_analysis(df, target_col=None, threshold=0.5):
    """Analyze correlations and identify strong relationships."""
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()

    # Find strong correlations
    strong_correlations = []
    for i, col1 in enumerate(corr_matrix.columns):
        for j, col2 in enumerate(corr_matrix.columns):
            if i < j:  # Upper triangle only
                corr = corr_matrix.iloc[i, j]
                if abs(corr) >= threshold:
                    strong_correlations.append({
                        'variable_1': col1,
                        'variable_2': col2,
                        'correlation': round(corr, 4),
                        'strength': 'strong' if abs(corr) > 0.7 else 'moderate',
                        'direction': 'positive' if corr > 0 else 'negative'
                    })

    # Target correlations if specified
    target_corr = None
    if target_col and target_col in corr_matrix.columns:
        target_corr = corr_matrix[target_col].drop(target_col).sort_values(ascending=False)

    return {
        'correlation_matrix': corr_matrix,
        'strong_correlations': sorted(strong_correlations, key=lambda x: abs(x['correlation']), reverse=True),
        'target_correlations': target_corr
    }
```

### Cluster/Segment Detection

```python
def segment_analysis(df, numeric_cols, n_segments=4):
    """Identify natural segments in data."""
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans

    # Prepare data
    data = df[numeric_cols].dropna()
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    # Find optimal clusters (elbow method)
    inertias = []
    K_range = range(2, min(10, len(data) // 10))
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(scaled_data)
        inertias.append(kmeans.inertia_)

    # Apply segmentation
    kmeans = KMeans(n_clusters=n_segments, random_state=42, n_init=10)
    segments = kmeans.fit_predict(scaled_data)

    # Segment profiles
    df_segmented = data.copy()
    df_segmented['segment'] = segments
    segment_profiles = df_segmented.groupby('segment').agg(['mean', 'std', 'count'])

    return {
        'segment_labels': segments,
        'segment_profiles': segment_profiles,
        'elbow_data': list(zip(K_range, inertias))
    }
```

---

## 7. Anomaly Identification

### Statistical Anomaly Detection

```python
def detect_anomalies_iqr(series, multiplier=1.5):
    """Detect anomalies using IQR method."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - (multiplier * iqr)
    upper_bound = q3 + (multiplier * iqr)

    anomalies = series[(series < lower_bound) | (series > upper_bound)]

    return {
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'anomaly_count': len(anomalies),
        'anomaly_pct': len(anomalies) / len(series) * 100,
        'anomaly_indices': anomalies.index.tolist(),
        'anomaly_values': anomalies.tolist()
    }

def detect_anomalies_zscore(series, threshold=3):
    """Detect anomalies using Z-score method."""
    z_scores = (series - series.mean()) / series.std()
    anomalies = series[abs(z_scores) > threshold]

    return {
        'threshold': threshold,
        'anomaly_count': len(anomalies),
        'anomaly_pct': len(anomalies) / len(series) * 100,
        'anomaly_indices': anomalies.index.tolist(),
        'z_scores': z_scores[abs(z_scores) > threshold].tolist()
    }
```

### Time-Series Anomaly Detection

```python
def detect_timeseries_anomalies(series, window=7, sigma=2):
    """Detect anomalies in time series using rolling statistics."""
    rolling_mean = series.rolling(window=window).mean()
    rolling_std = series.rolling(window=window).std()

    upper_band = rolling_mean + (sigma * rolling_std)
    lower_band = rolling_mean - (sigma * rolling_std)

    anomalies = series[(series > upper_band) | (series < lower_band)]

    return {
        'anomaly_count': len(anomalies),
        'anomaly_dates': anomalies.index.tolist(),
        'anomaly_values': anomalies.tolist(),
        'upper_band': upper_band,
        'lower_band': lower_band,
        'rolling_mean': rolling_mean
    }
```

### SQL Anomaly Detection Patterns

```sql
-- IQR-based anomaly detection
WITH stats AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY value) as q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY value) as q3
    FROM dataset
),
bounds AS (
    SELECT
        q1 - 1.5 * (q3 - q1) as lower_bound,
        q3 + 1.5 * (q3 - q1) as upper_bound
    FROM stats
)
SELECT d.*
FROM dataset d, bounds b
WHERE d.value < b.lower_bound OR d.value > b.upper_bound;

-- Z-score anomalies
WITH stats AS (
    SELECT
        AVG(value) as mean_val,
        STDDEV(value) as std_val
    FROM dataset
)
SELECT
    d.*,
    (d.value - s.mean_val) / s.std_val as z_score
FROM dataset d, stats s
WHERE ABS((d.value - s.mean_val) / s.std_val) > 3;
```

### Anomaly Report Template

```markdown
## Anomaly Detection Report

### Summary
- **Total Records Analyzed**: [N]
- **Anomalies Detected**: [X] ([Y]%)
- **Detection Method**: [IQR/Z-score/Rolling Window]
- **Threshold**: [value]

### Anomaly Details
| Record ID | Value | Expected Range | Deviation |
|-----------|-------|----------------|-----------|
| 123       | 999   | 10-100         | +899%     |

### Potential Causes
1. [Data entry error]
2. [Legitimate extreme value]
3. [System malfunction]

### Recommended Actions
- [Investigate record 123]
- [Validate with source system]
```

---

## 8. Reporting Templates

### Executive Summary Template

```markdown
# Data Analysis Report: [Title]

## Executive Summary
**Analysis Period**: [Date Range]
**Dataset**: [Description]
**Key Finding**: [One-sentence headline finding]

### Key Metrics
| Metric | Current | Previous | Change |
|--------|---------|----------|--------|
| [KPI 1] | [value] | [value] | [+/-]% |
| [KPI 2] | [value] | [value] | [+/-]% |

### Top 3 Insights
1. **[Insight Title]**: [Description with supporting data]
2. **[Insight Title]**: [Description with supporting data]
3. **[Insight Title]**: [Description with supporting data]

### Recommendations
1. [Action item with expected impact]
2. [Action item with expected impact]
3. [Action item with expected impact]
```

### Technical Analysis Report Template

```markdown
# Technical Analysis Report

## 1. Dataset Overview
- **Source**: [filename/database]
- **Shape**: [rows] rows x [columns] columns
- **Date Range**: [start] to [end]
- **Data Quality Score**: [X]%

## 2. Methodology
- **Tools Used**: [Pandas, SQL, etc.]
- **Statistical Methods**: [List methods applied]
- **Assumptions**: [List key assumptions]

## 3. Data Quality Assessment
### Completeness
| Column | Complete % | Missing Count |
|--------|------------|---------------|

### Validity Issues
[List any data quality issues found]

## 4. Statistical Analysis

### Descriptive Statistics
[Include key summary statistics table]

### Correlation Analysis
[Include correlation findings]

### Distribution Analysis
[Include distribution characteristics]

## 5. Findings

### Finding 1: [Title]
- **Observation**: [What was observed]
- **Evidence**: [Supporting data/statistics]
- **Implication**: [What this means]

## 6. Appendix
- Data dictionary
- Full statistical tables
- Methodology details
```

### Automated Report Generation

```python
def generate_analysis_report(df, output_file='analysis_report.md'):
    """Generate markdown analysis report."""
    report = []

    # Header
    report.append("# Automated Data Analysis Report")
    report.append(f"\n**Generated**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")

    # Overview
    report.append("\n## Dataset Overview")
    report.append(f"- **Rows**: {df.shape[0]:,}")
    report.append(f"- **Columns**: {df.shape[1]}")
    report.append(f"- **Memory Usage**: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    # Data Quality
    report.append("\n## Data Quality")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        report.append("\n### Missing Values")
        report.append("| Column | Missing | Percentage |")
        report.append("|--------|---------|------------|")
        for col in missing[missing > 0].index:
            pct = missing[col] / len(df) * 100
            report.append(f"| {col} | {missing[col]:,} | {pct:.1f}% |")

    # Numeric Statistics
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        report.append("\n## Numeric Column Statistics")
        report.append("| Column | Mean | Median | Std Dev | Min | Max |")
        report.append("|--------|------|--------|---------|-----|-----|")
        for col in numeric_cols:
            stats = df[col].describe()
            report.append(f"| {col} | {stats['mean']:.2f} | {stats['50%']:.2f} | "
                         f"{stats['std']:.2f} | {stats['min']:.2f} | {stats['max']:.2f} |")

    # Categorical Statistics
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(cat_cols) > 0:
        report.append("\n## Categorical Column Statistics")
        for col in cat_cols:
            report.append(f"\n### {col}")
            report.append(f"- **Unique Values**: {df[col].nunique()}")
            top_5 = df[col].value_counts().head(5)
            report.append("\n| Value | Count | Percentage |")
            report.append("|-------|-------|------------|")
            for val, count in top_5.items():
                pct = count / len(df) * 100
                report.append(f"| {val} | {count:,} | {pct:.1f}% |")

    return '\n'.join(report)
```

---

## 9. Common Metrics and KPIs

### Business Metrics by Domain

#### E-commerce/Retail
| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Conversion Rate | Purchases / Visits * 100 | % of visitors who buy |
| Average Order Value (AOV) | Total Revenue / Number of Orders | Spend per transaction |
| Customer Lifetime Value (CLV) | AOV * Purchase Frequency * Lifespan | Total customer value |
| Cart Abandonment Rate | Abandoned Carts / Created Carts * 100 | Lost sales opportunity |
| Return Rate | Returned Items / Sold Items * 100 | Product satisfaction |

#### SaaS/Product
| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Monthly Recurring Revenue (MRR) | Sum of monthly subscription values | Predictable revenue |
| Churn Rate | Lost Customers / Starting Customers * 100 | Customer retention |
| Daily Active Users (DAU) | Unique users in 24h | Engagement level |
| DAU/MAU Ratio | DAU / Monthly Active Users | Stickiness |
| Net Promoter Score (NPS) | % Promoters - % Detractors | Customer satisfaction |

#### Marketing
| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Customer Acquisition Cost (CAC) | Marketing Spend / New Customers | Cost to acquire |
| Return on Ad Spend (ROAS) | Revenue from Ads / Ad Spend | Ad effectiveness |
| Click-Through Rate (CTR) | Clicks / Impressions * 100 | Ad engagement |
| Cost Per Lead (CPL) | Campaign Cost / Leads Generated | Lead generation efficiency |

### Metric Calculation Patterns

```python
def calculate_growth_metrics(df, value_col, date_col):
    """Calculate growth and change metrics."""
    df = df.sort_values(date_col)

    metrics = {
        # Period over period
        'daily_change': df[value_col].diff(),
        'daily_pct_change': df[value_col].pct_change() * 100,

        # Rolling metrics
        'rolling_7d_avg': df[value_col].rolling(7).mean(),
        'rolling_30d_avg': df[value_col].rolling(30).mean(),

        # Cumulative
        'cumulative_sum': df[value_col].cumsum(),
        'cumulative_max': df[value_col].cummax(),

        # Growth rates
        'week_over_week': df[value_col].pct_change(periods=7) * 100,
        'month_over_month': df[value_col].pct_change(periods=30) * 100
    }

    return pd.DataFrame(metrics, index=df.index)

def calculate_cohort_metrics(df, user_col, date_col, value_col):
    """Calculate cohort-based retention metrics."""
    # Assign cohort (first activity month)
    df['cohort'] = df.groupby(user_col)[date_col].transform('min').dt.to_period('M')
    df['period'] = df[date_col].dt.to_period('M')
    df['cohort_age'] = (df['period'] - df['cohort']).apply(lambda x: x.n)

    # Cohort pivot
    cohort_data = df.groupby(['cohort', 'cohort_age'])[user_col].nunique().unstack(fill_value=0)

    # Retention rates
    cohort_sizes = cohort_data[0]
    retention = cohort_data.divide(cohort_sizes, axis=0) * 100

    return {
        'cohort_sizes': cohort_sizes,
        'retention_matrix': retention
    }
```

### SQL KPI Calculation Patterns

```sql
-- Conversion funnel
SELECT
    COUNT(DISTINCT CASE WHEN event = 'visit' THEN user_id END) as visits,
    COUNT(DISTINCT CASE WHEN event = 'add_to_cart' THEN user_id END) as cart_adds,
    COUNT(DISTINCT CASE WHEN event = 'purchase' THEN user_id END) as purchases,
    ROUND(COUNT(DISTINCT CASE WHEN event = 'purchase' THEN user_id END) * 100.0 /
          NULLIF(COUNT(DISTINCT CASE WHEN event = 'visit' THEN user_id END), 0), 2) as conversion_rate
FROM events
WHERE date >= CURRENT_DATE - INTERVAL '30 days';

-- Month-over-month growth
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', date) as month,
        SUM(revenue) as revenue
    FROM sales
    GROUP BY 1
)
SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) as prev_month_revenue,
    ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) * 100.0 /
          NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 2) as mom_growth_pct
FROM monthly;

-- Rolling averages
SELECT
    date,
    value,
    AVG(value) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as rolling_7d_avg,
    AVG(value) OVER (ORDER BY date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) as rolling_30d_avg
FROM daily_metrics;
```

---

## 10. Tool Recommendations

### Python/Pandas Patterns

#### Data Loading Best Practices

```python
# Optimized CSV loading
df = pd.read_csv(
    'large_file.csv',
    dtype={
        'id': 'int32',
        'category': 'category',
        'value': 'float32'
    },
    parse_dates=['date_column'],
    usecols=['id', 'category', 'value', 'date_column'],  # Only needed columns
    nrows=1000000  # Limit rows for initial exploration
)

# Chunked processing for large files
def process_large_csv(filepath, chunksize=100000):
    results = []
    for chunk in pd.read_csv(filepath, chunksize=chunksize):
        # Process each chunk
        chunk_result = chunk.groupby('category')['value'].sum()
        results.append(chunk_result)
    return pd.concat(results).groupby(level=0).sum()
```

#### Memory Optimization

```python
def optimize_dataframe(df):
    """Reduce memory usage of DataFrame."""
    for col in df.columns:
        col_type = df[col].dtype

        if col_type == 'object':
            # Convert to category if low cardinality
            if df[col].nunique() / len(df) < 0.5:
                df[col] = df[col].astype('category')

        elif col_type == 'int64':
            # Downcast integers
            df[col] = pd.to_numeric(df[col], downcast='integer')

        elif col_type == 'float64':
            # Downcast floats
            df[col] = pd.to_numeric(df[col], downcast='float')

    return df
```

#### Efficient Aggregations

```python
# Fast groupby operations
def efficient_groupby(df, group_cols, agg_dict):
    """Optimized groupby with named aggregations."""
    return df.groupby(group_cols, observed=True).agg(**{
        f'{col}_{func}': (col, func)
        for col, funcs in agg_dict.items()
        for func in (funcs if isinstance(funcs, list) else [funcs])
    })

# Example usage
result = efficient_groupby(df,
    group_cols=['region', 'product'],
    agg_dict={
        'revenue': ['sum', 'mean'],
        'quantity': ['sum', 'count']
    }
)
```

### SQL Query Optimization Patterns

#### Indexing Strategy

```sql
-- Create indexes for common query patterns
CREATE INDEX idx_date ON sales(date);
CREATE INDEX idx_category_date ON sales(category, date);
CREATE INDEX idx_customer ON sales(customer_id);

-- Composite index for multi-column filters
CREATE INDEX idx_status_date ON orders(status, created_at);
```

#### Query Optimization

```sql
-- Use CTEs for complex queries
WITH daily_totals AS (
    SELECT
        date,
        SUM(revenue) as total_revenue
    FROM sales
    GROUP BY date
),
daily_with_rolling AS (
    SELECT
        date,
        total_revenue,
        AVG(total_revenue) OVER (
            ORDER BY date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) as rolling_7d_avg
    FROM daily_totals
)
SELECT * FROM daily_with_rolling
WHERE date >= CURRENT_DATE - INTERVAL '30 days';

-- Avoid SELECT * in production
SELECT
    id,
    customer_id,
    order_date,
    total_amount
FROM orders
WHERE status = 'completed'
  AND order_date >= '2024-01-01';

-- Use EXISTS instead of IN for subqueries
SELECT o.*
FROM orders o
WHERE EXISTS (
    SELECT 1 FROM customers c
    WHERE c.id = o.customer_id
    AND c.status = 'premium'
);
```

### Tool Selection Matrix

| Task | Recommended Tool | Alternative |
|------|------------------|-------------|
| Data loading (small/medium) | pandas | polars |
| Data loading (large) | polars, dask | pandas with chunking |
| Complex transformations | pandas | SQL |
| Aggregations (in-memory) | pandas groupby | numpy |
| Aggregations (large data) | SQL | dask, spark |
| Statistical tests | scipy.stats | statsmodels |
| Time series | pandas + statsmodels | prophet |
| Visualization (static) | matplotlib, seaborn | plotly |
| Visualization (interactive) | plotly | altair, bokeh |
| ML preprocessing | scikit-learn | pandas |

### Performance Comparison Reference

```python
# Benchmark different approaches
import time

def benchmark(func, *args, n_runs=5):
    """Benchmark function execution time."""
    times = []
    for _ in range(n_runs):
        start = time.time()
        func(*args)
        times.append(time.time() - start)
    return {
        'mean_time': np.mean(times),
        'std_time': np.std(times),
        'min_time': np.min(times)
    }

# Example: Compare groupby methods
# Method 1: Standard groupby
result1 = df.groupby('category')['value'].sum()

# Method 2: Using transform (when needing original index)
result2 = df.groupby('category')['value'].transform('sum')

# Method 3: Using pivot_table
result3 = df.pivot_table(values='value', index='category', aggfunc='sum')
```

---

## Quick Reference Card

### Analysis Workflow Checklist

```
[ ] 1. Load and validate data
[ ] 2. Check shape, dtypes, memory
[ ] 3. Assess data quality (missing, duplicates, validity)
[ ] 4. Calculate descriptive statistics
[ ] 5. Analyze distributions (numeric columns)
[ ] 6. Analyze frequencies (categorical columns)
[ ] 7. Check correlations
[ ] 8. Detect patterns and trends
[ ] 9. Identify anomalies
[ ] 10. Generate report with findings
```

### Common One-Liners

```python
# Quick data overview
df.info(memory_usage='deep')
df.describe(include='all')

# Missing data heatmap data
df.isnull().sum().sort_values(ascending=False)

# Correlation with target
df.corrwith(df['target']).sort_values(ascending=False)

# Top categories by mean
df.groupby('category')['value'].mean().nlargest(10)

# Duplicate check
df[df.duplicated(keep=False)].sort_values(by='key_column')

# Date range
df['date'].agg(['min', 'max', 'count'])
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01-21 | Initial release |
