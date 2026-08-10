/* eslint-disable no-unused-vars */
import "react";
import { Clock, MessageSquare, FileText, Compass } from "lucide-react";

export const RecentActivities = ({ activities = [] }) => {
  return (
    <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
      <h3 className="text-base font-semibold text-slate-100 mb-4 flex items-center gap-2">
        <Clock className="w-4 h-4 text-emerald-400" />
        Aktivitas Terakhir
      </h3>

      {activities.length === 0 ? (
        <p className="text-xs text-slate-500">Belum ada aktivitas tercatat.</p>
      ) : (
        <div className="space-y-3">
          {activities.map((act, index) => (
            <div key={index} className="flex items-center justify-between text-xs py-2 border-b border-slate-800/60 last:border-0">
              <div className="flex items-center gap-2.5">
                <MessageSquare className="w-4 h-4 text-emerald-400 shrink-0" />
                <span className="text-slate-300 truncate">{act.title}</span>
              </div>
              <span className="text-slate-500 text-[10px] shrink-0">{act.time}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RecentActivities;