# 📊 Pure Python Salary Data Analysis & Processing Pipeline (Data Science Focus)

An end-to-end, production-grade Data Engineering pipeline built purely in Python (no external dependencies) to ingest, sanitize, audit, analyze, and export employee compensation records.

## 🚀 Key Features & Pipeline Architecture

* **Robust Data Ingestion & Sanitization (`clean_row`)**:
  * Safe type casting (`Age` -> `int`, `Salary`/`Experience` -> `float`).
  * Degree level standardization using lookup mappings (`EDUCATION_MAP`).
  * Automatic text normalization (`.strip().title()`).
  * **Scale Anomaly Guard Clause**: Quarantines entries with `Salary < $10,000` (e.g., scale typos like `$350`) directly into a Dead-Letter Queue (`dirt_data`).
* **Categorical Quality Auditing (`audit_text_column`)**: Dynamic frequency distribution auditing and whitespace/casing variant detection.
* **Core Analytics Functions**: Decoupled, reusable functions for overall means (`calculate_mean_salary`), categorical aggregations (`calculate_salary_by_dimension`), and extrema detection (`find_salary_extrema`).
* **Executive Terminal Reporting (`generate_executive_summary`)**: Decoupled reporting module featuring custom degree progression ordering (`EDUCATION_ORDER`) and demographic sorting (`GENDER_ORDER`).
* **Clean CSV Export (`export_clean_data`)**: Exports sanitized records safely to `data/cleaned_salary_data.csv`.

## 📈 Pipeline Health & Benchmark Results

* **Total Records Processed**: 6,704
* **Validated Clean Records**: 6,695 (99.9%)
* **Quarantined (Dirt) Rows**: 9 (0.1% — 5 missing values + 4 scale typos)
* **Portfolio Mean Salary**: \$115,326.96

### Executive Compensation Highlights

| Category | Ordering | Average Salary |
| :--- | :--- | :--- |
| **Education** | High School -> Bachelor's -> Master's -> PhD | \$36,706.69 -> \$95,082.91 -> \$130,112.06 -> \$165,651.46 |
| **Gender** | Female / Male / Other | \$107,889.00 (n=3,013) / \$121,389.87 (n=3,672) / \$125,869.86 (n=14) |
| **Junior Roles (< 2 Yrs Exp)** | Data Scientist / Data Analyst / Software Engineer | \$115,000.00 / \$99,714.29 / \$56,213.33 |

## 🛠️ Project Structure

```text
large-salary-analysis/
├── data/
│   ├── Salary_Data.csv           # Raw dataset
│   └── cleaned_salary_data.csv   # Sanitized export
├── scripts/
│   ├── __init__.py  
│   └── main.py                   # Primary ETL pipeline
└── README.md                     # Documentation
```

## 💻 How to Run

```bash
python scripts/main.py
```