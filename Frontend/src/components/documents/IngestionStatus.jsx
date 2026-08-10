import "react";
import { CheckCircle2, Clock, AlertCircle } from "lucide-react";

export const IngestionStatus = ({ status = "indexed" }) => {
  switch (status.toLowerCase()) {
    case "indexed":
    case "completed":
      return (
        <span className="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-400 bg-emerald-500/10 px-2.5 py-0.5 rounded-full border border-emerald-500/20">
          <CheckCircle2 className="w-3 h-3" /> Indexed
        </span>
      );
    case "processing":
    case "pending":
      return (
        <span className="inline-flex items-center gap-1 text-[11px] font-medium text-amber-400 bg-amber-500/10 px-2.5 py-0.5 rounded-full border border-amber-500/20">
          <Clock className="w-3 h-3 animate-spin" /> Memproses
        </span>
      );
    case "failed":
      return (
        <span className="inline-flex items-center gap-1 text-[11px] font-medium text-rose-400 bg-rose-500/10 px-2.5 py-0.5 rounded-full border border-rose-500/20">
          <AlertCircle className="w-3 h-3" /> Gagal
        </span>
      );
    default:
      return null;
  }
};

export default IngestionStatus;