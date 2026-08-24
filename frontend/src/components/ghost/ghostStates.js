/**
 * Animation variants for the GhostAvatar, keyed by agent state.
 * Kept separate from the component so new states/tuning don't
 * require touching the SVG markup.
 */

export const GHOST_STATES = {
  idle: {
    label: "idle",
    animate: { y: [0, -8, 0], rotate: 0 },
    transition: { duration: 3, repeat: Infinity, ease: "easeInOut" },
    eyeScale: 1,
  },
  running: {
    label: "running",
    animate: { y: [0, -4, 0], x: [0, 3, -3, 0], rotate: 0 },
    transition: { duration: 0.9, repeat: Infinity, ease: "easeInOut" },
    eyeScale: 1,
  },
  foundIssue: {
    label: "found an issue",
    animate: { rotate: [0, -6, 6, -6, 0], y: 0 },
    transition: { duration: 0.5, ease: "easeInOut" },
    eyeScale: 1.3,
  },
  done: {
    label: "done",
    animate: { y: [0, -10, 0], rotate: 0 },
    transition: { duration: 0.6, ease: "easeOut" },
    eyeScale: 0.85, // slightly squinted/content
  },
};

// Per-persona movement personality, layered on top of the "running" state
export const PERSONA_MOTION = {
  impatient: { duration: 0.5, ease: "easeInOut" }, // fast, jittery
  confused_first_timer: { duration: 1.6, ease: "easeInOut" }, // slow, hesitant
  power_user: { duration: 0.8, ease: "linear" }, // clean, steady
};