CSV Health Checker
A robust Python diagnostic tool designed to perform pre-pipeline validation on CSV files. This tool inspects data for quality issues and structural inconsistencies, providing a comprehensive "Diagnosis Report" without modifying the source data.

🚀 Key Features
Path Validation: Ensures the file exists and is a valid .csv format.

Structural Integrity: Checks for missing headers, duplicate column names, and identifies total rows/columns.

Data Quality: Detects duplicate rows and completely empty rows or columns.

Statistical Overview: Generates basic descriptive statistics for all data types.

Cleanliness Check: Flags "whitespace pollution" (leading/trailing spaces) in string columns based on a 10% threshold.

🛠️ Requirements
Python 3.x

Pandas library

📖 Usage
Clone the repository.

Run the script: python csv_health_tracker.py.

Enter the full path to your CSV file when prompted (e.g., C:/Users/Data/file.csv).

📊 Sample Output
The tool generates a detailed report including:

Count of Rows and Columns

Inferred Data Types

Warnings for missing headers or empty data

Detailed whitespace analysis
