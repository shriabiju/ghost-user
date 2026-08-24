"""
Wraps Playwright for the agent loop: launches a browser, executes the
structured actions the LLM decides on, and saves screenshots for replay.
"""

import os
from playwright.async_api import async_playwright, Page

from app.agent.actions import AgentAction, ActionType

SCREENSHOT_DIR = "screenshots"


class BrowserDriver:
    def __init__(self):
        self._playwright = None
        self._browser = None
        self.page: Page | None = None
        self.last_action_failed = False

    async def start(self, url: str):
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=True)
        self.page = await self._browser.new_page(viewport={"width": 1000, "height": 800})
        await self.page.goto(url, wait_until="networkidle")
        # give client-rendered React apps a beat to paint after network idle
        await self.page.wait_for_timeout(400)

    async def execute(self, action: AgentAction):
        """Executes a structured AgentAction against the live page."""
        self.last_action_failed = False

        if action.action_type == ActionType.CLICK and action.selector:
            self.last_action_failed = not await self._safe_click(action.selector)

        elif action.action_type == ActionType.TYPE and action.selector:
            self.last_action_failed = not await self._safe_fill(action.selector, action.text or "")

        elif action.action_type == ActionType.SCROLL:
            await self.page.mouse.wheel(0, 600)

        elif action.action_type == ActionType.WAIT:
            await self.page.wait_for_timeout(1000)

        # let any UI update (animations, re-renders) settle before the next observation
        await self.page.wait_for_timeout(300)

    async def _safe_click(self, selector: str) -> bool:
        """Tries a few strategies to find and click an element by its accessible name. Returns True on success."""
        strategies = [
            lambda: self.page.get_by_role("button", name=selector, exact=False),
            lambda: self.page.get_by_role("link", name=selector, exact=False),
            lambda: self.page.get_by_text(selector, exact=False),
            lambda: self.page.locator(selector),
        ]
        for strategy in strategies:
            try:
                locator = strategy().first
                await locator.click(timeout=2000)
                return True
            except Exception:
                continue
        return False

    async def _safe_fill(self, selector: str, text: str) -> bool:
        strategies = [
            lambda: self.page.get_by_label(selector, exact=False),
            lambda: self.page.get_by_placeholder(selector, exact=False),
            lambda: self.page.locator(selector),
        ]
        for strategy in strategies:
            try:
                locator = strategy().first
                await locator.fill(text, timeout=2000)
                return True
            except Exception:
                continue
        return False

    async def screenshot(self, session_id, step_number: int) -> str:
        os.makedirs(f"{SCREENSHOT_DIR}/{session_id}", exist_ok=True)
        path = f"{SCREENSHOT_DIR}/{session_id}/step_{step_number}.png"
        await self.page.screenshot(path=path)
        return path

    async def close(self):
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()