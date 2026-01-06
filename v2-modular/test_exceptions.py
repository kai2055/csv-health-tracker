
"""
Test script for custom exceptions

"""



from exceptions import(
    CSVHealthTrackerError,
    CSVNotFoundError,
    CSVReadError,
    InvalidCSVFormatError,
    DuplicateRowsExceededError,
    MissingValuesExceededError,
    WhiteSpacePollutionError,
    ReportGenerationError,
    
)


def test_exception_inheritance():
    """Test that exception hierarchy works correctly"""
    print("=" * 60)
    print("TEST 1: Exception Inheritance")
    print("=" * 80)


    # Test that specific exceptions can be caught by base exception
    try:
        raise CSVNotFoundError("Test file not found")
    except CSVHealthTrackerError as e:
        print(f"CSVNotFoundError caought by CSVHealthTrackerError: {e}")


    try:
        raise DuplicateRowsExceededError("Test duplicate error")
    except CSVHealthTrackerError as e:
        print(f"DuplicateRowsExceededError caught by CSVHealthTrackerError: {e}")
    
    print()



def test_specific_exception_handling():
    """Test handling different exception types differently"""
    print("=" * 80)
    print("TEST 2: Specific Exception Handling")
    print("=" * 80)


    def simulate_error(error_type):
        """Simulate different types of errors"""
        if error_type == "not_found":
            raise CSVNotFoundError("data.csv not found")
        elif error_type == "read_error":
            raise CSVReadError("File is corrupted")
        elif error_type == "validation":
            raise DuplicateRowsExceededError("8% duplicates > 5% threshold")
    

    # Handle each error type differently
    for error_type in ['not_found', 'read_error', 'validation']:
        try:
            simulate_error(error_type)
        except CSVNotFoundError as e:
            print(f"File Error - Action: Check file path | Error: {e}")
        except CSVReadError as e:
            print(f"Read Error - Action: Check file integrity | Error: {e}")
        except DuplicateRowsExceededError as e:
            print(f"Validation Error - Action: Review data quality | Error: {e}")

    print()



def test_exception_with_logger():
    """Test how exceptions work with logger"""
    print("=" * 80)
    print("TEST 3: Exceptions with Logger")
    print("=" * 60)


    from logger import setup_logger
    logger = setup_logger("test_exceptions", "INFO", log_to_file=False)


    try:
        # Simulate validation failure
        duplicate_pct = 8.5
        threshold = 5.0

        if duplicate_pct > threshold:
            error_msg = f"Duplicate rows: {duplicate_pct}% exceeds threshold {threshold}"
            logger.error(error_msg)
            raise DuplicateRowsExceededError(error_msg)
        
    except DuplicateRowsExceededError as e:
        logger.error(f"Validation failed: {type(e).__name__}")
        print(f"Exception logged and caught: {e}")

    print()




if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("CUSTOM EXCEPTIONS TESTING")
    print("=" * 80 + "\n")

    test_exception_inheritance()
    test_specific_exception_handling()
    test_exception_with_logger()



    print("=" * 80)
    print("ALL TESTS COMPLETE")
    
