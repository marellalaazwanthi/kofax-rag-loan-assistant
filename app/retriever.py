
from app.models import LoanApplication
from app.utils import parse_documents


def read_policy_text(policy_path: str) -> str:
    with open(policy_path, "r", encoding="utf-8") as f:
        return f.read()


def get_application(db, application_id: str):
    return db.query(LoanApplication).filter(
        LoanApplication.application_id == application_id
    ).first()


def get_application_context(db, application_id: str) -> str:
    app_row = get_application(db, application_id)
    if not app_row:
        return ""

    return f"""
Application ID: {app_row.application_id}
Customer Name: {app_row.customer_name}
Income: {app_row.annual_income}
Loan Amount Requested: {app_row.loan_amount_requested}
Employment Status: {app_row.employment_status}
Credit Score: {app_row.credit_score}
Documents Submitted: {app_row.documents_submitted}
""".strip()


def get_application_payload(db, application_id: str) -> dict | None:
    app_row = get_application(db, application_id)
    if not app_row:
        return None

    return {
        "application_id": app_row.application_id,
        "customer_name": app_row.customer_name,
        "annual_income": float(app_row.annual_income),
        "loan_amount_requested": float(app_row.loan_amount_requested),
        "employment_status": app_row.employment_status,
        "credit_score": int(app_row.credit_score),
        "documents_submitted": parse_documents(app_row.documents_submitted),
    }
