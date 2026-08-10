import "react";
import { MessageSquare, Trash2 } from "lucide-react";

export const ChatSessionItem = ({
  session,
  isActive,
  onSelect,
  onDelete,
}) => {
  return (
    <div
      onClick={() => onSelect(session.id)}
      className={`flex items-center justify-between p-2.5 rounded-xl cursor-pointer text-xs transition-colors group ${
        isActive
          ? "bg-slate-800 text-emerald-400 font-medium"
          : "text-slate-400 hover:bg-slate-900 hover:text-slate-200"
      }`}
    >
      <div className="flex items-center gap-2 truncate pr-2">
        <MessageSquare className="w-4 h-4 shrink-0" />
        <span className="truncate">{session.title || "Sesi Obrolan"}</span>
      </div>
      {onDelete && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            onDelete(session.id);
          }}
          className="p-1 text-slate-500 hover:text-rose-400 opacity-0 group-hover:opacity-100 transition-opacity"
        >
          <Trash2 className="w-3.5 h-3.5" />
        </button>
      )}
    </div>
  );
};

export default ChatSessionItem;