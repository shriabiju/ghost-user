"""
The core observe -> decide -> act loop. Runs a full session end to end:
launches a browser, steps through actions until the goal is reached,
the agent gives up, or the step cap is hit, and persists every step.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session as DBSession

from app.config import settings
from app.models.session import Session as SessionModel
from app.models.step import Step
from app.agent.observer import get_observation
from app.agent.llm_client import decide_next_action
from app.agent.actions import ActionType
from app.browser.playwright_driver import BrowserDriver
from app.reports.generator import generate_finding


async def run_session(db: DBSession, session: SessionModel) -> SessionModel:
    session.status = "running"
    session.started_at = datetime.now(timezone.utc)
    db.commit()

    history: list[str] = []
    driver = BrowserDriver()

    try:
        await driver.start(session.target_url)

        for step_number in range(1, settings.max_steps_per_session + 1):
            observation = await get_observation(driver.page)

            action = decide_next_action(
                persona_system_prompt=session.persona.system_prompt,
                goal=session.goal,
                observation=observation,
                history=history,
            )

            if action.action_type == ActionType.DONE:
                screenshot_path = await driver.screenshot(session.id, step_number)
                history.append(f"Step {step_number}: done - {action.reasoning}")

                step = Step(
                    session_id=session.id,
                    step_number=step_number,
                    action_type=action.action_type.value,
                    action_payload={"selector": action.selector, "text": action.text},
                    reasoning=action.reasoning,
                    observation_summary=observation[:500],
                    screenshot_path=screenshot_path,
                )
                db.add(step)
                session.total_steps = step_number
                db.commit()
                break

            if action.action_type == ActionType.REPORT_ISSUE:
                screenshot_path = await driver.screenshot(session.id, step_number)
                history.append(f"Step {step_number}: report_issue - {action.reasoning}")

                step = Step(
                    session_id=session.id,
                    step_number=step_number,
                    action_type=action.action_type.value,
                    action_payload={"issue_description": action.issue_description},
                    reasoning=action.reasoning,
                    observation_summary=observation[:500],
                    screenshot_path=screenshot_path,
                )
                db.add(step)
                session.total_steps = step_number
                db.commit()
                continue

            # click / type / scroll / wait — actually interact with the page
            await driver.execute(action)
            screenshot_path = await driver.screenshot(session.id, step_number)

            result_note = "FAILED (element not found)" if driver.last_action_failed else "succeeded"
            history.append(
                f"Step {step_number}: {action.action_type.value} "
                f"({action.selector}) {result_note} - {action.reasoning}"
            )

            step = Step(
                session_id=session.id,
                step_number=step_number,
                action_type=action.action_type.value,
                action_payload={"selector": action.selector, "text": action.text},
                reasoning=action.reasoning,
                observation_summary=observation[:500],
                screenshot_path=screenshot_path,
            )
            db.add(step)
            session.total_steps = step_number
            db.commit()

        session.status = "completed"

    except Exception:
        session.status = "failed"
        raise

    finally:
        session.completed_at = datetime.now(timezone.utc)
        db.commit()
        await driver.close()

    generate_finding(db, session)
    return session