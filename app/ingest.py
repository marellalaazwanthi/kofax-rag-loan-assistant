
from app.models import LoanApplication


def save_application(db, data: dict):
    existing = db.query(LoanApplication).filter(
        LoanApplication.application_id == data["application_id"]
    ).first()

    documents = ", ".join(data["documents_submitted"])

    if existing:
        existing.customer_name = data["customer_name"]
        existing.ssn_last4 = data["ssn_last4"]
        existing.annual_income = data["annual_income"]
        existing.loan_amount_requested = data["loan_amount_requested"]
        existing.employment_status = data["employment_status"]
        existing.credit_score = data["credit_score"]
        existing.documents_submitted = documents
        db.commit()
        db.refresh(existing)
        return existing

    row = LoanApplication(
        application_id=data["application_id"],
        customer_name=data["customer_name"],
        ssn_last4=data["ssn_last4"],
        annual_income=data["annual_income"],
        loan_amount_requested=data["loan_amount_requested"],
        employment_status=data["employment_status"],
        credit_score=data["credit_score"],
        documents_submitted=documents,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
