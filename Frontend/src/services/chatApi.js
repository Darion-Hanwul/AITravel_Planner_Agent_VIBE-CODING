import apiClient from "./apiClient";

export const createChatSession = async (sessionData) => {
  const response = await apiClient.post(
    "/chats/sessions",
    sessionData
  );

  return response.data;
};

export const getUserChatSessions = async () => {
  const response = await apiClient.get(
    "/chats/sessions"
  );

  return response.data;
};

export const getChatSessionDetail = async (
  sessionId
) => {
  const response = await apiClient.get(
    `/chats/sessions/${sessionId}`
  );

  return response.data;
};

export const renameChatSession = async (
  sessionId,
  title
) => {
  const response = await apiClient.patch(
    `/chats/sessions/${sessionId}`,
    {
      title,
    }
  );

  return response.data;
};

export const deleteChatSession = async (
  sessionId
) => {
  await apiClient.delete(
    `/chats/sessions/${sessionId}`
  );
};

export const sendChatMessage = async (
  sessionId,
  messageText
) => {
  const response = await apiClient.post(
    `/chats/sessions/${sessionId}/messages`,
    null,
    {
      params: {
        message_text: messageText,
      },
    }
  );

  return response.data;
};

export default {
  createChatSession,
  getUserChatSessions,
  getChatSessionDetail,
  renameChatSession,
  deleteChatSession,
  sendChatMessage,
};