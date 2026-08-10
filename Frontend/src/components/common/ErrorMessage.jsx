import { AlertCircle, RefreshCw } from "lucide-react";
import Button from "./Button";

export const ErrorMessage = ({
  title = "Terjadi Kesalahan",
  message,
  onRetry,
  className = "",
}) => {
  return (
    <div
      className={`p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 flex flex-col gap-3 ${className}`}
    >
      <div className="flex items-start gap-3">
        <AlertCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
        <div className="flex-1">
          <h4 className="text-sm font-semibold text-rose-200">{title}</h4>
          {message && <p className="text-xs text-rose-300/80 mt-1">{message}</p>}
        </div>
      </div>
      {onRetry && (
        <div className="self-end">
          <Button size="sm" variant="danger" onClick={onRetry}>
            <RefreshCw className="w-3.5 h-3.5 mr-1.5" />
            Coba Lagi
          </Button>
        </div>
      )}
    </div>
  );
};

export default ErrorMessage;