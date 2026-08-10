import apiClient from "./apiClient";

export const getHealth = async () => {
  const response = await apiClient.get(
    "/health"
  );

  return response.data;
};

export const getRootStatus = async () => {
  const response = await apiClient.get(
    "/"
  );

  return response.data;
};

export const getDatabaseTest = async () => {
  const response = await apiClient.get(
    "/db-test"
  );

  return response.data;
};

export default {
  getHealth,
  getRootStatus,
  getDatabaseTest,
};