
import json
from pathlib import Path


def load_kofax_json(file_path: str) -> dict:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Kofax JSON file not found: {file_path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    required_fields = {
        "application_id",
        "customer_name",
        "ssn_last4",
        "annual_income",
        "loan_amount_requested",
        "employment_status",
        "credit_score",
        "documents_submitted",
    }

    missing = required_fields - set(data.keys())
    if missing:
        raise ValueError(f"Missing required fields in Kofax JSON: {sorted(missing)}")

    if not isinstance(data["documents_submitted"], list):
        raise ValueError("documents_submitted must be a list")

    return data
