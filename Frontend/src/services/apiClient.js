import axios from "axios";
import env from "../config/env";

const apiClient = axios.create({
  baseURL: env.apiBaseUrl,
  timeout: env.apiTimeout,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

// ============================================================
// REQUEST INTERCEPTOR
// Menambahkan JWT otomatis ke setiap request terproteksi
// ============================================================

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// ============================================================
// RESPONSE INTERCEPTOR
// Menangani response dan error secara global
// ============================================================

apiClient.interceptors.response.use(
  (response) => {
    return response;
  },

  (error) => {
    if (!error.response) {
      return Promise.reject({
        ...error,
        message:
          "Tidak dapat terhubung ke server. Periksa koneksi atau pastikan backend sedang berjalan.",
      });
    }

    const { status, data } = error.response;

    if (status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
    }

    return Promise.reject({
      ...error,
      status,
      message:
        data?.detail ||
        data?.message ||
        "Terjadi kesalahan pada server.",
    });
  }
);

export default apiClient;