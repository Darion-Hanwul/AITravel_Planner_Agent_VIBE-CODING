import "react";

export const DocumentFilter = ({ currentFilter, onFilterChange }) => {
  const filters = [
    { id: "all", label: "Semua" },
    { id: "indexed", label: "Indexed" },
    { id: "processing", label: "Memproses" },
    { id: "failed", label: "Gagal" },
  ];

  return (
    <div className="flex items-center gap-1.5 bg-slate-900 border border-slate-800 p-1 rounded-xl">
      {filters.map((f) => (
        <button
          key={f.id}
          onClick={() => onFilterChange(f.id)}
          className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
            currentFilter === f.id
              ? "bg-slate-800 text-emerald-400 font-semibold"
              : "text-slate-400 hover:text-slate-200"
          }`}
        >
          {f.label}
        </button>
      ))}
    </div>
  );
};

export default DocumentFilter;