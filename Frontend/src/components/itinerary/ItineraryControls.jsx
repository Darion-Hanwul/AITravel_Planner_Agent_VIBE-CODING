import "react";
import { Calendar, Plus, Download, Save } from "lucide-react";
import Button from "../common/Button";

export const ItineraryControls = ({ onAddActivity, onExportPDF, onSave }) => {
  return (
    <div className="flex flex-wrap items-center justify-between gap-3 p-4 bg-slate-900 border border-slate-800 rounded-2xl mb-6">
      <div className="flex items-center gap-2">
        <Calendar className="w-5 h-5 text-emerald-400" />
        <h3 className="text-sm font-bold text-slate-100">Itinerary Planner</h3>
      </div>
      <div className="flex items-center gap-2">
        <Button size="sm" variant="outline" onClick={onAddActivity}>
          <Plus className="w-3.5 h-3.5 mr-1" /> Tambah Kegiatan
        </Button>
        <Button size="sm" variant="secondary" onClick={onExportPDF}>
          <Download className="w-3.5 h-3.5 mr-1" /> Ekspor PDF
        </Button>
        <Button size="sm" onClick={onSave}>
          <Save className="w-3.5 h-3.5 mr-1" /> Simpan
        </Button>
      </div>
    </div>
  );
};

export default ItineraryControls;