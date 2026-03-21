"""
API Module - CSV Health Tracker

FastAPI interface for the CSV Health Tracker.
Exposes the validation logic over HTTP so anyone
can submit a CSV file and receive a health report.

This is a separate entry point from main.py.
The validation logic underneath is identical.
"""

import tempfile
import json
from pathlib import Path

import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from config import load_config
from logger import get_logger_from_config
from validation import validate_csv
from exceptions import CSVHealthTrackerError


class NumpyEncoder(json.JSONEncoder):
    """Converts numpy types to JSON serializable Python types."""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# Initialize FastAPI app
app = FastAPI(
    title="CSV Health Tracker",
    description="Validates CSV files for data quality issues",
    version="2.0"
)

# Load config and logger once at startup
config = load_config()
logger = get_logger_from_config(config)


@app.get("/")
def health_check():
    """
    Health check endpoint.
    Returns running status of the service.
    """
    return {"status": "running", "service": "CSV Health Tracker v2.0"}


@app.post("/validate")
async def validate(file: UploadFile = File(...)):
    """
    Validate a CSV file for data quality issues.
    Accepts a CSV file upload and returns validation results.
    """

    # Check file is a CSV
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are accepted"
        )

    logger.info(f"Received file: {file.filename}")

    # Save uploaded file to a temp location
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".csv"
    ) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = Path(tmp.name)

    # Run validation
    try:
        results = validate_csv(tmp_path, logger, config)

        return JSONResponse(content=json.loads(
            json.dumps({
                "status": "passed",
                "filename": file.filename,
                "rows": results["basic_info"]["shape"][0],
                "columns": results["basic_info"]["shape"][1],
                "checks": {
                    "duplicates": results["duplicates"],
                    "missing_values": results["missing_values"],
                    "whitespace": results["whitespace"]
                }
            }, cls=NumpyEncoder)
        ))

    except CSVHealthTrackerError as e:
        return JSONResponse(
            status_code=422,
            content={
                "status": "failed",
                "filename": file.filename,
                "error": str(e)
            }
        )

    finally:
        # Always clean up the temp file
        tmp_path.unlink(missing_ok=True)