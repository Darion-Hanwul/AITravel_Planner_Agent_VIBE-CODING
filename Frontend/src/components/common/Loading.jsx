import Spinner from "./Spinner";

export const Loading = ({ text = "Memuat data...", fullPage = false }) => {
  const content = (
    <div className="flex flex-col items-center justify-center gap-3 p-6 text-center">
      <Spinner size="lg" />
      {text && <p className="text-xs text-slate-400 font-medium">{text}</p>}
    </div>
  );

  if (fullPage) {
    return (
      <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center">
        {content}
      </div>
    );
  }

  return content;
};

export default Loading;