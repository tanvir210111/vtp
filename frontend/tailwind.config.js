/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: {
          light: "#FFFFFF",
          dark: "#0B1120",
        },
        surface: {
          light: "#F8FAFC",
          dark: "#111827",
        },
        primary: {
          DEFAULT: "#2563EB",
          hover: "#1D4ED8",
          glow: "#60A5FA",
        },
        secondary: {
          DEFAULT: "#7C3AED",
          hover: "#6D28D9",
        },
        accent: {
          cyan: "#0891B2",
          purple: "#8B5CF6",
          amber: "#F59E0B",
        },
      },
      boxShadow: {
        soft: "0 4px 20px -2px rgba(15, 23, 42, 0.08)",
        glow: "0 0 25px -5px rgba(37, 99, 235, 0.3)",
      },
    },
  },
  plugins: [],
};
