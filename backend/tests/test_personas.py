"""
Tests for persona data integrity — since personas are the core "content"
of the product, a bad entry here would silently break the picker UI or
produce a persona with no real behavior.
"""

from app.agent.personas import PERSONAS

REQUIRED_KEYS = {"id", "name", "category", "description", "system_prompt"}
EXPECTED_CATEGORIES = {
    "Tech Comfort",
    "Shopping Behavior",
    "Accessibility & Special Needs",
    "Age & Life Stage",
    "Context & Environment",
}


def test_persona_count():
    assert len(PERSONAS) == 23


def test_every_persona_has_required_keys():
    for persona in PERSONAS:
        assert REQUIRED_KEYS.issubset(persona.keys())


def test_persona_ids_are_unique():
    ids = [p["id"] for p in PERSONAS]
    assert len(ids) == len(set(ids))


def test_persona_categories_are_valid():
    for persona in PERSONAS:
        assert persona["category"] in EXPECTED_CATEGORIES


def test_all_five_categories_are_represented():
    categories_used = {p["category"] for p in PERSONAS}
    assert categories_used == EXPECTED_CATEGORIES


def test_no_empty_system_prompts_or_descriptions():
    for persona in PERSONAS:
        assert len(persona["system_prompt"].strip()) > 20
        assert len(persona["description"].strip()) > 10