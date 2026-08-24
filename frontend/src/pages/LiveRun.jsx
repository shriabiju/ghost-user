import { useEffect, useState, useRef } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";

import Card from "../components/ui/Card";
import GhostAvatar from "../components/ghost/GhostAvatar";
import { getSession } from "../api/client";

const POLL_INTERVAL_MS = 1500;

function stateForStep(actionType) {
  if (actionType === "report_issue") return "foundIssue";
  if (actionType === "done") return "done";
  return "running";
}

export default function LiveRun() {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const [session, setSession] = useState(null);
  const pollRef = useRef(null);

  useEffect(() => {
    async function poll() {
      const data = await getSession(sessionId);
      setSession(data);

      if (data.status === "completed") {
        clearInterval(pollRef.current);
        navigate(`/runs/${sessionId}/findings`, { replace: true });
      } else if (data.status === "failed") {
        clearInterval(pollRef.current);
      }
    }

    poll();
    pollRef.current = setInterval(poll, POLL_INTERVAL_MS);
    return () => clearInterval(pollRef.current);
  }, [sessionId, navigate]);

  if (!session) {
    return <p className="text-center text-ghost-dim">Loading run…</p>;
  }

  const lastStep = session.steps[session.steps.length - 1];
  const ghostState = lastStep ? stateForStep(lastStep.action_type) : "running";
  const latestScreenshot = lastStep?.screenshot_path;

  return (
    <div className="space-y-8">
      <div className="flex flex-col items-center gap-3 text-center">
        <GhostAvatar state={ghostState} persona={session.persona_id} size={110} />
        <div>
          <p className="text-sm text-ghost-dim">
            {session.persona_id.replace(/_/g, " ")} · {session.status}
          </p>
          <h1 className="text-xl font-medium">{session.goal}</h1>
        </div>
      </div>

      <div className="grid gap-6 sm:grid-cols-2">
        <Card className="p-0 overflow-hidden">
          <div className="border-b border-ink-700 px-4 py-2 text-xs font-medium text-ghost-dim">
            App under test
          </div>
          <div className="aspect-video bg-ink-900 flex items-center justify-center">
            {latestScreenshot ? (
              <img
                src={`http://localhost:8000/${latestScreenshot}`}
                alt="Latest screenshot of the app under test"
                className="h-full w-full object-contain"
              />
            ) : (
              <p className="text-sm text-ghost-dim">Waiting for the first step…</p>
            )}
          </div>
        </Card>

        <Card className="p-0 overflow-hidden">
          <div className="border-b border-ink-700 px-4 py-2 text-xs font-medium text-ghost-dim">
            Ghost activity
          </div>
          <div className="max-h-[360px] space-y-3 overflow-y-auto p-4 font-mono text-xs">
            {session.steps.length === 0 && (
              <p className="text-ghost-dim">No actions yet.</p>
            )}
            {session.steps.map((step) => (
              <div key={step.id} className="border-l-2 border-ink-600 pl-3">
                <p className="text-ghost-white">
                  <span className="text-accent">{step.action_type}</span>
                  {step.action_payload?.selector ? ` → "${step.action_payload.selector}"` : ""}
                </p>
                <p className="mt-0.5 text-ghost-dim">{step.reasoning}</p>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {session.status === "failed" && (
        <Card className="text-center text-signal-high">
          This run failed unexpectedly.{" "}
          <Link to="/new" className="underline">
            Try again
          </Link>
          .
        </Card>
      )}
    </div>
  );
}