import { MAX_FILE_SIZE_MB, ALLOWED_DOC_TYPES } from "./constants";

export const validateDocumentFile = (file) => {
  if (!file) {
    return { isValid: false, error: "File tidak boleh kosong." };
  }

  const maxBytes = MAX_FILE_SIZE_MB * 1024 * 1024;
  if (file.size > maxBytes) {
    return {
      isValid: false,
      error: `Ukuran file melebihi batas maksimal (${MAX_FILE_SIZE_MB}MB).`,
    };
  }

  if (!ALLOWED_DOC_TYPES.includes(file.type) && !file.name.endsWith(".txt") && !file.name.endsWith(".pdf")) {
    return {
      isValid: false,
      error: "Format file tidak didukung. Gunakan PDF, TXT, atau DOCX.",
    };
  }

  return { isValid: true, error: null };
};