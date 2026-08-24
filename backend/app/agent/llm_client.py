"""
Thin wrapper around the Groq API for the agent's per-step decisions.
Keeps the tool-calling / parsing logic in one place so the agent loop
stays readable.
"""

import json
from groq import Groq

from app.config import settings
from app.agent.actions import AgentAction, BROWSER_ACTION_TOOL


_client = Groq(api_key=settings.groq_api_key)


def decide_next_action(persona_system_prompt: str, goal: str, observation: str, history: list[str]) -> AgentAction:
    """
    Sends the current page observation + persona + goal + recent history
    to the LLM and returns the single structured action it chose.
    """
    history_text = "\n".join(history[-5:]) if history else "(no actions yet)"

    messages = [
        {"role": "system", "content": persona_system_prompt},
        {
            "role": "user",
            "content": (
                f"Your goal: {goal}\n\n"
                f"Recent actions you've taken:\n{history_text}\n\n"
                f"Current page state:\n{observation}\n\n"
                "Decide your single next action by calling the browser_action tool."
            ),
        },
    ]

    response = _client.chat.completions.create(
        model=settings.groq_model,
        messages=messages,
        tools=[BROWSER_ACTION_TOOL],
        tool_choice={"type": "function", "function": {"name": "browser_action"}},
        temperature=0.7,
    )

    tool_call = response.choices[0].message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    return AgentAction(**args)