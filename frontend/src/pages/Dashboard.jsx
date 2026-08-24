import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import GhostAvatar from "../components/ghost/GhostAvatar";
import { getSessions } from "../api/client";

const STATUS_STYLES = {
  pending: "text-ghost-dim",
  running: "text-accent",
  completed: "text-signal-low",
  failed: "text-signal-high",
};

function formatTime(iso) {
  if (!iso) return "—";
  return new Date(iso).toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function Dashboard() {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSessions()
      .then(setSessions)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-10">
      <section className="flex flex-col items-center gap-6 py-10 text-center">
        <GhostAvatar state="idle" size={140} />
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">Ghost User</h1>
          <p className="mt-2 max-w-md text-ghost-dim">
            Synthetic users find your app's friction before real ones do. Run a
            persona through your product and see where it gets stuck.
          </p>
        </div>
        <Link to="/new">
          <Button size="lg">Run a test</Button>
        </Link>
      </section>

      <section>
        <h2 className="mb-4 text-lg font-medium">Past runs</h2>

        {loading && <p className="text-ghost-dim">Loading sessions…</p>}

        {!loading && sessions.length === 0 && (
          <Card className="text-center text-ghost-dim">
            No runs yet. Send a ghost through your app to see it here.
          </Card>
        )}

        <div className="grid gap-4 sm:grid-cols-2">
          {sessions.map((session) => (
            <Link
              key={session.id}
              to={
                session.status === "completed"
                  ? `/runs/${session.id}/findings`
                  : `/runs/${session.id}`
              }
            >
              <Card className="h-full transition-colors hover:border-accent/50">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="font-medium">{session.goal}</p>
                    <p className="mt-1 text-sm text-ghost-dim">{session.target_url}</p>
                  </div>
                  <span className={`text-xs font-medium uppercase tracking-wide ${STATUS_STYLES[session.status]}`}>
                    {session.status}
                  </span>
                </div>
                <div className="mt-4 flex items-center justify-between text-xs text-ghost-dim">
                  <span>{session.persona_id.replace(/_/g, " ")}</span>
                  <span>{formatTime(session.created_at)}</span>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}