import "react";

export const ItineraryYear = ({ year = "2026" }) => {
  return (
    <div className="p-4 bg-slate-900 border border-slate-800 rounded-2xl text-xs text-slate-400">
      Rencana Liburan Tahunan ({year})
    </div>
  );
};

export default ItineraryYear;