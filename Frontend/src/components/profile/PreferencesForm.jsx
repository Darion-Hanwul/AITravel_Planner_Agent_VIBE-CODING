// src/components/profile/PreferencesForm.jsx
import { useState } from 'react';

export default function PreferencesForm() {
  const [preferences, setPreferences] = useState({
    travelStyle: 'adventure',
    budget: 'medium',
    pace: 'moderate',
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Preferensi berhasil disimpan!');
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <h3 className="text-lg font-semibold text-white mb-4">Preferensi Perjalanan AI</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm text-slate-300 mb-1">Gaya Perjalanan</label>
          <select
            value={preferences.travelStyle}
            onChange={(e) => setPreferences({ ...preferences, travelStyle: e.target.value })}
            className="w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 focus:outline-none focus:border-teal-500"
          >
            <option value="adventure">Petualangan & Alam</option>
            <option value="cultural">Budaya & Sejarah</option>
            <option value="relaxation">Santai & Kuliner</option>
          </select>
        </div>

        <div>
          <label className="block text-sm text-slate-300 mb-1">Kategori Anggaran</label>
          <select
            value={preferences.budget}
            onChange={(e) => setPreferences({ ...preferences, budget: e.target.value })}
            className="w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 focus:outline-none focus:border-teal-500"
          >
            <option value="budget">Hemat / Backpacker</option>
            <option value="medium">Menengah / Standar</option>
            <option value="luxury">Mewah / Premium</option>
          </select>
        </div>

        <button
          type="submit"
          className="w-full bg-teal-600 hover:bg-teal-500 text-white font-medium py-2.5 rounded-lg transition-colors"
        >
          Simpan Preferensi
        </button>
      </form>
    </div>
  );
}