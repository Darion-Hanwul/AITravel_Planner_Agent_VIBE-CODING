export const generateSessionId = () => {
  if (typeof crypto !== "undefined" && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return "session-" + Date.now() + "-" + Math.random().toString(36).substring(2, 9);
};