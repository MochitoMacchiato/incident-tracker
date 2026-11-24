# Incident Tracker

FastAPI + PostgreSQL incident API (work in progress).

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Docs page: http://127.0.0.1:8000/docs

![API docs](docs/api-docs.png)

## Running tests

The tests use a separate PostgreSQL database so your real data is never touched.

### One-time setup

1. Create the test database (the name must end in `_test`):

   ```bash
   sudo -u postgres psql -c "CREATE DATABASE incident_tracker_test OWNER incident_app;"
   ```

2. Create and activate a virtual environment, then install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

### Each new terminal

```bash
source .venv/bin/activate
export TEST_DATABASE_URL="postgresql+psycopg2://incident_app:<your-password>@localhost:5432/incident_tracker_test"
```

Replace `<your-password>` with your own. Never commit it.

### Run

From the repository root:

```bash
python -m pytest tests/ -v
```

### Notes

- Each test starts with fresh, empty tables. The fixture in `tests/conftest.py` drops and recreates them, then inserts one service (`id 1`).
- `conftest.py` refuses to run if the database name does not end in `_test`.
- Run pytest from the repo root. Running it from inside `tests/` causes `ModuleNotFoundError: No module named 'app'`.