# CSV Health Tracker

A command-line tool that validates CSV files for data quality issues before they enter a data pipeline.

## What it does

- Detects missing values, duplicate rows, and whitespace pollution
- Compares findings against configurable thresholds
- Generates a detailed health report on pass, or a log entry on fail
- Exits with a clear error message and actionable suggestions

## Project Structure
```
csv-health-tracker/
├── v1-simple-script/    # Original single-file prototype
└── v2-modular/          # Production refactor with modular architecture
    ├── main.py          # Entry point, CLI interface
    ├── config.py        # Configuration loader
    ├── config.yaml      # Thresholds and settings
    ├── logger.py        # Logging setup
    ├── exceptions.py    # Custom exception hierarchy
    ├── validation.py    # Core validation logic
    ├── report.py        # Report generation
    └── requirements.txt # Dependencies
```

## How to run locally

### Plain Python
```
cd v2-modular
pip install -r requirements.txt
python main.py your_file.csv
```

### Docker
```
docker build -t csv-health-tracker .
docker run --rm -v "%cd%":/app/data -v "%cd%/output":/app/output -v "%cd%/logs":/app/logs csv-health-tracker python main.py data/your_file.csv
```

## Output

- **Pass**: report saved to `output/health_report_<filename>_<timestamp>.txt`
- **Fail**: error logged to `logs/csv_health_tracker.log`

## GCP Deployment

Image is stored in Artifact Registry (europe-west3) and deployed as a Cloud Run Job.
```
gcloud run jobs execute csv-health-tracker-job --region=europe-west3 --wait
```

## Planned improvements

- V3: Google Cloud Storage integration for cloud-native file handling
- V3: FastAPI wrapper for HTTP-based CSV submission