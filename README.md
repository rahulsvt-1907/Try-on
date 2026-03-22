# Stylish AI — FastAPI Edition

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-async-success)
![Docker](https://img.shields.io/badge/deploy-docker-informational)
![Tests](https://img.shields.io/badge/tests-pytest-green)

A portfolio-ready AI virtual fashion try-on app migrated from Flask to FastAPI with async SQLAlchemy, JWT auth, HTMX+Jinja, and an AI service layer.

## Stack
- FastAPI + Pydantic + async SQLAlchemy 2.0
- SQLite + optional Redis cache
- HTMX + Alpine.js + TailwindCSS
- Tenacity retry, Loguru structured logs
- AI extras: recommender, style-description generation, measurement estimator

## Project structure
```text
app/
  core/        # config + logging
  db/          # async engine/session
  models/      # SQLAlchemy ORM
  routers/     # auth, clothing, try-on, pages
  schemas/     # Pydantic contracts
  services/    # AI, cache, auth, recommender, CV
main.py
seed.py
templates/
tests/
```

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python seed.py
uvicorn main:app --reload
```

Docs: `http://localhost:8000/docs`

## Docker
```bash
docker compose up --build
```

## Migration guide (old Flask -> new FastAPI)
1. **Delete/retire**: `app.py` Flask entrypoint, old localStorage-only profile logic in templates/static JS.
2. **Create**: `main.py`, `app/{routers,models,schemas,services,db,core}`.
3. **Create DB models**: `ClothingItem`, `User`; run `python seed.py`.
4. **Replace JS interactions**: use HTMX requests for catalog filtering and Alpine.js for try-on UX state.
5. **Add auth**: use `/auth/register` + `/auth/login`, store JWT and pass bearer token to `/api/tryon`.
6. **Add ops**: `/health`, `/metrics`, Docker + compose.

## Testing
```bash
pytest -q
```
