import uuid

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Finding(Base):
    """
    The post-session, LLM-generated UX report for a session.
    One finding per session.
    """

    __tablename__ = "findings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False, unique=True)

    summary = Column(Text, nullable=False)  # plain-English headline finding
    # list of {"step_number": int, "issue": str, "severity": "low"|"medium"|"high"}
    issues = Column(JSON, nullable=False, default=list)

    outcome = Column(String, nullable=False)  # "goal_completed" | "abandoned" | "blocked"

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("Session", back_populates="finding")