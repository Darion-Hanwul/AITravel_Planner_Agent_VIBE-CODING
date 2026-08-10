export const TRIP_STATUS = {
  PLANNED: "planned",
  ONGOING: "ongoing",
  COMPLETED: "completed",
  CANCELLED: "cancelled",
};

export const MAX_FILE_SIZE_MB = 100; // 100MB limit untuk upload dokumen RAG
export const ALLOWED_DOC_TYPES = [
  "application/pdf",
  "text/plain",
  "application/msword",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
];

export const CHAT_ROLES = {
  USER: "user",
  ASSISTANT: "assistant",
  SYSTEM: "system",
};