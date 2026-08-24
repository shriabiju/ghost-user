import uuid

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Session(Base):
    """
    A single agent run: one persona pursuing one goal against the target app.
    """

    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    persona_id = Column(String, ForeignKey("personas.id"), nullable=False)

    target_url = Column(String, nullable=False)
    goal = Column(Text, nullable=False)  # e.g. "Complete checkout for one item"

    # pending -> running -> completed | failed
    status = Column(String, nullable=False, default="pending")

    total_steps = Column(Integer, nullable=False, default=0)

    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    persona = relationship("Persona", back_populates="sessions")
    steps = relationship(
        "Step", back_populates="session", order_by="Step.step_number", cascade="all, delete-orphan"
    )
    finding = relationship(
        "Finding", back_populates="session", uselist=False, cascade="all, delete-orphan"
    )