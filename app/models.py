
from sqlalchemy import Column, Integer, String, Float, Text
from app.db import Base


class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(String, unique=True, nullable=False, index=True)
    customer_name = Column(String, nullable=False)
    ssn_last4 = Column(String, nullable=False)
    annual_income = Column(Float, nullable=False)
    loan_amount_requested = Column(Float, nullable=False)
    employment_status = Column(String, nullable=False)
    credit_score = Column(Integer, nullable=False)
    documents_submitted = Column(Text, nullable=False)
