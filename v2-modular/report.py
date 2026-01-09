"""
Report Generation Module

Generates formatted health reports from CSV validation resullts.

This module takes the validation results dictionary and creates:
- Human-readable text reports
- Saved to output directory with timestamps
- Clear formatting for eacy reading

"""


from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from exceptions import ReportGenerationError


class HealthReportGenerator:
    """
    Generates health reports from validation results.

    Why a class?
    - Groups report generation logic together
    - Can store config and logger
    - Easy to extend with different report formats (JSON, HTML, etc.)
    - Professional practice for complex formatting

    """

    def __init__(self, logger, config: Dict[str, Any]):
        """
        Initialize the report generator.

        Args:
            logger: Logger instance for logging
            config: Configuration dictionary from config.yaml

        """
        self.logger = logger
        self.config = config


    
    def _create_output_directory(self) -> Path:
        """
        Create output directory if it doesn't exist.

        Private method (leading underscore)

        Returns:
            Path object to output directory

        Raises:
            ReportGenerationError: If directory can't be created

        
        """

        output_dir = Path(self.config['output']['directory'])

        try:
            output_dir.mkdir(exist_ok=True)
            self.logger.debug(f"Output directory ready: {output_dir}")
            return output_dir
        
        except Exception as e:
            self.logger.error(f"Failed to create output directory: {e}")
            raise ReportGenerationError(f"Cannot create output directory: {e}")
    


    def _generate_header(self, filename: str) -> str:
        """
        Generate report header section.

        Args:
            filename: Name of the CSV file that was validated

        Returns:
            Formatted header string

        """

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        header = [
            "=" * 80,
            "CSV HEALTH TRACKER - VALIDATION REPORT",
            "=" * 80,
            f"File: {filename}",
            f"Report Generated: {timestamp}",
            "=" * 80,
            ""
        ]

        return "\n".join(header)
    



    def _generate_basic_info_section(self, basic_info: Dict[str, Any]) -> str:
        """
        Generates basic information section.

        Args:
            basic_info: Dictionary with filename, shape, columns,  dtypes

        Returns:
            Formatted basic info string
        
        """
        
        rows, cols = basic_info['shape']
        columns = basic_info['columns']
        dtypes = basic_info['dtypes']

        section = [
            "BASIC INFORMATION",
            "-" * 80,
            f"Dimensions: {rows} rows X {cols} columns",
            f"",
            f"Columns ({len(columns)}):",
        ]


        # List columns with their data types
        for col in columns:
            dtype = dtypes.get(col, 'unknown')
            section.append(f" .{col} ({dtype})")


        section.append("")


        return "\n".join(section)
    
    


    def _generate_headers_section(self, headers: Dict[str, Any]) -> str:
        """
        Generate column headers section.

        Args:
            headers: Dictionary with has_headers, column_names, duplicate_columns


        Returns:
            Formatted headers section string
        
    
        """
        section = [
            "COLUMN HEADERS",
            "-" * 80,
        ]

        # Check is headers exist
        if headers['has_headers']:
            section.append("Column headers detected")
        else:
            section.append("WARNING: No column headers detected (using default: 0, 1, 2, .....)")

        # Check for duplicate column names
        if headers['duplicate_columns']:
            section.append(f"WARNING: Duplicate column names: {headers['duplicate_columns']}")
        else:
            section.append("No duplicate column names")

        section.append("")

        return "\n".join(section)
    


    def _generate_duplicates_section(self, duplicates: Dict[str, Any]) -> str:
        """
        Generate duplicate rows section.

        Args:
            duplicates: Dictionary with count and percentage

        Returns:
            Formatted duplicates section string
        
        
        """
        count = duplicates['count']
        percentage = duplicates['percentage']
        threshold = self.config['validation']['max_duplicate_pct']


        section = [
            "DUPLICATE ROWS",
            "=" * 80,
            f"Duplicate Count: {count}",
            f"Duplicate Percentage: {percentage:.2f}%",
            f"Threshold: {threshold}%",
            ""
        ]


        # status
        if percentage <= threshold:
            section.append(f"PASSED: {percentage:.2f}% <= {threshold}%")
        else:
            section.append(f"FAILED: {percentage:.2f}% > {threshold}%")


        section.append("")

        return "\n".join(section)
    



    def _generate_missing_values_section(self, missing_values:Dict[str, float]) -> str:
        """
        Generate missing values section.

        Args: 
            missing_values: Dictionary mapping column names to missing percentages

        Returns:
            Formatted missing values section string

        """
        threshold = self.config['validation']['max_missing_pct']

        section = [
            "MISSING VALUES",
            "-" * 80,
            f"Threshold: {threshold}%",
            ""
        ]

        # Check if any missing values
        has_missing = any(pct > 0 for pct in missing_values.values())

        if not has_missing:
            section.append("No missing values detected")
        else:
            section.append("Missing values by column:")
            for col, pct in missing_values.items():
                if pct > 0:
                    status = "Right" if pct <= threshold else "wrong"
                    section.append(f"{status} {col}: {pct:.2f}%")

        section.append("")

        return "\n".join(section)
    


    def _generate_whitespace_section(self, whitespace:Dict[str, float]) -> str:
        """
        Generate whitespace pollution section

        Args:
            whitespace: Dictionary mapping column names to whitespace percentages

        Returns:
            Formatted whitespace section string

        
        
        """

        threshold = self.config['validation']['whitespace_threshold_pct']


        section = [
            "WHITESPACE POLLUTION",
            "-" * 80,
            f"Threshold: {threshold}%",
            ""
        ]

        # Check if any whitespace issues
        has_whitespace = any(pct > 0 for pct in whitespace.values())


        if not has_whitespace:
            section.append("No whitespace pollution detected")
        else:
            section.append("Whitespace by column:")
            for col, pct in whitespace.items():
                if pct > 0:
                    status = "right" if pct <= threshold else "wrong"
                    section.append(f"{status} {col}: {pct:.2f}%")

        
        section.append("")

        return "\n".join(section)
    


    def _generate_empty_data_section(self, empty_data: Dict[str, Any]) ->  str:
        """
        Generate empty rows/columns section.

        Args:
            empty_data: Dictionary with empty_columns and empty_row_count

        Returns:
            Formatted empty data section string

        
        """

        empty_cols =empty_data['empty_columns']
        empty_rows = empty_data['empty_row_count']

        section = [
            "EMPTY DATA",
            "=" * 80,
        ]


        # Empty columns
        if empty_cols:
            section.append(f"WARNING: {len(empty_cols)} empty column(s): {empty_cols}")
        else:
            section.append("No empty columns")


        # Empty rows
        if empty_rows > 0:
            section.append(f"WARNING: {empty_rows} completely empty row(s)")
        else:
            section.append("No empty rows")


        section.append("")

        return "\n".join(section)
    


    def _generate_summary(self, results: Dict[str, Any]) -> str:
        """
        Generate overall summary section

        Args:
            results: Complete validation results dictionary

        Returns:
            Formatted summary string

        """
        section = [
            "=" * 80,
            "SUMMARY",
            "=" * 80,
        ]



        # Count issues
        issues = []

        # Check duplicates
        dup_pct = results['duplicates']['percentage']
        dup_threshold = self.config['validation']['max_duplicate_pct']
        if dup_pct > dup_threshold:
            issues.append(f"Duplicate rows: {dup_pct:.2f}% > {dup_threshold}%")

        # Check missing values 
        max_missing_threshold = self.config['validation']['max_missing_pct']
        for col, pct in  results['missing_values'].items():
            if pct > max_missing_threshold:
                issues.append(f"Missing values in '{col}': {pct:.2f}% > {max_missing_threshold}%")

        
        # Check whitespace
        ws_threshold = self.config['validation']['whitespace_threshold_pct']
        for col, pct in results['whitespace'].items():
            if pct > ws_threshold:
                issues.append(f"Whitespace in '{col}: {pct:.2f}% > {ws_threshold}%")



        # Check empty data
        if results['empty_data']['empty_columns']:
            issues.append(f"Empty columns: {results['empty_data']['empty_column']}")
        if results['empty_data']['empty_row_count'] > 0:
            issues.append(f"Empty rows: {results['empty_data']['empty_row_count']}")


        # Overall status
        if not issues:
            section.append("ALL CHECK PASSED")
            section.append("No data quality issues detected.")
        else:
            section.append(f"x {len(issues)} ISSUE(s) DETECTED")
            section.append("")
            for issue in issues:
                section.append(f" . {issue}")

        section.append("")
        section.append("=" * 80)

        return "\n".join(section)
    

    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """
        Generate complete health report from validation results.

        Args:
            results: Validation results dictionary from CSVValidator


        Returns: 
            Complete formatted report as string
        
    
        """

        self.logger.info("Generating health report...")

        report_sections = [
            self._generate_header(results['basic_info']['filename']),
            self._generate_basic_info_section(results['basic_info']),
            self._generate_headers_section(results['headers']),
            self._generate_duplicates_section(results['duplicates']),
            self._generate_missing_values_section(results['missing_values']),
            self._generate_whitespace_section(results['whitespace']),
            self._generate_empty_data_section(results['empty_data']),
            self._generate_summary(results)

        ]

        report = "\n".join(report_sections)

        self.logger.info("Report generated sucessfully!")
        return report
    


    def save_report(self, report: str, original_filename: str) -> Path:
        """
        Save report to output directory with timestamp.

        Args:
            report: Formatted report string
            original_filename: Original CSV filename (for report naming)

        Returns:
            Path to saved report file

        Raises:
            ReportGenerationError: If file can't be saved

        """
        self.logger.info("Saving report to file...")

        # Create output directory
        output_dir = self._create_output_directory()

        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename_prefix = self.config['output']['filename_prefix']


        # Extract base name from original file (without .csv)
        base_name = Path(original_filename).stem

        report_filename = f"{filename_prefix}_{base_name}_{timestamp}.txt"
        report_path = output_dir / report_filename

        # Write report to file
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)

            self.logger.info(f"Report saved: {report_path}")
            return report_path
        
        except Exception as e:
            self.logger.error(f"Failed to save report: {e}")
            raise ReportGenerationError(f"Cannot save report to {report_path}: {e}")
        


    def generate_and_save(self, results: Dict[str, Any]) -> Path:
        """
        Convinence method: generate and save report in one call
        
        Args:
            results: Validation results dictionary
            
        Returns:
            Path to saved report file
            
        """

        report = self.generate_report(results)
        report_path = self.save_report(report, results['basic_info']['filename'])
        return report_path
    

    # Convenience function for simple usage
def generate_health_report(results: Dict[str, Any], logger, config: Dict[str, Any]) -> Path:
    """
    Convienence function to generate and save a health report

    Args:
        result: Validation results dictionary
        logger: Logger instance
        config: Configuration dictionary

    Returns:
        Path to saved report file

    Raises:
    ReportGenerationError: If report generation fails
        
        
    """

    generator = HealthReportGenerator(logger, config)
    return generator.generate_and_save(results)



