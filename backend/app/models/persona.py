from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class Persona(Base):
    """
    A synthetic user archetype (e.g. "impatient", "confused_first_timer").
    Personas are seeded once and reused across many sessions.
    """

    __tablename__ = "personas"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # e.g. "Tech Comfort", "Age & Life Stage"
    description = Column(Text, nullable=False)
    system_prompt = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sessions = relationship("Session", back_populates="persona")