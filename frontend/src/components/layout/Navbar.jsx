import { Link, useLocation } from "react-router-dom";
import GhostAvatar from "../ghost/GhostAvatar";

export default function Navbar() {
  const location = useLocation();

  const navLink = (to, label) => {
    const active = location.pathname === to;
    return (
      <Link
        to={to}
        className={`text-sm font-medium transition-colors ${
          active ? "text-ghost-white" : "text-ghost-dim hover:text-ghost-white"
        }`}
      >
        {label}
      </Link>
    );
  };

  return (
    <header className="sticky top-0 z-10 border-b border-ink-700 bg-ink-900/80 backdrop-blur-md">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-3">
        <Link to="/" className="flex items-center gap-2">
          <GhostAvatar state="idle" size={32} />
          <span className="text-lg font-semibold tracking-tight">Ghost User</span>
        </Link>

        <nav className="flex items-center gap-6">
          {navLink("/", "Dashboard")}
          {navLink("/new", "New Run")}
        </nav>
      </div>
    </header>
  );
}