# CSV Health Tracker

> Validate CSV quality before it reaches your pipeline — not after it breaks something.

![Python](https://img.shields.io/badge/Python-3.10-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-deployed-green) ![Docker](https://img.shields.io/badge/Docker-containerised-blue) ![GCP Cloud Run](https://img.shields.io/badge/GCP-Cloud%20Run-orange)

---

## Overview

Bad data reaching a pipeline is expensive to debug. CSV Health Tracker runs a configurable validation pass on any CSV file — catching missing values, duplicate rows, and whitespace pollution before they propagate downstream. It is non-destructive: it never modifies source data.

Built as the first project in a deliberate MLOps portfolio sprint, it evolved from a single-file script to a modular, containerised service deployed on GCP Cloud Run with CI/CD — intentionally over-engineered to practice production patterns on a small, controlled problem.

---

## Live deployment

**Interactive API docs**: https://csv-health-tracker-127482995435.europe-west3.run.app/docs

---

## Architecture: v1 → v2

The codebase has two versions, kept intentionally for comparison.

**`v1-simple-script/`** — a single-file prototype. Useful reference for what the refactor was reacting against.

**`v2-modular/`** — production refactor with separated concerns:

| File | Responsibility |
|---|---|
| `main.py` | CLI entry point |
| `validation.py` | Core check logic |
| `report.py` | Report generation |
| `config.py` + `config.yaml` | Threshold configuration, decoupled from logic |
| `logger.py` + `exceptions.py` | Structured logging, custom exception hierarchy |

---

## What it validates

- File path, extension, and read accessibility
- Missing values — by column and overall
- Duplicate rows
- Whitespace pollution (leading/trailing spaces in string fields)

All thresholds are configurable in `config.yaml` — no hardcoded limits.

---

## Output

- **Pass**: detailed report → `output/health_report_<filename>_<timestamp>.txt`
- **Fail**: structured log entry → `logs/csv_health_tracker.log`

---

## Running locally

### Plain Python

```bash
cd v2-modular
pip install -r requirements.txt
python main.py your_file.csv
```

### Docker

```bash
cd v2-modular
docker build -t csv-health-tracker .
docker run --rm \
  -v "%cd%":/app/data \
  -v "%cd%/output":/app/output \
  -v "%cd%/logs":/app/logs \
  csv-health-tracker python main.py data/your_file.csv
```

---

## Deploying to GCP

Image stored in Artifact Registry (europe-west3), served via Cloud Run.

```bash
gcloud run deploy csv-health-tracker \
  --image=europe-west3-docker.pkg.dev/csv-health-tracker/csv-health-tracker-repo/csv-health-tracker:v2 \
  --region=europe-west3 \
  --platform=managed \
  --allow-unauthenticated \
  --port=8080
```

---

## Design decisions worth noting

- **Thresholds live in YAML, not code** — changing validation strictness requires no code change and no redeployment
- **Custom exception hierarchy** — validation failures and I/O errors surface with distinct, actionable messages rather than generic exceptions
- **v1 is preserved alongside v2** — the diff shows the architectural reasoning more clearly than any comment could

---

## Planned improvements

- GCS integration for cloud-persisted reports
- Auth layer for the API endpoint
- Support for larger file uploads (streaming validation)