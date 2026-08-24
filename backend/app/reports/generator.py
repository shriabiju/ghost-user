"""
Post-session pass: takes the full step trace and asks the LLM to produce
a plain-English UX finding, in the same voice as "users abandoned checkout
at step 3" from the original pitch.
"""

import json
from groq import Groq
from sqlalchemy.orm import Session as DBSession

from app.config import settings
from app.models.session import Session as SessionModel
from app.models.finding import Finding

_client = Groq(api_key=settings.groq_api_key)

REPORT_TOOL = {
    "type": "function",
    "function": {
        "name": "submit_finding",
        "description": "Submit the UX finding for this test session.",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "One or two sentence plain-English summary of what happened and why it matters.",
                },
                "outcome": {
                    "type": "string",
                    "enum": ["goal_completed", "abandoned", "blocked"],
                },
                "issues": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "step_number": {"type": "integer"},
                            "issue": {"type": "string"},
                            "severity": {"type": "string", "enum": ["low", "medium", "high"]},
                        },
                        "required": ["step_number", "issue", "severity"],
                    },
                },
            },
            "required": ["summary", "outcome", "issues"],
        },
    },
}


def generate_finding(db: DBSession, session: SessionModel) -> Finding:
    trace_lines = [
        f"Step {s.step_number}: {s.action_type} — {s.reasoning}"
        for s in session.steps
    ]
    trace_text = "\n".join(trace_lines)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a UX researcher reviewing a synthetic user test session. "
                "Summarize what happened in plain English, as if reporting to a product team. "
                "Be specific about where and why friction occurred."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Persona: {session.persona.name}\n"
                f"Goal: {session.goal}\n\n"
                f"Action trace:\n{trace_text}\n\n"
                "Submit your finding by calling submit_finding."
            ),
        },
    ]

    response = _client.chat.completions.create(
        model=settings.groq_model,
        messages=messages,
        tools=[REPORT_TOOL],
        tool_choice={"type": "function", "function": {"name": "submit_finding"}},
        temperature=0.4,
    )

    args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)

    finding = Finding(
        session_id=session.id,
        summary=args["summary"],
        issues=args["issues"],
        outcome=args["outcome"],
    )
    db.add(finding)
    db.commit()
    return finding