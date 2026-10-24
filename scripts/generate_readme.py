# ============================================
# IMPORTS & PATHS SETUP
# ============================================
## Imports
from pathlib import Path
import pandas as pd
from extract_stats import (
    calculate_overall_stats, 
    calculate_education_stats, 
    calculate_experience_stats
)

## Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / 'data'
README_PATH = BASE_DIR / 'README.md'




def generate_readme():
    # Load CSV
    df = pd.read_csv(DATA_PATH / 'clean-salary-data.csv')

    # Calculations
    overall_stats = calculate_overall_stats(df) # dict type
    edu_stats = calculate_education_stats(df) # dt type
    exp_stats = calculate_experience_stats(df) # dict type

    # Format Education Stats columns for display 
    edu_display = edu_stats.copy() 
    for col in ['mean', 'median', 'std']:
        edu_display[col] = edu_display[col].apply( lambda x: f'${x:,.2f}' if pd.notna(x) else 'N/A')

    # 1. Convert Overall Stats dict -> DataFrame table 
    overall_df = pd.DataFrame([ {"Metric": "Mean Salary", "Value": f"${overall_stats['mean']:,.2f}"}, {"Metric": "Median Salary", "Value": f"${overall_stats['median']:,.2f}"}, {"Metric": "Standard Deviation", "Value": f"${overall_stats['std']:,.2f}"}, {"Metric": "Minimum Salary", "Value": f"${overall_stats['min']:,.2f}"}, {"Metric": "Maximum Salary", "Value": f"${overall_stats['max']:,.2f}"}, {"Metric": "Skewness", "Value": f"{overall_stats['skew']:.2f}"}, ])
    # 2. Convert Experience Stats dict -> DataFrame table 
    exp_df = pd.DataFrame([ {"Metric": "Correlation (r)", "Value": f"{exp_stats['corr']:.4f}"}, {"Metric": "Explanatory Power (R²)", "Value": f"{exp_stats['r_squared']:.4f}"}, {"Metric": "Annual Gain (Slope)", "Value": f"+${exp_stats['slope']:,.2f} / year"}, {"Metric": "Base Salary (Intercept)", "Value": f"${exp_stats['intercept']:,.2f}"}, ])

    ## README content
    readme_content = (f"""# Compensation & Carrer Progression Analysis

## 📊 Executive Summary
This project analyzes salary distributions across professional experience tiers and education levels using a cleaned dataset of employment records.

## 📁 Project Architecture 
```text 
large-salary-analysis/ 
├── data/ 
│   ├── clean-salary-data.csv
│   ├── cleaned-salary_data.csv
│   └── Salary_Data.csv
├── scripts/ 
│   ├── __init__.py 
│   ├── eda_visualizations.py
│   ├── main.py 
│   ├── pandas_pipeline.py
│   ├── extract_stats.py 
│   └── generate_readme.py 
├── visualizations/ 
│   ├── salary_distribution.png 
│   ├── education_vs_salary.png 
│   └── experience_vs_salary.png 
├── .gitignore 
├── README.md 
└── requirements.txt
```

## 📈 Key Statistical Findings
### Overall Salary Metrics
{overall_df.to_markdown(index = False)}

### Education Level Breakdown
{edu_display.to_markdown()}

### Experience Regression Model
{exp_df.to_markdown(index = False)}

## 🖼️ Visualizations

### 1. Overall Salary Distribution
![Salary Distribution](visualizations/salary_distribution.png)

### 2. Salary by Education Level
![Education VS Salary](visualizations/education_vs_salary.png)

### 3. Salary vs. Years of Experience
![Experience VS Salary](visualizations/experience_vs_salary.png)

## 🚀 How to Run
1. Clone the repository and install requirements:
    ```bash
    pip install -r requirements.txt
    ````
2. Generate data stats and README:
    ```bash
    python scripts/generate_readme.py
    ```
""")

    README_PATH.write_text(readme_content.strip(), encoding = 'utf-8')
    print("\n✅ README.me generated successfully!")

if __name__ == '__main__':
    generate_readme()