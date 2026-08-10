import apiClient from "./apiClient";

/**
 * Registrasi pengguna baru
 * Backend:
 * POST /auth/signup
 */
export const signup = async (userData) => {
  const response = await apiClient.post("/auth/signup", userData);

  return response.data;
};

/**
 * Login pengguna
 * Backend menggunakan OAuth2PasswordRequestForm,
 * sehingga data harus dikirim sebagai application/x-www-form-urlencoded.
 *
 * Backend:
 * POST /auth/signin
 */
export const signin = async ({ email, password }) => {
  const formData = new URLSearchParams();

  formData.append("username", email);
  formData.append("password", password);

  const response = await apiClient.post(
    "/auth/signin",
    formData,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );

  return response.data;
};

/**
 * Helper untuk menyimpan token autentikasi
 */
export const saveAccessToken = (accessToken) => {
  localStorage.setItem("access_token", accessToken);
};

/**
 * Helper untuk mengambil token autentikasi
 */
export const getAccessToken = () => {
  return localStorage.getItem("access_token");
};

/**
 * Helper untuk menghapus token autentikasi
 */
export const removeAccessToken = () => {
  localStorage.removeItem("access_token");
};

/**
 * Helper untuk mengecek apakah pengguna sudah login
 */
export const isAuthenticated = () => {
  return Boolean(getAccessToken());
};