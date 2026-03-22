# Migration Roadmap — Stylish AI

## Phase 1: Foundation (Day 1-2)
- [ ] Create FastAPI app entrypoint and migrate Flask routes to async routers.
- [ ] Add Pydantic schemas for request/response validation.
- [ ] Add CORS middleware and structured logging.
- [ ] Replace static catalog access with SQLite + async SQLAlchemy models.
- [ ] Create and run `seed.py` to populate clothing data.

## Phase 2: AI Upgrade (Day 3-4)
- [ ] Implement `AIService` class for Try-On Diffusion calls.
- [ ] Add tenacity retry with exponential backoff and detailed timing logs.
- [ ] Add Redis cache with in-memory fallback.
- [ ] Add request queue control for concurrent try-on generation.
- [ ] Add style recommender using sentence-transformers + cosine similarity.
- [ ] Add outfit description generator fallback service (OpenAI/Ollama pluggable).
- [ ] Add body measurement estimator endpoint using OpenCV heuristic.

## Phase 3: Auth & DB (Day 5)
- [ ] Add `User` ORM model and profile fields (measurements/avatar).
- [ ] Implement `/auth/register` and `/auth/login` with JWT.
- [ ] Hash passwords with passlib and verify through login flow.
- [ ] Gate protected AI endpoints with bearer auth dependency.

## Phase 4: Testing & Deploy (Day 6-7)
- [ ] Add pytest + pytest-asyncio setup.
- [ ] Add unit tests for AI service and clothing CRUD.
- [ ] Add integration test for `/api/tryon` endpoint.
- [ ] Dockerize with `Dockerfile` + `docker-compose.yml` including Redis.
- [ ] Add `/health` and `/metrics` endpoints for operations monitoring.
- [ ] Finalize README for deployment on Render/Railway/Fly.io free tier.
