import "react";
import { FileText, Eye, Trash2 } from "lucide-react";
import IngestionStatus from "./IngestionStatus";

export const DocumentTable = ({ documents = [], onView, onDelete }) => {
  return (
    <div className="overflow-x-auto bg-slate-900 border border-slate-800 rounded-2xl">
      <table className="w-full text-left text-xs text-slate-300">
        <thead className="bg-slate-950 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
          <tr>
            <th className="py-3.5 px-4">Nama Dokumen</th>
            <th className="py-3.5 px-4">Status Ingestion</th>
            <th className="py-3.5 px-4">Tanggal Upload</th>
            <th className="py-3.5 px-4 text-right">Aksi</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800/80">
          {documents.map((doc) => (
            <tr key={doc.id} className="hover:bg-slate-800/40 transition-colors">
              <td className="py-3 px-4 flex items-center gap-2.5 font-medium text-slate-100">
                <FileText className="w-4 h-4 text-emerald-400 shrink-0" />
                <span className="truncate max-w-[200px] sm:max-w-xs">{doc.title || doc.name}</span>
              </td>
              <td className="py-3 px-4">
                <IngestionStatus status={doc.status || "indexed"} />
              </td>
              <td className="py-3 px-4 text-slate-400">
                {doc.created_at ? new Date(doc.created_at).toLocaleDateString() : "-"}
              </td>
              <td className="py-3 px-4 text-right space-x-2">
                <button
                  onClick={() => onView(doc)}
                  className="p-1.5 hover:bg-slate-800 rounded text-slate-400 hover:text-emerald-400 transition-colors"
                >
                  <Eye className="w-4 h-4" />
                </button>
                {onDelete && (
                  <button
                    onClick={() => onDelete(doc.id)}
                    className="p-1.5 hover:bg-slate-800 rounded text-slate-400 hover:text-rose-400 transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DocumentTable;