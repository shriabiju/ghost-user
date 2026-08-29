"""
Tests for the Pydantic response schemas — specifically the UUID-to-string
coercion added after a ResponseValidationError surfaced in production
(SQLAlchemy returns UUID objects; the schemas declare plain str fields).
"""

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace

from app.schemas.session import SessionOut
from app.schemas.step import StepOut
from app.schemas.finding import FindingOut, Issue
from app.schemas.persona import PersonaOut


def test_session_out_coerces_uuid_to_string():
    row = SimpleNamespace(
        id=uuid.uuid4(),
        persona_id="impatient",
        target_url="https://example.com",
        goal="Buy something",
        status="completed",
        total_steps=4,
        started_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
    )
    out = SessionOut.model_validate(row)
    assert isinstance(out.id, str)


def test_step_out_coerces_both_uuid_fields():
    row = SimpleNamespace(
        id=uuid.uuid4(),
        session_id=uuid.uuid4(),
        step_number=1,
        action_type="click",
        action_payload=None,
        reasoning="Clicking the obvious button.",
        observation_summary="Some page text.",
        screenshot_path=None,
        created_at=datetime.now(timezone.utc),
    )
    out = StepOut.model_validate(row)
    assert isinstance(out.id, str)
    assert isinstance(out.session_id, str)


def test_finding_out_validates_issue_list():
    row = SimpleNamespace(
        id=uuid.uuid4(),
        session_id=uuid.uuid4(),
        summary="The user abandoned checkout.",
        issues=[{"step_number": 3, "issue": "Button unclear", "severity": "medium"}],
        outcome="abandoned",
        created_at=datetime.now(timezone.utc),
    )
    out = FindingOut.model_validate(row)
    assert isinstance(out.issues[0], Issue)
    assert out.issues[0].severity == "medium"


def test_persona_out_reads_from_orm_style_object():
    row = SimpleNamespace(
        id="power_user",
        name="Power User",
        category="Tech Comfort",
        description="Experienced and efficient.",
    )
    out = PersonaOut.model_validate(row)
    assert out.id == "power_user"
    assert out.category == "Tech Comfort"