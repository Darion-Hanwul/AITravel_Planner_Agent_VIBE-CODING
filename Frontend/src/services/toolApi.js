import apiClient from "./apiClient";

export const getToolLogsByTrip = async (tripId) => {
  const response = await apiClient.get(
    `/tools/logs/trip/${tripId}`
  );

  return response.data;
};

export const getToolLogsByFilter = async ({
  toolName = null,
  statusType = null,
} = {}) => {
  const params = {};

  if (toolName) {
    params.tool_name = toolName;
  }

  if (statusType) {
    params.status_type = statusType;
  }

  const response = await apiClient.get(
    "/tools/logs/filter",
    {
      params,
    }
  );

  return response.data;
};

export const getToolLog = async (logId) => {
  const response = await apiClient.get(
    `/tools/logs/${logId}`
  );

  return response.data;
};

export default {
  getToolLogsByTrip,
  getToolLogsByFilter,
  getToolLog,
};