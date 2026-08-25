# Ghost User

A synthetic user simulator for testing web apps. AI agents, each roleplaying a different kind of user, browse your app, take real actions in a real browser, hit friction, and report what went wrong — before real users do.

**Live app:** https://ghost-user-frontend.shriabiju.workers.dev
**Demo app under test:** https://ghost-user-demo-shop.shriabiju.workers.dev
**API:** https://ghost-user.onrender.com

*The backend is on a free tier and sleeps after ~15 minutes of inactivity — the first request after a while can take 30-60s.*

---

## What it does

Pick a persona — Impatient User, Confused First-Timer, Skeptical Shopper, Low-Vision User, and 19 others across 5 categories — and give it a goal, like "buy the headphones and complete checkout."

An agent loop launches a real headless browser pointed at your app and repeats a simple cycle: observe the page, decide the next action in character for that persona, execute it. Every step is logged with the model's reasoning and a screenshot. Once the run ends, a second pass reads the full trace and writes a plain-English finding — goal completed, abandoned, or blocked — with specific issues called out.

The frontend shows a step-by-step replay next to that report.

Unlike scripted QA, there's no predefined path. The agent reasons over real page state each step, and different personas don't just move at different speeds — they notice different things. A screen-reader-style persona and an impatient one can look at the same page and flag entirely different problems.

## Screenshots

**Dashboard** — past runs at a glance, with status and a "Run a test" entry point.

![Dashboard](screenshots/dashboard.png)

**Persona category picker** — 23 personas grouped into 5 categories, kept behind a dropdown so nothing's cluttered by default.

![Persona category picker](screenshots/persona-category.png)

**Persona selection** — pick the specific persona and see its description before starting a run.

![Persona selection](screenshots/persona.png)

**New run setup** — set the target URL and goal, then send the ghost.

![New run](screenshots/new-run.png)

**Finding** — the generated report: outcome plus specific, severity-tagged issues.

![Finding](screenshots/finding.png)

**Replay** — step-by-step trace with the app's screenshot and the agent's reasoning at each step.

![Replay](screenshots/replay.png)

## Stack

Frontend — React, Vite, Tailwind, Framer Motion. Deployed on Cloudflare Workers.
Backend — FastAPI, deployed on Render as a Docker image built on Microsoft's official Playwright base.
Database — PostgreSQL on Neon, via SQLAlchemy.
Browser automation — Playwright (Chromium).
LLM — Groq (`openai/gpt-oss-120b`), tool-calling for a constrained action schema: click, type, scroll, wait, report_issue, done.

## Structure

```
backend/     FastAPI app — DB models, agent loop, Playwright driver, report generator
frontend/    React dashboard
demo-app/    A small, intentionally flawed checkout flow used as the app under test
docs/        Architecture notes
```

## Running locally

**Backend**
```
cd backend
pip install -r requirements.txt --break-system-packages
playwright install chromium
# copy .env.example to .env and fill in DATABASE_URL / GROQ_API_KEY
python run.py
```
`run.py`, not `uvicorn --reload`, is required on Windows — Playwright needs asyncio's ProactorEventLoop, which `--reload` doesn't reliably carry into its Windows subprocess. Details in `docs/ARCHITECTURE.md`.

**Demo app**
```
cd demo-app
npm install
npm run dev   # localhost:5174
```

**Frontend**
```
cd frontend
npm install
npm run dev   # localhost:5173
```