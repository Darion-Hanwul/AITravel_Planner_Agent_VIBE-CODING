
import "react";
import { MessageSquareText, FileText, Calendar, Sparkles } from "lucide-react";

const features = [
  {
    icon: MessageSquareText,
    title: "AI Travel Assistant",
    description:
      "Asisten interaktif berbasis AI yang memahami preference, budget, dan gaya liburan Anda secara personal.",
  },
  {
    icon: FileText,
    title: "Document Knowledge Base (RAG)",
    description:
      "Unggah tiket, voucher hotel, atau PDF panduan wisata. AI akan menjawab pertanyaan berdasarkan berkas asli Anda.",
  },
  {
    icon: Calendar,
    title: "Automatic Itinerary Builder",
    description:
      "Jadwalkan kegiatan harian dari jam ke jam lengkap dengan estimasi alokasi waktu dan urutan rute perjalanan.",
  },
];

export const TravelFeatureSection = () => {
  return (
    <section id="features" className="py-20 px-6 lg:px-12 bg-slate-900/50 border-y border-slate-800/60 relative">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-medium mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Fitur Unggulan</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-100">
            Teknologi Cerdas untuk Setiap Perjalanan
          </h2>
          <p className="mt-3 text-sm text-slate-400 max-w-xl mx-auto">
            Solusi komprehensif mulai dari perencanaan awal hingga eksekusi perjalanan liburan Anda.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {features.map((item, index) => {
            const Icon = item.icon;
            return (
              <div
                key={index}
                className="p-8 rounded-2xl bg-slate-900 border border-slate-800 hover:border-emerald-500/40 transition-all duration-300 hover:-translate-y-1 group relative overflow-hidden"
              >
                <div className="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center mb-6 group-hover:bg-emerald-500 group-hover:text-white transition-colors duration-300">
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-semibold text-slate-100 mb-2">{item.title}</h3>
                <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">{item.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default TravelFeatureSection;