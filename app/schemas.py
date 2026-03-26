
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    application_id: str = Field(..., examples=["APP1001"])
    question: str = Field(..., examples=["Why was this application rejected?"])


class AskResponse(BaseModel):
    application_id: str
    answer: str


class LoadFileRequest(BaseModel):
    file_path: str


class ApplicationResponse(BaseModel):
    application_id: str
    customer_name: str
    annual_income: float
    loan_amount_requested: float
    employment_status: str
    credit_score: int
    documents_submitted: list[str]
