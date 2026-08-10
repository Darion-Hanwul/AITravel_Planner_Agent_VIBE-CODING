import { useState, useCallback } from "react";
import documentStore from "../stores/documentStore";

export const useDocumentIngestion = () => {
  const [ingestStatus, setIngestStatus] = useState("idle"); // idle | processing | success | error
  const [statusMessage, setStatusMessage] = useState("");

  const startIngestion = useCallback((docTitle = "Dokumen") => {
    setIngestStatus("processing");
    setStatusMessage(`Sedang memproses dan mengindeks "${docTitle}"...`);
    documentStore.setIngestionStatus({ status: "processing", message: statusMessage });

    setTimeout(() => {
      setIngestStatus("success");
      setStatusMessage(`Dokumen "${docTitle}" berhasil diindeks ke Knowledge Base.`);
      documentStore.setIngestionStatus({ status: "success", message: statusMessage });
    }, 2000);
  }, [statusMessage]);

  const resetIngestion = useCallback(() => {
    setIngestStatus("idle");
    setStatusMessage("");
    documentStore.setIngestionStatus(null);
  }, []);

  return {
    ingestStatus,
    statusMessage,
    startIngestion,
    resetIngestion,
  };
};

export default useDocumentIngestion;