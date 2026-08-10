import "react";
import DocumentCard from "./DocumentCard";
import DocumentTable from "./DocumentTable";

export const DocumentList = ({ documents = [], viewMode = "grid", onView, onDelete }) => {
  if (documents.length === 0) {
    return (
      <div className="text-center py-12 bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <p className="text-xs text-slate-400">Belum ada dokumen yang tersedia di Knowledge Base.</p>
      </div>
    );
  }

  if (viewMode === "table") {
    return <DocumentTable documents={documents} onView={onView} onDelete={onDelete} />;
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {documents.map((doc) => (
        <DocumentCard key={doc.id} doc={doc} onView={onView} onDelete={onDelete} />
      ))}
    </div>
  );
};

export default DocumentList;