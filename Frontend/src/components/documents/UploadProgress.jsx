import "react";
import ProgressBar from "../common/ProgressBar";

export const UploadProgress = ({ progress = 0, fileName = "File" }) => {
  return (
    <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
      <div className="flex justify-between text-xs text-slate-300">
        <span className="truncate max-w-[200px]">{fileName}</span>
        <span className="text-emerald-400 font-semibold">{progress}%</span>
      </div>
      <ProgressBar progress={progress} />
    </div>
  );
};

export default UploadProgress;