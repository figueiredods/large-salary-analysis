# ============================================
# IMPORTS, PATHS & CONSTANTS
# ============================================
import pandas as pd
from pathlib import Path
from scipy import stats

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / 'data'

# Constant
EDUCATION_ORDER = ["High School", "Bachelor's", "Master's", "PhD", "NR"]

# ============================================
# STATS FUNCTION
# ============================================
def calculate_overall_stats(df: pd.DataFrame) -> dict[str, float]:
    # 1. Calculate stats on df['Salary']
    # mean_val, median_val, std_val, min_val, max_val, skew_val = 
    return df['Salary'].agg(['mean', 'median', 'std', 'min', 'max', 'skew']).to_dict()

def calculate_education_stats(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Calculate stats on df['Education Level']
    edu_stats = df.groupby('Education Level')['Salary'].agg(['count', 'mean', 'median', 'std']).reindex(EDUCATION_ORDER)
    
    return edu_stats

def calculate_experience_stats(df: pd.DataFrame) -> dict[str, float]:
    # 1. Pearson Correlation (r)
    corr = df['Years of Experience'].corr(df['Salary'])

    # 2. Linear Regression (Slope, Intercept, R-value)
    res = stats.linregress(df['Years of Experience'], df['Salary'])
    r_squared = res.rvalue**2

    # Pack all in a dictionary
    experience_stats = {'corr': corr, 'r_squared': r_squared, 'slope': res.slope, 'intercept': res.intercept}

    return experience_stats   

def main():
    df = pd.read_csv(DATA_PATH / 'clean-salary-data.csv')

    overall_stats = calculate_overall_stats(df)
    print("\n=== OVERALL SALARY STATS ===")
    print(f"Mean: ${overall_stats['mean']:,.2f}")
    print(f"Median: ${overall_stats['median']:,.2f}")
    print(f"Standard Deviation: ${overall_stats['std']:,.2f}")
    print(f"Min & Max: ${overall_stats['min']:,.2f} | ${overall_stats['max']:,.2f}")
    print(f"Skewness: {overall_stats['skew']:.2f}")
    
    education_stats = calculate_education_stats(df)
    print("\n=== SALARY STATS BY EDUCATION LEVEL ===")
    print(education_stats)

    experience_stats = calculate_experience_stats(df)
    print("\n=== EXPERIENCE VS SALARY STATS ===")
    print(f"Correlation (r): {experience_stats['corr']:.4f}")
    print(f"Explanatory Power (R²): {experience_stats['r_squared']:.4f}")
    print(f"Annual Gain (Slope): +${experience_stats['slope']:,.2f} per year")
    print(f"Base Salary (Intercept): ${experience_stats['intercept']:,.2f}")   

# ============================================
# MAIN EXECUTION
# ============================================
if __name__ == '__main__':
    main()