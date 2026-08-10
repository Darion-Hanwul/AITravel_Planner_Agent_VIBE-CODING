import "react";
import { Bot } from "lucide-react";

export const StreamingMessage = ({ text = "" }) => {
  return (
    <div className="flex items-start gap-3 my-4 flex-row">
      <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 text-white flex items-center justify-center shrink-0 shadow-md">
        <Bot className="w-4 h-4" />
      </div>

      <div className="max-w-[85%] sm:max-w-[75%] rounded-2xl rounded-tl-none px-4 py-3 text-sm leading-relaxed bg-slate-900 text-slate-200 border border-slate-800 shadow-md">
        <p className="whitespace-pre-wrap break-words inline">{text}</p>
        <span className="inline-block w-2 h-4 ml-1 bg-emerald-400 animate-pulse align-middle" />
      </div>
    </div>
  );
};

export default StreamingMessage;