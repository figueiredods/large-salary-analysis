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
# LOAD & AUDIT
# ============================================
df_clean = pd.read_csv(DATA_PATH / 'clean-salary-data.csv')
df_clean.info()

# ============================================
# PLOTS
# ============================================
mean_val, median_val = df_clean['Salary'].agg(['mean', 'median'])

plt.figure(figsize = (10, 6))
sns.histplot(df_clean['Salary'], kde = True)

plt.axvline(mean_val, color = 'red', linestyle = '--', label = f'Mean: ${mean_val:,.2f}')
plt.axvline(median_val, color = 'green', linestyle = '-', label = f'Median: ${median_val:,.2f}')
plt.title("Salary Distribution & Central Tendency")
plt.xlabel("Annual Salary ($USD)")
plt.ylabel("Employee Frequency")
plt.legend()
plt.savefig(OUTPUT_DIR / 'salary_distribution.png', dpi = 300)
plt.close()