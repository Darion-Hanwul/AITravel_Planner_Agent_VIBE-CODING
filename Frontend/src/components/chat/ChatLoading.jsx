import "react";
import Spinner from "../common/Spinner";

export const ChatLoading = ({ message = "AI sedang menyusun jawaban..." }) => {
  return (
    <div className="flex items-center gap-2.5 text-xs text-slate-400 py-3 px-4 bg-slate-900/60 rounded-xl border border-slate-800/80 w-fit my-2">
      <Spinner size="sm" />
      <span>{message}</span>
    </div>
  );
};

export default ChatLoading;