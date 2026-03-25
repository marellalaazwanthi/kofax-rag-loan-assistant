
from app.rag_service import evaluate_application, build_answer


def test_evaluate_application_rejected():
    application = {
        "application_id": "APP1001",
        "customer_name": "John Smith",
        "annual_income": 42000,
        "loan_amount_requested": 30000,
        "employment_status": "Contract",
        "credit_score": 598,
        "documents_submitted": ["loan_application_form", "drivers_license", "pay_stub"],
    }

    evaluation = evaluate_application(application)
    assert evaluation["status"] in {"rejected", "manual_review"}
    assert "bank_statement" in [doc.lower() for doc in evaluation["missing_documents"]]


def test_build_answer_missing_docs():
    application = {
        "application_id": "APP1001",
        "customer_name": "John Smith",
        "annual_income": 42000,
        "loan_amount_requested": 30000,
        "employment_status": "Contract",
        "credit_score": 598,
        "documents_submitted": ["loan_application_form", "drivers_license", "pay_stub"],
    }
    application_context = "dummy"
    policy_text = "dummy"

    answer = build_answer(
        question="What documents are missing?",
        application=application,
        application_context=application_context,
        policy_text=policy_text,
    )
    assert "Missing required documents" in answer
