import sys
import asyncio

# Windows fix: Playwright needs to spawn a subprocess (the browser process),
# which the default SelectorEventLoop on Windows doesn't support.
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.config import settings
from app.database import Base, engine, SessionLocal
from app.models.persona import Persona
from app.agent.personas import PERSONAS
from app.api import routes_personas, routes_sessions, routes_runs

app = FastAPI(title="Ghost User API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_personas.router)
app.include_router(routes_sessions.router)
app.include_router(routes_runs.router)

os.makedirs("screenshots", exist_ok=True)
app.mount("/screenshots", StaticFiles(directory="screenshots"), name="screenshots")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        for p in PERSONAS:
            if not db.query(Persona).filter(Persona.id == p["id"]).first():
                db.add(Persona(**p))
        db.commit()
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}