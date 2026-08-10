import userApi from "../services/userApi";

const TOKEN_KEY = "access_token";
const USER_KEY = "user_data";

class SessionStore {
  constructor() {
    this.listeners = new Set();
    this.user = this.getStoredUser();
    this.preferences = null;
    this.loading = false;
    this.error = null;

    if (typeof window !== "undefined") {
      window.addEventListener("auth:unauthorized", () => {
        this.clearSession();
      });
    }
  }

  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  notify() {
    this.listeners.forEach((listener) => listener());
  }

  getStoredUser() {
    try {
      const userStr = localStorage.getItem(USER_KEY);
      return userStr ? JSON.parse(userStr) : null;
    } catch {
      return null;
    }
  }

  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  }

  isAuthenticated() {
    return Boolean(this.getToken());
  }

  setSession(token, user = null) {
    localStorage.setItem(TOKEN_KEY, token);
    if (user) {
      this.setUser(user);
    } else {
      this.notify();
    }
  }

  setUser(user) {
    this.user = user;
    if (user) {
      localStorage.setItem(USER_KEY, JSON.stringify(user));
    } else {
      localStorage.removeItem(USER_KEY);
    }
    this.notify();
  }

  setPreferences(preferences) {
    this.preferences = preferences;
    this.notify();
  }

  clearSession() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    this.user = null;
    this.preferences = null;
    this.notify();
  }

  async fetchUserProfile() {
    if (!this.getToken()) return null;
    this.loading = true;
    this.notify();
    try {
      const data = await userApi.getMyProfile();
      this.setUser(data);
      this.loading = false;
      return data;
    } catch (err) {
      this.error = err.message || "Gagal memuat profil.";
      this.loading = false;
      this.notify();
      throw err;
    }
  }

  async fetchUserPreferences() {
    if (!this.getToken()) return null;
    try {
      const data = await userApi.getMyPreferences();
      this.setPreferences(data);
      return data;
    } catch (err) {
      console.error("Gagal mengambil preferensi:", err);
      return null;
    }
  }
}

export const sessionStore = new SessionStore();
export default sessionStore;