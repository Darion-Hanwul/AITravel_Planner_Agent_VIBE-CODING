import "react";
import { Activity, ShieldCheck } from "lucide-react";

export const SystemStatus = ({ status = "Online", backendVersion = "v1.0.0 (FastAPI)" }) => {
  return (
    <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between text-xs">
      <div className="flex items-center gap-2">
        <Activity className="w-4 h-4 text-emerald-400" />
        <span className="text-slate-300 font-medium">Status Engine RAG</span>
      </div>
      <div className="flex items-center gap-2">
        <span className="inline-flex items-center gap-1 text-emerald-400 font-medium">
          <ShieldCheck className="w-3.5 h-3.5" /> {status}
        </span>
        <span className="text-slate-500">| {backendVersion}</span>
      </div>
    </div>
  );
};

export default SystemStatus;