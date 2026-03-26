
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import Base, engine, get_db
from app.kofax_adapter import load_kofax_json
from app.ingest import save_application
from app.retriever import (
    read_policy_text,
    get_application_context,
    get_application_payload,
)
from app.rag_service import build_answer
from app.schemas import AskRequest, AskResponse, LoadFileRequest, ApplicationResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kofax RAG Loan Assistant", version="1.0.0")

POLICY_PATH = "data/policy_docs/loan_policy.txt"
KOFAX_SAMPLE_PATH = "data/sample_kofax_json/application_1001.json"


@app.get("/")
def health():
    return {"status": "ok", "service": "kofax-rag-loan-assistant"}


@app.post("/load-sample")
def load_sample(db: Session = Depends(get_db)):
    data = load_kofax_json(KOFAX_SAMPLE_PATH)
    row = save_application(db, data)
    return {"message": "Sample application loaded", "application_id": row.application_id}


@app.post("/load-from-file")
def load_from_file(payload: LoadFileRequest, db: Session = Depends(get_db)):
    try:
        data = load_kofax_json(payload.file_path)
        row = save_application(db, data)
        return {"message": "Application loaded", "application_id": row.application_id}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/applications/{application_id}", response_model=ApplicationResponse)
def get_application(application_id: str, db: Session = Depends(get_db)):
    payload = get_application_payload(db, application_id)
    if not payload:
        raise HTTPException(status_code=404, detail="Application not found")
    return payload


@app.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest, db: Session = Depends(get_db)):
    policy_text = read_policy_text(POLICY_PATH)
    application_context = get_application_context(db, payload.application_id)
    application = get_application_payload(db, payload.application_id)

    if not application_context or not application:
        raise HTTPException(status_code=404, detail="Application not found")

    answer = build_answer(
        question=payload.question,
        application=application,
        application_context=application_context,
        policy_text=policy_text,
    )

    return AskResponse(
        application_id=payload.application_id,
        answer=answer,
    )
