import apiClient from "./apiClient";

/**
 * Mengambil profil pengguna yang sedang login
 *
 * Backend:
 * GET /users/me
 */
export const getMyProfile = async () => {
  const response = await apiClient.get("/users/me");

  return response.data;
};

/**
 * Memperbarui profil pengguna
 *
 * Backend:
 * PUT /users/me
 */
export const updateMyProfile = async (userData) => {
  const response = await apiClient.put(
    "/users/me",
    userData
  );

  return response.data;
};

/**
 * Memperbarui avatar pengguna
 *
 * Backend:
 * PATCH /users/me/avatar
 *
 * Backend menerima:
 * avatar_url: str
 */
export const updateMyAvatar = async (avatarUrl) => {
  const response = await apiClient.patch(
    "/users/me/avatar",
    null,
    {
      params: {
        avatar_url: avatarUrl,
      },
    }
  );

  return response.data;
};

/**
 * Mengambil preferensi pengguna
 *
 * Backend:
 * GET /users/me/preferences
 */
export const getMyPreferences = async () => {
  const response = await apiClient.get(
    "/users/me/preferences"
  );

  return response.data;
};

/**
 * Memperbarui preferensi pengguna
 *
 * Backend:
 * PUT /users/me/preferences
 */
export const updateMyPreferences = async (preferencesData) => {
  const response = await apiClient.put(
    "/users/me/preferences",
    preferencesData
  );

  return response.data;
};

export default {
  getMyProfile,
  updateMyProfile,
  updateMyAvatar,
  getMyPreferences,
  updateMyPreferences,
};