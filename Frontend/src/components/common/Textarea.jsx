import { forwardRef } from "react";

export const TextArea = forwardRef(
  (
    { label, error, rows = 4, className = "", containerClassName = "", ...props },
    ref
  ) => {
    return (
      <div className={`w-full flex flex-col gap-1.5 ${containerClassName}`}>
        {label && (
          <label className="text-xs font-medium text-slate-300">
            {label}
          </label>
        )}
        <textarea
          ref={ref}
          rows={rows}
          className={`w-full bg-slate-900 border ${
            error ? "border-rose-500 focus:ring-rose-500/30" : "border-slate-800 focus:border-emerald-500 focus:ring-emerald-500/20"
          } text-slate-100 placeholder-slate-500 rounded-lg text-sm p-3 outline-none transition-all duration-200 focus:ring-2 resize-y min-h-[80px] ${className}`}
          {...props}
        />
        {error && <span className="text-xs text-rose-400">{error}</span>}
      </div>
    );
  }
);

TextArea.displayName = "TextArea";
export default TextArea;