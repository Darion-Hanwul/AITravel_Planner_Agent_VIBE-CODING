import "react";
import ItineraryBlock from "./ItineraryBlock";

export const ItineraryDay = ({ dayNumber = 1, activities = [], onDeleteActivity }) => {
  return (
    <div className="space-y-3">
      <h3 className="text-xs font-bold text-emerald-400 uppercase tracking-wider bg-emerald-500/10 px-3 py-1.5 rounded-lg border border-emerald-500/20 w-fit">
        Hari Ke-{dayNumber}
      </h3>
      <div className="space-y-2 pl-2 border-l-2 border-slate-800">
        {activities.length === 0 ? (
          <p className="text-xs text-slate-500 italic py-2 pl-2">Belum ada agenda kegiatan.</p>
        ) : (
          activities.map((act, i) => (
            <ItineraryBlock key={act.id || i} activity={act} onDelete={onDeleteActivity} />
          ))
        )}
      </div>
    </div>
  );
};

export default ItineraryDay;