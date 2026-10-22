# ============================================
# IMPORTS & PATH CONFIGURATION
# ============================================
from pathlib import Path
from csv import DictReader, DictWriter
from collections import defaultdict

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / 'data'

# ============================================
# CONSTANTS & LOOKUP MAPPINGS
# ============================================
EDUCATION_MAP = {
    "high school": "High School",
    "bachelor's": "Bachelor's",
    "bachelor's degree": "Bachelor's",
    "master's": "Master's",
    "master's degree": "Master's",
    "phd": "PhD",
    "": "NR" # Maps empty strings to 'NR' (Not Reported)
}
# Custom display orders for report formatting
EDUCATION_ORDEM = ["High School", "Bachelor's", "Master's", "PhD", "NR"]
GENDER_ORDER = ['Female', 'Male', 'Other']

# ============================================
# DATA AUDITING & CLEANING FUNCTIONS
# ============================================
def find_anomalous_salaries(data: list[dict], threshold: float = 10000.0) -> list[dict]:
    """
    Audits a 'Salary' column searching for anomalous values (Anual Salary < 10,000)
    """
    anomalous_salaries = []
    for row in data:
        if row['Salary'] < threshold:
            anomalous_salaries.append(row)
    return anomalous_salaries

def audit_text_column(data: list[dict], column_name: str) -> dict[str, int]:
    """ 
    Audits a text column for unique values and frequencies, flagging casing or whitespace variants if present.
    """
    unique_name = defaultdict(int)
    for row in data:
        category = row[column_name]
        unique_name[category] += 1
    #
    raw_keys = set(unique_name.keys())
    normalized_keys = {k.strip().lower() for k in raw_keys}
    
    if len(raw_keys) != len(normalized_keys):
        print(f"\n⚠️ Warning: Found {len(raw_keys) - len(normalized_keys)} casing/whitespace variants in '{column_name}'⚠️\n")

    return dict(sorted(unique_name.items(), key = lambda item: item[1], reverse = True))

def clean_row(row: dict) -> dict | None:
    """
    Cleans and standardizes a single raw row dictionary from Salary_Data.csv.
    Casts numeric fields to float/int, normalizes education levels, and handles missing data safely.
    Returns the cleaned dictionary, or None if the record is invalid.
    """
    try:
        raw_edu = row['Education Level'].strip().lower()
        standardized_edu = EDUCATION_MAP.get(raw_edu, row['Education Level'].strip())
        if float(row['Salary']) < 10000.0:
            return None
        cleaned = {
            'Age': int(float(row['Age'])),
            'Gender': row['Gender'].strip().title(),
            'Education Level': standardized_edu,
            'Job Title': row['Job Title'].strip().title(),
            'Years of Experience': float(row['Years of Experience']),
            'Salary': float(row['Salary'])
        }
        return cleaned
    except (ValueError, KeyError, TypeError):
        # Catches missing values, empty strings or bad numeric casts
        return None

def export_clean_data(cleaned_data: list[dict], filepath: Path | str) -> None:
    """
    Exports the validated list of cleaned row dictionaries to a CSV file.
    """
    if not cleaned_data:
        print("\n ⚠️ Warning: No cleaned data available to export.")
        return # Prevents IndexError on cleaned_data[0]

    fieldname = list(cleaned_data[0].keys())

    with open(filepath, mode = 'w', encoding = 'utf-8-sig', newline = '') as f:
        writer = DictWriter(f, fieldnames = fieldname)
        writer.writeheader()
        writer.writerows(cleaned_data)
    print(f"\n ✅ Successfully exported {len(cleaned_data):,} records to '{filepath}'\n")

# ============================================
# CORE ANALYTICS FUNCTIONS
# ============================================
def calculate_mean_salary(data: list[dict]) -> float:
    """Calculates the average salary across all valid employee records."""
    try:
        totals = sum(row['Salary'] for row in data)
        count = len(data)
        return round(float(totals / count), 2)
    except (ZeroDivisionError, TypeError):
        return 0.0

def calculate_salary_by_dimension(data: list[dict], dimension_key: str) -> dict[str, float]:
    """
    Calculates average salary grouped by a category (e.g., 'Education Level' or 'Gender').
    Returns a dictionary mapping each category name to irs rounded average salary.
    """
    totals = defaultdict(float)
    counts = defaultdict(int)
    for row in data:
        category = row[dimension_key]
        salary = row['Salary']
        totals[category] += salary
        counts[category] += 1

    averages = {
        category: round(totals[category] / counts[category], 2) 
        for category in totals
    }
    return averages

def find_salary_extrema(data: list[dict]) -> tuple[dict, dict]:
    """
    Finds and returns the highest-paid and lowest-paid employee records.
    Returns a tuple of (highest_paid_dict, lowest_paid_dict).
    """
    highest = max(data, key = lambda row: row['Salary'])
    lowest = min(data, key = lambda row: row['Salary'])
    return highest, lowest

