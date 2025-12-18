
"""
CSV Health Checker +  Log Analyzer

A python tool that inspects CSV files for data quality issues (missing value, wrong data types, outliers)
and analyzes log files to detect errors, warnings and anomalies. It provides clear summaries and reports,
helping you quickly understand your data and system bahevior.

"""



# First part of the project - Take the file path and the filename from the user and then see if the file exist
#  or if the path has been given in the correct format to raise exception
# FileNotFoundError, Empty input, right type file and is it a file itself

"""

print("Welcome to CSV Health Checker. Please provide your specific csv filename along with the correct path.")
print("This python tool provides a pre-checking and validation of the apecific file before it can be further passed down in the piplrline for processing or discarded.")
csv_file_path = input()

"""


print("CSV Health Checker")
print("--------------------")
print("Provide the path to the CSV file you want to validate.")
print("Example: C:/Users/YourName/Desktop/data.csv")
print()


csv_file_path = input("Enter csv file path: ")

if not csv_file_path:
    print("The filename is empty. Please enter the csv file name.")



