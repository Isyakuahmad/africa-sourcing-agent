# Africa Sourcing Agent

A free-first starter application for organising buyer requirements, supplier information, and evidence-led commodity sourcing workflows.

> **Important:** Demo records are fictional. This project does not verify suppliers, guarantee prices or stock, or execute transactions. Validate supplier identities, certificates, prices, and availability independently.

## Current foundation

- FastAPI application with a homepage, health endpoint, and interactive API documentation.
- SQLAlchemy models for buyer requests and suppliers.
- SQLite by default; DATABASE_URL can be configured for another SQLAlchemy-supported database.
- Rule-based supplier matching/report helpers.
- Automated tests and GitHub Actions CI.

## Run locally

Requires Python 3.11 or newer.

### Windows PowerShell

    py -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
    Copy-Item .env.example .env
    uvicorn app.main:app --reload

### macOS / Linux

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    cp .env.example .env
    uvicorn app.main:app --reload

Open http://127.0.0.1:8000, health check http://127.0.0.1:8000/health, and API docs http://127.0.0.1:8000/docs.

The database file is created under data/ by default. Keep .env and real supplier/buyer data private; never commit credentials.

## Run tests

    pytest -q

Tests run automatically on pushes and pull requests through GitHub Actions.

## Configuration

Copy .env.example to .env and adjust only as needed:

- APP_NAME: display name.
- APP_ENV: use development locally; production requires a strong SECRET_KEY.
- DATABASE_URL: defaults to a local SQLite database.
- OPENAI_API_KEY: optional; AI features are not yet connected to a real model API.

## Development status

This is an early foundation, not a production-ready procurement system. Before handling real customer information, add authentication/authorisation, CSRF protection for form actions, audit logging, database migrations, backups, and rate limiting. Require human approval for supplier outreach and commercial commitments.