# ============================================
# EXECUTIVE REPORTING FUNCTION
# ============================================
def generate_executive_summary(cleaned_data: list[dict], dirt_data: list[dict]):
    """
    Prints a formatted Executive Compensation Summary Report incorporating pipeline health, demographic benchmarks, and compensation extrema.
    """
    total_records = len(cleaned_data) + len(dirt_data)
    mean_overall = calculate_mean_salary(cleaned_data)

    print("")
    print("=" * 68)
    print("             EXECUTIVE COMPENSATION SUMMARY REPORT               ")
    print("=" * 68)

    # 1. Pipeline Health
    print("\n[ DATA PIPELINE HEALTH ]")
    print(f"    · Total Processed Records   :   {total_records:,}")
    print(f"    · Validated Clean Records   :   {len(cleaned_data):,} ({len(cleaned_data) / total_records:.1%})")
    print(f"    · Quarantined (Dirt) Rows   :   {len(dirt_data):,} ({len(dirt_data) / total_records:.1%})")
    print(f"    · Portefolio Mean Salary    :   ${mean_overall:>11,.2f}")

    # 2. Education Benchmarks
    print("\n[ COMPENSATION BY EDUCATION LEVEL ]")
    edu_means = calculate_salary_by_dimension(cleaned_data, 'Education Level')
    sorted_edu = sorted(edu_means.items(), key = lambda item: EDUCATION_ORDEM.index(item[0]) if item[0] in EDUCATION_ORDEM else 999)
    for edu, val in sorted_edu:
        print(f"    · {edu:<21}     :   ${val:>11,.2f}")

    # 3. Gender Demographic Benchmarks
    print("\n[ COMPENSATION BY GENDER ]")
    gender_means = calculate_salary_by_dimension(cleaned_data, 'Gender')
    sorted_gender = sorted(gender_means.items(), key = lambda item: GENDER_ORDER.index(item[0]) if item[0] in GENDER_ORDER else 999)
    for gender, val in sorted_gender:
        count = sum(1 for row in cleaned_data if row['Gender'] == gender)
        print(f"    · {gender:<10} (n = {count:>5,})    :   ${val:>11,.2f}")

    # 4. Entry-Level Role Benchmarks (< 2 Years Experience)
    print("\n[ ENTRY-LEVEL BENCHMARKS (< 2 YRS EXP) ]")
    junior_data = [row for row in cleaned_data if row['Years of Experience'] < 2]
    junior_means = calculate_salary_by_dimension(junior_data, 'Job Title')
    target_roles = ['Software Engineer', 'Data Scientist', 'Data Analyst']
    for role in target_roles:
        if role in junior_means:
            print(f"    · {role:<22}    :   ${junior_means[role]:>11,.2f}")

    # 5. Compensaition Extrema
    print("\n[ SALARY EXTREMA HIGHLIGHTS ]")
    top_emp, bot_emp = find_salary_extrema(cleaned_data)
    print(f"    · Top Earner    :   {top_emp['Job Title']} (${top_emp['Salary']:,.2f} | {top_emp['Years of Experience']} yrs exp | {top_emp['Education Level']})")
    print(f"    · Entry Floor   :   {bot_emp['Job Title']} (${bot_emp['Salary']:,.2f} | {bot_emp['Years of Experience']} yrs exp | {bot_emp['Education Level']})")
    print("=" * 68, "\n")

# ============================================
# MAIN EXECUTION PIPELINE
# ============================================
SHOW_AUDITS = False # Set to True whenever you want quick column inspections

if __name__ == '__main__':
    # 1. Ingest and Sanitize Raw CSV Data
    with open(DATA_PATH / 'Salary_Data.csv', encoding = 'utf-8-sig') as df:
        reader = DictReader(df)
        raw_data = []
        cleaned_data = []
        dirt_data = []

        for row in reader:
            raw_data.append(row)
            current_row = clean_row(row)
            if current_row is not None:
                cleaned_data.append(current_row)
            else:
                dirt_data.append(row)

    # 2. Optional Debug Audits
    if SHOW_AUDITS:
        job_audit = audit_text_column(raw_data, 'Job Title')
        print(f"\nTop 5 Job Titles out of {len(job_audit)} unique titles:")
        for title, qty in list(job_audit.items())[0:5]:
            print(f" - {title}: {qty} employees")
    
    # 3. Generate Final Execution Summary Report
    generate_executive_summary(cleaned_data, dirt_data)

    # 4. Export sanitized records to a new CSV file
    export_clean_data(cleaned_data, DATA_PATH / 'cleaned-salary-data.csv')