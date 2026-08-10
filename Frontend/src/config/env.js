const getEnv = (key, fallback = "") => {
  const value = import.meta.env[key];

  if (value === undefined || value === null || value === "") {
    return fallback;
  }

  return value;
};

export const env = {
  apiBaseUrl: getEnv("VITE_API_BASE_URL", "http://localhost:8000"),
  apiTimeout: Number(getEnv("VITE_API_TIMEOUT", "60000")),
  apiStreamTimeout: Number(getEnv("VITE_API_STREAM_TIMEOUT", "600000")),
  appName: getEnv("VITE_APP_NAME", "Travel AI"),
  appEnv: getEnv("VITE_APP_ENV", "development"),
};

export default env;