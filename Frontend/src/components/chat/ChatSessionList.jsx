import "react";
import { Plus } from "lucide-react";
import Button from "../common/Button";
import ChatSessionItem from "./ChatSessionItem";

export const ChatSessionList = ({
  sessions = [],
  activeSessionId,
  onSelectSession,
  onNewSession,
  onDeleteSession,
}) => {
  return (
    <div className="flex flex-col h-full bg-slate-950 border-r border-slate-800 p-3 w-64 shrink-0">
      <Button onClick={onNewSession} className="w-full mb-3 justify-start gap-2">
        <Plus className="w-4 h-4" />
        Sesi Baru
      </Button>

      <div className="flex-1 overflow-y-auto space-y-1">
        {sessions.length === 0 ? (
          <p className="text-xs text-slate-500 text-center py-4">Belum ada riwayat sesi.</p>
        ) : (
          sessions.map((session) => (
            <ChatSessionItem
              key={session.id}
              session={session}
              isActive={session.id === activeSessionId}
              onSelect={onSelectSession}
              onDelete={onDeleteSession}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default ChatSessionList;