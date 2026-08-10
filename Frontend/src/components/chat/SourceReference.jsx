/* eslint-disable no-unused-vars */
import "react";
import { FileText, ExternalLink } from "lucide-react";

export const SourceReference = ({ sources = [] }) => {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-3 pt-3 border-t border-slate-800/80 text-xs">
      <span className="text-[11px] font-semibold text-emerald-400 block mb-1.5">
        Sumber RAG Knowledge Base:
      </span>
      <div className="flex flex-wrap gap-1.5">
        {sources.map((src, idx) => (
          <div
            key={idx}
            className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-950 border border-slate-800 text-slate-300 text-[11px]"
          >
            <FileText className="w-3 h-3 text-emerald-400 shrink-0" />
            <span className="truncate max-w-[150px]">{src.document_name || src.title || "Dokumen"}</span>
            {src.score && (
              <span className="text-slate-500 text-[10px]">
                ({Math.round(src.score * 100)}%)
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default SourceReference;