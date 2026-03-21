# CSV Health Tracker

A command-line tool that validates CSV files for data quality issues before they enter a data pipeline. Non-destructive — reports problems without modifying source data.

---

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

---

## What it does

- Validates file path, extension, and accessibility
- Detects missing values, duplicate rows, and whitespace pollution
- Compares findings against configurable thresholds
- Generates a detailed health report on pass, or a log entry on fail
- Exits with a clear error message and actionable suggestions

---

## How to run locally

### Plain Python
```
cd v2-modular
pip install -r requirements.txt
python main.py your_file.csv
```

### Docker
```
cd v2-modular
docker build -t csv-health-tracker .
docker run --rm -v "%cd%":/app/data -v "%cd%/output":/app/output -v "%cd%/logs":/app/logs csv-health-tracker python main.py data/your_file.csv
```

---

## Output

- **Pass**: report saved to `output/health_report_<filename>_<timestamp>.txt`
- **Fail**: error logged to `logs/csv_health_tracker.log`

---
## GCP Deployment

Image is stored in Artifact Registry (europe-west3) and deployed as a Cloud Run Service.

**Live URL**: https://csv-health-tracker-127482995435.europe-west3.run.app

**Interactive API docs**: https://csv-health-tracker-127482995435.europe-west3.run.app/docs

To redeploy:
```
gcloud run deploy csv-health-tracker --image=europe-west3-docker.pkg.dev/csv-health-tracker/csv-health-tracker-repo/csv-health-tracker:v2 --region=europe-west3 --platform=managed --allow-unauthenticated --port=8080
```


---

## What I learned

### V1
- Migrating from `os.path` to `pathlib` for modern path handling
- Defensive programming patterns (guard clauses, fail-fast validation)
- Pandas data inspection methods
- Input validation and user-friendly error messaging

### V2
- Modular architecture — separation of concerns across config, logging, validation, reporting
- Custom exception hierarchies
- Configurable thresholds via YAML
- Production logging patterns
- Docker — writing Dockerfiles, building images, volume mounts
- GCP — Artifact Registry, Cloud Run Jobs, gcloud CLI

---

## Future improvements

- GCS integration for storing validation reports in the cloud
- Authentication layer for the API
- Support for larger file uploads