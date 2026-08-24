"""
Kicks off a new agent run. The session is created immediately (status
"pending") so the frontend can navigate to a live-run view right away,
and the actual browser/agent work happens in a background task.
"""

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session as DBSession

from app.database import get_db, SessionLocal
from app.models.session import Session as SessionModel
from app.models.persona import Persona
from app.schemas.session import SessionCreate, SessionOut
from app.agent.loop import run_session

router = APIRouter(prefix="/runs", tags=["runs"])


async def _execute_run(session_id: str):
    """Runs in the background with its own DB session, independent of the request."""
    db = SessionLocal()
    try:
        session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if session:
            await run_session(db, session)
    finally:
        db.close()


@router.post("", response_model=SessionOut)
def start_run(payload: SessionCreate, background_tasks: BackgroundTasks, db: DBSession = Depends(get_db)):
    persona = db.query(Persona).filter(Persona.id == payload.persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Unknown persona")

    session = SessionModel(
        persona_id=payload.persona_id,
        target_url=payload.target_url,
        goal=payload.goal,
        status="pending",
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    background_tasks.add_task(_execute_run, str(session.id))

    return session