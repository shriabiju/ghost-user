import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import GhostAvatar from "../components/ghost/GhostAvatar";
import { getSession } from "../api/client";

const SEVERITY_STYLES = {
  low: "border-signal-low/40 text-signal-low",
  medium: "border-signal-medium/40 text-signal-medium",
  high: "border-signal-high/40 text-signal-high",
};

const OUTCOME_LABEL = {
  goal_completed: "Goal completed",
  abandoned: "Abandoned",
  blocked: "Blocked",
};

export default function Findings() {
  const { sessionId } = useParams();
  const [session, setSession] = useState(null);
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    getSession(sessionId).then(setSession);
  }, [sessionId]);

  if (!session) {
    return <p className="text-center text-ghost-dim">Loading findings…</p>;
  }

  const { finding, steps } = session;
  const step = steps[activeStep];

  return (
    <div className="space-y-8">
      <div className="flex flex-col items-center gap-3 text-center">
        <GhostAvatar state="done" size={100} />
        <div>
          <p className="text-sm text-ghost-dim">{session.persona_id.replace(/_/g, " ")}</p>
          <h1 className="text-xl font-medium">{session.goal}</h1>
        </div>
      </div>

      {finding && (
        <Card>
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-medium">Finding</h2>
            <span className="text-xs font-medium uppercase tracking-wide text-accent">
              {OUTCOME_LABEL[finding.outcome] ?? finding.outcome}
            </span>
          </div>
          <p className="mt-3 text-ghost-dim">{finding.summary}</p>

          {finding.issues.length > 0 && (
            <div className="mt-5 space-y-2">
              {finding.issues.map((issue, i) => (
                <div
                  key={i}
                  className={`rounded-lg border bg-ink-900/50 px-3 py-2 text-sm ${SEVERITY_STYLES[issue.severity]}`}
                >
                  <span className="font-mono text-xs opacity-70">Step {issue.step_number}</span>{" "}
                  {issue.issue}
                </div>
              ))}
            </div>
          )}
        </Card>
      )}

      <div>
        <h2 className="mb-3 text-lg font-medium">Replay</h2>
        <Card className="p-0 overflow-hidden">
          <div className="grid gap-0 sm:grid-cols-[1fr_260px]">
            <div className="aspect-video bg-ink-900 flex items-center justify-center border-b sm:border-b-0 sm:border-r border-ink-700">
              {step?.screenshot_path ? (
                <img
                  src={`${import.meta.env.VITE_API_URL || "http://localhost:8000"}/${step.screenshot_path}`}
                  alt={`Step ${step.step_number} screenshot`}
                  className="h-full w-full object-contain"
                />
              ) : (
                <p className="text-sm text-ghost-dim">No screenshot for this step.</p>
              )}
            </div>

            <div className="max-h-[360px] overflow-y-auto p-3 space-y-1">
              {steps.map((s, i) => (
                <button
                  key={s.id}
                  onClick={() => setActiveStep(i)}
                  className={`
                    block w-full rounded-lg px-3 py-2 text-left text-xs font-mono transition-colors
                    ${i === activeStep ? "bg-accent/15 text-ghost-white" : "text-ghost-dim hover:bg-ink-700/50"}
                  `}
                >
                  {s.step_number}. {s.action_type}
                </button>
              ))}
            </div>
          </div>

          {step && (
            <div className="border-t border-ink-700 px-4 py-3 text-sm text-ghost-dim">
              {step.reasoning}
            </div>
          )}
        </Card>
      </div>

      <div className="flex justify-center">
        <Link to="/new">
          <Button variant="secondary">Run another test</Button>
        </Link>
      </div>
    </div>
  );
}