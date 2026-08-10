import { useState, useCallback } from "react";
import ragApi from "../services/ragApi";
import documentStore from "../stores/documentStore";
import { validateDocumentFile } from "../utils/validateFile";
import { parseApiError } from "../utils/errorHandler";

export const useDocumentUpload = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);

  const uploadDocument = useCallback(async (file, metadata = {}) => {
    const validation = validateDocumentFile(file);
    if (!validation.isValid) {
      setError(validation.error);
      throw new Error(validation.error);
    }

    setIsUploading(true);
    documentStore.setIsUploading(true);
    setProgress(10);
    setError(null);

    try {
      const docPayload = {
        title: metadata.title || file.name,
        filename: file.name,
        file_size: file.size,
        file_type: file.type,
        ...metadata,
      };

      setProgress(50);
      const createdDoc = await ragApi.createDocument(docPayload);
      setProgress(100);
      documentStore.addDocument(createdDoc);
      return createdDoc;
    } catch (err) {
      const msg = parseApiError(err);
      setError(msg);
      throw err;
    } finally {
      setIsUploading(false);
      documentStore.setIsUploading(false);
      setTimeout(() => setProgress(0), 1000);
    }
  }, []);

  return {
    isUploading,
    progress,
    error,
    uploadDocument,
  };
};

export default useDocumentUpload;