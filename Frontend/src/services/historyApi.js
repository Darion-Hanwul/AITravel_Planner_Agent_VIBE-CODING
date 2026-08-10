import apiClient from "./apiClient";

export const getChatHistory = async (
  sessionId,
  limit = null
) => {
  const params = {};

  if (limit !== null && limit !== undefined) {
    params.limit = limit;
  }

  const response = await apiClient.get(
    `/history/${sessionId}`,
    {
      params,
    }
  );

  return response.data;
};

export const countChatMessages = async (
  sessionId
) => {
  const response = await apiClient.get(
    `/history/${sessionId}/count`
  );

  return response.data;
};

export const clearChatHistory = async (
  sessionId
) => {
  await apiClient.delete(
    `/history/${sessionId}/clear`
  );
};

export default {
  getChatHistory,
  countChatMessages,
  clearChatHistory,
};