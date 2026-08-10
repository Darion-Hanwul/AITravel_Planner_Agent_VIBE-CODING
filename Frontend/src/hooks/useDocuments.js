/* eslint-disable react-hooks/set-state-in-effect */
import { useState, useCallback, useEffect } from "react";
import ragApi from "../services/ragApi";
import documentStore from "../stores/documentStore";
import { parseApiError } from "../utils/errorHandler";

export const useDocuments = (autoFetch = false) => {
  const [documents, setDocuments] = useState(documentStore.documents);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const unsubscribe = documentStore.subscribe(() => {
      setDocuments(documentStore.documents);
    });
    return () => unsubscribe();
  }, []);

  const fetchDocuments = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await ragApi.getDocuments();
      documentStore.setDocuments(data);
      return data;
    } catch (err) {
      const msg = parseApiError(err);
      setError(msg);
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteDocument = useCallback(async (documentId) => {
    setLoading(true);
    setError(null);
    try {
      await ragApi.deleteDocument(documentId);
      documentStore.removeDocument(documentId);
    } catch (err) {
      const msg = parseApiError(err);
      setError(msg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (autoFetch) {
      fetchDocuments();
    }
  }, [autoFetch, fetchDocuments]);

  return {
    documents,
    loading,
    error,
    fetchDocuments,
    deleteDocument,
  };
};

export default useDocuments;