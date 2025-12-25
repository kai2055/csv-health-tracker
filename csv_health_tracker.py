
from pathlib import Path

print("=" * 80)
print("CSV Health Tracker")
print("A python tool that checks the status of the CSV file before heading down the data workflow.")
print("Please provide the path to the 'CSV file'")
print("Example: /User/Desktop/Documents/example.csv")
print("=" * 80)


print("Please provide the file path to the specific CSV file")
user_input = input().strip()

while not user_input:
    print("The input provided is empty. Please provide the file path.")
    user_input = input("Enter file path: ").strip()

file_path = Path(user_input)




# Check 1: Does the file path exist?
if not file_path.exists():
    print(f"Error: '{file_path}' does not exist")
    exit()

# Check 2: Is it a file?
if not file_path.is_file():
    print(f"Error: '{file_path}' is a directory, not a file")
    exit()

# Check 3: Is it a csv?
if file_path.suffix.lower() != '.csv':
    print(f"Error: '{file_path}' is not a CSV file.")
    exit()


print(" File is valid. Beginning analysis")

# getting the filename
user_file = file_path.name

import pandas as pd

# reading the file with pandas
df = pd.read_csv(file_path)

print("=" * 80)
print(f"DIAGNOSIS REPORT OF {user_file}:")
print("=" * 80)


print(f"Number of Rows and Columns: {df.shape}")

print("\nColumn Names:")
column_names = df.columns.tolist()

# Check if pandas assigned default numeric column names (0, 1,2 ...)
# This happens when CSV has no header row
has_default_names = all(isinstance(col, int) for col in df.columns)

if has_default_names:
    print("WARNNING: No column headers detected (using default names: 0, 1,2,....)")
    print((f"Columns: {column_names}"))
else: print(f"Columns: {column_names}")

# Check for duplicate column names
duplicate_columns = df.columns[df.columns.duplicated()].tolist()

if duplicate_columns:
    print(f"WARNING: Duplicate column names detected: {duplicate_columns}")

# Number of duplicated rows
num_duplicated_rows = df.duplicated().sum() # Total count

print(f"Number of duplicated rows: {num_duplicated_rows}")

# The data type of the columns as inferred by pandas
print(f"Data types:\n{df.dtypes}")

# Empty columns
empty_cols = df.columns[df.isna().all()].tolist()

if empty_cols:
    print(f"WARNNING: Empty columns detected: {empty_cols} ")

# Empty rows
empty_rows = df[df.isna().all(axis=1)]
num_empty_rows = len(empty_rows)

print(f"Number of completely empty rows: {num_empty_rows}")

# Showing the basic statistics of all the columns; numeric as well as non-numeric
print("Basic Statistics: ")
print(df.describe(include='all'))

# Whitespace pollution (flag if beyond threshold)

# Check each string column for whitespace pollution

threshold = 10 # 10% threshold

for col in df.select_dtypes(include='object').columns:
    has_whitespace = df[col].apply(lambda x: isinstance(x, str) and x != x.strip())
    whitespace_count = has_whitespace.sum()
    whitespace_pct = (whitespace_count / len(df)) * 100

    if whitespace_pct > threshold: 
        print(f" Column '{col}': {whitespace_pct:.1f}% of values have whitespace")





"""
AREAS FOR IMPROVEMENT

1. ⚠️ No encoding error handling: If the file has encoding issues (non-UTF-8),
 pandas will crash with UnicodeDecodeError.

2. ⚠️ No handling for malformed CSV: If the CSV is corrupted or has inconsistent 
 columns, pandas might fail or behave unexpectedly

3. ❌ Everything is in a single linear script: No functions, no reusability

4. ❌ Lots of commented-out code: The top ~60 lines are old attempts. This clutters the file.

5. ❌ Hard to test: Can't test individual checks without running the entire script

6. ❌ Hard to extend: Adding new checks requires inserting code in the middle of the script

7. ❌ Missing exception handling: No try/except around pd.read_csv()

8. ⚠️ No if __name__ == "__main__": block: Not critical for a script, but good practice

9. ⚠️ Data types output is raw pandas: df.dtypes prints as a Series, which can be hard to read for large files
   ⚠️ df.describe() can be overwhelming: For files with 50+ columns, this becomes unreadable
   ⚠️ Missing summary at the end: No final "✓ File passed all checks" or "⚠ Found 3 issues"

"""













