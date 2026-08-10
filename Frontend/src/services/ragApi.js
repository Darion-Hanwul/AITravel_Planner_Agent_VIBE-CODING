import apiClient from "./apiClient";

export const createDocument = async (
  documentData
) => {
  const response = await apiClient.post(
    "/rag/documents",
    documentData
  );

  return response.data;
};

export const getDocuments = async () => {
  const response = await apiClient.get(
    "/rag/documents"
  );

  return response.data;
};

export const searchDocumentByTitle = async (
  title
) => {
  const response = await apiClient.get(
    "/rag/documents/search",
    {
      params: {
        title,
      },
    }
  );

  return response.data;
};

export const getDocumentsBySource = async (
  source
) => {
  const response = await apiClient.get(
    "/rag/documents/source",
    {
      params: {
        source,
      },
    }
  );

  return response.data;
};

export const getDocumentDetail = async (
  documentId
) => {
  const response = await apiClient.get(
    `/rag/documents/${documentId}`
  );

  return response.data;
};

export const deleteDocument = async (
  documentId
) => {
  await apiClient.delete(
    `/rag/documents/${documentId}`
  );
};

export default {
  createDocument,
  getDocuments,
  searchDocumentByTitle,
  getDocumentsBySource,
  getDocumentDetail,
  deleteDocument,
};