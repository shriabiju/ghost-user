from datetime import datetime
from pydantic import BaseModel, field_validator


class Issue(BaseModel):
    step_number: int
    issue: str
    severity: str  # "low" | "medium" | "high"


class FindingOut(BaseModel):
    id: str
    session_id: str
    summary: str
    issues: list[Issue]
    outcome: str  # "goal_completed" | "abandoned" | "blocked"
    created_at: datetime

    @field_validator("id", "session_id", mode="before")
    @classmethod
    def coerce_ids(cls, v):
        return str(v)

    class Config:
        from_attributes = True