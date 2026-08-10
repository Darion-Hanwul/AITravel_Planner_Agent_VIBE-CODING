import apiClient from "./apiClient";

export const createSavedPlace = async (placeData) => {
  const response = await apiClient.post(
    "/saved-places",
    placeData
  );

  return response.data;
};

export const getUserSavedPlaces = async () => {
  const response = await apiClient.get(
    "/saved-places"
  );

  return response.data;
};

export const searchSavedPlaces = async (keyword) => {
  const response = await apiClient.get(
    "/saved-places/search",
    {
      params: {
        keyword,
      },
    }
  );

  return response.data;
};

export const getSavedPlaceDetail = async (placeId) => {
  const response = await apiClient.get(
    `/saved-places/${placeId}`
  );

  return response.data;
};

export const updateSavedPlace = async (
  placeId,
  placeData
) => {
  const response = await apiClient.put(
    `/saved-places/${placeId}`,
    placeData
  );

  return response.data;
};

export const deleteSavedPlace = async (placeId) => {
  await apiClient.delete(
    `/saved-places/${placeId}`
  );
};

export default {
  createSavedPlace,
  getUserSavedPlaces,
  searchSavedPlaces,
  getSavedPlaceDetail,
  updateSavedPlace,
  deleteSavedPlace,
};