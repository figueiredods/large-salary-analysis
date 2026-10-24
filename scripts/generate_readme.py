# ============================================
# IMPORTS & PATHS SETUP
# ============================================
## Imports
from pathlib import Path
import pandas as pd
from extract_stats import calculate_overall_stats, calculate_education_stats, calculate_experience_stats

## Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / 'data'
README_PATH = BASE_DIR / 'README.md'

# ============================================
# DATA EXTRACTION & TRANSFORMATION
# ============================================
## Read CSV
df = pd.read_csv(DATA_PATH / 'clean-salary-data.csv')

overall_stats = calculate_overall_stats(df) # dict type
edu_stats = calculate_education_stats(df) # dt type
exp_stats = calculate_experience_stats(df) # dict type

edu_stats.to_markdown()

# ============================================
# TEMPLATE ASSEMBLY (MULTI-LINE F-STRING)
# ============================================
## Variable
readme_content = (f"""
# Title & Project Overview

## 📊 Executive Summary

## 📈 Key Statistical Findings
    ·
""")