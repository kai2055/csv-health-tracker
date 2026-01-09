"""
CSV Health Tracker - Main Entry Point

Command-line interface for the CSV Health Tracker.
This is what users run to validate their CSV files.

Usage:
    python main.py <path_to_csv_file>

Example:
    python main.py data/health_metrics.csv

This module orchestrates:
    1. Load configuration
    2. Set up logging
    3. Validate CSV file
    4. Generate health report
    5. Display results


"""

import sys
from pathlib import Path

from config import load_config, ConfigurationError
from logger import get_logger_from_config
from validation import validate_csv
from report import generate_health_report
from exceptions import(
        CSVHealthTrackerError,
        CSVNotFoundError,
        InvalidCSVFormatError,
        DuplicateRowsExceededError,
        MissingValuesExceededError,
        WhiteSpacePollutionError,
        ReportGenerationError,
        CSVReadError
)


def print_banner():
    """
    Print application banner.

    Displays a welcome message when the program starts.
    """

    print("\n" + "=" * 80)
    print("CSV HEALTH TRACKER v2.0")
    print("Professional CSV Data Quality Validation Tool")
    print("=" * 80 + "\n")



def print_usage():
    """
    Print usage instructions.

    Shows the user how to run the program correctly.
    
    """

    print("Usage:")
    print("python main.py <path_to_csv_file>")
    print("\nExample:")
    print("python main.py data/health_metrics.csv")
    print("python main.py C:/Users/Documents/data.csv")
    print("\nThe tool will:")
    print(" 1. Validate your CSV file for quality issues")
    print(" 2. Generates a detailed health report")
    print(" 3. Save the report to the output/ directory")
    print()


def parse_arguments():
    """
    Parse command-line arguments

    Returns:
        Path to CSV file if valid, None otherwise

    """

    # Check if user provided a file path
    if len(sys.argv) < 2:
        print("Error: No CSV file specified\n")
        print_usage()
        return None
    
    # Get the file path from command line
    file_path = sys.argv[1]

    return file_path


def handle_validation_sucess(report_path: Path, logger):
    """
    Handles sucessfull validation.

    Args:
        report_path: Path to the generated report
        logger: Logger instance
    """

    print("\n" + "=" * 80)
    print("VALIDATION SUCESSFUL - ALL CHECKS PASSED")
    print("=" * 80)
    print(f"\n Health report saved to: {report_path}")
    print(f"\nYour CSV file passed all data quality checks!")
    print("\nThresholds checked:")
    print(" - Duplicate rows")
    print(" - Missing values")
    print(" - Whitespace pollution")
    print(" - Empty rows/columns")
    print("\nReview the detailed report for complete analysis.")
    print("=" * 80 + "\n")


    logger.info("CSV Health Tracker completed sucessfully")

