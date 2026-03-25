
# Architecture

## End-to-end flow

1. Customer uploads loan application and supporting documents.
2. Kofax extracts structured fields from the scanned documents.
3. Application JSON is sent to this service.
4. Service stores extracted data in PostgreSQL.
5. RAG layer retrieves:
   - application details
   - policy rules
   - document checklist rules
6. Answer generation service returns business explanation.

## Logical architecture

```text
User / Ops / Underwriter
        |
        v
    FastAPI Service
        |
        +--> PostgreSQL (loan application data)
        |
        +--> Policy Documents (knowledge source)
        |
        +--> RAG Service
                |
                +--> Rule-based engine
                +--> Optional LLM
```

## Where mainframe can fit in later

In a real banking system, this demo can be extended so that after ingestion:
- customer history is fetched from DB2
- delinquency details come from mainframe APIs
- fraud flags are retrieved from another system
- application status is synchronized with workflow engine
