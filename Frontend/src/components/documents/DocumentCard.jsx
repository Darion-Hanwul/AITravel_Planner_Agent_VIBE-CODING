import "react";
import { FileText, Trash2, Eye } from "lucide-react";
import IngestionStatus from "./IngestionStatus";

export const DocumentCard = ({ doc, onView, onDelete }) => {
  return (
    <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800 flex flex-col justify-between hover:border-slate-700 transition-colors">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-3 truncate">
          <div className="p-2.5 rounded-xl bg-slate-950 border border-slate-800 text-emerald-400 shrink-0">
            <FileText className="w-5 h-5" />
          </div>
          <div className="truncate">
            <h4 className="text-xs font-bold text-slate-100 truncate">{doc.title || doc.name}</h4>
            <span className="text-[10px] text-slate-500 block mt-0.5">
              {doc.created_at ? new Date(doc.created_at).toLocaleDateString() : "Baru saja"}
            </span>
          </div>
        </div>
        <IngestionStatus status={doc.status || "indexed"} />
      </div>

      <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
        <button
          onClick={() => onView(doc)}
          className="text-slate-400 hover:text-emerald-400 flex items-center gap-1 transition-colors"
        >
          <Eye className="w-3.5 h-3.5" /> Liha Detail
        </button>
        {onDelete && (
          <button
            onClick={() => onDelete(doc.id)}
            className="text-slate-500 hover:text-rose-400 transition-colors"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>
        )}
      </div>
    </div>
  );
};

export default DocumentCard;