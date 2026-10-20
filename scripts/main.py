# imports
import sys
from pathlib import Path
from csv import DictReader
from collections import defaultdict

sys.path.append(str(Path(__file__).resolve().parent.parent))

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / 'data'

# CONSTANTS
EDUCATION_MAP = {
    "": "NR", # Maps empty strings to 'NR' (Not Reported)
    "bachelor's": "Bachelor's",
    "bachelor's degree": "Bachelor's",
    "master's": "Master's",
    "master's degree": "Master's",
    "phd": "PhD",
    "high school": "High School"
}

# Funcions
def clean_row(row: dict) -> dict | None:
    """
    Cleans and standardizes a single raw row dictionary from Salary_Data.csv.
    Casts numeric fields to float/int, normalizes education levels, and handles missing data safely.
    Returns the cleaned dictionary, or None if the record is invalid.
    """
    try:
        raw_edu = row['Education Level'].strip().lower()
        # Fallback to the original stripped string if not in the map
        standardized_edu = EDUCATION_MAP.get(raw_edu, row['Education Level'].strip())

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

def calculate_mean_salary(data: list[dict]) -> float:
    # Calculates the average salary across all valid employee records.
    try:
        totals = sum(row['Salary'] for row in data)
        count = len(data)
        return round(float(totals / count), 2)
    except (ZeroDivisionError, TypeError):
        return 0

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

def audit_text_column(data: list[dict], column_name: str) -> dict[str, int]:
    unique_name = defaultdict(int)
    for row in data:
        category = row[column_name]
        unique_name[category] += 1
    # Sort by frequency descending
    raw_keys = set(unique_name.keys())
    normalized_keys = {k.strip().lower() for k in raw_keys}
    
    if len(raw_keys) != len(normalized_keys):
        print(f"\n⚠️ Warning: Found {len(raw_keys) - len(normalized_keys)} casing/whitespace variants in '{column_name}'⚠️\n")

    return dict(sorted(unique_name.items(), key = lambda item: item[1], reverse = True))

# Read file and clean
with open(DATA_PATH /'Salary_Data.csv', encoding = 'utf-8-sig') as df:
    reader = DictReader(df)
    dirt_data = []
    cleaned_data = []
    raw_data = []
    count = 0
    for row in reader:
        count += 1
        raw_data.append(row)
        current_row = clean_row(row)
        if current_row is not None:
            cleaned_data.append(current_row)
        else:
            dirt_data.append(row)

print(f"\nRaw Records: {count}")
print(f"Cleaned Records: {len(cleaned_data)}")
print(f"Dirt Records: {len(dirt_data)}")
print(f"\nThe first row is :\n{cleaned_data[0]}\n")
# print("\n--- Dirty Records Audit Log ---")
# for index, record in enumerate(dirt_data, start = 1):
#     print(f"Record #{index}: {record}\n")

mean_salary = calculate_mean_salary(cleaned_data)
print(f"\nThe average salary is: $ {mean_salary:,.2f} \n")

mean_by_category = calculate_salary_by_dimension(cleaned_data, 'Education Level')
for key, value in mean_by_category.items():
    print(f"\n{key}: $ {value:,.2f}")