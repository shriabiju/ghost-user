from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator

from app.schemas.step import StepOut
from app.schemas.finding import FindingOut


class SessionCreate(BaseModel):
    persona_id: str
    target_url: str
    goal: str


class SessionOut(BaseModel):
    id: str
    persona_id: str
    target_url: str
    goal: str
    status: str
    total_steps: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    @field_validator("id", mode="before")
    @classmethod
    def coerce_id(cls, v):
        return str(v)

    class Config:
        from_attributes = True


class SessionDetail(SessionOut):
    steps: list[StepOut] = []
    finding: Optional[FindingOut] = None