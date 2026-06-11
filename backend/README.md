# PRE Comparison Backend

FastAPI-based REST API for the Package Runnability Explorer (PRE) comparison tool.

## Setup

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

## Environment

Copy `.env.example` to `.env` and update values:

```
DATABASE_URL=postgresql://user:password@host:5432/database
AZURE_STORAGE_CONNECTION_STRING=...
SECRET_KEY=your-secret-key
```

## Tech Stack

- **FastAPI** — Web framework
- **SQLAlchemy** — ORM
- **PostgreSQL** — Database
- **pythonocc-core** — CAD file parsing
- **reportlab** — PDF generation
- **Azure Storage** — File uploads

## Project Structure

```
app/
  ├── models/      # Database models
  ├── schemas/     # Pydantic schemas
  ├── api/         # Route handlers
  ├── services/    # Business logic
  ├── dependencies/# Dependency injection
  ├── utils/       # Utilities
  └── middleware/  # Middleware
tests/            # Unit & integration tests
main.py           # Entry point
```

## Development

```bash
pip install -r requirements-dev.txt
pytest              # Run tests
black app/          # Format code
flake8 app/         # Lint
```
