import { motion } from "framer-motion";
import { GHOST_STATES, PERSONA_MOTION } from "./ghostStates";

/**
 * The reusable Ghost User mascot. Same SVG shape everywhere in the app;
 * only the animation state (and optionally persona) changes.
 *
 * state: "idle" | "running" | "foundIssue" | "done"
 * persona: optional persona id, tweaks motion speed/character while running
 * size: pixel size (square)
 */
export default function GhostAvatar({ state = "idle", persona = null, size = 120 }) {
  const config = GHOST_STATES[state] ?? GHOST_STATES.idle;
  const transition =
    state === "running" && persona && PERSONA_MOTION[persona]
      ? { ...config.transition, ...PERSONA_MOTION[persona] }
      : config.transition;

  return (
    <div
      className="relative flex items-center justify-center"
      style={{ width: size, height: size }}
      role="img"
      aria-label={`Ghost User avatar: ${config.label}`}
    >
      <div
        className="absolute inset-0 rounded-full blur-2xl opacity-40"
        style={{ background: "radial-gradient(circle, #8b5cf6, transparent 70%)" }}
      />

      <motion.svg
        viewBox="0 0 200 220"
        width={size}
        height={size}
        className="relative"
        animate={config.animate}
        transition={transition}
      >
        <path
          d="M100 10
             C 145 10 178 45 178 90
             L 178 165
             C 178 175 168 180 160 172
             C 152 164 148 164 140 172
             C 132 180 122 180 114 172
             C 106 164 94 164 86 172
             C 78 180 68 180 60 172
             C 52 164 48 164 40 172
             C 32 180 22 175 22 165
             L 22 90
             C 22 45 55 10 100 10 Z"
          fill="#f5f5f7"
          stroke="#0f1019"
          strokeWidth="4"
          strokeLinejoin="round"
        />

        <motion.ellipse
          cx="72"
          cy="95"
          rx="10"
          ry="16"
          fill="#0f1019"
          animate={{ scaleY: config.eyeScale }}
          transition={{ duration: 0.25 }}
        />
        <motion.ellipse
          cx="128"
          cy="95"
          rx="10"
          ry="16"
          fill="#0f1019"
          animate={{ scaleY: config.eyeScale }}
          transition={{ duration: 0.25 }}
        />
      </motion.svg>
    </div>
  );
}