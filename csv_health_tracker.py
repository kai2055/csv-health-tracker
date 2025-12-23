
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
print("This tool provides you with the comprehensive summary of the csv file file before it goes further down the pipeline.")
print("Provide the path to the CSV file you want to validate.")
print("Example: C:/Users/YourName/Desktop/data.csv")
print()



"""
csv_file_path = input("Enter csv file path: ")

if not csv_file_path:
    print("The filename is empty. Please enter the csv file name.")

 """

"""
import os # needed for validating the file path and file exceptions 

# Before we ask for the filepath to the user we need to provide them with the current directory that we are in 
# since we want relative path to locate the file that the user is giving

current_directory = os.getcwd()
print(f"This is our current directory - {current_directory} . Please provide the path to you file while considering the current directory ")

user_file_path = input()

# After taking the file path we want to make sure that the file exists
# Here we will be specifically checking if the path provided leads to file or not


print(f"\n Checking if '{user_file_path}' exists...")

# Checking if the user provided us with empty input

if not user_file_path:
    print("The given input is empty. Please enter the file path to the CSV file.")

if os.path.exists(user_file_path):
    print(f"The given file exists. Now we will begin further processing.")
else:
    print(f" The given file doesnot exist. Please make sure that you gave the correct file path")


# Till now what we have basically done is checck whther the input is empty 
# as well as whether the given path leads to file or not
# now we need to make sure that the file is csv 


# using pandas to do operations on the file

import pandas as pd



"""

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


"""
print(f"Checking if the provided file_path exists.{file_path}")
if file_path.exists():
    print("The file path exists")

    print("Checking is the file path leads to a file.")
    if file_path.is_file():
        print("The given filepath leads to the file")
        if file_path.suffix.lower() == '.csv':
            print("The given filepath leads to a csv file. Now we will check the status of the file")
    else:
        print("The given filepath doesnot lead to a file. Please provide a file path that leads to a file.")
"""

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



