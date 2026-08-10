// src/pages/DocumentsPage.jsx
import { useState } from 'react';
import PageContainer from '../components/layout/PageContainer';
import DocumentUploader from '../components/documents/DocumentUploader';
import DocumentList from '../components/documents/DocumentList';
import DocumentSearch from '../components/documents/DocumentSearch';
import IngestionStatus from '../components/documents/IngestionStatus';
import { useDocuments } from '../hooks/useDocuments';

export default function DocumentsPage() {
  const { documents, loading, uploadDocument, refreshDocuments } = useDocuments();
  const [searchQuery, setSearchQuery] = useState('');

  const filteredDocs = documents.filter((doc) =>
    doc.filename?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    doc.title?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <PageContainer title="Dokumen Knowledge Base" subtitle="Kelola berkas referensi RAG untuk meningkatkan akurasi jawaban AI Assistant.">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <DocumentUploader onUploadSuccess={refreshDocuments} onUpload={uploadDocument} />
          <IngestionStatus />
        </div>
        <div className="lg:col-span-2 space-y-6">
          <DocumentSearch value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} />
          <DocumentList documents={filteredDocs} loading={loading} onDeleteSuccess={refreshDocuments} />
        </div>
      </div>
    </PageContainer>
  );
}