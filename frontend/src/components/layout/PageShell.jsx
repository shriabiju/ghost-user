import Navbar from "./Navbar";

/**
 * Shared page wrapper: navbar + centered content column.
 * Every route renders inside this.
 */
export default function PageShell({ children }) {
  return (
    <div className="min-h-screen bg-ink-900">
      <Navbar />
      <main className="mx-auto max-w-5xl px-6 py-10">{children}</main>
    </div>
  );
}