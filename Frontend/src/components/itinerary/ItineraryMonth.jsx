import "react";

export const ItineraryMonth = ({ title = "Perencanaan Bulanan", totalDays = 30 }) => {
  return (
    <div className="p-4 bg-slate-900 border border-slate-800 rounded-2xl text-xs text-slate-300">
      <h4 className="font-bold text-slate-100 mb-2">{title}</h4>
      <p className="text-slate-400">Total estimasi durasi trip: {totalDays} Hari.</p>
    </div>
  );
};

export default ItineraryMonth;