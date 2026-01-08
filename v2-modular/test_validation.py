

"""
Test script for validation module

Tests CSV validation logic with sample data

"""


import pandas as pd
from pathlib import Path


from config import load_config
from logger import get_logger_from_config
from validation import CSVValidator, validate_csv
from exceptions import (
    CSVNotFoundError,
    CSVReadError,
    InvalidCSVFormatError,
    DuplicateRowsExceededError,
    MissingValuesExceededError,
    WhiteSpacePollutionError
)


def create_test_csv_good():
    """Create a clean test CSV file"""
    data = {
        'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04'],
        'metric': ['temperature', 'humidity', 'pressure', 'temperature'],
        'value': [22.5, 65.0, 1013.25, 23.0],
        'notes': ['clear', 'cloudy', 'sunny', 'clear']
    }

    df = pd.DataFrame(data)
    df.to_csv('test_data_good.csv', index=False)
    print("Created test_data_good.csv")



def create_test_csv_duplicates():
    """Create a CSV with duplicate rows"""
    data = {
        'date': ['2024-01-01', '2024-01-02', '2024-01-01', '2024-01-01'],  # duplicates
        'metric': ['temperature', 'humidity', 'temperature', 'temperature'],
        'value': [22.5, 65.0, 22.5, 22.5],
        'notes': ['clear', 'cloudy', 'clear', 'clear']
    }
    df = pd.DataFrame(data)
    df.to_csv('test_data_duplicates.csv', index=False)
    print("Create test_data_duplicates.csv (50% duplicates)")



def create_test_csv_missing():
    """Create a CSV with missing values"""
    data = {
        'data': ['2024-01-01', '2024-01-02', None, None],  # 50% missing 
        'metric': ['temperature', None, 'pressure', None],
        'value': [22.5, 65.0, 1013.25, None],
        'notes': ['clear', 'cloudy', 'sunny', None]
    }
    df = pd.DataFrame(data)
    df.to_csv('test_data_missing.csv', index=False)
    print("Created test_data_missing.csv (high missing values)")



def create_test_csv_whitespace():
    """Create a CSV with whitespace pollution"""
    data = {
        'date': ['2024-0101', ' 2024-01-02', '2024-01-03 ', '   2024-01-04  '],  # Whitespace
        'metric': ['temperature', 'humidity  ', '  pressure',  'temperature'],
        'value': [22.5, 65.0, 1013.25, 23.0],
        'notes': ['clear', 'cloudy', 'suny', 'clear'] 
    }
    df = pd.DataFrame(data)
    df.to_csv('test_data_whitespace.csv', index=False)
    print("Created test_data_whitespace.csv, (whitespace pollution)")



def test_file_path_validation():
    """Test file path validation"""
    print("\n" + "=" * 80)
    print("TEST 1: File Path Validation")
    print("=" * 80)


    config = load_config()
    logger = get_logger_from_config(config)
    validator = CSVValidator(logger, config)

    # Test 1a: Non-existent file
    print("\nTest 1a: Non-existent file")
    try:
        validator.validate_file_path('nonexistent.csv')
        print("Should have raised CSVNotFoundError")
    except CSVNotFoundError as e:
        print(f"Correctly raised CSVNotFoundError: {e}")

    # Test 1b: Not a CSV file
    print("\nTest 1b: Not a CSV file (testing with config.yaml)")
    try:
        validator.validate_file_path('config.yaml')
        print("Should have raised InvalidCSVFormatError")
    except InvalidCSVFormatError as e:
        print(f"Correctly raised InvalidCSVFormatError: {e}")


    # Test 1c: Valid CSV file
    print("\nTest 1c: Valid CSV file")
    create_test_csv_good()
    try:
        path = validator.validate_file_path('test_data_good.csv')
        print(f"Valid file path accepted: {path}")
    except Exception as e:
        print(f"Unexpected error: {e}")



def test_good_csv():
    """Test with a clean CSV"""
    print("\n" + "=" * 80)
    print("TEST 2: Clean CSV (Should Pass ALL Checks)")
    print("=" * 80)


    config = load_config()
    logger = get_logger_from_config(config)

    create_test_csv_good()


    try:
        results = validate_csv('test_data_good.csv', logger, config)
        print("\nALL VALIDATION CHECKS PASSED")
        print(f"- Shape: {results['basic_info']['shape']}")
        print(f"- Columns: {results['basic_info']['columns']}")
        print(f"- Duplicates: {results['duplicates']['percentage']:.2f}%")
    except Exception as e:
        print(f"Unexpected error: {e}")



def test_csv_with_duplicates():
    """Test CSV with excessive duplicates"""
    print("\n" + "=" * 80)
    print("TEST 3: CSV with Excessive Duplicates (Should Fail")
    print("=" * 80)

    config = load_config()
    logger = get_logger_from_config(config)
    

    create_test_csv_duplicates()

    try:
        results = validate_csv('test_data_duplicates.csv', logger, config)
        print("Should have raised DuplicateRowsExceededError")
    except DuplicateRowsExceededError as e:
        print(f"Correctly raised DuplicateRowsExceededError")
        print(f"Error: {e}")



def test_csv_with_missing_values():
    """Test CSV with excessive missing values"""
    print("\n" + "=" * 80)
    print("TEST 4: CSV with Excessive Missing Values (Should Fail)")
    print("=" * 80)

    config = load_config()
    logger = get_logger_from_config(config)

    create_test_csv_missing()

    try:
        results = validate_csv('test_data_missing.csv', logger, config)
        print("Should have raised MissingValuesExceededError")
    except MissingValuesExceededError as e:
        print(f"Correctly raised MissingValuesExceededError")
        print(f"Error: {e}")



def test_csv_with_whitespace():
    """Test CSV with whitespace pollution"""
    print("\n" + "=" * 80)
    print("TEST 5: CSV with Whitespace Pollution (Should Fail)")
    print("=" * 80)

    config = load_config()
    logger = get_logger_from_config(config)

    create_test_csv_whitespace()

    try:
        results = validate_csv('test_data_whitespace.csv', logger, config)
        print("Should have raised WhitespacePollutionError")
    except WhiteSpacePollutionError as e:
        print(f"Correctly raised WhitespacePollutionError")
        print(f"Error: {e}")





def cleanup_test_files():
    """Remove test CSV files"""
    test_files = [
        'test_data_good.csv',
        'test_data_duplicates.csv',
        'test_data_missing.csv',
        'test_data_whitespace.csv'
    ]

    for file in test_files:
        path = Path(file)
        if path.exists():
            path.unlink()

    print("\nCleanned up test files")



if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("CSV VALIDATION MODULE TESTING")
    print("=" * 80)

    try:
        test_file_path_validation()
        test_good_csv()
        test_csv_with_duplicates()
        test_csv_with_missing_values()
        test_csv_with_whitespace()


        print("\n" + "=" * 80)
        print("ALL TESTS COMPLETE")
        print("=" * 80)



    finally: 
        cleanup_test_files()


