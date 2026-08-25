# Architecture

## The agent loop

```
┌─────────┐   ┌──────────┐   ┌─────────┐   ┌─────────┐
│ observe │ → │  decide  │ → │   act   │ → │  log    │ → (repeat, up to 12 steps)
└─────────┘   └──────────┘   └─────────┘   └─────────┘
     ↑                                           │
     └───────────────────────────────────────────┘
```

1. **Observe** (`agent/observer.py`) — reads the live page via Playwright and
   produces a compact text snapshot: interactive elements (buttons, links,
   inputs) by accessible name, *plus* visible headings/text (added after
   discovering the agent couldn't perceive a confirmation message that had no
   interactive role).
2. **Decide** (`agent/llm_client.py`) — sends the persona's system prompt, the
   goal, recent history, and the current observation to Groq, using forced
   tool-calling against a strict action schema (`agent/actions.py`):
   `click | type | scroll | wait | report_issue | done`. This is what keeps
   the LLM's output directly executable rather than free-text.
3. **Act** (`browser/playwright_driver.py`) — executes the chosen action
   against the real page, using layered selector strategies (role+name → text
   → raw locator) and reporting success/failure back into the agent's own
   history, so it knows when it's actually stuck instead of hallucinating
   progress.
4. **Log** — every step (action, reasoning, screenshot, success/failure) is
   persisted to Postgres (`models/step.py`), so the frontend can replay a run
   step by step.
5. **Report** (`reports/generator.py`) — once the loop ends (goal reached,
   agent gives up, or the step cap hits), a second LLM call reads the full
   trace and produces a structured finding: outcome + a specific, severity-
   tagged issue list.

## Persona design

Personas (`agent/personas.py`) are plain data — an id, category, description,
and a system prompt — seeded into the DB on startup. Keeping them as
versioned code (not DB-only) means the exact wording driving each persona's
behavior is reviewable and diffable. 23 personas span 5 categories: Tech
Comfort, Shopping Behavior, Accessibility & Special Needs, Age & Life Stage,
and Context & Environment.

## Real bugs hit and fixed along the way

- **Windows + Playwright + uvicorn `--reload`:** Playwright needs to spawn a
  subprocess (the browser), which requires asyncio's `ProactorEventLoop` on
  Windows. uvicorn's `--reload` runs the server in a child process that
  doesn't reliably inherit a policy set inside the app — fixed with a small
  launcher script (`run.py`) that sets the policy before uvicorn starts, with
  `reload` off.
- **Groq model deprecation:** `llama-3.3-70b-versatile` was retired; switched
  to `openai/gpt-oss-120b`.
- **Strict tool-call schema vs. nullable fields:** Groq's tool-calling
  rejected `null` against a plain `"string"` type when the model correctly
  left an inapplicable field empty (e.g. no selector for `wait`). Fixed by
  typing those fields as `["string", "null"]`.
- **Blank demo app:** missing `vite.config.js` meant no React plugin, so Vite
  fell back to a JSX transform requiring an explicit `React` import that
  wasn't present — silent blank page, no error until checking DevTools.
- **Observer blindness:** the agent reported "no confirmation shown" on a page
  that *did* show one, because the observer only read interactive elements.
  Fixed by also reading visible headings/text.
- **Render deploy chain:** Python 3.14 (no `pydantic-core` wheel yet) → pinned
  via `PYTHON_VERSION` env var → Playwright's `--with-deps` needing root apt
  access unavailable on Render's native runtime → switched to Docker using
  Microsoft's official Playwright image → a `groq`/`httpx` version conflict
  (`proxies` kwarg removed) → pinned `httpx==0.27.2`.

## Design note: text-based vs. visual observation

The observer works off the accessibility tree (element roles + labels), which
means personas reason about *semantics* — an element's name and purpose — the
same way a screen reader or keyboard-only user would, rather than about pixel
appearance. This is what makes the accessibility-reliant and keyboard-only
personas meaningfully realistic, and it's also why the app's functional flaws
(like a silently-failing required checkbox) are what actually drive
persona-dependent success/failure variation, rather than purely stylistic
ones. Extending the observer with a vision-capable model reading screenshots
is a natural next step for catching purely visual issues (contrast, layout)
on top of the current semantic layer.