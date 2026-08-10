import { useState } from "react";
import { Send } from "lucide-react";
import Input from "../common/Input";
import TextArea from "../common/TextArea";
import Button from "../common/Button";

export const DocumentUploadForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    title: "",
    content: "",
    category: "general",
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.title || !formData.content) return;
    onSubmit(formData);
    setFormData({ title: "", content: "", category: "general" });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Judul Dokumen / Catatan"
        placeholder="Misal: Tiket Penerbangan Bali 2026"
        value={formData.title}
        onChange={(e) => setFormData({ ...formData, title: e.target.value })}
        required
      />
      <TextArea
        label="Konten Dokumen Teks (Metadata RAG)"
        placeholder="Tempelkan atau ketik detail dokumen perjalanan di sini agar dapat diproses oleh AI RAG..."
        rows={5}
        value={formData.content}
        onChange={(e) => setFormData({ ...formData, content: e.target.value })}
        required
      />
      <Button type="submit" disabled={isLoading} className="w-full justify-center">
        <Send className="w-4 h-4 mr-1.5" /> Submit Ke RAG Engine
      </Button>
    </form>
  );
};

export default DocumentUploadForm;