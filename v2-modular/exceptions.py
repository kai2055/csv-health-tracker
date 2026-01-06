"""
Custom Exceptions Module

Defines specific error types for the CSV Health Tracker.

Why custom exceptions?
- More descriptive than generic Exception
- Easier to handle different error types seperately
- Better error messages for users and logs
- Professional practice in procuction code

Exception Hierarchy:
    CSVHealthTrackerError (base)
        ConfigurationError (already in config.py)

        CSVFileError
            CSVNotFoundError
            CSVReadError
            InvalidCSVFormatError
        
        ValidationError
            DuplicateRowsExceededError
            MissingValuesExceededError
            WhitespacePollutionError
    
    ReportGenerationError


"""


class CSVHealthTrackerError(Exception):
    """
    Base exception for all CSV Health Tracker errors.

    Why a base exception?
    - Allows catching ALL project errors with one except clause
    - Creates a clear hierarchy
    - Professional practice for larger projects

    """
    pass



# FILE-RELATED EXCEPTIONS

class CSVFileError(CSVHealthTrackerError):
    """
    Base exception for CSV file-related errors.

    Inherits from CSVHealthTrackerError, so it's also catchable
    by the base exception
    
    """
    pass


class CSVNotFoundError(CSVFileError):
    """
    Raised when the CSV file doesn't exist
    
    """
    pass

class CSVReadError(CSVFileError):
    """
    Raised when file exists but can't be read.

    Common causes:
    - File is corrupted
    - File is locked by another program
    - Permission denied
    - Not actually a CSV file
    
    """
    pass


class InvalidCSVFormatError(CSVFileError):
    """
    Raised when CSV file has wrong structure.
    
    Examples:
    - Missing required columns
    - Wrong column names
    - Empty file
    - No header row
    
    """

    pass




# VALIDATION-RELATED EXCEPTIONS

class ValidationError(CSVHealthTrackerError):
    """
    Base exception for data validation errors.

    These are raised when data fails quality checks
    """

    pass


class DuplicateRowsExceededError(ValidationError):
    """
    Raised when duplicate row percentage exceeds threshold.

    """
    pass


class MissingValuesExceededError(ValidationError):
    """
    Raised when missing value percentage exceeds thresholds.
    
    """
    pass


class WhiteSpacePollutionError(ValidationError):
    """
    Raised when whitespace pollution exceeds threshold.

    Whitespace pollution = calls that are empty or only contain spaces/tabs
    
    """
    pass



# REPORT RELATED EXCEPTIONS


class ReportGenerationError(CSVHealthTrackerError):
    """
    Raised when report generation fails.

    Common causes:
    - can't create output directory
    - can't write to output file
    - permission denied
    
    """

    pass







