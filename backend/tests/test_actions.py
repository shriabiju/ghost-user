"""
Tests for the agent's action schema — the contract between the LLM's
tool-call output and what Playwright can actually execute.
"""

import pytest
from pydantic import ValidationError

from app.agent.actions import AgentAction, ActionType, BROWSER_ACTION_TOOL


def test_action_type_enum_has_six_actions():
    assert len(ActionType) == 6
    assert set(a.value for a in ActionType) == {
        "click", "type", "scroll", "wait", "report_issue", "done"
    }


def test_agent_action_requires_reasoning():
    with pytest.raises(ValidationError):
        AgentAction(action_type="click", selector="Add to Cart")


def test_agent_action_valid_click():
    action = AgentAction(
        action_type="click",
        selector="Add to Cart",
        reasoning="This is the obvious next step toward the goal.",
    )
    assert action.action_type == ActionType.CLICK
    assert action.selector == "Add to Cart"
    assert action.text is None


def test_agent_action_optional_fields_default_none():
    action = AgentAction(action_type="wait", reasoning="The page seems to still be loading.")
    assert action.selector is None
    assert action.text is None
    assert action.issue_description is None


def test_browser_action_tool_schema_matches_action_type_enum():
    schema_enum = BROWSER_ACTION_TOOL["function"]["parameters"]["properties"]["action_type"]["enum"]
    assert set(schema_enum) == set(a.value for a in ActionType)


def test_browser_action_tool_nullable_fields_accept_string_or_null():
    props = BROWSER_ACTION_TOOL["function"]["parameters"]["properties"]
    for field in ("selector", "text", "issue_description"):
        assert props[field]["type"] == ["string", "null"]


def test_browser_action_tool_requires_action_type_and_reasoning():
    required = BROWSER_ACTION_TOOL["function"]["parameters"]["required"]
    assert set(required) == {"action_type", "reasoning"}