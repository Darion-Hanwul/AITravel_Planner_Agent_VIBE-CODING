import { forwardRef } from "react";

export const Input = forwardRef(
  (
    {
      label,
      error,
      icon: Icon,
      type = "text",
      className = "",
      containerClassName = "",
      ...props
    },
    ref
  ) => {
    return (
      <div className={`w-full flex flex-col gap-1.5 ${containerClassName}`}>
        {label && (
          <label className="text-xs font-medium text-slate-300">
            {label}
          </label>
        )}
        <div className="relative flex items-center">
          {Icon && (
            <div className="absolute left-3 text-slate-400 pointer-events-none">
              <Icon className="w-4 h-4" />
            </div>
          )}
          <input
            ref={ref}
            type={type}
            className={`w-full bg-slate-900 border ${
              error ? "border-rose-500 focus:ring-rose-500/30" : "border-slate-800 focus:border-emerald-500 focus:ring-emerald-500/20"
            } text-slate-100 placeholder-slate-500 rounded-lg text-sm ${
              Icon ? "pl-9" : "pl-3"
            } pr-3 py-2 outline-none transition-all duration-200 focus:ring-2 ${className}`}
            {...props}
          />
        </div>
        {error && <span className="text-xs text-rose-400">{error}</span>}
      </div>
    );
  }
);

Input.displayName = "Input";
export default Input;