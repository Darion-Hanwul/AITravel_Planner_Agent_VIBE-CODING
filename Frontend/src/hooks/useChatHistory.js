import { useState, useCallback } from "react";
import historyApi from "../services/historyApi";
import { parseApiError } from "../utils/errorHandler";

export const useChatHistory = (sessionId) => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchHistory = useCallback(async () => {
    if (!sessionId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await historyApi.getChatHistory(sessionId);
      setHistory(data);
    } catch (err) {
      setError(parseApiError(err));
    } finally {
      setLoading(false);
    }
  }, [sessionId]);

  const clearHistory = useCallback(async () => {
    if (!sessionId) return;
    setLoading(true);
    setError(null);
    try {
      await historyApi.clearChatHistory(sessionId);
      setHistory([]);
    } catch (err) {
      setError(parseApiError(err));
    } finally {
      setLoading(false);
    }
  }, [sessionId]);

  return {
    history,
    loading,
    error,
    fetchHistory,
    clearHistory,
  };
};

export default useChatHistory;