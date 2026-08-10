import "react";
import { Sparkles } from "lucide-react";
import Button from "../common/Button";

export const ContinueBlockPrompt = ({ onGenerateMore }) => {
  return (
    <div className="p-4 rounded-xl bg-slate-950 border border-emerald-500/30 flex items-center justify-between gap-3 text-xs">
      <span className="text-slate-300 flex items-center gap-2">
        <Sparkles className="w-4 h-4 text-emerald-400" /> Ingin menambah rekomendasi hari berikutnya secara otomatis?
      </span>
      <Button size="sm" onClick={onGenerateMore}>
        Generate Lanjutan AI
      </Button>
    </div>
  );
};

export default ContinueBlockPrompt;