import { forwardRef } from "react";

const VARIANTS = {
  primary: "bg-accent hover:bg-accent-soft text-white shadow-glow",
  secondary: "bg-ink-700 hover:bg-ink-600 text-ghost-white border border-ink-600",
  ghost: "bg-transparent hover:bg-ink-800 text-ghost-dim hover:text-ghost-white",
};

const SIZES = {
  sm: "px-3 py-1.5 text-sm",
  md: "px-4 py-2.5 text-sm",
  lg: "px-6 py-3 text-base",
};

/**
 * Shared button primitive. Use `as="button"` (default) or `as="link"`-style
 * usage isn't needed here — for navigation, wrap react-router's <Link> around
 * this or pass an onClick that navigates.
 */
const Button = forwardRef(function Button(
  { variant = "primary", size = "md", className = "", children, ...props },
  ref
) {
  return (
    <button
      ref={ref}
      className={`
        inline-flex items-center justify-center gap-2 rounded-lg font-medium
        transition-colors duration-150 disabled:opacity-40 disabled:cursor-not-allowed
        ${VARIANTS[variant]} ${SIZES[size]} ${className}
      `}
      {...props}
    >
      {children}
    </button>
  );
});

export default Button;