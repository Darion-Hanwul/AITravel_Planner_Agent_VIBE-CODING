import "react";
import { Clock, MapPin, Trash2 } from "lucide-react";

export const ItineraryBlock = ({ activity, onDelete }) => {
  return (
    <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 flex items-start justify-between gap-3 hover:border-slate-700 transition-colors">
      <div className="space-y-1">
        <div className="flex items-center gap-2 text-xs">
          <span className="font-semibold text-emerald-400 flex items-center gap-1">
            <Clock className="w-3.5 h-3.5" /> {activity.time}
          </span>
          {activity.location && (
            <span className="text-slate-400 flex items-center gap-1">
              • <MapPin className="w-3 h-3 text-slate-500" /> {activity.location}
            </span>
          )}
        </div>
        <h4 className="text-xs font-bold text-slate-100">{activity.title}</h4>
        {activity.notes && <p className="text-[11px] text-slate-400 mt-1">{activity.notes}</p>}
      </div>

      {onDelete && (
        <button
          onClick={() => onDelete(activity.id)}
          className="text-slate-500 hover:text-rose-400 transition-colors p-1"
        >
          <Trash2 className="w-3.5 h-3.5" />
        </button>
      )}
    </div>
  );
};

export default ItineraryBlock;