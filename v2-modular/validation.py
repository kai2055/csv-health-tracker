"""
CSV Validation Module

Contains all CSV file validation logic.


This module performs:
- File path validation
- CSV structure checks
- Data quality checks (duplicates, missing values, whitespce)
- Uses config thresholds
- Raises custom exceptions
- Logs all findings


"""


import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Any

from exceptions import(
    CSVNotFoundError,
    CSVReadError,
    InvalidCSVFormatError,
    DuplicateRowsExceededError,
    MissingValuesExceededError,
    WhiteSpacePollutionError
)



class CSVValidator:
    """
    Validates CSV files for data quality issues.

    This class encapsulates all validation logic in one place

    Why a class?
    - Groups related validation functions together
    - can store state (config, logger, dataframe)
    - Easier to test and maintain
    - Professional practice for complex logic
    
    """


    def __init__(self, logger, config: Dict[str, Any]):
        """
        Initialize th validator with logger and config

        Args:
            logger: Logger instance for logging messages
            config: Configuration dictionary from config.yaml

        """
        self.logger = logger
        self.config = config
        self.df = None  # Will hold the loaded DataFrame
        self.file_path = None   # Will hold the file path

    

    def validate_file_path(self, file_path: str) -> Path:
        """
        Validate that the file path exists and is a CSV file.

        Args:
            file_path: String path to the CSV file

        Raises: 
            CSVNotFoundError: If file doesn't exist
            InvalidCSVFormatError: If not a file or not a CSV
        
        
        """
        self.logger.info(f"Validating file path: {file_path}")

        file_path_obj = Path(file_path)


        # Check 1: DOes the file exist?
        if not file_path_obj.exists():
            self.logger.error(f"File not found: {file_path}")
            raise CSVNotFoundError(f"File '{file_path}' does not exist")
        

        # Check 2: Is it a file (not a directory)
        if not file_path_obj.is_file():
            self.logger.error(f"Path is a directory, not a file: {file_path}")


        # Check 3: Is it a CSV file?
        if file_path_obj.suffix.lower() != '.csv':
            self.logger.error(f"File is not a CSV: {file_path}")
            raise InvalidCSVFormatError(
                f"File '{file_path}' is not a CSV file (extension: {file_path_obj.suffix})"

            )
        
        self.logger.info("File path validation passed")
        self.file_path = file_path_obj
        return file_path_obj
    

    def load_csv(self, file_path: Path) -> pd.DataFrame:
        """
        Load CSV file into a pandas DataFrame

        Args:
            file_path: Path object to the CSV file

        Returns:
            Loaded DataFrame

        Raises:
            CSVReadError: If file can't be read

        """
        self.logger.info(f"Loading CSV file: {file_path.name}")


        try:
            df = pd.read_csv(file_path)
            self.logger.info(f"CSV loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
            self.df = df
            return df
        
        except Exception as e:
            self.logger.error(f"Failed to read CSV: {e}")
            raise CSVReadError(f"Failed to read CSV file: {e}")
        

    
    def check_column_headers(self) -> Dict[str, Any]:
        """
        Check for column header issues.

        Checks:
        - Missing headers (pandas assigns default numeric names)
        - Duplicate column names

        Returns:
            Dictionary with findings

        """

        self.logger.info("Checking column headers...")

        results = {
            'has_headers': True,
            'column_names': self.df.columns.tolist(),
            'duplicate_columns': []
        }

        # Check if pandas assigned default numeric column names
        # This happens when CSV has no header row
        has_default_names = all(isinstance(col, int) for col in self.df.columns)

        if has_default_names:
            self.logger.warning("No column headers detected (using default names: 0,1,2,....)")
            results['has_headdrs'] = False

        # Check for duplicate column names
        duplicate_columns = self.df.columns[self.df.columns.duplicated()].tolist()
        results['duplicate_columns'] = duplicate_columns

        if results['has_headers'] and not duplicate_columns:
            self.logger.info("Column headers check passed")

        return results
    

    def check_duplicate_rows(self) -> Tuple[int, float]:
        """
        Check for duplicate rows and compare against threshold

        Returns:
            Tuple of (duplicate_count, duplicate_percentage)

        Raises:
            DuplicateRowsExceededError: If duplicates exceed threshold
        
        """

        self.logger.info("Checking for duplicate rows....")

        num_duplicates = self.df.duplicated().sum()
        total_rows = len(self.df)
        duplicate_pct = (num_duplicates / total_rows * 100) if total_rows > 0 else 0

        self.logger.info(f"Found {num_duplicates} duplicate rows {duplicate_pct:.2f}%")

        # Get threshold from config
        max_duplicate_pct = self.config['validation']['max_duplicate_pct']
        

        # Check against threshold
        if duplicate_pct > max_duplicate_pct:
            error_msg = (
                f"Duplicate rows check FAILED: {duplicate_pct:.2f}% exceeds "
                f"threshold of {max_duplicate_pct}%"
            )
            self.logger.error(error_msg)
            raise DuplicateRowsExceededError(error_msg)
        
        self.logger.info(f"Duplicate rows check PASSED: {duplicate_pct:.2f}% <= {max_duplicate_pct}%")
        return num_duplicates, duplicate_pct
    


    def check_empty_rows_columns(self) -> Dict[str, Any]:
        """
        Check for completely empty rows and columns.

        Returns:
            Dictionary with findings
        
        
        """
        self.logger.info("Checking for empty rows and columns...")


        # Empty columns
        empty_cols = self.df.columns[self.df.isna().all()].tolist()

        if empty_cols:
            self.logger.warning(f"Empty columns detected: {empty_cols}")


        # Empty rows
        empty_rows = self.df[self.df.isna().all(axis=1)]
        num_empty_rows = len(empty_rows)

        if num_empty_rows > 0:
            self.logger.warning(f"Found {num_empty_rows} completely empty rows")

        if not empty_cols and num_empty_rows == 0:
            self.logger.info("No empty rows or columns detected")

        return {
            'empty_columns': empty_cols,
            'empty_row_count': num_empty_rows
        }    
    

    def check_missing_values(self) -> Dict[str, float]:
        """
        Check for missing values per column and compare against threshold.

        Returns:
            Dictionary mapping column names to missing percentage

        Raises:
            MissingValueExceededError: IF any column excceeds threshold
        
        """
        self.logger.info("Checking for missing values...")

        max_missing_pct = self.config['validation']['max_missing_pct']
        missing_by_column = {}
        violations = []

        for col in self.df.columns:
            missing_count = self.df[col].isna().sum()
            missing_pct = (missing_count / len(self.df) * 100) if len(self.df) > 0 else 0
            missing_by_column[col] = missing_pct

            if missing_pct > 0:
                self.logger.debug(f"Column '{col}': {missing_pct:.2f}% missing values")

            # Check against threshold
            if missing_pct > max_missing_pct:
                violations.append(f"Column '{col}': {missing_pct:.2f}% > {max_missing_pct}%")

        
        if violations:
            error_msg = f"Missing values exceeded threshold:\n" + "\n".join(violations)
            self.logger.error(error_msg)
            raise MissingValuesExceededError(error_msg)
        
        self.logger.info(f"Missing values check PASSED (all columns <= {max_missing_pct}%)")
        return missing_by_column
    

    def check_whitespace_pollution(self) -> Dict[str, float]:
        """
        Check for whitespece pollution in string columns.

        Whitespace pollution = values with leading/trailing whitespace

        Returns:
            Dictionary mapping column names to whitespace percentage

        Raises:
            WhitespacePollutionError: If any column exceeds threshold
        
        
        """
        self.logger.info("Checkig for whitespace pollution...")

        threshold = self.config['validation']['whitespace_threshold_pct']
        whitespace_by_column = {}
        violations = []


        # Check each string column 
        for col in self.df.select_dtypes(include='object').columns:
            # Check if value is string and has whitespace
            has_whitespace = self.df[col].apply(
                lambda x: isinstance(x, str) and x != x.strip()
            )
            whitespace_count = has_whitespace.sum()
            whitespace_pct = (whitespace_count / len(self.df) * 100) if len(self.df) > 0 else 0
            whitespace_by_column[col] = whitespace_pct

            if whitespace_pct > 0:
                self.logger.debug(f"Column '{col}: {whitespace_pct:.2f}% whitespace pollution'")

            # Check against threshold 
            if whitespace_pct > threshold:
                violations.append(f"Column '{col}': {whitespace_pct:.2f}% > {threshold}%")


        if violations:
            error_msg = "Whitespace pollution exceeded threshold:\n" + "\n".join(violations)
            self.logger.warning(error_msg)
            raise WhiteSpacePollutionError(error_msg)
        

        self.logger.info(f"Whitespace check PASSED (all columns <= {threshold}%)")
        return whitespace_by_column
    


    def get_basic_info(self) -> Dict[str, Any]:
        """
        Get basic information about the DataFrame.

        Returns:
            Dictionary with basic statistics

        
        """

        self.logger.info("Gathering basic CSV information...")

        return {
            'filename': self.file_path.name if self.validate_file_path else 'unknown',
            'shape': self.df.shape,
            'columns': self.df.columns.tolist(),
            'dtypes': self.df.dtypes.to_dict(),
            'memory_usage': self.df.memory_usage(deep=True).sum()

        }
    


    def validate_all(self, file_path: str) -> Dict[str, Any]:
        """
        Run all validation checks on a CSV file

        This is the main function that orchestrates all checks.

        Args:
            file_path: Path to the CSV file

        Returns:
            Dictionary containing all validation results

        Raises:
            Various CSVHealthTrackerError exceptions id validation fails
        
        """

        self.logger.info("=" * 80)
        self.logger.info("Starting CSV Health Check")
        self.logger.info("=" * 80)

        # Validate and load file
        validated_path = self.validate_file_path(file_path)
        self.load_csv(validated_path)

        # Run all checks
        results = {
            'basic_info': self.get_basic_info(),
            'headers': self.check_column_headers(),
            'empty_data': self.check_empty_rows_columns()
        }

        # These checks can raise exceptions
        try:
            dup_count, dup_pct = self.check_duplicate_rows()
            results['duplicates'] = {'count': dup_count, 'percentage': dup_pct}
        except DuplicateRowsExceededError:
            raise # Re-raise to let caller handle

        try:
            results['missing_values'] = self.check_missing_values()
        except MissingValuesExceededError:
            raise   # Re-raise to let caller handle
        

        try:
            results['whitespace'] = self.check_whitespace_pollution()
        except WhiteSpacePollutionError:
            raise # Re-raise to let the caller handle

        self.logger.info("=" * 80)
        self.logger.info("CSV Health Check Complete - ALL CHECKS PASSED")
        self.logger.info("=" * 80)

        return results
    

# Convenience function for simple usage
def validate_csv(file_path: str, logger, config:Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to validate a CSV file.


    Args:
        file_path: Path to CSV file
        logger: Logger instance
        config: Configuration dictionary

    Returns:
        Validtion results dictionary

    Raises:
        Various CSVHealthTrackerError exceptions

    
    """

    validator = CSVValidator(logger, config)
    return validator.validate_all(file_path)




            