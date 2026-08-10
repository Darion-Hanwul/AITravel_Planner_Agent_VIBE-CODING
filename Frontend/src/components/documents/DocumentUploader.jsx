/* eslint-disable no-unused-vars */
import { useState } from "react";
import { UploadCloud, FileText } from "lucide-react";
import DocumentUploadForm from "./DocumentUploadForm";

export const DocumentUploader = ({ onUploadFile, onUploadText, isLoading }) => {
  const [tab, setTab] = useState("file");

  const handleFileDrop = (e) => {
    e.preventDefault();
    const files = e.dataTransfer ? e.dataTransfer.files : e.target.files;
    if (files && files[0] && onUploadFile) {
      onUploadFile(files[0]);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
      <div className="flex border-b border-slate-800 mb-6 gap-4 text-xs font-semibold">
        <button
          onClick={() => setTab("file")}
          className={`pb-3 transition-colors border-b-2 ${
            tab === "file"
              ? "border-emerald-500 text-emerald-400"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          Upload Berkas (PDF/TXT)
        </button>
        <button
          onClick={() => setTab("text")}
          className={`pb-3 transition-colors border-b-2 ${
            tab === "text"
              ? "border-emerald-500 text-emerald-400"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          Input Teks Metadata Direct
        </button>
      </div>

      {tab === "file" ? (
        <div
          onDragOver={(e) => e.preventDefault()}
          onDrop={handleFileDrop}
          className="border-2 border-dashed border-slate-800 hover:border-emerald-500/50 rounded-2xl p-8 text-center transition-colors cursor-pointer bg-slate-950/50"
        >
          <input
            type="file"
            id="file-upload"
            className="hidden"
            accept=".pdf,.txt,.docx"
            onChange={handleFileDrop}
          />
          <label htmlFor="file-upload" className="cursor-pointer">
            <div className="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center mx-auto mb-3">
              <UploadCloud className="w-6 h-6" />
            </div>
            <p className="text-xs font-semibold text-slate-200">Klik atau seret berkas ke sini</p>
            <p className="text-[11px] text-slate-500 mt-1">Mendukung format PDF, TXT, DOCX hingga 10MB</p>
          </label>
        </div>
      ) : (
        <DocumentUploadForm onSubmit={onUploadText} isLoading={isLoading} />
      )}
    </div>
  );
};

export default DocumentUploader;