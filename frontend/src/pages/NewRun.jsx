import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import GhostAvatar from "../components/ghost/GhostAvatar";
import { getPersonas, startRun } from "../api/client";

const DEFAULT_TARGET = "https://ghost-user-demo-shop.shriabiju.workers.dev";
const DEFAULT_GOAL = "Buy the headphones and complete checkout";

const selectClass =
  "w-full rounded-lg border border-ink-600 bg-ink-900 px-3 py-2.5 text-sm outline-none focus:border-accent appearance-none cursor-pointer";

export default function NewRun() {
  const navigate = useNavigate();
  const [personas, setPersonas] = useState([]);
  const [activeCategory, setActiveCategory] = useState("");
  const [selectedPersona, setSelectedPersona] = useState("");
  const [targetUrl, setTargetUrl] = useState(DEFAULT_TARGET);
  const [goal, setGoal] = useState(DEFAULT_GOAL);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    getPersonas().then((data) => {
      setPersonas(data);
    });
  }, []);

  const categories = useMemo(() => {
    const seen = [];
    for (const p of personas) {
      if (!seen.includes(p.category)) seen.push(p.category);
    }
    return seen;
  }, [personas]);

  const personasInCategory = useMemo(
    () => personas.filter((p) => p.category === activeCategory),
    [personas, activeCategory]
  );

  const selected = personas.find((p) => p.id === selectedPersona);

  function handleCategoryChange(category) {
    setActiveCategory(category);
    setSelectedPersona(""); // force an explicit persona choice within the new category
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const session = await startRun({
        persona_id: selectedPersona,
        target_url: targetUrl,
        goal,
      });
      navigate(`/runs/${session.id}`);
    } catch (err) {
      setError("Couldn't start the run. Check that the backend is reachable and try again.");
      setSubmitting(false);
    }
  }

  return (
    <div className="mx-auto max-w-xl space-y-8">
      <div className="text-center">
        <h1 className="text-2xl font-semibold tracking-tight">New run</h1>
        <p className="mt-1 text-ghost-dim">Choose a persona and tell it what to do.</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <Card className="space-y-4">
          <label className="block">
            <span className="mb-1.5 block text-sm font-medium">Persona category</span>
            <select
              value={activeCategory}
              onChange={(e) => handleCategoryChange(e.target.value)}
              className={selectClass}
              required
            >
              <option value="" disabled>
                Select a category…
              </option>
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
          </label>

          <label className="block">
            <span className="mb-1.5 block text-sm font-medium">Persona</span>
            <select
              value={selectedPersona}
              onChange={(e) => setSelectedPersona(e.target.value)}
              className={selectClass}
              disabled={!activeCategory}
              required
            >
              <option value="" disabled>
                {activeCategory ? "Select a persona…" : "Choose a category first"}
              </option>
              {personasInCategory.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name}
                </option>
              ))}
            </select>
          </label>

          {selected && (
            <div className="flex items-start gap-3 rounded-lg border border-ink-700 bg-ink-900/60 p-3">
              <GhostAvatar state="idle" size={40} />
              <div>
                <p className="text-sm font-medium">{selected.name}</p>
                <p className="mt-0.5 text-xs text-ghost-dim leading-snug">{selected.description}</p>
              </div>
            </div>
          )}
        </Card>

        <Card className="space-y-4">
          <label className="block">
            <span className="mb-1.5 block text-sm font-medium">Target URL</span>
            <input
              type="text"
              value={targetUrl}
              onChange={(e) => setTargetUrl(e.target.value)}
              className="w-full rounded-lg border border-ink-600 bg-ink-900 px-3 py-2 text-sm outline-none focus:border-accent"
              required
            />
          </label>

          <label className="block">
            <span className="mb-1.5 block text-sm font-medium">Goal</span>
            <textarea
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              rows={3}
              className="w-full rounded-lg border border-ink-600 bg-ink-900 px-3 py-2 text-sm outline-none focus:border-accent"
              required
            />
          </label>
        </Card>

        {error && <p className="text-sm text-signal-high">{error}</p>}

        <Button type="submit" size="lg" disabled={submitting || !selectedPersona} className="w-full">
          {submitting ? "Starting…" : "Send the ghost"}
        </Button>
      </form>
    </div>
  );
}