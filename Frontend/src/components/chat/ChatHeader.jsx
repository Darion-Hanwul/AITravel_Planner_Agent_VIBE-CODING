/* eslint-disable no-unused-vars */
import "react";
import { MessageSquare, Sparkles, Trash2, RefreshCw } from "lucide-react";
import Button from "../common/Button";

export const ChatHeader = ({
  sessionTitle = "Percakapan Baru",
  onClearChat,
  onNewSession,
  isStreaming = false,
}) => {
  return (
    <div className="h-16 px-6 bg-slate-900 border-b border-slate-800 flex items-center justify-between shrink-0">
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <MessageSquare className="w-5 h-5" />
        </div>
        <div>
          <h2 className="text-sm font-semibold text-slate-100 truncate max-w-[200px] sm:max-w-xs">
            {sessionTitle}
          </h2>
          <div className="flex items-center gap-1.5 text-[11px] text-slate-400">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span>AI Travel Assistant Active</span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <Button variant="outline" size="sm" onClick={onNewSession} disabled={isStreaming}>
          <Sparkles className="w-3.5 h-3.5 mr-1 text-emerald-400" />
          <span className="hidden sm:inline">Sesi Baru</span>
        </Button>
        {onClearChat && (
          <Button variant="ghost" size="sm" onClick={onClearChat} disabled={isStreaming}>
            <Trash2 className="w-4 h-4 text-slate-400 hover:text-rose-400" />
          </Button>
        )}
      </div>
    </div>
  );
};

export default ChatHeader;