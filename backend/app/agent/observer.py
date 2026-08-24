"""
Turns the live page state into a compact, LLM-friendly text description.
Reports two things: interactive elements the agent can act on, and
static text/headings the agent can read (e.g. confirmation messages,
labels, error text) — without this second part, the agent is "blind"
to any page state that isn't itself clickable.
"""

from playwright.async_api import Page

INTERACTIVE_ROLES = ["button", "link", "textbox", "checkbox", "combobox"]
TEXT_SELECTORS = ["h1", "h2", "h3", "p", "label", "span"]


async def get_observation(page: Page, max_per_role: int = 15, max_text_nodes: int = 20) -> str:
    """
    Returns a compact text snapshot: interactive elements grouped by role,
    plus visible static text/headings, plus current URL and title.
    """
    interactive_lines: list[str] = []

    for role in INTERACTIVE_ROLES:
        try:
            locator = page.get_by_role(role)
            count = min(await locator.count(), max_per_role)
            for i in range(count):
                el = locator.nth(i)
                name = (await el.inner_text()) or (await el.get_attribute("aria-label")) or ""
                name = name.strip().replace("\n", " ")
                if name:
                    interactive_lines.append(f'- [{role}] "{name}"')
        except Exception:
            continue

    text_lines: list[str] = []
    seen_text = set()
    for selector in TEXT_SELECTORS:
        try:
            locator = page.locator(selector)
            count = min(await locator.count(), max_text_nodes)
            for i in range(count):
                el = locator.nth(i)
                if not await el.is_visible():
                    continue
                text = (await el.inner_text()).strip().replace("\n", " ")
                # skip empty, very long, or already-captured (e.g. text also inside a button)
                if not text or len(text) > 200 or text in seen_text:
                    continue
                seen_text.add(text)
                text_lines.append(f'- {selector}: "{text}"')
                if len(text_lines) >= max_text_nodes:
                    break
        except Exception:
            continue
        if len(text_lines) >= max_text_nodes:
            break

    header = f"URL: {page.url}\nTitle: {await page.title()}"
    interactive_block = "Interactive elements:\n" + (
        "\n".join(interactive_lines) if interactive_lines else "(none detected)"
    )
    text_block = "Visible text on page:\n" + (
        "\n".join(text_lines) if text_lines else "(none detected)"
    )

    return f"{header}\n\n{interactive_block}\n\n{text_block}"