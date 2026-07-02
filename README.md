# CSV Health Tracker

> Validate CSV quality before it reaches your pipeline — not after it breaks something.

`Python` · `FastAPI` · `Docker` · `GCP Cloud Run`

## Overview

Bad data reaching a pipeline is expensive to debug. By the time it breaks something, the cause is usually far from the symptom. CSV Health Tracker runs a configurable validation pass over any CSV file and catches the common problems — missing values, duplicate rows, whitespace pollution — before they move downstream. It never touches the source data; it only reports on it.

This was the first project in a deliberate MLOps sprint. It started as a single-file script and grew into a modular, containerised service deployed on GCP Cloud Run with CI/CD. The problem is small on purpose. The point wasn't the problem — it was to practice production patterns on something I could fully control.

## Architecture: v1 → v2

The codebase keeps two versions side by side, on purpose.

- `v1-simple-script/` — the single-file prototype. Useful mostly as a record of what the refactor was reacting against.
- `v2-modular/` — the production refactor, with concerns separated out:

| File | Responsibility |
|------|----------------|
| `main.py` | CLI entry point |
| `validation.py` | Core check logic |
| `report.py` | Report generation |
| `config.py` + `config.yaml` | Threshold configuration, decoupled from logic |
| `logger.py` + `exceptions.py` | Structured logging, custom exception hierarchy |

Keeping v1 next to v2 was deliberate: the diff shows the architectural reasoning more clearly than any comment could.

## What it validates

- File path, extension, and read accessibility
- Missing values — per column and overall
- Duplicate rows
- Whitespace pollution — leading/trailing spaces in string fields

Every threshold lives in `config.yaml`. There are no hardcoded limits — changing how strict the checks are needs no code change and no redeployment.

## What a real run looks like

Run against the full SBA 7(a) loan dataset (545,751 rows, 43 columns), the tool passes the duplicate check but flags several columns that are mostly empty:

```
INFO  - CSV loaded successfully: 545751 rows, 43 columns
INFO  - Checking for duplicate rows...
INFO  - Found 1136 duplicate rows (0.21%)
INFO  - Duplicate rows check PASSED: 0.21% <= 5%
INFO  - Checking for missing values...
ERROR - Missing values exceeded threshold (30%):
        bankncuanumber : 96.87%
        franchisecode  : 91.29%
        franchisename   : 91.31%
        chargeoffdate   : 93.17%
        soldsecmrktind  : 76.55%
```

On a clean file, the run ends with a full pass report written to `output/` instead.

## Running it (CLI)

The command line is the primary interface.

**Plain Python**
```bash
cd v2-modular
pip install -r requirements.txt
python main.py your_file.csv
```

**Docker**
```bash
cd v2-modular
docker build -t csv-health-tracker .

# macOS / Linux
docker run --rm \
  -v "$(pwd)":/app/data \
  -v "$(pwd)/output":/app/output \
  -v "$(pwd)/logs":/app/logs \
  csv-health-tracker python main.py data/your_file.csv

# Windows (CMD): replace $(pwd) with %cd%
```

**Output**
- Pass → a detailed report at `output/health_report_<filename>_<timestamp>.txt`
- Fail → a structured entry in `logs/csv_health_tracker.log`

## Tests

Each module has its own test file, run with `pytest`.

```bash
cd v2-modular
pytest -v
```

```
test_exceptions.py   3 passed   — exception hierarchy, specific handling, logging
test_logger.py       3 passed   — setup, config, log levels
test_report.py       5 passed   — generation, saving, end-to-end, reports with issues
test_validation.py   5 passed   — file path, clean CSV, duplicates, missing values, whitespace
================================================================
16 passed
```

The validation tests are the ones that matter most: each check has a fixture that deliberately triggers it, so a broken check fails loudly instead of silently passing bad data.

## Same logic, deployed

The exact validation logic is also exposed as a hosted service on GCP Cloud Run, so you can check a file without cloning anything.

**Live API docs:** https://csv-health-tracker-127482995435.europe-west3.run.app/docs

`POST /validate` takes a CSV upload and returns the results as JSON:

```bash
curl -X POST 'https://csv-health-tracker-127482995435.europe-west3.run.app/validate' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_file.csv;type=text/csv'
```

```jsonc
{
  "status": "passed",
  "filename": "landtempssample.csv",
  "rows": 100000,
  "columns": 10,
  "checks": {
    "duplicates": { "count": 0, "percentage": 0 },
    "missing_values": {          // values are % missing per column
      "temp": 14.446,
      "country": 0.005,
      "latitude": 0,
      "longitude": 0
    },
    "whitespace": { }
  }
}
```

The image is stored in Artifact Registry (`europe-west3`) and served from Cloud Run:

```bash
gcloud run deploy csv-health-tracker \
  --image=europe-west3-docker.pkg.dev/csv-health-tracker/csv-health-tracker-repo/csv-health-tracker:v2 \
  --region=europe-west3 --platform=managed \
  --allow-unauthenticated --port=8080
```

## Design decisions worth noting

- **Thresholds live in YAML, not code.** Changing validation strictness needs no code change and no redeployment.
- **Custom exception hierarchy.** Validation failures and I/O errors surface with distinct, actionable messages instead of a generic traceback.
- **v1 is kept alongside v2.** The comparison carries the reasoning better than documentation would.

## Planned improvements

- GCS integration for cloud-persisted reports
- An auth layer on the API endpoint
- Streaming validation, to support larger uploads