import { useCallback } from "react";
import { useChatContext } from "../context/ChatContext";

export const useChatSession = () => {
  const {
    sessions,
    activeSessionId,
    fetchSessions,
    selectSession,
    createSession,
    deleteSession,
    startNewSession,
    error,
  } = useChatContext();

  const handleCreateSession = useCallback(
    async (title = "Percakapan Baru") => {
      return await createSession({ title });
    },
    [createSession]
  );

  return {
    sessions,
    activeSessionId,
    fetchSessions,
    selectSession,
    createSession: handleCreateSession,
    deleteSession,
    startNewSession,
    error,
  };
};

export default useChatSession;