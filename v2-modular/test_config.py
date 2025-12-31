

from config import load_config

# Try to load config
try:
    config = load_config()
    print(" Config loaded successfully!")
    print(f"Whitespace threshold: {config['validation']['whitespace_threshold_pct']}%")
    print(f"Output directory: {config['output']['directory']}")
    print(f"Log level: {config['logging']['level']}")
except Exception as e:
    print(f"x Config loading failed: {e}")


    