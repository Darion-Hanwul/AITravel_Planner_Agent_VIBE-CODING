/* eslint-disable react-hooks/set-state-in-effect */
/* eslint-disable no-unused-vars */
import { useState, useEffect, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import PageContainer from "../components/layout/PageContainer";
import ChatSessionList from "../components/chat/ChatSessionList";
import ChatWindow from "../components/chat/ChatWindow";
import {
  sendChatMessage,
  getChatSessionDetail,
  createChatSession,
} from "../services/chatApi";

export default function ChatPage() {
  const { sessionId } = useParams();
  const navigate = useNavigate();

  const [messages, setMessages] = useState([]);
  const [sessionTitle, setSessionTitle] = useState("Percakapan Baru");
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);

  // 1. Fetch riwayat percakapan jika ada sessionId
  const fetchSessionDetail = useCallback(async () => {
    if (!sessionId) {
      setMessages([]);
      setSessionTitle("Percakapan Baru");
      return;
    }

    try {
      setIsLoading(true);
      const data = await getChatSessionDetail(sessionId);
      setSessionTitle(data.title || "Percakapan Baru");
      
      // Sesuaikan mapping data messages sesuai response backend
      if (data.messages) {
        setMessages(
          data.messages.map((msg) => ({
            id: msg.id,
            role: msg.role, // 'user' atau 'assistant'
            content: msg.content || msg.message_text,
          }))
        );
      }
    } catch (error) {
      console.error("Gagal memuat detail sesi chat:", error);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId]);

  useEffect(() => {
    fetchSessionDetail();
  }, [fetchSessionDetail]);

  // 2. Fungsi Handler Kirim Pesan Ke AI
  const handleSendMessage = async (text) => {
    let currentSessionId = sessionId;

    try {
      setIsLoading(true);

      // Jika belum ada sesi aktif, buat sesi baru terlebih dahulu di backend
      if (!currentSessionId) {
        const newSession = await createChatSession({
          title: text.slice(0, 30) + "...",
        });
        currentSessionId = newSession.id;
        // Navigasi ke URL sesi baru tanpa mereload halaman
        navigate(`/chat/${currentSessionId}`, { replace: true });
      }

      // Tampilkan pesan user di UI secara langsung (Optimistic UI Update)
      const userMsg = { id: Date.now(), role: "user", content: text };
      setMessages((prev) => [...prev, userMsg]);

      // Kirim pesan ke Backend API
      const response = await sendChatMessage(currentSessionId, text);

      // Tambahkan respon dari AI ke UI
      const aiMsg = {
        id: Date.now() + 1,
        role: "assistant",
        content: response.reply || response.message || response.content,
      };

      setMessages((prev) => [...prev, aiMsg]);
    } catch (error) {
      console.error("Gagal mengirim pesan:", error);
      // Tampilkan notifikasi error di UI jika pesan gagal terkirim
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          role: "assistant",
          content:
            "Maaf, terjadi kesalahan saat menghubungi AI Server. Pastikan Backend dan Ollama berjalan.",
          isError: true,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // 3. Handler Buat Sesi Baru
  const handleNewSession = () => {
    navigate("/chat");
    setMessages([]);
    setSessionTitle("Percakapan Baru");
  };

  // 4. Handler Hapus/Clear Chat
  const handleClearChat = () => {
    setMessages([]);
  };

  return (
    <PageContainer fullHeight noPadding title="AI Travel Assistant">
      <div className="flex h-[calc(100vh-4rem)] overflow-hidden bg-slate-900 border-t border-slate-800">
        {/* Sidebar Daftar Sesi Chat */}
        <div className="w-80 border-r border-slate-800 hidden md:block flex-shrink-0 bg-slate-950">
          <ChatSessionList activeSessionId={sessionId} />
        </div>

        {/* Jendela Utama Chat */}
        <div className="flex-1 flex flex-col h-full bg-slate-900 overflow-hidden">
          <ChatWindow
            sessionTitle={sessionTitle}
            messages={messages}
            isLoading={isLoading}
            isStreaming={isStreaming}
            onSendMessage={handleSendMessage}
            onNewSession={handleNewSession}
            onClearChat={handleClearChat}
          />
        </div>
      </div>
    </PageContainer>
  );
}