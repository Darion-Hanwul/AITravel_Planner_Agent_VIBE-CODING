import "react";
import Modal from "../common/Modal";
import IngestionStatus from "./IngestionStatus";

export const DocumentDetailModal = ({ doc, isOpen, onClose }) => {
  if (!doc) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Detail Dokumen Knowledge Base">
      <div className="space-y-4 text-xs">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div>
            <h4 className="font-bold text-slate-100 text-sm">{doc.title || doc.name}</h4>
            <span className="text-slate-500 text-[10px]">ID: {doc.id}</span>
          </div>
          <IngestionStatus status={doc.status || "indexed"} />
        </div>

        <div>
          <span className="text-slate-400 font-semibold block mb-1">Isi/Ekstraksi Teks RAG:</span>
          <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-300 max-h-60 overflow-y-auto whitespace-pre-wrap leading-relaxed">
            {doc.content || "Tidak ada rincian teks mentah."}
          </div>
        </div>
      </div>
    </Modal>
  );
};

export default DocumentDetailModal;