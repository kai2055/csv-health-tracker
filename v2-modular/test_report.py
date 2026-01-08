"""
Test Script for report module

Tests report generation from validation results

"""


import pandas as pd
from pathlib import Path


from config import load_config
from logger import get_logger_from_config
from validation import validate_csv
from report import HealthReportGenerator, generate_health_report
from exceptions import ReportGenerationError


def create_sample_csv():
    """Create a sample CSV for testing"""
    data = {
        'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-0104'],\
        'metric': ['temperature', 'humidity', 'pressure', 'temperature'],
        'value': [22.5, 65.0, 1013.25, 23.0],
        'notes': ['clear', 'cloudy', 'sunny', 'clear']
    }

    df = pd.DataFrame(data)
    df.to_csv('sample_data.csv', index=False)
    print("Created sample_data.csv")


def test_report_generation():
    """Test generating report from validation results"""
    print("\n" + "=" * 80)
    print("TEST 1: Report Generation")
    print("=" * 80)


    # Setup
    config = load_config()
    logger = get_logger_from_config(config)


    # Create sample CSV and validate it
    create_sample_csv()

    try:
        # Validate CSV to get results
        results = validate_csv('sample_data.csv', logger, config)


        # Generate report
        generator = HealthReportGenerator(logger, config)
        report = generator.generate_report(results)


        print("\nReport generated sucessfully")
        print(f"Report length: {len(report)} characters")
        print(f"Report lines: {len(report.split(chr(10)))}")

        # Show first few lines
        print("\nReport preview (first 500 characters):")
        print("-" * 80)
        print(report[:500])
        print(".....")


    except Exception as e:
        print(f"x Error: {e}")



def test_save_report():
    """Test saving report to file"""
    print("\n" + "=" * 80)
    print("TEST 2: Save Report to File")
    print("=" * 80)


    # Setup
    config = load_config()
    logger = get_logger_from_config(config)


    # Create sample CSV and validate it
    create_sample_csv()

    try:
        # Validate CSV
        results = validate_csv('sample_data.csv', logger, config)

        # Generate and save report
        generator = HealthReportGenerator(logger, config)
        report = generator.generate_report(results)
        report_path = generator.save_report(report, results['basic_info']['filename'])


        print(f"\nReport saved sucessfully")
        print(f"Location: {report_path}")
        print(f"File exists: {report_path.exists()}")
        print(f"File size: {report_path.stat().st_size} bytes")


        # Verify output directory exists
        output_dir = Path(config['output']['directory'])
        print(f"Output directory: {output_dir}")
        print(f"Contains files: {list(output_dir.glob('*.txt'))}")

    except Exception as e:
        print(f"x Error: {e}")



def test_convenience_function():
    """Test the convenience function"""
    print("\n" + "=" * 80)
    print("TEST 3: COnvenience Function")
    print("=" * 80)


    # Setup
    config = load_config()
    logger = get_logger_from_config(config)


    # Create sample CSV and validate it
    create_sample_csv()

    try:
        # Validate CSV
        results = validate_csv('sample_data.csv', logger, config)

        # Generate and save using convenience function
        report_path = generate_health_report(results, logger, config)

        print(f"\nReport generated and saved using convenience function")
        print(f"Location: {report_path}")

    except Exception as e:
        print(f"x Error: {e}")



def test_end_to_end():
    """Test complete workflow: validate -> generate report -> save"""
    print("\n" + "=" * 80)
    print("TEST 4: Complete End-to-End Workflow")
    print("=" * 80)


    # Setup
    config = load_config()
    logger = get_logger_from_config(config)

    # Create sample CSV
    create_sample_csv()

    try:
        print("\nStep 1: Validating CSV...")
        results = validate_csv('sample_data.csv', logger, config)
        print("Validation complete")

        print("\nStep 2: Generating report...")
        report_path = generate_health_report(results, logger, config)
        print(f"Report saved to: {report_path}")

        print("\nStep 3: Reading saved report...")
        with open(report_path, 'r', encoding='utf-8') as f:
            saved_report = f.read()
        print(f"Report read sucessfully ({len(saved_report)} characters)")

        print("\n" + "=" * 80)
        print("SAVED REPORT CONTENT:")
        print("=" * 80)
        print(saved_report)
        print("=" * 80)


    except Exception as e:
        print(f"Error: {e}")




def test_report_with_issues():
    """Test report generation with data quality issues"""
    print("\n" + "=" * 80)
    print("TEST 5: Report with Data Quality Issues")
    print("=" * 80)


    # Create CSV with issues
    data = {
        'date': ['2024-01-01', '2024-01-01', None, ' 2024-01-04 '],  # duplicate, missing, whitespace
        'metric': ['temp', 'temp', 'pressure', None],  # duplicate, missing
        'value': [22.5, 22.5, 1013.25, None],
        'notes': ['clear', 'clear', 'sunny', None]
    }
    df = pd.DataFrame(data)
    df.to_csv('data_with_issues.csv', index=False)
    print("Created data_with_issues.csv")

    # Setup
    config = load_config()
    logger = get_logger_from_config(config)

    try:
        # This should pass validation (under thresholds)
        # but report should show the issues
        results = validate_csv('data_with_issues.csv', logger, config)

        # Generate report
        report_path = generate_health_report(results, logger, config)

        print(f"\nReport generated: {report_path}")

        # Show report
        with open(report_path, 'r', encoding='utf-8') as f:
            report = f.read()

        print("\n" + "=" * 80)
        print("REPORT WITH ISSUES:")
        print("=" * 80)
        print(report)

    except Exception as e:
        print(f"Note: {type(e).__name__}: {e}")
        print("(This is expected if issues exceed thresholds)")



def cleanup_test_files():
    """Remove test files"""
    test_files = [
        'sample_data.csv',
        'data_with_issues.csv'
    ]

    for file in test_files:
        path = Path(file)
        if path.exists():
            path.unlink()

    print("\nCleaned up test CSV files")
    print("(Output reports kept in output/directory for review)")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("REPORT MODULE TESTING")
    print("=" * 60)

    try:
        test_report_generation()
        test_save_report()
        test_convenience_function()
        test_end_to_end()
        test_report_with_issues()

        print("\n" + "=" * 80)
        print("ALL TESTS COMPLETE")
        print("=" * 80)
        print("\nCheck the 'output/' directory to see generated reports!")

    finally:
        cleanup_test_files()



    


