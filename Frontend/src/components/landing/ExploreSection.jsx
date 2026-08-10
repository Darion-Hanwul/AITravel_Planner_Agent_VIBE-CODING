import "react";
import { Link } from "react-router-dom";
import { Database, Search, ArrowRight, CheckCircle } from "lucide-react";
import Button from "../common/Button";

export const ExploreSection = () => {
  return (
    <section id="explore" className="py-20 px-6 lg:px-12 bg-slate-900/40 relative border-t border-slate-800/80">
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        {/* Mockup Interaktif / Visual */}
        <div className="p-6 sm:p-8 rounded-2xl bg-slate-900 border border-slate-800 relative shadow-2xl order-2 lg:order-1">
          <div className="flex items-center gap-3 pb-4 border-b border-slate-800 mb-4">
            <Database className="w-5 h-5 text-emerald-400" />
            <span className="text-xs font-semibold text-slate-200">Knowledge Base RAG Processing</span>
          </div>
          <div className="space-y-3 text-xs">
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-300 flex items-center justify-between">
              <span>PDF_Penerbangan_Garuda_Bali.pdf</span>
              <span className="text-emerald-400 font-medium">Indexed</span>
            </div>
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-300 flex items-center justify-between">
              <span>Voucher_Hotel_Ubud_2026.pdf</span>
              <span className="text-emerald-400 font-medium">Indexed</span>
            </div>
            <div className="p-4 rounded-xl bg-emerald-950/30 border border-emerald-500/30 text-emerald-200 leading-relaxed mt-4">
              <p className="font-medium text-emerald-400 mb-1">AI Output Prompt:</p>
              "Penerbangan Anda dijadwalkan tiba pukul 14:20 WITA di Ngurah Rai. Check-in hotel Ubud dapat dilakukan mulai pukul 15:00 WITA."
            </div>
          </div>
        </div>

        {/* Penjelasan Konten */}
        <div className="order-1 lg:order-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 text-xs font-semibold mb-4 border border-blue-500/20">
            <Search className="w-3.5 h-3.5" />
            <span>Pencarian Berbasis Konteks</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-bold text-slate-100 leading-tight">
            Eksplorasi Perjalanan Tanpa Batas dengan RAG Engine
          </h2>
          <p className="mt-4 text-sm text-slate-400 leading-relaxed">
            Tidak perlu lagi membaca puluhan lembar dokumen perjalanan secara manual. Cukup unggah berkas PDF atau teks Anda, dan ajukan pertanyaan langsung kepada AI.
          </p>

          <ul className="mt-6 space-y-3">
            {[
              "Memahami isi tiket, reservasi, dan brosur PDF secara otomatis",
              "Memberikan jawaban presisi tanpa risiko halusinasi informasi",
              "Sinkronisasi langsung ke dalam jadwal itinerary harian Anda",
            ].map((text, idx) => (
              <li key={idx} className="flex items-center gap-3 text-xs sm:text-sm text-slate-300">
                <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>{text}</span>
              </li>
            ))}
          </ul>

          <div className="mt-8">
            <Link to="/documents">
              <Button className="gap-2">
                <span>Kelola Dokumen Anda</span>
                <ArrowRight className="w-4 h-4" />
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ExploreSection;