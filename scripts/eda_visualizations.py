# ============================================
# IMPORTS & PATH SETUP
# ============================================
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / 'data'
OUTPUT_DIR = BASE_DIR / 'visualizations'

OUTPUT_DIR.mkdir(parents = True, exist_ok = True)

# ============================================
# CONSTANTS & CATEGORY ORDER
# ============================================
EDUCATION_ORDER = ["High School", "Bachelor's", "Master's", "PhD"]
GENDER_ORDER = ['Female', 'Male', 'Other']

# ============================================
# LOAD & AUDIT
# ============================================
def load_and_audit(data_path: Path | str) -> pd.DataFrame:
    df_clean = pd.read_csv(data_path)
    df_clean.info()

    print("\n--- Education Level Categories ---")
    print(df_clean['Education Level'].value_counts())
    print("\n--- Gender Categories ---")
    print(df_clean['Gender'].value_counts())
    return df_clean

# ============================================
# PLOTS & CHARTS
# ============================================
def plot_salary_distribution(data: pd.DataFrame) -> None:
    mean_val, median_val = data['Salary'].agg(['mean', 'median'])

    plt.figure(figsize = (10, 6))
    sns.histplot(data['Salary'], kde = True)

    plt.axvline(mean_val, color = 'red', linestyle = '--', label = f'Mean: ${mean_val:,.2f}')
    plt.axvline(median_val, color = 'green', linestyle = '-', label = f'Median: ${median_val:,.2f}')
    plt.title("Salary Distribution & Central Tendency")
    plt.xlabel("Annual Salary ($USD)")
    plt.ylabel("Employee Frequency")
    plt.legend()
    plt.grid(axis = 'y', linestyle = '-.', alpha = 0.5)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'salary_distribution.png', dpi = 300)
    plt.close()

def plot_education_vs_salary(data: pd.DataFrame) -> None:
    plt.figure(figsize = (10,6))
    sns.boxplot(data = data, x = 'Education Level', y = 'Salary', order = EDUCATION_ORDER, palette = 'Blues_r', hue = 'Education Level', legend = False)

    plt.title("Compensation Progression by Academic Credentials")
    plt.xlabel("Education Level")
    plt.ylabel("Annual Salary ($USD)")
    plt.grid(axis = 'y', linestyle = '-.', alpha = 0.5)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'education_vs_salary.png', dpi = 300)
    plt.close()

def plot_experience_vs_salary(data: pd.DataFrame) -> None:
    plt.figure(figsize = (10,6))
    sns.regplot(data = data, x = 'Years of Experience', y = 'Salary', scatter_kws = {'alpha': 0.3}, line_kws = {'color': 'red', 'alpha': 0.5})

    plt.title("Compensation Progression over Years of Experience")
    plt.xlabel("Years of Experience")
    plt.ylabel("Annual Salary ($USD)")
    plt.grid(linestyle = '-.', alpha = 0.5)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'experience_vs_salary.png', dpi = 300)
    plt.close()

def main():
    df_clean = load_and_audit(DATA_PATH / 'clean-salary-data.csv')
    plot_salary_distribution(df_clean)
    plot_education_vs_salary(df_clean)
    plot_experience_vs_salary(df_clean)

# ============================================
# MAIN EXECUTION
# ============================================
if __name__ == '__main__':
    main()