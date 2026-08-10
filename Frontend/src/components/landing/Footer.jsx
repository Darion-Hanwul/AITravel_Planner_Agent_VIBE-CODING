import "react";
import { Link } from "react-router-dom";
import { Compass } from "lucide-react";

export const Footer = () => {
  return (
    <footer className="bg-slate-950 border-t border-slate-800/80 py-12 px-6 lg:px-12 text-xs text-slate-500">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-emerald-600 text-white">
            <Compass className="w-4 h-4" />
          </div>
          <span className="font-bold text-sm text-slate-200">Travel AI Assistant</span>
        </div>

        <p className="text-center md:text-left">
          &copy; {new Date().getFullYear()} Travel AI Platform. All rights reserved.
        </p>

        <div className="flex items-center gap-6">
          <Link to="/chat" className="hover:text-slate-300 transition-colors">
            AI Assistant
          </Link>
          <Link to="/destinations" className="hover:text-slate-300 transition-colors">
            Destinasi
          </Link>
          <Link to="/documents" className="hover:text-slate-300 transition-colors">
            Dokumen
          </Link>
        </div>
      </div>
    </footer>
  );
};

export default Footer;