def handle_validation_failure(error: Exception, logger):
    """
    Handle validation failure with user-friendly messages.

    Args:
        error: The exception that was raised
        logger: Logger instance
    
    """
    print("\n" + "=" * 80)
    print("VALIDATION FAILED")
    print("=" * 80 + "\n")


    # Provide specific guidance based on error type
    if isinstance(error, CSVNotFoundError):
        print("Isue: CSV file not found")
        print(f"Details: {error}")
        print("\nSuggestions:")
        print(" - Check that the file path is correct")
        print(" - Verify the file exists at the specified location")
        print(" - Use absolute path if relative path doesnot work")

    elif isinstance(error, InvalidCSVFormatError):
        print("Issue: Invalid CSV file format")
        print(f"Details: {error}")
        print("\nSuggestions:")
        print(" - Ensure the file has a .csv extension")
        print(" - Verify it's a CSV file, not a directory")
        print(" - Check the file isn't corrupted")

    elif isinstance(error, CSVReadError):
        print("Issues: Cannot read CSV file")
        print(f"Details: {error}")
        print("\nSuggestions:")
        print(" - Check if the file is open in another program")
        print(" - Verify you have read  permissions")
        print(" - Ensure the file isn't corrupted")

    elif isinstance(error, DuplicateRowsExceededError):
        print("Issue: Too many duplicate rows detected")
        print(f"Details: {error}")
        print("\nSuggestions:")
        print(" - Review and remove duplicate entries")
        print(" - Check if duplicates are intentional")
        print(" - Consider adjusting threshold in config.yaml if needed")

    elif isinstance(error, MissingValuesExceededError):
        print("Issue: too many missing values detected")
        print(f"Details: {error}")
        print("\nSuggestions:")
        print(" - Fill in missing values where possible")
        print(" - Remove rows/columns with excessive missing data")
        print(" - Consider if missing data is acceptable for your use case")

    elif isinstance(error, WhiteSpacePollutionError):
        print("Issue: Excessive whitespace pollution detected")
        print(f"Details: {error}")
        print("\nSuggestions:")
        print(" - Clean whitespace from affected columns")
        print(" - Use Excel/Sheets to trim cell values")
        print(" - Consider data cleaning scripts")

    elif isinstance(error, ReportGenerationError):
        print("Issue: Failed to generate report")
        print(f"Details: {error}")
        print("\nSuggestions:")
        print(" - Check that you have write permissions")
        print(" - Ensure output directory is accessible")
        print(" - Verify disk space id availble")

    else:
        print("Issue: Unexpected error occured")
        print(f"Details: {error}")
        print("\nSuggestions:")
        print(" - Check the log file for more details")
        print(" - Verify all requirements are installed")
        print(" - Report this error if it persits")

    print("\n" + "=" * 80 + "\n")

    logger.error(f"Validation failed: {type(error).__name__}: {error}")



def main():
    """
    Main function - orchestrates the entire workflow

    This is the entry point that runs when you execute.
        python main.py <csv_file>

    Workflow:
        1. Parse command-line arguments
        2. Load configuration
        3. Set up logger
        4. Validate CSV file
        5. Generate report
        6. Handle sucess/failure

    Returns:
        Exit code (0 for sucess, 1 for failure)

    
    """

    # Print banner
    print_banner()

    # Parse command-line arguments
    file_path = parse_arguments()
    if file_path is None:
        return 1    # Exit with error code
    
    try:
        # Step 1: Load configuration
        print("Loading configuraration...")
        config = load_config()
        print("Configuration loaded\n")

        # Step 2: Set up logger
        print("Setting up logger...")
        logger = get_logger_from_config(config)
        logger.info("=" * 80)
        logger.info("CSV Health Tracker started")
        logger.info(f"Target file: {file_path}")
        logger.info("=" * 80)
        print("Logger configured\n")


        # Step 3: Validate CSV file
        print(f"Validating CSV file: {file_path}")
        print("Running quality checks...\n")


        results = validate_csv(file_path, logger, config)

        # Step 4: Generate report
        print("\nGenerating health report...")
        report_path = generate_health_report(results, logger, config)
        print("Report generated\n")

        # Step 5: Success!
        handle_validation_sucess(report_path, logger)

        return 0 # Exit with sucess code
    
    except ConfigurationError as e:
        print(f"\n Configuration Error: {e}\n")
        print("Please check your config.yaml file")
        print("run with a valid configuration file.\n")
        return 1
    
    except  CSVHealthTrackerError as e:
        # Handle all CSV Health Tracker specific errors
        logger = None
        try:
            # Try to get logger for error logging
            config = load_config()
            logger = get_logger_from_config(config)
        except:
            pass    # If we can't get logger, continue without it

        handle_validation_failure(e, logger if logger else type('obj', (object), {'error': lambda *args: None}))
        return 1
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user\n")
        return 1
    
    except Exception as e:
        print(f"\nUnexpected error: {e}\n")
        print("This is a bug. Please report it with the error details above.\n")
        return 1
    



if __name__ == "__main__":
    """
    This block runs when you execute: python main.py
    
    It calls main() and exits with the appropiate exit code
    Exit code 0 = success
    Exit code 1 = failure
    
    """
    exit_code = main()
    sys.exit(exit_code)
