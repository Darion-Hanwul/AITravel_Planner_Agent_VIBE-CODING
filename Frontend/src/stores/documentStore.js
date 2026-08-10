class DocumentStore {
  constructor() {
    this.listeners = new Set();
    this.documents = [];
    this.selectedDocument = null;
    this.searchResults = [];
    this.loading = false;
    this.uploadProgress = 0;
    this.isUploading = false;
    this.error = null;
    this.ingestionStatus = null; // { status: 'idle'|'processing'|'success'|'failed', message: string }
  }

  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  notify() {
    this.listeners.forEach((listener) => listener());
  }

  setDocuments(docs) {
    this.documents = Array.isArray(docs) ? docs : [];
    this.notify();
  }

  setSelectedDocument(doc) {
    this.selectedDocument = doc;
    this.notify();
  }

  setSearchResults(results) {
    this.searchResults = Array.isArray(results) ? results : [];
    this.notify();
  }

  setLoading(loading) {
    this.loading = Boolean(loading);
    this.notify();
  }

  setUploadProgress(progress) {
    this.uploadProgress = Number(progress);
    this.notify();
  }

  setIsUploading(isUploading) {
    this.isUploading = Boolean(isUploading);
    this.notify();
  }

  setError(error) {
    this.error = error;
    this.notify();
  }

  setIngestionStatus(status) {
    this.ingestionStatus = status;
    this.notify();
  }

  addDocument(doc) {
    this.documents = [doc, ...this.documents];
    this.notify();
  }

  removeDocument(docId) {
    this.documents = this.documents.filter(
      (d) => (d.id || d.document_id) !== docId
    );
    this.notify();
  }
}

export const documentStore = new DocumentStore();
export default documentStore;