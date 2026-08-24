/** Ghost User design tokens — navy/glow theme with one accent color. */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          950: "#0f1019",
          900: "#14151f",
          800: "#1a1c2b",
          700: "#242639",
          600: "#31344a",
        },
        ghost: {
          white: "#f5f5f7",
          dim: "#9a9db3",
        },
        accent: {
          DEFAULT: "#8b5cf6", // electric violet
          soft: "#a78bfa",
          glow: "#c4b5fd",
        },
        signal: {
          low: "#4ade80",
          medium: "#facc15",
          high: "#f87171",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      boxShadow: {
        glow: "0 0 60px 10px rgba(139, 92, 246, 0.25)",
      },
      keyframes: {
        bob: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-8px)" },
        },
        wobble: {
          "0%, 100%": { transform: "rotate(0deg)" },
          "25%": { transform: "rotate(-4deg)" },
          "75%": { transform: "rotate(4deg)" },
        },
      },
      animation: {
        bob: "bob 3s ease-in-out infinite",
        wobble: "wobble 0.5s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};