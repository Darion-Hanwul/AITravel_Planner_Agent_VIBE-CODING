import "react";
import { Zap, Shield, Cpu, Clock } from "lucide-react";

const reasons = [
  {
    icon: Zap,
    title: "Sangat Cepat",
    description: "Menyusun itinerary perjalanan komprehensif dalam hitungan detik.",
  },
  {
    icon: Cpu,
    title: "Teknologi RAG Modern",
    description: "Jawaban AI akurat berbasis data dari dokumen perjalanan asli Anda.",
  },
  {
    icon: Clock,
    title: "Hemat Waktu 90%",
    description: "Eliminasi proses riset manual dan perbandingan jadwal yang rumit.",
  },
  {
    icon: Shield,
    title: "Aman & Privat",
    description: "Seluruh data sesi obrolan dan dokumen terenkripsi dengan aman.",
  },
];

export const WhyChooseUs = () => {
  return (
    <section className="py-20 px-6 lg:px-12 bg-slate-950">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-100">
            Mengapa Memilih Travel AI?
          </h2>
          <p className="mt-3 text-sm text-slate-400 max-w-xl mx-auto">
            Keunggulan utama platform kami dalam memberikan pengalaman perencanaan perjalanan terbaik.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {reasons.map((item, index) => {
            const Icon = item.icon;
            return (
              <div
                key={index}
                className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 text-center hover:border-slate-700 transition-colors"
              >
                <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center mx-auto mb-4">
                  <Icon className="w-5 h-5" />
                </div>
                <h3 className="text-base font-semibold text-slate-100 mb-2">{item.title}</h3>
                <p className="text-xs text-slate-400 leading-relaxed">{item.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default WhyChooseUs;