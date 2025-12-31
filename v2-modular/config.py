
"""
Configuration Management Module

Handles loading and validating configuration from YAML files.

Key Principle: Fail fast with clear errors.
Better to crash at startup with "Invalid config" than to crash 
after 10 minutes of processing with a mysterious error.

"""

import yaml
from pathlib import Path
from typing import Dict, Any

class ConfigurationError(Exception):
    """
    Custom exception for configuration problems.

    Why create our own exception?
    - Makes it clear WHAT kind of error occured
    - Lets calling code handle config errors differently than other errors
    - More professional than generic Exception
    
    """
    pass

def load_config(config_path: str = 'config.yaml') -> Dict[str, Any]:
    """
    Load and validate configuration from a YAML file.

    Args:
        config_path: Path to the YAML configuration file

    Returns:
        Dictionary containing validated configuration

    Raises:
        ConfigurationError: If config file is missing or invalid

    
    """

    config_file = Path(config_path)

    # Check if it exists
    if not config_file.exists():
        raise ConfigurationError(
            f"Configuration file not found: {config_path}\n"
            f"Please create a config.yaml file in the project directory."
        )
    
    # Load the YAML file
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ConfigurationError(
            f"Invalid YAML in configuration file: {e}"
        )
    
    # Validate that config isn't empty
    if config is None:
        raise ConfigurationError(
            "Configuration file is empty"
        )
    
    # Validate required sections and fields exist
    _validate_config(config)

    return config



def _validate_config(config: Dict[str, Any]) -> None:
    """
    Validate that configuration has all required fields with valid values.

    This is a PRIVATE function (leading underscore _)
    Only used inside this module.

    Args:
        config: Configuuration dictionary to validate

    Raises:
        ConfigurationError: If required fields are missing or invalid
    
    """

    # Define required structure
    required_structure = {
        'validation': ['whitespace_threshold_pct', 'max_duplicate_pct', 'max_missing_pct'],
        'output': ['directory', 'filename_prefix'],
        'logging': ['level', 'log_to_file']

    }

    # Check that top-level sections exist
    for section in required_structure.keys():
        if section not in config:
            raise ConfigurationError(
                f"Missing required configuration sections: '{section}'"
            )
        
    
    # Check that each section has its required fields
    for section, fields in required_structure.items():
        for field in fields:
            if field not in config[section]:
                raise ConfigurationError(
                    f"Missing required field: '{section}.{field}'"
                )
            


    # Validate specific field values
    _validate_validation_section(config['validation'])
    _validate_logging_section(config['logging'])



def _validate_validation_section(validation_config: Dict[str, Any]) -> None:
    """
    Validate the 'validation' section of config

    Checks that thresholds are reasonable numbers.
    
    """

    # Check whitespace_threshold_pct
    threshold = validation_config['whitespace_threshold_pct']
    if not isinstance(threshold, (int, float)):
        raise ConfigurationError(
            f"validation.whitespace_threshold_pct must be between 0 and 100, got: {threshold}"
        )
    

    # Check max_duplicate_pct
    max_dup = validation_config['max_duplicate_pct']
    if not isinstance(max_dup, (int, float)):
        raise ConfigurationError(
            f"validation.max_duplicate_pct must be a number, got: {type(max_dup).__name__}"

        )
    
    # Check max_missing_pct
    max_missing = validation_config['max_missing_pct']
    if not isinstance(max_missing, (int, float)):
        raise ConfigurationError(
            f"validation.max_missing_pct must be a number, got: {type(max_missing).__name__})"

        )
    if max_missing < 0 or max_missing > 100:
        raise ConfigurationError(
            f"validation.max_missing_pct must be between 0 and 100, got: {max_missing}"
        )
    



def _validate_logging_section(logging_config: Dict[str, Any]) -> None:
    """
    Validate the 'logging section of config'
    """

    # Check log levels is valid
    valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    level = logging_config['level'].upper()


    if level not in valid_levels:
        raise ConfigurationError(
            f"logging.level must be one of {valid_levels}, got: '{logging_config['level']}'"

        )
    
    # Check log_to_file is boolean
    log_to_file = logging_config['log_to_file']
    if not isinstance(log_to_file, bool):
        raise ConfigurationError(
            f"logging.log_to_file must be true or false, got: {log_to_file}"
        )
    

def get_validation_thresholds(config: Dict[str, Any]) -> Dict[str, float]:
    """
    Extract validation thresholds from config.

    Helper function to get all validation thresholds at once.
    Makes calling code cleaner.

    Args:
        congig: Configuration dictionary

    Returns:
        Dictionary with thresholds values
    
    """
    return {
        'whitespace_threshold_pct': config['validation']['whitespace_threshold_pct'],
        'max_duplicate_pct': config['validation']['max_duplicate_pct'],
        'max_missing_pct': config['validation']['max_missing_pct']
    }



    



