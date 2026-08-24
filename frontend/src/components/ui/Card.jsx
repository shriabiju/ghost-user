/**
 * Shared surface for content blocks — session cards, panels, form containers.
 */
export default function Card({ children, className = "", ...props }) {
  return (
    <div
      className={`
        rounded-xl border border-ink-700 bg-ink-800/60 backdrop-blur-sm
        p-6 ${className}
      `}
      {...props}
    >
      {children}
    </div>
  );
}