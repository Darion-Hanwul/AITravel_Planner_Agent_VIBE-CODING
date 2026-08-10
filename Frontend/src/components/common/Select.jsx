import { forwardRef } from "react";

export const Select = forwardRef(
  (
    { label, error, options = [], className = "", containerClassName = "", ...props },
    ref
  ) => {
    return (
      <div className={`w-full flex flex-col gap-1.5 ${containerClassName}`}>
        {label && (
          <label className="text-xs font-medium text-slate-300">
            {label}
          </label>
        )}
        <select
          ref={ref}
          className={`w-full bg-slate-900 border ${
            error ? "border-rose-500 focus:ring-rose-500/30" : "border-slate-800 focus:border-emerald-500 focus:ring-emerald-500/20"
          } text-slate-100 rounded-lg text-sm px-3 py-2 outline-none transition-all duration-200 focus:ring-2 cursor-pointer ${className}`}
          {...props}
        >
          {options.map((opt) => (
            <option key={opt.value} value={opt.value} className="bg-slate-900 text-slate-100">
              {opt.label}
            </option>
          ))}
        </select>
        {error && <span className="text-xs text-rose-400">{error}</span>}
      </div>
    );
  }
);

Select.displayName = "Select";
export default Select;