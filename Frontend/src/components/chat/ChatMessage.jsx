import "react";
import { User, Bot } from "lucide-react";
import SourceReference from "./SourceReference";

export const ChatMessage = ({ message }) => {
  const isUser = message.sender === "user" || message.role === "user";

  return (
    <div className={`flex items-start gap-3 my-4 ${isUser ? "flex-row-reverse" : "flex-row"}`}>
      <div
        className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 text-xs font-bold shadow-md ${
          isUser
            ? "bg-slate-800 text-slate-200 border border-slate-700"
            : "bg-gradient-to-tr from-emerald-600 to-teal-500 text-white"
        }`}
      >
        {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
      </div>

      <div
        className={`max-w-[85%] sm:max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
          isUser
            ? "bg-emerald-600 text-white rounded-tr-none shadow-lg shadow-emerald-950/20"
            : "bg-slate-900 text-slate-200 border border-slate-800 rounded-tl-none shadow-md"
        }`}
      >
        <p className="whitespace-pre-wrap break-words">{message.message_text || message.content}</p>

        {/* Sumber Referensi Dokumen RAG jika ada */}
        {message.sources && message.sources.length > 0 && (
          <SourceReference sources={message.sources} />
        )}

        {message.created_at && (
          <span
            className={`text-[10px] block mt-1.5 ${
              isUser ? "text-emerald-200 text-right" : "text-slate-500 text-left"
            }`}
          >
            {new Date(message.created_at).toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          </span>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;