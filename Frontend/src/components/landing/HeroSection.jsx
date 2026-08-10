import  "react";
import { Link } from "react-router-dom";
import { Sparkles, ArrowRight, ShieldCheck, Compass, MapPin } from "lucide-react";
import Button from "../common/Button";

export const HeroSection = () => {
  return (
    <section className="relative pt-32 pb-20 px-6 lg:px-12 flex flex-col items-center text-center overflow-hidden bg-slate-950">
      {/* Background Glow Overlay */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-emerald-500/10 blur-[120px] rounded-full pointer-events-none" />

      {/* Hero Badge */}
      <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold mb-6">
        <Sparkles className="w-4 h-4" />
        <span>Next-Gen AI Travel Assistant & RAG Engine</span>
      </div>

      {/* Main Title */}
      <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-100 tracking-tight max-w-4xl leading-tight">
        Rencanakan Petualangan Impian Anda Secara{" "}
        <span className="bg-gradient-to-r from-emerald-400 to-teal-300 bg-clip-text text-transparent">
          Cerdas & Otomatis
        </span>
      </h1>

      {/* Subtitle */}
      <p className="mt-6 text-base sm:text-lg text-slate-400 max-w-2xl leading-relaxed">
        Gunakan kecerdasan buatan berbasis Retrieval-Augmented Generation (RAG) untuk menyusun itinerary kustom, mengeksplorasi destinasi tersembunyi, dan mengelola dokumen perjalanan Anda.
      </p>

      {/* Action Buttons */}
      <div className="mt-8 flex flex-wrap justify-center gap-4">
        <Link to="/chat">
          <Button size="lg" className="px-8 font-semibold shadow-xl shadow-emerald-950/50">
            Mulai Percakapan AI
            <ArrowRight className="w-5 h-5 ml-1" />
          </Button>
        </Link>
        <a href="#explore">
          <Button variant="secondary" size="lg" className="px-8">
            Eksplorasi Destinasi
          </Button>
        </a>
      </div>

      {/* Feature Highlights Minimal */}
      <div className="mt-16 flex flex-wrap justify-center items-center gap-6 sm:gap-10 text-xs font-medium text-slate-400 border-t border-slate-800/80 pt-8 w-full max-w-4xl">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <span>Privasi Data Terjamin</span>
        </div>
        <div className="flex items-center gap-2">
          <Compass className="w-4 h-4 text-emerald-400" />
          <span>Rekomendasi Real-time</span>
        </div>
        <div className="flex items-center gap-2">
          <MapPin className="w-4 h-4 text-emerald-400" />
          <span>Itinerary Kustom Sesuai Budget</span>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;