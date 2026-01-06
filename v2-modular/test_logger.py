"""
Test script for logger module

Demonstration how logger.py integrates with config.py


"""

from config import load_config
from logger import get_logger_from_config, setup_logger

def test_basic_logger():
    """Test basic logger setup without config"""
    print("=" * 80)
    print("TEST 1: Basic logger setup")
    print("=" * 80)



    logger = setup_logger("test_basic", "DEBUG", log_to_file=False)

    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")


    print("\n")


def test_logger_with_config():
    """ Test logger setup using config.yaml settings"""
    print("=" * 80)
    print("TEST 2: Logger with config.yaml settings")
    print("=" * 80)


    try:
        # Load config
        config = load_config()

        # Create logger from config
        logger = get_logger_from_config(config)

        # Log some messages
        logger.info("Logger created from config.yaml settings")
        logger.info(f"Log level: {config['logging']['level']}")
        logger.info(f"Log to file: {config['logging']['log_to_file']}")


        # Test different levels
        logger.debug("This is a debug message")
        logger.info("Processing data...")
        logger.warning("Found 5% duplicate rows")
        logger.error("Failed to read file")

        print("\nSucecess! Check 'logs' directory for log file.")

    except Exception as e:
        print(f"Error: {e}")

    print("\n")



def test_log_levels():
    """Demonstrate how log levels filter messages"""
    print("=" * 80)
    print("TEST 3: Log level filtering")
    print("=" * 80)

    print("\nWith log level INFO (should NOT see DEBUG):")
    logger_info = setup_logger("test_info", "INFO", log_to_file=False)
    logger_info.debug("DEBUG: YOU SHOULD NOT SEE THIS")
    logger_info.info("INFO: You should see this")
    logger_info.warning("WARNING: You should see this")

    print("\nWith log level WARNING (should only see WARNING and above):")
    logger_warning = setup_logger("test_warning", "WARNING", log_to_file=False)
    logger_warning.debug("DEBUG: YOU SHOULD NOT SEE THIS")
    logger_warning.info("INFO: YOU SHOULD NOT SEE THIS")
    logger_warning.warning("WARNING: You should see this")
    logger_warning.error("ERROR: You should see this")

    print("\n")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("LOGGER MODULE TESTING")
    print("=" * 80 + "\n")

    test_basic_logger()
    test_logger_with_config()
    test_log_levels()

    print("=" * 80)
    print("ALL TESTS COMPLETE")
    print("=" * 80)