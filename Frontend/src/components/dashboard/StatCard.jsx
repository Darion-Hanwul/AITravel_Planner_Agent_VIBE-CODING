import "react";

export const StatCard = ({ title, value, icon: Icon, change, trend = "up" }) => {
  return (
    <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-between">
      <div>
        <span className="text-xs text-slate-400 font-medium">{title}</span>
        <h3 className="text-2xl font-bold text-slate-100 mt-1">{value}</h3>
        {change && (
          <span
            className={`text-[11px] font-medium mt-1 inline-block ${
              trend === "up" ? "text-emerald-400" : "text-rose-400"
            }`}
          >
            {change}
          </span>
        )}
      </div>
      {Icon && (
        <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <Icon className="w-6 h-6" />
        </div>
      )}
    </div>
  );
};

export default StatCard;