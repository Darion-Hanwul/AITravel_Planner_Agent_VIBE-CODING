export const THEME = {
  colors: {
    primary: {
      DEFAULT: "#10b981", // Emerald 500
      hover: "#059669",   // Emerald 600
      light: "#a7f3d0",   // Emerald 200
      dark: "#064e3b",    // Emerald 900
    },
    background: {
      main: "#020617",    // Slate 950
      card: "#0f172a",    // Slate 900
      sidebar: "#090d16",
    },
    status: {
      planned: { bg: "bg-blue-500/10", text: "text-blue-400", border: "border-blue-500/20" },
      ongoing: { bg: "bg-emerald-500/10", text: "text-emerald-400", border: "border-emerald-500/20" },
      completed: { bg: "bg-slate-500/10", text: "text-slate-400", border: "border-slate-500/20" },
      cancelled: { bg: "bg-red-500/10", text: "text-red-400", border: "border-red-500/20" },
    },
  },
  breakpoints: {
    sm: "640px",
    md: "768px",
    lg: "1024px",
    xl: "1280px",
    "2xl": "1536px",
  },
};

export default THEME;