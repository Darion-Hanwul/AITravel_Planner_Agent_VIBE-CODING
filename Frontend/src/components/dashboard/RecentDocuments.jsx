import "react";
import { FileText, Database } from "lucide-react";

export const RecentDocuments = ({ documents = [] }) => {
  return (
    <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
      <h3 className="text-base font-semibold text-slate-100 mb-4 flex items-center gap-2">
        <Database className="w-4 h-4 text-emerald-400" />
        Dokumen Knowledge Base RAG
      </h3>

      {documents.length === 0 ? (
        <p className="text-xs text-slate-500">Belum ada dokumen yang diunggah.</p>
      ) : (
        <div className="space-y-3">
          {documents.map((doc, idx) => (
            <div key={idx} className="flex items-center justify-between text-xs p-2.5 rounded-xl bg-slate-950 border border-slate-800">
              <div className="flex items-center gap-2 truncate">
                <FileText className="w-4 h-4 text-emerald-400 shrink-0" />
                <span className="text-slate-300 truncate">{doc.title || doc.filename}</span>
              </div>
              <span className="text-[10px] text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                Indexed
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RecentDocuments;