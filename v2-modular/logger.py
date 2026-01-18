
"""
Logging Setup Module

Configures Python's logging system for the CSV Health Tracker.

Why seperate logging setup?
- Consistent log format across all modules
- easy to change logging behavior in one place


Key Concepts:
- Logger - The object you call to log messages (logger.info("message"))
- Handler - Where logs go (console, file, or both)
- Formatter - How logs look (timestamp, level, message)
- Level - Importance threshold (DEBUG < INFO < WARNING < ERROR < CRITICAL)


"""


import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


def setup_logger(
        name: str = "csv_health_tracker",
        log_level: str = "INFO",
        log_to_file: bool = False,
        log_dir: str = "logs",        
) -> logging.Logger:
    """
    Set up and configure a logger with console and optional file output.

    This is the main function you call to get a logger for your module.

    Args:
        name: Logger name (usually module name or app name)
        log_level: Minimum level to log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to write logs to a file
        log_dir: Directory for log files (created if doesn't exist)

    Returns:
        configured logger instance

    """

    # Get logger instance
    # If a logger with this name already exists, Python returns it
    
    logger = logging.getLogger(name)

    # Set the base logging level
    # This is the MINIMUM level this logger will process
    logger.setLevel(log_level.upper())

    # Clear any existing handlers
    # Important: prevents duplicate log messages if logger is reconfigured
    if logger.handlers:
        logger.handlers.clear()

    # Create console handler (logs to terminal/stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level.upper())

    # Create formatter - defines how log messages look
    # Format: "2024-01-15 14:30:45 - INFO - This is the message"
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Attach formatter to console handler
    console_handler.setFormatter(formatter)

    # Add console handler to logger
    logger.addHandler(console_handler)

    # Add file handler if requested
    if log_to_file:
        file_handler = _create_file_handler(log_dir, log_level)
        logger.addHandler(file_handler)

    return logger


def _create_file_handler(log_dir: str, log_level: str) -> logging.FileHandler:
    """
    Create a file handler for writing logs to a file.

    This is a PRIVAATE helper function
    Only used inside this module

    

    Args:
        log_dir: Directory where log files will be stored
        log_level: Minimum level to log to file

    Returns:
        Configured FileHandler instance
    
    
    """

    # Create log directory if it doesn't exist
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)   # exist_ok=True means "don't error if already exists"

    # Create timestamped log filename
    # Example: "csv_health_tracker_2024-01-15_14-30-45.log"
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = f"csv_health_tracker_{timestamp}.log"
    log_file = log_path / log_filename

    # Create file handler
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(log_level.upper())

    # Create formatter with more detail for file logs
    # File logs include module name and line number for debugging
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(detailed_formatter)

    return file_handler


def get_logger_from_config(config: dict, name: str = "csv_health_tracker") -> logging.Logger:
    """
    Create a logger using settings from config dictionary

    This is a convenience function that bridges config.py and logger.py
    It extracts logging settings from your config.yaml and passes them to setup_logger()

    Why this function exists?
    - Makes it easy to use config settings for logging
    - calling code doesn't need to know config structrure
    - Single point of integration between config and logging

    Args:
        config: Configuration dictionary (from config.load_config())
        name: Logger name

    Return:
        Configured logger instance

    
    """

    # Extract logging settings from config
    log_level = config['logging']['level']
    log_to_file = config['logging']['log_to_file']

    

    log_dir = "logs"

    # Create and return logger with config settings
    return setup_logger(
        name=name,
        log_level=log_level,
        log_to_file=log_to_file,
        log_dir=log_dir
    )






