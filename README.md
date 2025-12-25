# CSV Health Checker

A robust Python diagnostic tool designed to perform pre-pipeline validation on CSV files. This tool inspects data for quality issues and structural inconsistencies, providing a comprehensive "Diagnosis Report" **without modifying the source data**.

---

## 🚀 Key Features

- **Path Validation**: Ensures the file exists, is accessible, and has a valid `.csv` extension
- **Structural Integrity**: Checks for missing headers, duplicate column names, and reports total rows/columns
- **Data Quality**: Detects duplicate rows and completely empty rows or columns
- **Missing Value Analysis**: Reports the count of missing values per column
- **Statistical Overview**: Generates basic descriptive statistics for numeric and non-numeric columns
- **Cleanliness Check**: Flags "whitespace pollution" (leading/trailing spaces) in string columns when >10% of values are affected

---

## 🛠️ Requirements

- Python 3.x
- `pandas` library

**Installation:**
```bash
pip install pandas
```

---

## 📖 Usage

1. Clone the repository:
```bash
   git clone https://github.com/kai2055/csv-health-tracker.git
   cd csv-health-tracker
```

2. Run the script:
```bash
   python csv_health_tracker.py
```

3. Enter the full path to your CSV file when prompted:
```
   Example: C:/Users/Data/file.csv
```

---

## 📊 Sample Output

The tool generates a detailed diagnostic report including:

- **File Metadata**: Number of rows and columns
- **Column Information**: Column names and inferred data types
- **Data Quality Warnings**:
  - Missing or duplicate headers
  - Empty rows/columns
  - Duplicate rows
  - Whitespace pollution per column
- **Statistical Summary**: Descriptive statistics (mean, std, min, max, quartiles) for all columns



## 🎯 Design Philosophy

This tool follows a **"report, don't repair"** approach:
- **Non-destructive**: Original data remains untouched
- **Transparent**: All issues are clearly flagged with warnings
- **Informative**: Provides actionable insights for data cleaning decisions

---

## 🔄 Project Status

**Version 1:** ✅ Complete
- Single-script implementation
- Cross-platform path handling with `pathlib`
- Pandas-based analysis
- Guard clause validation pattern

**Version 2:** 🚧 Planned
- Modular architecture with functions
- Custom exception handling
- Configurable thresholds
- Command-line argument support
- Unit tests

---

## 📚 What I Learned

### Technical Skills
- Migrating from `os.path` to `pathlib` for modern path handling
- Defensive programming patterns (guard clauses, fail-fast validation)
- Pandas data inspection methods (`.describe()`, `.isna()`, `.duplicated()`)
- Input validation and user-friendly error messaging

### Design Decisions
- **Why validation over manipulation**: Health checkers should inform, not transform
- **Exact vs. fuzzy matching**: When to use case-sensitive duplicate detection
- **Threshold-based reporting**: Balancing noise vs. signal in whitespace detection (10% threshold)

---

## 🤝 Contributing

This is a learning project, but feedback and suggestions are welcome! 

---


