# CSV Health Tracker

**Validate CSV quality before it reaches your pipeline — not after it breaks something.**

Bad data reaching a pipeline is expensive to debug: by the time it breaks something, the cause is far from the symptom. CSV Health Tracker runs a configurable validation pass over any CSV and catches the common problems — missing values, duplicate rows, whitespace pollution — before they move downstream. It **never touches the source data; it only reports.**

[![CI](https://github.com/kai2055/csv-health-tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/kai2055/csv-health-tracker/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Cloud Run](https://img.shields.io/badge/GCP%20Cloud%20Run-4285F4?logo=googlecloud&logoColor=white)
![YAML config](https://img.shields.io/badge/config-YAML%20thresholds-CB171E?logo=yaml&logoColor=white)
![tests](https://img.shields.io/badge/tests-16-brightgreen)

🔗 **[Live API](https://csv-health-tracker-127482995435.europe-west3.run.app/docs)** — check a file without cloning anything &nbsp;·&nbsp; 🎥 Demo *(coming)* <!-- replace with: 🎥 [Watch demo](VIDEO_URL) -->

<!-- Screenshot slot — drop a terminal-run or /docs screenshot here:
![example run](docs/img/example-run.png)
-->

> **Context:** the first project in a deliberate MLOps sprint. It started as a single-file script and grew into a modular, containerised service on Cloud Run with CI/CD. **The problem is small on purpose** — the point wasn't the problem, it was to practice production patterns on something fully controllable.

---

## What a real run catches

Run against the full SBA 7(a) loan dataset (**545,751 rows, 43 columns**), it passes the duplicate check but flags five columns that are mostly empty — the silent rot that wrecks any model trained on it:

```
INFO  - CSV loaded successfully: 545751 rows, 43 columns
INFO  - Found 1136 duplicate rows (0.21%)
INFO  - Duplicate rows check PASSED: 0.21% <= 5%
ERROR - Missing values exceeded threshold (30%):
        bankncuanumber : 96.87%
        franchisecode  : 91.29%
        franchisename  : 91.31%
        chargeoffdate  : 93.17%
        soldsecmrktind : 76.55%
```

On a clean file, the run ends with a full pass report written to `output/` instead.

---

## What it validates

- File path, extension, and read accessibility
- **Missing values** — per column and overall
- **Duplicate rows**
- **Whitespace pollution** — leading/trailing spaces in string fields

Every threshold lives in `config.yaml`. **No hardcoded limits** — changing how strict the checks are needs no code change and no redeployment.

---

## Architecture: v1 → v2

The codebase keeps two versions side by side, **on purpose** — the diff shows the architectural reasoning more clearly than any comment could.

- **`v1-simple-script/`** — the single-file prototype; a record of what the refactor was reacting against.
- **`v2-modular/`** — the production refactor, with concerns separated:

| File | Responsibility |
| --- | --- |
| `main.py` | CLI entry point |
| `validation.py` | Core check logic |
| `report.py` | Report generation |
| `config.py` + `config.yaml` | Threshold configuration, decoupled from logic |
| `logger.py` + `exceptions.py` | Structured logging, custom exception hierarchy |

**Design decisions worth noting:** thresholds live in YAML, not code · a custom exception hierarchy surfaces validation vs. I/O errors with distinct, actionable messages instead of a generic traceback · v1 is kept beside v2 because the comparison carries the reasoning better than documentation would.

---

## Running it (CLI)

The command line is the primary interface.

```bash
# Plain Python
cd v2-modular
pip install -r requirements.txt
python main.py your_file.csv
```

```bash
# Docker
cd v2-modular
docker build -t csv-health-tracker .

# macOS / Linux  (Windows CMD: replace $(pwd) with %cd%)
docker run --rm \
  -v "$(pwd)":/app/data \
  -v "$(pwd)/output":/app/output \
  -v "$(pwd)/logs":/app/logs \
  csv-health-tracker python main.py data/your_file.csv
```

**Output:** a pass writes a detailed report to `output/health_report_<filename>_<timestamp>.txt`; a fail writes a structured entry to `logs/csv_health_tracker.log`.

---

## Same logic, deployed

The exact validation logic is also a hosted service on GCP Cloud Run. `POST /validate` takes a CSV upload and returns JSON:

```bash
curl -X POST 'https://csv-health-tracker-127482995435.europe-west3.run.app/validate' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_file.csv;type=text/csv'
```

```json
{
  "status": "passed",
  "filename": "landtempssample.csv",
  "rows": 100000,
  "columns": 10,
  "checks": {
    "duplicates": { "count": 0, "percentage": 0 },
    "missing_values": { "temp": 14.446, "country": 0.005, "latitude": 0, "longitude": 0 },
    "whitespace": { }
  }
}
```

---

## Tests

Each module has its own test file. **16 tests**, run with `pytest -v`:

```
test_exceptions.py   3 passed   — exception hierarchy, specific handling, logging
test_logger.py       3 passed   — setup, config, log levels
test_report.py       5 passed   — generation, saving, end-to-end, reports with issues
test_validation.py   5 passed   — file path, clean CSV, duplicates, missing values, whitespace
============================================================  16 passed
```

The validation tests matter most: each check has a fixture that deliberately triggers it, so a broken check **fails loudly instead of silently passing bad data.**

---

## Planned improvements

- GCS integration for cloud-persisted reports
- An auth layer on the API endpoint
- Streaming validation, to support larger uploads
