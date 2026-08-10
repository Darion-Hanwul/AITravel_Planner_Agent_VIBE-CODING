/* eslint-disable no-unused-vars */
// src/components/chat/ChatEmptyState.jsx
import 'react';
import { Compass, Sparkles, MessageSquare, MapPin } from 'lucide-react';

export default function ChatEmptyState({ onSelectPrompt }) {
  const suggestions = [
    'Buatkan itinerary 3 hari 2 malam di Bali untuk backpacker',
    'Rekomendasi tempat wisata tersembunyi di Labuan Bajo',
    'Berapa perkiraan anggaran liburan ke Yogyakarta selama 5 hari?',
  ];

  return (
    <div className="flex flex-col items-center justify-center h-full p-6 text-center max-w-lg mx-auto space-y-6">
      <div className="p-4 bg-teal-500/10 text-teal-400 rounded-full border border-teal-500/20">
        <Compass className="w-12 h-12" />
      </div>
      <div className="space-y-2">
        <h2 className="text-xl font-bold text-white flex items-center justify-center gap-2">
          Selamat Datang di AI Travel Assistant <Sparkles className="w-5 h-5 text-amber-400" />
        </h2>
        <p className="text-sm text-slate-400">
          Tanyakan apa saja seputar perencanaan perjalanan, rekomendasi wisata, atau estimasi anggaran liburan Anda.
        </p>
      </div>

      <div className="w-full space-y-2 text-left">
        <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
          Coba Pertanyaan Contoh:
        </p>
        {suggestions.map((item, idx) => (
          <button
            key={idx}
            onClick={() => onSelectPrompt && onSelectPrompt(item)}
            className="w-full text-left p-3 text-sm bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 hover:border-teal-500/40 rounded-lg text-slate-300 transition-all flex items-center gap-3"
          >
            <MessageSquare className="w-4 h-4 text-teal-400 flex-shrink-0" />
            <span>{item}</span>
          </button>
        ))}
      </div>
    </div>
  );
}