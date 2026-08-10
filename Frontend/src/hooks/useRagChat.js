import { useState, useCallback } from "react";
import ragApi from "../services/ragApi";
import { parseApiError } from "../utils/errorHandler";

export const useRagChat = () => {
  const [searchResults, setSearchResults] = useState([]);
  const [sourceDetail, setSourceDetail] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const searchKnowledge = useCallback(async (query, topK = 5) => {
    setLoading(true);
    setError(null);
    try {
      const results = await ragApi.searchDocuments(query, topK);
      setSearchResults(results);
      return results;
    } catch (err) {
      const msg = parseApiError(err);
      setError(msg);
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchSourceDetail = useCallback(async (documentId) => {
    setLoading(true);
    setError(null);
    try {
      const detail = await ragApi.getDocumentSource(documentId);
      setSourceDetail(detail);
      return detail;
    } catch (err) {
      const msg = parseApiError(err);
      setError(msg);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    searchResults,
    sourceDetail,
    loading,
    error,
    searchKnowledge,
    fetchSourceDetail,
  };
};

export default useRagChat;