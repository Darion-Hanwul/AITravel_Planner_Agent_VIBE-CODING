import { useState } from "react";
import Input from "../common/Input";
import TextArea from "../common/TextArea";
import Button from "../common/Button";

export const AddActivityForm = ({ onAdd, onCancel }) => {
  const [activity, setActivity] = useState({
    time: "09:00",
    title: "",
    location: "",
    notes: "",
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!activity.title) return;
    onAdd(activity);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3 p-4 bg-slate-950 rounded-xl border border-slate-800">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <Input
          label="Waktu"
          type="time"
          value={activity.time}
          onChange={(e) => setActivity({ ...activity, time: e.target.value })}
        />
        <Input
          label="Lokasi"
          placeholder="Misal: Pantai Kuta"
          value={activity.location}
          onChange={(e) => setActivity({ ...activity, location: e.target.value })}
        />
      </div>
      <Input
        label="Nama Kegiatan"
        placeholder="Misal: Sarapan & Foto Sunrise"
        value={activity.title}
        onChange={(e) => setActivity({ ...activity, title: e.target.value })}
        required
      />
      <TextArea
        label="Catatan Opsional"
        placeholder="Estimasi tiket, pesan transportasi..."
        rows={2}
        value={activity.notes}
        onChange={(e) => setActivity({ ...activity, notes: e.target.value })}
      />
      <div className="flex justify-end gap-2 pt-2">
        <Button type="button" variant="ghost" size="sm" onClick={onCancel}>
          Batal
        </Button>
        <Button type="submit" size="sm">
          Simpan Kegiatan
        </Button>
      </div>
    </form>
  );
};

export default AddActivityForm;