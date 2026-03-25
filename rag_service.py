
from typing import Any

from app.config import OPENAI_API_KEY, USE_OPENAI, MODEL_NAME
from app.utils import income_threshold, missing_items

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None


BASE_REQUIRED_DOCS = ["loan_application_form", "drivers_license", "income_proof"]


def evaluate_application(application: dict[str, Any]) -> dict[str, Any]:
    annual_income = float(application["annual_income"])
    loan_amount = float(application["loan_amount_requested"])
    credit_score = int(application["credit_score"])
    employment_status = application["employment_status"].strip().lower()
    documents = application["documents_submitted"]

    reasons: list[str] = []
    manual_review_reasons: list[str] = []

    if credit_score < 650:
        reasons.append("credit score is below the minimum required score of 650")

    if annual_income < income_threshold(loan_amount):
        reasons.append("annual income does not meet the 1.5x requested loan amount rule")

    if employment_status == "contract":
        manual_review_reasons.append("contract employment requires additional verification")

    required_docs = list(BASE_REQUIRED_DOCS)
    if loan_amount > 25000:
        required_docs.append("bank_statement")

    missing_docs = missing_items(required_docs, documents)

    if "income_proof" in [doc.lower() for doc in missing_docs]:
        manual_review_reasons.append("income proof is missing")
    if "drivers_license" in [doc.lower() for doc in missing_docs]:
        manual_review_reasons.append("identity proof is missing")
    if missing_docs:
        manual_review_reasons.append("some required documents are missing")

    if 620 <= credit_score <= 649:
        manual_review_reasons.append("credit score is in borderline manual review range")

    auto_reject = (
        "credit score is below the minimum required score of 650" in reasons
        and "annual income does not meet the 1.5x requested loan amount rule" in reasons
    )

    likely_status = "approved"
    if auto_reject:
        likely_status = "rejected"
    elif reasons or manual_review_reasons:
        likely_status = "manual_review"

    return {
        "status": likely_status,
        "reasons": reasons,
        "manual_review_reasons": manual_review_reasons,
        "missing_documents": missing_docs,
        "required_income": income_threshold(loan_amount),
    }


def _build_rule_based_answer(question: str, application: dict[str, Any], policy_text: str) -> str:
    q = question.lower()
    evaluation = evaluate_application(application)

    if "reject" in q or "rejected" in q or "why" in q:
        if evaluation["status"] == "rejected":
            items = evaluation["reasons"] + evaluation["manual_review_reasons"]
            return "Application likely failed because " + ", and ".join(items) + "."
        if evaluation["status"] == "manual_review":
            details = evaluation["reasons"] + evaluation["manual_review_reasons"]
            return "Application may not be auto-approved. It likely requires manual review because " + ", and ".join(details) + "."
        return "Application looks eligible based on the current policy and extracted details."

    if "missing" in q and "document" in q:
        missing = evaluation["missing_documents"]
        if not missing:
            return "No required documents appear to be missing."
        return "Missing required documents: " + ", ".join(missing) + "."

    if "manual review" in q:
        reasons = evaluation["manual_review_reasons"]
        if not reasons:
            return "This application does not appear to require manual review."
        return "Manual review is likely needed because " + ", and ".join(reasons) + "."

    if "income" in q and "required" in q:
        return (
            f"Required income for this requested loan amount is {evaluation['required_income']:.2f}. "
            f"Applicant income is {float(application['annual_income']):.2f}."
        )

    if "credit" in q:
        return (
            f"Applicant credit score is {int(application['credit_score'])}. "
            "Minimum required credit score under the policy is 650."
        )

    if "status" in q or "decision" in q:
        return f"Likely application decision is: {evaluation['status']}."

    return (
        "Based on the retrieved application details and policy, "
        f"the likely status is {evaluation['status']}. "
        f"Reasons: {', '.join(evaluation['reasons'] + evaluation['manual_review_reasons']) or 'none'}."
    )


def _build_openai_answer(question: str, application_context: str, policy_text: str) -> str:
    if not USE_OPENAI or not OPENAI_API_KEY or OpenAI is None:
        raise RuntimeError("OpenAI integration is not enabled.")

    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"""
You are a banking loan-assistant system.
Answer only from the supplied application context and policy text.
Do not hallucinate.

Question:
{question}

Application Context:
{application_context}

Policy Text:
{policy_text}
"""

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )
    return response.output_text.strip()


def build_answer(
    question: str,
    application: dict[str, Any],
    application_context: str,
    policy_text: str,
) -> str:
    if USE_OPENAI and OPENAI_API_KEY:
        try:
            return _build_openai_answer(question, application_context, policy_text)
        except Exception:
            pass

    return _build_rule_based_answer(question, application, policy_text)
