import uuid

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, JSON, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Step(Base):
    """
    A single observe -> decide -> act cycle within a session.
    Stored in order so the frontend can replay a run step by step.
    """

    __tablename__ = "steps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)

    step_number = Column(Integer, nullable=False)

    # click | type | scroll | wait | report_issue | done
    action_type = Column(String, nullable=False)
    action_payload = Column(JSON, nullable=True)  # e.g. {"selector": "...", "text": "..."}

    reasoning = Column(Text, nullable=True)  # the LLM's stated reason for this action
    observation_summary = Column(Text, nullable=True)  # brief note on what the agent "saw"

    screenshot_path = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("Session", back_populates="steps")