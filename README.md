# Ghost User

A synthetic user simulator for testing apps. AI agents with different personas
(impatient, confused first-timer, power user) browse your app, take actions,
hit friction, and report what went wrong — before real users do.

## Stack
- Frontend: React + Vite + Tailwind CSS + Framer Motion
- Backend: FastAPI
- DB: PostgreSQL + SQLAlchemy
- Browser automation: Playwright
- LLM: Groq API (Llama 3.3 70B, tool-calling)

## Structure
- `backend/` — FastAPI app, agent loop, Playwright driver, DB models
- `frontend/` — React dashboard (Ghost User UI)
- `demo-app/` — small intentionally-flawed app used as the "app under test"
- `docs/` — architecture notes

## Setup
See `backend/README` and `frontend/README` sections (added as we build).
