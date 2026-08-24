from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, field_validator


class StepOut(BaseModel):
    id: str
    session_id: str
    step_number: int
    action_type: str
    action_payload: Optional[dict[str, Any]] = None
    reasoning: Optional[str] = None
    observation_summary: Optional[str] = None
    screenshot_path: Optional[str] = None
    created_at: datetime

    @field_validator("id", "session_id", mode="before")
    @classmethod
    def coerce_ids(cls, v):
        return str(v)

    class Config:
        from_attributes = True