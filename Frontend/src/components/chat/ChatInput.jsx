import { useState } from "react";
import { Send } from "lucide-react";

export const ChatInput = ({ onSendMessage, disabled = false }) => {
  const [text, setText] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!text.trim() || disabled) return;

    // Keamanan: pastikan onSendMessage adalah fungsi sebelum dipanggil
    if (typeof onSendMessage === "function") {
      onSendMessage(text);
      setText("");
    } else {
      console.error("onSendMessage callback belum dioper ke ChatInput!");
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="p-3 sm:p-4 bg-slate-950 border-t border-slate-800 flex items-center gap-2 shrink-0"
    >
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ketik pesan atau pertanyaan liburan Anda..."
        rows={1}
        disabled={disabled}
        className="flex-1 bg-slate-900 border border-slate-800 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-500 outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500/30 resize-none max-h-32 disabled:opacity-50"
      />
      <button
        type="submit"
        disabled={!text.trim() || disabled}
        className="p-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl transition-all disabled:opacity-40 shrink-0 shadow-lg shadow-emerald-950/30 cursor-pointer disabled:cursor-not-allowed"
      >
        <Send className="w-5 h-5" />
      </button>
    </form>
  );
};

export default ChatInput;