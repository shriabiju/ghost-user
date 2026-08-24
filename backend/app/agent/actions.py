from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel


class ActionType(str, Enum):
    CLICK = "click"
    TYPE = "type"
    SCROLL = "scroll"
    WAIT = "wait"
    REPORT_ISSUE = "report_issue"
    DONE = "done"


class AgentAction(BaseModel):
    """
    A single structured action the agent decided to take.
    Parsed out of the LLM's tool call each step of the loop.
    """

    action_type: ActionType
    selector: Optional[str] = None      # CSS/accessibility selector, for click/type
    text: Optional[str] = None          # text to type, for TYPE
    issue_description: Optional[str] = None  # for REPORT_ISSUE
    reasoning: str                      # why the agent chose this action


# Groq/OpenAI-style tool definition passed to the LLM each step.
# The model must respond by calling this tool — this is what keeps
# actions constrained to things Playwright can actually execute.
#
# Note: selector/text/issue_description allow ["string", "null"] because
# the model sometimes explicitly returns null for fields that don't apply
# to the chosen action_type (e.g. no selector for "wait"), and Groq's
# strict tool-call validation rejects null against a plain "string" type.
BROWSER_ACTION_TOOL = {
    "type": "function",
    "function": {
        "name": "browser_action",
        "description": (
            "Take the single next action in the browser based on the current page "
            "state and your persona's goal and behavior."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "action_type": {
                    "type": "string",
                    "enum": [a.value for a in ActionType],
                    "description": (
                        "click: click an element. type: enter text into a field. "
                        "scroll: scroll the page. wait: pause (e.g. for a slow load). "
                        "report_issue: flag a UX problem you just encountered. "
                        "done: you completed the goal or are giving up."
                    ),
                },
                "selector": {
                    "type": ["string", "null"],
                    "description": "Accessible name/text of the target element, required for click/type, otherwise null.",
                },
                "text": {
                    "type": ["string", "null"],
                    "description": "Text to type, required for the type action, otherwise null.",
                },
                "issue_description": {
                    "type": ["string", "null"],
                    "description": "Plain-English description of the problem, required for report_issue, otherwise null.",
                },
                "reasoning": {
                    "type": "string",
                    "description": "One sentence: why you're taking this action, in character for your persona.",
                },
            },
            "required": ["action_type", "reasoning"],
        },
    },
}
