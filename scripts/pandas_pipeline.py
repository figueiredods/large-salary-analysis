# ============================================
# IMPORTS & PATH CONFIGURATION
# ============================================
from pathlib import Path
import pandas as pd

## sys.path.append(str(Path(__file__).resolve().parent.parent))

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / 'data'

# ============================================
# LOAD & AUDIT DATA
# ============================================
def load_and_audit_data(csv_path: Path) -> pd.DataFrame:
    """
    Loads raw CSV data and prints baseline statistical summaries.
    """
    df = pd.read_csv(csv_path)
    print("\n=== Raw DataSet Info ===")
    print(df.info())
    print("\n=== Statistical Summary ===")
    print(df.describe())
    return df

def clean_salary_data(df: pd.DataFrame, text_cols: list[str], threshold: float = 10000.0) -> pd.DataFrame:
    """
    Sanitizes raw DataFrame using vectorized pandas operations.
    """
    # Filter anomalies & drop missing values
    df_clean = df[df['Salary'] >= threshold].dropna().copy()

    # Normalize string columns
    for col in text_cols:
        df_clean[col] = df_clean[col].str.strip().str.title()

    print("\n=== Clean DataSet Info ===")
    print(df_clean.info())
    print("\n=== Statistical Summary ===")
    print(df_clean.describe())
    return df_clean

def export_data(df: pd.DataFrame, output_path: Path) -> None:
    """
    Exports sanitized DataFrame to CSV without index column.
    """
    df.to_csv(output_path, index = False)
    print(f"\n✅ Successfully exported {len(df):,} clean records to '{output_path}'.\n")

def main():
    raw_csv = DATA_PATH / 'Salary_Data.csv'
    clean_csv = DATA_PATH / 'clean-salary-data.csv'
    text_cols = ['Gender', 'Education Level', 'Job Title']

    raw_df = load_and_audit_data(raw_csv)
    clean_df = clean_salary_data(raw_df, text_cols)
    export_data(clean_df, clean_csv)

# ============================================
# MAIN EXECUTION PIPELINE
# ============================================
if __name__ == '__main__':
    main()