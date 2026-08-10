import "react";
import { Calendar, Download, Share2 } from "lucide-react";
import Button from "../common/Button";

export const ItineraryControls = ({ onExport, onSave }) => {
  return (
    <div className="p-3 bg-slate-900 border-t border-slate-800 flex items-center justify-between text-xs">
      <span className="text-slate-400 flex items-center gap-1.5">
        <Calendar className="w-4 h-4 text-emerald-400" /> Opsi Itinerary AI
      </span>
      <div className="flex items-center gap-2">
        <Button variant="outline" size="sm" onClick={onExport}>
          <Download className="w-3.5 h-3.5 mr-1" /> Ekspor PDF
        </Button>
        <Button size="sm" onClick={onSave}>
          <Share2 className="w-3.5 h-3.5 mr-1" /> Simpan Itinerary
        </Button>
      </div>
    </div>
  );
};

export default ItineraryControls;