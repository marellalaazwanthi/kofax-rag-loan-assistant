
from typing import Iterable


def parse_documents(documents_csv: str) -> list[str]:
    if not documents_csv.strip():
        return []
    return [item.strip() for item in documents_csv.split(",") if item.strip()]


def missing_items(required: Iterable[str], available: Iterable[str]) -> list[str]:
    available_set = {item.strip().lower() for item in available}
    return [item for item in required if item.lower() not in available_set]


def income_threshold(loan_amount: float) -> float:
    return loan_amount * 1.5
