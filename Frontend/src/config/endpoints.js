export const ENDPOINTS = {
  AUTH: {
    SIGNUP: "/auth/signup",
    SIGNIN: "/auth/signin",
  },
  USER: {
    ME: "/users/me",
    AVATAR: "/users/me/avatar",
    PREFERENCES: "/users/me/preferences",
  },
  TRIP: {
    BASE: "/trips",
    BY_ID: (id) => `/trips/${id}`,
    STATUS: (id) => `/trips/${id}/status`,
  },
  CALENDAR: {
    EVENTS: "/calendar/events",
    REMINDERS: "/calendar/events/reminders",
    FILTER: "/calendar/events/filter",
    BY_ID: (id) => `/calendar/events/${id}`,
  },
  CHAT: {
    SESSIONS: "/chats/sessions",
    SESSION_BY_ID: (id) => `/chats/sessions/${id}`,
    MESSAGES: (sessionId) => `/chats/sessions/${sessionId}/messages`,
  },
  HISTORY: {
    BY_SESSION: (sessionId) => `/history/${sessionId}`,
    COUNT: (sessionId) => `/history/${sessionId}/count`,
    CLEAR: (sessionId) => `/history/${sessionId}/clear`,
  },
  RAG: {
    DOCUMENTS: "/rag/documents",
    SEARCH: "/rag/documents/search",
    SOURCE: "/rag/documents/source",
    BY_ID: (id) => `/rag/documents/${id}`,
  },
  SAVED_PLACES: {
    BASE: "/saved-places",
    SEARCH: "/saved-places/search",
    BY_ID: (id) => `/saved-places/${id}`,
  },
  TOOLS: {
    LOGS_BY_TRIP: (tripId) => `/tools/logs/trip/${tripId}`,
    LOGS_FILTER: "/tools/logs/filter",
    LOG_BY_ID: (logId) => `/tools/logs/${logId}`,
  },
  SYSTEM: {
    ROOT: "/",
    HEALTH: "/health",
    DB_TEST: "/db-test",
  },
};

export default ENDPOINTS;