
# Kofax RAG Loan Assistant

A complete demo project that simulates a **Kofax + RAG** workflow for banking loan processing.

## What this project does

1. Accepts Kofax-style extracted JSON from a scanned loan application.
2. Stores that structured data in PostgreSQL.
3. Reads business policy documents from local text files.
4. Retrieves relevant application + policy context.
5. Generates a business answer such as:
   - Why was the application rejected?
   - What rules failed?
   - Which documents are missing?
   - Does the applicant need manual review?

## Tech stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker Compose
- Rule-based RAG layer (easy to understand and interview friendly)
- Optional OpenAI support

## Project structure

```text
kofax-rag-loan-assistant/
├── README.md
├── requirements.txt
├── .gitignore
├── sample.env
├── docker-compose.yml
├── app/
├── data/
├── tests/
└── docs/
```

## Setup

### 1. Create virtual environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

On Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start PostgreSQL

```bash
docker-compose up -d
```

### 4. Create `.env`

Copy `sample.env` to `.env` and update values if needed.

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

## API endpoints

### Health check

```http
GET /
```

### Load sample Kofax application

```http
POST /load-sample
```

### Load custom Kofax JSON file already present on disk

```http
POST /load-from-file
```

Request body:
```json
{
  "file_path": "data/sample_kofax_json/application_1001.json"
}
```

### Ask a question about an application

```http
POST /ask
```

Request body:
```json
{
  "application_id": "APP1001",
  "question": "Why was this application rejected?"
}
```

## Example response

```json
{
  "application_id": "APP1001",
  "answer": "Application likely failed because credit score is below the minimum required score of 650, annual income does not meet the 1.5x requested loan amount rule, contract employment requires additional verification, and some required documents are missing."
}
```

## Swagger UI

After starting the service, open:

- http://127.0.0.1:8000/docs

## Sample interview explanation

> I built a Kofax plus RAG demo project for banking loan-processing scenarios. Kofax-style extracted JSON is ingested into PostgreSQL, policy documents are retrieved from the knowledge layer, and a RAG service combines the application context with policy rules to generate business explanations like rejection reasons, missing documents, and manual-review decisions. The system is modular, so a real Kofax feed, DB2 API, or vector database can be plugged in later.

## Future enhancements

- Replace rule-based retrieval with embeddings + vector DB
- Plug in real Kofax export
- Add DB2/mainframe API integration
- Add audit logging
- Add user authentication
- Add workflow status tracking
- Add file upload endpoint
- Add OpenAI-based answer generation
